# KỊCH BẢN THUYẾT TRÌNH DỰ ÁN QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM TRỰC TUYẾN & CHECK-IN QR THÔNG MINH (CINEMANAGEMENT)
**Thời lượng chuẩn:** 05 Phút (300 giây) | **Khung tham chiếu:** 15 Slide PowerPoint & Báo cáo Đồ án QLDACNTT  
**Giảng viên hướng dẫn:** TS. Trần Khánh Dung | **Bộ môn:** Quản lý Dự án CNTT - Đại học Xây dựng Hà Nội (HUCE)  
**Nhóm thực hiện (5 thành viên):**  
1. **Lâm Tuấn Kiệt** (Product Owner - PO)  
2. **Luyện Đức Chiến** (Scrum Master & Backend Dev - SM/BE)  
3. **Nguyễn Phúc Tiến** (Backend & Database Specialist - BE/DB)  
4. **Nguyễn Tiến Đạt** (Fullstack Developer & Background Worker - Fullstack/Worker)  
5. **Trần Phương Nam** (UI/UX Designer & QA/Tester - UI/Tester)  

---

## I. BẢNG PHÂN BỔ THỜI LƯỢNG CHI TIẾT (TIMING & CUE SHEET)

| Mốc thời gian | Slide | Nội dung trọng tâm | Hành động & Nhấn nhá (Cue) |
|---|---|---|---|
| **0:00 - 0:20** | **Slide 1** | Giới thiệu tên đề tài, GVHD TS. Trần Khánh Dung, nhóm 5 thành viên | Chào trang trọng, phong thái tự tin |
| **0:20 - 0:40** | **Slide 2** | Nỗi đau rạp truyền thống: Xếp hàng 15-30p, vé giấy thất lạc, ghế ảo, dữ liệu trễ | Nhấn mạnh 4 điểm nghẽn thực tế |
| **0:40 - 0:55** | **Slide 3** | Mục tiêu: Hệ sinh thái khép kín từ đặt vé -> VietQR -> Check-in QR < 2s | Khẳng định giải pháp số hóa toàn diện |
| **0:55 - 1:15** | **Slide 4** | 3 vai trò (Customer - Staff - Admin) & Background Worker nền | Nêu bật sự phân tách trách nhiệm rõ ràng |
| **1:15 - 1:35** | **Slide 5** | Quy trình Agile/Scrum: 4 Sprint, 90 Story Points hoàn thành 100% | Nhấn mạnh đúng tiến độ, 0 nợ kỹ thuật |
| **1:35 - 1:55** | **Slide 6** | Phân bổ 21 User Stories qua 4 Sprint (Nền tảng -> Vận hành -> Giao dịch -> BI) | Nêu bật tính kế thừa qua từng Sprint |
| **1:55 - 2:30** | **Slide 7** | 9 tính năng cốt lõi: RBAC, lịch chống trùng, ghế real-time 10p, VietQR, Scan < 2s | Điểm sáng công nghệ của dự án |
| **2:30 - 2:50** | **Slide 8** | Kiến trúc N-Tier 3 tầng (.NET 10, EF Core, MySQL 10.11 / SQLite Portable) | Nhấn mạnh tính mở rộng và đóng gói EXE |
| **2:50 - 3:15** | **Slide 9 & 10** | Sequence đặt vé - thanh toán - soát vé & ERD CSDL chuẩn hóa 3NF | Chỉ nhanh luồng dữ liệu liên thông |
| **3:15 - 3:45** | **Slide 11** | Kiểm thử: 8 Kịch bản trọng yếu (TC-01 -> TC-08) PASS 100% | Khẳng định độ tin cậy và ngăn Race Condition |
| **3:45 - 4:10** | **Slide 12** | Quản lý 4 rủi ro lớn (Race condition, Worker treo, Mail SMTP, Camera/Vé giả) | Thể hiện tư duy quản trị dự án chuyên nghiệp |
| **4:10 - 4:35** | **Slide 13** | Đánh giá: Ưu điểm (Đạt 100% phạm vi, EXE độc lập) & Hạn chế (Webhook tự động) | Đánh giá khách quan, trung thực |
| **4:35 - 4:50** | **Slide 14** | Hướng phát triển: Webhook Open Banking, AI gợi ý combo, App Mobile | Tầm nhìn nâng cấp sản phẩm |
| **4:50 - 5:00** | **Slide 15** | Lời cảm ơn GVHD, Hội đồng & Mời đặt câu hỏi Q&A | Cúi chào, mở phiên phản biện |

