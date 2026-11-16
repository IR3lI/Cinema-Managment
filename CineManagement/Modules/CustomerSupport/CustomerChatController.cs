using System.Data.Common;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.Extensions.Options;

namespace CineManagement.Modules.CustomerSupport;

[ApiController]
[Route("api/chat")]
[EnableRateLimiting("customer-chat")]
public sealed class CustomerChatController(
    IOptions<OllamaOptions> config, ChatCapacity capacity, ILogger<CustomerChatController> logger) : ControllerBase
{
    [HttpPost]
    [ValidateAntiForgeryToken]
    [RequestSizeLimit(16384)]
    public async Task<IActionResult> Send(ChatRequest request, CancellationToken ct)
    {
        if (!config.Value.Enabled)
            return NotFound();
        if (string.IsNullOrWhiteSpace(request.Message))
            return BadRequest(new { message = "Bạn nhập câu hỏi giúp mình nhé." });
        if (!await capacity.Slots.WaitAsync(0, ct))
            return StatusCode(429, new { message = "Trợ lý đang bận. Bạn thử lại sau ít giây nhé." });

        try
        {
            var service = HttpContext.RequestServices.GetRequiredService<CustomerSupportService>();
            var reply = await service.ReplyAsync(request, ct);
            return Ok(new
            {
                reply.Text,
                reply.Context,
                Items = reply.Items.Select(item => new
                {
                    item.Title,
                    item.Detail,
                    Url = item.ShowtimeId is int showtimeId
                        ? Url.Action("SelectSeat", "Booking", new { showtimeId })
                        : item.MovieId is int id ? Url.Action("MovieDetail", "Home", new { id }) : null,
                    Action = item.ShowtimeId.HasValue ? "Xem ghế" : "Xem phim"
                })
            });
        }
        catch (OperationCanceledException) when (!ct.IsCancellationRequested)
        {
            return StatusCode(504, new { message = "Trợ lý phản hồi chậm. Bạn thử lại hoặc dùng mục Phim đang chiếu nhé." });
        }
        catch (DbException ex)
        {
            logger.LogWarning(ex, "Customer chat could not read cinema data.");
            return StatusCode(503, new { message = "Mình chưa kết nối được dữ liệu rạp. Bạn thử lại sau nhé." });
        }
        catch (Exception ex) when (ex is HttpRequestException or JsonException or UriFormatException)
        {
            logger.LogWarning(ex, "Customer chat could not get a valid Ollama response.");
            return StatusCode(503, new { message = "Trợ lý tạm thời chưa sẵn sàng. Bạn có thể tiếp tục xem phim và đặt vé trên website." });
        }
        finally
        {
            capacity.Slots.Release();
        }
    }
}
