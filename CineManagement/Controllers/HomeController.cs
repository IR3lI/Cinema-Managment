using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using CineManagement.Data;
using CineManagement.Models;
using CineManagement.ViewModels;

namespace CineManagement.Controllers;

public class HomeController : Controller
{
    private readonly ApplicationDbContext _context;

    public HomeController(ApplicationDbContext context)
    {
        _context = context;
    }

    // ── Public Home (SCRUM-10 – search & filter) ──────────────────────────────
    public async Task<IActionResult> Index(string? search, int? genreId, MovieStatus? status)
    {
        var query = _context.Movies
            .Include(m => m.Genre)
            .Where(m => m.IsActive)
            .AsQueryable();

        // Default: show Now Showing + Coming Soon
        if (!status.HasValue)
            query = query.Where(m => m.Status == MovieStatus.NowShowing || m.Status == MovieStatus.ComingSoon);

        if (!string.IsNullOrWhiteSpace(search))
            query = query.Where(m =>
                m.Title.Contains(search) ||
                (m.Director != null && m.Director.Contains(search)) ||
                (m.Actors != null && m.Actors.Contains(search)));

        if (genreId.HasValue)
            query = query.Where(m => m.GenreId == genreId);

        if (status.HasValue)
            query = query.Where(m => m.Status == status);

        var genres = await _context.Genres.OrderBy(g => g.Name).ToListAsync();

        var vm = new MovieIndexViewModel
        {
            Movies = await query.OrderBy(m => m.Status).ThenByDescending(m => m.ReleaseDate).ToListAsync(),
            SearchTerm = search,
            GenreId = genreId,
            Status = status,
            Genres = genres.Select(g => new Microsoft.AspNetCore.Mvc.Rendering.SelectListItem(g.Name, g.GenreId.ToString()))
        };

        return View(vm);
    }

    // ── Movie Detail (public) – SCRUM-14 ──────────────────────────────────────
    public async Task<IActionResult> MovieDetail(int id)
    {
        var movie = await _context.Movies
            .Include(m => m.Genre)
            .FirstOrDefaultAsync(m => m.MovieId == id && m.IsActive);

        if (movie == null) return NotFound();

        // Load upcoming showtimes (today onwards), grouped by date
        var showtimes = await _context.Showtimes
            .Include(s => s.Room)
            .Where(s => s.MovieId == id
                     && s.StartTime >= DateTime.Now
                     && s.Status == ShowtimeStatus.Available)
            .OrderBy(s => s.StartTime)
            .ToListAsync();

        var showtimesByDate = showtimes
            .GroupBy(s => s.StartTime.Date)
            .OrderBy(g => g.Key)
            .ToDictionary(g => g.Key, g => g.ToList());

        ViewBag.ShowtimesByDate = showtimesByDate;
        return View(movie);
    }

    public IActionResult Privacy() => View();

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new CineManagement.Models.ErrorViewModel
        {
            RequestId = System.Diagnostics.Activity.Current?.Id ?? HttpContext.TraceIdentifier
        });
    }
}
