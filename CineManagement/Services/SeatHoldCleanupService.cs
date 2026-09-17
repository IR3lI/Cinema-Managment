using CineManagement.Data;
using CineManagement.Models;
using Microsoft.EntityFrameworkCore;

namespace CineManagement.Services;

/// <summary>
/// SCRUM-20: Runs every 5 minutes and releases seat holds that have expired,
/// marking their parent Booking as Expired if still Pending.
/// </summary>
public class SeatHoldCleanupService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<SeatHoldCleanupService> _logger;

    public SeatHoldCleanupService(IServiceScopeFactory scopeFactory,
                                  ILogger<SeatHoldCleanupService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await CleanupExpiredHoldsAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }

    private async Task CleanupExpiredHoldsAsync(CancellationToken cancellationToken)
    {
        try
        {
            using var scope = _scopeFactory.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

            var now = DateTime.Now;

            // Luồng mới dùng HoldSeat. Chỉ cập nhật trạng thái để giữ audit trail;
            // ghế trở thành khả dụng ngay vì mọi query availability đều lọc ExpiresAt.
            var expiredHolds = await context.HoldSeats
                .Where(h => h.Status == HoldSeatStatus.Active && h.ExpiresAt <= now)
                .ToListAsync(cancellationToken);

            foreach (var hold in expiredHolds)
            {
                hold.Status = HoldSeatStatus.Expired;
                hold.UpdatedAt = now;
            }

            // Find all Pending bookings whose hold has expired
            var expiredBookings = await context.Bookings
                .Include(b => b.BookedSeats)
                .Where(b => b.Status == BookingStatus.Pending)
                .ToListAsync();

            var toExpire = expiredBookings
                .Where(b => b.BookedSeats.Any(s => s.HoldUntil.HasValue && s.HoldUntil < now))
                .ToList();

            foreach (var booking in toExpire)
            {
                booking.Status = BookingStatus.Expired;
                _logger.LogInformation("Booking {BookingId} ({Code}) expired – seats released.", booking.BookingId, booking.BookingCode);
            }

            if (expiredHolds.Count > 0 || toExpire.Count > 0)
                await context.SaveChangesAsync(cancellationToken);

            if (expiredHolds.Count > 0)
                _logger.LogInformation("Released {Count} expired seat holds.", expiredHolds.Count);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during seat hold cleanup.");
        }
    }
}
