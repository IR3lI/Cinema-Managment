# -*- coding: utf-8 -*-
"""
Script tạo Báo cáo Tổng quan Dự án CineManagement hoàn chỉnh (Word .docx)
Đáp ứng toàn diện các mục yêu cầu:
1. Nội dung (tên dự án, bối cảnh, người dùng chính, công nghệ sử dụng)
2. Lý do chọn dự án (3 luận điểm chuyên sâu)
3. Mục đích và mục tiêu (Product Goal & SMART Goals)
4. Danh sách 21 User Stories chuẩn hóa (Đúng 4 cột: ID, As a..., I want..., So that...)
5. Yêu cầu và phạm vi dự án (yêu cầu chức năng 5 module, phi chức năng, nguyên tắc thiết kế)
6. Biểu đồ phân rã chức năng (BFD) - Nhúng hình ảnh tối giản sắc nét
7. Thiết kế CSDL & Sơ đồ ERD (14 bảng) - Nhúng hình ảnh và bảng đặc tả
8. Quy trình hoạt động tổng thể (End-to-End Workflow 9 bước)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_overview_report():
    doc = docx.Document()

    # Cấu hình lề trang A4 chuẩn học thuật (2.0 - 2.0 - 3.0 - 2.0 cm)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)

    # Helper format tables
    def set_cell_border(cell, **kwargs):
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>\n'
                              f'<w:top w:val="{kwargs.get("top", "single")}" w:sz="{kwargs.get("sz", "4")}" w:space="0" w:color="{kwargs.get("color", "CBD5E1")}"/>\n'
                              f'<w:left w:val="{kwargs.get("left", "single")}" w:sz="{kwargs.get("sz", "4")}" w:space="0" w:color="{kwargs.get("color", "CBD5E1")}"/>\n'
                              f'<w:bottom w:val="{kwargs.get("bottom", "single")}" w:sz="{kwargs.get("sz", "4")}" w:space="0" w:color="{kwargs.get("color", "CBD5E1")}"/>\n'
                              f'<w:right w:val="{kwargs.get("right", "single")}" w:sz="{kwargs.get("sz", "4")}" w:space="0" w:color="{kwargs.get("color", "CBD5E1")}"/>\n'
                              f'</w:tcBorders>')
        tcPr.append(tcBorders)

    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def make_row_header(row):
        trPr = row._tr.get_or_add_trPr()
        tblHeader = parse_xml(f'<w:tblHeader {nsdecls("w")}/>')
        trPr.append(tblHeader)

    def make_row_cant_split(row):
        trPr = row._tr.get_or_add_trPr()
        cantSplit = parse_xml(f'<w:cantSplit {nsdecls("w")}/>')
        trPr.append(cantSplit)

    def add_header_cell(row, col_idx, text, width_cm=None):
        cell = row.cells[col_idx]
        if width_cm:
            cell.width = Cm(width_cm)
        set_cell_background(cell, "1E293B") # Dark Slate 800
        set_cell_border(cell, color="1E293B", sz="8")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(5)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    def add_body_cell(row, col_idx, text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, bg_hex="FFFFFF", font_size=9.5, width_cm=None):
        cell = row.cells[col_idx]
        if width_cm:
            cell.width = Cm(width_cm)
        if bg_hex != "FFFFFF":
            set_cell_background(cell, bg_hex)
        set_cell_border(cell, color="E2E8F0", sz="4")
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(15, 23, 42)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, color=(15, 23, 42), space_before=0, space_after=6, line_spacing=1.3):
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
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138) # Deep Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(185, 28, 28) # Dark Red
        return p

    def add_diagram_image(fig_num, caption, img_path, width_inches=6.0):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(f"Hình {fig_num}: {caption}")
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10)
            r_cap.font.bold = True
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(71, 85, 105)

    # ==========================================
    # TRANG BÌA (COVER PAGE)
    # ==========================================
    add_p("TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(15, 23, 42), space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(30, 58, 138), space_after=14)

    logo_path = os.path.join("extracted_media", "image1.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(14)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.6))

    add_p("BÁO CÁO TỔNG QUAN DỰ ÁN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, color=(185, 28, 28), space_after=4)
    add_p("HỌC PHẦN: QUẢN LÝ DỰ ÁN CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(30, 58, 138), space_after=14)

    add_p("ĐỀ TÀI:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, color=(100, 116, 139), space_after=2)
    add_p("XÂY DỰNG HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM TRỰC TUYẾN\n(CINEMA MANAGEMENT SYSTEM - CINEMANAGEMENT)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14.5, color=(15, 23, 42), space_after=20)

    info_data = [
        ("Giảng viên hướng dẫn:", "TS. Trần Khánh Dung"),
        ("Lớp học phần:", "66PMx - Quản lý dự án CNTT"),
        ("Nhóm sinh viên thực hiện:", "Nhóm 01 (CineManagement Team)"),
        ("1. Lâm Tuấn Kiệt (Nhóm trưởng):", "Product Owner / Fullstack Dev – Ký hiệu: KL"),
        ("2. Luyện Đức Chiến:", "Scrum Master / Backend Dev – Ký hiệu: CL"),
        ("3. Nguyễn Phúc Tiến:", "Backend / Database Architect – Ký hiệu: TP"),
        ("4. Nguyễn Tiến Đạt:", "Fullstack Dev / Background Worker – Ký hiệu: DN"),
        ("5. Trần Phương Nam:", "UI/UX Designer / QA Tester – Ký hiệu: NT")
    ]
    info_table = doc.add_table(rows=len(info_data), cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = Cm(6.2), Cm(9.8)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before, p1.paragraph_format.space_after = Pt(2), Pt(2)
        r1 = p1.add_run(label)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before, p2.paragraph_format.space_after = Pt(2), Pt(2)
        r2 = p2.add_run(val)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    add_p("\n\nHÀ NỘI, THÁNG 10 NĂM 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, color=(71, 85, 105), space_before=24)
    doc.add_page_break()

    # ==========================================
    # 1. NỘI DUNG TỔNG QUAN DỰ ÁN
    # ==========================================
    add_h1("1. NỘI DUNG TỔNG QUAN DỰ ÁN")
    
    add_h2("1.1. Tên dự án & Định vị sản phẩm")
    add_p(
        "• Tên dự án: Hệ thống Quản lý và Đặt vé Rạp chiếu phim trực tuyến & Check-in QR thông minh (Cinema Management System – CineManagement).\n"
        "• Định vị sản phẩm: Nền tảng thương mại điện tử và điều hành rạp chiếu phim kỹ thuật số khép kín, số hóa 100% trải nghiệm từ khâu tìm kiếm thông tin, "
        "đặt vé, chọn ghế ngồi thời gian thực, mua kèm bắp nước đến nghiệp vụ quét mã QR soát vé không chạm tại cửa phòng chiếu.",
        bold=False
    )

    add_h2("1.2. Bối cảnh thực tiễn & Xu thế chuyển đổi số")
    add_p(
        "Trong bối cảnh bùng nổ của nền kinh tế số và dịch vụ trực tuyến sau đại dịch, ngành công nghiệp điện ảnh đang chứng kiến sự chuyển dịch hành vi tiêu dùng mạnh mẽ. "
        "Khán giả – đặc biệt là thế hệ trẻ – ngày càng ưa chuộng các tiện ích không chạm (contactless), thanh toán trực tuyến qua ứng dụng ngân hàng và quản lý vé thông minh trên điện thoại di động."
    )
    add_p(
        "Tuy nhiên, qua khảo sát thực tế tại các cụm rạp chiếu phim vừa và nhỏ, quy trình bán vé và kiểm soát ra vào vẫn tồn tại nhiều rào cản lớn: ùn tắc kéo dài tại quầy vé giờ cao điểm, "
        "vé in nhiệt truyền thống dễ bị rách mờ, nguy cơ dùng lại vé cũ và tình trạng thất thoát doanh thu do khách hàng giữ chỗ ảo mà không thanh toán."
    )

    # ==========================================
    # 2. LÝ DO CHỌN DỰ ÁN
    # ==========================================
    add_h1("2. LÝ DO CHỌN DỰ ÁN")
    add_p("Nhóm nghiên cứu quyết định lựa chọn đề tài xây dựng hệ thống CineManagement dựa trên 3 lý do cốt lõi:")
    add_p("1. Khắc phục triệt để điểm nghẽn thực tế của quy trình truyền thống: Chấm dứt cảnh khách hàng phải xếp hàng chờ đợi 15–30 phút tại quầy vé vào các khung giờ cao điểm; loại bỏ hoàn toàn chi phí in ấn và rủi ro thất lạc của vé giấy truyền thống bằng giải pháp vé điện tử mã QR không chạm gửi thẳng về Gmail.")
    add_p("2. Giải quyết bài toán kỹ thuật trọng yếu của ngành CNTT: Xây dựng thành công cơ chế Khóa ghế thời gian thực 10 phút (Real-time Seat Hold) chống xung đột chọn trùng ghế đồng thời (Concurrency Race Condition), tích hợp thanh toán ngân hàng tự động qua chuẩn VietQR Napas 247 và phát triển công cụ quét mã QR bằng camera di động cho nhân viên xác thực khách vào rạp dưới 2 giây.")
    add_p("3. Áp dụng thực chiến khung làm việc Agile/Scrum vào môn học: Đề tài có quy mô nghiệp vụ vừa vặn và độ phức tạp kỹ thuật tiêu biểu (CSDL chuẩn 3NF, xử lý giao tác Transaction, tích hợp API ngoài). Đây là môi trường lý tưởng để nhóm thực hành trọn vẹn quy trình Scrum qua 4 Sprint với 21 User Stories được quản lý minh bạch trên Jira Software.")

    # ==========================================
    # 3. MỤC ĐÍCH VÀ MỤC TIÊU DỰ ÁN
    # ==========================================
    add_h1("3. MỤC ĐÍCH VÀ MỤC TIÊU DỰ ÁN")
    add_p(
        "• Mục đích tổng thể (Product Goal): Xây dựng một hệ sinh thái rạp chiếu phim kỹ thuật số hoàn chỉnh, kết nối liền mạch hành trình từ lúc khách hàng tra cứu phim, "
        "đặt vé, thanh toán VietQR cho đến khi nhân viên soát vé tại cửa và ban giám đốc theo dõi báo cáo doanh thu theo thời gian thực.",
        bold=True
    )
    add_p("• Mục tiêu cụ thể (SMART Goals):")
    add_p("  - Mục tiêu phạm vi: Hoàn thành 100% 21 User Stories chuẩn hóa (tổng 90 Story Points) qua 4 Sprint liên tục.")
    add_p("  - Tối ưu thời gian đặt vé: Rút ngắn toàn bộ thời gian chọn phim, giữ ghế và thanh toán của khách hàng xuống dưới 2 phút.")
    add_p("  - Độ chính xác giữ chỗ: Cơ chế khóa ghế 10 phút hoạt động chính xác tuyệt đối, triệt tiêu hoàn toàn lỗi đặt trùng ghế giữa các khách hàng.")
    add_p("  - Tốc độ soát vé tại cửa: Camera di động của nhân viên quét và xác thực mã QR vé đạt tốc độ dưới 2 giây/vé.")
    add_p("  - Tỷ lệ gửi vé tự động: 100% vé điện tử được gửi thành công về Gmail của khách hàng ngay sau khi ghi nhận thanh toán VietQR.")
    add_p("  - Tính toàn vẹn và linh hoạt: Ứng dụng chạy độc lập (Portable Single EXE), bảo tồn dữ liệu vĩnh viễn qua các lần khởi động.")

    # ==========================================
    # 4. PHÂN TÍCH ĐỐI TƯỢNG NGƯỜI DÙNG CHÍNH (3 NHÓM ĐỐI TƯỢNG - RBAC)
    # ==========================================
    add_h1("4. PHÂN TÍCH ĐỐI TƯỢNG NGƯỜI DÙNG CHÍNH (3 NHÓM ĐỐI TƯỢNG - RBAC)")
    add_p("Hệ thống được thiết kế theo mô hình phân quyền đa vai trò (Role-Based Access Control - RBAC) độc lập, phục vụ 3 nhóm đối tượng trọng yếu:")
    add_p("1. Khách hàng (Customer): Có nhu cầu tra cứu phim đang chiếu và sắp chiếu với poster điện ảnh chất lượng cao, xem trailer YouTube bản quyền, lựa chọn suất chiếu theo ngày/phòng, "
          "tương tác trực quan trên sơ đồ ghế động (Standard, VIP, Couple), giữ ghế thời gian thực chống tranh chấp trong 10 phút, đặt kèm combo bắp nước F&B, áp dụng mã voucher giảm giá, "
          "quét mã VietQR chuyển khoản nhanh và tự động nhận vé điện tử kèm mã QR bảo mật gửi về Gmail cá nhân.")
    add_p("2. Nhân viên rạp (Staff): Nhân viên làm việc tại sảnh và cửa phòng chiếu. Sử dụng ứng dụng web mở camera trên điện thoại di động (Mobile QR Scanner) để quét mã vé của khách hàng, "
          "xác thực tính hợp lệ của vé chỉ dưới 2 giây, tự động đổi trạng thái sang Đã soát vé và ngăn chặn triệt để vé giả mạo.")
    add_p("3. Quản trị viên (Admin): Ban giám đốc và quản lý rạp. Sở hữu Dashboard điều hành tập trung: quản lý danh mục phim kèm 15 poster điện ảnh, thiết lập thông số phòng chiếu và tự sinh ma trận ghế, "
          "lập lịch suất chiếu tối ưu có thuật toán chống trùng lặp giờ phòng, quản lý thực đơn F&B/voucher, cấp tài khoản nhân viên và theo dõi biểu đồ doanh thu cùng tỷ lệ lấp đầy rạp (Occupancy Rate).")

    # ==========================================
    # 5. BỘ CÔNG NGHỆ SỬ DỤNG (TECHNOLOGY STACK)
    # ==========================================
    add_h1("5. BỘ CÔNG NGHỆ SỬ DỤNG (TECHNOLOGY STACK)")
    add_p("Dự án ưu tiên tính ổn định, tốc độ và khả năng đóng gói độc lập không phụ thuộc môi trường cài đặt phức tạp:")
    add_p("• Backend: C# / .NET 10 (ASP.NET Core MVC kết hợp RESTful Web APIs, Entity Framework Core 10).")
    add_p("• Cơ sở dữ liệu: Hệ quản trị CSDL quan hệ MySQL / MariaDB 10.11 (kết nối cổng 3306, collation chuẩn tiếng Việt utf8mb4_unicode_ci, ORM Pomelo.EntityFrameworkCore.MySql kết hợp cơ chế tự động chuyển tiếp sang SQLite app.db dự phòng nếu mất kết nối server).")
    add_p("• Dịch vụ chạy nền (Background Worker): Background Hosted Service (SeatHoldTimeoutWorker chu kỳ quét 30 giây độc lập với HTTP Request, tự động giải phóng ghế quá hạn 10 phút về trạng thái trống).")
    add_p("• Dịch vụ Email & Cổng thanh toán: MailKit / Google Gmail SMTP (smtp.gmail.com:587 TLS) tự động gửi vé; VietQR API tích hợp chuyển khoản liên ngân hàng chuẩn Napas 247.")
    add_p("• Xử lý mã QR & Giao diện: Thư viện QRCoder (server-side token) và html5-qrcode (client-side scanner); Tailwind CSS v4 tông màu Trắng Kem (#FAF7F2), Phosphor Icons, JavaScript ES6 Fetch API.")
    add_p("• Đóng gói & Triển khai: Đóng gói dưới dạng Single-File Self-contained Portable Windows EXE (CineManagement.exe ~60MB), khởi chạy trực tiếp bằng file batch START-Cinema.bat mà không cần cài đặt .NET Runtime hay MySQL thủ công.")

    # ==========================================
    # 6. DANH SÁCH 21 USER STORIES CHUẨN HÓA
    # ==========================================
    add_h1("6. DANH SÁCH 21 USER STORIES CHUẨN HÓA (PRODUCT BACKLOG)")
    add_p("Toàn bộ 21 User Stories được chuẩn hóa theo đúng cấu trúc 4 cột (ID, As a..., I want to be able to..., So that...), loại bỏ hoàn toàn thông tin phụ nhằm tập trung tối đa vào giá trị nghiệp vụ:")

    t_stories = doc.add_table(rows=22, cols=4)
    t_stories.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_stories.rows[0])
    make_row_cant_split(t_stories.rows[0])

    t_headers = ["ID", "As a... (Vai trò)", "I want to be able to... (Tính năng mong muốn)", "So that... (Mục đích / Lợi ích mang lại)"]
    t_widths = [1.2, 2.6, 6.2, 6.0] # Sum = 16.0 cm
    for i, h in enumerate(t_headers):
        add_header_cell(t_stories.rows[0], i, h, width_cm=t_widths[i])

    stories_data = [
        ("1", "Khách hàng", "Tạo tài khoản thành viên của rạp", "Tôi có thể tích điểm, nhận ưu đãi và không phải điền lại thông tin cá nhân mỗi lần mua vé"),
        ("2", "Quản lý", "Cấp tài khoản cho thành viên mới", "Nhân viên có thể bắt đầu làm việc tại quầy mà không xem được dữ liệu doanh thu"),
        ("3", "Quản lý", "Truy cập vào trang điều khiển nội bộ", "Điều hành toàn bộ hoạt động của rạp chiếu phim từ xa"),
        ("4", "Quản lý", "Đảm bảo hệ thống tự chặn các quyền truy cập sai", "Dữ liệu khách hàng và tài chính của rạp không bị kẻ gian đánh cắp"),
        ("5", "Quản lý", "Cập nhật danh sách các bộ phim mới (kèm trailer, poster)", "Khách hàng có thể biết rạp đang chiếu phim gì hấp dẫn để đi xem"),
        ("6", "Khách hàng", "Tìm kiếm bằng cách gõ tên phim hoặc thể loại yêu thích", "Tôi nhanh chóng tìm được bộ phim yêu thích"),
        ("7", "Quản lý", "Vẽ lại sơ đồ ghế ngồi trên hệ thống cho tương tự với ngoài đời", "Khách hàng không bị bỡ ngỡ và ngồi đúng vị trí khi bước vào rạp"),
        ("8", "Quản lý", "Xếp lịch chiếu cho từng phim vào các khung giờ", "Rạp tối ưu hoá được doanh thu và khách có nhiều lựa chọn thời gian"),
        ("9", "Quản lý", "Đưa các combo bắp nước lên hệ thống", "Khách hàng có thể bị hấp dẫn và mua kèm lúc đặt vé"),
        ("10", "Khách hàng", "Xem lịch chiếu chi tiết của các bộ phim tôi đang quan tâm", "Tôi có thể chốt khung giờ hợp nhất với lịch trình cá nhân của mình"),
        ("11", "Khách hàng", "Nhìn thấy sơ đồ rạp và tự tay chọn ghế ngồi", "Tôi có thể đảm bảo mình được ngồi cạnh bạn bè và có góc nhìn tốt nhất"),
        ("12", "Khách hàng", "Vị trí ghế tôi vừa chọn được hệ thống giữ lại trong vài phút", "Người khác không thể cướp mất chỗ ưng ý trong lúc tôi đang thanh toán"),
        ("13", "Khách hàng", "Đặt trước combo bắp nước ngay trên điện thoại", "Tôi có thể đi thẳng vào rạp mà không cần xếp hàng mệt mỏi ở quầy bán đồ ăn"),
        ("14", "Khách hàng", "Sử dụng các mã giảm giá tôi sưu tầm được khi chốt đơn", "Tôi tiết kiệm được tiền vé cho các buổi đi chơi"),
        ("15", "Khách hàng", "Thanh toán tiền vé qua các ví điện tử hoặc thẻ ngân hàng", "Tôi có thể chốt vé ngay tại nhà mà không sợ đến nơi rạp báo hết chỗ"),
        ("16", "Quản lý", "Tự động huỷ vé đã giữ chỗ quá 10 phút mà chưa thanh toán", "Tôi có thể mở lại ghế đó cho những khách hàng muốn mua"),
        ("17", "Khách hàng", "Nhận được mã vé điện tử (QR) về điện thoại khi trả tiền xong", "Tôi yên tâm là mình đã mua thành công và có mã để đưa cho người soát vé"),
        ("18", "Nhân viên", "Dùng điện thoại quét mã vé của khách một cách nhanh chóng", "Tôi có thể cho khách vào rạp kịp giờ chiếu mà không gây ùn tắc ở cửa"),
        ("19", "Khách hàng", "Xem lại danh sách những bộ phim mình đã từng đi xem tại rạp", "Tôi có thể nhớ lại kỷ niệm hoặc lấy thông tin giới thiệu lại cho bạn bè"),
        ("20", "Khách hàng", "Để lại nhận xét và chấm điểm cho bộ phim tôi vừa xem", "Tôi có thể chia sẻ cảm xúc và giúp người khác biết phim này có đáng xem không"),
        ("21", "Quản lý", "Theo dõi biểu đồ doanh thu bán vé hàng ngày", "Tôi biết rạp đang làm ăn ra sao và phim nào đang hút khách nhất để tăng suất chiếu")
    ]
    for row_idx, data in enumerate(stories_data):
        row = t_stories.rows[row_idx + 1]
        make_row_cant_split(row)
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9, width_cm=t_widths[col_idx])

    doc.add_page_break()

    # ==========================================
    # 7. YÊU CẦU VÀ PHẠM VI DỰ ÁN
    # ==========================================
    add_h1("7. YÊU CẦU VÀ PHẠM VI DỰ ÁN")

    add_h2("7.1. Yêu cầu chức năng chi tiết & Đặc tả nghiệp vụ (Functional Requirements)")
    add_p(
        "Hệ thống CineManagement được thiết kế bao gồm 5 phân hệ chức năng cốt lõi với 20 ca sử dụng (Use Cases) chi tiết, "
        "đáp ứng đầy đủ các yêu cầu nghiệp vụ thực tế của một cụm rạp chiếu phim hiện đại từ khâu đặt vé trực tuyến đến vận hành tại rạp:"
    )

    # Bảng 20 Use Cases
    t_uc = doc.add_table(rows=21, cols=4)
    t_uc.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_uc.rows[0])
    make_row_cant_split(t_uc.rows[0])

    uc_headers = ["Mã UC", "Tên chức năng nghiệp vụ", "Tác nhân chính", "Mô tả tóm tắt nghiệp vụ"]
    uc_widths = [1.8, 4.2, 3.2, 6.8] # Sum = 16.0 cm
    for i, h in enumerate(uc_headers):
        add_header_cell(t_uc.rows[0], i, h, width_cm=uc_widths[i])

    uc_data = [
        ("UC-1.1", "Đăng ký & Đăng nhập (RBAC)", "Khách hàng, Nhân viên, Admin", "Xác thực tài khoản, mã hóa PBKDF2, phát hành Cookie Authentication an toàn."),
        ("UC-1.2", "Quản lý hồ sơ & Đổi mật khẩu", "Tất cả người dùng", "Cập nhật thông tin cá nhân, số điện thoại; cơ chế xác thực mật khẩu cũ khi đổi."),
        ("UC-1.3", "Cấp & Quản lý tài khoản Staff", "Quản trị viên (Admin)", "Tạo tài khoản nhân viên quầy/soát vé, phân quyền nghiệp vụ, bảo mật doanh thu."),
        ("UC-1.4", "Kiểm soát phân quyền & Anti-CSRF", "Hệ thống (System)", "Bộ lọc Authorize chặn URL trái phép (403 Forbidden); Anti-Forgery Token trên Form."),
        ("UC-2.1", "Quản lý danh mục phim & Trailer", "Quản trị viên (Admin)", "CRUD phim, upload 15 poster điện ảnh chuẩn kích thước, nhúng link trailer YouTube."),
        ("UC-2.2", "Cấu hình phòng chiếu & Sinh ma trận ghế", "Quản trị viên (Admin)", "Thiết lập phòng 2D/3D/IMAX; tự động sinh ma trận ghế (Standard, VIP, Couple)."),
        ("UC-2.3", "Lập lịch suất chiếu & Chống trùng phòng", "Quản trị viên (Admin)", "Xếp lịch chiếu tối ưu, tự động tính EndTime = StartTime + Duration + 20p dọn dẹp."),
        ("UC-2.4", "Tra cứu, tìm kiếm & Lọc phim", "Khách hàng", "Tìm kiếm phim theo tên, thể loại yêu thích; xem lịch chiếu theo từng ngày/phòng."),
        ("UC-3.1", "Chọn ghế trực quan trên sơ đồ động", "Khách hàng", "Hiển thị sơ đồ ghế thời gian thực theo trạng thái: Trống, Đang giữ, Đã bán, Đang chọn."),
        ("UC-3.2", "Khóa ghế thời gian thực (Hold 10p)", "Khách hàng, Hệ thống", "Cơ chế SeatHoldEngine khóa ghế 10 phút chống tranh chấp ghế (Concurrency Lock)."),
        ("UC-3.3", "Tự động giải phóng ghế quá hạn", "Background Worker", "Dịch vụ chạy nền SeatHoldTimeoutWorker quét mỗi 30s tự động nhả ghế quá hạn về Trống."),
        ("UC-3.4", "Thanh toán chuyển khoản VietQR", "Khách hàng, Hệ thống", "Sinh mã VietQR động chuẩn Napas 247 đúng số tiền sau voucher; xác nhận đơn tự động."),
        ("UC-4.1", "Sinh vé điện tử & Mã hóa Token QR", "Hệ thống (System)", "Sinh mã vé Token ngẫu nhiên SHA-256 bảo mật cao; mã hóa ảnh QR qua QRCoder."),
        ("UC-4.2", "Tự động gửi vé qua Gmail SMTP", "Hệ thống (System)", "MailKit tự động đóng gói vé HTML Cinema Pass và ảnh QR gửi 100% về Gmail khách."),
        ("UC-4.3", "Quét mã QR soát vé bằng Camera", "Nhân viên (Staff)", "Sử dụng camera điện thoại quét mã QR vé tại cửa phòng; xác thực hợp lệ dưới 2 giây."),
        ("UC-4.4", "Lịch sử đặt vé phong cách Cinema Pass", "Khách hàng", "Quản lý toàn bộ danh sách vé đã mua, xem lại mã QR và thông tin suất chiếu."),
        ("UC-5.1", "Quản lý & Đặt kèm combo bắp nước F&B", "Khách hàng, Quản lý", "Quản lý thực đơn F&B; khách hàng đặt trước bắp ngọt/nước ngọt khi mua vé."),
        ("UC-5.2", "Quản lý & Áp dụng mã Voucher giảm giá", "Khách hàng, Quản lý", "Thiết lập mã khuyến mại; tự động khấu trừ số tiền đơn hàng khi thỏa điều kiện."),
        ("UC-5.3", "Đánh giá 1-5 sao & Bình luận phim", "Khách hàng", "Khán giả sau khi xem phim xong có thể chấm điểm và viết review chia sẻ cảm nhận."),
        ("UC-5.4", "Dashboard báo cáo doanh thu & Occupancy", "Quản trị viên (Admin)", "Thống kê doanh thu 3 nguồn (Vé, F&B, Thực thu) và Tỷ lệ lấp đầy rạp (Occupancy Rate).")
    ]
    for row_idx, data in enumerate(uc_data):
        row = t_uc.rows[row_idx + 1]
        make_row_cant_split(row)
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=8.8, width_cm=uc_widths[col_idx])

    add_p("\nBảng Ma trận phân quyền các chức năng hệ thống (Role-Based Access Control - RBAC Matrix):", bold=True)
    t_rbac = doc.add_table(rows=9, cols=5)
    t_rbac.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_rbac.rows[0])
    make_row_cant_split(t_rbac.rows[0])

    rbac_headers = ["Nhóm chức năng nghiệp vụ", "Khách hàng", "Nhân viên (Staff)", "Quản trị viên (Admin)", "Background Worker"]
    rbac_widths = [5.6, 2.6, 2.6, 2.6, 2.6] # Sum = 16.0 cm
    for i, h in enumerate(rbac_headers):
        add_header_cell(t_rbac.rows[0], i, h, width_cm=rbac_widths[i])

    rbac_data = [
        ("1. Đăng ký, đăng nhập & quản lý hồ sơ cá nhân", "X Cho phép", "X Cho phép", "X Cho phép", "--"),
        ("2. Cấp tài khoản nhân viên & cấu hình quyền hạn", "--", "--", "X Cho phép", "--"),
        ("3. CRUD Phim, Phòng chiếu & Lập lịch suất chiếu", "--", "--", "X Cho phép", "--"),
        ("4. Tra cứu phim, chọn ghế & thanh toán VietQR", "X Cho phép", "--", "--", "--"),
        ("5. Khóa giữ ghế 10 phút thời gian thực", "X Kích hoạt", "--", "--", "--"),
        ("6. Quét định kỳ tự động nhả ghế quá hạn 10p", "--", "--", "--", "X Tự động chạy"),
        ("7. Quét camera điện thoại soát vé QR tại cửa (<2s)", "--", "X Cho phép", "X Cho phép", "--"),
        ("8. Xem Dashboard doanh thu & Tỷ lệ lấp đầy rạp", "--", "--", "X Cho phép", "--")
    ]
    for row_idx, data in enumerate(rbac_data):
        row = t_rbac.rows[row_idx + 1]
        make_row_cant_split(row)
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            bold_val = True if "X" in text else False
            add_body_cell(row, col_idx, text, align=align, bold=bold_val, bg_hex=bg, font_size=8.8, width_cm=rbac_widths[col_idx])

    # Chi tiết nghiệp vụ 5 phân hệ
    add_p("\nĐặc tả chi tiết quy tắc nghiệp vụ (Business Rules) 5 phân hệ:", bold=True, size=11.5)
    
    add_p("• Phân hệ 1 - Quản trị người dùng & Bảo mật: Mật khẩu người dùng được băm một chiều PBKDF2/SHA-256 kèm muối ngẫu nhiên (salt); phiên đăng nhập quản lý bằng Cookie HttpOnly và SameSite=Strict; toàn bộ các thao tác tạo/sửa/xóa đều được bảo vệ bởi Anti-Forgery Token; nhân viên rạp được cấp tài khoản riêng và bị giới hạn nghiêm ngặt không được xem số liệu doanh thu.")
    
    add_p("• Phân hệ 2 - Quản lý phim & Suất chiếu: Ma trận ghế tự sinh theo số hàng và số cột ($M \\times N$) phân loại rõ: Ghế thường (Standard), Ghế VIP (tự động phụ thu +20%), và Ghế đôi (Couple). Thuật toán lập lịch suất chiếu tự động tính thời gian kết thúc: EndTime = StartTime + Movie.Duration + 20 phút (dành cho quảng cáo và vệ sinh phòng); đồng thời chạy thuật toán kiểm tra xung đột thời gian (Collision Detection) để từ chối xếp trùng 2 phim vào cùng một phòng chiếu.")
    
    add_p("• Phân hệ 3 - Đặt vé, Khóa ghế 10 phút & VietQR: Khi khách hàng chọn ghế, hệ thống mở Database Transaction ghi nhận trạng thái Holding trong bảng HoldSeats với thời hạn đúng 10 phút (ExpiresAt = UtcNow + 10p). Cơ chế khóa ghế ngăn chặn triệt để tình trạng tranh chấp (Race Condition) giữa các khách hàng chọn đồng thời. Dịch vụ nền SeatHoldTimeoutWorker (Hosted Service) thức giấc định kỳ mỗi 30 giây để quét và xóa bỏ các lượt giữ chỗ quá hạn, trả ghế về trạng thái trống. Mã VietQR động được tạo đúng chuẩn Napas 247 tương ứng với số tiền sau khi đã trừ mã giảm giá voucher và cộng tiền bắp nước F&B.")
    
    add_p("• Phân hệ 4 - Vé điện tử & Soát vé QR di động: Mỗi vé sau thanh toán được cấp một mã Token ngẫu nhiên 32 ký tự và mã hóa thành mã QR qua thư viện QRCoder. Dịch vụ MailKit tự động gửi mẫu vé điện tử HTML Cinema Pass kèm ảnh mã QR về Gmail của khách hàng. Tại cửa phòng chiếu, nhân viên dùng ứng dụng web mở camera điện thoại quét mã QR. API /api/tickets/check-in kiểm tra 3 quy tắc: (1) Suất chiếu phải đúng ngày hôm nay; (2) Vé ở trạng thái Issued; (3) Nếu vé đã quét trước đó (CheckedIn), hệ thống lập tức báo đỏ kèm thời gian và tên nhân viên đã quét trước đó để chống vé dùng lại. Thời gian phản hồi xác thực dưới 2 giây.")
    
    add_p("• Phân hệ 5 - F&B, Voucher & Báo cáo quản trị: Khách hàng chỉ được phép chấm điểm 1-5 sao và viết review phim khi đã thực sự mua vé và suất chiếu đã kết thúc. Dashboard báo cáo bóc tách độc lập 3 nguồn: Doanh thu vé (TicketRevenue), Doanh thu bắp nước (FnBRevenue) và Doanh thu thực thu sau voucher (FinalAmount); đồng thời tự động tính Tỷ lệ lấp đầy phòng chiếu: Occupancy Rate = (Số vé đã bán / Tổng số ghế phòng) * 100%.")

    add_h2("7.2. Yêu cầu phi chức năng chi tiết (Non-Functional Requirements - NFR)")
    add_p(
        "Hệ thống CineManagement được thiết kế đáp ứng toàn diện 6 nhóm chỉ số phi chức năng chuẩn công nghiệp phần mềm ISO/IEC 25010:"
    )

    t_nfr = doc.add_table(rows=7, cols=4)
    t_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_nfr.rows[0])
    make_row_cant_split(t_nfr.rows[0])

    nfr_headers = ["Nhóm tiêu chuẩn (ISO 25010)", "Chỉ số kỹ thuật mục tiêu", "Giải pháp kiến trúc áp dụng", "Mức độ ưu tiên"]
    nfr_widths = [3.2, 4.0, 6.6, 2.2] # Sum = 16.0 cm
    for i, h in enumerate(nfr_headers):
        add_header_cell(t_nfr.rows[0], i, h, width_cm=nfr_widths[i])

    nfr_data = [
        ("1. Hiệu năng & Khả năng chịu tải (Performance)", "• Tải trang ban đầu < 1.5s\n• Quét & soát vé QR < 2s/vé\n• Khóa ghế tức thì (< 200ms)\n• Tải đồng thời 500+ users", "Tối ưu hóa truy vấn EF Core 10 (AsNoTracking), chỉ mục Index CSDL 14 bảng, kết hợp lưu Cache sơ đồ ghế và CDN tĩnh.", "Cao nhất (P0)"),
        ("2. An toàn & Bảo mật (Security)", "• Băm mật khẩu chuẩn PBKDF2\n• 100% Form có Anti-CSRF Token\n• Token QR vé không đoán được\n• Chặn URL trái phép (403)", "Tích hợp ASP.NET Core Identity, mã hóa một chiều kèm Salt, Cookie HttpOnly/SameSite, phân quyền RBAC đa tầng.", "Cao nhất (P0)"),
        ("3. Độ tin cậy & Sẵn sàng (Reliability)", "• Uptime hệ thống >= 99.5%\n• Tỷ lệ gửi vé Gmail = 100%\n• Đảm bảo tính toàn vẹn ACID", "Cơ chế Dual-Database Fallback (MySQL 10.11 tự chuyển sang SQLite app.db), bọc Database Transaction khi thanh toán/giữ ghế.", "Cao (P1)"),
        ("4. Giao diện & Trải nghiệm (Usability / UX)", "• Responsive 100% đa thiết bị\n• Màu sắc tối giản chuẩn điện ảnh\n• Thao tác đặt vé < 2 phút", "Giao diện Tailwind CSS v4 màu Trắng Kem (#FAF7F2), đồng hồ đếm ngược 10:00 rõ ràng, phân màu ghế trực quan.", "Cao (P1)"),
        ("5. Khả năng đóng gói & Triển khai (Portability)", "• Single-File Windows EXE (~60MB)\n• Khởi chạy 1-click qua file .bat\n• Không cần cài .NET/MySQL rời", "Đóng gói Portable Self-contained .NET 10, cấu hình sẵn chuỗi kết nối và bộ công cụ tự động kích hoạt CSDL.", "Cao (P1)"),
        ("6. Khả năng bảo trì & Mở rộng (Maintainability)", "• Cấu trúc N-Tier phân tầng rõ ràng\n• Tuân thủ nghiêm ngặt SOLID\n• Code-First Migrations dễ bảo trì", "Tách bạch Controllers, Services, Background Workers và DAL; quản lý toàn bộ 21 User Stories trên Jira Scrum.", "Trung bình (P2)")
    ]
    for row_idx, data in enumerate(nfr_data):
        row = t_nfr.rows[row_idx + 1]
        make_row_cant_split(row)
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=8.8, width_cm=nfr_widths[col_idx])

    add_h2("7.3. Nguyên tắc thiết kế và phát triển")
    add_p("• Nguyên tắc Agile/Scrum: Phát triển theo từng Sprint lặp và gia tăng (Iterative & Incremental), kiểm soát tiến độ minh bạch trên Jira Board, mỗi User Story tuân thủ nghiêm ngặt tiêu chuẩn INVEST.")
    add_p("• Kiến trúc phân tầng (N-Tier Architecture): Tách bạch rõ ràng các tầng độc lập: Tầng giao diện (Presentation Layer), Tầng máy chủ web & API (.NET 10 ASP.NET Core), Tầng nghiệp vụ (Business Logic Services), Tầng dịch vụ chạy nền (Background Worker), Tầng truy xuất dữ liệu (Data Access Layer - EF Core 10) và Tầng tích hợp dịch vụ bên thứ ba.")
    add_p("• Chuẩn hóa CSDL 3NF: 14 bảng quan hệ chặt chẽ, đầy đủ khóa chính (PK), khóa ngoại (FK) và chỉ mục (Index) tăng tốc độ truy vấn.")

    add_h2("7.4. Sơ đồ Thiết kế Kiến trúc Hệ thống (System Architecture Diagram)")
    add_p("Sơ đồ thiết kế hệ thống thể hiện cấu trúc 5 tầng liên kết chặt chẽ, luồng dữ liệu tương tác qua giao thức mạng và cơ chế tích hợp dịch vụ nền độc lập của CineManagement:")
    add_diagram_image("7.1", "Sơ đồ Thiết kế Kiến trúc Hệ thống (System Architecture Diagram - N-Tier)", "diagrams/fig_kientruc_hethong.png", width_inches=6.2)

    # ==========================================
    # 8. BIỂU ĐỒ PHÂN RÃ CHỨC NĂNG (BFD)
    # ==========================================
    add_h1("8. BIỂU ĐỒ PHÂN RÃ CHỨC NĂNG (FUNCTIONAL DECOMPOSITION DIAGRAM - BFD)")
    add_p("Biểu đồ phân rã chức năng (BFD) thể hiện cấu trúc cây phân cấp từ mục tiêu chung của hệ thống CineManagement (Mức 0) xuống 5 phân hệ cốt lõi (Mức 1) và 20 chức năng chi tiết (Mức 2):")

    add_diagram_image("8.1", "Biểu đồ Phân rã Chức năng (Functional Decomposition Diagram - BFD)", "diagrams/fig_chucnang_bfd.png", width_inches=6.2)

    add_p("Phân tích cấu trúc phân cấp:")
    add_p("• Mức 0 (Root): Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement).")
    add_p("• Mức 1: Gồm 5 nhánh phân hệ chức năng: 1.0 Quản trị người dùng & bảo mật; 2.0 Quản lý phim & phòng chiếu; 3.0 Đặt vé & giữ ghế thời gian thực; 4.0 Soát vé QR & dịch vụ vé điện tử; 5.0 Dịch vụ F&B, voucher & báo cáo.")
    add_p("• Mức 2: Gồm 20 chức năng lá cụ thể, ánh xạ đầy đủ và chính xác 100% phạm vi 21 User Stories đã cam kết trong Product Backlog.")

    # ==========================================
    # 9. THIẾT KẾ CƠ SỞ DỮ LIỆU & SƠ ĐỒ ERD
    # ==========================================
    add_h1("9. THIẾT KẾ CƠ SỞ DỮ LIỆU & SƠ ĐỒ ERD")
    add_p("Cơ sở dữ liệu được xây dựng trên hệ quản trị MySQL / MariaDB 10.11 (Port 3306, Collation utf8mb4_unicode_ci), chuẩn hóa bậc 3 (3NF) với 14 bảng dữ liệu thực thể:")

    add_diagram_image("9.1", "Sơ đồ Quan hệ Thực thể CSDL MySQL (Database ERD - 14 Bảng Quan hệ)", "diagrams/drawio_erd_interface.png", width_inches=6.2)

    add_p("Bảng thống kê 14 bảng dữ liệu cốt lõi:", bold=True)
    t_tables = doc.add_table(rows=15, cols=4)
    t_tables.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_tables.rows[0])
    make_row_cant_split(t_tables.rows[0])

    t_tables_headers = ["STT", "Tên bảng dữ liệu", "Khóa chính / Khóa ngoại", "Chức năng & Ý nghĩa nghiệp vụ"]
    tbl_widths = [1.2, 3.4, 4.4, 7.0] # Sum = 16.0 cm
    for i, h in enumerate(t_tables_headers):
        add_header_cell(t_tables.rows[0], i, h, width_cm=tbl_widths[i])

    tables_info = [
        ("1", "AspNetUsers", "PK: Id", "Lưu trữ tài khoản người dùng (Khách hàng, Nhân viên, Admin), email, mật khẩu băm, sđt."),
        ("2", "AspNetRoles", "PK: Id", "Định nghĩa 3 vai trò quyền hạn cốt lõi: Admin, Staff, Customer."),
        ("3", "AspNetUserRoles", "PK: (UserId, RoleId)", "Bảng liên kết quan hệ nhiều-nhiều giữa tài khoản người dùng và vai trò quyền hạn."),
        ("4", "Staffs", "PK: Id | FK: UserId", "Lưu trữ hồ sơ chi tiết của nhân viên rạp: phòng ban, chức vụ, mức lương, trạng thái."),
        ("5", "Genres", "PK: Id", "Danh mục thể loại phim: Hành động, Hài kịch, Kinh dị, Hoạt hình, Tâm lý..."),
        ("6", "Movies", "PK: Id | FK: GenreId", "Thông tin phim điện ảnh: tiêu đề, thời lượng, đạo diễn, diễn viên, link trailer YouTube, poster, rating."),
        ("7", "ScreeningRooms", "PK: Id", "Thông tin phòng chiếu: tên phòng, loại phòng (2D, 3D, IMAX, VIP), tổng số hàng, cột, sức chứa."),
        ("8", "Seats", "PK: Id | FK: RoomId", "Tọa độ ghế ngồi trong phòng: mã ghế (A1, A2...), loại ghế (Standard, VIP, Couple), trạng thái hoạt động."),
        ("9", "Showtimes", "PK: Id | FK: MovieId, RoomId", "Suất chiếu phim cụ thể: ngày giờ bắt đầu, kết thúc, giá vé cơ bản của suất chiếu."),
        ("10", "BookedSeats", "PK: Id | FK: ShowtimeId, SeatId, BookingId", "Quản lý cơ chế khóa ghế thời gian thực trong 10 phút, trạng thái Holding/Confirmed/Released."),
        ("11", "Bookings", "PK: Id | FK: UserId, ShowtimeId", "Đơn đặt vé tổng thể: mã hóa đơn, tổng tiền, tiền sau voucher, trạng thái thanh toán VietQR."),
        ("12", "Tickets", "PK: Id | FK: BookingId, BookedSeatId", "Vé điện tử chi tiết: chuỗi token mã QR bảo mật, đơn giá vé, trạng thái đã soát vé (IsUsed), thời gian soát."),
        ("13", "FoodItems", "PK: Id", "Danh mục thức ăn, nước uống, combo bắp nước bán kèm tại quầy rạp chiếu."),
        ("14", "BookingFoodItems", "PK: Id | FK: BookingId, FoodItemId", "Bảng chi tiết số lượng từng combo bắp nước được đặt kèm trong đơn đặt vé.")
    ]
    for row_idx, data in enumerate(tables_info):
        row = t_tables.rows[row_idx + 1]
        make_row_cant_split(row)
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9, width_cm=tbl_widths[col_idx])

    doc.add_page_break()

    # ==========================================
    # 10. QUY TRÌNH HOẠT ĐỘNG TỔNG THỂ (WORKFLOW)
    # ==========================================
    add_h1("10. QUY TRÌNH HOẠT ĐỘNG TỔNG THỂ (END-TO-END WORKFLOW)")
    add_p("Hệ thống CineManagement vận hành theo chu trình nghiệp vụ khép kín gồm 9 bước liên tục từ lúc người dùng bắt đầu tìm kiếm phim cho đến khi hoàn tất xem phim và kiểm soát tài chính:")

    wf_steps = [
        ("Bước 1: Tra cứu & Chọn suất chiếu", "Khách hàng truy cập trang chủ, xem poster điện ảnh sắc nét, trailer YouTube, lọc theo thể loại và chọn suất chiếu theo ngày/phòng mong muốn."),
        ("Bước 2: Chọn ghế & Kích hoạt Khóa ghế 10 phút", "Khách hàng chọn vị trí ghế trên sơ đồ trực quan (Standard, VIP, Couple). Hệ thống ngay lập tức đổi trạng thái ghế sang Đang giữ (Holding) và hiển thị đồng hồ đếm ngược 10:00. Người dùng khác không thể chọn trùng vị trí này."),
        ("Bước 3: Chọn bắp nước F&B & Áp dụng Voucher", "Khách hàng có thể chọn thêm combo bắp nước và nhập mã giảm giá. Hệ thống tự động tính toán tổng hóa đơn chính xác đến từng đồng."),
        ("Bước 4: Thanh toán chuyển khoản VietQR", "Hệ thống sinh mã VietQR động chuẩn Napas 247 đúng số tiền sau voucher. Khách hàng quét mã trên app ngân hàng để chuyển khoản nhanh."),
        ("Bước 5: Xác nhận đơn hàng & Sinh vé điện tử QR", "Hệ thống ghi nhận thanh toán thành công, đổi trạng thái đơn hàng sang Đã thanh toán (Paid), chuyển trạng thái ghế sang Đã xác nhận (Confirmed) và sinh mã Token QR bảo mật cho từng ghế."),
        ("Bước 6: Tự động gửi vé qua Gmail SMTP", "Dịch vụ nền tự động gửi email chứa giao diện Thẻ vé điện tử HTML và ảnh mã QR về đúng địa chỉ Gmail đăng ký của khách hàng."),
        ("Bước 7: Đến rạp & Soát vé qua Camera di động", "Khách hàng đến rạp xuất trình mã QR trên điện thoại. Nhân viên rạp sử dụng camera điện thoại quét mã QR; hệ thống xác thực tính hợp lệ dưới 2 giây và đổi trạng thái vé sang Đã soát vé (Used)."),
        ("Bước 8: Tự động giải phóng ghế hết hạn (Cơ chế nền)", "Nếu khách hàng chọn ghế nhưng quá 10 phút không thanh toán, Background Hosted Service (SeatHoldTimeoutWorker quét định kỳ 30s) sẽ tự động hủy đơn và trả ghế về trạng thái trống cho người khác chọn."),
        ("Bước 9: Đánh giá phim & Báo cáo quản trị", "Sau suất chiếu, khách hàng có thể chấm điểm 1-5 sao và viết review phim; Quản trị viên theo dõi Dashboard biểu đồ doanh thu và tỷ lệ lấp đầy rạp để tối ưu hóa kế hoạch kinh doanh.")
    ]

    t_wf = doc.add_table(rows=len(wf_steps)+1, cols=2)
    t_wf.alignment = WD_TABLE_ALIGNMENT.CENTER
    make_row_header(t_wf.rows[0])
    make_row_cant_split(t_wf.rows[0])

    wf_widths = [4.5, 11.5] # Sum = 16.0 cm
    add_header_cell(t_wf.rows[0], 0, "Giai đoạn / Bước nghiệp vụ", width_cm=wf_widths[0])
    add_header_cell(t_wf.rows[0], 1, "Mô tả chi tiết luồng xử lý", width_cm=wf_widths[1])

    for row_idx, (st_name, st_desc) in enumerate(wf_steps):
        row = t_wf.rows[row_idx + 1]
        make_row_cant_split(row)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        add_body_cell(row, 0, st_name, bold=True, bg_hex=bg, font_size=9.5, width_cm=wf_widths[0])
        add_body_cell(row, 1, st_desc, bg_hex=bg, font_size=9, width_cm=wf_widths[1])

    add_p("\n\nKẾT LUẬN:", bold=True, size=12.5)
    add_p(
        "Báo cáo tổng quan dự án CineManagement đã phản ánh đầy đủ, toàn diện và trung thực toàn bộ quá trình nghiên cứu, "
        "thiết kế kiến trúc CSDL, phân rã 21 User Stories theo chuẩn Agile/Scrum và kiểm thử phần mềm thực tế. "
        "Sản phẩm sẵn sàng được nghiệm thu, bảo vệ trước Hội đồng chấm thi học phần Quản lý Dự án Công nghệ Thông tin."
    )

    output_filename = "Bao_Cao_Tong_Quan_Du_An_CineManagement.docx"
    alt_filename = "Bao_Cao_Tong_Quan_Du_An_CineManagement_v2.docx"
    saved_main = False
    try:
        doc.save(output_filename)
        print(f"[OK] Đã cập nhật thành công file Word chính: {output_filename}")
        saved_main = True
    except PermissionError:
        print(f"[NOTE] File {output_filename} đang mở trong Word.")

    try:
        doc.save(alt_filename)
        print(f"[OK] Đã đồng bộ file Word phụ: {alt_filename}")
    except PermissionError:
        pass

if __name__ == "__main__":
    create_overview_report()
