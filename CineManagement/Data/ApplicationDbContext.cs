using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using CineManagement.Models;

namespace CineManagement.Data;

public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    // Sprint 1
    public DbSet<Movie> Movies { get; set; }
    public DbSet<Genre> Genres { get; set; }
    public DbSet<Staff> Staffs { get; set; }

    // Sprint 2
    public DbSet<ScreeningRoom> ScreeningRooms { get; set; }
    public DbSet<Seat> Seats { get; set; }
    public DbSet<Showtime> Showtimes { get; set; }
    public DbSet<FoodItem> FoodItems { get; set; }

    // Sprint 3
    public DbSet<Voucher> Vouchers { get; set; }
    public DbSet<Booking> Bookings { get; set; }
    public DbSet<BookedSeat> BookedSeats { get; set; }
    public DbSet<BookingFoodItem> BookingFoodItems { get; set; }
    public DbSet<Ticket> Tickets { get; set; }
    public DbSet<OrderFnB> OrderFnBs { get; set; }
    public DbSet<HoldSeat> HoldSeats { get; set; }
    public DbSet<Review> Reviews { get; set; }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        // Staff -> User (one-to-one)
        builder.Entity<Staff>()
            .HasOne(s => s.User)
            .WithOne(u => u.Staff)
            .HasForeignKey<Staff>(s => s.UserId);

        // Movie -> Genre (many-to-one)
        builder.Entity<Movie>()
            .HasOne(m => m.Genre)
            .WithMany(g => g.Movies)
            .HasForeignKey(m => m.GenreId)
            .OnDelete(DeleteBehavior.SetNull);

        // Seat -> ScreeningRoom (many-to-one)
        builder.Entity<Seat>()
            .HasOne(s => s.Room)
            .WithMany(r => r.Seats)
            .HasForeignKey(s => s.RoomId)
            .OnDelete(DeleteBehavior.Cascade);

        // Showtime -> Movie (many-to-one)
        builder.Entity<Showtime>()
            .HasOne(st => st.Movie)
            .WithMany(m => m.Showtimes)
            .HasForeignKey(st => st.MovieId)
            .OnDelete(DeleteBehavior.Cascade);

        // Showtime -> ScreeningRoom (many-to-one)
        builder.Entity<Showtime>()
            .HasOne(st => st.Room)
            .WithMany(r => r.Showtimes)
            .HasForeignKey(st => st.RoomId)
            .OnDelete(DeleteBehavior.Cascade);

        // Primary keys
        builder.Entity<ScreeningRoom>()
            .HasKey(r => r.RoomId);

        // Ignore computed properties
        builder.Entity<ScreeningRoom>().Ignore(r => r.Capacity);
        builder.Entity<Seat>().Ignore(s => s.SeatCode);
        builder.Entity<BookingFoodItem>().Ignore(b => b.SubTotal);
        builder.Entity<OrderFnB>().Ignore(o => o.SubTotal);
        builder.Entity<HoldSeat>().Ignore(h => h.IsActive);

        // Booking -> User
        builder.Entity<Booking>()
            .HasOne(b => b.User)
            .WithMany(u => u.Bookings)
            .HasForeignKey(b => b.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        // Booking -> Showtime
        builder.Entity<Booking>()
            .HasOne(b => b.Showtime)
            .WithMany(st => st.Bookings)
            .HasForeignKey(b => b.ShowtimeId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<Booking>()
            .HasIndex(b => b.BookingCode)
            .IsUnique();

        // Booking -> Voucher (optional)
        builder.Entity<Booking>()
            .HasOne(b => b.Voucher)
            .WithMany(v => v.Bookings)
            .HasForeignKey(b => b.VoucherId)
            .OnDelete(DeleteBehavior.SetNull);

        // BookedSeat -> Booking
        builder.Entity<BookedSeat>()
            .HasOne(bs => bs.Booking)
            .WithMany(b => b.BookedSeats)
            .HasForeignKey(bs => bs.BookingId)
            .OnDelete(DeleteBehavior.Cascade);

        // BookedSeat -> Seat
        builder.Entity<BookedSeat>()
            .HasOne(bs => bs.Seat)
            .WithMany()
            .HasForeignKey(bs => bs.SeatId)
            .OnDelete(DeleteBehavior.Restrict);

        // BookingFoodItem -> Booking
        builder.Entity<BookingFoodItem>()
            .HasOne(bf => bf.Booking)
            .WithMany(b => b.BookingFoodItems)
            .HasForeignKey(bf => bf.BookingId)
            .OnDelete(DeleteBehavior.Cascade);

        // BookingFoodItem -> FoodItem
        builder.Entity<BookingFoodItem>()
            .HasOne(bf => bf.FoodItem)
            .WithMany()
            .HasForeignKey(bf => bf.FoodItemId)
            .OnDelete(DeleteBehavior.Restrict);

        // Unique index on Voucher.Code
        builder.Entity<Voucher>()
            .HasIndex(v => v.Code)
            .IsUnique();

        // Ticket -> Booking
        builder.Entity<Ticket>()
            .HasOne(t => t.Booking)
            .WithMany(b => b.Tickets)
            .HasForeignKey(t => t.BookingId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.Entity<Ticket>()
            .HasOne(t => t.Showtime)
            .WithMany(st => st.Tickets)
            .HasForeignKey(t => t.ShowtimeId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<Ticket>()
            .HasOne(t => t.Seat)
            .WithMany(s => s.Tickets)
            .HasForeignKey(t => t.SeatId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<Ticket>()
            .HasOne(t => t.CheckedInBy)
            .WithMany()
            .HasForeignKey(t => t.CheckedInByUserId)
            .OnDelete(DeleteBehavior.SetNull);

        builder.Entity<Ticket>()
            .HasIndex(t => t.TicketCode)
            .IsUnique();

        builder.Entity<Ticket>()
            .HasIndex(t => new { t.BookingId, t.SeatId })
            .IsUnique();

        // Ghế đã bán / đang phát hành: không cho 2 vé sống cùng suất + ghế
        builder.Entity<Ticket>()
            .HasIndex(t => new { t.ShowtimeId, t.SeatId })
            .IsUnique()
            .HasFilter("\"Status\" IN (0, 1, 2)");

        // OrderFnB -> Booking
        builder.Entity<OrderFnB>()
            .HasOne(o => o.Booking)
            .WithMany(b => b.OrderFnBs)
            .HasForeignKey(o => o.BookingId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.Entity<OrderFnB>()
            .HasOne(o => o.FoodItem)
            .WithMany(f => f.OrderFnBs)
            .HasForeignKey(o => o.FoodItemId)
            .OnDelete(DeleteBehavior.Restrict);

        // HoldSeat
        builder.Entity<HoldSeat>()
            .HasOne(h => h.Showtime)
            .WithMany(st => st.HoldSeats)
            .HasForeignKey(h => h.ShowtimeId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<HoldSeat>()
            .HasOne(h => h.Seat)
            .WithMany(s => s.HoldSeats)
            .HasForeignKey(h => h.SeatId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<HoldSeat>()
            .HasOne(h => h.User)
            .WithMany(u => u.HoldSeats)
            .HasForeignKey(h => h.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<HoldSeat>()
            .HasOne(h => h.Booking)
            .WithMany(b => b.HoldSeats)
            .HasForeignKey(h => h.BookingId)
            .OnDelete(DeleteBehavior.SetNull);

        // SQLite: một ghế / suất chỉ được Active-hold một lần
        builder.Entity<HoldSeat>()
            .HasIndex(h => new { h.ShowtimeId, h.SeatId })
            .IsUnique()
            .HasFilter("\"Status\" = 0");

        builder.Entity<HoldSeat>()
            .HasIndex(h => h.ExpiresAt);

        // Review: 1 user / 1 phim
        builder.Entity<Review>()
            .HasOne(r => r.Movie)
            .WithMany(m => m.Reviews)
            .HasForeignKey(r => r.MovieId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.Entity<Review>()
            .HasOne(r => r.User)
            .WithMany(u => u.Reviews)
            .HasForeignKey(r => r.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.Entity<Review>()
            .HasIndex(r => new { r.UserId, r.MovieId })
            .IsUnique();
    }
}
