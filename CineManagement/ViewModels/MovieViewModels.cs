using System.ComponentModel.DataAnnotations;
using CineManagement.Models;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace CineManagement.ViewModels;

// ── Create / Edit Movie ───────────────────────────────────────────────────────
public class MovieFormViewModel
{
    public int MovieId { get; set; }

    [Required(ErrorMessage = "Tên phim không được để trống")]
    [StringLength(200)]
    [Display(Name = "Tên phim")]
    public string Title { get; set; } = string.Empty;

    [StringLength(2000)]
    [Display(Name = "Mô tả")]
    public string? Description { get; set; }

    [StringLength(200)]
    [Display(Name = "Đạo diễn")]
    public string? Director { get; set; }

    [StringLength(500)]
    [Display(Name = "Diễn viên")]
    public string? Actors { get; set; }

    [Required(ErrorMessage = "Vui lòng nhập thời lượng")]
    [Range(1, 600, ErrorMessage = "Thời lượng phải từ 1 đến 600 phút")]
    [Display(Name = "Thời lượng (phút)")]
    public int Duration { get; set; }

    [Display(Name = "Ngày khởi chiếu")]
    [DataType(DataType.Date)]
    public DateTime? ReleaseDate { get; set; }

    [Display(Name = "Ngày kết thúc")]
    [DataType(DataType.Date)]
    public DateTime? EndDate { get; set; }

    public string? PosterUrl { get; set; }

    [Display(Name = "Ảnh bìa phim")]
    public IFormFile? PosterFile { get; set; }

    [StringLength(500)]
    [Display(Name = "Trailer URL (YouTube)")]
    public string? TrailerUrl { get; set; }

    [Display(Name = "Trạng thái")]
    public MovieStatus Status { get; set; } = MovieStatus.ComingSoon;

    [Range(0, 10)]
    [Display(Name = "Điểm đánh giá (0–10)")]
    public decimal Rating { get; set; } = 0;

    [StringLength(10)]
    [Display(Name = "Phân loại độ tuổi")]
    public string? AgeRating { get; set; }

    [StringLength(100)]
    [Display(Name = "Ngôn ngữ")]
    public string? Language { get; set; } = "Tiếng Việt";

    [Display(Name = "Thể loại")]
    public int? GenreId { get; set; }

    // Select list for dropdown
    public IEnumerable<SelectListItem> Genres { get; set; } = new List<SelectListItem>();
    public IEnumerable<SelectListItem> AgeRatings { get; set; } = new List<SelectListItem>
    {
        new("P – Mọi lứa tuổi", "P"),
        new("C13 – Trên 13 tuổi", "C13"),
        new("C16 – Trên 16 tuổi", "C16"),
        new("C18 – Trên 18 tuổi", "C18"),
    };
}

// ── Movie Index (filter/search) ───────────────────────────────────────────────
public class MovieIndexViewModel
{
    public IEnumerable<Movie> Movies { get; set; } = new List<Movie>();
    public string? SearchTerm { get; set; }
    public int? GenreId { get; set; }
    public MovieStatus? Status { get; set; }
    public IEnumerable<SelectListItem> Genres { get; set; } = new List<SelectListItem>();
}
