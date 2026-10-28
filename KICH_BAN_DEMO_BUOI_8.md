# 🎬 KỊCH BẢN THỰC HÀNH & DEMO CHI TIẾT - BUỔI 8
## Đề tài: Cấu hình NGINX Reverse Proxy – Upstream Nhiều Backend
**Hệ thống thực hành:** Hệ thống Quản lý Rạp chiếu phim (*CineManagement*)

---

## I. MỤC TIÊU VÀ CHUẨN BỊ MÔI TRƯỜNG

### 1. Phân biệt 3 môi trường thực hành (Theo mục 2.6 trong tài liệu)
* **Trường hợp 1 — Windows native (Hiện đang áp dụng chính thức)**:
  - NGINX chạy trực tiếp trên Windows qua thư mục `nginx/bin/nginx-1.26.2/`.
  - Backend ASP.NET Core chạy trực tiếp trên các cổng `5001` và `5002`.
  - Trình duyệt truy cập tại Windows. Cấu hình file `C:\Windows\System32\drivers\etc\hosts`.
* **Trường hợp 2 — NGINX trong WSL / Ubuntu + Trình duyệt Windows**:
  - Khi đã cài đặt WSL (`wsl --install -d Ubuntu`), chạy script `nginx/scripts/setup_wsl_nginx.sh`.
  - NGINX chạy trong Linux, Windows phân giải domain qua file hosts của Windows.
* **Trường hợp 3 — Docker Compose**:
  - Chạy toàn bộ bằng lệnh: `docker compose -f docker-compose.buoi8.yml up -d`.

### 2. Khởi động nhanh toàn bộ môi trường (1-Click)
Chạy file:
```cmd
START-DEMO-BUOI8.bat
```
Lệnh này sẽ tự động:
1. Đồng bộ cấu hình NGINX và thư mục giao diện `nginx/html/`.
2. Khởi chạy **Backend Node 1** (Port 5001).
3. Khởi chạy **Backend Node 2** (Port 5002).
4. Khởi chạy **NGINX Reverse Proxy** (Port 80 HTTP & Port 443 HTTPS).
5. Tự động mở trình duyệt tại `http://localhost`.

---

## II. KỊCH BẢN 6 BƯỚC THỰC HIỆN & THUYẾT TRÌNH DEMO

### 🎯 BƯỚC 1: NGINX là Web Server (Phục vụ File Tĩnh & Fallback SPA)
* **Ý nghĩa**: NGINX phục vụ trực tiếp các tài nguyên HTML, CSS, JavaScript của giao diện người dùng mà không cần tiêu tốn tài nguyên xử lý của Backend.
* **Thao tác demo**:
  1. Mở trình duyệt truy cập `http://localhost`.
  2. Trang web `index.html` của CineManagement hiện lên ngay lập tức.
  3. Bấm nút **"Test SPA Route Fallback"** trên thẻ Bước 1 hoặc truy cập `http://localhost/movies/avatar-3`.
* **Giải thích kỹ thuật**:
  - Trong `nginx.conf`:
    ```nginx
    location / {
        root html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
    ```
  - `try_files` kiểm tra nếu không tìm thấy file vật lý `/movies/avatar-3`, NGINX tự động fallback trả về `index.html`, cho phép router phía client (React/Vue/JS) xử lý điều hướng mà không bị lỗi `404 Not Found`.

---

### 🎯 BƯỚC 2: NGINX là Reverse Proxy FE + BE (Không bị CORS & Forward Headers)
* **Ý nghĩa**: Trình duyệt truy cập cả giao diện và gọi API trên cùng một domain/origin (`http://localhost`), loại bỏ hoàn toàn rào cản CORS (Cross-Origin Resource Sharing). NGINX chịu trách nhiệm forward request ngầm về backend.
* **Thao tác demo**:
  1. Trên giao diện demo, bấm nút **"Gọi API /api/demo/node-info"**.
  2. Quan sát khung log phản hồi:
     - HTTP Status: `200 OK`.
     - Client IP thực tế (`X-Real-IP`): `127.0.0.1`.
     - Host: `localhost`.
     - Node phục vụ: `Backend-Node-5001`.
* **Giải thích kỹ thuật**:
  - Mặc định, nếu không cấu hình, Backend sẽ chỉ nhìn thấy IP của proxy (127.0.0.1) làm remote address.
  - Các chỉ thị quan trọng trong NGINX:
    ```nginx
    location /api/ {
        proxy_pass http://cine_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    ```
  - Backend đọc `Request.Headers["X-Real-IP"]` để log IP thật của khách hàng phục vụ kiểm soát an ninh và rate-limit.

---

### 🎯 BƯỚC 3: Upstream Cluster & Cân Bằng Tải (Load Balancing)
* **Ý nghĩa**: Khi một backend không đủ tải hoặc cần dự phòng sự cố (high availability), NGINX phân phối request đều qua nhiều node server.
* **Thao tác demo**:
  1. Trên giao diện, bấm nút **"🚀 Gửi 10 Request Luân Phiên"**.
  2. Quan sát dòng log và thanh tỷ lệ:
     - Request 1, 3, 5, 7, 9 được xử lý bởi **Node 1 (Port 5001)**.
     - Request 2, 4, 6, 8, 10 được xử lý bởi **Node 2 (Port 5002)**.
     - Tỷ lệ phân tải đạt đúng `50% : 50%` (Round-Robin).
  3. Kiểm chứng bằng lệnh PowerShell:
     ```powershell
     1..6 | ForEach-Object { (Invoke-RestMethod "http://localhost/api/demo/node-info").nodeId }
     ```
     *Kết quả in ra luân phiên*: `Backend-Node-5001`, `Backend-Node-5002`, `Backend-Node-5001`...
