using System.Data;
using CineManagement.Data;
using CineManagement.DTOs;
using CineManagement.Models;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;

namespace CineManagement.Services;

public class BookingService : IBookingService
{
    public const int DefaultHoldMinutes = 10;

    private static readonly TicketStatus[] OccupyingTicketStatuses =
    [
        TicketStatus.Held,
        TicketStatus.Issued,
        TicketStatus.CheckedIn
    ];

    private readonly ApplicationDbContext _db;
    private readonly ILogger<BookingService> _logger;

    public BookingService(ApplicationDbContext db, ILogger<BookingService> logger)
    {
        _db = db;
        _logger = logger;
    }

    public async Task<SeatMapDto> GetSeatMapAsync(
        int showtimeId,
        string? userId,
        CancellationToken cancellationToken = default)
    {
        var showtime = await _db.Showtimes
            .AsNoTracking()
            .Include(s => s.Movie)
            .Include(s => s.Room)
                .ThenInclude(r => r!.Seats.Where(seat => seat.IsActive))
            .FirstOrDefaultAsync(s => s.ShowtimeId == showtimeId, cancellationToken);

        if (showtime?.Room == null || showtime.Movie == null)
            throw new InvalidOperationException("Suất chiếu không tồn tại.");

        var now = DateTime.UtcNow;

        var soldSeatIds = await GetSoldSeatIdsAsync(showtimeId, cancellationToken);

        var activeHolds = await _db.HoldSeats
            .AsNoTracking()
            .Where(h => h.ShowtimeId == showtimeId
                     && h.Status == HoldSeatStatus.Active
                     && h.ExpiresAt > now)
            .Select(h => new { h.SeatId, h.UserId, h.ExpiresAt })
            .ToListAsync(cancellationToken);

        var holdBySeat = activeHolds
            .GroupBy(h => h.SeatId)
            .ToDictionary(g => g.Key, g => g.First());

        var legacyHolds = await _db.BookedSeats
            .AsNoTracking()
            .Where(bs => bs.Booking!.ShowtimeId == showtimeId
                      && bs.Booking.Status == BookingStatus.Pending
                      && bs.HoldUntil > now)
            .Select(bs => new { bs.SeatId, bs.Booking!.UserId, bs.HoldUntil })
            .ToListAsync(cancellationToken);

        foreach (var legacy in legacyHolds)
        {
            if (!holdBySeat.ContainsKey(legacy.SeatId) && !soldSeatIds.Contains(legacy.SeatId))
            {
                holdBySeat[legacy.SeatId] = new
                {
                    legacy.SeatId,
                    legacy.UserId,
                    ExpiresAt = legacy.HoldUntil!.Value
                };
            }
        }

        DateTime? myHoldExpires = null;
        if (!string.IsNullOrEmpty(userId))
        {
            var mine = activeHolds.Where(h => h.UserId == userId).ToList();
            if (mine.Count > 0)
                myHoldExpires = mine.Max(h => h.ExpiresAt);
        }

        var seats = showtime.Room.Seats
            .OrderBy(s => s.RowLabel)
            .ThenBy(s => s.SeatNumber)
            .ToList();

        var rows = seats
            .GroupBy(s => s.RowLabel)
            .Select(g => new SeatRowDto
            {
                RowLabel = g.Key,
                Seats = g.Select(seat =>
                {
                    var status = SeatAvailabilityStatus.Available;
                    var heldByMe = false;

                    if (soldSeatIds.Contains(seat.SeatId))
                    {
                        status = SeatAvailabilityStatus.Sold;
                    }
                    else if (holdBySeat.TryGetValue(seat.SeatId, out var hold))
                    {
                        status = SeatAvailabilityStatus.Held;
                        heldByMe = !string.IsNullOrEmpty(userId) && hold.UserId == userId;
                    }

                    return new SeatCellDto
                    {
                        SeatId = seat.SeatId,
                        SeatCode = $"{seat.RowLabel}{seat.SeatNumber}",
                        RowLabel = seat.RowLabel,
                        SeatNumber = seat.SeatNumber,
                        SeatType = seat.SeatType,
                        Status = status,
                        IsHeldByCurrentUser = heldByMe,
                        Price = GetSeatPrice(showtime.TicketPrice, seat.SeatType)
                    };
                }).ToList()
            })
            .ToList();

        var total = seats.Count;
        var available = rows.SelectMany(r => r.Seats)
            .Count(s => s.Status == SeatAvailabilityStatus.Available);

        return new SeatMapDto
        {
            ShowtimeId = showtime.ShowtimeId,
            MovieId = showtime.MovieId,
            MovieTitle = showtime.Movie.Title,
            RoomId = showtime.RoomId,
            RoomName = showtime.Room.RoomName,
            StartTime = showtime.StartTime,
            BaseTicketPrice = showtime.TicketPrice,
            TotalSeats = total,
            AvailableSeats = available,
            MyHoldExpiresAt = myHoldExpires,
            Rows = rows
        };
    }

