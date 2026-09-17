namespace CineManagement.DTOs;

public sealed record DailyRevenueDto
{
    public DateTime Date { get; init; }
    public int BookingCount { get; init; }
    public decimal Revenue { get; init; }
}

public sealed record TopMovieDto
{
    public int MovieId { get; init; }
    public string MovieTitle { get; init; } = string.Empty;
    public int TicketsSold { get; init; }
    public decimal TicketRevenue { get; init; }
}

public sealed record RoomOccupancyRateDto
{
    public int ShowtimeId { get; init; }
    public int RoomId { get; init; }
    public string RoomName { get; init; } = string.Empty;
    public int TotalSeats { get; init; }
    public int SoldSeats { get; init; }
    public decimal OccupancyRate { get; init; }
}