* **Giải thích kỹ thuật**:
  - Khối cấu hình upstream:
    ```nginx
    upstream cine_backend {
        server 127.0.0.1:5001 weight=1;
        server 127.0.0.1:5002 weight=1;
    }
    ```
  - Có thể mở rộng sang `least_conn` (ưu tiên node ít kết nối nhất) hoặc `weight=2` (node mạnh nhận gấp đôi request).

---

### 🎯 BƯỚC 4: Cấu hình Container FE/BE (Docker Compose)
* **Ý nghĩa**: Đóng gói NGINX và toàn bộ các node backend vào mạng nội bộ Docker.
* **Thao tác thuyết minh**:
  1. Trình chiếu file `docker-compose.buoi8.yml`.
  2. Chỉ ra rằng trong mạng Docker, `proxy_pass` không trỏ vào `localhost` mà trỏ vào service name nhờ **Docker DNS Service Discovery**:
     ```yaml
     services:
       backend-node1:
         build: .
       backend-node2:
         build: .
       nginx-proxy:
         image: nginx:alpine
         ports: ["80:80", "443:443"]
     ```
  3. Cấu hình trong `nginx/nginx-docker.conf`:
     ```nginx
     upstream cine_backend_cluster {
         server backend-node1:5000;
         server backend-node2:5000;
     }
     ```

---

### 🎯 BƯỚC 5: Kiểm soát Kích thước Body (`client_max_body_size`)
* **Ý nghĩa**: Ngăn chặn tấn công DoS bằng payload quá lớn, nhưng cho phép tải lên file poster/ảnh hợp lệ.
* **Thao tác demo**:
  1. Thử nghiệm gửi dữ liệu lớn khi NGINX giới hạn 1MB:
     - Bấm nút **"Gửi 2.5 MB (Thử nghiệm 413)"**.
     - Nếu cấu hình NGINX là 1M, NGINX trả về ngay:
       `❌ HTTP 413 Request Entity Too Large`
     - Backend thậm chí không cần xử lý, giúp tiết kiệm băng thông và CPU của server.
  2. Thử nghiệm khi đã cấu hình `client_max_body_size 20M;`:
     - Bấm gửi lại file hoặc upload qua form -> Nhận kết quả:
       `✅ HTTP 200 OK - Nhận thành công dữ liệu qua NGINX!`
* **Giải thích kỹ thuật**:
  - Khai báo tại block `http` hoặc `server`:
    ```nginx
    client_max_body_size 20M;
    ```

---

### 🎯 BƯỚC 6: Tên Miền Giả Lập & Chứng Chỉ SSL Tự Ký (HTTPS 443)
* **Ý nghĩa**: Mô phỏng tên miền doanh nghiệp `cinemanet.local` và mã hóa toàn bộ dữ liệu qua SSL/TLS.
* **Thao tác demo**:
  1. **File hosts**: Mở file `C:\Windows\System32\drivers\etc\hosts` và thêm dòng:
     ```
     127.0.0.1  cinemanet.local
     ```
  2. **Tạo chứng chỉ SSL**: Đã tạo bằng OpenSSL:
     - `cinemanet.crt` (Certificate)
     - `cinemanet.key` (Private Key)
  3. **Truy cập HTTPS**:
     - Mở trình duyệt gõ: `https://cinemanet.local`
     - Trình duyệt hiển thị cảnh báo: **"Kết nối của bạn không phải là kết nối riêng tư" / "NET::ERR_CERT_AUTHORITY_INVALID"**.
     - Bấm *Nâng cao (Advanced)* ➜ *Tiếp tục truy cập (Proceed)*.
     - Trang web bảo mật bằng HTTPS hiển thị thành công.
* **Giải thích lý thuyết Chain of Trust**:
  - **Vì sao bị cảnh báo?** Chứng chỉ do ta tự ký (Self-signed), không có chữ ký của bất kỳ Root CA (Certificate Authority) nào có trong trust store của Hệ điều hành / Trình duyệt.
  - **Giải pháp trên Production**: Dùng công cụ **Certbot (Let's Encrypt)** để xin cấp chứng chỉ miễn phí được thế giới công nhận tự động (`certbot --nginx -d yourdomain.com`).

---

## III. TỔNG KẾT BÀI THUYẾT TRÌNH
1. NGINX hoàn thành xuất sắc vai trò vừa là **Web Server file tĩnh**, vừa là **Reverse Proxy** bảo vệ Backend.
2. Hệ thống backend rạp chiếu phim được nâng cao độ tin cậy và khả năng chịu tải nhờ kiến trúc **Upstream Cluster Round-Robin**.
3. Toàn bộ kịch bản 6 bước được cấu hình chuẩn chỉ, minh họa trực quan từ giao diện web đến mã nguồn và dòng lệnh.
