using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

public enum ShowtimeStatus
{
    [Display(Name = "Còn vé")]
    Available,

    [Display(Name = "Hết vé")]
    SoldOut,

    [Display(Name = "Đã hủy")]
    Canceled,

    [Display(Name = "Đã kết thúc")]
    Ended
}

public class Showtime
{
    public int ShowtimeId { get; set; }

    [Required]
    [Display(Name = "Phim")]
    public int MovieId { get; set; }

    [Required]
    [Display(Name = "Phòng chiếu")]
    public int RoomId { get; set; }

    [Required]
    [Display(Name = "Giờ chiếu")]
    public DateTime StartTime { get; set; }

    [Display(Name = "Giờ kết thúc")]
    public DateTime? EndTime { get; set; }

    [Required]
    [Range(0, 10000000)]
    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Giá vé (VNĐ)")]
    public decimal TicketPrice { get; set; }

    [Display(Name = "Trạng thái")]
    public ShowtimeStatus Status { get; set; } = ShowtimeStatus.Available;

    [StringLength(500)]
    [Display(Name = "Ghi chú")]
    public string? Notes { get; set; }

    // Navigation
    public Movie? Movie { get; set; }
    public ScreeningRoom? Room { get; set; }
}
