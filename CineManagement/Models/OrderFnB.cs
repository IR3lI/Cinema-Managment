using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

/// <summary>
/// Dòng F&amp;B trong đơn hàng. UnitPrice là snapshot giá tại thời điểm đặt.
/// </summary>
public class OrderFnB
{
    [Key]
    public int OrderFnBId { get; set; }

    [Required]
    public int BookingId { get; set; }

    [Required]
    public int FoodItemId { get; set; }

    [Range(1, 50)]
    [Display(Name = "Số lượng")]
    public int Quantity { get; set; } = 1;

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Đơn giá")]
    public decimal UnitPrice { get; set; }

    [StringLength(200)]
    [Display(Name = "Tên món (snapshot)")]
    public string? ItemName { get; set; }

    [Display(Name = "Ngày tạo")]
    public DateTime CreatedAt { get; set; } = DateTime.Now;

    [Display(Name = "Ngày cập nhật")]
    public DateTime? UpdatedAt { get; set; }

    [NotMapped]
    [Display(Name = "Thành tiền")]
    public decimal SubTotal => UnitPrice * Quantity;

    // Navigation
    public Booking? Booking { get; set; }
    public FoodItem? FoodItem { get; set; }
}
