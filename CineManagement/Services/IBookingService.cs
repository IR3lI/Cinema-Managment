using CineManagement.DTOs;

namespace CineManagement.Services;

/// <summary>Core booking flow Sprint 3: sơ đồ ghế → giữ ghế → tính tiền → tạo đơn / thanh toán.</summary>
public interface IBookingService
{
    /// <summary>Sơ đồ ghế của suất chiếu, trạng thái Trống / Đang giữ / Đã bán.</summary>
    Task<SeatMapDto> GetSeatMapAsync(
        int showtimeId,
        string? userId,
        CancellationToken cancellationToken = default);

    /// <summary>Giữ ghế tạm thời (DB HoldSeat). Trả về ghế conflict nếu không giữ được.</summary>
    Task<HoldSeatResponseDto> HoldSeatAsync(
        string userId,
        HoldSeatRequestDto request,
        CancellationToken cancellationToken = default);

    /// <summary>Tính breakdown vé + F&amp;B + voucher, không ghi đơn.</summary>
    Task<BookingResponseDto> CalculateTotalAmountAsync(
        BookingRequestDto request,
        string? userId = null,
        CancellationToken cancellationToken = default);

    /// <summary>Tạo Booking + Ticket + OrderFnB, chuyển HoldSeat sang Converted khi thanh toán.</summary>
    Task<BookingResponseDto> CreateBookingAsync(
        string userId,
        BookingRequestDto request,
        CancellationToken cancellationToken = default);
}