---

## II. LỜI THOẠI THUYẾT TRÌNH CHI TIẾT (FULL SCRIPT NÓI TỰ NHIÊN)

### [PHẦN 1: MỞ ĐẦU & BỐI CẢNH DỰ ÁN] (0:00 - 0:55)

**[SLIDE 1 - Bìa đề tài] (0:00 - 0:20)**  
> *"Kính thưa quý Thầy, Cô trong Hội đồng và toàn thể các bạn sinh viên!*  
> *Hôm nay, nhóm chúng em xin phép được đại diện trình bày báo cáo đề tài Quản lý dự án CNTT với sản phẩm: **'Hệ thống Quản lý đặt vé rạp chiếu phim trực tuyến và Check-in mã QR thông minh - CineManagement'**.*  
> *Đề tài được thực hiện dưới sự hướng dẫn khoa học tận tình của **Tiến sĩ Trần Khánh Dung**, cùng sự phối hợp của 5 thành viên trong nhóm, phụ trách đầy đủ các vai trò Product Owner, Scrum Master, Backend, Database, Worker và QA/Tester."*

**[SLIDE 2 - Nỗi đau rạp truyền thống] (0:20 - 0:40)**  
> *[Bấm chuyển Slide 2]*  
> *"Thưa thầy cô, khảo sát thực tế tại các cụm rạp chiếu phim truyền thống cho thấy 4 nút thắt lớn:*  
> *Thứ nhất, khách hàng phải **xếp hàng từ 15 đến 30 phút** vào giờ cao điểm.*  
> *Thứ hai, **vé giấy dễ rách, thất lạc** và tốn kém chi phí in ấn nhiệt.*  
> *Thứ ba là vấn nạn **'xung đột giữ ghế ảo'** gây thất thu cho rạp khi nhiều người cùng chọn một ghế.*  
> *Và thứ tư, dữ liệu quản trị bị phân tán, ban giám đốc không thể nắm bắt doanh thu tức thời."*

**[SLIDE 3 - Mục tiêu đề tài & Định hướng] (0:40 - 0:55)**  
> *[Bấm chuyển Slide 3]*  
> *"Xuất phát từ bài toán đó, mục tiêu của CineManagement là xây dựng một **hệ sinh thái số hóa toàn diện, khép kín**: từ khâu khách hàng đặt vé trên Web, thanh toán chuyển khoản VietQR chuẩn quốc gia, nhận vé điện tử kèm mã QR qua Gmail, cho đến khâu nhân viên soát vé tại cửa chỉ bằng Camera điện thoại trong **chưa đầy 2 giây**."*

---

### [PHẦN 2: QUẢN TRỊ AGILE/SCRUM & PHÂN BỔ SPRINT] (0:55 - 1:55)

**[SLIDE 4 - Hệ sinh thái 3 vai trò + Background Worker] (0:55 - 1:15)**  
> *[Bấm chuyển Slide 4]*  
> *"Kiến trúc nghiệp vụ của hệ thống được thiết kế xoay quanh 3 đối tượng người dùng chính:*  
> *- **Khách hàng**: Tự do chọn phim, suất chiếu, ghế ngồi trực quan và đặt kèm combo Bắp Nước.*  
> *- **Nhân viên soát vé**: Sử dụng Camera tích hợp để check-in tức thì và tra cứu trạng thái vé.*  
> *- **Quản trị viên**: Theo dõi Dashboard báo cáo doanh thu phim và combo F&B theo thời gian thực.*  
> *Đặc biệt, hệ thống có một **Background Worker** chạy ngầm độc lập để tự động giải phóng ghế hết hạn sau 10 phút, bảo đảm rạp không bao giờ bị giữ ghế ảo."*

**[SLIDE 5 - Quy trình Agile/Scrum chuẩn mực] (1:15 - 1:35)**  
> *[Bấm chuyển Slide 5]*  
> *"Về phương pháp luận quản trị, nhóm áp dụng nghiêm ngặt khung làm việc **Agile/Scrum** qua 4 Sprint.*  
> *Chúng em duy trì đầy đủ các sự kiện: Sprint Planning, Daily Scrum 15 phút, Sprint Review và Retrospective.*  
> *Toàn bộ tiến độ được theo dõi trực quan trên Jira Board và GitHub. Kết quả là nhóm đã hoàn thành **100% mục tiêu với tổng số 90 Story Points**, hoàn thành đúng hạn và hoàn toàn **không phát sinh nợ kỹ thuật (0 Technical Debt)**."*

