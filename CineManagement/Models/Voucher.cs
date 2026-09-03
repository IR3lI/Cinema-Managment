using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

public class Voucher
{
    public int VoucherId { get; set; }

    [Required]
    [StringLength(50)]
    [Display(Name = "Mã giảm giá")]
    public string Code { get; set; } = string.Empty;

    [StringLength(200)]
    [Display(Name = "Mô tả")]
    public string? Description { get; set; }

    [Range(0, 100)]
    [Display(Name = "Phần trăm giảm (%)")]
    public decimal DiscountPercent { get; set; }

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Giảm tối đa (VNĐ)")]
    public decimal? MaxDiscountAmount { get; set; }

    [Display(Name = "Hiệu lực từ")]
    public DateTime ValidFrom { get; set; } = DateTime.Today;

    [Display(Name = "Hết hạn")]
    public DateTime ValidTo { get; set; } = DateTime.Today.AddDays(30);

    [Display(Name = "Giới hạn lượt dùng")]
    public int? UsageLimit { get; set; }

    [Display(Name = "Đã sử dụng")]
    public int UsedCount { get; set; } = 0;

    [Display(Name = "Kích hoạt")]
    public bool IsActive { get; set; } = true;

    // Navigation
    public ICollection<Booking> Bookings { get; set; } = new List<Booking>();
}
