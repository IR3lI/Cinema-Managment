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
        ViewBag.TotalMovies    = await _context.Movies.CountAsync(m => m.IsActive);
        ViewBag.NowShowing     = await _context.Movies.CountAsync(m => m.Status == MovieStatus.NowShowing && m.IsActive);
        ViewBag.ComingSoon     = await _context.Movies.CountAsync(m => m.Status == MovieStatus.ComingSoon && m.IsActive);
        ViewBag.TotalStaff     = await _context.Staffs.CountAsync(s => s.IsActive);

        var recentMovies = await _context.Movies
            .Include(m => m.Genre)
            .Where(m => m.IsActive)
            .OrderByDescending(m => m.CreatedAt)
            .Take(5)
            .ToListAsync();

        return View(recentMovies);
    }
}
