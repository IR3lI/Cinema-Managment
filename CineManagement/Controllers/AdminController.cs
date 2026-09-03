using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using CineManagement.Data;
using CineManagement.Models;

namespace CineManagement.Controllers;

[Authorize(Roles = "Admin,Staff")]
public class AdminController : Controller
{
    private readonly ApplicationDbContext _context;

    public AdminController(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<IActionResult> Dashboard()
    {
        var today = DateTime.Today;

        ViewBag.TotalMovies    = await _context.Movies.CountAsync(m => m.IsActive);
        ViewBag.NowShowing     = await _context.Movies.CountAsync(m => m.Status == MovieStatus.NowShowing && m.IsActive);
        ViewBag.ComingSoon     = await _context.Movies.CountAsync(m => m.Status == MovieStatus.ComingSoon && m.IsActive);
        ViewBag.TotalStaff     = await _context.Staffs.CountAsync(s => s.IsActive);
        ViewBag.TotalRooms     = await _context.ScreeningRooms.CountAsync(r => r.IsActive);
        ViewBag.TotalShowtimes = await _context.Showtimes.CountAsync(s => s.StartTime >= today && s.Status == ShowtimeStatus.Available);
        ViewBag.TotalFood      = await _context.FoodItems.CountAsync(f => f.IsAvailable);

        // Sprint 3 stats
        ViewBag.TodayBookings  = await _context.Bookings.CountAsync(b => b.BookingTime.Date == today && b.Status == BookingStatus.Confirmed);
        ViewBag.TodayRevenue   = await _context.Bookings
            .Where(b => b.BookingTime.Date == today && b.Status == BookingStatus.Confirmed)
            .SumAsync(b => (decimal?)b.FinalAmount) ?? 0;

        var recentMovies = await _context.Movies
            .Include(m => m.Genre)
            .Where(m => m.IsActive)
            .OrderByDescending(m => m.CreatedAt)
            .Take(5)
            .ToListAsync();

        return View(recentMovies);
    }

    // ── Admin Bookings list ────────────────────────────────────────────────
    public async Task<IActionResult> Bookings(BookingStatus? status, DateTime? date, string? search)
    {
        var query = _context.Bookings
            .Include(b => b.User)
            .Include(b => b.Showtime).ThenInclude(s => s!.Movie)
            .Include(b => b.Showtime).ThenInclude(s => s!.Room)
            .Include(b => b.BookedSeats)
            .AsQueryable();

        if (status.HasValue)
            query = query.Where(b => b.Status == status);
        if (date.HasValue)
            query = query.Where(b => b.BookingTime.Date == date.Value.Date);
        if (!string.IsNullOrWhiteSpace(search))
            query = query.Where(b => b.BookingCode.Contains(search) || b.User!.Email!.Contains(search));

        ViewBag.Status = status;
        ViewBag.Date   = date;
        ViewBag.Search = search;

        return View(await query.OrderByDescending(b => b.BookingTime).ToListAsync());
    }
}
