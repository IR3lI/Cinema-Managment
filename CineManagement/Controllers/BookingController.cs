using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;
using CineManagement.Data;
using CineManagement.Models;
using CineManagement.ViewModels;

namespace CineManagement.Controllers;

[Authorize]
public class BookingController : Controller
{
    private readonly ApplicationDbContext _context;
    private const int HoldMinutes = 10;

    public BookingController(ApplicationDbContext context)
    {
        _context = context;
    }

    // ── SCRUM-15: Select Seat ─────────────────────────────────────────────────
    [HttpGet]
    public async Task<IActionResult> SelectSeat(int showtimeId)
    {
        var showtime = await _context.Showtimes
            .Include(s => s.Movie)
            .Include(s => s.Room)
                .ThenInclude(r => r!.Seats.Where(s => s.IsActive).OrderBy(s => s.RowLabel).ThenBy(s => s.SeatNumber))
            .FirstOrDefaultAsync(s => s.ShowtimeId == showtimeId && s.Status == ShowtimeStatus.Available);

        if (showtime == null) return NotFound();

        var userId = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
        var now = DateTime.Now;

        // Get all occupied seats for this showtime
        var occupiedSeatIds = await _context.BookedSeats
            .Include(bs => bs.Booking)
            .Where(bs => bs.Booking!.ShowtimeId == showtimeId
                      && (bs.Booking.Status == BookingStatus.Confirmed
                          || (bs.Booking.Status == BookingStatus.Pending && bs.HoldUntil > now)))
            .Select(bs => new { bs.SeatId, bs.Booking!.UserId, bs.HoldUntil })
            .ToListAsync();

        var myPendingBooking = await _context.Bookings
            .Include(b => b.BookedSeats)
            .FirstOrDefaultAsync(b => b.ShowtimeId == showtimeId
                                   && b.UserId == userId
                                   && b.Status == BookingStatus.Pending);

        var myHeldSeatIds = myPendingBooking?.BookedSeats
            .Where(bs => bs.HoldUntil > now)
            .Select(bs => bs.SeatId)
            .ToHashSet() ?? new HashSet<int>();

        var seatMap = new Dictionary<string, List<SelectSeatViewModel.SeatInfo>>();
        foreach (var seat in showtime.Room!.Seats)
        {
            var occupied = occupiedSeatIds.FirstOrDefault(o => o.SeatId == seat.SeatId);
            SelectSeatViewModel.SeatStatus status;

            if (myHeldSeatIds.Contains(seat.SeatId))
                status = SelectSeatViewModel.SeatStatus.HeldByMe;
            else if (occupied != null && occupied.UserId == userId)
                status = SelectSeatViewModel.SeatStatus.HeldByMe;
            else if (occupied != null)
                status = SelectSeatViewModel.SeatStatus.HeldByOther;
            else
                status = SelectSeatViewModel.SeatStatus.Available;

            if (!seatMap.ContainsKey(seat.RowLabel))
                seatMap[seat.RowLabel] = new List<SelectSeatViewModel.SeatInfo>();

            seatMap[seat.RowLabel].Add(new SelectSeatViewModel.SeatInfo
            {
                SeatId   = seat.SeatId,
                SeatCode = $"{seat.RowLabel}{seat.SeatNumber}",
                SeatType = seat.SeatType,
                Status   = status
            });
        }

        ViewBag.PendingBookingId = myPendingBooking?.BookingId;
        ViewBag.HoldUntil = myPendingBooking?.BookedSeats.Max(bs => bs.HoldUntil);

        return View(new SelectSeatViewModel
        {
            Showtime = showtime,
            Room     = showtime.Room,
            SeatMap  = seatMap
        });
    }