    public async Task<HoldSeatResponseDto> HoldSeatAsync(
        string userId,
        HoldSeatRequestDto request,
        CancellationToken cancellationToken = default)
    {
        var seatIds = request.SeatIds.Distinct().ToList();
        if (seatIds.Count == 0)
        {
            return new HoldSeatResponseDto
            {
                Success = false,
                Message = "Vui lòng chọn ít nhất một ghế."
            };
        }

        var holdMinutes = request.HoldMinutes > 0 ? request.HoldMinutes : DefaultHoldMinutes;
        IDbContextTransaction transaction = await _db.Database.BeginTransactionAsync(
            IsolationLevel.Serializable,
            cancellationToken);

        try
        {
            var showtime = await _db.Showtimes
                .Include(s => s.Room)
                    .ThenInclude(r => r!.Seats.Where(s => s.IsActive))
                .FirstOrDefaultAsync(s => s.ShowtimeId == request.ShowtimeId, cancellationToken);

            if (showtime?.Room == null || showtime.Status != ShowtimeStatus.Available)
            {
                await transaction.RollbackAsync(cancellationToken);
                return new HoldSeatResponseDto
                {
                    Success = false,
                    Message = "Suất chiếu không khả dụng."
                };
            }

            var roomSeatIds = showtime.Room.Seats.Select(s => s.SeatId).ToHashSet();
            if (seatIds.Any(id => !roomSeatIds.Contains(id)))
            {
                await transaction.RollbackAsync(cancellationToken);
                return new HoldSeatResponseDto
                {
                    Success = false,
                    Message = "Có ghế không thuộc phòng chiếu của suất này.",
                    ConflictSeatIds = seatIds.Where(id => !roomSeatIds.Contains(id)).ToList()
                };
            }

            var now = DateTime.UtcNow;
            var expiresAt = now.AddMinutes(holdMinutes);

            var staleHolds = await _db.HoldSeats
                .Where(h => h.ShowtimeId == request.ShowtimeId
                         && seatIds.Contains(h.SeatId)
                         && h.Status == HoldSeatStatus.Active
                         && h.ExpiresAt <= now)
                .ToListAsync(cancellationToken);

            foreach (var hold in staleHolds)
            {
                hold.Status = HoldSeatStatus.Expired;
                hold.UpdatedAt = now;
            }

            var soldSeatIds = await GetSoldSeatIdsAsync(request.ShowtimeId, cancellationToken);
            var soldConflicts = seatIds.Where(soldSeatIds.Contains).ToList();
            if (soldConflicts.Count > 0)
            {
                await transaction.RollbackAsync(cancellationToken);
                return FailHold("Ghế đã được bán.", soldConflicts);
            }

            var othersHolds = await _db.HoldSeats
                .Where(h => h.ShowtimeId == request.ShowtimeId
                         && seatIds.Contains(h.SeatId)
                         && h.Status == HoldSeatStatus.Active
                         && h.ExpiresAt > now
                         && h.UserId != userId)
                .Select(h => h.SeatId)
                .Distinct()
                .ToListAsync(cancellationToken);

            if (othersHolds.Count > 0)
            {
                await transaction.RollbackAsync(cancellationToken);
                return FailHold("Ghế đang được người khác giữ.", othersHolds);
            }

            var myActiveHolds = await _db.HoldSeats
                .Where(h => h.ShowtimeId == request.ShowtimeId
                         && h.UserId == userId
                         && h.Status == HoldSeatStatus.Active)
                .ToListAsync(cancellationToken);

            var requested = seatIds.ToHashSet();
            foreach (var hold in myActiveHolds)
            {
                if (!requested.Contains(hold.SeatId))
                {
                    hold.Status = HoldSeatStatus.Released;
                    hold.UpdatedAt = now;
                }
                else
                {
                    hold.ExpiresAt = expiresAt;
                    hold.UpdatedAt = now;
                }
            }

            var alreadyHeld = myActiveHolds
                .Where(h => requested.Contains(h.SeatId))
                .Select(h => h.SeatId)
                .ToHashSet();

            foreach (var seatId in seatIds.Where(id => !alreadyHeld.Contains(id)))
            {
                _db.HoldSeats.Add(new HoldSeat
                {
                    ShowtimeId = request.ShowtimeId,
                    SeatId = seatId,
                    UserId = userId,
                    HeldAt = now,
                    ExpiresAt = expiresAt,
                    Status = HoldSeatStatus.Active,
                    CreatedAt = now
                });
            }

            await _db.SaveChangesAsync(cancellationToken);
            await transaction.CommitAsync(cancellationToken);

            return new HoldSeatResponseDto
            {
                Success = true,
                Message = $"Đã giữ {seatIds.Count} ghế trong {holdMinutes} phút.",
                ExpiresAt = expiresAt,
                HeldSeatIds = seatIds
            };
        }
        catch (DbUpdateException ex) when (IsUniqueConstraintViolation(ex))
        {
            _logger.LogWarning(ex, "Race condition khi giữ ghế suất {ShowtimeId}", request.ShowtimeId);
            await transaction.RollbackAsync(cancellationToken);
            return FailHold("Ghế vừa được người khác giữ. Vui lòng chọn ghế khác.", seatIds);
        }
        catch
        {
            await transaction.RollbackAsync(cancellationToken);
            throw;
        }
    }