**[SLIDE 6 - Chi tiết 4 Sprint & 21 User Stories] (1:35 - 1:55)**  
> *[Bấm chuyển Slide 6]*  
> *"Khối lượng 90 Story Points được cụ thể hóa thành 21 User Stories kế thừa chặt chẽ qua 4 Sprint:*  
> *- **Sprint 1 (22 SP)**: Thiết lập nền tảng kiến trúc, mô hình CSDL và phân quyền RBAC 3 cấp độ.*  
> *- **Sprint 2 (24 SP)**: Xây dựng module vận hành rạp, phim, phòng chiếu và thuật toán xếp lịch chống trùng giờ.*  
> *- **Sprint 3 (26 SP)**: Hoàn thiện luồng giao dịch cốt lõi: sơ đồ ghế động, khóa ghế 10 phút, đặt F&B và cổng thanh toán VietQR.*  
> *- **Sprint 4 (18 SP)**: Tự động gửi vé HTML qua Gmail, module Camera quét QR dưới 2 giây, Dashboard BI quản trị và đóng gói thành một file EXE duy nhất chạy độc lập."*

---

### [PHẦN 3: TÍNH NĂNG ĐỘT PHÁ & NỀN TẢNG KỸ THUẬT] (1:55 - 3:15)

**[SLIDE 7 - 9 Tính năng nổi bật cốt lõi] (1:55 - 2:30)**  
> *[Bấm chuyển Slide 7]*  
> *"Trên màn hình là **9 tính năng vượt trội** của CineManagement.*  
> *Điểm nhấn kỹ thuật đáng chú ý nhất gồm có:*  
> *1. **Cơ chế Khóa ghế tạm thời 10 phút**: Giải quyết triệt để vấn đề Race Condition khi hàng trăm người truy cập cùng lúc.*  
> *2. **Cổng thanh toán VietQR Napas 247**: Khách hàng chỉ cần mở app ngân hàng quét mã, không cần nhập số tài khoản thủ công.*  
> *3. **Vé điện tử đa phương tiện**: Hệ thống tự động gửi email xác nhận kèm vé HTML sắc nét và mã QR được mã hóa bảo mật.*  
> *4. **Check-in Camera siêu tốc**: Nhân viên không cần đầu đọc mã vạch đắt tiền, chỉ cần mở trình duyệt là có thể quét vé trong vòng dưới 2 giây."*

**[SLIDE 8 - Kiến trúc N-Tier & Công nghệ hiện đại] (2:30 - 2:50)**  
> *[Bấm chuyển Slide 8]*  
> *"Về kiến trúc kỹ thuật, sản phẩm được xây dựng theo mô hình **N-Tier 3 tầng chuẩn công nghiệp**:*  
> *- **Tầng giao diện**: ASP.NET Core Razor Pages, tối ưu bằng Tailwind CSS và thư viện quét `html5-qrcode`.*  
> *- **Tầng nghiệp vụ**: Tích hợp các Service chuyên biệt như QRCoder, MailKit SMTP và Hosted Service Worker.*  
> *- **Tầng dữ liệu**: Sử dụng Entity Framework Core 10 kết nối MySQL/MariaDB 10.11, đồng thời hỗ trợ chế độ SQLite cục bộ, cho phép đóng gói thành file **EXE Portable** có thể chạy ngay trên mọi máy tính mà không cần cài đặt môi trường phức tạp."*

**[SLIDE 9 & 10 - Sơ đồ tuần tự & ERD chuẩn 3NF] (2:50 - 3:15)**  
> *[Bấm chuyển Slide 9 rồi lướt Slide 10]*  
> *"Ở Slide 9 và Slide 10, quý thầy cô có thể quan sát Sơ đồ tuần tự và CSDL chuẩn hóa 3NF gồm 12 bảng liên kết chặt chẽ.*  
> *Mọi giao dịch từ chọn ghế, đối soát trạng thái vé `Confirmed`, `Used` hay `Expired` đều được bao bọc trong Database Transaction, đảm bảo tính toàn vẹn dữ liệu tuyệt đối (ACID)."*

