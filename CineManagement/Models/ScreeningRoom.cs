using System.ComponentModel.DataAnnotations;

namespace CineManagement.Models;

public enum RoomType
{
    [Display(Name = "Tiêu chuẩn")]
    Standard,

    [Display(Name = "VIP")]
    VIP,

    [Display(Name = "IMAX")]
    IMAX
}

public class ScreeningRoom
{
    [Key]
    public int RoomId { get; set; }

    [Required(ErrorMessage = "Tên phòng không được để trống")]
    [StringLength(100)]
    [Display(Name = "Tên phòng")]
    public string RoomName { get; set; } = string.Empty;

    [Display(Name = "Loại phòng")]
    public RoomType RoomType { get; set; } = RoomType.Standard;

    [Range(1, 26)]
    [Display(Name = "Số hàng")]
    public int Rows { get; set; } = 8;

    [Range(1, 30)]
    [Display(Name = "Số ghế mỗi hàng")]
    public int SeatsPerRow { get; set; } = 12;

    [Display(Name = "Sức chứa")]
    public int Capacity => Rows * SeatsPerRow;

    [StringLength(500)]
    [Display(Name = "Mô tả")]
    public string? Description { get; set; }

    [Display(Name = "Đang hoạt động")]
    public bool IsActive { get; set; } = true;

    // Navigation
    public ICollection<Seat> Seats { get; set; } = new List<Seat>();
    public ICollection<Showtime> Showtimes { get; set; } = new List<Showtime>();
}
