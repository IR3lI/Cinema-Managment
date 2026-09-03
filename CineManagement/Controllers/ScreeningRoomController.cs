using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using CineManagement.Data;
using CineManagement.Models;
using CineManagement.ViewModels;

namespace CineManagement.Controllers;

[Authorize(Roles = "Admin")]
public class ScreeningRoomController : Controller
{
    private readonly ApplicationDbContext _context;

    public ScreeningRoomController(ApplicationDbContext context)
    {
        _context = context;
    }

    // ── Index ─────────────────────────────────────────────────────────────
    public async Task<IActionResult> Index()
    {
        var rooms = await _context.ScreeningRooms
            .Include(r => r.Seats)
            .Include(r => r.Showtimes)
            .OrderBy(r => r.RoomName)
            .ToListAsync();
        return View(rooms);
    }

    // ── Details (Seat Map) ─────────────────────────────────────────────────
    public async Task<IActionResult> Details(int id)
    {
        var room = await _context.ScreeningRooms
            .Include(r => r.Seats.OrderBy(s => s.RowLabel).ThenBy(s => s.SeatNumber))
            .FirstOrDefaultAsync(r => r.RoomId == id);

        if (room == null) return NotFound();
        return View(room);
    }

    // ── Create ────────────────────────────────────────────────────────────
    [HttpGet]
    public IActionResult Create() => View(new ScreeningRoomFormViewModel());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(ScreeningRoomFormViewModel model)
    {
        if (!ModelState.IsValid) return View(model);

        var room = new ScreeningRoom
        {
            RoomName    = model.RoomName,
            RoomType    = model.RoomType,
            Rows        = model.Rows,
            SeatsPerRow = model.SeatsPerRow,
            Description = model.Description,
            IsActive    = model.IsActive
        };
        _context.ScreeningRooms.Add(room);
        await _context.SaveChangesAsync();

        // Auto-generate seats
        await GenerateSeatsAsync(room);

        TempData["Success"] = $"Tạo phòng \"{room.RoomName}\" thành công với {room.Rows * room.SeatsPerRow} ghế!";
        return RedirectToAction(nameof(Index));
    }

    // ── Edit ──────────────────────────────────────────────────────────────
    [HttpGet]
    public async Task<IActionResult> Edit(int id)
    {
        var room = await _context.ScreeningRooms.FindAsync(id);
        if (room == null) return NotFound();

        return View(new ScreeningRoomFormViewModel
        {
            RoomId      = room.RoomId,
            RoomName    = room.RoomName,
            RoomType    = room.RoomType,
            Rows        = room.Rows,
            SeatsPerRow = room.SeatsPerRow,
            Description = room.Description,
            IsActive    = room.IsActive
        });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, ScreeningRoomFormViewModel model)
    {
        if (id != model.RoomId) return BadRequest();
        if (!ModelState.IsValid) return View(model);

        var room = await _context.ScreeningRooms.FindAsync(id);
        if (room == null) return NotFound();

        bool layoutChanged = room.Rows != model.Rows || room.SeatsPerRow != model.SeatsPerRow;

        room.RoomName    = model.RoomName;
        room.RoomType    = model.RoomType;
        room.Rows        = model.Rows;
        room.SeatsPerRow = model.SeatsPerRow;
        room.Description = model.Description;
        room.IsActive    = model.IsActive;

        _context.Update(room);
        await _context.SaveChangesAsync();

        // Regenerate seats if layout changed
        if (layoutChanged)
        {
            var oldSeats = _context.Seats.Where(s => s.RoomId == id);
            _context.Seats.RemoveRange(oldSeats);
            await _context.SaveChangesAsync();
            await GenerateSeatsAsync(room);
            TempData["Success"] = $"Cập nhật phòng \"{room.RoomName}\" thành công. Sơ đồ ghế đã được tạo lại!";
        }
        else
        {
            TempData["Success"] = $"Cập nhật phòng \"{room.RoomName}\" thành công!";
        }

        return RedirectToAction(nameof(Index));
    }

    // ── Delete (soft) ─────────────────────────────────────────────────────
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(int id)
    {
        var room = await _context.ScreeningRooms.FindAsync(id);
        if (room == null) return NotFound();

        room.IsActive = false;
        _context.Update(room);
        await _context.SaveChangesAsync();

        TempData["Success"] = $"Đã vô hiệu hóa phòng \"{room.RoomName}\"!";
        return RedirectToAction(nameof(Index));
    }

    // ── Helper: Generate seats ─────────────────────────────────────────────
    private async Task GenerateSeatsAsync(ScreeningRoom room)
    {
        var seats = new List<Seat>();
        for (int r = 0; r < room.Rows; r++)
        {
            char rowChar = (char)('A' + r);
            for (int s = 1; s <= room.SeatsPerRow; s++)
            {
                SeatType type = SeatType.Standard;
                if (r >= room.Rows - 2) type = SeatType.VIP;
                if (room.RoomType == RoomType.VIP && s == room.SeatsPerRow) type = SeatType.Couple;

                seats.Add(new Seat
                {
                    RoomId     = room.RoomId,
                    RowLabel   = rowChar.ToString(),
                    SeatNumber = s,
                    SeatType   = type,
                    IsActive   = true
                });
            }
        }
        _context.Seats.AddRange(seats);
        await _context.SaveChangesAsync();
    }
}
