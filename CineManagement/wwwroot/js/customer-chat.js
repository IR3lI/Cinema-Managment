(() => {
    const root = document.querySelector("[data-cine-chat]");
    if (!root) return;

    const dialog = root.querySelector("dialog");
    const trigger = root.querySelector(".cine-chat__trigger");
    const messages = root.querySelector("[data-chat-messages]");
    const greeting = messages.firstElementChild.cloneNode(true);
    const status = root.querySelector("[data-chat-status]");
    const quick = root.querySelector("[data-chat-quick]");
    const form = root.querySelector("form");
    const input = form.elements.message;
    const sendButton = form.querySelector('[type="submit"]');
    const token = form.elements.__RequestVerificationToken.value;
    let context = null;
    let history = [];
    let recentMovies = [];
    let pending = null;

    function appendMessage(text, items = [], fromUser = false) {
        const turn = document.createElement("div");
        turn.className = "cine-chat__turn";
        const bubble = document.createElement("p");
        bubble.className = "cine-chat__bubble" + (fromUser ? " cine-chat__bubble--user" : "");
        bubble.textContent = text;
        turn.append(bubble);
        for (const item of items) {
            const card = document.createElement("article");
            card.className = "cine-chat__result";
            const title = document.createElement("strong");
            title.textContent = item.title;
            const detail = document.createElement("p");
            detail.textContent = item.detail;
            card.append(title, detail);
            if (typeof item.url === "string" && item.url.startsWith("/") && !item.url.startsWith("//")) {
                const link = document.createElement("a");
                link.href = item.url;
                link.textContent = item.action + " →";
                card.append(link);
            }
            turn.append(card);
        }
        messages.append(turn);
        while (messages.childElementCount > 32) messages.firstElementChild.remove();
        messages.scrollTop = fromUser ? messages.scrollHeight : turn.offsetTop;
    }

    function showStatus(text = "") {
        status.textContent = text;
        status.hidden = !text;
        sendButton.disabled = Boolean(text);
        for (const button of quick.querySelectorAll("button")) button.disabled = Boolean(text);
    }

    async function send(text) {
        if (!text || pending) return;
        const request = new AbortController();
        pending = request;
        appendMessage(text, [], true);
        showStatus("Đang tra cứu…");
        try {
            const response = await fetch(root.dataset.endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json", RequestVerificationToken: token },
                body: JSON.stringify({ message: text, context, history, recentMovies }),
                signal: request.signal
            });
            const result = await response.json().catch(() => null);
            if (pending !== request) return;
            if (!response.ok) {
                const fallback = response.status === 429
                    ? "Trợ lý đang bận. Bạn thử lại sau nhé."
                    : "Mình chưa trả lời được lúc này. Bạn thử lại nhé.";
                appendMessage(result?.message || fallback);
                return;
            }
            if (typeof result?.text !== "string") throw new Error("Missing chat response");
            context = result.context ?? null;
            appendMessage(result.text, result.items ?? []);
            if (context?.intent === "movies" && result.items?.length > 1) {
                recentMovies = result.items.slice(0, 8).map(item => item.title.slice(0, 150));
            }
            const titles = (result.items ?? []).map(item => item.title).join(" | ");
            const reply = titles ? `Kết quả theo thứ tự: ${titles.slice(0, 200)}. ${result.text}` : result.text;
            history = [...history, { question: text.slice(0, 280), reply: reply.slice(0, 340) }].slice(-4);
        } catch (error) {
            if (pending === request) appendMessage("Kết nối bị gián đoạn. Bạn thử lại nhé.");
        } finally {
            if (pending === request) {
                pending = null;
                showStatus();
            }
        }
    }

    trigger.addEventListener("click", () => {
        dialog.showModal();
        trigger.setAttribute("aria-expanded", "true");
    });
    dialog.addEventListener("close", () => trigger.setAttribute("aria-expanded", "false"));
    root.querySelector("[data-chat-close]").addEventListener("click", () => dialog.close());
    root.querySelector("[data-chat-reset]").addEventListener("click", () => {
        pending?.abort();
        pending = null;
        context = null;
        history = [];
        recentMovies = [];
        messages.replaceChildren(greeting.cloneNode(true));
        showStatus();
        input.value = "";
        input.focus();
    });
    quick.addEventListener("click", event => {
        const button = event.target.closest("button");
        if (button) send(button.textContent.trim());
    });
    form.addEventListener("submit", event => {
        event.preventDefault();
        const question = input.value.trim();
        if (!question || pending) return;
        input.value = "";
        send(question);
    });
})();