    public async Task<BookingResponseDto> CalculateTotalAmountAsync(
        BookingRequestDto request,
        string? userId = null,
        CancellationToken cancellationToken = default)
    {
        var quote = await BuildQuoteAsync(request, userId, persistVoucherCheck: false, cancellationToken);
        return MapQuoteToResponse(quote, booking: null, holdExpiresAt: null);
    }

    public async Task<BookingResponseDto> CreateBookingAsync(
        string userId,
        BookingRequestDto request,
        CancellationToken cancellationToken = default)
    {
        var seatIds = request.SeatIds.Distinct().ToList();
        if (seatIds.Count == 0)
            throw new InvalidOperationException("Vui lòng chọn ít nhất một ghế.");

        IDbContextTransaction transaction = await _db.Database.BeginTransactionAsync(
            IsolationLevel.Serializable,
            cancellationToken);

        try
        {
            var now = DateTime.UtcNow;

            var holds = await _db.HoldSeats
                .Where(h => h.ShowtimeId == request.ShowtimeId
                         && h.UserId == userId
                         && seatIds.Contains(h.SeatId)
                         && h.Status == HoldSeatStatus.Active)
                .ToListAsync(cancellationToken);

            var activeHoldSeatIds = holds
                .Where(h => h.ExpiresAt > now)
                .Select(h => h.SeatId)
                .ToHashSet();

            var missing = seatIds.Where(id => !activeHoldSeatIds.Contains(id)).ToList();
            if (missing.Count > 0)
            {
                await transaction.RollbackAsync(cancellationToken);
                throw new InvalidOperationException(
                    "Ghế chưa được giữ hoặc thời gian giữ đã hết. Vui lòng chọn lại ghế.");
            }

            var soldSeatIds = await GetSoldSeatIdsAsync(request.ShowtimeId, cancellationToken);
            if (seatIds.Any(soldSeatIds.Contains))
            {
                await transaction.RollbackAsync(cancellationToken);
                throw new InvalidOperationException("Ghế đã được bán. Không thể hoàn tất đơn hàng.");
            }

            var quote = await BuildQuoteAsync(request, userId, persistVoucherCheck: true, cancellationToken);

            var booking = new Booking
            {
                UserId = userId,
                ShowtimeId = request.ShowtimeId,
                VoucherId = quote.Voucher?.VoucherId,
                BookingCode = await GenerateUniqueBookingCodeAsync(cancellationToken),
                BookingTime = now,
                TicketAmount = quote.TicketAmount,
                FnBAmount = quote.FnBAmount,
                TotalAmount = quote.TotalAmount,
                DiscountAmount = quote.DiscountAmount,
                FinalAmount = quote.FinalAmount,
                Status = BookingStatus.Confirmed,
                PaymentStatus = PaymentStatus.Paid,
                PaymentMethod = request.PaymentMethod,
                PaymentReference = $"PAY-{Guid.NewGuid():N}"[..20],
                PaidAt = now,
                ContactEmail = request.ContactEmail,
                ContactPhone = request.ContactPhone,
                CreatedAt = now
            };

            _db.Bookings.Add(booking);
            await _db.SaveChangesAsync(cancellationToken);

            foreach (var line in quote.TicketLines)
            {
                var ticketCode = GenerateTicketCode();
                _db.Tickets.Add(new Ticket
                {
                    BookingId = booking.BookingId,
                    ShowtimeId = request.ShowtimeId,
                    SeatId = line.SeatId,
                    TicketCode = ticketCode,
                    SeatCode = line.SeatCode,
                    UnitPrice = line.UnitPrice,
                    Status = TicketStatus.Issued,
                    QrPayload = ticketCode,
                    CreatedAt = now
                });
            }

            foreach (var line in quote.FnBLines)
            {
                _db.OrderFnBs.Add(new OrderFnB
                {
                    BookingId = booking.BookingId,
                    FoodItemId = line.FoodItemId,
                    Quantity = line.Quantity,
                    UnitPrice = line.UnitPrice,
                    ItemName = line.ItemName,
                    CreatedAt = now
                });
            }

            foreach (var hold in holds.Where(h => activeHoldSeatIds.Contains(h.SeatId)))
            {
                hold.Status = HoldSeatStatus.Converted;
                hold.BookingId = booking.BookingId;
                hold.UpdatedAt = now;
            }

            var leftoverHolds = await _db.HoldSeats
                .Where(h => h.ShowtimeId == request.ShowtimeId
                         && h.UserId == userId
                         && h.Status == HoldSeatStatus.Active
                         && !seatIds.Contains(h.SeatId))
                .ToListAsync(cancellationToken);

            foreach (var hold in leftoverHolds)
            {
                hold.Status = HoldSeatStatus.Released;
                hold.UpdatedAt = now;
            }

            if (quote.Voucher != null)
            {
                var voucher = await _db.Vouchers
                    .FirstAsync(v => v.VoucherId == quote.Voucher.VoucherId, cancellationToken);

                if (voucher.UsageLimit.HasValue && voucher.UsedCount >= voucher.UsageLimit.Value)
                {
                    await transaction.RollbackAsync(cancellationToken);
                    throw new InvalidOperationException("Mã giảm giá vừa hết lượt sử dụng.");
                }

                voucher.UsedCount++;
                voucher.UpdatedAt = now;
            }

            await _db.SaveChangesAsync(cancellationToken);
            await transaction.CommitAsync(cancellationToken);

            booking.Tickets = await _db.Tickets
                .Where(t => t.BookingId == booking.BookingId)
                .ToListAsync(cancellationToken);
            booking.OrderFnBs = await _db.OrderFnBs
                .Where(o => o.BookingId == booking.BookingId)
                .ToListAsync(cancellationToken);
            booking.Voucher = quote.Voucher;

            return MapQuoteToResponse(quote, booking, holdExpiresAt: null);
        }
        catch (DbUpdateException ex) when (IsUniqueConstraintViolation(ex))
        {
            await transaction.RollbackAsync(cancellationToken);
            _logger.LogWarning(ex, "Race condition khi tạo booking suất {ShowtimeId}", request.ShowtimeId);
            throw new InvalidOperationException("Ghế vừa được người khác đặt. Vui lòng chọn lại.");
        }
        catch
        {
            await transaction.RollbackAsync(cancellationToken);
            throw;
        }
    }

