# KỊCH BẢN DEMO SẢN PHẨM TRỰC TIẾP DÀNH CHO GIÁO VIÊN (THỜI LƯỢNG: 05 PHÚT)
**Đề tài:** Hệ thống Quản lý đặt vé rạp chiếu phim trực tuyến & Check-in QR thông minh (CineManagement)  
**Giảng viên hướng dẫn:** TS. Trần Khánh Dung | **Bộ môn:** Quản lý dự án CNTT - HUCE  
**Nhóm sinh viên thực hiện:** Lâm Tuấn Kiệt (PO), Luyện Đức Chiến (SM/BE), Nguyễn Phúc Tiến (BE/DB), Nguyễn Tiến Đạt (Fullstack/Worker), Trần Phương Nam (UI/Tester)  
**Môi trường chạy:** `http://localhost:5006` (hoặc file `.exe` độc lập)

---

## I. CÔNG TÁC CHUẨN BỊ TRƯỚC DEMO (SETUP CHECKLIST - 1 PHÚT TRƯỚC KHI BẮT ĐẦU)

> [!TIP]
> **Bí quyết không bị đè Session đăng nhập:** Hãy mở **2 trình duyệt song song (Split Screen 50/50)** trên màn hình:
> - **Cửa sổ Trái (Google Chrome - Vai trò Khách hàng)**: Mở sẵn trang chủ `http://localhost:5006`, đã đăng nhập sẵn tài khoản `customer@cinema.com` (Mật khẩu: `Customer@123`).
> - **Cửa sổ Phải (Microsoft Edge - Vai trò Nhân viên / Admin)**: Mở sẵn `http://localhost:5006/Account/Login`, chuẩn bị sẵn tài khoản Nhân viên `staff@cinema.com` và Quản trị viên `admin@cinema.com`.
> - **Điện thoại di động**: Bật sẵn màn hình điện thoại hoặc chụp ảnh mã QR để sẵn sàng giơ trước Webcam máy tính test quét vé.

---

## II. BẢNG PHÂN BỔ THỜI GIAN DEMO (TIMING SHEET - ĐÚNG 300 GIÂY)

| Thời gian | Phân đoạn Demo | Vai trò & Màn hình | Thao tác chính cần thực hiện | Điểm kỹ thuật mấu chốt để "ghi điểm" |
|---|---|---|---|---|
| **0:00 - 0:35** (35s) | **1. Khởi động & Trang chủ** | Khách hàng (Chrome) | Lướt trang chủ CineManagement, banner, poster phim, ngày tiếng Việt | Logo chuẩn CineManagement, UI hiện đại, mượt mà |
| **0:35 - 1:50** (75s) | **2. Luồng Đặt vé trọn gói** | Khách hàng (Chrome) | Chọn phim -> Chọn 2 ghế (F5, F6) -> Chọn Combo F&B -> Thanh toán VietQR | **Cơ chế khóa ghế 10 phút**, gộp **1 mã QR duy nhất cho 2 ghế**, gửi Gmail |
| **1:50 - 3:10** (80s) | **3. Soát vé QR bằng Camera** | Nhân viên Staff (Edge) | Đăng nhập Staff -> Mở "Soát vé QR" -> Bật Camera quét -> Quét lại lần 2 | **Quét < 2s**, đổi trạng thái "Đã sử dụng", **quét lần 2 báo đỏ cảnh báo vé đã dùng** |
| **3:10 - 4:25** (75s) | **4. Dashboard & Báo cáo BI** | Quản trị Admin (Edge) | Đăng nhập Admin -> Mở Dashboard -> Mở Báo cáo & Thống kê | **Doanh thu phim cao nhất**, **Doanh thu combo theo ngày**, chặn trùng lịch |
| **4:25 - 5:00** (35s) | **5. Đóng gói EXE & Kết luận** | Hội đồng | Mở thư mục chứa file `.exe` độc lập -> Mời Thầy/Cô phản biện | Chạy không cần cài SDK .NET/MySQL, Background Worker 30s |

---

## III. KỊCH BẢN THAO TÁC VÀ LỜI THOẠI CHI TIẾT (STEP-BY-STEP LIVE SCRIPT)

### 🎬 PHÂN ĐOẠN 1: KHỞI ĐỘNG & TỔNG QUAN KHÁCH HÀNG (0:00 - 0:35)
- **Màn hình:** Trình duyệt Trái (Chrome) - Trang chủ `http://localhost:5006`.
- **Thao tác:** 
  1. Cuộn nhẹ chuột từ trên xuống dưới trang chủ: lướt qua Hero Banner, danh sách phim Đang chiếu, Đánh giá sao của khán giả.
  2. Chỉ chuột vào thanh menu điều hướng và logo **CineManagement**.
