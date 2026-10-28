# -*- coding: utf-8 -*-
"""
Script tạo báo cáo chuẩn hóa cho Buổi 1 và Buổi 2
Môn học: Quản lý Dự án Công nghệ Thông tin (Agile/Scrum)
Đề tài: Hệ thống Quản lý và Đặt vé Rạp chiếu phim trực tuyến (CineManagement)
"""

import os
import sys
import docx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_buoi_1_2_report():
    doc = docx.Document()

    # Cấu hình lề trang A4 chuẩn (Top=2cm, Bottom=2cm, Left=3cm, Right=2cm)
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)

    # Helper format
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

    def add_header_cell(row, col_idx, text):
        cell = row.cells[col_idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_border(cell, color="1E3A8A", sz="8")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

    def add_body_cell(row, col_idx, text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, bg_hex="FFFFFF", font_size=10):
        cell = row.cells[col_idx]
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
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(185, 28, 28)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_diagram_image(fig_num, caption, img_path, width_inches=6.0):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
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
    # 1. TRANG BÌA
    # ==========================================
    add_p("TRƯỜNG ĐẠI HỌC XÂY DỰNG HÀ NỘI", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(15, 23, 42), space_after=2)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(30, 58, 138), space_after=24)

    add_p("BÁO CÁO KẾT QUẢ THỰC HIỆN BUỔI 1 & BUỔI 2", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, color=(185, 28, 28), space_after=6)
    add_p("HỌC PHẦN: QUẢN LÝ DỰ ÁN CÔNG NGHỆ THÔNG TIN", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(30, 58, 138), space_after=14)

    add_p("ĐỀ TÀI:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, color=(100, 116, 139), space_after=2)
    add_p("XÂY DỰNG HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM TRỰC TUYẾN\n(CINEMA MANAGEMENT SYSTEM)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, color=(15, 23, 42), space_after=28)

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
    # table has 8 rows
    info_table = doc.add_table(rows=8, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for idx, (label, val) in enumerate(info_data):
        row = info_table.rows[idx]
        c1, c2 = row.cells[0], row.cells[1]
        c1.width, c2.width = Cm(6.0), Cm(9.5)
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
    # PHẦN 1: BÁO CÁO THỰC HIỆN NỘI DUNG BUỔI 1
    # ==========================================
    add_h1("PHẦN 1: BÁO CÁO THỰC HIỆN NỘI DUNG BUỔI 1")
    add_p("Mục tiêu buổi 1: Đạt chuẩn đầu ra CLO 1, CLO 2. Thành lập nhóm dự án, lựa chọn và bảo vệ đề tài, khảo sát hệ thống tương đương, thiết lập công cụ quản lý dự án (Jira Software) và phân rã danh sách tính năng thành Product Backlog chuẩn hóa (21 User Stories).", italic=True)

    add_h2("1.1. Hoạt động Chuẩn bị (Pre-Class): Lập nhóm, Chọn đề tài & Khảo sát hệ thống")
    add_h3("a) Cơ cấu nhân sự và phân công vai trò Scrum Team")
    add_p("Nhóm dự án bao gồm 5 thành viên, áp dụng mô hình Scrum đa năng (Cross-functional Team), phân định trách nhiệm cụ thể như sau:")

    # Table: Phân công nhân sự
    t_team = doc.add_table(rows=6, cols=5)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_team_headers = ["STT", "Họ và tên", "Ký hiệu", "Vai trò Scrum", "Nhiệm vụ chính trong dự án"]
    for i, h in enumerate(t_team_headers):
        add_header_cell(t_team.rows[0], i, h)

    team_data = [
        ("1", "Lâm Tuấn Kiệt", "KL", "Product Owner / Dev", "Chịu trách nhiệm định nghĩa tầm nhìn sản phẩm (Product Goal), quản lý và sắp xếp độ ưu tiên Product Backlog, lập trình Lập lịch suất chiếu, tích hợp VietQR và Dashboard thống kê."),
        ("2", "Luyện Đức Chiến", "CL", "Scrum Master / Dev", "Bảo đảm quy trình làm việc theo Agile/Scrum, điều phối Daily Scrum, giải quyết trở ngại kỹ thuật; lập trình Module Xác thực RBAC, Cơ chế khóa giữ ghế 10 phút và Dịch vụ gửi Gmail tự động."),
        ("3", "Nguyễn Phúc Tiến", "TP", "Backend / Database", "Khảo sát và thiết kế CSDL MySQL 14 bảng quan hệ chuẩn hóa 3NF, xử lý Transaction chống trùng lặp, lập trình API quét mã QR soát vé trên camera di động cho nhân viên."),
        ("4", "Nguyễn Tiến Đạt", "DN", "Fullstack / Worker", "Phát triển bộ lọc tra cứu phim đa tiêu chí, quản lý danh mục combo F&B, áp dụng mã voucher giảm giá, lập trình dịch vụ nền Background Hosted Worker giải phóng ghế hết hạn."),
        ("5", "Trần Phương Nam", "NT", "UI/UX & QA Tester", "Thiết kế hệ thống Design System chuẩn màu Trắng Kem (#FAF7F2), lập trình CRUD danh mục phim kèm poster điện ảnh, xây dựng kịch bản Test Cases và thực hiện kiểm thử E2E.")
    ]
    for row_idx, data in enumerate(team_data):
        row = t_team.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9.5)

    add_h3("b) Khảo sát thực tế các hệ thống tương đương trên thị trường")
    add_p("Nhóm đã tiến hành khảo sát và đánh giá 4 nền tảng ứng dụng rạp chiếu phim phổ biến tại Việt Nam (CGV Cinemas, BHD Star, Galaxy Cinema, Beta Cinemas). Kết quả khảo sát cho thấy:")
    add_p("• Điểm mạnh hiện có: Giao diện tra cứu phim hiện đại, hỗ trợ nhiều hình thức thanh toán ví điện tử.")
    add_p("• Điểm nghẽn nghiêm trọng (Pain Points):")
    add_p("  1. Ùn tắc giờ cao điểm: Khách hàng vẫn mất từ 15–30 phút xếp hàng tại quầy để lấy vé giấy hoặc mua thêm bắp nước.")
    add_p("  2. Lỗi giữ ghế ảo và tranh chấp ghế (Concurrency Race Condition): Nhiều người chọn cùng một vị trí ghế trong cùng thời điểm dẫn đến lỗi thanh toán hoặc không tự giải phóng ghế khi khách hàng bỏ dở giỏ hàng.")
    add_p("  3. Thất lạc vé giấy và khó kiểm soát gian lận: Vé in nhiệt dễ mờ rách, nhân viên soát vé thủ công dễ nhầm lẫn hoặc không kiểm soát được vé đã sử dụng.")
    add_p("• Định vị giải pháp của đề tài: Xây dựng hệ sinh thái rạp chiếu phim CineManagement khép kín, tối ưu hóa quy trình giữ ghế thời gian thực đúng 10 phút, tự động gửi vé QR vào Gmail cá nhân ngay sau khi thanh toán VietQR, và cung cấp web app quét mã QR siêu tốc dưới 2 giây bằng camera điện thoại cho nhân viên.")

    add_h2("1.2. Hoạt động Trên lớp (In-Class): Thiết lập Jira & Phân rã tính năng")
    add_h3("a) Thiết lập công cụ quản lý dự án Jira Software")
    add_p("Nhóm đã đăng ký và cấu hình dự án Scrum trên nền tảng Jira Software Cloud với các thông số:")
    add_p("- Tên Project: Cinema Management System (CineManagement)")
    add_p("- Project Key: SCRUM")
    add_p("- Mô hình phát triển: Scrum Framework với 4 Sprint liên tục.")
    add_p("- Cấu hình Workflow: Gồm 5 trạng thái: To Do ➔ In Progress ➔ Code Review ➔ Testing ➔ Done.")
    add_p("- Đơn vị ước lượng (Estimation Unit): Story Points (SP) theo dãy số Fibonacci (1, 2, 3, 5, 8, 13).")

    add_diagram_image("1.1", "Quy trình khung làm việc Agile Scrum áp dụng trong dự án", "diagrams/fig1_scrum_process.png", width_inches=6.0)
    add_diagram_image("1.2", "Giao diện quản lý Backlog và tiến độ Sprint trên Jira Board", "diagrams/fig2_sprint1_jira.png", width_inches=6.0)

    add_h3("b) Chuẩn hóa cú pháp viết User Story")
    add_p("Các User Story được đội ngũ xây dựng tuân thủ chặt chẽ khuôn mẫu chuẩn quốc tế:")
    add_p("« Là [Vai trò người dùng], tôi muốn [Hành động / Tính năng mong muốn], để [Mục đích / Giá trị mang lại] »", bold=True, italic=True)
    add_p("Mỗi User Story đều đi kèm Tiêu chí chấp nhận (Acceptance Criteria - AC) rõ ràng, phục vụ trực tiếp cho việc viết kịch bản kiểm thử (Test Cases).")

    add_h2("1.3. Hoạt động Sau giờ học (Post-Class): Hoàn thiện Product Backlog chuẩn hóa (21 User Stories)")
    add_p("Dưới đây là bảng Product Backlog hoàn chỉnh gồm 21 User Stories được kế thừa và đồng bộ 100% từ hồ sơ dự án, phân loại theo 4 Sprint và 3 vai trò (Customer, Staff, Admin):")

    # Table Product Backlog
    t_backlog = doc.add_table(rows=22, cols=4)
    t_backlog.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_backlog_headers = ["ID", "As a...", "I want to be able to...", "So that..."]
    for i, h in enumerate(t_backlog_headers):
        add_header_cell(t_backlog.rows[0], i, h)

    backlog_data = [
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
    for row_idx, data in enumerate(backlog_data):
        row = t_backlog.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1] else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9.5)

    add_p("\nTổng số Story Points của toàn bộ Product Backlog: 90 SP. Phân bổ đồng đều qua 4 Sprint phát triển.", bold=True, italic=True)
    doc.add_page_break()

    # ==========================================
    # PHẦN 2: BÁO CÁO THỰC HIỆN NỘI DUNG BUỔI 2
    # ==========================================
    add_h1("PHẦN 2: BÁO CÁO THỰC HIỆN NỘI DUNG BUỔI 2")
    add_p("Mục tiêu buổi 2: Đạt chuẩn đầu ra CLO 1. Phân tích bài toán nghiệp vụ Domain rạp chiếu phim, xác định ranh giới (Boundaries) giữa các module, thiết kế kiến trúc CSDL phân rã Schema / DbContext độc lập, hoàn thiện Sơ đồ quan hệ thực thể (Database ERD) và viết script SQL DDL khởi tạo DB thô.", italic=True)

    add_h2("2.1. Hoạt động Chuẩn bị (Pre-Class): Nghiên cứu Domain & Bounded Contexts")
    add_p("Nhóm đã áp dụng phương pháp thiết kế hướng miền (Domain-Driven Design - DDD) để phân tích không gian nghiệp vụ rạp chiếu phim, xác định 8 Bounded Contexts (ngữ cảnh nghiệp vụ độc lập) với các ranh giới rành mạch:")

    # Table Bounded Contexts
    t_bc = doc.add_table(rows=9, cols=4)
    t_bc.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bc_headers = ["STT", "Bounded Context / Phân hệ", "Thực thể chính (Entities)", "Ranh giới trách nhiệm & Nghiệp vụ cốt lõi"]
    for i, h in enumerate(t_bc_headers):
        add_header_cell(t_bc.rows[0], i, h)

    bc_data = [
        ("1", "Identity & RBAC Context", "AspNetUsers, AspNetRoles, Staffs", "Quản lý định danh tài khoản, phân quyền vai trò (Admin, Staff, Customer), hồ sơ nhân viên rạp."),
        ("2", "Movie Catalog Context", "Movies, Genres, Reviews", "Quản lý danh mục phim, phân loại thể loại, quản lý poster, link trailer YouTube và đánh giá/bình luận của khách."),
        ("3", "Auditorium & Geometry Context", "ScreeningRooms, Seats", "Quản lý thông số kỹ thuật phòng chiếu (Standard, VIP, IMAX) và cấu trúc ma trận tọa độ hàng/cột của từng ghế."),
        ("4", "Showtime Scheduling Context", "Showtimes", "Lập lịch chiếu theo ngày/giờ/phòng, thuật toán kiểm tra xung đột thời gian (Collision Detection) chống trùng phòng."),
        ("5", "Seat Hold & Concurrency Engine", "HoldSeats", "Quản lý khóa ghế tạm thời thời gian thực (10 phút), lưu vết User giữ ghế, giải phóng ghế hết hạn qua Background Worker."),
        ("6", "Order & Booking Context", "Bookings, Tickets", "Quản lý giao dịch mua vé, tính toán tổng tiền vé, lưu thông tin khách hàng, trạng thái thanh toán (Pending/Paid/Cancelled)."),
        ("7", "Concession & Promotion Context", "FoodItems, BookingFoodItems, Vouchers", "Quản lý danh mục bắp nước F&B, giỏ hàng combo ăn kèm, áp dụng chính sách chiết khấu mã giảm giá (Voucher)."),
        ("8", "Check-in & Admission Context", "Tickets (QrToken, IsUsed, UsedAt)", "Sinh chuỗi token bảo mật cho mã QR vé, xác thực check-in tại cửa phòng chiếu bằng camera điện thoại của nhân viên.")
    ]
    for row_idx, data in enumerate(bc_data):
        row = t_bc.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9.5)

    add_h2("2.2. Hoạt động Trên lớp (In-Class): Thiết kế CSDL phân rã Schema & Sơ đồ ERD")
    add_h3("a) Nguyên tắc phân rã Schema và tách biệt DbContext")
    add_p("Trong kiến trúc hướng dịch vụ và mở rộng tương lai của CineManagement:")
    add_p("• Phân rã Schema vật lý/logic: Cơ sở dữ liệu được quy hoạch theo các Schema tách biệt logic: Identity Schema (quản lý người dùng), Catalog Schema (quản lý phim, phòng, suất chiếu), Transaction Schema (quản lý đơn đặt vé, giữ ghế, vé điện tử), và Concession Schema (quản lý F&B, voucher).")
    add_p("• Tách biệt DbContext trong Entity Framework Core:")
    add_p("  - `AppIdentityDbContext`: Chuyên trách ánh xạ bảng người dùng, vai trò Identity.")
    add_p("  - `CinemaDbContext`: Chuyên trách quản lý toàn bộ các thực thể vận hành rạp (Movies, Showtimes, Rooms, Seats, Bookings, Tickets, FoodItems, HoldSeats).")
    add_p("  - Cơ chế Transaction cô lập cao (Isolation Level ReadCommitted / Serializable) đảm bảo không bao giờ xảy ra tình trạng đặt trùng một ghế cho 2 người (Race Condition).")

    add_h3("b) Sơ đồ Quan hệ Thực thể CSDL (Database ERD - 14 Bảng)")
    add_p("Hệ thống CSDL được thiết kế chuẩn hóa bậc 3 (3NF) gồm 14 bảng dữ liệu, sử dụng bộ mã ký tự tiếng Việt đầy đủ `utf8mb4_unicode_ci` trên MySQL / MariaDB 10.11 (kết hợp chế độ SQLite dự phòng).")

    add_diagram_image("2.1", "Sơ đồ Quan hệ Thực thể CSDL MySQL (Database ERD - 14 Bảng Chuẩn hóa)", "diagrams/fig14_database_erd.png", width_inches=6.2)

    # Table 14 bảng dữ liệu
    add_p("Bảng thống kê 14 bảng dữ liệu cốt lõi trong CSDL:", bold=True)
    t_tables = doc.add_table(rows=15, cols=4)
    t_tables.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_tables_headers = ["STT", "Tên bảng dữ liệu", "Khóa chính / Khóa ngoại", "Chức năng & Ý nghĩa nghiệp vụ"]
    for i, h in enumerate(t_tables_headers):
        add_header_cell(t_tables.rows[0], i, h)

    tables_info = [
        ("1", "AspNetUsers", "PK: Id", "Lưu trữ tài khoản người dùng (Khách hàng, Nhân viên, Admin), email, mật khẩu băm, sđt."),
        ("2", "AspNetRoles", "PK: Id", "Định nghĩa 3 vai trò quyền hạn cốt lõi: Admin, Staff, Customer."),
        ("3", "AspNetUserRoles", "PK: (UserId, RoleId)", "Bảng liên kết quan hệ nhiều-nhiều giữa tài khoản người dùng và vai trò quyền hạn."),
        ("4", "Staffs", "PK: StaffId | FK: UserId", "Lưu trữ thông tin chi tiết của nhân viên rạp: phòng ban, chức vụ, mức lương, ngày vào làm."),
        ("5", "Genres", "PK: GenreId", "Danh mục thể loại phim: Hành động, Hài kịch, Kinh dị, Hoạt hình, Tâm lý..."),
        ("6", "Movies", "PK: MovieId | FK: GenreId", "Thông tin phim điện ảnh: tiêu đề, thời lượng, đạo diễn, dàn diễn viên, link trailer YouTube, poster."),
        ("7", "ScreeningRooms", "PK: RoomId", "Thông tin phòng chiếu: tên phòng, loại phòng (2D, 3D, IMAX, VIP), tổng số hàng, cột."),
        ("8", "Seats", "PK: SeatId | FK: RoomId", "Tọa độ ghế ngồi trong phòng: mã ghế (A1, A2...), loại ghế (Standard, VIP, Couple), trạng thái hoạt động."),
        ("9", "Showtimes", "PK: ShowtimeId | FK: MovieId, RoomId", "Suất chiếu phim cụ thể: ngày giờ bắt đầu, kết thúc, giá vé cơ bản của suất chiếu."),
        ("10", "HoldSeats", "PK: HoldSeatId | FK: SeatId, ShowtimeId, UserId", "Quản lý cơ chế khóa ghế thời gian thực trong 10 phút, tự động nhả ghế nếu hết hạn chưa thanh toán."),
        ("11", "Bookings", "PK: BookingId | FK: UserId, ShowtimeId, VoucherId", "Đơn đặt vé tổng thể: mã hóa đơn, tổng tiền, số tiền giảm voucher, trạng thái thanh toán VietQR."),
        ("12", "Tickets", "PK: TicketId | FK: BookingId, SeatId", "Vé điện tử chi tiết: chuỗi token mã QR bảo mật, đơn giá vé, trạng thái đã soát vé (IsUsed), thời gian soát."),
        ("13", "FoodItems", "PK: FoodItemId", "Danh mục thức ăn, nước uống, combo bắp nước bán kèm tại quầy rạp chiếu."),
        ("14", "BookingFoodItems", "PK: (BookingId, FoodItemId)", "Bảng chi tiết số lượng từng combo bắp nước được đặt kèm trong đơn đặt vé."),
    ]
    for row_idx, data in enumerate(tables_info):
        row = t_tables.rows[row_idx + 1]
        for col_idx, text in enumerate(data):
            align = WD_ALIGN_PARAGRAPH.CENTER if col_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            add_body_cell(row, col_idx, text, align=align, bg_hex=bg, font_size=9.5)

    add_h2("2.3. Hoạt động Sau giờ học (Post-Class): Script SQL DDL Khởi tạo CSDL thô")
    add_p("Nhóm đã hoàn thiện bộ mã SQL Data Definition Language (DDL) chuẩn hóa cho hệ quản trị MySQL / MariaDB 10.11 để khởi tạo toàn bộ cấu trúc bảng, khóa chính, khóa ngoại và chỉ mục (Index) tăng tốc truy vấn:")

    sql_ddl_sample = """-- ============================================================
-- SCRIPT KHỞI TẠO CSDL THÔ: CINEMA MANAGEMENT SYSTEM
-- Hệ quản trị: MySQL / MariaDB 10.11 (Collation: utf8mb4_unicode_ci)
-- ============================================================

CREATE DATABASE IF NOT EXISTS `cinema_db` 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `cinema_db`;

-- 1. Bảng Thể loại phim
CREATE TABLE IF NOT EXISTS `Genres` (
    `GenreId` INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(100) NOT NULL,
    `Description` VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Bảng Phim điện ảnh
CREATE TABLE IF NOT EXISTS `Movies` (
    `MovieId` INT AUTO_INCREMENT PRIMARY KEY,
    `Title` VARCHAR(250) NOT NULL,
    `Description` TEXT NULL,
    `Duration` INT NOT NULL, -- Thời lượng tính bằng phút
    `ReleaseDate` DATETIME NOT NULL,
    `EndDate` DATETIME NOT NULL,
    `Director` VARCHAR(150) NULL,
    `Actors` VARCHAR(300) NULL,
    `TrailerUrl` VARCHAR(500) NULL,
    `PosterUrl` VARCHAR(500) NULL,
    `Rating` DECIMAL(3,1) DEFAULT 0.0,
    `AgeRating` VARCHAR(10) DEFAULT 'P',
    `Status` INT NOT NULL DEFAULT 0, -- 0: NowShowing, 1: ComingSoon, 2: Ended
    `GenreId` INT NOT NULL,
    `IsActive` TINYINT(1) DEFAULT 1,
    `CreatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `UpdatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT `FK_Movies_Genres` FOREIGN KEY (`GenreId`) REFERENCES `Genres` (`GenreId`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Bảng Phòng chiếu
CREATE TABLE IF NOT EXISTS `ScreeningRooms` (
    `RoomId` INT AUTO_INCREMENT PRIMARY KEY,
    `RoomName` VARCHAR(100) NOT NULL,
    `RoomType` INT NOT NULL DEFAULT 0, -- 0: 2D, 1: 3D, 2: IMAX, 3: VIP
    `TotalRows` INT NOT NULL,
    `TotalColumns` INT NOT NULL,
    `Capacity` INT NOT NULL,
    `IsActive` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Bảng Ghế ngồi
CREATE TABLE IF NOT EXISTS `Seats` (
    `SeatId` INT AUTO_INCREMENT PRIMARY KEY,
    `RoomId` INT NOT NULL,
    `RowName` VARCHAR(5) NOT NULL,
    `SeatNumber` INT NOT NULL,
    `SeatType` INT NOT NULL DEFAULT 0, -- 0: Standard, 1: VIP, 2: Couple
    `PriceMultiplier` DECIMAL(3,2) DEFAULT 1.00,
    `IsActive` TINYINT(1) DEFAULT 1,
    CONSTRAINT `FK_Seats_ScreeningRooms` FOREIGN KEY (`RoomId`) REFERENCES `ScreeningRooms` (`RoomId`) ON DELETE CASCADE,
    UNIQUE KEY `UQ_Room_Row_Seat` (`RoomId`, `RowName`, `SeatNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Bảng Suất chiếu
CREATE TABLE IF NOT EXISTS `Showtimes` (
    `ShowtimeId` INT AUTO_INCREMENT PRIMARY KEY,
    `MovieId` INT NOT NULL,
    `RoomId` INT NOT NULL,
    `StartTime` DATETIME NOT NULL,
    `EndTime` DATETIME NOT NULL,
    `TicketPrice` DECIMAL(18,2) NOT NULL,
    `Status` INT NOT NULL DEFAULT 0, -- 0: Active, 1: Cancelled, 2: Finished
    `CreatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_Showtimes_Movies` FOREIGN KEY (`MovieId`) REFERENCES `Movies` (`MovieId`) ON DELETE RESTRICT,
    CONSTRAINT `FK_Showtimes_Rooms` FOREIGN KEY (`RoomId`) REFERENCES `ScreeningRooms` (`RoomId`) ON DELETE RESTRICT,
    INDEX `IX_Showtime_Room_Time` (`RoomId`, `StartTime`, `EndTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Bảng Khóa giữ ghế 10 phút (Concurrency Seat Hold)
CREATE TABLE IF NOT EXISTS `HoldSeats` (
    `HoldSeatId` INT AUTO_INCREMENT PRIMARY KEY,
    `ShowtimeId` INT NOT NULL,
    `SeatId` INT NOT NULL,
    `UserId` VARCHAR(100) NOT NULL,
    `HeldAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ExpiresAt` DATETIME NOT NULL,
    `Status` INT NOT NULL DEFAULT 0, -- 0: Holding, 1: Released, 2: Confirmed
    CONSTRAINT `FK_HoldSeats_Showtimes` FOREIGN KEY (`ShowtimeId`) REFERENCES `Showtimes` (`ShowtimeId`) ON DELETE CASCADE,
    CONSTRAINT `FK_HoldSeats_Seats` FOREIGN KEY (`SeatId`) REFERENCES `Seats` (`SeatId`) ON DELETE CASCADE,
    INDEX `IX_Hold_Expire` (`Status`, `ExpiresAt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Bảng Đơn đặt vé (Bookings)
CREATE TABLE IF NOT EXISTS `Bookings` (
    `BookingId` INT AUTO_INCREMENT PRIMARY KEY,
    `BookingCode` VARCHAR(50) NOT NULL UNIQUE,
    `UserId` VARCHAR(100) NOT NULL,
    `ShowtimeId` INT NOT NULL,
    `TotalAmount` DECIMAL(18,2) NOT NULL,
    `DiscountAmount` DECIMAL(18,2) DEFAULT 0.00,
    `FinalAmount` DECIMAL(18,2) NOT NULL,
    `PaymentStatus` INT NOT NULL DEFAULT 0, -- 0: Pending, 1: Paid, 2: Failed, 3: Expired
    `PaymentMethod` VARCHAR(50) DEFAULT 'VietQR',
    `CustomerEmail` VARCHAR(150) NULL,
    `CreatedAt` DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `FK_Bookings_Showtimes` FOREIGN KEY (`ShowtimeId`) REFERENCES `Showtimes` (`ShowtimeId`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Bảng Chi tiết vé (Tickets) kèm mã QR
CREATE TABLE IF NOT EXISTS `Tickets` (
    `TicketId` INT AUTO_INCREMENT PRIMARY KEY,
    `BookingId` INT NOT NULL,
    `SeatId` INT NOT NULL,
    `Price` DECIMAL(18,2) NOT NULL,
    `QrCodeToken` VARCHAR(255) NOT NULL UNIQUE,
    `IsUsed` TINYINT(1) DEFAULT 0,
    `UsedAt` DATETIME NULL,
    CONSTRAINT `FK_Tickets_Bookings` FOREIGN KEY (`BookingId`) REFERENCES `Bookings` (`BookingId`) ON DELETE CASCADE,
    CONSTRAINT `FK_Tickets_Seats` FOREIGN KEY (`SeatId`) REFERENCES `Seats` (`SeatId`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Bảng Danh mục Combo F&B
CREATE TABLE IF NOT EXISTS `FoodItems` (
    `FoodItemId` INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(150) NOT NULL,
    `Description` VARCHAR(300) NULL,
    `Price` DECIMAL(18,2) NOT NULL,
    `ImageUrl` VARCHAR(500) NULL,
    `Category` VARCHAR(50) DEFAULT 'Combo',
    `IsAvailable` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Bảng Chi tiết F&B theo Đơn đặt
CREATE TABLE IF NOT EXISTS `BookingFoodItems` (
    `BookingId` INT NOT NULL,
    `FoodItemId` INT NOT NULL,
    `Quantity` INT NOT NULL DEFAULT 1,
    `UnitPrice` DECIMAL(18,2) NOT NULL,
    PRIMARY KEY (`BookingId`, `FoodItemId`),
    CONSTRAINT `FK_BFI_Bookings` FOREIGN KEY (`BookingId`) REFERENCES `Bookings` (`BookingId`) ON DELETE CASCADE,
    CONSTRAINT `FK_BFI_FoodItems` FOREIGN KEY (`FoodItemId`) REFERENCES `FoodItems` (`FoodItemId`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
    p_sql = doc.add_paragraph()
    p_sql.paragraph_format.space_before = Pt(4)
    p_sql.paragraph_format.space_after = Pt(8)
    r_sql = p_sql.add_run(sql_ddl_sample)
    r_sql.font.name = "Consolas"
    r_sql.font.size = Pt(8.5)
    r_sql.font.color.rgb = RGBColor(30, 41, 59)

    add_h2("2.4. Kết luận và Kế hoạch triển khai tiếp theo (Buổi 3 & 4)")
    add_p("Toàn bộ các yêu cầu của Buổi 1 và Buổi 2 đã được nhóm thực hiện hoàn thiện 100%, bảo đảm bám sát mục tiêu đào tạo chuẩn CLO 1, CLO 2:")
    add_p("1. Đã chốt danh sách 21 User Stories chuẩn hóa (90 SP) trên Jira Software.")
    add_p("2. Đã xác định 8 Bounded Contexts và thiết kế xong CSDL 14 bảng quan hệ chuẩn hóa 3NF.")
    add_p("3. Đã viết và thực thi thành công script DDL khởi tạo CSDL MySQL/SQLite có đầy đủ ràng buộc toàn vẹn.")
    add_p("4. Kế hoạch buổi tiếp theo: Triển khai lập trình Sprint 1 (Module Xác thực RBAC, Quản lý danh mục phim kèm 15 poster điện ảnh).")

    # Lưu file
    output_filename = "Bao_Cao_Buoi_1_va_2_CineManagement.docx"
    doc.save(output_filename)
    print(f"[OK] Đã tạo thành công file: {output_filename}")

if __name__ == "__main__":
    create_buoi_1_2_report()
