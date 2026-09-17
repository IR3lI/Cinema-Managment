using CineManagement.Data;
using CineManagement.DTOs;
using CineManagement.Models;
using Microsoft.EntityFrameworkCore;

namespace CineManagement.Services;

public sealed class ReportService : IReportService
{
    private static readonly TicketStatus[] SoldTicketStatuses =
    [
        TicketStatus.Issued,
        TicketStatus.CheckedIn
    ];

    private readonly ApplicationDbContext _db;

    public ReportService(ApplicationDbContext db)
    {
        _db = db;
    }

    public async Task<IReadOnlyList<DailyRevenueDto>> GetRevenueReportAsync(
        DateTime fromDate,
        DateTime toDate,
        CancellationToken cancellationToken = default)
    {
        var from = fromDate.Date;
        var untilExclusive = toDate.Date.AddDays(1);
        if (untilExclusive <= from)
            throw new ArgumentException("Ngày kết thúc phải bằng hoặc sau ngày bắt đầu.");

        return await _db.Bookings
            .AsNoTracking()
            .Where(booking => booking.Status == BookingStatus.Confirmed
                           && booking.PaidAt != null
                           && booking.PaidAt >= from
                           && booking.PaidAt < untilExclusive)
            .GroupBy(booking => booking.PaidAt!.Value.Date)
            .OrderBy(group => group.Key)
            .Select(group => new DailyRevenueDto
            {
                Date = group.Key,
                BookingCount = group.Count(),
                Revenue = group.Sum(booking => booking.FinalAmount)
            })
            .ToListAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<TopMovieDto>> GetTopMoviesAsync(
        int top,
        CancellationToken cancellationToken = default)
    {
        if (top is < 1 or > 100)
            throw new ArgumentOutOfRangeException(nameof(top), "Top phải nằm trong khoảng 1 đến 100.");

        return await _db.Tickets
            .AsNoTracking()
            .Where(ticket => SoldTicketStatuses.Contains(ticket.Status)
                          && ticket.Booking!.Status == BookingStatus.Confirmed)
            .GroupBy(ticket => new { ticket.Showtime!.MovieId, ticket.Showtime.Movie!.Title })
            .Select(group => new TopMovieDto
            {
                MovieId = group.Key.MovieId,
                MovieTitle = group.Key.Title,
                TicketsSold = group.Count(),
                TicketRevenue = group.Sum(ticket => ticket.UnitPrice)
            })
            .OrderByDescending(movie => movie.TicketRevenue)
            .ThenBy(movie => movie.MovieTitle)
            .Take(top)
            .ToListAsync(cancellationToken);
    }

    public async Task<RoomOccupancyRateDto?> GetRoomOccupancyRateAsync(
        int showtimeId,
        CancellationToken cancellationToken = default)
    {
        var showtime = await _db.Showtimes
            .AsNoTracking()
            .Where(item => item.ShowtimeId == showtimeId)
            .Select(item => new
            {
                item.ShowtimeId,
                item.RoomId,
                RoomName = item.Room!.RoomName,
                TotalSeats = item.Room.Seats.Count(seat => seat.IsActive)
            })
            .FirstOrDefaultAsync(cancellationToken);

        if (showtime is null)
            return null;

        var soldSeats = await _db.Tickets
            .AsNoTracking()
            .CountAsync(ticket => ticket.ShowtimeId == showtimeId
                               && SoldTicketStatuses.Contains(ticket.Status), cancellationToken);

        return new RoomOccupancyRateDto
        {
            ShowtimeId = showtime.ShowtimeId,
            RoomId = showtime.RoomId,
            RoomName = showtime.RoomName,
            TotalSeats = showtime.TotalSeats,
            SoldSeats = soldSeats,
            OccupancyRate = showtime.TotalSeats == 0
                ? 0
                : Math.Round((decimal)soldSeats / showtime.TotalSeats * 100, 2)
        };
    }
}