- **Lời nói với giáo viên:**
  > *"Em kính chào Thầy/Cô và Hội đồng! Tiếp theo phần thuyết trình, em xin phép được demo trực tiếp toàn bộ luồng vận hành của hệ thống CineManagement.*  
  > *Đầu tiên, đây là giao diện trang chủ dành cho Khách hàng. Hệ thống đã được chuẩn hóa nhận diện thương hiệu CineManagement, hỗ trợ xem danh sách phim đang chiếu, sắp chiếu, trailer và đánh giá sao thực tế từ người xem. Toàn bộ lịch chiếu và thời gian đều được bản địa hóa 100% bằng tiếng Việt."*

---

### 🎟️ PHÂN ĐOẠN 2: TRẢI NGHIỆM ĐẶT VÉ, KHÓA GHẾ 10P & VIETQR (0:35 - 1:50)
- **Màn hình:** Trình duyệt Trái (Chrome).
- **Thao tác:**
  1. Click vào nút **"Đặt vé ngay"** của một bộ phim hot (ví dụ: *Đào, Phở và Piano* hoặc *Mai*).
  2. Chọn ngày chiếu hôm nay và chọn một suất chiếu cụ thể.
  3. **Tại màn hình Chọn ghế (`SelectSeat`):**
     - Click chọn **2 ghế cạnh nhau** (Ví dụ: `F5`, `F6`).
     - *Dừng chuột 3 giây*: Chỉ vào đồng hồ đếm ngược `09:59` và 2 ghế chuyển sang màu cam/vàng (Trạng thái Held).
  4. Bấm **"Tiếp tục chọn Bắp Nước"**:
     - Chọn `1 Combo Bắp Nước Siêu Tiết Kiệm` (có ảnh minh họa bắp rang bơ và nước ngọt sinh động).
  5. Bấm **"Tiến hành Thanh toán" (`Checkout`)**:
     - Màn hình xuất hiện cổng **VietQR chuẩn Napas 247** với mã QR thanh toán động đã tích hợp sẵn số tiền và nội dung đơn.
     - Bấm nút **"Xác nhận đã thanh toán"**.
  6. **Tại màn hình Xác nhận (`Confirmation`):**
     - Chỉ vào dòng chữ: *"Đặt vé thành công!"*.
     - **Chỉ rõ điểm cải tiến:** Nhóm đã **gộp 2 ghế vào đúng 1 mã QR duy nhất** kèm mã Booking, và hệ thống thông báo vé điện tử đã tự động gửi thẳng về hòm thư Gmail của khách hàng.
- **Lời nói với giáo viên:**
  > *"Bây giờ em sẽ thực hiện đặt vé cho khách hàng. Em chọn phim, chọn suất chiếu. Tại sơ đồ phòng chiếu, em chọn 2 ghế F5 và F6.*  
  > *Thưa cô, điểm kỹ thuật đặc biệt ở đây là ngay khi em chọn ghế, cơ chế **Seat Hold Lock** lập tức kích hoạt: 2 ghế này chuyển sang trạng thái giữ chỗ với đồng hồ đếm ngược đúng 10 phút. Nếu có một khách hàng khác ở máy tính khác mở lên lúc này thì 2 ghế F5, F6 sẽ bị khóa, hoàn toàn không thể tranh chấp, loại bỏ 100% lỗi Race Condition.*  
  > *Tiếp theo, khách hàng chọn thêm Combo Bắp nước có hình ảnh trực quan. Tại trang thanh toán, hệ thống tạo mã **VietQR tiêu chuẩn quốc gia**, khách hàng chỉ cần quét app ngân hàng là tiền về đúng số tài khoản.*  
  > *Sau khi thanh toán thành công, theo đúng yêu cầu thực tế của rạp, hệ thống **tự động gộp cả 2 ghế vào 1 mã QR duy nhất**, đồng thời kích hoạt Background Worker gửi email vé điện tử HTML về Gmail của khách hàng."*

---