---

### [PHẦN 4: KIỂM THỬ, QUẢN TRỊ RỦI RO & ĐÁNH GIÁ] (3:15 - 4:35)

**[SLIDE 11 - Kết quả Kiểm thử: 8/8 Test Cases PASS] (3:15 - 3:45)**  
> *[Bấm chuyển Slide 11]*  
> *"Để chứng minh chất lượng phần mềm, nhóm đã thực hiện nghiêm ngặt **8 kịch bản kiểm thử tích hợp trọng yếu (TC-01 đến TC-08)**:*  
> *- Kiểm thử phân quyền RBAC: PASS.*  
> *- Xếp lịch chiếu trùng phòng: Bị thuật toán chặn chính xác: PASS.*  
> *- Hai người tranh chấp 1 ghế cùng mili-giây: Hệ thống khóa ghế đầu tiên, thông báo cho người thứ hai: PASS.*  
> *- Quét mã QR vé giả hoặc vé đã qua cửa: Hệ thống cảnh báo từ chối ngay lập tức: PASS.*  
> *Tất cả 8 kịch bản đều đạt **tỷ lệ thành công 100%**, bảo đảm hệ thống vận hành trơn tru không lỗi nghiêm trọng."*

**[SLIDE 12 - Ma trận Quản lý 4 Rủi ro trọng yếu] (3:45 - 4:10)**  
> *[Bấm chuyển Slide 12]*  
> *"Dưới góc độ Quản lý dự án, nhóm đã chủ động nhận diện và kiểm soát **4 rủi ro lớn** bằng các giải pháp kỹ thuật cụ thể:*  
> *1. Rủi ro Race condition: Khống chế bằng Seat Hold Lock 10 phút.*  
> *2. Rủi ro Worker treo: Sử dụng BackgroundService chu kỳ 30s với cơ chế tự phục hồi lỗi.*  
> *3. Rủi ro gián đoạn gửi Gmail: Xử lý qua Async Queue và ghi log.*  
> *4. Rủi ro gian lận vé: Mã hóa chuỗi QR ngẫu nhiên chống làm giả."*

**[SLIDE 13 - Đánh giá Ưu điểm & Hạn chế] (4:10 - 4:35)**  
> *[Bấm chuyển Slide 13]*  
> *"Nhìn lại toàn bộ quá trình, dự án đạt được những **ưu điểm nổi bật**:*  
> *- Hoàn thành 100% các tiêu chí cam kết trong đề cương.*  
> *- Ứng dụng thực tiễn cao, hỗ trợ cả triển khai Server lẫn chạy file EXE độc lập.*  
> *Tuy nhiên, nhóm cũng thẳng thắn nhìn nhận **hạn chế**: Do rào cản tài khoản doanh nghiệp nên cổng VietQR hiện tại vẫn cần nhân viên đối soát trạng thái chuyển khoản thay vì Webhook tự động 24/7."*

---

### [PHẦN 5: ĐỊNH HƯỚNG TƯƠNG LAI & KẾT LUẬN] (4:35 - 5:00)

**[SLIDE 14 - Hướng phát triển tương lai] (4:35 - 4:50)**  
> *[Bấm chuyển Slide 14]*  
> *"Trong giai đoạn tiếp theo, nhóm định hướng 4 nâng cấp chiến lược:*  
> *Thứ nhất, tích hợp **Webhook Open Banking** để tự động xác nhận tiền về tài khoản trong 1 giây.*  
> *Thứ hai, ứng dụng **AI Machine Learning** để phân tích hành vi, gợi ý suất chiếu và combo F&B cá nhân hóa.*  
> *Thứ ba, bổ sung hệ thống tích điểm thành viên Loyalty Points.*  
> *Và thứ tư, phát triển ứng dụng di động đa nền tảng bằng Flutter hoặc .NET MAUI."*

**[SLIDE 15 - Lời cảm ơn & Phiên Q&A] (4:50 - 5:00)**  
> *[Bấm chuyển Slide 15]*  
> *"Một lần nữa, nhóm chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới **Tiến sĩ Trần Khánh Dung** đã luôn tận tâm dìu dắt nhóm hoàn thành đề tài này.*  
> *Chúng em xin trân trọng cảm ơn quý Thầy Cô trong Hội đồng đã chú ý lắng nghe.*  
> *Sau đây, nhóm chúng em xin phép được lắng nghe ý kiến nhận xét và giải đáp các câu hỏi phản biện của Hội đồng. Em xin trân trọng cảm ơn!"*