    // ── SCRUM-17: Hold Seats (POST) ───────────────────────────────────────────
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> HoldSeats(int showtimeId, int[] selectedSeatIds)
    {
        if (selectedSeatIds.Length == 0)
        {
            TempData["Error"] = "Vui lòng chọn ít nhất một ghế.";
            return RedirectToAction(nameof(SelectSeat), new { showtimeId });
        }

        var showtime = await _context.Showtimes
            .Include(s => s.Room)
            .FirstOrDefaultAsync(s => s.ShowtimeId == showtimeId);

        if (showtime == null) return NotFound();

        var userId = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
        var now    = DateTime.Now;
        var holdUntil = now.AddMinutes(HoldMinutes);

        // Cancel any previous pending booking by this user for this showtime
        var oldBooking = await _context.Bookings
            .Include(b => b.BookedSeats)
            .FirstOrDefaultAsync(b => b.ShowtimeId == showtimeId
                                   && b.UserId == userId
                                   && b.Status == BookingStatus.Pending);
        if (oldBooking != null)
        {
            oldBooking.Status = BookingStatus.Cancelled;
            _context.BookedSeats.RemoveRange(oldBooking.BookedSeats);
        }

        // Check seats are still available
        var takenSeatIds = await _context.BookedSeats
            .Include(bs => bs.Booking)
            .Where(bs => bs.Booking!.ShowtimeId == showtimeId
                      && (bs.Booking.Status == BookingStatus.Confirmed
                          || (bs.Booking.Status == BookingStatus.Pending && bs.HoldUntil > now))
                      && selectedSeatIds.Contains(bs.SeatId))
            .Select(bs => bs.SeatId)
            .ToListAsync();

        if (takenSeatIds.Count > 0)
        {
            TempData["Error"] = "Một số ghế bạn chọn đã được đặt. Vui lòng chọn lại.";
            return RedirectToAction(nameof(SelectSeat), new { showtimeId });
        }

        // Get seat prices from showtime
        var seatPrice = showtime.TicketPrice;

        // Create booking
        var booking = new Booking
        {
            UserId      = userId,
            ShowtimeId  = showtimeId,
            BookingTime = now,
            TotalAmount = seatPrice * selectedSeatIds.Length,
            Status      = BookingStatus.Pending,
            BookingCode = GenerateBookingCode()
        };
        _context.Bookings.Add(booking);
        await _context.SaveChangesAsync();

        // Add booked seats with hold
        var bookedSeats = selectedSeatIds.Select(seatId => new BookedSeat
        {
            BookingId = booking.BookingId,
            SeatId    = seatId,
            SeatPrice = seatPrice,
            HoldUntil = holdUntil
        }).ToList();
        _context.BookedSeats.AddRange(bookedSeats);
        await _context.SaveChangesAsync();

        TempData["Success"] = $"Đã giữ {selectedSeatIds.Length} ghế trong {HoldMinutes} phút.";
        return RedirectToAction(nameof(AddFnB), new { bookingId = booking.BookingId });
    }

