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
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
            await CleanupExpiredHoldsAsync();
        }
    }

    private async Task CleanupExpiredHoldsAsync()
    {
        try
        {
            using var scope = _scopeFactory.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

            var now = DateTime.Now;

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

            if (toExpire.Count > 0)
                await context.SaveChangesAsync();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during seat hold cleanup.");
        }
    }
}
