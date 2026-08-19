using Microsoft.AspNetCore.Identity;
using System.ComponentModel.DataAnnotations;

namespace CineManagement.Models;

public class ApplicationUser : IdentityUser
{
    [Required]
    [StringLength(100)]
    public string FullName { get; set; } = string.Empty;

    public DateTime? DateOfBirth { get; set; }

    [StringLength(200)]
    public string? AvatarUrl { get; set; }

    [StringLength(500)]
    public string? Address { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.Now;

    public bool IsActive { get; set; } = true;

    // Navigation
    public Staff? Staff { get; set; }
}
