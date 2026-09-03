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
            .WithMany()
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

        // Booking -> User
        builder.Entity<Booking>()
            .HasOne(b => b.User)
            .WithMany()
            .HasForeignKey(b => b.UserId)
            .OnDelete(DeleteBehavior.Restrict);

        // Booking -> Showtime
        builder.Entity<Booking>()
            .HasOne(b => b.Showtime)
            .WithMany()
            .HasForeignKey(b => b.ShowtimeId)
            .OnDelete(DeleteBehavior.Restrict);

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
    }
}
