using System.ComponentModel.DataAnnotations;

namespace CineManagement.Modules.CustomerSupport;

public sealed class OllamaOptions
{
    public bool Enabled { get; set; } = true;
    public string BaseUrl { get; set; } = "http://127.0.0.1:11434/";
    public string Model { get; set; } = "qwen3:4b";
    public int TimeoutSeconds { get; set; } = 45;
}

public sealed record ChatRequest(
    [Required, StringLength(450)] string Message,
    ChatContext? Context,
    [MaxLength(4)] ChatTurn[]? History = null,
    [MaxLength(8)] string[]? RecentMovies = null);

public sealed record ChatTurn(
    [Required, StringLength(280)] string Question,
    [Required, StringLength(340)] string Reply);

public sealed record ChatContext(
    [StringLength(16)] string? Intent = null,
    [StringLength(150)] string? Movie = null,
    [StringLength(100)] string? Genre = null,
    [StringLength(150)] string? Cinema = null,
    [StringLength(10)] string? Date = null,
    [StringLength(5)] string? AfterTime = null,
    [StringLength(12)] string? MovieStatus = null);

public sealed record ChatItem(string Title, string Detail, int? MovieId = null, int? ShowtimeId = null);

public sealed record ChatReply(string Text, ChatContext? Context, IReadOnlyList<ChatItem> Items);

internal sealed record ChatInterpretation(
    string Intent, bool FollowUp, string? Movie, string? Genre, string? Cinema,
    string? Date, string? AfterTime, string? MovieStatus, string? Answer);
