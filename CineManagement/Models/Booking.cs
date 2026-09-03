using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

public enum BookingStatus
{
    [Display(Name = "Chờ thanh toán")]
    Pending,

    [Display(Name = "Đã xác nhận")]
    Confirmed,

    [Display(Name = "Đã hủy")]
    Cancelled,

    [Display(Name = "Hết hạn")]
    Expired
}

public enum PaymentMethod
{
    [Display(Name = "Tiền mặt tại quầy")]
    Cash,

    [Display(Name = "Thẻ ngân hàng")]
    BankCard,

    [Display(Name = "Ví điện tử")]
    EWallet
}

public class Booking
{
    public int BookingId { get; set; }

    [Required]
    public string UserId { get; set; } = string.Empty;

    [Required]
    public int ShowtimeId { get; set; }

    public int? VoucherId { get; set; }

    [Display(Name = "Thời gian đặt")]
    public DateTime BookingTime { get; set; } = DateTime.Now;

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Tổng tiền gốc")]
    public decimal TotalAmount { get; set; }

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Tiền giảm giá")]
    public decimal DiscountAmount { get; set; }

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Thành tiền")]
    public decimal FinalAmount { get; set; }

    [Display(Name = "Trạng thái")]
    public BookingStatus Status { get; set; } = BookingStatus.Pending;

    [Display(Name = "Phương thức thanh toán")]
    public PaymentMethod? PaymentMethod { get; set; }

    [Display(Name = "Thời gian thanh toán")]
    public DateTime? PaidAt { get; set; }

    // Unique booking reference code
    [StringLength(20)]
    [Display(Name = "Mã đặt vé")]
    public string BookingCode { get; set; } = string.Empty;

    // Navigation
    public ApplicationUser? User { get; set; }
    public Showtime? Showtime { get; set; }
    public Voucher? Voucher { get; set; }
    public ICollection<BookedSeat> BookedSeats { get; set; } = new List<BookedSeat>();
    public ICollection<BookingFoodItem> BookingFoodItems { get; set; } = new List<BookingFoodItem>();
}
