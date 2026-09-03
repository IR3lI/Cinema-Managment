using Microsoft.AspNetCore.Identity;
using CineManagement.Models;

namespace CineManagement.Data;

public static class SeedData
{
    public static async Task InitializeAsync(IServiceProvider serviceProvider)
    {
        var roleManager = serviceProvider.GetRequiredService<RoleManager<IdentityRole>>();
        var userManager = serviceProvider.GetRequiredService<UserManager<ApplicationUser>>();
        var context = serviceProvider.GetRequiredService<ApplicationDbContext>();

        await context.Database.EnsureCreatedAsync();

        // ── Roles ──────────────────────────────────────────────
        string[] roles = { "Admin", "Staff", "Customer" };
        foreach (var role in roles)
        {
            if (!await roleManager.RoleExistsAsync(role))
                await roleManager.CreateAsync(new IdentityRole(role));
        }

        // ── Default Admin account ──────────────────────────────
        const string adminEmail = "admin@cinema.com";
        var adminUser = await userManager.FindByEmailAsync(adminEmail);
        if (adminUser == null)
        {
            adminUser = new ApplicationUser
            {
                UserName = adminEmail,
                Email = adminEmail,
                FullName = "Quản trị viên",
                EmailConfirmed = true,
                IsActive = true,
                CreatedAt = DateTime.Now
            };
            var result = await userManager.CreateAsync(adminUser, "Admin@123");
            if (result.Succeeded)
                await userManager.AddToRoleAsync(adminUser, "Admin");
        }

        // ── Test Staff account ──────────────────────────────────
        const string staffEmail = "staff@cinema.com";
        var staffUser = await userManager.FindByEmailAsync(staffEmail);
        if (staffUser == null)
        {
            staffUser = new ApplicationUser
            {
                UserName    = staffEmail,
                Email       = staffEmail,
                FullName    = "Nhân viên Test",
                EmailConfirmed = true,
                IsActive    = true,
                CreatedAt   = DateTime.Now
            };
            var result = await userManager.CreateAsync(staffUser, "Staff@123");
            if (result.Succeeded)
            {
                await userManager.AddToRoleAsync(staffUser, "Staff");
                // Also create Staff record
                if (!context.Staffs.Any(s => s.UserId == staffUser.Id))
                {
                    context.Staffs.Add(new Staff
                    {
                        UserId   = staffUser.Id,
                        Position = "Nhân viên bán vé",
                        IsActive = true,
                        HireDate = DateTime.Today
                    });
                    await context.SaveChangesAsync();
                }
            }
        }

        // ── Test Customer account ───────────────────────────────
        const string customerEmail = "customer@cinema.com";
        var customerUser = await userManager.FindByEmailAsync(customerEmail);
        if (customerUser == null)
        {
            customerUser = new ApplicationUser
            {
                UserName    = customerEmail,
                Email       = customerEmail,
                FullName    = "Khách hàng Test",
                EmailConfirmed = true,
                IsActive    = true,
                CreatedAt   = DateTime.Now
            };
            var result = await userManager.CreateAsync(customerUser, "Customer@123");
            if (result.Succeeded)
                await userManager.AddToRoleAsync(customerUser, "Customer");
        }

        // ── Seed Genres ────────────────────────────────────────
        if (!context.Genres.Any())
        {
            context.Genres.AddRange(
                new Genre { Name = "Hành động", Description = "Phim hành động, võ thuật" },
                new Genre { Name = "Hài hước", Description = "Phim hài, kịch tính nhẹ" },
                new Genre { Name = "Kinh dị", Description = "Phim kinh dị, rùng rợn" },
                new Genre { Name = "Tình cảm", Description = "Phim tình cảm, lãng mạn" },
                new Genre { Name = "Hoạt hình", Description = "Phim hoạt hình" },
                new Genre { Name = "Khoa học viễn tưởng", Description = "Phim sci-fi" },
                new Genre { Name = "Tâm lý", Description = "Phim tâm lý, kịch tính" }
            );
            await context.SaveChangesAsync();
        }

        // ── Seed Sample Movies ─────────────────────────────────
        if (!context.Movies.Any())
        {
            var actionGenre = context.Genres.FirstOrDefault(g => g.Name == "Hành động");
            var horrorGenre = context.Genres.FirstOrDefault(g => g.Name == "Kinh dị");
            var animGenre   = context.Genres.FirstOrDefault(g => g.Name == "Hoạt hình");

            context.Movies.AddRange(
                new Movie
                {
                    Title = "Avengers: Endgame",
                    Description = "Các siêu anh hùng Avengers chiến đấu với Thanos để cứu vũ trụ.",
                    Director = "Anthony & Joe Russo",
                    Actors = "Robert Downey Jr., Chris Evans, Scarlett Johansson",
                    Duration = 181,
                    ReleaseDate = new DateTime(2019, 4, 26),
                    Status = MovieStatus.NowShowing,
                    Rating = 8.4m,
                    AgeRating = "C13",
                    Language = "Phụ đề Việt",
                    GenreId = actionGenre?.GenreId,
                    IsActive = true
                },
                new Movie
                {
                    Title = "Kính Vạn Hoa",
                    Description = "Phim kinh dị tâm lý về những bí ẩn ẩn sau một căn nhà cũ.",
                    Director = "Nguyễn Văn An",
                    Duration = 105,
                    ReleaseDate = DateTime.Today.AddDays(7),
                    Status = MovieStatus.ComingSoon,
                    AgeRating = "C18",
                    Language = "Tiếng Việt",
                    GenreId = horrorGenre?.GenreId,
                    IsActive = true
                },
                new Movie
                {
                    Title = "Doraemon: Nobita và Robot Thiên Hà",
                    Description = "Nobita và Doraemon phiêu lưu trong thế giới robot.",
                    Director = "Takashi Yamazaki",
                    Duration = 95,
                    ReleaseDate = DateTime.Today.AddDays(-7),
                    Status = MovieStatus.NowShowing,
                    Rating = 7.5m,
                    AgeRating = "P",
                    Language = "Lồng tiếng Việt",
                    GenreId = animGenre?.GenreId,
                    IsActive = true
                }
            );
            await context.SaveChangesAsync();
        }

        // ── Seed Screening Rooms ────────────────────────────────
        if (!context.ScreeningRooms.Any())
        {
            var rooms = new List<ScreeningRoom>
            {
                new ScreeningRoom { RoomName = "Phòng 1 - Standard", RoomType = RoomType.Standard, Rows = 8, SeatsPerRow = 12, IsActive = true },
                new ScreeningRoom { RoomName = "Phòng 2 - VIP",      RoomType = RoomType.VIP,      Rows = 6, SeatsPerRow = 8,  IsActive = true },
                new ScreeningRoom { RoomName = "Phòng 3 - IMAX",     RoomType = RoomType.IMAX,     Rows = 10, SeatsPerRow = 16, IsActive = true }
            };
            context.ScreeningRooms.AddRange(rooms);
            await context.SaveChangesAsync();

            // Generate seats for each room
            foreach (var room in rooms)
            {
                var seats = new List<Seat>();
                for (int r = 0; r < room.Rows; r++)
                {
                    char rowChar = (char)('A' + r);
                    for (int s = 1; s <= room.SeatsPerRow; s++)
                    {
                        SeatType type = SeatType.Standard;
                        // Last 2 rows are VIP
                        if (r >= room.Rows - 2) type = SeatType.VIP;
                        // Last seat of each row in VIP rooms is Couple
                        if (room.RoomType == RoomType.VIP && s == room.SeatsPerRow) type = SeatType.Couple;

                        seats.Add(new Seat
                        {
                            RoomId = room.RoomId,
                            RowLabel = rowChar.ToString(),
                            SeatNumber = s,
                            SeatType = type,
                            IsActive = true
                        });
                    }
                }
                context.Seats.AddRange(seats);
            }
            await context.SaveChangesAsync();
        }

        // ── Seed Showtimes ─────────────────────────────────────
        if (!context.Showtimes.Any())
        {
            var movie1 = context.Movies.FirstOrDefault(m => m.Title == "Avengers: Endgame");
            var movie3 = context.Movies.FirstOrDefault(m => m.Title == "Doraemon: Nobita và Robot Thiên Hà");
            var room1  = context.ScreeningRooms.FirstOrDefault(r => r.RoomName.Contains("Standard"));
            var room2  = context.ScreeningRooms.FirstOrDefault(r => r.RoomName.Contains("VIP"));
            var room3  = context.ScreeningRooms.FirstOrDefault(r => r.RoomName.Contains("IMAX"));

            if (movie1 != null && room1 != null && room2 != null && room3 != null)
            {
                context.Showtimes.AddRange(
                    // Today
                    new Showtime { MovieId = movie1.MovieId, RoomId = room1.RoomId, StartTime = DateTime.Today.AddHours(9),  TicketPrice = 90000, Status = ShowtimeStatus.Available },
                    new Showtime { MovieId = movie1.MovieId, RoomId = room2.RoomId, StartTime = DateTime.Today.AddHours(13), TicketPrice = 150000, Status = ShowtimeStatus.Available },
                    new Showtime { MovieId = movie1.MovieId, RoomId = room3.RoomId, StartTime = DateTime.Today.AddHours(18), TicketPrice = 200000, Status = ShowtimeStatus.Available },
                    // Tomorrow
                    new Showtime { MovieId = movie1.MovieId, RoomId = room1.RoomId, StartTime = DateTime.Today.AddDays(1).AddHours(10), TicketPrice = 90000, Status = ShowtimeStatus.Available },
                    new Showtime { MovieId = movie1.MovieId, RoomId = room2.RoomId, StartTime = DateTime.Today.AddDays(1).AddHours(15), TicketPrice = 150000, Status = ShowtimeStatus.Available }
                );
            }

            if (movie3 != null && room1 != null)
            {
                context.Showtimes.AddRange(
                    new Showtime { MovieId = movie3.MovieId, RoomId = room1.RoomId, StartTime = DateTime.Today.AddHours(10), TicketPrice = 75000, Status = ShowtimeStatus.Available },
                    new Showtime { MovieId = movie3.MovieId, RoomId = room1.RoomId, StartTime = DateTime.Today.AddDays(1).AddHours(14), TicketPrice = 75000, Status = ShowtimeStatus.Available }
                );
            }

            await context.SaveChangesAsync();
        }
        else
        {
            // Auto-reschedule: if ALL Available showtimes are in the past, shift them to start from today.
            // This preserves admin-created showtimes while bumping stale seeded ones.
            var availableShowtimes = context.Showtimes
                .Where(s => s.Status == ShowtimeStatus.Available)
                .ToList();

            bool allPast = availableShowtimes.Any() && availableShowtimes.All(s => s.StartTime < DateTime.Now);
            if (allPast)
            {
                var oldest = availableShowtimes.Min(s => s.StartTime.Date);
                int daysDiff = (DateTime.Today - oldest).Days;
                foreach (var st in availableShowtimes)
                {
                    st.StartTime = st.StartTime.AddDays(daysDiff);
                    if (st.EndTime.HasValue)
                        st.EndTime = st.EndTime.Value.AddDays(daysDiff);
                }
                await context.SaveChangesAsync();
            }
        }

        // ── Seed F&B Items ─────────────────────────────────────
        if (!context.FoodItems.Any())
        {
            context.FoodItems.AddRange(
                new FoodItem { Name = "Bắp rang bơ nhỏ", Category = FoodCategory.Popcorn, Price = 49000, Description = "Bắp rang bơ size nhỏ thơm ngon", IsAvailable = true },
                new FoodItem { Name = "Bắp rang bơ vừa", Category = FoodCategory.Popcorn, Price = 65000, Description = "Bắp rang bơ size vừa", IsAvailable = true },
                new FoodItem { Name = "Bắp rang bơ lớn", Category = FoodCategory.Popcorn, Price = 79000, Description = "Bắp rang bơ size lớn", IsAvailable = true },
                new FoodItem { Name = "Coca-Cola 22oz", Category = FoodCategory.Drink, Price = 39000, Description = "Nước ngọt Coca-Cola size 22oz", IsAvailable = true },
                new FoodItem { Name = "Pepsi 22oz",     Category = FoodCategory.Drink, Price = 39000, Description = "Nước ngọt Pepsi size 22oz", IsAvailable = true },
                new FoodItem { Name = "Nước lọc",       Category = FoodCategory.Drink, Price = 20000, Description = "Nước lọc đóng chai", IsAvailable = true },
                new FoodItem { Name = "Combo 1: Bắp nhỏ + Coca", Category = FoodCategory.Combo, Price = 79000, Description = "1 bắp rang nhỏ + 1 Coca-Cola 22oz", IsAvailable = true },
                new FoodItem { Name = "Combo 2: Bắp lớn + 2 Coca", Category = FoodCategory.Combo, Price = 149000, Description = "1 bắp rang lớn + 2 Coca-Cola 22oz", IsAvailable = true },
                new FoodItem { Name = "Nachos",         Category = FoodCategory.Snack, Price = 55000, Description = "Nachos giòn với sốt phô mai", IsAvailable = true },
                new FoodItem { Name = "Hotdog",         Category = FoodCategory.Snack, Price = 45000, Description = "Xúc xích nướng bánh mì", IsAvailable = true }
            );
            await context.SaveChangesAsync();
        }

        // ── Seed Vouchers (Sprint 3) ────────────────────────────
        if (!context.Vouchers.Any())
        {
            context.Vouchers.AddRange(
                new Voucher
                {
                    Code = "CINEMA10",
                    Description = "Giảm 10% hóa đơn đặt vé",
                    DiscountPercent = 10,
                    MaxDiscountAmount = 50000,
                    ValidFrom = DateTime.Today,
                    ValidTo = DateTime.Today.AddDays(90),
                    IsActive = true
                },
                new Voucher
                {
                    Code = "NEWUSER20",
                    Description = "Ưu đãi khách hàng mới – Giảm 20%",
                    DiscountPercent = 20,
                    MaxDiscountAmount = 100000,
                    ValidFrom = DateTime.Today,
                    ValidTo = DateTime.Today.AddDays(30),
                    UsageLimit = 1,
                    IsActive = true
                },
                new Voucher
                {
                    Code = "VIP30",
                    Description = "Ưu đãi VIP – Giảm 30% (tối đa 150k)",
                    DiscountPercent = 30,
                    MaxDiscountAmount = 150000,
                    ValidFrom = DateTime.Today,
                    ValidTo = DateTime.Today.AddDays(60),
                    IsActive = true
                }
            );
            await context.SaveChangesAsync();
        }
    }
}
