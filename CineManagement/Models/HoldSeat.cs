using System.ComponentModel.DataAnnotations;

namespace CineManagement.Models;

/// <summary>
/// Ghế đang bị giữ tạm (SCRUM-17 / SCRUM-20). Unique (ShowtimeId, SeatId) khi Status = Active.
/// Khi thanh toán thành công: Converted. Khi timeout: Expired rồi xóa hoặc đánh dấu.
/// </summary>
public class HoldSeat
{
    [Key]
    public int HoldSeatId { get; set; }

    [Required]
    public int ShowtimeId { get; set; }

    [Required]
    public int SeatId { get; set; }

    [Required]
    [StringLength(450)]
    public string UserId { get; set; } = string.Empty;

    /// <summary>Đơn tạm thời (Pending) gắn với lần giữ ghế, nếu có.</summary>
    public int? BookingId { get; set; }

    [Display(Name = "Giữ lúc")]
    public DateTime HeldAt { get; set; } = DateTime.UtcNow;

    [Display(Name = "Hết hạn lúc")]
    public DateTime ExpiresAt { get; set; }

    [Display(Name = "Trạng thái giữ ghế")]
    public HoldSeatStatus Status { get; set; } = HoldSeatStatus.Active;

    [Display(Name = "Ngày tạo")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    [Display(Name = "Ngày cập nhật")]
    public DateTime? UpdatedAt { get; set; }

    [Display(Name = "Còn hiệu lực")]
    public bool IsActive => Status == HoldSeatStatus.Active && ExpiresAt > DateTime.UtcNow;

    // Navigation
    public Showtime? Showtime { get; set; }
    public Seat? Seat { get; set; }
    public ApplicationUser? User { get; set; }
    public Booking? Booking { get; set; }
}
