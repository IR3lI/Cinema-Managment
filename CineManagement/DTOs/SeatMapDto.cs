using System.ComponentModel.DataAnnotations;
using CineManagement.Models;

namespace CineManagement.DTOs;

public enum SeatAvailabilityStatus
{
    [Display(Name = "Trống")]
    Available = 0,

    [Display(Name = "Đang giữ")]
    Held = 1,

    [Display(Name = "Đã bán")]
    Sold = 2
}

public sealed record SeatCellDto
{
    public int SeatId { get; init; }

    [Required]
    [StringLength(10)]
    public string SeatCode { get; init; } = string.Empty;

    [Required]
    [StringLength(2)]
    public string RowLabel { get; init; } = string.Empty;

    public int SeatNumber { get; init; }

    public SeatType SeatType { get; init; }

    public SeatAvailabilityStatus Status { get; init; }

    /// <summary>True khi ghế đang được chính user hiện tại giữ.</summary>
    public bool IsHeldByCurrentUser { get; init; }

    [Range(0, double.MaxValue)]
    public decimal Price { get; init; }
}

public sealed record SeatRowDto
{
    [Required]
    [StringLength(2)]
    public string RowLabel { get; init; } = string.Empty;

    [Required]
    [MinLength(1)]
    public IReadOnlyList<SeatCellDto> Seats { get; init; } = [];
}

/// <summary>Sơ đồ ghế của một suất chiếu kèm trạng thái Trống / Đang giữ / Đã bán.</summary>
public sealed record SeatMapDto
{
    [Range(1, int.MaxValue)]
    public int ShowtimeId { get; init; }

    [Range(1, int.MaxValue)]
    public int MovieId { get; init; }

    [Required]
    [StringLength(200)]
    public string MovieTitle { get; init; } = string.Empty;

    [Range(1, int.MaxValue)]
    public int RoomId { get; init; }

    [Required]
    [StringLength(100)]
    public string RoomName { get; init; } = string.Empty;

    public DateTime StartTime { get; init; }

    [Range(0, double.MaxValue)]
    public decimal BaseTicketPrice { get; init; }

    public int TotalSeats { get; init; }

    public int AvailableSeats { get; init; }

    public DateTime? MyHoldExpiresAt { get; init; }

    [Required]
    [MinLength(1)]
    public IReadOnlyList<SeatRowDto> Rows { get; init; } = [];
}