    private async Task<HashSet<int>> GetSoldSeatIdsAsync(int showtimeId, CancellationToken cancellationToken)
    {
        var fromTickets = await _db.Tickets
            .AsNoTracking()
            .Where(t => t.ShowtimeId == showtimeId && OccupyingTicketStatuses.Contains(t.Status))
            .Select(t => t.SeatId)
            .ToListAsync(cancellationToken);

        var fromLegacy = await _db.BookedSeats
            .AsNoTracking()
            .Where(bs => bs.Booking!.ShowtimeId == showtimeId
                      && bs.Booking.Status == BookingStatus.Confirmed)
            .Select(bs => bs.SeatId)
            .ToListAsync(cancellationToken);

        return fromTickets.Concat(fromLegacy).ToHashSet();
    }

    private async Task<Quote> BuildQuoteAsync(
        BookingRequestDto request,
        string? userId,
        bool persistVoucherCheck,
        CancellationToken cancellationToken)
    {
        var seatIds = request.SeatIds.Distinct().ToList();

        var showtime = await _db.Showtimes
            .AsNoTracking()
            .Include(s => s.Room)
                .ThenInclude(r => r!.Seats)
            .FirstOrDefaultAsync(s => s.ShowtimeId == request.ShowtimeId, cancellationToken);

        if (showtime?.Room == null)
            throw new InvalidOperationException("Suất chiếu không tồn tại.");

        var seats = showtime.Room.Seats
            .Where(s => seatIds.Contains(s.SeatId) && s.IsActive)
            .ToList();

        if (seats.Count != seatIds.Count)
            throw new InvalidOperationException("Một hoặc nhiều ghế không hợp lệ.");

        var ticketLines = seats
            .OrderBy(s => s.RowLabel)
            .ThenBy(s => s.SeatNumber)
            .Select(s => new BookingTicketLineDto
            {
                SeatId = s.SeatId,
                SeatCode = $"{s.RowLabel}{s.SeatNumber}",
                UnitPrice = GetSeatPrice(showtime.TicketPrice, s.SeatType),
                Status = TicketStatus.Held
            })
            .ToList();

        var ticketAmount = ticketLines.Sum(t => t.UnitPrice);

        var fnbLines = new List<BookingFnBLineDto>();
        foreach (var item in request.FnBItems.Where(x => x.Quantity > 0))
        {
            var food = await _db.FoodItems
                .AsNoTracking()
                .FirstOrDefaultAsync(f => f.FoodItemId == item.FoodItemId && f.IsAvailable, cancellationToken);

            if (food == null)
                throw new InvalidOperationException($"Món F&B #{item.FoodItemId} không còn phục vụ.");

            fnbLines.Add(new BookingFnBLineDto
            {
                FoodItemId = food.FoodItemId,
                ItemName = food.Name,
                Quantity = item.Quantity,
                UnitPrice = food.Price,
                SubTotal = food.Price * item.Quantity
            });
        }

        var fnbAmount = fnbLines.Sum(x => x.SubTotal);
        var total = ticketAmount + fnbAmount;

        var voucherResult = await TryApplyVoucherAsync(
            request.VoucherCode,
            total,
            userId,
            persistVoucherCheck,
            cancellationToken);

        var discount = voucherResult.Discount;
        var finalAmount = Math.Max(0, total - discount);

        return new Quote
        {
            ShowtimeId = request.ShowtimeId,
            PaymentMethod = request.PaymentMethod,
            TicketAmount = ticketAmount,
            FnBAmount = fnbAmount,
            TotalAmount = total,
            DiscountAmount = discount,
            FinalAmount = finalAmount,
            Voucher = voucherResult.Voucher,
            VoucherCode = voucherResult.Code,
            VoucherMessage = voucherResult.Message,
            VoucherApplied = voucherResult.Applied,
            TicketLines = ticketLines,
            FnBLines = fnbLines
        };
    }