### 📷 PHÂN ĐOẠN 3: NHÂN VIÊN SOÁT VÉ BẰNG CAMERA & CHỐNG VÉ GIA LẬN (1:50 - 3:10)
- **Màn hình:** Trình duyệt Phải (Edge).
- **Thao tác:**
  1. Đăng nhập tài khoản Nhân viên: `staff@cinema.com` / Mật khẩu: `Staff@123`.
  2. Bấm vào Avatar góc phải -> mở nhanh **"Hồ sơ cá nhân"** (Profile đã được cập nhật giao diện thẻ nhân viên, ca trực chuyên nghiệp).
  3. Bấm vào nút màu xanh **"Soát vé QR"** trên thanh Menu (`/Admin/ScanTicket`).
  4. Bấm **"Bật Camera"**:
     - *Cách 1 (Nếu máy có webcam):* Giơ màn hình điện thoại có mã QR (hoặc mở ảnh QR của đơn vừa đặt) trước webcam.
     - *Cách 2 (Siêu an toàn nếu phòng thi không tiện giơ camera):* Nhấn nút **"Tải/Chụp ảnh QR"** hoặc click trực tiếp vào vé mẫu vừa đặt ở bảng danh sách bên dưới!
  5. **Quét lần 1 (Vé hợp lệ):**
     - Màn hình lóe xanh, phát âm thanh `bíp` và hiển thị thẻ thông báo: **"Check-in thành công! Mã đơn: ..., Phim: ..., Ghế: F5, F6. Thời gian: Vừa xong"**.
  6. **Quét lần 2 (Kiểm thử vé đã sử dụng):**
     - Đưa lại mã QR đó vào Camera quét lần nữa (hoặc bấm lại vé đó).
     - Màn hình lập tức hiện khung cảnh báo màu đỏ: **"CẢNH BÁO: Vé này đã được check-in vào lúc [HH:mm] bởi nhân viên Staff! Từ chối vào rạp!"**.
- **Lời nói với giáo viên:**
  > *"Bây giờ em chuyển sang vai trò Nhân viên soát vé tại cửa rạp. Em đăng nhập bằng tài khoản staff@cinema.com.*  
  > *Đây là hồ sơ cá nhân của nhân viên với đầy đủ thông tin ca trực và mã số. Em bấm vào tính năng 'Soát vé QR'. Ứng dụng tích hợp thư viện html5-qrcode, cho phép sử dụng trực tiếp Camera laptop hoặc Camera điện thoại mà không cần mua đầu đọc đắt tiền.*  
  > *Em bật Camera và đưa mã QR đơn hàng vừa đặt vào... Thưa cô, trong **chưa đầy 1.5 giây**, hệ thống đã xác thực thành công cả 2 ghế F5, F6 và đổi trạng thái vé sang Đã sử dụng.*  
  > *Và để kiểm tra tính năng bảo mật: Giả sử khách hàng chụp lại màn hình mã QR này gửi cho bạn bè để vào rạp lần thứ hai. Em đưa lại mã này trước camera... Hệ thống lập tức hiện **cảnh báo đỏ: Vé đã được sử dụng lúc [giờ:phút]**, ngăn chặn tuyệt đối tình trạng gian lận vé!"*

---

### 📊 PHÂN ĐOẠN 4: ADMIN DASHBOARD & BÁO CÁO DOANH THU CHUYÊN SÂU (3:10 - 4:25)
- **Màn hình:** Trình duyệt Phải (Edge).
- **Thao tác:**
  1. Đăng xuất Staff -> Đăng nhập tài khoản Quản trị: `admin@cinema.com` / `Admin@123`.
  2. Vào trang **Quản trị (`Admin/Dashboard`)**:
     - Chỉ vào các thẻ KPI: Tổng doanh thu hôm nay, số vé bán hôm nay vừa tự động nhảy số theo đơn hàng khách vừa đặt!
  3. Bấm vào nút **"Xem báo cáo"** để sang trang **Báo cáo & Phân tích Doanh thu (`Admin/Reports`)**:
     - **Chỉ vào Mục 1 - Báo cáo phim doanh thu cao nhất:** Bảng xếp hạng phim có doanh thu cao nhất, số lượng vé đã bán và tỷ lệ lấp đầy rạp.
     - **Chỉ vào Mục 2 - Báo cáo Doanh thu Combo F&B theo các ngày:** Biểu đồ đường/cột thể hiện doanh thu bắp rang bơ và nước ngọt tăng trưởng theo từng ngày.
     - Bấm thử bộ lọc: Lọc theo *"Hôm nay"*, *"7 ngày qua"*, *"Tháng này"* để chứng minh tính linh hoạt.
  4. Lướt nhanh sang mục **Lịch chiếu (`Showtime`)**:
     - Nhấn nút "Thêm suất chiếu", chọn phòng chiếu 1 và chọn giờ trùng với một suất đang có.
     - Bấm Lưu -> Hệ thống hiển thị thông báo lỗi chống trùng: *"Phòng chiếu đã có suất chiếu khác trong khung giờ này!"*.
