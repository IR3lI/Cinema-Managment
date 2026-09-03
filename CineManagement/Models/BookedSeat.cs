using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace CineManagement.Models;

public class BookedSeat
{
    public int BookedSeatId { get; set; }

    [Required]
    public int BookingId { get; set; }

    [Required]
    public int SeatId { get; set; }

    [Column(TypeName = "decimal(15,0)")]
    [Display(Name = "Giá ghế")]
    public decimal SeatPrice { get; set; }

    // When the hold expires (for Pending bookings)
    [Display(Name = "Giữ đến")]
    public DateTime? HoldUntil { get; set; }

    // Navigation
    public Booking? Booking { get; set; }
    public Seat? Seat { get; set; }
}
