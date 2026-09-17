using CineManagement.Data;
using CineManagement.Models;
using Microsoft.EntityFrameworkCore;

namespace CineManagement.Services;

/// <summary>
/// SCRUM-20: Periodically removes expired temporary seat holds.
/// A new scope is required because hosted services are singletons whereas
/// <see cref="ApplicationDbContext"/> is registered as scoped.
/// </summary>
public sealed class SeatHoldTimeoutWorker : BackgroundService
{
    private static readonly TimeSpan PollInterval = TimeSpan.FromMinutes(1);

    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<SeatHoldTimeoutWorker> _logger;

    public SeatHoldTimeoutWorker(
        IServiceProvider serviceProvider,
        ILogger<SeatHoldTimeoutWorker> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(PollInterval);

        // Run once at startup, then every minute. Availability queries still
        // check the expiry timestamp, so a seat is never blocked between scans.
        do
        {
            await RemoveExpiredHoldsAsync(stoppingToken);
        }
        while (await timer.WaitForNextTickAsync(stoppingToken));
    }

    private async Task RemoveExpiredHoldsAsync(CancellationToken cancellationToken)
    {
        try
        {
            using var scope = _serviceProvider.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            var now = DateTime.UtcNow;

            var expiredHolds = await db.HoldSeats
                // Converted holds belong to a completed booking and are retained
                // as audit data; only temporary active holds are released.
                .Where(hold => hold.Status == HoldSeatStatus.Active && hold.ExpiresAt < now)
                .ToListAsync(cancellationToken);

            if (expiredHolds.Count == 0)
                return;

            db.HoldSeats.RemoveRange(expiredHolds);
            await db.SaveChangesAsync(cancellationToken);

            _logger.LogInformation("Deleted {Count} expired seat holds.", expiredHolds.Count);
        }
        catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
        {
            // Normal application shutdown.
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unable to remove expired seat holds.");
        }
    }
}
