import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_presentation_docx():
    doc = Document()
    
    # Page setup: A4, 2cm margins
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles
    navy = RGBColor(15, 23, 42)
    primary = RGBColor(29, 78, 216)
    dark_gray = RGBColor(51, 65, 85)
    accent = RGBColor(225, 29, 72)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.25, bold=False, italic=False, size=12, color=dark_gray):
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
            run.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = primary
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = navy
        return p

    # Header / Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run("KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN (05 PHÚT)")
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = primary

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("HỆ THỐNG QUẢN LÝ ĐẶT VÉ RẠP CHIẾU PHIM & CHECK-IN QR THÔNG MINH (CINEMANAGEMENT)\nChuẩn khớp 15 Slide PowerPoint | GVHD: TS. Trần Khánh Dung")
    run_sub.font.name = "Times New Roman"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = navy

    # Info box
    info_table = doc.add_table(rows=1, cols=1)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = info_table.rows[0].cells[0]
    cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w'))))
    set_cell_margins(cell, 120, 120, 200, 200)
    p_info = cell.paragraphs[0]
    p_info.paragraph_format.space_after = Pt(0)
    p_info.paragraph_format.line_spacing = 1.2
    r1 = p_info.add_run("• Thời lượng thuyết trình: ")
    r1.font.bold = True
    p_info.add_run("Đúng 05 phút (300 giây) | Tốc độ nói: 135 - 145 từ/phút (chuẩn học thuật)\n")
    r2 = p_info.add_run("• Đơn vị đào tạo: ")
    r2.font.bold = True
    p_info.add_run("Bộ môn Quản lý Dự án CNTT - Khoa Công nghệ Thông tin - Trường Đại học Xây dựng Hà Nội (HUCE)\n")
    r3 = p_info.add_run("• Nhóm sinh viên (5 thành viên): ")
    r3.font.bold = True
    p_info.add_run("Lâm Tuấn Kiệt (PO), Luyện Đức Chiến (SM/BE), Nguyễn Phúc Tiến (BE/DB), Nguyễn Tiến Đạt (Fullstack/Worker), Trần Phương Nam (UI/Tester)")
    for run in p_info.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    add_p("", space_after=8)

    # Section 1: Cue sheet
    add_h1("I. BẢNG PHÂN BỔ THỜI LƯỢNG CHI TIẾT (TIMING & CUE SHEET)")
    
    table_data = [
        ["Mốc thời gian", "Slide", "Nội dung trọng tâm", "Hành động & Nhấn nhá (Cue)"],
        ["0:00 - 0:20", "Slide 1", "Giới thiệu đề tài, GVHD TS. Trần Khánh Dung, 5 thành viên", "Chào trang trọng, phong thái tự tin"],
        ["0:20 - 0:40", "Slide 2", "Nỗi đau rạp truyền thống: Xếp hàng 15-30p, vé giấy, ghế ảo", "Nhấn mạnh 4 điểm nghẽn thực tế"],
        ["0:40 - 0:55", "Slide 3", "Mục tiêu: Hệ sinh thái khép kín từ đặt vé -> VietQR -> Check-in < 2s", "Khẳng định giải pháp toàn diện"],
        ["0:55 - 1:15", "Slide 4", "3 vai trò (Customer - Staff - Admin) & Background Worker nền", "Nêu bật phân tách trách nhiệm"],
        ["1:15 - 1:35", "Slide 5", "Quy trình Agile/Scrum: 4 Sprint, 90 Story Points hoàn thành 100%", "Nhấn mạnh 0 nợ kỹ thuật"],
        ["1:35 - 1:55", "Slide 6", "Phân bổ 21 User Stories qua 4 Sprint (Nền tảng -> BI)", "Nêu bật tính kế thừa qua từng Sprint"],
        ["1:55 - 2:30", "Slide 7", "9 tính năng cốt lõi: RBAC, lịch chống trùng, khóa ghế 10p, VietQR, Scan", "Điểm sáng công nghệ trọng tâm"],
        ["2:30 - 2:50", "Slide 8", "Kiến trúc N-Tier 3 tầng (.NET 10, EF Core, MySQL 10.11 / SQLite Portable)", "Nhấn mạnh tính mở rộng & đóng gói EXE"],
        ["2:50 - 3:15", "Slide 9, 10", "Sequence đặt vé - soát vé & ERD CSDL chuẩn hóa 3NF (12 bảng)", "Chỉ nhanh luồng giao dịch khép kín"],
        ["3:15 - 3:45", "Slide 11", "Kiểm thử: 8 Kịch bản trọng yếu (TC-01 -> TC-08) PASS 100%", "Khẳng định ngăn ngừa Race Condition"],
        ["3:45 - 4:10", "Slide 12", "Quản trị 4 rủi ro lớn (Race condition, Worker treo, Mail, Vé giả)", "Thể hiện tư duy quản trị dự án"],
        ["4:10 - 4:35", "Slide 13", "Đánh giá: Ưu điểm (Đạt 100% phạm vi, EXE) & Hạn chế (Webhook)", "Đánh giá khách quan, trung thực"],
        ["4:35 - 4:50", "Slide 14", "Hướng phát triển: Webhook Open Banking, AI gợi ý combo, Mobile", "Tầm nhìn nâng cấp sản phẩm"],
        ["4:50 - 5:00", "Slide 15", "Lời cảm ơn GVHD, Hội đồng & Mời đặt câu hỏi Q&A", "Cúi chào, mở phiên phản biện"]
    ]

    t = doc.add_table(rows=len(table_data), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Inches(1.1), Inches(0.9), Inches(2.7), Inches(1.9)]
    
    for r_idx, row in enumerate(t.rows):
        is_hdr = (r_idx == 0)
        for c_idx, cell in enumerate(row.cells):
            cell.width = widths[c_idx]
            tcPr = cell._tc.get_or_add_tcPr()
            if is_hdr:
                tcPr.append(parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w'))))
            elif r_idx % 2 == 1:
                tcPr.append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            set_cell_margins(cell, 80, 80, 100, 100)
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            txt = table_data[r_idx][c_idx]
            run = p.add_run(txt)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5 if not is_hdr else 11)
            run.font.bold = is_hdr or (c_idx == 0)
            if is_hdr:
                run.font.color.rgb = RGBColor(255, 255, 255)
            else:
                run.font.color.rgb = navy if c_idx == 0 else dark_gray

    add_p("", space_after=10)

    # Section 2: Detailed Spoken Script
    add_h1("II. LỜI THOẠI THUYẾT TRÌNH CHI TIẾT (FULL SCRIPT NÓI TỰ NHIÊN)")

    script_sections = [
        ("PHẦN 1: MỞ ĐẦU & BỐI CẢNH DỰ ÁN (0:00 - 0:55)", [
            ("[SLIDE 1 - Bìa đề tài] (0:00 - 0:20)",
             "\"Kính thưa quý Thầy, Cô trong Hội đồng và toàn thể các bạn sinh viên!\n"
             "Hôm nay, nhóm chúng em xin phép được đại diện trình bày báo cáo đề tài Quản lý dự án CNTT với sản phẩm: "
             "'Hệ thống Quản lý đặt vé rạp chiếu phim trực tuyến và Check-in mã QR thông minh - CineManagement'.\n"
             "Đề tài được thực hiện dưới sự hướng dẫn khoa học tận tình của Tiến sĩ Trần Khánh Dung, cùng sự phối hợp nhịp nhàng của 5 thành viên trong nhóm, phụ trách đầy đủ các vai trò Product Owner, Scrum Master, Backend, Database, Worker và QA/Tester.\""),
            
            ("[SLIDE 2 - Nỗi đau rạp truyền thống] (0:20 - 0:40)",
             "[Bấm chuyển Slide 2]\n"
             "\"Thưa thầy cô, khảo sát thực tế tại các cụm rạp chiếu phim truyền thống cho thấy 4 nút thắt lớn:\n"
             "Thứ nhất, khách hàng phải xếp hàng chờ đợi từ 15 đến 30 phút vào các khung giờ cao điểm.\n"
             "Thứ hai, vé giấy in nhiệt rất dễ rách, thất lạc và tốn kém chi phí vận hành.\n"
             "Thứ ba là vấn nạn 'xung đột giữ ghế ảo' gây thất thu nghiêm trọng cho rạp khi nhiều người cùng chọn một ghế.\n"
             "Và thứ tư, dữ liệu quản trị bị phân tán, ban giám đốc không thể nắm bắt doanh thu tức thời để ra quyết định kinh doanh.\""),

            ("[SLIDE 3 - Mục tiêu đề tài & Định hướng] (0:40 - 0:55)",
             "[Bấm chuyển Slide 3]\n"
             "\"Xuất phát từ bài toán đó, mục tiêu của CineManagement là xây dựng một hệ sinh thái số hóa toàn diện, khép kín: "
             "từ khâu khách hàng đặt vé trên Web, thanh toán chuyển khoản VietQR chuẩn quốc gia, nhận vé điện tử kèm mã QR bảo mật qua Gmail, "
             "cho đến khâu nhân viên soát vé tại cửa chỉ bằng Camera điện thoại trong chưa đầy 2 giây.\"")
        ]),

        ("PHẦN 2: QUẢN TRỊ AGILE/SCRUM & PHÂN BỔ SPRINT (0:55 - 1:55)", [
            ("[SLIDE 4 - Hệ sinh thái 3 vai trò + Background Worker] (0:55 - 1:15)",
             "[Bấm chuyển Slide 4]\n"
             "\"Kiến trúc nghiệp vụ của hệ thống được thiết kế xoay quanh 3 đối tượng người dùng chính:\n"
             "- Khách hàng (Customer): Tự do tra cứu lịch chiếu tiếng Việt, chọn ghế ngồi sơ đồ trực quan và đặt kèm combo Bắp Nước.\n"
             "- Nhân viên soát vé (Staff): Sử dụng Camera trực tiếp trên trình duyệt để check-in tức thì và đối soát trạng thái vé.\n"
             "- Quản trị viên (Admin): Giám sát Dashboard doanh thu theo phim và F&B real-time, quản lý lịch chiếu chống trùng.\n"
             "Đặc biệt, hệ thống có một Background Worker chạy ngầm độc lập để tự động giải phóng ghế hết hạn giữ chỗ sau 10 phút, bảo đảm rạp không bao giờ bị giữ ghế ảo.\""),

            ("[SLIDE 5 - Quy trình Agile/Scrum chuẩn mực] (1:15 - 1:35)",
             "[Bấm chuyển Slide 5]\n"
             "\"Về phương pháp luận quản trị dự án, nhóm áp dụng nghiêm ngặt khung làm việc Agile/Scrum qua 4 Sprint.\n"
             "Nhóm duy trì đầy đủ các sự kiện: Sprint Planning, Daily Scrum 15 phút, Sprint Review và Retrospective.\n"
             "Toàn bộ tiến độ được theo dõi trực quan trên Jira Board và GitHub. Kết quả là nhóm đã hoàn thành 100% mục tiêu với tổng khối lượng 90 Story Points, đúng hạn và hoàn toàn không phát sinh nợ kỹ thuật (0 Technical Debt).\""),

            ("[SLIDE 6 - Chi tiết 4 Sprint & 21 User Stories] (1:35 - 1:55)",
             "[Bấm chuyển Slide 6]\n"
             "\"Khối lượng 90 Story Points được cụ thể hóa thành 21 User Stories kế thừa chặt chẽ qua 4 Sprint:\n"
             "- Sprint 1 (22 SP): Thiết lập nền tảng kiến trúc, mô hình CSDL và phân quyền RBAC 3 cấp độ.\n"
             "- Sprint 2 (24 SP): Xây dựng module vận hành rạp, quản lý phim, phòng chiếu và thuật toán xếp lịch chống trùng giờ.\n"
             "- Sprint 3 (26 SP): Hoàn thiện luồng giao dịch cốt lõi: sơ đồ ghế động, khóa ghế 10 phút, đặt F&B và cổng thanh toán VietQR.\n"
             "- Sprint 4 (18 SP): Tự động gửi vé HTML qua Gmail, module Camera quét QR dưới 2 giây, Dashboard BI quản trị và đóng gói thành một file EXE duy nhất chạy độc lập.\"")
        ]),

        ("PHẦN 3: TÍNH NĂNG ĐỘT PHÁ & NỀN TẢNG KỸ THUẬT (1:55 - 3:15)", [
            ("[SLIDE 7 - 9 Tính năng nổi bật cốt lõi] (1:55 - 2:30)",
             "[Bấm chuyển Slide 7]\n"
             "\"Trên màn hình là 9 tính năng vượt trội của CineManagement. Trong đó, điểm nhấn kỹ thuật đáng chú ý nhất gồm có:\n"
             "1. Cơ chế Khóa ghế tạm thời 10 phút: Giải quyết triệt để xung đột Race Condition khi hàng trăm người truy cập cùng lúc.\n"
             "2. Cổng thanh toán VietQR Napas 247: Khách hàng chỉ cần mở app ngân hàng quét mã, không cần nhập số tài khoản thủ công.\n"
             "3. Vé điện tử đa phương tiện: Hệ thống tự động gửi email xác nhận kèm vé HTML sắc nét và mã QR được mã hóa bảo mật.\n"
             "4. Check-in Camera siêu tốc: Nhân viên không cần đầu đọc mã vạch đắt tiền, chỉ cần mở trình duyệt là có thể quét vé trong vòng dưới 2 giây.\""),

            ("[SLIDE 8 - Kiến trúc N-Tier & Công nghệ hiện đại] (2:30 - 2:50)",
             "[Bấm chuyển Slide 8]\n"
             "\"Về kiến trúc kỹ thuật, sản phẩm được xây dựng theo mô hình N-Tier 3 tầng chuẩn công nghiệp:\n"
             "- Tầng giao diện: ASP.NET Core Razor Pages, tối ưu bằng Tailwind CSS và thư viện quét html5-qrcode.\n"
             "- Tầng nghiệp vụ: Tích hợp các Service chuyên biệt như QRCoder, MailKit SMTP và Hosted Service Worker.\n"
             "- Tầng dữ liệu: Sử dụng Entity Framework Core 10 kết nối MySQL/MariaDB 10.11, đồng thời hỗ trợ chế độ SQLite cục bộ, cho phép đóng gói thành file EXE Portable có thể chạy ngay trên mọi máy tính mà không cần cài đặt môi trường phức tạp.\""),

            ("[SLIDE 9 & 10 - Sơ đồ tuần tự & ERD chuẩn 3NF] (2:50 - 3:15)",
             "[Bấm chuyển Slide 9 rồi lướt Slide 10]\n"
             "\"Ở Slide 9 và Slide 10, quý thầy cô có thể quan sát Sơ đồ tuần tự và CSDL chuẩn hóa 3NF gồm 12 bảng liên kết chặt chẽ.\n"
             "Mọi giao dịch từ chọn ghế, đối soát trạng thái vé Confirmed, Used hay Expired đều được bao bọc trong Database Transaction, đảm bảo tính toàn vẹn dữ liệu tuyệt đối (ACID).\"")
        ]),

        ("PHẦN 4: KIỂM THỬ, QUẢN TRỊ RỦI RO & ĐÁNH GIÁ (3:15 - 4:35)", [
            ("[SLIDE 11 - Kết quả Kiểm thử: 8/8 Test Cases PASS] (3:15 - 3:45)",
             "[Bấm chuyển Slide 11]\n"
             "\"Để chứng minh chất lượng phần mềm, nhóm đã thực hiện nghiêm ngặt 8 kịch bản kiểm thử tích hợp trọng yếu (TC-01 đến TC-08):\n"
             "- Kiểm thử phân quyền RBAC: PASS.\n"
             "- Xếp lịch chiếu trùng phòng: Bị thuật toán chặn chính xác: PASS.\n"
             "- Hai người tranh chấp 1 ghế cùng mili-giây: Hệ thống khóa ghế đầu tiên, thông báo cho người thứ hai: PASS.\n"
             "- Quét mã QR vé giả hoặc vé đã qua cửa: Hệ thống cảnh báo từ chối ngay lập tức: PASS.\n"
             "Tất cả 8 kịch bản đều đạt tỷ lệ thành công 100%, bảo đảm hệ thống vận hành trơn tru không lỗi nghiêm trọng.\""),

            ("[SLIDE 12 - Ma trận Quản trị 4 Rủi ro trọng yếu] (3:45 - 4:10)",
             "[Bấm chuyển Slide 12]\n"
             "\"Dưới góc độ Quản lý dự án, nhóm đã chủ động nhận diện và kiểm soát 4 rủi ro lớn bằng các giải pháp kỹ thuật cụ thể:\n"
             "1. Rủi ro Race condition: Khống chế bằng Seat Hold Lock 10 phút.\n"
             "2. Rủi ro Worker treo: Sử dụng BackgroundService chu kỳ 30s với cơ chế tự phục hồi lỗi.\n"
             "3. Rủi ro gián đoạn gửi Gmail: Xử lý qua Async Queue và ghi log.\n"
             "4. Rủi ro gian lận vé: Mã hóa chuỗi QR ngẫu nhiên chống làm giả.\""),

            ("[SLIDE 13 - Đánh giá Ưu điểm & Hạn chế] (4:10 - 4:35)",
             "[Bấm chuyển Slide 13]\n"
             "\"Nhìn lại toàn bộ quá trình, dự án đạt được những ưu điểm nổi bật:\n"
             "- Hoàn thành 100% các tiêu chí cam kết trong đề cương.\n"
             "- Ứng dụng thực tiễn cao, hỗ trợ cả triển khai Server lẫn chạy file EXE độc lập.\n"
             "Tuy nhiên, nhóm cũng thẳng thắn nhìn nhận hạn chế: Do rào cản tài khoản doanh nghiệp nên cổng VietQR hiện tại vẫn cần nhân viên đối soát trạng thái chuyển khoản thay vì Webhook tự động 24/7.\"")
        ]),

        ("PHẦN 5: ĐỊNH HƯỚNG TƯƠNG LAI & KẾT LUẬN (4:35 - 5:00)", [
            ("[SLIDE 14 - Hướng phát triển tương lai] (4:35 - 4:50)",
             "[Bấm chuyển Slide 14]\n"
             "\"Trong giai đoạn tiếp theo, nhóm định hướng 4 nâng cấp chiến lược:\n"
             "Thứ nhất, tích hợp Webhook Open Banking để tự động xác nhận tiền về tài khoản trong 1 giây.\n"
             "Thứ hai, ứng dụng AI Machine Learning để phân tích hành vi, gợi ý suất chiếu và combo F&B cá nhân hóa.\n"
             "Thứ ba, bổ sung hệ thống tích điểm thành viên Loyalty Points.\n"
             "Và thứ tư, phát triển ứng dụng di động đa nền tảng bằng Flutter hoặc .NET MAUI.\""),

            ("[SLIDE 15 - Lời cảm ơn & Phiên Q&A] (4:50 - 5:00)",
             "[Bấm chuyển Slide 15]\n"
             "\"Một lần nữa, nhóm chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới Tiến sĩ Trần Khánh Dung đã luôn tận tâm dìu dắt nhóm hoàn thành đề tài này.\n"
             "Chúng em xin trân trọng cảm ơn quý Thầy Cô trong Hội đồng đã chú ý lắng nghe.\n"
             "Sau đây, nhóm chúng em xin phép được lắng nghe ý kiến nhận xét và giải đáp các câu hỏi phản biện của Hội đồng. Em xin trân trọng cảm ơn!\"")
        ])
    ]

    for part_title, slides in script_sections:
        add_h1(part_title)
        for slide_title, spoken_text in slides:
            add_h2(slide_title)
            # Create a quote block
            q_table = doc.add_table(rows=1, cols=1)
            q_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            c = q_table.rows[0].cells[0]
            c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
            set_cell_margins(c, 100, 100, 150, 150)
            
            p_q = c.paragraphs[0]
            p_q.paragraph_format.space_after = Pt(0)
            p_q.paragraph_format.line_spacing = 1.25
            
            lines = spoken_text.split('\n')
            for l_idx, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                if l_idx > 0:
                    p_q = c.add_paragraph()
                    p_q.paragraph_format.space_after = Pt(0)
                    p_q.paragraph_format.line_spacing = 1.25
                
                if line.startswith('[') and line.endswith(']'):
                    r_act = p_q.add_run(line)
                    r_act.font.bold = True
                    r_act.font.italic = True
                    r_act.font.color.rgb = accent
                else:
                    r_txt = p_q.add_run(line)
                    r_txt.font.italic = True
                    r_txt.font.color.rgb = navy
                r_last = p_q.runs[-1]
                r_last.font.name = "Times New Roman"
                r_last.font.size = Pt(11.5)
            
            add_p("", space_after=6)

    # Section 3: Q&A Defense Guide
    add_h1("III. BỘ CÂU HỎI & TRẢ LỜI PHẢN BIỆN DỰ KIẾN (Q&A DEFENSE GUIDE)")

    qa_list = [
        ("Câu 1: Làm thế nào hệ thống chống được hiện tượng 2 người cùng đặt 1 ghế (Race Condition)?",
         "Trả lời: Thưa Thầy/Cô, hệ thống xử lý qua 2 tầng bảo vệ:\n"
         "1. Tầng ứng dụng: Khi khách hàng chọn ghế, hệ thống ngay lập tức gán trạng thái Held và đóng dấu thời gian HoldExpiresAt = UtcNow + 10 phút. Mọi yêu cầu chọn ghế từ người khác trong khoảng thời gian này đều bị từ chối.\n"
         "2. Tầng cơ sở dữ liệu: Khi thanh toán, câu lệnh Update được bọc trong một Database Transaction với mức cô lập phù hợp, kiểm tra lại điều kiện ghế chưa bị Booked. Nhờ đó loại bỏ hoàn toàn khả năng 2 khách hàng mua trùng một vị trí ghế."),
        
        ("Câu 2: Background Worker hoạt động thế nào và có ảnh hưởng đến hiệu năng Web không?",
         "Trả lời: Thưa Thầy/Cô, nhóm sử dụng IHostedService / BackgroundService tích hợp sẵn trong .NET 10.\n"
         "Worker này chạy ngầm trên một background thread hoàn toàn tách biệt với Web Request Pipeline, theo chu kỳ PeriodicTimer mỗi 30 giây hoặc 1 phút.\n"
         "Mỗi chu kỳ, Worker chỉ thực hiện một truy vấn nhẹ quét các ghế ở trạng thái Held có HoldExpiresAt < UtcNow để hoàn trả về trạng thái trống (Available). Do đó, Worker chiếm dụng CPU và RAM cực thấp (< 1%), không gây bất kỳ độ trễ nào cho khách hàng đang lướt web."),

        ("Câu 3: Làm sao ngăn ngừa việc khách hàng chụp màn hình mã QR gửi cho người khác đi xem trước?",
         "Trả lời: Thưa Thầy/Cô, mã QR của CineManagement không chỉ chứa mã vé thông thường mà chứa chuỗi QrPayload được sinh ngẫu nhiên theo chuẩn bảo mật và được lưu trong CSDL.\n"
         "Khi nhân viên quét mã tại cửa, hệ thống lập tức kiểm tra: nếu vé đang ở trạng thái Confirmed, hệ thống đổi ngay trạng thái sang CheckedIn / Used và ghi nhận nhân viên soát vé cùng thời gian check-in.\n"
         "Nếu có bất kỳ ai sử dụng lại ảnh chụp mã QR này lần thứ hai, màn hình quét lập tức hiển thị màu đỏ cảnh báo: 'Vé đã được sử dụng lúc [giờ:phút]', ngăn chặn hoàn toàn việc gian lận vé."),

        ("Câu 4: Nhóm phân chia công việc trong 4 Sprint thế nào để đạt 90 Story Points mà không trễ hạn?",
         "Trả lời: Thưa Thầy/Cô, nhóm áp dụng đúng quy trình Scrum:\n"
         "- Sprint Planning: Ước lượng điểm bằng Planning Poker, chia nhỏ User Story không quá 8 SP.\n"
         "- Daily Scrum: Họp ngắn 15 phút mỗi sáng để tháo gỡ ngay các vướng mắc (Blockers).\n"
         "- Definition of Done (DoD) chặt chẽ: Mỗi tính năng chỉ được xem là xong khi đã viết mã, review code trên GitHub và kiểm thử chạy thực tế.\n"
         "Nhờ chia việc song song giữa Front-end, Back-end và Database theo hợp đồng API rõ ràng, nhóm đã hoàn thành trọn vẹn 90 Story Points đúng cam kết.")
    ]

    for q, a in qa_list:
        add_h2(q)
        q_table = doc.add_table(rows=1, cols=1)
        q_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = q_table.rows[0].cells[0]
        c._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="EFF6FF"/>'.format(nsdecls('w'))))
        set_cell_margins(c, 100, 100, 150, 150)
        p_a = c.paragraphs[0]
        p_a.paragraph_format.space_after = Pt(0)
        p_a.paragraph_format.line_spacing = 1.25
        
        for idx, line in enumerate(a.split('\n')):
            if idx > 0:
                p_a = c.add_paragraph()
                p_a.paragraph_format.space_after = Pt(0)
                p_a.paragraph_format.line_spacing = 1.25
            r = p_a.add_run(line.strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.font.color.rgb = navy
        add_p("", space_after=6)

    out_file = "Kich_Ban_Thuyet_Trinh_5_Phut_CineManagement.docx"
    doc.save(out_file)
    print(f"SUCCESS: Saved '{out_file}' ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    create_presentation_docx()
