using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.EntityFrameworkCore;

namespace CineManagement.Modules.CustomerSupport;

public sealed class CustomerSupportService(ApplicationDbContext db, OllamaIntentClient ollama, ILogger<CustomerSupportService> logger)
{
    private static readonly CultureInfo Vietnamese = CultureInfo.GetCultureInfo("vi-VN");
    private static readonly TimeZoneInfo Vietnam = TimeZoneInfo.FindSystemTimeZoneById("Asia/Ho_Chi_Minh");
    private const int ResultLimit = 8;

    public async Task<ChatReply> ReplyAsync(ChatRequest request, CancellationToken ct)
    {
        var now = TimeZoneInfo.ConvertTimeFromUtc(DateTime.UtcNow, Vietnam);
        using var deadline = CancellationTokenSource.CreateLinkedTokenSource(ct);
        deadline.CancelAfter(TimeSpan.FromSeconds(52));
        var message = request.Message.Trim();
        ChatInterpretation? interpretation = null;
        var referencedMovie = MovieByPosition(message, request.RecentMovies);
        var context = message switch
        {
            "Phim đang chiếu" => new ChatContext("movies", MovieStatus: "now"),
            "Lịch chiếu hôm nay" => new ChatContext("showtimes"),
            "Danh sách chi nhánh" => new ChatContext("cinemas"),
            "Cách đặt vé" => new ChatContext("help"),
            _ => Merge(interpretation = await ollama.InterpretAsync(
                referencedMovie is null ? request : request with { Message = message + $" (Phim được nhắc tới: {referencedMovie})" },
                now, deadline.Token), request.Context)
        };
        if (referencedMovie is not null)
        {
            var asksForShowtimes = Regex.IsMatch(message, @"\b(suất|lịch chiếu|giờ chiếu)\b", RegexOptions.IgnoreCase);
            var date = Regex.IsMatch(message, @"\b(ngày mai|mai)\b", RegexOptions.IgnoreCase)
                ? now.AddDays(1).ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)
                : context.Date;
            context = context with
            {
                Movie = referencedMovie,
                Genre = null,
                Intent = asksForShowtimes ? "showtimes" : "movies",
                Date = date
            };
        }

        var reply = context.Intent switch
        {
            "movies" => await MoviesAsync(context, now, deadline.Token),
            "showtimes" => await ShowtimesAsync(context, now, deadline.Token),
            "cinemas" => await CinemasAsync(context, deadline.Token),
            "food" => await FoodAsync(context, deadline.Token),
            "help" => new("Bạn mở trang phim, chọn suất chiếu rồi đăng nhập để chọn ghế. Sau đó bạn có thể thêm bắp nước, nhập voucher và xem tổng tiền trước khi xác nhận. Vé đã đặt nằm trong mục Lịch sử đặt vé. Với yêu cầu đổi hoặc hoàn vé, bạn có thể hỏi trực tiếp chi nhánh.", request.Context, []),
            _ => new("Mình có thể tra phim, lịch chiếu, giá vé, chi nhánh và bắp nước. Bạn muốn tìm thông tin gì?", request.Context, [])
        };

        if (context.Intent is "help" or "other" && interpretation is not null)
            return UsableAnswer(interpretation.Answer) ? reply with { Text = interpretation.Answer! } : reply;

