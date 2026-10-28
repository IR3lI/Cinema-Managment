// State
let totalRequests = 0;
let node1Count = 0;
let node2Count = 0;

// Update UI info
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("badge-protocol").textContent = window.location.protocol.replace(":", "").toUpperCase();
    document.getElementById("badge-host").textContent = window.location.host;
    if (window.location.protocol === "https:") {
        document.getElementById("badge-protocol").className = "tag tag-nginx";
    }
});

// Step 1: SPA Client-side routing test
function testSpaRouting(path) {
    window.history.pushState({}, "", path);
    const resultSpan = document.getElementById("spa-result");
    resultSpan.textContent = `Đã đổi route: ${path} (NGINX try_files vẫn phục vụ index.html)`;
    resultSpan.style.color = "#38bdf8";
}

// Step 2: Single API call
async function callSingleApi() {
    const logBox = document.getElementById("proxy-log");
    logBox.textContent = "Đang gọi /api/demo/node-info...";
    try {
        const res = await fetch("/api/demo/node-info");
        const data = await res.json();
        
        recordNodeHit(data.nodeId);
        
        logBox.textContent = `[HTTP ${res.status} OK] Nhận từ ${data.nodeId}\n` +
            `• Client IP thực tế (X-Real-IP): ${data.clientIp}\n` +
            `• Host header: ${data.hostHeader}\n` +
            `• X-Forwarded-Proto: ${data.protocol}\n` +
            `• Timestamp: ${data.timestamp}\n` +
            `• Thông điệp: ${data.message}`;

        if (data.clientIp && data.clientIp !== "Unknown") {
            document.getElementById("stat-client-ip").textContent = data.clientIp;
        }
    } catch (err) {
        logBox.textContent = `[Lỗi] Không thể kết nối backend: ${err.message}\n(Hãy đảm bảo các backend node và NGINX đã khởi động)`;
    }
}

// Record hit
function recordNodeHit(nodeId) {
    totalRequests++;
    const isNode1 = (nodeId && nodeId.includes("1")) || (nodeId && nodeId.includes("5001"));
    if (isNode1) {
        node1Count++;
    } else {
        node2Count++;
    }
    updateStatsUI(nodeId);
}

function updateStatsUI(lastNodeId) {
    document.getElementById("stat-total-req").textContent = totalRequests;
    document.getElementById("stat-node1").textContent = node1Count;
    document.getElementById("stat-node2").textContent = node2Count;

    const ratio1 = totalRequests > 0 ? Math.round((node1Count / totalRequests) * 100) : 50;
    const ratio2 = 100 - ratio1;

    const bar1 = document.getElementById("ratio-node1");
    const bar2 = document.getElementById("ratio-node2");
    bar1.style.width = `${ratio1}%`;
    bar1.textContent = `Node 1: ${ratio1}% (${node1Count})`;
    bar2.style.width = `${ratio2}%`;
    bar2.textContent = `Node 2: ${ratio2}% (${node2Count})`;
}

// Step 3: Upstream load balancing test
async function simulateLoadTest(count = 10) {
    const btn = document.getElementById("btn-run-10");
    const stream = document.getElementById("lb-stream");
    btn.disabled = true;
    btn.textContent = "⏳ Đang gửi request...";

    for (let i = 1; i <= count; i++) {
        try {
            const start = performance.now();
            const res = await fetch("/api/demo/node-info?req=" + i + "&t=" + Date.now());
            const duration = Math.round(performance.now() - start);
            const data = await res.json();
            
            recordNodeHit(data.nodeId);

            const isNode1 = (data.nodeId && data.nodeId.includes("1")) || (data.nodeId && data.nodeId.includes("5001"));
            const entry = document.createElement("div");
            entry.className = `log-entry ${isNode1 ? 'entry-node1' : 'entry-node2'}`;
            entry.innerHTML = `<span>#${totalRequests} [${data.nodeId}]</span> <span>${duration}ms - IP: ${data.clientIp}</span>`;
            stream.prepend(entry);
        } catch (err) {
            const entry = document.createElement("div");
            entry.className = "log-entry";
            entry.style.color = "#ef4444";
            entry.textContent = `#${i} Lỗi: ${err.message}`;
            stream.prepend(entry);
        }
        await new Promise(r => setTimeout(r, 120));
    }

    btn.disabled = false;
    btn.textContent = "🚀 Gửi 10 Request Luân Phiên";
}

function resetStats() {
    totalRequests = 0;
    node1Count = 0;
    node2Count = 0;
    document.getElementById("lb-stream").innerHTML = "";
    updateStatsUI("");
}

// Step 5: Test client_max_body_size
async function testUploadPayload(sizeKB) {
    const resultBox = document.getElementById("upload-result");
    resultBox.textContent = `Đang tạo dữ liệu giả lập dung lượng ${sizeKB} KB và gửi đến /api/demo/upload...`;

    // Tạo payload chuỗi đúng kích thước
    const byteLength = sizeKB * 1024;
    const blob = new Blob([new Uint8Array(byteLength)], { type: "application/octet-stream" });
    const formData = new FormData();
    formData.append("file", blob, `test_payload_${sizeKB}KB.bin`);

    try {
        const res = await fetch("/api/demo/upload", {
            method: "POST",
            body: formData
        });

        if (res.status === 413) {
            resultBox.textContent = `❌ [HTTP 413 Request Entity Too Large]\n` +
                `NGINX ĐÃ CHẶN REQUEST NÀY VÌ KÍCH THƯỚC VƯỢT QUÁ GIỚI HẠN 'client_max_body_size'!\n` +
                `Dung lượng gửi: ${(sizeKB / 1024).toFixed(2)} MB. Giới hạn hiện tại nhỏ hơn mức này.`;
            resultBox.style.color = "#ef4444";
            return;
        }

        const data = await res.json();
        resultBox.textContent = `✅ [HTTP ${res.status} OK] Gửi thành công!\n` +
            `• Phản hồi từ backend: ${data.message}\n` +
            `• Dung lượng ghi nhận: ${data.sizeMB} MB (${data.sizeBytes} bytes)`;
        resultBox.style.color = "#10b981";
    } catch (err) {
        resultBox.textContent = `❌ Lỗi kết nối: ${err.message}`;
        resultBox.style.color = "#ef4444";
    }
}

async function uploadRealFile() {
    const input = document.getElementById("test-file-input");
    const resultBox = document.getElementById("upload-result");
    if (!input.files || input.files.length === 0) {
        alert("Vui lòng chọn một file để upload!");
        return;
    }

    const file = input.files[0];
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    resultBox.textContent = `Đang tải file ${file.name} (${sizeMB} MB)...`;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/api/demo/upload", {
            method: "POST",
            body: formData
        });

        if (res.status === 413) {
            resultBox.textContent = `❌ [HTTP 413 Request Entity Too Large]\nNGINX đã chặn file ${file.name} (${sizeMB} MB)!`;
            resultBox.style.color = "#ef4444";
            return;
        }

        const data = await res.json();
        resultBox.textContent = `✅ [HTTP ${res.status} OK] Upload thành công!\n` +
            `• Tên file: ${data.fileName}\n• Dung lượng: ${data.sizeMB} MB\n• Phản hồi: ${data.message}`;
        resultBox.style.color = "#10b981";
    } catch (err) {
        resultBox.textContent = `❌ Lỗi: ${err.message}`;
        resultBox.style.color = "#ef4444";
    }
}
