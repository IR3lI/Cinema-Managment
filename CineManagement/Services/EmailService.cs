using System.Net;
using System.Net.Mail;
using System.Text;
using System.Text.Encodings.Web;
using CineManagement.DTOs;
using Microsoft.Extensions.Options;

namespace CineManagement.Services;

public sealed class SmtpOptions
{
    public const string SectionName = "Smtp";
    public string Host { get; init; } = string.Empty;
    public int Port { get; init; } = 587;
    public bool EnableSsl { get; init; } = true;
    public string UserName { get; init; } = string.Empty;
    public string Password { get; init; } = string.Empty;
    public string FromEmail { get; init; } = string.Empty;
    public string FromName { get; init; } = "Cinema Management";
    public string CinemaName { get; init; } = "Cinema Management";
}

public sealed class EmailService : IEmailService
{
    private readonly SmtpOptions _options;
    private readonly ILogger<EmailService> _logger;

    public EmailService(IOptions<SmtpOptions> options, ILogger<EmailService> logger)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task SendTicketEmailAsync(
        string toEmail,
        OrderResponseDto orderDetails,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(_options.Host) || string.IsNullOrWhiteSpace(_options.FromEmail))
            throw new InvalidOperationException("SMTP chưa được cấu hình. Thiết lập section 'Smtp' bằng User Secrets hoặc biến môi trường.");

        using var message = new MailMessage
        {
            From = new MailAddress(_options.FromEmail, _options.FromName),
            Subject = $"Vé điện tử {orderDetails.BookingCode} - {orderDetails.MovieTitle}",
            Body = BuildTicketHtml(orderDetails),
            IsBodyHtml = true,
            BodyEncoding = Encoding.UTF8,
            SubjectEncoding = Encoding.UTF8
        };
        message.To.Add(new MailAddress(toEmail));

        using var client = new SmtpClient(_options.Host, _options.Port)
        {
            EnableSsl = _options.EnableSsl,
            Credentials = string.IsNullOrWhiteSpace(_options.UserName)
                ? CredentialCache.DefaultNetworkCredentials
                : new NetworkCredential(_options.UserName, _options.Password)
        };

        await client.SendMailAsync(message, cancellationToken);
        _logger.LogInformation("Sent e-ticket for booking {BookingCode} to {Email}.", orderDetails.BookingCode, toEmail);
    }

    private static string BuildTicketHtml(OrderResponseDto order)
    {
        static string Encode(string? value) => HtmlEncoder.Default.Encode(value ?? string.Empty);

        var tickets = string.Join(string.Empty, order.Tickets.Select(ticket => $"""
            <li><strong>{Encode(ticket.SeatCode)}</strong> — {Encode(ticket.TicketCode)}</li>
            """));

        return $"""
            <!doctype html>
            <html><body style="font-family:Arial,sans-serif;color:#1f2937">
              <h2>Vé điện tử của bạn</h2>
              <p><strong>Mã đặt vé:</strong> {Encode(order.BookingCode)}</p>
              <p><strong>Phim:</strong> {Encode(order.MovieTitle)}</p>
              <p><strong>Rạp:</strong> {Encode(order.CinemaName)}</p>
              <p><strong>Phòng chiếu:</strong> {Encode(order.RoomName)}</p>
              <p><strong>Giờ chiếu:</strong> {order.StartTime:dd/MM/yyyy HH:mm}</p>
              <p><strong>Ghế:</strong></p><ul>{tickets}</ul>
              <p>Vui lòng xuất trình mã QR hoặc mã vé tại quầy soát vé.</p>
            </body></html>
            """;
    }
}
