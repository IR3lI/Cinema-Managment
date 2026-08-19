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

        // Ensure DB is created / migrated
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
                    Status = MovieStatus.Ended,
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
                    Director = "Nguyễn Văn A",
                    Duration = 105,
                    ReleaseDate = DateTime.Today.AddDays(14),
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
    }
}