    // ── SCRUM-16: Add F&B ─────────────────────────────────────────────────────
    [HttpGet]
    public async Task<IActionResult> AddFnB(int bookingId)
    {
        var booking = await GetMyBookingAsync(bookingId);
        if (booking == null) return NotFound();

        var foodItems = await _context.FoodItems
            .Where(f => f.IsAvailable)
            .OrderBy(f => f.Category).ThenBy(f => f.Name)
            .ToListAsync();

        var existingFnB = await _context.BookingFoodItems
            .Where(bf => bf.BookingId == bookingId)
            .ToListAsync();

        var items = foodItems.Select(f => new FnBItemViewModel
        {
            FoodItemId  = f.FoodItemId,
            Name        = f.Name,
            Description = f.Description,
            Price       = f.Price,
            Category    = f.Category,
            ImageUrl    = f.ImageUrl,
            Quantity    = existingFnB.FirstOrDefault(e => e.FoodItemId == f.FoodItemId)?.Quantity ?? 0
        }).ToList();

        var seatTotal = booking.BookedSeats.Sum(s => s.SeatPrice);

        return View(new AddFnBViewModel
        {
            BookingId   = bookingId,
            ShowtimeId  = booking.ShowtimeId,
            Items       = items,
            SeatTotal   = seatTotal
        });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> AddFnB(int bookingId, Dictionary<int, int> quantities)
    {
        var booking = await GetMyBookingAsync(bookingId);
        if (booking == null) return NotFound();

        // Remove existing FnB items
        var existing = _context.BookingFoodItems.Where(bf => bf.BookingId == bookingId);
        _context.BookingFoodItems.RemoveRange(existing);

        // Add new ones
        decimal fnbTotal = 0;
        foreach (var (foodItemId, qty) in quantities.Where(q => q.Value > 0))
        {
            var food = await _context.FoodItems.FindAsync(foodItemId);
            if (food == null || !food.IsAvailable) continue;

            _context.BookingFoodItems.Add(new BookingFoodItem
            {
                BookingId  = bookingId,
                FoodItemId = foodItemId,
                Quantity   = qty,
                UnitPrice  = food.Price
            });
            fnbTotal += food.Price * qty;
        }

        // Update booking total
        var seatTotal = booking.BookedSeats.Sum(s => s.SeatPrice);
        booking.TotalAmount  = seatTotal + fnbTotal;
        booking.FinalAmount  = booking.TotalAmount - booking.DiscountAmount;
        _context.Update(booking);
        await _context.SaveChangesAsync();

        return RedirectToAction(nameof(Checkout), new { bookingId });
    }

    // ── SCRUM-18 + 19: Checkout ───────────────────────────────────────────────
    [HttpGet]
    public async Task<IActionResult> Checkout(int bookingId)
    {
        var booking = await GetMyBookingAsync(bookingId);
        if (booking == null) return NotFound();

        var seatTotal = booking.BookedSeats.Sum(bs => bs.SeatPrice);
        var fnbTotal  = booking.BookingFoodItems.Sum(bf => bf.UnitPrice * bf.Quantity);

        var seatCodes = await _context.BookedSeats
            .Include(bs => bs.Seat)
            .Where(bs => bs.BookingId == bookingId)
            .Select(bs => bs.Seat!.RowLabel + bs.Seat.SeatNumber.ToString())
            .ToListAsync();

        return View(new CheckoutViewModel
        {
            BookingId      = bookingId,
            Booking        = booking,
            SeatCodes      = seatCodes,
            SeatTotal      = seatTotal,
            FnBTotal       = fnbTotal,
            DiscountAmount = booking.DiscountAmount,
            VoucherCode    = booking.Voucher?.Code,
            VoucherApplied = booking.VoucherId.HasValue
        });
    }

    // ── SCRUM-18: Apply Voucher (AJAX) ────────────────────────────────────────
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ApplyVoucher(int bookingId, string code)
    {
        var booking = await GetMyBookingAsync(bookingId);
        if (booking == null) return NotFound();

        var now = DateTime.Now;
        var voucher = await _context.Vouchers
            .FirstOrDefaultAsync(v => v.Code == code.ToUpper().Trim()
                                    && v.IsActive
                                    && v.ValidFrom <= now
                                    && v.ValidTo >= now);

        if (voucher == null)
            return Json(new { success = false, message = "Mã giảm giá không hợp lệ hoặc đã hết hạn." });

        if (voucher.UsageLimit.HasValue && voucher.UsedCount >= voucher.UsageLimit)
            return Json(new { success = false, message = "Mã giảm giá đã được sử dụng hết." });

        var subtotal = booking.TotalAmount;
        var discount = Math.Round(subtotal * voucher.DiscountPercent / 100, 0);
        if (voucher.MaxDiscountAmount.HasValue)
            discount = Math.Min(discount, voucher.MaxDiscountAmount.Value);

        // Save to booking
        booking.VoucherId      = voucher.VoucherId;
        booking.DiscountAmount = discount;
        booking.FinalAmount    = subtotal - discount;
        _context.Update(booking);
        await _context.SaveChangesAsync();

        return Json(new
        {
            success        = true,
            message        = $"Áp dụng thành công! Giảm {discount:N0} VNĐ",
            discountAmount = discount,
            finalAmount    = booking.FinalAmount
        });
    }

    // ── SCRUM-19: Pay ─────────────────────────────────────────────────────────
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Pay(int bookingId, string paymentMethod)
    {
        var booking = await GetMyBookingAsync(bookingId);
        if (booking == null) return NotFound();

        if (booking.Status != BookingStatus.Pending)
        {
            TempData["Error"] = "Đơn đặt vé này không còn hiệu lực.";
            return RedirectToAction(nameof(Checkout), new { bookingId });
        }

        // Check hold still valid
        var now = DateTime.Now;
        var holdExpired = booking.BookedSeats.Any(bs => bs.HoldUntil < now);
        if (holdExpired)
        {
            booking.Status = BookingStatus.Expired;
            _context.Update(booking);
            await _context.SaveChangesAsync();
            TempData["Error"] = "Thời gian giữ ghế đã hết. Vui lòng đặt lại.";
            return RedirectToAction("Index", "Home");
        }

        // Finalize booking
        var method = paymentMethod switch
        {
            "BankCard" => PaymentMethod.BankCard,
            "EWallet"  => PaymentMethod.EWallet,
            _          => PaymentMethod.Cash
        };

        booking.Status        = BookingStatus.Confirmed;
        booking.PaymentMethod = method;
        booking.PaidAt        = now;
        booking.FinalAmount   = booking.TotalAmount - booking.DiscountAmount;

        // Increment voucher usage
        if (booking.VoucherId.HasValue)
        {
            var voucher = await _context.Vouchers.FindAsync(booking.VoucherId.Value);
            if (voucher != null) voucher.UsedCount++;
        }

        _context.Update(booking);
        await _context.SaveChangesAsync();

        TempData["Success"] = "Đặt vé thành công!";
        return RedirectToAction(nameof(Confirmation), new { bookingId });
    }

    // ── Confirmation ──────────────────────────────────────────────────────────
    public async Task<IActionResult> Confirmation(int bookingId)
    {
        var userId  = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
        var booking = await _context.Bookings
            .Include(b => b.Showtime).ThenInclude(s => s!.Movie)
            .Include(b => b.Showtime).ThenInclude(s => s!.Room)
            .Include(b => b.BookedSeats).ThenInclude(bs => bs.Seat)
            .Include(b => b.BookingFoodItems).ThenInclude(bf => bf.FoodItem)
            .Include(b => b.Voucher)
            .FirstOrDefaultAsync(b => b.BookingId == bookingId && b.UserId == userId);

        if (booking == null) return NotFound();

        var seatCodes = booking.BookedSeats
            .Select(bs => bs.Seat!.RowLabel + bs.Seat.SeatNumber.ToString())
            .OrderBy(c => c).ToList();

        return View(new ConfirmationViewModel { Booking = booking, SeatCodes = seatCodes });
    }

    // ── My Bookings ───────────────────────────────────────────────────────────
    public async Task<IActionResult> MyBookings()
    {
        var userId = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
        var bookings = await _context.Bookings
            .Include(b => b.Showtime).ThenInclude(s => s!.Movie)
            .Include(b => b.Showtime).ThenInclude(s => s!.Room)
            .Include(b => b.BookedSeats)
            .Where(b => b.UserId == userId)
            .OrderByDescending(b => b.BookingTime)
            .ToListAsync();

        return View(bookings);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────
    private async Task<Booking?> GetMyBookingAsync(int bookingId)
    {
        var userId = User.FindFirstValue(ClaimTypes.NameIdentifier)!;
        return await _context.Bookings
            .Include(b => b.BookedSeats)
            .Include(b => b.BookingFoodItems)
            .Include(b => b.Voucher)
            .FirstOrDefaultAsync(b => b.BookingId == bookingId && b.UserId == userId);
    }

    private static string GenerateBookingCode()
        => "BK" + DateTime.Now.ToString("yyMMdd") + Random.Shared.Next(1000, 9999).ToString();
}