    private async Task<(Voucher? Voucher, string? Code, string? Message, bool Applied, decimal Discount)> TryApplyVoucherAsync(
        string? code,
        decimal subtotal,
        string? userId,
        bool strictUsage,
        CancellationToken cancellationToken)
    {
        if (string.IsNullOrWhiteSpace(code))
            return (null, null, null, false, 0);

        var normalized = code.Trim().ToUpperInvariant();
        var now = DateTime.UtcNow;

        var voucher = await _db.Vouchers
            .FirstOrDefaultAsync(v => v.Code == normalized, cancellationToken);

        if (voucher == null || !voucher.IsActive)
            return (null, normalized, "Mã giảm giá không hợp lệ hoặc đã hết hạn.", false, 0);

        if (voucher.ValidFrom > now || voucher.ValidTo.Date < now.Date)
            return (null, normalized, "Mã giảm giá không hợp lệ hoặc đã hết hạn.", false, 0);

        if (voucher.UsageLimit.HasValue && voucher.UsedCount >= voucher.UsageLimit.Value)
            return (null, normalized, "Mã giảm giá đã được sử dụng hết.", false, 0);

        if (voucher.MinOrderAmount > 0 && subtotal < voucher.MinOrderAmount)
        {
            return (null, normalized,
                $"Đơn tối thiểu {voucher.MinOrderAmount:N0} VNĐ để dùng mã này.",
                false, 0);
        }

        if (!string.IsNullOrEmpty(userId) && voucher.PerUserLimit > 0)
        {
            var usedByUser = await _db.Bookings.CountAsync(
                b => b.UserId == userId
                  && b.VoucherId == voucher.VoucherId
                  && (b.Status == BookingStatus.Confirmed || b.Status == BookingStatus.Pending),
                cancellationToken);

            if (usedByUser >= voucher.PerUserLimit)
                return (null, normalized, "Bạn đã dùng hết lượt cho mã này.", false, 0);
        }

        decimal discount;
        if (voucher.DiscountType == DiscountType.FixedAmount)
            discount = voucher.DiscountAmount;
        else
            discount = Math.Round(subtotal * voucher.DiscountPercent / 100, 0, MidpointRounding.AwayFromZero);

        if (voucher.MaxDiscountAmount.HasValue)
            discount = Math.Min(discount, voucher.MaxDiscountAmount.Value);

        discount = Math.Min(discount, subtotal);

        _ = strictUsage;
        return (voucher, voucher.Code, $"Áp dụng thành công! Giảm {discount:N0} VNĐ", true, discount);
    }

