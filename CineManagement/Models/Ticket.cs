using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

/// <summary>
/// Vé cho từng ghế, gắn với đơn hàng và suất chiếu.
/// Snapshot giá / mã ghế để lịch sử không đổi khi Seat hoặc Showtime bị sửa sau này.
/// </summary>
public class Ticket
{
    [Key]
    public int TicketId { get; set; }

    [Required]
    public int BookingId { get; set; }

    [Required]
    public int ShowtimeId { get; set; }

    [Required]
    public int SeatId { get; set; }

    /// <summary>Mã vé duy nhất, dùng cho QR / email (ví dụ: TCK-A1B2C3).</summary>
    [Required]
    [StringLength(30)]
    [Display(Name = "Mã vé")]
    public string TicketCode { get; set; } = string.Empty;

    [StringLength(10)]
    [Display(Name = "Mã ghế (snapshot)")]
    public string SeatCode { get; set; } = string.Empty;

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Giá vé")]
    public decimal UnitPrice { get; set; }

    [Display(Name = "Trạng thái vé")]
    public TicketStatus Status { get; set; } = TicketStatus.Held;

    [StringLength(500)]
    [Display(Name = "Nội dung QR")]
    public string? QrPayload { get; set; }

    [Display(Name = "Thời điểm soát vé")]
    public DateTime? CheckedInAt { get; set; }

    [StringLength(450)]
    [Display(Name = "Nhân viên soát vé")]
    public string? CheckedInByUserId { get; set; }

    [Display(Name = "Ngày tạo")]
    public DateTime CreatedAt { get; set; } = DateTime.Now;

    [Display(Name = "Ngày cập nhật")]
    public DateTime? UpdatedAt { get; set; }

    // Navigation
    public Booking? Booking { get; set; }
    public Showtime? Showtime { get; set; }
    public Seat? Seat { get; set; }

    [ForeignKey(nameof(CheckedInByUserId))]
    public ApplicationUser? CheckedInBy { get; set; }
}