        // A lookup can still return real data if the wording pass is slow or unavailable.
        using var wording = CancellationTokenSource.CreateLinkedTokenSource(deadline.Token);
        wording.CancelAfter(TimeSpan.FromSeconds(25));
        try
        {
            var answer = await ollama.WriteReplyAsync(request, reply, wording.Token);
            return UsableAnswer(answer) ? reply with { Text = answer } : reply;
        }
        catch (Exception ex) when (!ct.IsCancellationRequested &&
            (ex is OperationCanceledException or HttpRequestException or JsonException))
        {
            logger.LogDebug(ex, "Customer chat returned the lookup without model wording.");
            return reply;
        }
    }

    private static bool UsableAnswer(string? answer) =>
        !string.IsNullOrWhiteSpace(answer) && answer.Length <= 800;

    private static string? MovieByPosition(string message, string[]? recentMovies)
    {
        var match = Regex.Match(message, @"\bphim\s+(?:thứ\s+|số\s+)([1-8]|nhất|một|hai|ba|tư|bốn|năm|sáu|bảy|tám)\b",
            RegexOptions.IgnoreCase);
        if (!match.Success || recentMovies is null) return null;
        var position = match.Groups[1].Value.ToLowerInvariant() switch
        {
            "nhất" or "một" => 1,
            "hai" => 2,
            "ba" => 3,
            "tư" or "bốn" => 4,
            "năm" => 5,
            "sáu" => 6,
            "bảy" => 7,
            "tám" => 8,
            var digit => digit[0] - '0'
        };
        return position <= recentMovies.Length ? Filter(recentMovies[position - 1], null, 150) : null;
    }

    private static ChatContext Merge(ChatInterpretation intent, ChatContext? previous)
    {
        var last = intent.FollowUp ? previous : null;
        var movie = Filter(intent.Movie, last?.Movie, 150);
        if (movie?.ToLowerInvariant() is "phim" or "vài phim" or "các phim" or "phim đang chiếu" or "phim sắp chiếu"
            or "đang chiếu" or "sắp chiếu" or "tất cả phim")
        {
            movie = null;
        }
        return new(
            intent.Intent,
            movie,
            Filter(intent.Genre, last?.Genre, 100),
            Filter(intent.Cinema, last?.Cinema, 150),
            Filter(intent.Date, last?.Date, 10),
            Filter(intent.AfterTime, last?.AfterTime, 5),
            Filter(intent.MovieStatus, last?.MovieStatus, 12));
    }

    private static string? Filter(string? value, string? previous, int maxLength)
    {
        var result = (value ?? previous)?.Trim();
        return string.IsNullOrEmpty(result) ? null : result[..Math.Min(result.Length, maxLength)];
    }

    private IQueryable<Movie> PublicMovies(ChatContext context)
    {
        var query = db.Movies.AsNoTracking().Where(m => m.IsActive && m.Status != MovieStatus.Ended);
        if (context.Movie is { } movie)
            query = query.Where(m => m.Title.Contains(movie));
        if (context.Genre is { } genre)
            query = query.Where(m => m.Genre != null && m.Genre.Name.Contains(genre));
        return context.MovieStatus switch
        {
            "now" => query.Where(m => m.Status == MovieStatus.NowShowing),
            "upcoming" => query.Where(m => m.Status == MovieStatus.ComingSoon),
            _ => query
        };
    }

    private IQueryable<Showtime> PublicShowtimes(ChatContext context)
    {
        var movies = PublicMovies(context);
        var query = db.Showtimes.AsNoTracking().Where(s =>
            s.Status == ShowtimeStatus.Available && s.Room != null && s.Room.IsActive
            && (s.Room.Cinema == null || s.Room.Cinema.IsActive)
            && movies.Any(m => m.MovieId == s.MovieId));
        if (context.Cinema is { } cinema)
        {
            var cinemas = PublicCinemas(cinema);
            query = query.Where(s => cinemas.Any(c => c.CinemaId == s.Room!.CinemaId));
        }
        return query;
    }

    private IQueryable<Cinema> PublicCinemas(string? filter)
    {
        var query = db.Cinemas.AsNoTracking().Where(c => c.IsActive);
        return filter is null ? query : query.Where(c =>
            c.Name.Contains(filter) || c.Code == filter || c.City.Contains(filter) || c.Address.Contains(filter));
    }

    private async Task<ChatReply> MoviesAsync(ChatContext context, DateTime now, CancellationToken ct)
    {
        var movies = PublicMovies(context);
        if (context.Cinema is not null || context.Date is not null || context.AfterTime is not null)
        {
            // A branch or time filter is a request for actual showtimes, not just movie status.
            return await ShowtimesAsync(context with { Intent = "showtimes" }, now, ct);
        }

        var rows = await movies.OrderBy(m => m.Title).ThenBy(m => m.MovieId)
            .Select(m => new { m.MovieId, m.Title, Genre = m.Genre != null ? m.Genre.Name : null, m.Duration, m.Status, m.AgeRating })
            .Take(ResultLimit + 1).ToListAsync(ct);
        var items = rows.Take(ResultLimit).Select(m => new ChatItem(
            m.Title, $"{(m.Status == MovieStatus.ComingSoon ? "Sắp chiếu" : "Đang chiếu")} · {m.Genre ?? "Chưa rõ thể loại"} · {m.Duration} phút"
                + (string.IsNullOrWhiteSpace(m.AgeRating) ? "" : $" · Phân loại {m.AgeRating}"), m.MovieId
        )).ToArray();
        return Results("Mình tìm được các phim sau.", "Mình chưa tìm thấy phim phù hợp. Bạn thử tên phim hoặc thể loại khác nhé.", context, items, rows.Count);
    }

    private async Task<ChatReply> ShowtimesAsync(ChatContext context, DateTime now, CancellationToken ct)
    {
        var date = DateOnly.FromDateTime(now);
        if (context.Date is { } dateText
            && !DateOnly.TryParseExact(dateText, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out date))
            return new("Bạn muốn xem ngày nào? Bạn có thể ghi ngày theo dạng ngày/tháng/năm.", context with { Date = null }, []);

        if (date < DateOnly.FromDateTime(now))
            return new("Ngày bạn chọn đã qua. Bạn muốn xem hôm nay hay một ngày khác?", context with { Date = null }, []);
        if (date > DateOnly.FromDateTime(now.AddYears(1)))
            return new("Bạn chọn ngày trong vòng một năm tới để mình tra lịch nhé.", context with { Date = null }, []);

        var after = TimeOnly.MinValue;
        if (context.AfterTime is { } timeText
            && !TimeOnly.TryParseExact(timeText, "HH:mm", CultureInfo.InvariantCulture, DateTimeStyles.None, out after))
            return new("Bạn muốn xem từ mấy giờ?", context with { AfterTime = null }, []);

        var earliest = date.ToDateTime(after);
        var until = date.AddDays(1).ToDateTime(TimeOnly.MinValue);
        var rows = await PublicShowtimes(context)
            .Where(s => s.StartTime >= earliest && s.StartTime >= now && s.StartTime < until)
            .OrderBy(s => s.StartTime).ThenBy(s => s.ShowtimeId)
            .Select(s => new
            {
                s.ShowtimeId, s.MovieId, Title = s.Movie!.Title,
                Cinema = s.Room!.Cinema == null ? null : s.Room.Cinema.Name,
                s.Room.RoomName, s.StartTime, s.TicketPrice
            }).Take(ResultLimit + 1).ToListAsync(ct);

        var items = rows.Take(ResultLimit).Select(s => new ChatItem(
            s.Title, $"{s.StartTime:HH:mm} · {s.Cinema ?? "Chưa gán chi nhánh"} · {s.RoomName}\nGiá cơ sở {Money(s.TicketPrice)}",
            s.MovieId, s.ShowtimeId)).ToArray();
        var scope = date.ToString("dd/MM/yyyy", Vietnamese) + (context.Cinema is { } cinema ? $" · {cinema}" : "");
        var next = context with { Date = date.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture) };
        return Results($"Suất chiếu ngày {scope}. Bạn mở suất để xem ghế và giá theo loại ghế.",
            $"Mình chưa tìm thấy suất phù hợp ngày {scope}. Bạn có muốn đổi giờ, ngày hoặc chi nhánh?", next, items, rows.Count);
    }

    private async Task<ChatReply> CinemasAsync(ChatContext context, CancellationToken ct)
    {
        var rows = await PublicCinemas(context.Cinema).OrderBy(c => c.Name).ThenBy(c => c.CinemaId)
            .Select(c => new { c.Name, c.Address, c.City, c.Hotline }).Take(ResultLimit + 1).ToListAsync(ct);
        var items = rows.Take(ResultLimit).Select(c => new ChatItem(
            c.Name, $"{c.Address}, {c.City}" + (string.IsNullOrWhiteSpace(c.Hotline) ? "" : $"\nĐiện thoại {c.Hotline}"))).ToArray();
        return Results("Đây là các chi nhánh phù hợp.", "Mình chưa tìm thấy chi nhánh phù hợp. Bạn thử tên rạp hoặc tên thành phố nhé.", context, items, rows.Count);
    }

    private async Task<ChatReply> FoodAsync(ChatContext context, CancellationToken ct)
    {
        var rows = await db.FoodItems.AsNoTracking().Where(f => f.IsAvailable)
            .OrderBy(f => f.Category).ThenBy(f => f.Name).ThenBy(f => f.FoodItemId)
            .Select(f => new { f.Name, f.Price }).Take(ResultLimit + 1).ToListAsync(ct);
        var items = rows.Take(ResultLimit).Select(f => new ChatItem(f.Name, Money(f.Price))).ToArray();
        return Results("Đây là một số món đang phục vụ. Bạn xem đầy đủ khi thêm bắp nước vào đơn.", "Hiện mình chưa thấy món nào đang phục vụ.", context, items, rows.Count);
    }

    private static ChatReply Results(string found, string empty, ChatContext context, ChatItem[] items, int count)
        => new(count == 0 ? empty : found + (count > ResultLimit ? $" Mình hiển thị {ResultLimit} kết quả đầu." : ""), context, items);

    private static string Money(decimal amount) => amount.ToString("N0", Vietnamese) + " đ";
}