    private static BookingResponseDto MapQuoteToResponse(Quote quote, Booking? booking, DateTime? holdExpiresAt)
    {
        var tickets = booking?.Tickets.Count > 0
            ? booking.Tickets.Select(t => new BookingTicketLineDto
            {
                TicketId = t.TicketId,
                TicketCode = t.TicketCode,
                SeatId = t.SeatId,
                SeatCode = t.SeatCode,
                UnitPrice = t.UnitPrice,
                Status = t.Status
            }).ToList()
            : quote.TicketLines;

        var fnb = booking?.OrderFnBs.Count > 0
            ? booking.OrderFnBs.Select(o => new BookingFnBLineDto
            {
                FoodItemId = o.FoodItemId,
                ItemName = o.ItemName ?? string.Empty,
                Quantity = o.Quantity,
                UnitPrice = o.UnitPrice,
                SubTotal = o.UnitPrice * o.Quantity
            }).ToList()
            : quote.FnBLines;

        return new BookingResponseDto
        {
            BookingId = booking?.BookingId ?? 0,
            BookingCode = booking?.BookingCode ?? string.Empty,
            ShowtimeId = quote.ShowtimeId,
            Status = booking?.Status ?? BookingStatus.Pending,
            PaymentStatus = booking?.PaymentStatus ?? PaymentStatus.Unpaid,
            PaymentMethod = booking?.PaymentMethod ?? quote.PaymentMethod,
            TicketAmount = quote.TicketAmount,
            FnBAmount = quote.FnBAmount,
            TotalAmount = quote.TotalAmount,
            DiscountAmount = quote.DiscountAmount,
            FinalAmount = quote.FinalAmount,
            VoucherCode = quote.VoucherCode,
            VoucherMessage = quote.VoucherMessage,
            VoucherApplied = quote.VoucherApplied,
            HoldExpiresAt = holdExpiresAt,
            PaidAt = booking?.PaidAt,
            Tickets = tickets,
            FnBItems = fnb
        };
    }

