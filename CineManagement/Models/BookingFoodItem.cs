using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

public class BookingFoodItem
{
    public int BookingFoodItemId { get; set; }

    [Required]
    public int BookingId { get; set; }

    [Required]
    public int FoodItemId { get; set; }

    [Range(1, 20)]
    [Display(Name = "Số lượng")]
    public int Quantity { get; set; } = 1;

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Đơn giá")]
    public decimal UnitPrice { get; set; }

    // Computed
    public decimal SubTotal => UnitPrice * Quantity;

    // Navigation
    public Booking? Booking { get; set; }
    public FoodItem? FoodItem { get; set; }
}