- **Lời nói với giáo viên:**
  > *"Tiếp theo, em xin phép demo phân hệ Quản trị viên cấp cao. Em đăng nhập tài khoản admin@cinema.com.*  
  > *Tại Dashboard quản trị, các chỉ số doanh thu và số vé hôm nay vừa được cập nhật tức thời theo thời gian thực ngay sau đơn đặt vé vừa rồi.*  
  > *Em bấm vào mục **Báo cáo & Thống kê Doanh thu chi tiết**: Hệ thống phân tích sâu 2 bài toán kinh doanh cốt lõi của rạp:*  
  > *Một là **Bảng xếp hạng phim có doanh thu cao nhất**: Giúp quản lý rạp biết phim nào đang ăn khách để tăng thêm suất chiếu.*  
  > *Hai là **Báo cáo doanh thu đồ ăn nước uống F&B theo từng ngày**: Giúp kiểm soát tỷ trọng bán bắp nước, kiểm kê kho và đánh giá hiệu quả của các gói combo.*  
  > *Ngoài ra, tại phần Quản lý suất chiếu, hệ thống có thuật toán kiểm tra xung đột thời gian, tự động ngăn chặn hoàn toàn việc nhân viên xếp trùng giờ chiếu trong cùng một phòng."*

---

### 🚀 PHÂN ĐOẠN 5: ĐÓNG GÓI EXE ĐỘC LẬP & TỔNG KẾT (4:25 - 5:00)
- **Màn hình:** Mở cửa sổ File Explorer / Terminal trên máy tính.
- **Thao tác:**
  1. Chỉ vào thư mục ứng dụng hoặc file `CineManagement.exe` đã được build single-file self-contained.
  2. Chỉ vào file cơ sở dữ liệu `app.db` (SQLite portable) hoạt động song song với MySQL.
  3. Chuyển ánh mắt về phía Thầy/Cô, nở nụ cười và nói lời kết thúc.
- **Lời nói với giáo viên:**
  > *"Điểm cuối cùng nhóm muốn chia sẻ là toàn bộ hệ thống đã được tối ưu và đóng gói thành một file **EXE Portable duy nhất**. Ứng dụng có thể copy sang bất kỳ máy tính Windows nào và khởi chạy ngay lập tức mà không cần cài đặt .NET SDK hay máy chủ MySQL phức tạp.*  
  > *Hệ thống cũng tích hợp một Background Service chạy ngầm định kỳ 30 giây để tự động quét dọn và giải phóng các ghế giữ chỗ quá 10 phút mà không làm tiêu tốn tài nguyên máy.*  
  > *Đến đây, nhóm em đã hoàn thành trọn vẹn kịch bản demo sản phẩm theo đúng cam kết trong đồ án. Nhóm em xin chân thành cảm ơn Thầy/Cô và kính mời Thầy/Cô đưa ra các câu hỏi nhận xét hoặc yêu cầu nhóm thao tác thêm bất kỳ chức năng nào ạ!"*

---

## IV. BẢNG DỰ PHÒNG TÌNH HUỐNG (TROUBLESHOOTING CHEAT-SHEET KHI DEMO)

| Tình huống phát sinh tại phòng thi | Nguyên nhân | Cách xử lý nhanh trong 3 giây |
|---|---|---|
| **Trình duyệt hỏi cấp quyền Camera mà không nhận** | Do máy chiếu hoặc trình duyệt chặn quyền video | Bấm ngay nút **"Tải/Chụp ảnh QR"** hoặc click vào **Vé mẫu** ở bảng danh sách bên dưới thẻ quét vé. Kết quả vẫn kiểm tra vé và đổi trạng thái 100%! |
| **Bấm thanh toán nhưng không có tài khoản ngân hàng thật** | Đang ở chế độ demo học thuật | Nhấn nút **"Xác nhận đã thanh toán"**, hệ thống đã có logic mô phỏng giao dịch thành công và sinh mã vé ngay lập tức. |
| **Muốn chứng minh cơ chế nhả ghế sau 10 phút** | Giáo viên hỏi: "Có thật là sau 10 phút nó tự nhả ghế không?" | Trả lời: *"Dạ thưa cô, hệ thống sử dụng `SeatCleanupWorker` kế thừa `BackgroundService` của .NET. Mỗi 30 giây nó chạy một câu truy vấn kiểm tra `HoldExpiresAt < UtcNow` để set lại ghế về `Available`. Em có thể mở trực tiếp file `SeatCleanupWorker.cs` để cô xem mã nguồn!"* |