    private static HoldSeatResponseDto FailHold(string message, IReadOnlyList<int> conflictSeatIds)
        => new()
        {
            Success = false,
            Message = message,
            ConflictSeatIds = conflictSeatIds
        };

    private static decimal GetSeatPrice(decimal basePrice, SeatType seatType)
        => seatType switch
        {
            SeatType.VIP => Math.Round(basePrice * 1.5m, 0, MidpointRounding.AwayFromZero),
            SeatType.Couple => Math.Round(basePrice * 2m, 0, MidpointRounding.AwayFromZero),
            _ => basePrice
        };

    private async Task<string> GenerateUniqueBookingCodeAsync(CancellationToken cancellationToken)
    {
        for (var i = 0; i < 8; i++)
        {
            var code = "BK" + DateTime.UtcNow.ToString("yyMMdd") + Random.Shared.Next(1000, 9999);
            var exists = await _db.Bookings.AnyAsync(b => b.BookingCode == code, cancellationToken);
            if (!exists)
                return code;
        }

        return "BK" + DateTime.UtcNow.ToString("yyMMddHHmmss") + Random.Shared.Next(10, 99);
    }

    private static string GenerateTicketCode()
        => "TCK" + Guid.NewGuid().ToString("N")[..10].ToUpperInvariant();

    private static bool IsUniqueConstraintViolation(DbUpdateException ex)
    {
        if (ex.InnerException is SqliteException sqlite)
            return sqlite.SqliteErrorCode is 19 or 2067;

        var message = ex.InnerException?.Message ?? ex.Message;
        return message.Contains("UNIQUE", StringComparison.OrdinalIgnoreCase);
    }

    private sealed class Quote
    {
        public int ShowtimeId { get; init; }
        public PaymentMethod PaymentMethod { get; init; }
        public decimal TicketAmount { get; init; }
        public decimal FnBAmount { get; init; }
        public decimal TotalAmount { get; init; }
        public decimal DiscountAmount { get; init; }
        public decimal FinalAmount { get; init; }
        public Voucher? Voucher { get; init; }
        public string? VoucherCode { get; init; }
        public string? VoucherMessage { get; init; }
        public bool VoucherApplied { get; init; }
        public List<BookingTicketLineDto> TicketLines { get; init; } = [];
        public List<BookingFnBLineDto> FnBLines { get; init; } = [];
    }
}
