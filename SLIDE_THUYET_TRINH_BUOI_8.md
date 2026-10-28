# 📊 BÀI THUYẾT TRÌNH SLIDE - BUỔI 8
## Đề tài: Cấu hình NGINX Reverse Proxy – Upstream Nhiều Backend
**Nhóm:** Hệ Thống Quản Lý Rạp Chiếu Phim (*CineManagement*)

---

## SLIDE 1: TRANG TIÊU ĐỀ
* **Tiêu đề**: Kiến Trúc Web Server, Reverse Proxy & Load Balancing với NGINX
* **Dự án**: CineManagement (Hệ thống Quản lý Rạp chiếu phim)
* **Giảng viên hướng dẫn**: [Tên Giảng Viên]
* **Thành viên nhóm**:
  - Thành viên 1: Nghiên cứu khái niệm cơ bản & Upstream Load Balancing
  - Thành viên 2: Nghiên cứu NGINX Web Server & Reverse Proxy FE/BE
  - Thành viên 3: Nghiên cứu Container Docker, client_max_body_size, SSL/Domain
  - Nhóm trưởng: Tổng hợp nội dung, điều phối kịch bản thuyết trình & demo

---

## SLIDE 2: MỤC TIÊU BÀI HỌC
1. Hiểu bản chất & phân biệt **Web Server** và **Reverse Proxy**.
2. Nắm vững cách định tuyến: `/` cho Frontend và `/api/` cho Backend (giải quyết triệt để lỗi CORS).
3. Triển khai cân bằng tải **Upstream** điều hướng request đến nhiều backend instances.
4. Nắm các cấu hình thực tế: Docker network discovery, `client_max_body_size`, logging.
5. Hiểu cơ chế phân giải tên miền qua file `hosts`, tự tạo chứng chỉ SSL, bản chất **Chain of Trust** và Let's Encrypt trên Production.

---

## SLIDE 3: CÁC KHÁI NIỆM MẠNG CƠ BẢN
| Khái niệm | Định nghĩa & Vai trò | Ví dụ thực tế |
| :--- | :--- | :--- |
| **IP Address** | Địa chỉ định danh duy nhất của thiết bị trên mạng | `127.0.0.1` (localhost), `192.168.1.10` |
| **Domain** | Tên gợi nhớ thay thế cho địa chỉ IP | `google.com`, `cinemanet.local` |
| **Port** | Cổng giao tiếp phân luồng các dịch vụ trên cùng 1 máy | Port `80` (HTTP), Port `443` (HTTPS) |
| **SSL/TLS** | Giao thức mã hóa đường truyền an toàn giữa Client & Server | Cung cấp ổ khóa xanh trên trình duyệt |
| **File hosts** | Bảng ánh xạ IP - Domain cục bộ trước khi hỏi DNS Server | `C:\Windows\System32\drivers\etc\hosts` |

---

## SLIDE 4: PHÂN BIỆT WEB SERVER VÀ REVERSE PROXY
* **Web Server**:
  - Trả trực tiếp các file tĩnh (HTML, CSS, JS, Poster ảnh) cho trình duyệt.
  - Sử dụng các chỉ thị: `root`, `index`, `try_files` (cho SPA client-side routing).
* **Reverse Proxy**:
  - Đứng trước các server ứng dụng backend (ASP.NET Core, Node.js, Spring Boot).
  - Nhận request từ Client, kiểm tra, chuyển tiếp qua `proxy_pass` và nhận kết quả trả về cho Client.
  - **Lợi ích**: Ẩn cấu trúc backend thật, tập trung quản lý SSL, cân bằng tải, bảo mật DDoS/WAF.

---

## SLIDE 5: KIẾN TRÚC REVERSE PROXY CHO CẶP FE + BE
* **Vấn đề CORS**: Khi Frontend chạy ở `localhost:3000` và Backend chạy ở `localhost:5000`, trình duyệt sẽ chặn request do vi phạm chính sách cùng nguồn gốc (Same-Origin Policy).
* **Giải pháp với NGINX**:
  - Cả FE và BE cùng đứng sau một địa chỉ duy nhất: `http://cinemanet.local`
  - NGINX định tuyến theo path:
    - `location /` ➜ Phục vụ HTML/CSS/JS frontend.
    - `location /api/` ➜ `proxy_pass http://cine_backend;`
