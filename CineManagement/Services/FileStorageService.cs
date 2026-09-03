using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;

namespace CineManagement.Services;

public class FileStorageService : IFileStorageService
{
    private readonly IWebHostEnvironment _webHostEnvironment;
    private static readonly string[] AllowedExtensions = { ".jpg", ".jpeg", ".png", ".webp", ".gif" };
    private const long MaxFileSizeBytes = 5 * 1024 * 1024; // 5 MB

    public FileStorageService(IWebHostEnvironment webHostEnvironment)
    {
        _webHostEnvironment = webHostEnvironment;
    }

    public async Task<string> SaveImageAsync(IFormFile file, string folderName)
    {
        if (file == null || file.Length == 0)
            throw new ArgumentException("File không hợp lệ hoặc rỗng.", nameof(file));

        var uploadsFolder = Path.Combine(_webHostEnvironment.WebRootPath, "uploads", folderName);
        if (!Directory.Exists(uploadsFolder))
        {
            Directory.CreateDirectory(uploadsFolder);
        }

        var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
        var uniqueFileName = $"{Guid.NewGuid()}{ext}";
        var filePath = Path.Combine(uploadsFolder, uniqueFileName);

        using (var fileStream = new FileStream(filePath, FileMode.Create))
        {
            await file.CopyToAsync(fileStream);
        }

        return $"/uploads/{folderName}/{uniqueFileName}";
    }

    public void DeleteFile(string? relativeUrl)
    {
        if (string.IsNullOrWhiteSpace(relativeUrl))
            return;

        // Strip leading slash if present
        var cleanPath = relativeUrl.TrimStart('/').Replace('/', Path.DirectorySeparatorChar);
        var fullPath = Path.Combine(_webHostEnvironment.WebRootPath, cleanPath);

        if (File.Exists(fullPath))
        {
            try
            {
                File.Delete(fullPath);
            }
            catch (Exception ex)
            {
                // Log warning or exception if file is in use
                System.Diagnostics.Debug.WriteLine($"Không thể xóa file {fullPath}: {ex.Message}");
            }
        }
    }

    public bool IsValidImage(IFormFile file, out string? errorMessage)
    {
        errorMessage = null;

        if (file == null || file.Length == 0)
        {
            errorMessage = "Vui lòng chọn tập tin ảnh.";
            return false;
        }

        if (file.Length > MaxFileSizeBytes)
        {
            errorMessage = "Dung lượng ảnh vượt quá giới hạn tối đa (5MB).";
            return false;
        }

        var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
        if (!AllowedExtensions.Contains(ext))
        {
            errorMessage = $"Định dạng tập tin '{ext}' không được hỗ trợ. Vui lòng chọn file ảnh (.jpg, .jpeg, .png, .webp).";
            return false;
        }

        return true;
    }
}
