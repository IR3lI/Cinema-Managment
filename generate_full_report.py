# -*- coding: utf-8 -*-
"""
generate_full_report.py
Tạo Báo cáo Quản lý Dự án Công nghệ Thông tin hoàn chỉnh:
- Đề tài: XÂY DỰNG HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM TRỰC TUYẾN (CINEMA MANAGEMENT SYSTEM)
- Khung làm việc: Agile / Scrum (4 Sprint, 21 User Stories)
- Nền tảng: ASP.NET Core MVC & .NET 10, MySQL / MariaDB 10.11 (Port 3306, utf8mb4_unicode_ci)
- Tích hợp ảnh thực tế: Biểu đồ Scrum, Jira boards Sprint 1-4, Use Case 4 phân hệ, Sequence diagrams, Database ERD (14 bảng), Kiến trúc hệ thống
- Khung ảnh chụp màn hình (Hình 16 - 33) giữ nguyên để người dùng tự chụp dán từ app đang chạy.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx_helpers import (
    set_cell_margins, set_cell_shading, set_cell_border,
    add_header_cell, add_body_cell, add_image_placeholder, add_diagram_image
)

def create_report():
    doc = Document()

    # 1. Căn lề trang chuẩn báo cáo học thuật HUCE (Trên 2cm, Dưới 2cm, Trái 3cm, Phải 2cm)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        
        # Đánh số trang tự động ở Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("Báo cáo QLDACNTT - Nhóm Cinema Management | Trang ")
        f_run.font.name = "Times New Roman"
        f_run.font.size = Pt(9)
        f_run.font.color.rgb = RGBColor(148, 163, 184)
        
        f_xml = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        f_p._p.append(f_xml)

    # Style Helpers
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.3, bold=False, italic=False, size=13, color=(30, 41, 59)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = RGBColor(*color)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138) # Navy Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 64, 175)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # ==========================================
    # 1. TRANG BÌA (COVER PAGE)
    # ==========================================
    add_p("TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(15, 23, 42), space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, color=(30, 58, 138), space_after=18)

    logo_path = os.path.join("extracted_media", "image1.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(18)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))
    else:
        add_p("[LOGO TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI]", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, color=(148, 163, 184), space_after=18)

    add_p("BÀI TẬP LỚN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, color=(15, 23, 42), space_after=4)
    add_p("MÔN HỌC: QUẢN LÝ DỰ ÁN CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, color=(30, 58, 138), space_after=16)

    add_p("ĐỀ TÀI:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(100, 116, 139), space_after=4)
    add_p("XÂY DỰNG HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM TRỰC TUYẾN\n(CINEMA MANAGEMENT SYSTEM)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=17, color=(185, 28, 28), space_after=36)

    info_table = doc.add_table(rows=7, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "TS. Trần Khánh Dung"),
        ("Lớp học phần:", "66PMx"),
        ("Sinh viên thực hiện:", "Lâm Tuấn Kiệt (Trưởng nhóm / PO) – Ký hiệu: KL"),
        ("", "Luyện Đức Chiến (Scrum Master / Backend) – Ký hiệu: CL"),
        ("", "Nguyễn Phúc Tiến (Backend / Database) – Ký hiệu: TP"),
        ("", "Nguyễn Tiến Đạt (Fullstack / Worker) – Ký hiệu: DN"),
        ("", "Trần Phương Nam (UI/UX & Tester) – Ký hiệu: NT")
    ]
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = Cm(5.5), Cm(10.0)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(label)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(30, 41, 59)
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(val)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(12)
        r2.font.color.rgb = RGBColor(15, 23, 42)

    add_p("\n\n\nHÀ NỘI, NĂM 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(71, 85, 105), space_before=24)
    doc.add_page_break()

    # ==========================================
    # 2. TÓM TẮT DỰ ÁN & ABSTRACT
    # ==========================================
    add_h1("TÓM TẮT DỰ ÁN")
    add_p(
        "Dự án tập trung vào việc nghiên cứu, phân tích, thiết kế và phát triển Hệ thống Quản lý và Đặt vé Rạp chiếu phim "
        "kỹ thuật số (Cinema Management System) nhằm giải quyết bài toán chuyển đổi số toàn diện cho các cụm rạp chiếu phim hiện đại. "
        "Quy trình quản lý dự án được áp dụng chặt chẽ theo khung làm việc Agile/Scrum, chia thành 4 Sprint với 21 User Stories hoàn chỉnh."
    )
    add_p(
        "Hệ thống được thiết kế với kiến trúc phân quyền đa vai trò (Role-Based Access Control - RBAC) độc lập, phục vụ ba nhóm đối tượng "
        "người dùng chính: Khách hàng (Customer), Nhân viên rạp (Staff) và Quản trị viên (Admin)."
    )
    add_p(
        "• Đối với Khách hàng, hệ thống mang lại trải nghiệm xem phim số hóa hiện đại: tra cứu thông tin phim, xem trailer YouTube bản quyền, "
        "tìm kiếm và lọc phim đa tiêu chí, lựa chọn suất chiếu theo ngày/phòng, tương tác trực quan trên sơ đồ ghế động (phân loại ghế Standard, VIP, Couple), "
        "cơ chế khóa ghế tạm thời thời gian thực (Real-time Seat Hold 10 phút) chống tranh chấp ghế, tích hợp đặt kèm combo đồ ăn/thức uống (F&B), "
        "áp dụng mã giảm giá (Voucher), thanh toán chuyển khoản ví điện tử chuẩn VietQR, và hệ thống tự động gửi vé điện tử "
        "chứa mã QR bảo mật về Gmail đã đăng ký của khách hàng (hoàn toàn tự động qua Gmail SMTP mà không cần người dùng nhập lại email)."
    )
    add_p(
        "• Đối với Nhân viên (Staff), hệ thống cung cấp công cụ quét mã QR bằng camera điện thoại di động (Mobile QR Scanner) để soát vé tại cửa "
        "phòng chiếu, xác thực tính hợp lệ của vé chỉ dưới 2 giây, ngăn chặn triệt để vé giả và tình trạng sử dụng lại vé."
    )
    add_p(
        "• Đối với Quản trị viên (Admin), hệ thống cung cấp Dashboard quản trị tập trung: quản lý danh mục phim kèm 15 poster điện ảnh chuẩn kích thước, "
        "quản lý tài khoản nhân viên, cấu hình thông số phòng chiếu và tự động sinh ma trận ghế, lập lịch suất chiếu tối ưu chống trùng lặp, "
        "quản lý combo F&B, chiến dịch voucher và theo dõi biểu đồ thống kê doanh thu cùng tỷ lệ lấp đầy rạp (Occupancy Rate)."
    )
    add_p(
        "Sản phẩm được xây dựng dựa trên nền tảng ASP.NET Core MVC & RESTful API (.NET 10), hệ quản trị cơ sở dữ liệu MySQL / MariaDB 10.11 "
        "(kết nối cổng 3306, collation chuẩn tiếng Việt utf8mb4_unicode_ci, ORM Pomelo.EntityFrameworkCore.MySql kết hợp chế độ SQLite dự phòng), "
        "thư viện QRCoder, giao diện tông màu Trắng Kem (#FAF7F2) phong cách điện ảnh thanh lịch, trang lịch sử vé Cinema Pass hiện đại, "
        "và dịch vụ nền Background Hosted Service tự động giải phóng ghế hết hạn. Dự án được đóng gói hoàn chỉnh dưới dạng tệp thực thi độc lập "
        "(Self-contained Single-file EXE CineManagement.exe kèm file nén CinemaManagement-Demo.zip), đảm bảo tính toàn vẹn và bảo tồn 100% dữ liệu qua các lần khởi động."
    )
    add_p("Từ khóa: Quản lý dự án, Agile, Scrum, Đặt vé xem phim, Real-time Seat Hold, QR Code Ticket, MySQL, VietQR, Gmail SMTP, ASP.NET Core.", italic=True, bold=True)

    add_h1("ABSTRACT OF PROJECT")
    add_p(
        "The project focuses on the research, analysis, architectural design, and software implementation of a comprehensive "
        "Digital Cinema Management and Online Booking Ecosystem to streamline modern cinema operational workflows. The software engineering "
        "lifecycle strictly follows the Agile/Scrum framework, structured into 4 cohesive Sprints delivering 21 comprehensive User Stories."
    )
    add_p(
        "The application implements a robust Role-Based Access Control (RBAC) mechanism catering to three primary user roles: Customer, Staff, and Administrator."
    )
    add_p(
        "• For Customers, the platform delivers an engaging digital experience: browsing curated movie catalogs with high-definition local posters, "
        "watching trailers, advanced multi-criteria filtering, dynamic showtime selection, interactive visual seat mapping (supporting Standard, VIP, and Couple seat tiers), "
        "a 10-minute real-time seat locking mechanism preventing concurrent booking race conditions, concession (Food & Beverage) add-ons, voucher discount redemptions, "
        "seamless VietQR digital payment (Account Number ), and automated e-ticket dispatch with secure QR code directly to the customer's registered Gmail account via Gmail SMTP."
    )
    add_p(
        "• For Cinema Staff, a mobile-first QR code scanning interface utilizing device cameras enables instant ticket admission validation at auditorium "
        "entrances in under two seconds, eliminating ticket fraud and double check-ins."
    )
    add_p(
        "• For Administrators, a centralized management portal provides tools for movie catalog CRUD, employee administration, auditorium geometry configuration "
        "with automated seat grid generation, collision-free showtime scheduling, concession catalog management, promotional voucher campaigns, and dynamic "
        "analytical dashboards monitoring daily revenue streams alongside auditorium occupancy rates."
    )
    add_p(
        "Technologically, the platform leverages ASP.NET Core MVC & RESTful Web APIs (.NET 10), MySQL / MariaDB 10.11 database (port 3306, utf8mb4 collation with SQLite fallback), "
        "Tailwind CSS in Warm Cream White palette (#FAF7F2), QRCoder library, and an automated Background Hosted Service worker for expiring unpaid seat holds. "
        "The application is packaged into a self-contained, single-file Windows executable (CineManagement.exe) ensuring portability and 100% data durability across deployments."
    )
    add_p("Keywords: Project Management, Agile, Scrum, Cinema Management, Real-time Seat Hold, QR Code Ticket, MySQL, VietQR, Gmail SMTP, ASP.NET Core.", italic=True, bold=True)
    doc.add_page_break()

    # ==========================================
    # 3. MỤC LỤC & DANH MỤC HÌNH ẢNH / BẢNG BIỂU
    # ==========================================
    add_h1("MỤC LỤC BÁO CÁO")
    toc_items = [
        ("TÓM TẮT DỰ ÁN", "1"),
        ("ABSTRACT OF PROJECT", "2"),
        ("DANH MỤC HÌNH ẢNH", "4"),
        ("DANH MỤC BẢNG BIỂU", "5"),
        ("PHẦN 1: MÔ TẢ ĐỀ TÀI VÀ ĐỊNH HƯỚNG GIẢI PHÁP", "6"),
        ("  1.1. Đặt vấn đề và tính cấp thiết", "6"),
        ("  1.2. Mục tiêu dự án (Product Goal)", "6"),
        ("  1.3. Khảo sát đối tượng người dùng", "7"),
        ("  1.4. Yêu cầu chức năng và phi chức năng", "7"),
        ("  1.5. Cơ sở lý thuyết và công nghệ lựa chọn", "8"),
        ("PHẦN 2: LẬP KẾ HOẠCH VÀ QUẢN LÝ DỰ ÁN THEO AGILE/SCRUM", "9"),
        ("  2.1. Cơ cấu nhân sự và vai trò trong Scrum Team", "9"),
        ("  2.2. Product Backlog chuẩn hóa (21 User Stories)", "10"),
        ("  2.3. Lịch biểu Sprints và Kế hoạch thời gian (Timeline)", "12"),
        ("  2.4. Phân tích chi tiết tiến độ thực hiện từng Sprint", "12"),
        ("  2.5. Bảng quản lý tiến độ tổng thể (Project Table / WBS)", "14"),
        ("PHẦN 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", "15"),
        ("  3.1. Kiến trúc hệ thống tổng thể", "15"),
        ("  3.2. Phân tích và Thiết kế Biểu đồ Use Case", "16"),
        ("    3.2.1. Xác định tác nhân (Actors) và phạm vi hệ thống", "16"),
        ("    3.2.2. Bảng phân rã Use Case và ánh xạ 21 User Stories", "17"),
        ("    3.2.3. Biểu đồ Use Case tổng thể toàn hệ thống", "18"),
        ("    3.2.4. Biểu đồ Use Case Phân hệ 1: Xác thực & Quản trị người dùng", "19"),
        ("    3.2.5. Biểu đồ Use Case Phân hệ 2: Phim, Phòng chiếu & Suất chiếu", "20"),
        ("    3.2.6. Biểu đồ Use Case Phân hệ 3: Đặt vé, Giữ ghế 10p & Thanh toán", "21"),
        ("    3.2.7. Biểu đồ Use Case Phân hệ 4: Soát vé mã QR & Báo cáo thống kê", "22"),
        ("    3.2.8. Các bảng đặc tả Use Case chi tiết", "23"),
        ("  3.3. Biểu đồ Tuần tự (Sequence Diagram)", "26"),
        ("  3.4. Thiết kế Cơ sở dữ liệu MySQL và Sơ đồ Thực thể (Database ERD)", "28"),
        ("PHẦN 4: KẾT QUẢ TRIỂN KHAI VÀ GIAO DIỆN SẢN PHẨM", "31"),
        ("  4.1. Quy trình phát triển qua các giai đoạn", "31"),
        ("  4.2. Giao diện thực tế của hệ thống (HCI)", "32"),
        ("  4.3. Kết quả kiểm thử hệ thống (Testing Results)", "36"),
        ("  4.4. Đóng gói và phát hành sản phẩm (Self-contained Package)", "37"),
        ("PHẦN 5: ĐÁNH GIÁ VÀ QUẢN LÝ RỦI RO (RISK MANAGEMENT)", "38"),
        ("  5.1. Tầm quan trọng của quản lý rủi ro", "38"),
        ("  5.2. Các bảng thông tin rủi ro chi tiết (Risk Information Sheets)", "38"),
        ("PHẦN 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "41"),
        ("  6.1. Tự đánh giá mức độ hoàn thành", "41"),
        ("  6.2. So sánh giải pháp với thị trường thực tế", "41"),
        ("  6.3. Bài học kinh nghiệm trong quản lý dự án", "42"),
        ("  6.4. Hướng phát triển trong tương lai", "42"),
        ("PHẦN 7: BIÊN BẢN CÁC CUỘC HỌP SCRUM (SCRUM MEETING NOTES)", "43"),
        ("  7.1. Biên bản họp Lập kế hoạch Sprint (Sprint Planning)", "43"),
        ("  7.2. Biên bản họp Scrum hàng ngày (Daily Scrum Sample)", "43"),
        ("  7.3. Biên bản họp Sơ kết Sprint (Sprint Review)", "44"),
        ("  7.4. Biên bản họp Cải tiến Sprint (Sprint Retrospective)", "45"),
        ("TÀI LIỆU THAM KHẢO", "46")
    ]
    for title, page in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(2)
        r_t = p_toc.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        if title.startswith("PHẦN") or title.startswith("TÓM") or title.startswith("ABSTRACT") or title.startswith("DANH") or title.startswith("TÀI"):
            r_t.font.bold = True
        r_dots = p_toc.add_run(" " + "." * max(5, 75 - len(title) * 2) + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        r_p = p_toc.add_run(page)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)
        r_p.font.bold = True

    doc.add_page_break()

    # DANH MỤC HÌNH ẢNH
    add_h1("DANH MỤC HÌNH ẢNH")
    figures_list = [
        ("Hình 1", "Quy trình khung làm việc Agile Scrum áp dụng trong dự án"),
        ("Hình 2", "Tiến độ tổng thể Sprint 1 trên Jira Board"),
        ("Hình 3", "Tiến độ tổng thể Sprint 2 trên Jira Board"),
        ("Hình 4", "Tiến độ tổng thể Sprint 3 trên Jira Board"),
        ("Hình 5", "Tiến độ tổng thể Sprint 4 trên Jira Board"),
        ("Hình 6", "Biểu đồ Use Case tổng thể toàn hệ thống"),
        ("Hình 7", "Biểu đồ Use Case Phân hệ 1: Xác thực và Quản trị người dùng"),
        ("Hình 8", "Biểu đồ Use Case Phân hệ 2: Phim, Phòng chiếu và Suất chiếu"),
        ("Hình 9", "Biểu đồ Use Case Phân hệ 3: Đặt vé, Giữ ghế 10p và Thanh toán"),
        ("Hình 10", "Biểu đồ Use Case Phân hệ 4: Soát vé bằng mã QR và Báo cáo"),
        ("Hình 11", "Biểu đồ Sequence chức năng Đặt vé và Khóa ghế tạm thời 10 phút"),
        ("Hình 12", "Biểu đồ Sequence chức năng Thanh toán VietQR và Phát hành vé điện tử QR qua Gmail"),
        ("Hình 13", "Biểu đồ Sequence chức năng Nhân viên quét mã QR soát vé"),
        ("Hình 14", "Sơ đồ quan hệ thực thể CSDL MySQL (Database ERD - 14 bảng quan hệ)"),
        ("Hình 15", "Biểu đồ Kiến trúc phân tầng ASP.NET Core MVC & MySQL"),
        ("Hình 16", "Giao diện Đăng ký tài khoản khách hàng"),
        ("Hình 17", "Giao diện Đăng nhập hệ thống đa vai trò"),
        ("Hình 18", "Giao diện Hồ sơ cá nhân người dùng"),
        ("Hình 19", "Giao diện Trang chủ và Bộ lọc danh mục phim (Tông màu Trắng Kem #FAF7F2)"),
        ("Hình 20", "Giao diện Chi tiết phim và Danh sách suất chiếu theo ngày"),
        ("Hình 21", "Giao diện Chọn ghế trực quan với đồng hồ đếm ngược 10 phút"),
        ("Hình 22", "Giao diện Chọn Combo bắp nước F&B"),
        ("Hình 23", "Giao diện Thanh toán VietQR và Áp dụng mã Voucher"),
        ("Hình 24", "Giao diện Xác nhận đơn hàng và hiển thị vé điện tử QR"),
        ("Hình 25", "Giao diện Xem lịch sử đặt vé phong cách Thẻ vé xem phim (Cinema Pass)"),
        ("Hình 26", "Giao diện Đánh giá và bình luận phim"),
        ("Hình 27", "Giao diện Quản lý nhân viên (Admin)"),
        ("Hình 28", "Giao diện Quản lý danh mục phim kèm poster điện ảnh (Admin)"),
        ("Hình 29", "Giao diện Cấu hình phòng chiếu và sơ đồ ma trận ghế (Admin)"),
        ("Hình 30", "Giao diện Lập lịch suất chiếu chống trùng giờ (Admin)"),
        ("Hình 31", "Giao diện Quản lý danh mục F&B và Voucher (Admin)"),
        ("Hình 32", "Giao diện Nhân viên quét mã QR soát vé qua camera điện thoại"),
        ("Hình 33", "Giao diện Dashboard Thống kê doanh thu và tỷ lệ lấp đầy rạp")
    ]
    for num, cap in figures_list:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.space_before = Pt(1)
        p_fig.paragraph_format.space_after = Pt(2)
        r_f = p_fig.add_run(f"{num}: {cap}")
        r_f.font.name = "Times New Roman"
        r_f.font.size = Pt(11)

    doc.add_page_break()

    # DANH MỤC BẢNG BIỂU
    add_h1("DANH MỤC BẢNG BIỂU")
    tables_list = [
        ("Bảng 1", "Cơ cấu nhân sự và phân định vai trò Scrum Team"),
        ("Bảng 2", "Danh sách Product Backlog chuẩn hóa (21 User Stories)"),
        ("Bảng 3", "Kế hoạch phân bổ thời gian các Sprints"),
        ("Bảng 4", "Bảng theo dõi tiến độ công việc tổng thể (Project Table / WBS)"),
        ("Bảng 5", "Bảng phân rã Use Case theo 4 phân hệ và ánh xạ 21 User Stories"),
        ("Bảng 6", "Bảng đặc tả Use Case UC01 – Đăng nhập hệ thống"),
        ("Bảng 7", "Bảng đặc tả Use Case UC02 – Đặt vé & Giữ ghế thời gian thực"),
        ("Bảng 8", "Bảng đặc tả Use Case UC03 – Quét mã QR soát vé"),
        ("Bảng 9", "Bảng đặc tả Use Case UC04 – Lập lịch suất chiếu chống trùng lặp"),
        ("Bảng 10", "Bảng danh mục 14 bảng dữ liệu trong CSDL MySQL (cinema_db)"),
        ("Bảng 11", "Bảng tổng hợp Test Cases và kết quả kiểm thử hệ thống"),
        ("Bảng 12", "Bảng thông tin rủi ro R01 – Xung đột giữ ghế đồng thời (Race Condition)"),
        ("Bảng 13", "Bảng thông tin rủi ro R02 – Treo tiến trình Background Service giải phóng ghế"),
        ("Bảng 14", "Bảng thông tin rủi ro R03 – Lỗi mạng và gián đoạn cổng thanh toán"),
        ("Bảng 15", "Bảng thông tin rủi ro R04 – Sự cố camera và vé giả mạo khi soát vé")
    ]
    for num, cap in tables_list:
        p_tab = doc.add_paragraph()
        p_tab.paragraph_format.space_before = Pt(1)
        p_tab.paragraph_format.space_after = Pt(2)
        r_t = p_tab.add_run(f"{num}: {cap}")
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)

    doc.add_page_break()

    # ==========================================
    # PHẦN 1: MÔ TẢ ĐỀ TÀI VÀ ĐỊNH HƯỚNG GIẢI PHÁP
    # ==========================================
    add_h1("PHẦN 1: MÔ TẢ ĐỀ TÀI VÀ ĐỊNH HƯỚNG GIẢI PHÁP")
    
    add_h2("1.1. Đặt vấn đề và tính cấp thiết")
    add_p(
        "Trong thời kỳ bùng nổ của chuyển đổi số và công nghệ thông tin, ngành dịch vụ giải trí – đặc biệt là rạp chiếu phim – "
        "đang chứng kiến sự thay đổi mạnh mẽ trong thị hiếu và thói quen tiêu dùng. Khách hàng ngày càng ưu tiên sự tiện lợi, "
        "nhanh chóng và trải nghiệm cá nhân hóa ngay trên các thiết bị di động cá nhân."
    )
    add_p(
        "Tuy nhiên, qua khảo sát thực tế tại các cụm rạp chiếu phim vừa và nhỏ, quy trình vận hành truyền thống vẫn đang bộc lộ "
        "những điểm nghẽn nghiêm trọng:"
    )
    add_p("1. Xếp hàng và ùn tắc tại quầy vé: Vào các khung giờ cao điểm, dịp cuối tuần hoặc ngày lễ tết, lượng khách hàng dồn về rạp rất lớn. Việc khách hàng phải xếp hàng chờ đợi từ 15 đến 30 phút để mua vé, chọn ghế và mua bắp nước gây ra tâm lý mệt mỏi và làm giảm trải nghiệm giải trí.")
    add_p("2. Sai sót và gian lận trong quản lý vé giấy: Vé giấy truyền thống dễ bị rách, thất lạc, tốn kém chi phí in ấn và rất khó kiểm soát chặt chẽ quy trình soát vé của nhân viên tại cửa phòng chiếu, dễ phát sinh tiêu cực.")
    add_p("3. Thất thoát doanh thu do giữ chỗ ảo: Việc khách hàng đổi ý hoặc giữ ghế nhưng không thanh toán kịp thời khiến rạp bị trống ghế trong những suất chiếu đông khách nếu không có cơ chế tự động nhả ghế.")
    add_p("4. Thiếu hụt số liệu thống kê thời gian thực: Ban quản lý rạp khó nắm bắt tức thời doanh số bán vé, lượng bắp nước tiêu thụ cũng như tỷ lệ lấp đầy (Occupancy Rate) của từng phòng chiếu để kịp thời điều chỉnh kế hoạch kinh doanh.")
    add_p(
        "Xuất phát từ các lý do cấp thiết trên, dự án “Xây dựng Hệ thống Quản lý và Đặt vé Rạp chiếu phim trực tuyến (Cinema Management System)” "
        "được triển khai nhằm giải quyết triệt để các tồn tại trên, mang lại lợi ích kép cho cả khách hàng và ban quản lý rạp."
    )

    add_h2("1.2. Mục tiêu dự án (Product Goal)")
    add_p(
        "• Product Goal: Xây dựng một hệ sinh thái rạp chiếu phim kỹ thuật số hoàn chỉnh, số hóa 100% quy trình từ khâu tra cứu thông tin, "
        "đặt vé trực tuyến, giữ ghế thời gian thực của khách hàng cho đến nghiệp vụ soát vé di động của nhân viên và báo cáo doanh thu quản trị của ban giám đốc.",
        bold=True
    )
    add_p("Chỉ tiêu chất lượng phần mềm cần đạt được:")
    add_p("- Hoàn thành đầy đủ 21 User Stories đã cam kết trong Product Backlog qua 4 Sprint.")
    add_p("- Tối ưu hóa thời gian đặt vé của khách hàng dưới 2 phút.")
    add_p("- Cơ chế giữ ghế thời gian thực hoạt động chính xác tuyệt đối, triệt tiêu lỗi xung đột đồng thời (Concurrency Race Condition).")
    add_p("- Tốc độ quét và xác thực vé QR bằng camera di động của nhân viên đạt dưới 2 giây/vé.")
    add_p("- Hệ thống thanh toán trực tuyến hỗ trợ chuẩn VietQR chính xác đến từng đồng.")
    add_p("- Tự động gửi vé điện tử (HTML Card & ảnh QR) về đúng Gmail đăng ký tài khoản khách hàng thông qua Google Gmail SMTP.")
    add_p("- Ứng dụng được đóng gói thành tệp thực thi duy nhất (Self-contained Portable EXE) CineManagement.exe kết nối hệ quản trị CSDL MySQL / MariaDB 10.11 bền vững, đảm bảo bảo lưu dữ liệu 100%.")

    add_h2("1.3. Khảo sát đối tượng người dùng")
    add_p("Hệ thống phục vụ ba nhóm đối tượng người dùng với các đặc điểm và nhu cầu riêng biệt:")
    add_p("• Khách hàng (Customer): Độ tuổi từ 15 đến 45, thường xuyên sử dụng điện thoại thông minh và máy tính. Có nhu cầu tra cứu phim đang chiếu/sắp chiếu với poster điện ảnh sắc nét, xem trailer YouTube bản quyền, chọn vị trí ghế ưng ý, mua combo bắp nước, áp mã giảm giá, quét mã VietQR thanh toán nhanh và tự động nhận vé điện tử QR qua email cá nhân.")
    add_p("• Nhân viên rạp (Staff): Nhân viên quầy vé và nhân viên soát vé tại cửa phòng. Cần công cụ quét mã QR bằng camera điện thoại di động đơn giản, phản hồi tức thì để xác thực khách vào rạp.")
    add_p("• Quản trị viên (Admin): Ban quản trị rạp. Cần công cụ quản lý danh mục phim, cấu hình phòng chiếu và sơ đồ ghế, lập lịch suất chiếu chống trùng giờ, quản lý F&B, voucher và xem báo cáo biểu đồ doanh thu.")

    add_h2("1.4. Yêu cầu chức năng và phi chức năng")
    add_p("Yêu cầu chức năng chính gồm:")
    add_p("- Module Xác thực & Phân quyền: Đăng ký tài khoản, đăng nhập, đổi mật khẩu, phân quyền RBAC 3 vai trò (Admin, Staff, Customer).")
    add_p("- Module Phim & Suất chiếu: CRUD phim, trailer YouTube, upload và quản lý poster nội bộ (15 phim có sẵn); quản lý phòng chiếu (Standard, VIP, IMAX) và ma trận ghế; lập lịch suất chiếu chống trùng giờ.")
    add_p("- Module Đặt vé & Giữ ghế: Chọn ghế tương tác trực quan (tính toán chính xác số tiền, không tính thừa ghế), khóa ghế tạm thời 10 phút, worker tự động nhả ghế quá hạn, mua kèm combo F&B, áp voucher giảm giá, thanh toán chuyển khoản VietQR.")
    add_p("- Module Vé điện tử & Soát vé: Sinh vé điện tử mã QR, tự động gửi Gmail vé điện tử qua SMTP, ứng dụng web camera di động soát vé cho nhân viên.")
    add_p("- Module Lịch sử vé & Báo cáo: Xem lịch sử đặt vé phong cách Cinema Pass, khách hàng đánh giá phim 1-5 sao; Admin xem Dashboard biểu đồ doanh thu theo ngày và tỷ lệ lấp đầy ghế.")

    add_h2("1.5. Cơ sở lý thuyết và công nghệ lựa chọn")
    add_p("Dự án áp dụng khung làm việc Agile Scrum với 4 Sprint, đo lường bằng Story Points (SP) thông qua Planning Poker.")
    add_p("Công nghệ lựa chọn:")
    add_p("- Backend: C# / .NET 10 (ASP.NET Core MVC & RESTful Web API).")
    add_p("- Cơ sở dữ liệu: Hệ quản trị CSDL quan hệ MySQL / MariaDB 10.11 (Port 3306, Collation utf8mb4_unicode_ci, ORM Pomelo.EntityFrameworkCore.MySql, hỗ trợ dual-provider SQLite dự phòng).")
    add_p("- Dịch vụ chạy nền: Background Hosted Service (SeatHoldTimeoutWorker chu kỳ 30 giây).")
    add_p("- Dịch vụ Email: MailKit / MimeKit kết nối Google Gmail SMTP (smtp.gmail.com:587 TLS, App Password).")
    add_p("- Cổng thanh toán: VietQR API (Chuẩn thanh toán liên ngân hàng Napas 247).")
    add_p("- Xử lý mã QR: Thư viện QRCoder (server-side) và html5-qrcode (client-side scanner camera).")
    add_p("- Frontend: HTML5, CSS3, Tailwind CSS v4 tông màu Trắng Kem (#FAF7F2), Phosphor Icons, JavaScript ES6 Fetch API.")
    add_p("- Đóng gói & Triển khai: Single-File Self-contained EXE (CineManagement.exe ~60MB) kèm server MariaDB daemon.")

    add_diagram_image(doc, "1", "Quy trình khung làm việc Agile Scrum áp dụng trong dự án", "diagrams/fig1_scrum_process.png", width_inches=6.2)

    # ==========================================
    # PHẦN 2: LẬP KẾ HOẠCH VÀ QUẢN LÝ DỰ ÁN THEO AGILE/SCRUM
    # ==========================================
    add_h1("PHẦN 2: LẬP KẾ HOẠCH VÀ QUẢN LÝ DỰ ÁN THEO AGILE/SCRUM")
    
    add_h2("2.1. Cơ cấu nhân sự và vai trò trong Scrum Team")
    add_p("Bảng 1 trình bày cơ cấu 5 thành viên trong nhóm dự án tương ứng với vai trò và mã ký hiệu trên Jira Board:")

    # Table 1: Nhân sự
    t1 = doc.add_table(rows=6, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_headers = ["STT", "Họ và tên", "Ký hiệu Jira", "Vai trò Scrum", "Nhiệm vụ chính trong dự án"]
    for i, h in enumerate(t1_headers):
        add_header_cell(t1.rows[0], i, h)
    
    t1_data = [
        ("1", "Lâm Tuấn Kiệt", "KL", "Product Owner / Dev", "Định nghĩa Product Goal, quản lý Backlog, lập trình Suất chiếu, Thanh toán VietQR và Dashboard"),
        ("2", "Luyện Đức Chiến", "CL", "Scrum Master / Dev", "Điều phối quy trình Scrum, lập trình Auth/RBAC, Cơ chế giữ ghế 10p và Dịch vụ gửi Gmail tự động"),
        ("3", "Nguyễn Phúc Tiến", "TP", "Backend / Database", "Thiết kế CSDL MySQL 14 bảng quan hệ, bảng mã utf8mb4, Sơ đồ ghế, API Camera quét mã QR soát vé"),
        ("4", "Nguyễn Tiến Đạt", "DN", "Fullstack / Worker", "Bộ lọc tìm kiếm phim, quản lý danh mục F&B, áp mã Voucher, Hosted Worker tự động hủy giữ ghế"),
        ("5", "Trần Phương Nam", "NT", "UI/UX & QA Tester", "Thiết kế giao diện Trắng Kem #FAF7F2, CRUD Danh mục phim, kịch bản Test Cases và kiểm thử E2E")
    ]
    for row_idx, data in enumerate(t1_data):
        row = t1.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 1: Cơ cấu nhân sự và phân định vai trò Scrum Team", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    add_h2("2.2. Product Backlog chuẩn hóa (21 User Stories)")
    add_p("Toàn bộ 21 User Stories được chuẩn hóa theo quy tắc INVEST với đầy đủ tiêu chí chấp nhận (AC), độ ưu tiên và Story Point:")

    # Table 2: Product Backlog
    t2 = doc.add_table(rows=22, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_headers = ["Mã US", "User Story", "Tiêu chí chấp nhận (Acceptance Criteria)", "Sprint", "Ưu tiên", "SP"]
    for i, h in enumerate(t2_headers):
        add_header_cell(t2.rows[0], i, h)

    backlog_data = [
        ("US-01", "Là khách hàng, tôi muốn đăng ký tài khoản", "Validate email, sđt, mật khẩu >= 6 ký tự; báo lỗi nếu trùng lặp", "1", "High", "3"),
        ("US-02", "Là quản lý, tôi muốn cấp tài khoản nhân viên", "Admin tạo tài khoản nhân viên, phân quyền mặc định là Staff", "1", "Medium", "2"),
        ("US-03", "Là quản lý, tôi muốn đăng nhập Admin Panel", "Đăng nhập quyền Admin chuyển hướng đến Dashboard rạp", "1", "High", "3"),
        ("US-04", "Là hệ thống, tôi muốn phân quyền truy cập", "Bảo mật Cookie Authentication & RBAC cho Admin, Staff, Customer", "1", "Critical", "5"),
        ("US-05", "Là quản lý, tôi muốn CRUD phim và trailer", "CRUD phim, upload poster, nhúng link trailer YouTube, trạng thái", "1", "High", "5"),
        ("US-06", "Là khách hàng, tôi muốn tìm kiếm và lọc phim", "Tìm kiếm theo từ khóa tên phim; lọc chính xác theo thể loại", "1", "Medium", "3"),
        ("US-07", "Là quản lý, tôi muốn tạo phòng chiếu & sơ đồ ghế", "Cấu hình số hàng, cột; tự sinh ma trận ghế Standard, VIP, Couple", "2", "High", "5"),
        ("US-08", "Là quản lý, tôi muốn lên lịch suất chiếu", "Chọn phim, phòng, giờ chiếu; thuật toán chặn trùng lịch phòng", "2", "Critical", "5"),
        ("US-09", "Là quản lý, tôi muốn quản lý combo bắp nước F&B", "CRUD món ăn/đồ uống/combo, giá bán, upload ảnh minh họa", "2", "Medium", "3"),
        ("US-10", "Là khách hàng, tôi muốn xem chi tiết phim & lịch chiếu", "Hiển thị tóm tắt phim, trailer, dàn diễn viên và suất chiếu theo ngày", "2", "High", "3"),
        ("US-11", "Là khách hàng, tôi muốn chọn ghế trực quan", "Sơ đồ ghế trực quan; tính đúng tiền ghế, không tính thừa ghế dummy", "3", "High", "5"),
        ("US-12", "Là hệ thống, tôi muốn khóa ghế tạm thời 10 phút", "Ngăn người khác chọn trùng ghế; hiển thị đếm ngược 10:00", "3", "Critical", "8"),
        ("US-13", "Là khách hàng, tôi muốn mua kèm combo F&B", "Thêm/bớt số lượng combo F&B vào giỏ hàng và cộng dồn tổng tiền", "3", "Medium", "3"),
        ("US-14", "Là khách hàng, tôi muốn nhập mã voucher giảm giá", "Validate mã hợp lệ, hạn dùng, tính số tiền giảm theo % hoặc cố định", "3", "Medium", "3"),
        ("US-15", "Là khách hàng, tôi muốn thanh toán qua VietQR", "Sinh mã VietQR đúng số tiền sau voucher, đổi trạng thái Paid", "3", "High", "5"),
        ("US-16", "Là hệ thống, tôi muốn tự động hủy ghế hết hạn", "Worker ngầm quét định kỳ đơn giữ quá 10 phút và trả về ghế trống", "3", "Critical", "5"),
        ("US-17", "Là hệ thống, tôi muốn tự động gửi vé qua Gmail", "Tự động lấy Gmail đăng ký tài khoản, gửi vé HTML và mã QR qua SMTP", "4", "Critical", "5"),
        ("US-18", "Là nhân viên, tôi muốn quét mã QR soát vé", "Camera di động quét QR, kiểm tra hợp lệ dưới 2s, đổi trạng thái vé", "4", "Critical", "8"),
        ("US-19", "Là khách hàng, tôi muốn xem lịch sử đặt vé", "Danh sách vé kiểu Cinema Pass kèm trạng thái, chi tiết đơn và mã QR", "4", "Medium", "3"),
        ("US-20", "Là khách hàng, tôi muốn đánh giá và bình luận phim", "Đánh giá 1-5 sao, nhận xét; cập nhật điểm rating trung bình của phim", "4", "Low", "3"),
        ("US-21", "Là quản lý, tôi muốn xem báo cáo doanh thu & tỷ lệ lấp đầy", "Thống kê doanh thu theo ngày, số vé bán, biểu đồ occupancy rate", "4", "High", "5")
    ]
    for row_idx, data in enumerate(backlog_data):
        row = t2.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 2: Danh sách Product Backlog chuẩn hóa (21 User Stories)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    add_h2("2.3. Lịch biểu Sprints và Kế hoạch thời gian (Timeline)")
    add_p("Toàn bộ 4 Sprint được thực hiện liên tục với tổng số 90 Story Points:")

    # Table 3: Sprints Schedule
    t3 = doc.add_table(rows=5, cols=6)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ["Tên Sprint", "Bắt đầu", "Kết thúc", "Trọng tâm công việc", "Tổng SP", "Tỷ lệ hoàn thành"]
    for i, h in enumerate(t3_headers):
        add_header_cell(t3.rows[0], i, h)

    sprints_data = [
        ("Sprint 1", "18/08/2026", "25/08/2026", "Khởi tạo dự án, CSDL MySQL, Xác thực, Phân quyền RBAC, Quản lý phim", "21 SP", "100% (6/6 tasks)"),
        ("Sprint 2", "25/08/2026", "08/09/2026", "Phòng chiếu, Sơ đồ ghế động, Lịch chiếu Showtimes, Danh mục F&B", "16 SP", "100% (4/4 tasks)"),
        ("Sprint 3", "08/09/2026", "18/09/2026", "Chọn ghế trực quan, Khóa ghế 10p, VietQR, Voucher, Worker", "29 SP", "100% (6/6 tasks)"),
        ("Sprint 4", "18/09/2026", "28/09/2026", "Tự gửi Gmail vé QR, Soát vé Camera, Lịch sử Cinema Pass, Báo cáo rạp", "24 SP", "100% (5/5 tasks)")
    ]
    for row_idx, data in enumerate(sprints_data):
        row = t3.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1, 2, 4, 5] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 3: Kế hoạch phân bổ thời gian các Sprints", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    add_diagram_image(doc, "2", "Tiến độ tổng thể Sprint 1 trên Jira Board", "diagrams/fig2_sprint1_jira.png", width_inches=6.2)
    add_diagram_image(doc, "3", "Tiến độ tổng thể Sprint 2 trên Jira Board", "diagrams/fig3_sprint2_jira.png", width_inches=6.2)
    add_diagram_image(doc, "4", "Tiến độ tổng thể Sprint 3 trên Jira Board", "diagrams/fig4_sprint3_jira.png", width_inches=6.2)
    add_diagram_image(doc, "5", "Tiến độ tổng thể Sprint 4 trên Jira Board", "diagrams/fig5_sprint4_jira.png", width_inches=6.2)

    add_h2("2.4. Bảng quản lý tiến độ tổng thể (Project Table / WBS)")
    add_p("Bảng 4 thể hiện đối soát thời gian kế hoạch (Planned) và thực tế (Actual) của toàn bộ 20 đầu việc kỹ thuật theo chuẩn mẫu báo cáo HUCE:")

    # Table 4: Project Table
    t4 = doc.add_table(rows=21, cols=8)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_headers = ["Mã Task", "Tên công việc", "Bắt đầu KH", "Bắt đầu TT", "Xong KH", "Xong TT", "Phụ trách", "Effort"]
    for i, h in enumerate(t4_headers):
        add_header_cell(t4.rows[0], i, h)

    tasks_wbs = [
        ("T01", "Phân tích yêu cầu và thiết kế CSDL MySQL 14 bảng", "W1, D1", "W1, D1", "W1, D3", "W1, D2", "Tiến (TP)", "2 p-d"),
        ("T02", "Thiết kế UI phong cách Trắng Kem #FAF7F2 trên Figma", "W1, D1", "W1, D2", "W1, D4", "W1, D5", "Nam (NT)", "3 p-d"),
        ("T03", "Tạo module Xác thực & Tài khoản (Login/Signup)", "W1, D2", "W1, D3", "W1, D5", "W1, D5", "Chiến (CL)", "3 p-d"),
        ("T04", "Triển khai phân quyền RBAC đa vai trò (Admin, Staff, Customer)", "W1, D4", "W1, D4", "W1, D6", "W1, D6", "Tiến (TP)", "2 p-d"),
        ("T05", "Lập trình CRUD danh mục phim & upload 15 poster", "W1, D4", "W1, D5", "W1, D7", "W1, D7", "Nam (NT)", "3 p-d"),
        ("T06", "Phát triển bộ lọc và tìm kiếm phim theo thể loại", "W1, D5", "W1, D6", "W2, D1", "W2, D1", "Đạt (DN)", "2 p-d"),
        ("T07", "Module quản lý phòng chiếu & ma trận ghế Standard/VIP", "W2, D2", "W2, D2", "W2, D5", "W2, D5", "Tiến (TP)", "3 p-d"),
        ("T08", "Module lập lịch suất chiếu chống trùng giờ phòng", "W2, D3", "W2, D4", "W2, D7", "W2, D7", "Kiệt (KL)", "4 p-d"),
        ("T09", "Quản lý danh mục đồ ăn và combo F&B", "W2, D4", "W2, D4", "W3, D1", "W3, D2", "Đạt (DN)", "2 p-d"),
        ("T10", "Giao diện xem chi tiết phim và suất chiếu theo ngày", "W2, D5", "W2, D6", "W3, D2", "W3, D2", "Chiến (CL)", "2 p-d"),
        ("T11", "Sơ đồ chọn ghế trực quan (sửa lỗi không tính thừa ghế)", "W3, D2", "W3, D2", "W3, D5", "W3, D5", "Kiệt (KL)", "3 p-d"),
        ("T12", "Lập trình cơ chế khóa ghế thời gian thực 10 phút", "W3, D3", "W3, D3", "W3, D7", "W3, D7", "Chiến (CL)", "4 p-d"),
        ("T13", "Tích hợp giỏ hàng F&B và mã giảm giá Voucher", "W3, D4", "W3, D5", "W4, D1", "W4, D2", "Đạt (DN)", "3 p-d"),
        ("T14", "Tích hợp cổng thanh toán VietQR", "W3, D5", "W3, D6", "W4, D3", "W4, D3", "Kiệt (KL)", "3 p-d"),
        ("T15", "Xây dựng Background Hosted Service tự động nhả ghế 10p", "W3, D6", "W4, D1", "W4, D3", "W4, D4", "Đạt (DN)", "3 p-d"),
        ("T16", "Tự động gửi vé điện tử QR qua Gmail SMTP đăng ký", "W4, D1", "W4, D2", "W4, D4", "W4, D4", "Chiến (CL)", "3 p-d"),
        ("T17", "Ứng dụng quét mã QR soát vé qua camera di động", "W4, D2", "W4, D3", "W4, D6", "W4, D6", "Tiến (TP)", "4 p-d"),
        ("T18", "Giao diện lịch sử đặt vé Cinema Pass và đánh giá phim", "W4, D4", "W4, D4", "W4, D7", "W4, D7", "Kiệt (KL)", "2 p-d"),
        ("T19", "Lập trình Dashboard báo cáo doanh thu & tỷ lệ lấp đầy rạp", "W4, D5", "W4, D5", "W5, D2", "W5, D2", "Kiệt (KL)", "3 p-d"),
        ("T20", "Kiểm thử liên thông E2E, bảo toàn DB và đóng gói Single EXE", "W5, D1", "W5, D2", "W5, D4", "W5, D4", "Cả nhóm", "4 p-d")
    ]
    for row_idx, data in enumerate(tasks_wbs):
        row = t4.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3, 4, 5, 7] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 4: Bảng theo dõi tiến độ công việc tổng thể (Project Table / WBS)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # ==========================================
    # PHẦN 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG
    # ==========================================
    add_h1("PHẦN 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")
    
    add_h2("3.1. Kiến trúc hệ thống tổng thể")
    add_p(
        "Hệ thống tuân thủ mô hình kiến trúc phân tầng (N-Tier Architecture) hiện đại kết hợp với cơ chế xử lý bất đồng bộ:\n"
        "1. Presentation Layer (Tầng giao diện): Razor Views kết hợp Tailwind CSS v4 tông màu Trắng Kem (#FAF7F2), Phosphor Icons và JavaScript ES6 Fetch API. Hỗ trợ giao diện Responsive trên cả điện thoại di động và máy tính bảng.\n"
        "2. Business Logic Layer (Tầng nghiệp vụ): Chứa các Service và Controller chuyên trách: BookingService (xử lý đặt vé, tính tiền chính xác), QrCodeService (sinh mã QR token bảo mật), EmailService (gửi vé tự động qua Gmail SMTP), VietQrService (sinh mã thanh toán VietQR), ReportService (thống kê doanh thu rạp).\n"
        "3. Background Hosted Services: SeatHoldTimeoutWorker chạy nền chu kỳ 30 giây độc lập với các HTTP request, tự động giải phóng ghế quá hạn 10 phút về trạng thái trống.\n"
        "4. Data Access Layer: Entity Framework Core 10 ORM, kết nối trực tiếp hệ quản trị CSDL MySQL / MariaDB 10.11 (Port 3306) với collation chuẩn tiếng Việt utf8mb4_unicode_ci, xử lý tranh chấp ghế đồng thời bằng Transaction cô lập cao và hỗ trợ SQLite dự phòng."
    )

    add_h2("3.2. Phân tích và Thiết kế Biểu đồ Use Case")
    
    add_h3("3.2.1. Xác định tác nhân (Actors) và phạm vi hệ thống (System Boundary)")
    add_p(
        "Dựa trên 21 User Stories từ Product Backlog, hệ thống xác định 4 tác nhân chính tương tác với phạm vi hệ thống:\n"
        "1. Khách hàng (Customer): Tác nhân chính thực hiện các ca sử dụng tra cứu phim, xem trailer, chọn suất chiếu, chọn ghế trực quan trên sơ đồ, đặt kèm bắp nước F&B, áp mã voucher, quét VietQR thanh toán, nhận vé tự động qua Gmail, xem lịch sử giao dịch Cinema Pass và đánh giá phim.\n"
        "2. Quản trị viên (Admin / Quản lý): Tác nhân quản trị sở hữu toàn quyền cấu hình: quản lý danh mục phim kèm poster, cấu hình phòng chiếu và sơ đồ ma trận ghế, lập lịch suất chiếu chống trùng giờ, quản lý đồ ăn F&B, quản lý nhân viên và theo dõi Dashboard báo cáo doanh thu.\n"
        "3. Nhân viên rạp (Staff): Tác nhân nghiệp vụ tại cửa rạp, sử dụng điện thoại di động truy cập giao diện Camera Scanner để quét mã QR trên vé điện tử của khách hàng, xác thực tính hợp lệ chỉ dưới 2 giây và cập nhật trạng thái vé.\n"
        "4. Hệ thống nền (System / Background Worker): Tác nhân tự động thực hiện các tiến trình chạy ngầm: Khóa ghế tạm thời 10 phút (Hold Seat), quét và hủy các ghế giữ quá hạn (Timeout Worker), và tự động gửi vé điện tử kèm mã QR qua Google Gmail SMTP sau khi đơn hàng được thanh toán thành công."
    )

    add_h3("3.2.2. Bảng phân rã Use Case và ánh xạ 21 User Stories")
    add_p("Bảng 5 trình bày đối chiếu chi tiết giữa 21 User Stories trên Jira với các Use Case trong hệ thống, chỉ rõ phân hệ, tác nhân và các mối quan hệ phụ thuộc:")

    # Table 5: Ánh xạ 21 US sang Use Cases
    t5_uc = doc.add_table(rows=22, cols=5)
    t5_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_headers = ["Phân hệ", "Mã Jira", "Tên Use Case", "Tác nhân chính", "Quan hệ phụ thuộc"]
    for i, h in enumerate(t5_headers):
        add_header_cell(t5_uc.rows[0], i, h)

    uc_mapping_data = [
        ("Phân hệ 1:\nXác thực & Người dùng", "SCRUM-5", "Quản lý hồ sơ cá nhân", "Khách hàng", "<<extend>> Đổi mật khẩu"),
        ("", "SCRUM-6", "Đăng nhập Admin Panel", "Quản lý", "<<include>> Xác thực quyền Admin"),
        ("", "SCRUM-7", "Phân quyền truy cập (RBAC)", "Hệ thống", "Bảo mật Cookie Authentication"),
        ("", "SCRUM-8", "Quản lý thông tin nhân viên", "Quản lý", "Admin cấp tài khoản Staff"),
        ("Phân hệ 2:\nPhim & Suất chiếu", "SCRUM-9", "Quản lý danh mục Phim", "Quản lý", "CRUD Phim, 15 Poster, Trailer"),
        ("", "SCRUM-10", "Bộ lọc & Tìm kiếm phim", "Khách hàng", "Lọc theo từ khóa, thể loại"),
        ("", "SCRUM-11", "Thiết lập phòng chiếu & Sơ đồ ghế", "Quản lý", "Cấu hình hàng, cột, loại ghế"),
        ("", "SCRUM-12", "Quản lý lịch chiếu (Showtimes)", "Quản lý", "<<include>> Check trùng giờ phòng"),
        ("", "SCRUM-13", "Quản lý danh mục đồ ăn (F&B)", "Quản lý", "CRUD Bắp nước, Combo"),
        ("", "SCRUM-14", "Xem chi tiết phim & Lịch chiếu", "Khách hàng", "Hiển thị trailer, ngày chiếu"),
        ("Phân hệ 3:\nĐặt vé & Thanh toán", "SCRUM-15", "Chọn suất chiếu & Xem sơ đồ ghế", "Khách hàng", "Hiển thị sơ đồ ghế động trực quan"),
        ("", "SCRUM-17", "Khóa ghế tạm thời (Hold Seat 10p)", "Hệ thống", "<<include>> Chọn ghế"),
        ("", "SCRUM-16", "Mua kèm Combo F&B", "Khách hàng", "<<extend>> Thêm bắp nước vào đơn"),
        ("", "SCRUM-18", "Áp dụng mã giảm giá (Voucher)", "Khách hàng", "<<extend>> Giảm trừ trực tiếp tổng tiền"),
        ("", "SCRUM-19", "Thanh toán VietQR", "Khách hàng", "Đổi trạng thái Paid"),
        ("", "SCRUM-20", "Tự động hủy giữ ghế (Timeout)", "Hệ thống", "Background Worker chu kỳ 30s"),
        ("Phân hệ 4:\nSoát vé & Báo cáo", "SCRUM-21", "Tự động gửi vé qua Gmail SMTP", "Hệ thống", "<<include>> Lấy Gmail tài khoản"),
        ("", "SCRUM-22", "Soát vé bằng mã QR qua camera", "Nhân viên", "<<include>> Check-in vé dưới 2s"),
        ("", "SCRUM-25", "Xem lịch sử giao dịch Cinema Pass", "Khách hàng", "Hiển thị thẻ vé, xem lại mã QR"),
        ("", "SCRUM-28", "Đánh giá & bình luận phim", "Khách hàng", "Chấm 1-5 sao, viết review"),
        ("", "SCRUM-29", "Xem báo cáo & thống kê rạp", "Quản lý", "Dashboard doanh thu, occupancy")
    ]
    for row_idx, data in enumerate(uc_mapping_data):
        row = t5_uc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [1, 3] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 5: Bảng phân rã Use Case theo 4 phân hệ và ánh xạ 21 User Stories", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    add_h3("3.2.3. Biểu đồ Use Case tổng thể toàn hệ thống")
    add_p(
        "Biểu đồ Use Case tổng thể bao quát toàn bộ 4 phân hệ chức năng tương ứng với 4 nhóm tác nhân. "
        "Khách hàng đóng vai trò trung tâm trong luồng trải nghiệm người dùng từ tra cứu đến giao dịch; "
        "Quản trị viên kiểm soát toàn bộ dữ liệu cấu hình; Nhân viên vận hành thiết bị soát vé tại hiện trường; "
        "và Hệ thống ngầm tự động điều phối các quy tắc khóa ghế và gửi email vé điện tử."
    )
    add_diagram_image(doc, "6", "Biểu đồ Use Case tổng thể toàn hệ thống", "diagrams/fig6_usecase_overall.png", width_inches=6.2)

    add_h3("3.2.4. Biểu đồ Use Case Phân hệ 1: Xác thực & Quản trị người dùng")
    add_p(
        "Phân hệ 1 giải quyết bài toán định danh và phân quyền bảo mật (RBAC). "
        "Các ca sử dụng Đăng ký tài khoản, Đăng nhập, Quản lý thông tin cá nhân và Đổi mật khẩu được thiết kế đồng bộ. "
        "Ca sử dụng 'Đăng nhập hệ thống' có quan hệ <<include>> với 'Xác thực & Cấp Cookie'. "
        "Ca sử dụng 'Quản lý hồ sơ cá nhân' có quan hệ <<extend>> với 'Đổi mật khẩu'. "
        "Admin sở hữu đặc quyền truy cập ca sử dụng 'Cấp tài khoản nhân viên' để cấp phát tài khoản cho nhân viên soát vé."
    )
    add_diagram_image(doc, "7", "Biểu đồ Use Case Phân hệ 1: Xác thực và Quản trị người dùng", "diagrams/fig7_usecase_auth.png", width_inches=6.0)

    add_h3("3.2.5. Biểu đồ Use Case Phân hệ 2: Phim, Phòng chiếu & Suất chiếu")
    add_p(
        "Phân hệ 2 số hóa toàn bộ cơ sở vật chất và lịch vận hành của rạp. "
        "Admin thực hiện ca sử dụng 'Thiết lập phòng chiếu', hệ thống sẽ tự động sinh ma trận ghế (ghế Standard, VIP, Couple). "
        "Khi Admin thực hiện ca sử dụng 'Lập lịch suất chiếu', hệ thống bắt buộc <<include>> ca sử dụng 'Kiểm tra xung đột thời gian' "
        "để ngăn chặn việc xếp 2 suất chiếu trùng phòng trong cùng một khoảng thời gian (bao gồm thời lượng phim và 15 phút dọn phòng). "
        "Phía Khách hàng có thể thực hiện ca sử dụng 'Tìm kiếm & Lọc phim' và 'Xem chi tiết phim cùng lịch chiếu theo ngày'."
    )
    add_diagram_image(doc, "8", "Biểu đồ Use Case Phân hệ 2: Phim, Phòng chiếu và Suất chiếu", "diagrams/fig8_usecase_movie_showtime.png", width_inches=6.0)

    add_h3("3.2.6. Biểu đồ Use Case Phân hệ 3: Đặt vé, Giữ ghế 10p & Thanh toán")
    add_p(
        "Phân hệ 3 là trung tâm giao dịch cốt lõi của hệ thống. "
        "Khi Khách hàng thực hiện ca sử dụng 'Chọn ghế trên sơ đồ', hệ thống bắt buộc <<include>> ca sử dụng 'Khóa ghế tạm thời 10 phút' "
        "nhằm thiết lập cờ Active trên bảng BookedSeats và khởi động đồng hồ đếm ngược 10:00. Hệ thống đã khắc phục lỗi logic tính thừa ghế dummy, "
        "chỉ tính tiền đúng những ghế khách hàng trực tiếp bấm chọn. "
        "Ca sử dụng 'Thanh toán trực tuyến' có quan hệ <<extend>> với 'Mua kèm Combo F&B' và 'Áp dụng mã Voucher'. "
        "Phương thức thanh toán được liên kết chuẩn VietQR. Nếu sau 10 phút khách không thanh toán, "
        "Background Worker ngầm sẽ kích hoạt ca sử dụng 'Tự động hủy giữ ghế' để trả lại ghế trống cho rạp."
    )
    add_diagram_image(doc, "9", "Biểu đồ Use Case Phân hệ 3: Đặt vé, Giữ ghế 10p và Thanh toán", "diagrams/fig9_usecase_booking.png", width_inches=6.0)

    add_h3("3.2.7. Biểu đồ Use Case Phân hệ 4: Soát vé bằng mã QR & Báo cáo thống kê")
    add_p(
        "Phân hệ 4 kết nối khâu bán vé trực tuyến với thực tế vận hành tại cửa rạp. "
        "Sau khi thanh toán thành công, tác nhân Hệ thống ngầm kích hoạt ca sử dụng 'Tự động gửi vé qua Gmail', "
        "lấy địa chỉ Gmail từ tài khoản người dùng đăng ký mà không cần yêu cầu nhập lại trên giao diện. "
        "Tại cửa phòng chiếu, Nhân viên thực hiện ca sử dụng 'Soát vé bằng mã QR qua camera điện thoại', "
        "hệ thống kiểm tra chữ ký token bảo mật, đối chiếu đúng suất chiếu và cập nhật trạng thái vé sang CheckedIn. "
        "Khách hàng có thể thực hiện ca sử dụng 'Xem lịch sử đặt vé' (phong cách Thẻ vé Cinema Pass) và 'Đánh giá phim (Rating 1-5 sao)'. "
        "Admin truy cập ca sử dụng 'Xem Dashboard doanh thu & tỷ lệ lấp đầy rạp' để theo dõi số liệu trực quan."
    )
    add_diagram_image(doc, "10", "Biểu đồ Use Case Phân hệ 4: Soát vé bằng mã QR và Báo cáo", "diagrams/fig10_usecase_ticket_report.png", width_inches=6.0)

    add_h3("3.2.8. Các bảng đặc tả Use Case chi tiết (Use Case Specifications)")

    # Table 6: Đặc tả UC01
    add_h3("Bảng đặc tả chi tiết Use Case UC01 – Đăng nhập hệ thống")
    t6_spec = doc.add_table(rows=7, cols=2)
    t6_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    uc01_data = [
        ("Mã Use Case / Tên", "UC01 – Đăng nhập hệ thống"),
        ("Tác nhân (Actor)", "Khách hàng (Customer), Nhân viên (Staff), Quản trị viên (Admin)"),
        ("Mô tả / Kích hoạt", "Xác thực danh tính người dùng và điều hướng phân quyền khi nhấn nút 'Đăng nhập'"),
        ("Tiền / Hậu điều kiện", "Tiền điều kiện: Đã có tài khoản. Hậu điều kiện: Được cấp Cookie xác thực và chuyển hướng hợp lệ."),
        ("Luồng sự kiện chính (Basic Flow)", "1. Nhập Email và Mật khẩu -> 2. Nhấn 'Đăng nhập' -> 3. Server kiểm tra CSDL MySQL và xác thực mật khẩu băm -> 4. Cấp Cookie xác thực an toàn -> 5. Chuyển hướng: Admin về Dashboard, Staff về Soát vé QR, Customer về Trang chủ."),
        ("Luồng rẽ nhánh (Alternative)", "Sai mật khẩu hoặc email không tồn tại: Cảnh báo 'Email hoặc mật khẩu không chính xác'. Tài khoản bị khóa: Thông báo liên hệ quản trị viên."),
        ("Luồng ngoại lệ (Exception)", "Mất kết nối CSDL MySQL: Hiển thị trang thông báo lỗi thân thiện và tự động ghi log hệ thống.")
    ]
    for row_idx, (col1, col2) in enumerate(uc01_data):
        row = t6_spec.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 6: Bảng đặc tả Use Case UC01 – Đăng nhập hệ thống", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Table 7: Đặc tả UC02
    add_h3("Bảng đặc tả chi tiết Use Case UC02 – Đặt vé & Giữ ghế thời gian thực")
    t7_spec = doc.add_table(rows=7, cols=2)
    t7_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    uc02_data = [
        ("Mã Use Case / Tên", "UC02 – Đặt vé và Giữ ghế thời gian thực (Real-time Seat Hold)"),
        ("Tác nhân (Actor)", "Khách hàng (Customer), Background Worker (SeatHoldTimeoutWorker)"),
        ("Mô tả / Kích hoạt", "Chọn ghế trực quan trên sơ đồ, khóa ghế 10 phút khi nhấn 'Tiếp tục'"),
        ("Tiền / Hậu điều kiện", "Tiền điều kiện: Suất chiếu còn vé trống. Hậu điều kiện: Ghế đổi sang 'Held' trong 10 phút, đếm ngược kích hoạt."),
        ("Luồng sự kiện chính (Basic Flow)", "1. Khách xem sơ đồ ghế -> 2. Click chọn ghế (đổi màu xanh, tính đúng tiền, không thừa ghế) -> 3. Nhấn 'Tiếp tục' -> 4. Server mở Transaction trong MySQL, kiểm tra ghế trống -> 5. Tạo bản ghi BookedSeats với Status = 'Held' và ExpiresAt = Hiện tại + 10 phút -> 6. Kích hoạt đồng hồ đếm ngược 10:00 trên giao diện."),
        ("Luồng rẽ nhánh (Alternative)", "Ghế bị người khác chọn trước: Rollback Transaction, báo lỗi 'Ghế vừa có người giữ', tải lại sơ đồ ghế. Hết 10 phút chưa thanh toán: Đếm ngược về 00:00, thông báo hết hạn và tự động hủy phiên."),
        ("Luồng ngoại lệ (Exception)", "Mất kết nối mạng: Client thử lại (retry) 3 lần trước khi hiển thị cảnh báo.")
    ]
    for row_idx, (col1, col2) in enumerate(uc02_data):
        row = t7_spec.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 7: Bảng đặc tả Use Case UC02 – Đặt vé & Giữ ghế thời gian thực", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Table 8: Đặc tả UC03
    add_h3("Bảng đặc tả chi tiết Use Case UC03 – Quét mã QR soát vé")
    t8_spec = doc.add_table(rows=7, cols=2)
    t8_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    uc03_data = [
        ("Mã Use Case / Tên", "UC03 – Quét mã QR soát vé (Staff Mobile Check-in)"),
        ("Tác nhân (Actor)", "Nhân viên soát vé (Staff)"),
        ("Mô tả / Kích hoạt", "Dùng camera di động quét mã QR vé của khách để kiểm tra vào rạp"),
        ("Tiền / Hậu điều kiện", "Tiền điều kiện: Đăng nhập quyền Staff. Hậu điều kiện: Vé cập nhật trạng thái CheckedIn."),
        ("Luồng sự kiện chính (Basic Flow)", "1. Mở trang /Staff/Scanner, cho phép truy cập camera -> 2. Quét mã QR của khách -> 3. Client giải mã token -> 4. Gọi API /Staff/ValidateTicket -> 5. Server đối chiếu ID vé trong MySQL, kiểm tra đúng ngày giờ và trạng thái Issued -> 6. Đổi trạng thái sang CheckedIn, lưu nhân viên và thời gian soát -> 7. Giao diện viền xanh lá, phát tiếng bíp 'HỢP LỆ'."),
        ("Luồng rẽ nhánh (Alternative)", "Vé đã dùng trước đó: Cảnh báo viền đỏ 'VÉ ĐÃ SỬ DỤNG LÚC [hh:mm]'. Vé sai ngày hoặc chưa thanh toán: Báo lỗi 'VÉ KHÔNG HỢP LỆ'. Camera mờ: Chuyển sang gõ mã vé 6 ký tự thủ công."),
        ("Luồng ngoại lệ (Exception)", "Thiết bị không hỗ trợ camera: Tự động chuyển về giao diện nhập mã vé bằng tay.")
    ]
    for row_idx, (col1, col2) in enumerate(uc03_data):
        row = t8_spec.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 8: Bảng đặc tả Use Case UC03 – Quét mã QR soát vé", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Table 9: Đặc tả UC04
    add_h3("Bảng đặc tả chi tiết Use Case UC04 – Lập lịch suất chiếu chống trùng lặp")
    t9_spec = doc.add_table(rows=7, cols=2)
    t9_spec.alignment = WD_TABLE_ALIGNMENT.CENTER
    uc04_data = [
        ("Mã Use Case / Tên", "UC04 – Lập lịch suất chiếu chống trùng giờ (Showtime Scheduling)"),
        ("Tác nhân (Actor)", "Quản trị viên (Admin)"),
        ("Mô tả / Kích hoạt", "Tạo suất chiếu mới cho phim tại các phòng chiếu khi nhấn 'Lưu suất chiếu'"),
        ("Tiền / Hậu điều kiện", "Tiền điều kiện: Đã có phim và phòng chiếu. Hậu điều kiện: Suất chiếu được lưu với trạng thái Available."),
        ("Luồng sự kiện chính (Basic Flow)", "1. Chọn Phim, Phòng chiếu, Ngày giờ bắt đầu, Giá vé -> 2. Tự tính giờ kết thúc = Bắt đầu + Thời lượng + 15p dọn phòng -> 3. Nhấn 'Lưu suất chiếu' -> 4. Server kiểm tra xung đột thời gian trong phòng đó -> 5. Lưu vào CSDL MySQL và thông báo thành công."),
        ("Luồng rẽ nhánh (Alternative)", "Phát hiện trùng lịch: Chặn lưu, thông báo 'Phòng đang có suất chiếu khác từ [hh:mm] đến [hh:mm]. Vui lòng chọn khung giờ khác.'"),
        ("Luồng ngoại lệ (Exception)", "Thời gian bắt đầu trong quá khứ: Báo lỗi 'Thời gian chiếu phải lớn hơn thời điểm hiện tại.'")
    ]
    for row_idx, (col1, col2) in enumerate(uc04_data):
        row = t9_spec.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 9: Bảng đặc tả Use Case UC04 – Lập lịch suất chiếu chống trùng lặp", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # 3.3 Sequence Diagram
    add_h2("3.3. Biểu đồ Tuần tự (Sequence Diagram)")
    add_p("Dưới đây là 3 biểu đồ tuần tự thể hiện sự tương tác luồng dữ liệu thời gian thực giữa Khách hàng, Server, CSDL MySQL, Dịch vụ VietQR, Gmail SMTP và Thiết bị di động:")
    
    add_diagram_image(doc, "11", "Biểu đồ Sequence chức năng Đặt vé và Khóa ghế tạm thời 10 phút", "diagrams/fig11_seq_booking.png", width_inches=6.2)
    add_diagram_image(doc, "12", "Biểu đồ Sequence chức năng Thanh toán VietQR và Phát hành vé điện tử QR qua Gmail", "diagrams/fig12_seq_payment_email.png", width_inches=6.2)
    add_diagram_image(doc, "13", "Biểu đồ Sequence chức năng Nhân viên quét mã QR soát vé", "diagrams/fig13_seq_scanner.png", width_inches=6.2)

    # 3.4 Database Design & ERD
    add_h2("3.4. Thiết kế Cơ sở dữ liệu MySQL và Sơ đồ Thực thể (Database ERD)")
    add_p(
        "Hệ thống sử dụng hệ quản trị CSDL quan hệ MySQL / MariaDB 10.11 (Port 3306), bảng mã utf8mb4_unicode_ci "
        "đảm bảo lưu trữ tiếng Việt có dấu chuẩn mực, không bao giờ bị lỗi font hay ký tự lạ. "
        "Cơ sở dữ liệu bao gồm 14 bảng quan hệ được thiết kế chuẩn hóa theo dạng chuẩn 3NF (Third Normal Form):"
    )

    add_diagram_image(doc, "14", "Sơ đồ quan hệ thực thể CSDL MySQL (Database ERD - 14 bảng quan hệ)", "diagrams/fig14_database_erd.png", width_inches=6.2)
    add_diagram_image(doc, "15", "Biểu đồ Kiến trúc phân tầng ASP.NET Core MVC & MySQL", "diagrams/fig15_architecture.png", width_inches=6.2)

    # Table 10: 14 Bảng dữ liệu MySQL
    add_h3("Bảng 10: Danh mục 14 bảng dữ liệu trong CSDL MySQL (cinema_db)")
    t10_db = doc.add_table(rows=15, cols=4)
    t10_db.alignment = WD_TABLE_ALIGNMENT.CENTER
    t10_headers = ["STT", "Tên bảng dữ liệu", "Khóa chính / Khóa ngoại", "Chức năng & Ý nghĩa nghiệp vụ"]
    for i, h in enumerate(t10_headers):
        add_header_cell(t10_db.rows[0], i, h)

    db_tables_data = [
        ("1", "AspNetUsers", "PK: Id (VARCHAR)", "Lưu trữ tài khoản người dùng (Khách hàng, Nhân viên, Admin), email, sđt, hash mật khẩu"),
        ("2", "Staffs", "PK: Id | FK: UserId", "Lưu thông tin nhân viên rạp, mã nhân viên (StaffCode), vị trí công tác và chi nhánh"),
        ("3", "Genres", "PK: Id (INT)", "Danh mục thể loại điện ảnh (Hành động, Kinh dị, Hoạt hình, Tình cảm, Viễn tưởng...)"),
        ("4", "Movies", "PK: Id | FK: GenreId", "Danh mục phim, thời lượng, ngày phát hành, đường dẫn trailer YouTube và poster cục bộ"),
        ("5", "ScreeningRooms", "PK: Id (INT)", "Thông số phòng chiếu: tên phòng, số hàng, số cột, tổng số ghế và công nghệ chiếu (IMAX, 2D)"),
        ("6", "Seats", "PK: Id | FK: RoomId", "Ma trận ghế thực tế trong phòng: hàng (A-J), số ghế (1-16), loại ghế (Standard, VIP, Couple)"),
        ("7", "Showtimes", "PK: Id | FK: MovieId, RoomId", "Lịch suất chiếu: phim, phòng, thời gian bắt đầu, kết thúc (tự cộng 15p dọn phòng), giá cơ bản"),
        ("8", "BookedSeats", "PK: Id | FK: ShowtimeId, SeatId, BookingId", "Trạng thái ghế theo suất: Available, Held (giữ 10p), Booked (đã bán), Expired (hết hạn)"),
        ("9", "Bookings", "PK: Id | FK: UserId, ShowtimeId", "Đơn đặt vé: mã đơn (BookingCode), tổng tiền, giảm giá voucher, thành tiền, trạng thái Paid"),
        ("10", "Tickets", "PK: Id | FK: BookingId, BookedSeatId", "Vé điện tử: mã vé 6 ký tự, chuỗi token QR bảo mật, trạng thái Issued/CheckedIn, ngày soát vé"),
        ("11", "FoodItems", "PK: Id (INT)", "Danh mục đồ ăn thức uống: Bắp rang bơ, Nước ngọt, Combo Family, Combo Couple, giá bán"),
        ("12", "BookingFoodItems", "PK: Id | FK: BookingId, FoodItemId", "Chi tiết combo F&B đi kèm trong từng đơn đặt vé của khách hàng"),
        ("13", "Vouchers", "PK: Id (INT)", "Mã giảm giá khuyến mãi (CINEMA10, DISCOUNT20), tỷ lệ giảm %, số tiền giảm tối đa, hạn dùng"),
        ("14", "Reviews", "PK: Id | FK: UserId, MovieId", "Đánh giá và bình luận phim của khách hàng sau khi xem (điểm rating từ 1 đến 5 sao)")
    ]
    for row_idx, data in enumerate(db_tables_data):
        row = t10_db.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg)

    add_p("\nBảng 10: Bảng danh mục 14 bảng dữ liệu trong CSDL MySQL (cinema_db)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # ==========================================
    # PHẦN 4: KẾT QUẢ TRIỂN KHAI VÀ GIAO DIỆN SẢN PHẨM
    # ==========================================
    add_h1("PHẦN 4: KẾT QUẢ TRIỂN KHAI VÀ GIAO DIỆN SẢN PHẨM")
    
    add_h2("4.1. Quy trình phát triển qua các giai đoạn và các bản sửa lỗi hoàn thiện")
    add_p("Dự án được triển khai qua 4 giai đoạn chuẩn mực và đã trải qua các đợt hoàn thiện, sửa lỗi kỹ thuật chuyên sâu:")
    add_p("1. Thiết kế giao diện (UI/UX) tông màu Trắng Kem (#FAF7F2): Thay đổi toàn bộ giao diện từ Dark Theme sang bảng màu Trắng Kem (#FAF7F2) phong cách điện ảnh cao cấp, thân thiện với mắt người dùng. Typography chuẩn Segoe UI/Inter loại bỏ hoàn toàn lỗi font tiếng Việt có dấu.")
    add_p("2. Chuyển đổi và bảo toàn CSDL MySQL chuẩn mực: Hệ thống chuyển từ lưu trữ tệp sang máy chủ CSDL MySQL / MariaDB 10.11 port 3306. Toàn bộ 15 bộ phim, 84 suất chiếu, các tài khoản và lịch sử giao dịch được bảo toàn 100% qua mọi lần khởi động ứng dụng.")
    add_p("3. Tối ưu thuật toán chọn ghế và giỏ hàng: Khắc phục triệt để lỗi logic tính thừa 1 ghế dummy khi chọn vị trí trên sơ đồ. Hệ thống chỉ ghi nhận và tính tiền chính xác các ghế khách hàng lựa chọn.")
    add_p("4. Tích hợp thanh toán VietQR: Tích hợp mã chuẩn VietQR chuẩn Napas 247, đồng bộ số tiền chính xác sau khi áp dụng mã voucher.")
    add_p("5. Tự động hóa phát hành vé qua Gmail SMTP: Hệ thống tự động trích xuất Gmail đã đăng ký của khách hàng (User.Identity.Name / ApplicationUser.Email) và gửi vé điện tử (HTML Card kèm ảnh mã QR đính kèm) mà không cần yêu cầu người dùng nhập lại email trên màn hình Checkout.")
    add_p("6. Chuẩn hóa trang Lịch sử đặt vé (MyBookings): Thiết kế lại theo phong cách Thẻ vé xem phim (Cinema Pass Ticket Card) hiện đại với mã QR, trạng thái vé, thông tin phòng chiếu và combo F&B.")
    add_p("7. Bộ poster phim nội bộ hoàn chỉnh: 15 bộ phim đều có poster độ nét cao lưu trữ cục bộ tại /uploads/posters/poster_{1..15}.jpg, hoạt động độc lập không phụ thuộc internet ngoài.")

    add_h2("4.2. Giao diện thực tế của hệ thống (HCI)")
    add_p("Dưới đây là hình ảnh chụp màn hình giao diện thực tế từ hệ thống đang vận hành hoàn chỉnh, minh chứng trực quan các tính năng đã hiện thực hóa thành công trên môi trường ASP.NET Core MVC:")

    add_diagram_image(doc, "16", "Giao diện Đăng ký tài khoản khách hàng", "screenshots/fig16_signup.png", width_inches=6.2)
    add_diagram_image(doc, "17", "Giao diện Đăng nhập hệ thống đa vai trò", "screenshots/fig17_login.png", width_inches=6.2)
    add_diagram_image(doc, "18", "Giao diện Hồ sơ cá nhân người dùng", "screenshots/fig18_profile.png", width_inches=6.2)
    add_diagram_image(doc, "19", "Giao diện Trang chủ và Bộ lọc danh mục phim (Tông màu Trắng Kem #FAF7F2)", "screenshots/fig19_home.png", width_inches=6.2)
    add_diagram_image(doc, "20", "Giao diện Chi tiết phim và Danh sách suất chiếu theo ngày", "screenshots/fig20_detail.png", width_inches=6.2)
    add_diagram_image(doc, "21", "Giao diện Chọn ghế trực quan với đồng hồ đếm ngược 10 phút", "screenshots/fig21_seat.png", width_inches=6.2)
    add_diagram_image(doc, "22", "Giao diện Chọn Combo bắp nước F&B", "screenshots/fig22_fnb.png", width_inches=6.2)
    add_diagram_image(doc, "23", "Giao diện Thanh toán VietQR và Áp dụng mã Voucher", "screenshots/fig23_checkout.png", width_inches=6.2)
    add_diagram_image(doc, "24", "Giao diện Xác nhận đơn hàng và hiển thị vé điện tử QR", "screenshots/fig24_confirm.png", width_inches=6.2)
    add_diagram_image(doc, "25", "Giao diện Xem lịch sử đặt vé phong cách Thẻ vé xem phim (Cinema Pass)", "screenshots/fig25_pass.png", width_inches=6.2)
    add_image_placeholder(doc, "26", "Giao diện Đánh giá và bình luận phim")
    add_image_placeholder(doc, "27", "Giao diện Quản lý nhân viên (Admin)")
    add_diagram_image(doc, "28", "Giao diện Quản lý danh mục phim kèm poster điện ảnh (Admin)", "screenshots/fig28_movies_admin.png", width_inches=6.2)
    add_diagram_image(doc, "29", "Giao diện Cấu hình phòng chiếu và sơ đồ ma trận ghế (Admin)", "screenshots/fig29_rooms_admin.png", width_inches=6.2)
    add_diagram_image(doc, "30", "Giao diện Lập lịch suất chiếu chống trùng giờ (Admin)", "screenshots/fig30_showtimes_admin.png", width_inches=6.2)
    add_diagram_image(doc, "31", "Giao diện Quản lý danh mục F&B và Voucher (Admin)", "screenshots/fig31_fnb_admin.png", width_inches=6.0)
    add_diagram_image(doc, "32", "Giao diện Nhân viên quét mã QR soát vé qua camera điện thoại", "screenshots/fig32_scanner_staff.png", width_inches=6.0)
    add_diagram_image(doc, "33", "Giao diện Dashboard Thống kê doanh thu và tỷ lệ lấp đầy rạp", "screenshots/fig33_dashboard_admin.png", width_inches=6.2)

    add_h2("4.3. Kết quả kiểm thử hệ thống (Testing Results)")
    add_p("Bảng 11 tổng hợp kết quả thực thi các Test Cases trọng yếu sau khi hoàn thiện toàn bộ bản sửa lỗi:")

    # Table 11: Testing
    t11_test = doc.add_table(rows=9, cols=6)
    t11_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    t11_headers = ["Mã TC", "Tên kịch bản kiểm thử", "Thao tác / Dữ liệu đầu vào", "Kết quả kỳ vọng", "Kết quả thực tế", "Đánh giá"]
    for i, h in enumerate(t11_headers):
        add_header_cell(t11_test.rows[0], i, h)

    test_data = [
        ("TC-01", "Đăng ký email trùng lặp", "Nhập email đã tồn tại", "Báo lỗi email đã được đăng ký", "Hiển thị thông báo đỏ chính xác", "PASS"),
        ("TC-02", "Tạo suất chiếu trùng giờ", "Chọn phòng 1, khung giờ đã có phim khác", "Chặn thao tác, cảnh báo xung đột phòng và giờ", "Chặn thành công, báo chi tiết suất trùng", "PASS"),
        ("TC-03", "Tranh chấp ghế đồng thời (Concurrency)", "2 trình duyệt cùng bấm giữ ghế A05 tại 1 giây", "Trình duyệt 1 giữ được, trình duyệt 2 báo lỗi ghế đã có người giữ", "Trình duyệt 1 giữ thành công, trình duyệt 2 báo lỗi", "PASS"),
        ("TC-04", "Tính toán giá trị giỏ hàng", "Chọn 2 ghế VIP (200.000đ) + 1 Combo (85.000đ)", "Tính đúng 285.000đ, không tính thừa ghế dummy", "Tính toán chính xác 100%", "PASS"),
        ("TC-05", "Worker nhả ghế quá hạn 10p", "Giữ ghế B01, chờ hết 10 phút không mua", "Worker tự động chuyển sang Expired, ghế về trống", "Ghế tự động trả về màu trống sau 10p", "PASS"),
        ("TC-06", "Áp mã Voucher & Thanh toán VietQR", "Nhập CINEMA10 cho đơn 200.000đ, quét mã VietQR", "Giảm đúng 10%, mã VietQR hiện đúng 180.000đ", "Mã VietQR hiển thị chính xác số tiền", "PASS"),
        ("TC-07", "Tự động gửi vé qua Gmail SMTP", "Thanh toán thành công đơn hàng", "Hệ thống tự gửi vé và QR về Gmail đăng ký của user", "Gmail nhận được vé HTML trong 3 giây", "PASS"),
        ("TC-08", "Quét mã QR vé tại cửa", "Đưa mã QR vé đã thanh toán vào camera", "Phát tiếng bíp, viền xanh 'HỢP LỆ', đổi sang CheckedIn", "Nhận diện trong 1.2s, ghi nhận soát vé", "PASS")
    ]
    for row_idx, data in enumerate(test_data):
        row = t11_test.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 5] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "DCFCE7" if col_idx == 5 else ("F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            bold = True if col_idx == 5 else False
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, bold=bold)

    add_p("\nBảng 11: Bảng tổng hợp Test Cases và kết quả kiểm thử hệ thống", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    add_h2("4.4. Đóng gói và phát hành sản phẩm (Self-contained Package)")
    add_p(
        "Ứng dụng đã được biên dịch thành công dưới dạng Portable Self-contained Single-file EXE và đóng gói đầy đủ:\n"
        "- Tệp thực thi CineManagement.exe (~60 MB) tích hợp sẵn toàn bộ .NET 10 Runtime, không yêu cầu máy cài đặt .NET SDK trước.\n"
        "- Kịch bản khởi động START-Cinema.bat tự động chạy ứng dụng tại http://localhost:5050 và mở trình duyệt mặc định.\n"
        "- Kịch bản START-MySQL.bat và dịch vụ máy chủ MariaDB 10.11 tích hợp sẵn trong thư mục mariadb-10.11.8-winx64, port 3306.\n"
        "- Cơ sở dữ liệu MySQL cinema_db lưu trữ dữ liệu demo hoàn chỉnh (15 phim, 15 poster cục bộ, 84 suất chiếu, 9 tài khoản, các đơn hàng và vé đã soát), đảm bảo lưu trữ vĩnh viễn không bị mất dữ liệu.\n"
        "- Gói nén phân phối CinemaManagement-Demo.zip (~80.3 MB) sẵn sàng gửi cho giảng viên và hội đồng chấm điểm."
    )

    # ==========================================
    # PHẦN 5: ĐÁNH GIÁ VÀ QUẢN LÝ RỦI RO (RISK MANAGEMENT)
    # ==========================================
    add_h1("PHẦN 5: ĐÁNH GIÁ VÀ QUẢN LÝ RỦI RO (RISK MANAGEMENT)")
    add_h2("5.1. Tầm quan trọng của quản lý rủi ro")
    add_p(
        "Quản lý rủi ro giúp nhóm dự báo trước các vấn đề kỹ thuật và tiến độ, thiết lập giải pháp phòng ngừa (Mitigation Approaches) "
        "và chuẩn bị kịch bản xử lý sự cố (Contingency Plans) để đảm bảo chất lượng và tiến độ dự án."
    )

    add_h2("5.2. Các bảng thông tin rủi ro chi tiết (Risk Information Sheets)")
    
    # Risk 1
    t12_r1 = doc.add_table(rows=8, cols=2)
    t12_r1.alignment = WD_TABLE_ALIGNMENT.CENTER
    r01_data = [
        ("Risk ID: R01", "Priority Level: Critical | Report Date: 20/08/2026"),
        ("Description", "Nguy cơ xung đột giữ ghế đồng thời (Race Condition) khi nhiều khách cùng chọn 1 ghế trong khung giờ cao điểm."),
        ("Probability / Impact", "Probability: 15% | Impact: Critical (Nguy cơ bán trùng ghế, phát sinh khiếu nại)"),
        ("First Indicator", "Log server ghi nhận nhiều ngoại lệ DbUpdateException vi phạm ràng buộc Unique Key trên bảng BookedSeats."),
        ("Mitigation Approaches", "1. Cấu hình Database Transaction ở mức cô lập cao (Serializable/Repeatable Read) trong MySQL.\n2. Kiểm tra trạng thái ghế trước khi INSERT bản ghi Held."),
        ("Date / Owner", "Bắt đầu: 22/08/2026 | Hoàn thành: 28/08/2026 | Owner: Luyện Đức Chiến (CL)"),
        ("Contingency Plan", "Tự động rollback giao dịch của người đến sau, thông báo 'Ghế vừa có người chọn' và tải lại sơ đồ ghế mới nhất."),
        ("Current Status", "Đã cấu hình hoàn tất Transaction và kiểm thử tải đa luồng thành công.")
    ]
    for row_idx, (col1, col2) in enumerate(r01_data):
        row = t12_r1.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 12: Bảng thông tin rủi ro R01 – Xung đột giữ ghế đồng thời (Race Condition)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Risk 2
    t13_r2 = doc.add_table(rows=8, cols=2)
    t13_r2.alignment = WD_TABLE_ALIGNMENT.CENTER
    r02_data = [
        ("Risk ID: R02", "Priority Level: High | Report Date: 25/08/2026"),
        ("Description", "Treo tiến trình Background Worker: Dịch vụ chạy ngầm nhả ghế quá 10 phút gặp lỗi chưa bắt, làm ghế bị khóa vĩnh viễn."),
        ("Probability / Impact", "Probability: 10% | Impact: High (Ghế bị chiếm giữ ảo, rạp bị thất thoát doanh thu)"),
        ("First Indicator", "Nhiều ghế hiển thị 'Đang giữ' trên sơ đồ mặc dù đã quá 30 phút."),
        ("Mitigation Approaches", "1. Bọc toàn bộ logic trong khối try-catch lồng nhau và cơ chế tự khởi động lại.\n2. Bổ sung nút bấm dọn dẹp thủ công ('Giải phóng ghế quá hạn') trên trang Admin Dashboard."),
        ("Date / Owner", "Bắt đầu: 28/08/2026 | Hoàn thành: 05/09/2026 | Owner: Nguyễn Tiến Đạt (DN)"),
        ("Contingency Plan", "Quản trị viên ấn nút 'Giải phóng ghế quá hạn' trên Admin Dashboard để lập tức cưỡng chế nhả ghế."),
        ("Current Status", "Đã triển khai Worker chu kỳ 30s kèm cơ chế tự phục hồi và nút dọn dẹp thủ công.")
    ]
    for row_idx, (col1, col2) in enumerate(r02_data):
        row = t13_r2.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 13: Bảng thông tin rủi ro R02 – Treo tiến trình Background Service giải phóng ghế", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Risk 3
    t14_r3 = doc.add_table(rows=8, cols=2)
    t14_r3.alignment = WD_TABLE_ALIGNMENT.CENTER
    r03_data = [
        ("Risk ID: R03", "Priority Level: Medium | Report Date: 02/09/2026"),
        ("Description", "Gián đoạn kết nối gửi Email SMTP: Mạng hoặc Google SMTP bị nghẽn làm chậm phản hồi trang xác nhận đặt vé."),
        ("Probability / Impact", "Probability: 8% | Impact: Medium (Khách phải chờ đợi lâu ở màn hình hoàn tất đơn)"),
        ("First Indicator", "Thời gian phản hồi CheckoutController vượt quá 5 giây."),
        ("Mitigation Approaches", "1. Gửi Email bất đồng bộ trong background thread hoặc Task.Run.\n2. Lưu trạng thái đơn sang Paid trước, sau đó gửi mail dự phòng.\n3. Cho phép khách hàng xem lại vé và ấn nút gửi lại vé trong trang MyBookings."),
        ("Date / Owner", "Bắt đầu: 05/09/2026 | Hoàn thành: 12/09/2026 | Owner: Lâm Tuấn Kiệt (KL)"),
        ("Contingency Plan", "Khách hàng luôn có thể mở trang /Booking/MyBookings hoặc trang Confirmation để xem trực tiếp mã QR."),
        ("Current Status", "Đã hoàn thiện gửi mail bất đồng bộ qua Google SMTP kèm nút gửi lại vé 1-click.")
    ]
    for row_idx, (col1, col2) in enumerate(r03_data):
        row = t14_r3.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 14: Bảng thông tin rủi ro R03 – Gián đoạn kết nối dịch vụ gửi Email SMTP", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # Risk 4
    t15_r4 = doc.add_table(rows=8, cols=2)
    t15_r4.alignment = WD_TABLE_ALIGNMENT.CENTER
    r04_data = [
        ("Risk ID: R04", "Priority Level: Medium | Report Date: 10/09/2026"),
        ("Description", "Sự cố camera và vé giả khi soát vé: Camera điện thoại bị mờ hoặc ánh sáng rạp tối không đọc được mã QR."),
        ("Probability / Impact", "Probability: 12% | Impact: Medium (Ùn tắc cửa vào rạp trong giờ cao điểm)"),
        ("First Indicator", "Hàng dài khách chờ soát vé, camera quét liên tục không nhận diện được mã."),
        ("Mitigation Approaches", "1. Tích hợp nút bật đèn Flash trên giao diện quét camera.\n2. Mã hóa dữ liệu QR bằng chuỗi token bảo mật chống làm giả.\n3. Bổ sung ô nhập mã vé 6 ký tự thủ công ngay bên dưới camera."),
        ("Date / Owner", "Bắt đầu: 15/09/2026 | Hoàn thành: 22/09/2026 | Owner: Nguyễn Phúc Tiến (TP)"),
        ("Contingency Plan", "Nhân viên chuyển sang gõ mã vé 6 ký tự hoặc tra cứu theo số điện thoại khách để check-in tức thì."),
        ("Current Status", "Đã tích hợp đầy đủ cả 2 chế độ: Quét camera tự động và Nhập mã vé thủ công.")
    ]
    for row_idx, (col1, col2) in enumerate(r04_data):
        row = t15_r4.rows[row_idx]
        add_body_cell(row, 0, col1, bold=True, bg_hex="F1F5F9", width_cm=4.5)
        add_body_cell(row, 1, col2, width_cm=11.0)
    add_p("Bảng 15: Bảng thông tin rủi ro R04 – Sự cố camera và vé giả mạo khi soát vé", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, italic=True, size=10.5)

    # ==========================================
    # PHẦN 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # ==========================================
    add_h1("PHẦN 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    
    add_h2("6.1. Tự đánh giá mức độ hoàn thành")
    add_p("• Ưu điểm:")
    add_p("- Hoàn thành 100% khối lượng công việc (21/21 User Stories) đúng tiến độ.")
    add_p("- Hệ quản trị CSDL MySQL / MariaDB 10.11 hoạt động ổn định, bảng mã utf8mb4_unicode_ci hiển thị tiếng Việt hoàn hảo, bảo toàn toàn bộ dữ liệu.")
    add_p("- Tích hợp thanh toán chuẩn VietQR và tự động gửi vé qua Gmail SMTP tiện lợi.")
    add_p("- Giao diện tông màu Trắng Kem (#FAF7F2) thẩm mỹ, lịch sử vé Cinema Pass hiện đại, khắc phục triệt để lỗi tính thừa ghế.")
    add_p("- Ứng dụng quét camera di động soát vé đạt tốc độ dưới 2 giây.")
    add_p("- Đóng gói thành công file EXE độc lập kèm bản demo zip 80.3 MB sẵn sàng sử dụng.")
    add_p("• Hạn chế:")
    add_p("- Cổng thanh toán VietQR hiện tại xử lý xác nhận thanh toán trực tiếp, chưa tích hợp webhook biến động số dư ngân hàng tự động 24/7.")
    add_p("- Chưa hỗ trợ đa ngôn ngữ (chủ yếu là Tiếng Việt).")

    add_h2("6.2. So sánh giải pháp với thị trường thực tế")
    add_p("So với các hệ thống lớn như CGV, Beta Cinemas, Lotte:")
    add_p("- Điểm tương đồng: Đầy đủ các bước từ tra cứu phim, chọn suất, sơ đồ ghế, combo F&B, voucher, VietQR đến vé điện tử QR.")
    add_p("- Ưu thế nổi bật của đề tài: Không bắt buộc khách hàng cài App cồng kềnh; nhân viên dùng ngay điện thoại cá nhân để soát vé mà không cần đầu tư máy quét chuyên dụng đắt tiền; toàn bộ hệ thống đóng gói chạy gọn trong 1 file EXE duy nhất, tối ưu chi phí cho các cụm rạp vừa và nhỏ.")

    add_h2("6.3. Bài học kinh nghiệm trong quản lý dự án")
    add_p("1. Khung làm việc Scrum giúp nhóm kiểm soát rủi ro kiến trúc sớm ngay từ Sprint 1 và liên tục bàn giao sản phẩm chạy được sau mỗi tuần.")
    add_p("2. Tầm quan trọng của Planning Poker: Giúp nhóm nhận diện đúng độ phức tạp của bài toán đồng bộ thời gian thực để tăng Story Point lên 8 SP và bố trí 2 lập trình viên phối hợp (Pair Programming).")
    add_p("3. Quản lý Git nghiêm ngặt qua Pull Request giúp triệt tiêu 95% nguy cơ xung đột mã nguồn.")

    add_h2("6.4. Hướng phát triển trong tương lai")
    add_p("- Tích hợp webhook tự động nhận diện biến động số dư ngân hàng qua VietQR.")
    add_p("- Ứng dụng trí tuệ nhân tạo (AI Recommendation) gợi ý phim dựa trên lịch sử xem phim của khách hàng.")
    add_p("- Mở rộng chương trình thành viên tích điểm (Loyalty Points) và phát triển ứng dụng di động Flutter/MAUI.")

    # ==========================================
    # PHẦN 7: BIÊN BẢN CÁC CUỘC HỌP SCRUM (SCRUM MEETING NOTES)
    # ==========================================
    add_h1("PHẦN 7: BIÊN BẢN CÁC CUỘC HỌP SCRUM (SCRUM MEETING NOTES)")
    
    add_h2("7.1. Biên bản họp Lập kế hoạch Sprint 1 (Sprint 1 Planning Meeting)")
    add_p("• Thời gian: 08:30 – 10:30, Ngày 18/08/2026. Địa điểm: Phòng máy thực hành CNTT – Tòa H1, Trường ĐH Xây dựng Hà Nội.")
    add_p("• Thành phần tham dự: Đầy đủ 5 thành viên nhóm. Chủ trì: Lâm Tuấn Kiệt (PO) & Luyện Đức Chiến (SM).")
    add_p("• Nội dung: PO trình bày mục tiêu Sprint 1; thảo luận 6 User Stories (US-01 đến US-06); chấm điểm Planning Poker thống nhất 21 SP. Phân công: Chiến làm Auth/Account; Tiến thiết kế CSDL MySQL & RBAC; Nam làm Figma giao diện Trắng Kem & CRUD Phim; Đạt làm bộ lọc tìm kiếm; Kiệt làm quản lý nhân viên.")
    add_p("• Cam kết Definition of Done (DoD): Code biên dịch 0 lỗi, API trả về chuẩn HTTP status code, giao diện Responsive, dữ liệu lưu trữ MySQL ổn định.")

    add_h2("7.2. Biên bản họp Scrum hàng ngày tiêu biểu (Daily Scrum Meeting Sample)")
    add_p("• Thời gian: 08:45 – 09:00, Ngày 12/09/2026 (Sprint 3). Hình thức: Họp Google Meet 15 phút.")
    add_p("• Báo cáo của các thành viên:")
    add_p("- Luyện Đức Chiến (CL): Hôm qua hoàn thành API HoldSeats() 10 phút. Hôm nay phối hợp với Đạt kiểm thử Worker nhả ghế. Khó khăn: Xử lý đồng thời giữa nhiều luồng ghi.")
    add_p("- Nguyễn Phúc Tiến (TP): Hôm qua xong hiển thị Combo F&B. Hôm nay cấu hình Transaction trong MySQL để giải quyết triệt để lỗi tranh chấp ghế. Khó khăn: Không.")
    add_p("- Lâm Tuấn Kiệt (KL): Hôm qua ghép nối màn hình thanh toán VietQR. Hôm nay viết logic trừ voucher và cập nhật trạng thái Paid. Cần Đạt chốt cấu trúc Voucher.")
    add_p("- Nguyễn Tiến Đạt (DN): Hôm qua viết xong SeatHoldTimeoutWorker. Hôm nay bàn giao cấu trúc Voucher cho Kiệt và kiểm thử đơn quá hạn 10 phút. Khó khăn: Không.")
    add_p("- Trần Phương Nam (NT): Hôm qua sửa lỗi không tính thừa ghế và hoàn thiện giao diện Trắng Kem. Hôm nay kiểm thử thanh toán VietQR và đếm ngược 10 phút. Cần Chiến cập nhật thông báo khi hết 10 phút.")

    add_h2("7.3. Biên bản họp Sơ kết Sprint 3 (Sprint 3 Review Meeting)")
    add_p("• Thời gian: 16:00 – 17:30, Ngày 18/09/2026. Địa điểm: Thư viện ĐH Xây dựng Hà Nội.")
    add_p("• Nội dung: Nhóm demo trọn vẹn luồng chọn ghế trực quan -> đếm ngược 10:00 -> chọn combo bắp nước -> áp mã CINEMA10 -> quét mã VietQR -> thanh toán thành công. Demo kịch bản 2 người tranh chấp cùng 1 ghế: Hệ thống chặn người thứ hai chính xác. Demo kịch bản hết 10 phút: Worker tự động nhả ghế thành công. PO nghiệm thu xác nhận 6/6 User Stories đạt chuẩn DoD.")

    add_h2("7.4. Biên bản họp Cải tiến Sprint 3 (Sprint 3 Retrospective Meeting)")
    add_p("• Thời gian: 17:30 – 18:30, Ngày 18/09/2026.")
    add_p("• Đánh giá:")
    add_p("- What went well: CSDL MySQL chạy rất mượt; cơ chế khóa ghế Transaction hoạt động chính xác; tích hợp mã VietQR hiển thị rõ nét; hoàn thành khối lượng SP lớn nhất (29 SP).")
    add_p("- What could be improved: Quy trình gửi vé điện tử cần được tự động hóa hoàn toàn để khách hàng không phải tự gõ email ở bước Checkout.")
    add_p("- Action Items cho Sprint 4: Lấy tự động Gmail từ tài khoản đăng ký để gửi vé qua SMTP; thiết kế giao diện Mobile-first ngay từ đầu cho màn hình quét QR của nhân viên; chuẩn hóa trang MyBookings theo phong cách Cinema Pass.")

    # ==========================================
    # TÀI LIỆU THAM KHẢO
    # ==========================================
    add_h1("TÀI LIỆU THAM KHẢO")
    add_p("1. TS. Trần Khánh Dung, Bài giảng Quản lý dự án Công nghệ Thông tin, Khoa CNTT, Trường Đại học Xây dựng Hà Nội.")
    add_p("2. Ken Schwaber & Jeff Sutherland, The Scrum Guide – Hướng dẫn chuẩn về Scrum: Luật chơi, Scrum.org, Phiên bản cập nhật.")
    add_p("3. Roger S. Pressman, Ph.D., Software Engineering: A Practitioner’s Approach, 8th Edition, McGraw-Hill Education, 2015.")
    add_p("4. Microsoft Corporation, ASP.NET Core MVC & Entity Framework Core Documentation, Microsoft Learn, URL: https://learn.microsoft.com/aspnet/core, 2026.")
    add_p("5. MariaDB & MySQL Foundation, MariaDB Server 10.11 & MySQL 8.0 Reference Manual, URL: https://mariadb.com/kb/en/documentation/, 2026.")
    add_p("6. Atlassian, Agile Project Management with Jira Software Documentation, URL: https://support.atlassian.com/jira-software-cloud/, 2026.")
    add_p("7. QRCoder Project, QRCoder: An open-source pure C# QRCode implementation, GitHub Repository, URL: https://github.com/codebude/QRCoder.")

    # Save document
    out_file = "Bao_Cao_QLDACNTT_Cinema_Management.docx"
    doc.save(out_file)
    print(f"SUCCESS: Report updated & saved as '{out_file}' (Size: {os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    create_report()