* **Forwarding Headers bắt buộc**:
  - `proxy_set_header Host $host;`
  - `proxy_set_header X-Real-IP $remote_addr;` (Giúp Backend biết IP thật của khách hàng)
  - `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
  - `proxy_set_header X-Forwarded-Proto $scheme;`

---

## SLIDE 6: UPSTREAM & CÁC CHIẾN LƯỢC CÂN BẰNG TẢI (LOAD BALANCING)
* **Khối `upstream`**: Định nghĩa nhóm các server backend:
  ```nginx
  upstream cine_backend {
      server 127.0.0.1:5001 weight=1;
      server 127.0.0.1:5002 weight=1;
  }
  ```
* **Các thuật toán cân bằng tải**:
  1. **Round-Robin (Mặc định)**: Phân phối lần lượt đều nhau cho các node (`Node 1 ➜ Node 2 ➜ Node 1...`).
  2. **Least Connections (`least_conn`)**: Chuyển request đến node đang có ít kết nối hoạt động nhất (phù hợp request tốn nhiều thời gian).
  3. **Weighted (`weight=N`)**: Phân phối theo tỷ lệ trọng số năng lực phần cứng (node có RAM/CPU cao hơn nhận nhiều request hơn).

---

## SLIDE 7: CÁC CẤU HÌNH THỰC TẾ HAY GẶP
1. **Container FE/BE trong Docker Network**:
   - Dùng tên dịch vụ (`server backend-node1:5000;`) thay vì `localhost`.
   - NGINX và Backend kết nối chung một bridge network khép kín.
2. **Giới hạn kích thước Body (`client_max_body_size`)**:
   - Mặc định của NGINX chỉ là **1MB**.
   - Nếu client upload ảnh/poster lớn hơn, NGINX trả về lỗi `HTTP 413 Request Entity Too Large`.
   - Cần tăng lên trong block http/server: `client_max_body_size 20M;`.
3. **Cấu hình Log riêng**:
   - Ghi nhận `$upstream_addr` để theo dõi node nào đã phản hồi request.

---

## SLIDE 8: BẢN CHẤT CHỨNG CHỈ SSL VÀ "CHAIN OF TRUST"
* **Tại sao chứng chỉ SSL được trình duyệt tin cậy?**
  1. Hệ điều hành & trình duyệt có sẵn danh sách các **Root CA (Certificate Authority)** uy tín (DigiCert, Sectigo, Let's Encrypt...).
  2. Root CA ký ủy quyền cho **Intermediate CA**.
  3. Intermediate CA ký cấp chứng chỉ cho tên miền của bạn sau khi xác minh quyền sở hữu.
  4. Trình duyệt kiểm tra chữ ký số ngược về Root CA thành công ➜ Hiện ổ khóa an toàn.
* **Tại sao chứng chỉ Tự Ký (Self-Signed) bị cảnh báo "Not Secure"?**
  - Tự mình làm CA cho chính mình, không có mắt xích nào trong chuỗi Root CA của hệ điều hành.
  - *Chỉ dùng cho môi trường thử nghiệm nội bộ / học tập.*
* **Giải pháp trên Server Production**:
  - Sử dụng **Certbot** để tự động xin và gia hạn chứng chỉ miễn phí từ **Let's Encrypt**:
    ```bash
    certbot --nginx -d cinemanet.vn
    ```

---

## SLIDE 9: BẢNG PHÂN CÔNG CÔNG VIỆC NHÓM (27 POINTS)
| Nhiệm vụ | Người thực hiện | Ước lượng |
| :--- | :--- | :---: |
| Nghiên cứu khái niệm cơ bản: Web server, Reverse Proxy, IP, Domain, Port, SSL, file hosts | TV1 | 3 Points |
| Nghiên cứu NGINX web server (phục vụ file tĩnh, SPA fallback) | TV2 | 2 Points |
| Nghiên cứu Reverse Proxy cho FE/BE và các `proxy_set_header` | TV2 | 3 Points |
| Nghiên cứu `upstream`, load balancing nhiều backend/node | TV1 | 3 Points |
| Nghiên cứu cấu hình thực tế: Docker container, `client_max_body_size`, server block chuẩn | TV3 | 3 Points |
| Nghiên cứu domain giả lập, SSL tự ký bằng OpenSSL, Certbot & Chain of Trust | TV3 | 3 Points |
| Chuẩn bị nội dung slide thuyết trình | Nhóm trưởng | 2 Points |
| Cấu hình NGINX & chuẩn bị kịch bản demo (6 bước thực hành) | Cả nhóm | 5 Points |
| Tổng hợp, kiểm tra và chạy thử toàn bộ demo | Cả nhóm | 2 Points |
| Luyện tập thuyết trình & demo | Cả nhóm | 1 Point |
| **Tổng cộng** | | **27 Points** |

---

## SLIDE 10: TỔNG KẾT & KẾT LUẬN
* NGINX là giải pháp Reverse Proxy & Web Server tiêu chuẩn công nghiệp mạnh mẽ, gọn nhẹ và linh hoạt.
* Việc kết hợp NGINX đứng trước các ứng dụng thực tế (như CineManagement) mang lại:
  - Khả năng mở rộng quy mô (Scale Out) không giới hạn.
  - Tính sẵn sàng cao (High Availability) khi có node gặp sự cố.
  - Bảo mật hạ tầng backend và trải nghiệm người dùng liền mạch.
