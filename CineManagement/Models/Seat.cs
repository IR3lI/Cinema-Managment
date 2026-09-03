using System.ComponentModel.DataAnnotations;

namespace CineManagement.Models;

public enum SeatType
{
    [Display(Name = "Thường")]
    Standard,

    [Display(Name = "VIP")]
    VIP,

    [Display(Name = "Ghế đôi")]
    Couple
}

public class Seat
{
    public int SeatId { get; set; }

    [Required]
    public int RoomId { get; set; }

    [Required]
    [StringLength(2)]
    [Display(Name = "Hàng")]
    public string RowLabel { get; set; } = "A"; // A, B, C...

    [Range(1, 30)]
    [Display(Name = "Số ghế")]
    public int SeatNumber { get; set; }

    [Display(Name = "Loại ghế")]
    public SeatType SeatType { get; set; } = SeatType.Standard;

    [Display(Name = "Đang hoạt động")]
    public bool IsActive { get; set; } = true;

    // Display name: A1, B5, etc.
    public string SeatCode => $"{RowLabel}{SeatNumber}";

    // Navigation
    public ScreeningRoom? Room { get; set; }
}