---

## III. BỘ CÂU HỎI & TRẢ LỜI PHẢN BIỆN DỰ KIẾN (Q&A DEFENSE GUIDE)

### Câu 1: Làm thế nào hệ thống chống được hiện tượng 2 người cùng đặt 1 ghế (Race Condition)?
> **Trả lời:**  
> *"Thưa Thầy/Cô, hệ thống xử lý qua 2 tầng bảo vệ:*  
> *1. **Tầng ứng dụng**: Khi khách hàng chọn ghế, hệ thống ngay lập tức gán trạng thái `Held` và đóng dấu thời gian `HoldExpiresAt = UtcNow + 10 phút`. Mọi yêu cầu chọn ghế từ người khác trong khoảng thời gian này đều bị từ chối.*  
> *2. **Tầng cơ sở dữ liệu**: Khi thanh toán, câu lệnh Update được bọc trong một `Database Transaction` với mức cô lập phù hợp, kiểm tra lại điều kiện ghế chưa bị `Booked`. Nhờ đó loại bỏ hoàn toàn khả năng 2 khách hàng mua trùng một vị trí ghế."*

### Câu 2: Background Worker hoạt động thế nào và có ảnh hưởng đến hiệu năng Web không?
> **Trả lời:**  
> *"Thưa Thầy/Cô, nhóm sử dụng `IHostedService / BackgroundService` tích hợp sẵn trong .NET 10.*  
> *Worker này chạy ngầm trên một background thread hoàn toàn tách biệt với Web Request Pipeline, theo chu kỳ `PeriodicTimer` mỗi 30 giây hoặc 1 phút.*  
> *Mỗi chu kỳ, Worker chỉ thực hiện một truy vấn nhẹ quét các ghế ở trạng thái `Held` có `HoldExpiresAt < UtcNow` để hoàn trả về trạng thái trống (`Available`). Do đó, Worker chiếm dụng CPU và RAM cực thấp (< 1%), không gây bất kỳ độ trễ nào cho khách hàng đang lướt web."*

### Câu 3: Làm sao ngăn ngừa việc khách hàng chụp màn hình mã QR gửi cho người khác đi xem trước?
> **Trả lời:**  
> *"Thưa Thầy/Cô, mã QR của CineManagement không chỉ chứa mã vé thông thường mà chứa chuỗi `QrPayload` được sinh ngẫu nhiên theo chuẩn bảo mật và được lưu trong CSDL.*  
> *Khi nhân viên quét mã tại cửa, hệ thống lập tức kiểm tra: nếu vé đang ở trạng thái `Confirmed`, hệ thống đổi ngay trạng thái sang `CheckedIn / Used` và ghi nhận nhân viên soát vé cùng thời gian check-in.*  
> *Nếu có bất kỳ ai sử dụng lại ảnh chụp mã QR này lần thứ hai, màn hình quét lập tức hiển thị màu đỏ cảnh báo: **'Vé đã được sử dụng lúc [giờ:phút]'**, ngăn chặn hoàn toàn việc gian lận vé."*

### Câu 4: Nhóm phân chia công việc trong 4 Sprint thế nào để đạt 90 Story Points mà không trễ hạn?
> **Trả lời:**  
> *"Thưa Thầy/Cô, nhóm áp dụng đúng quy trình Scrum:*  
> *- **Sprint Planning**: Ước lượng điểm bằng Planning Poker, chia nhỏ User Story không quá 8 SP.*  
> *- **Daily Scrum**: Họp ngắn 15 phút mỗi sáng để tháo gỡ ngay các vướng mắc (Blockers).*  
> *- **Definition of Done (DoD) chặt chẽ**: Mỗi tính năng chỉ được xem là xong khi đã viết mã, review code trên GitHub và kiểm thử chạy thực tế.*  
> *Nhờ chia việc song song giữa Front-end, Back-end và Database theo hợp đồng API rõ ràng, nhóm đã hoàn thành trọn vẹn 90 Story Points đúng cam kết."*
