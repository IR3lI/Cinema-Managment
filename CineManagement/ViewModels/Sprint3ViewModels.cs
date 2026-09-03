using CineManagement.Models;

namespace CineManagement.ViewModels;

// ── SelectSeat ViewModel ────────────────────────────────────────────────────
public class SelectSeatViewModel
{
    public Showtime Showtime { get; set; } = null!;
    public ScreeningRoom Room { get; set; } = null!;

    // Rows -> Seats (ordered)
    public Dictionary<string, List<SeatInfo>> SeatMap { get; set; } = new();

    public class SeatInfo
    {
        public int SeatId { get; set; }
        public string SeatCode { get; set; } = "";
        public SeatType SeatType { get; set; }
        public SeatStatus Status { get; set; }
    }

    public enum SeatStatus { Available, HeldByMe, HeldByOther, Booked }
}

// ── FnB Item selection ───────────────────────────────────────────────────────
public class FnBItemViewModel
{
    public int FoodItemId { get; set; }
    public string Name { get; set; } = "";
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public FoodCategory Category { get; set; }
    public string? ImageUrl { get; set; }
    public int Quantity { get; set; } = 0;
}

public class AddFnBViewModel
{
    public int BookingId { get; set; }
    public int ShowtimeId { get; set; }
    public List<FnBItemViewModel> Items { get; set; } = new();
    public decimal SeatTotal { get; set; }
}

// ── Checkout ViewModel ───────────────────────────────────────────────────────
public class CheckoutViewModel
{
    public int BookingId { get; set; }
    public Booking Booking { get; set; } = null!;

    // Seat summary
    public List<string> SeatCodes { get; set; } = new();
    public decimal SeatTotal { get; set; }

    // F&B summary
    public decimal FnBTotal { get; set; }

    // Totals
    public decimal SubTotal => SeatTotal + FnBTotal;
    public decimal DiscountAmount { get; set; }
    public decimal FinalAmount => SubTotal - DiscountAmount;

    // Voucher
    public string? VoucherCode { get; set; }
    public string? VoucherMessage { get; set; }
    public bool VoucherApplied { get; set; }

    // Payment
    public string PaymentMethod { get; set; } = "Cash";
}

// ── Confirmation ViewModel ────────────────────────────────────────────────────
public class ConfirmationViewModel
{
    public Booking Booking { get; set; } = null!;
    public List<string> SeatCodes { get; set; } = new();
}
