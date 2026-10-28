# -*- coding: utf-8 -*-
"""
Script tạo Sơ đồ Thiết kế Kiến trúc Hệ thống (System Architecture Diagram)
chuẩn định dạng draw.io (.drawio), Trình xem Web tương tác (.html) và ảnh chất lượng cao (.png)
cho dự án CineManagement.
Phong cách tối giản, chuẩn kỹ thuật học thuật (Minimalist Slate/Charcoal).
"""

import sys
import os
import zlib
import urllib.parse
import base64
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, ArrowStyle
import matplotlib.patheffects as patheffects

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng màu tối giản Slate / Monochrome
COLOR_TIER_BG = "#F8FAFC"       # Nền xám nhạt cho từng tầng
COLOR_TIER_BORDER = "#CBD5E1"   # Viền xám mảnh
COLOR_TIER_HEADER = "#1E293B"   # Slate 800 cho thanh tiêu đề tầng
COLOR_BOX_BG = "#FFFFFF"        # Nền trắng cho các khối module
COLOR_BOX_BORDER = "#475569"    # Viền xám đậm cho module
COLOR_ACCENT_BG = "#F1F5F9"     # Nền xám nhấn nhẹ cho background worker & db
COLOR_LINE = "#475569"          # Màu đường kết nối
TEXT_WHITE = "#FFFFFF"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"

def build_drawio_xml():
    """Tạo cấu trúc draw.io mxGraphModel chuẩn cho kiến trúc hệ thống CineManagement"""
    root = ET.Element("mxGraphModel", {
        "dx": "1600", "dy": "1100", "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1",
        "pageWidth": "1600", "pageHeight": "1100",
        "background": "#FFFFFF", "math": "0", "shadow": "0"
    })
    mx_root = ET.SubElement(root, "root")
    ET.SubElement(mx_root, "mxCell", {"id": "0"})
    ET.SubElement(mx_root, "mxCell", {"id": "1", "parent": "0"})

    # Tiêu đề biểu đồ
    title = ET.SubElement(mx_root, "mxCell", {
        "id": "title_banner",
        "value": "SƠ ĐỒ THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE DIAGRAM)\nHỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM (CINEMANAGEMENT)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Helvetica;fontSize=15;fontStyle=1;fontColor=#0F172A;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(title, "mxGeometry", {"x": "350", "y": "15", "width": "900", "height": "40", "as": "geometry"})

    # ==========================================
    # TẦNG 1: PRESENTATION TIER (CLIENTS)
    # ==========================================
    t1_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier1",
        "value": "TẦNG 1: GIAO DIỆN NGƯỜI DÙNG & THIẾT BỊ ĐẦU CUỐI (PRESENTATION TIER)",
        "style": "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=0;fillColor=#1E293B;strokeColor=#CBD5E1;fontColor=#FFFFFF;fontSize=11.5;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t1_box, "mxGeometry", {"x": "60", "y": "70", "width": "1480", "height": "140", "as": "geometry"})

    # 3 Khối Client
    c1 = ET.SubElement(mx_root, "mxCell", {
        "id": "client_customer",
        "value": "<b>Khách hàng (Customer Web Client)</b><br>• Giao diện Web Responsive (Tailwind CSS v4)<br>• Tra cứu phim, xem trailer YouTube, lọc theo ngày<br>• Sơ đồ ghế trực quan, đếm ngược giữ ghế 10:00<br>• Đặt bắp nước F&B, áp voucher & thanh toán VietQR",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10.5;align=left;spacingLeft=12;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(c1, "mxGeometry", {"x": "90", "y": "110", "width": "440", "height": "85", "as": "geometry"})

    c2 = ET.SubElement(mx_root, "mxCell", {
        "id": "client_staff",
        "value": "<b>Nhân viên soát vé (Staff Mobile Scanner)</b><br>• Ứng dụng Web Camera di động (html5-qrcode)<br>• Quét mã QR soát vé tại cửa phòng chiếu (&lt; 2s)<br>• Tự động đổi trạng thái vé sang Đã soát vé<br>• Ngăn chặn vé giả, vé quá hạn hoặc đã qua cổng",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10.5;align=left;spacingLeft=12;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(c2, "mxGeometry", {"x": "580", "y": "110", "width": "440", "height": "85", "as": "geometry"})

    c3 = ET.SubElement(mx_root, "mxCell", {
        "id": "client_admin",
        "value": "<b>Quản trị viên (Admin Portal Dashboard)</b><br>• Dashboard điều hành tập trung hoạt động rạp<br>• Quản lý phim, tải poster, trailer YouTube<br>• Cấu hình phòng chiếu & sinh ma trận ghế<br>• Xếp lịch chiếu chống trùng & Báo cáo doanh thu",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10.5;align=left;spacingLeft=12;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(c3, "mxGeometry", {"x": "1070", "y": "110", "width": "440", "height": "85", "as": "geometry"})

    # ==========================================
    # TẦNG 2: WEB APPLICATION & API TIER (.NET 10)
    # ==========================================
    t2_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier2",
        "value": "TẦNG 2: MÁY CHỦ ỨNG DỤNG & ĐIỀU PHỐI (WEB APPLICATION & API TIER - ASP.NET CORE / .NET 10)",
        "style": "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=0;fillColor=#334155;strokeColor=#CBD5E1;fontColor=#FFFFFF;fontSize=11.5;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t2_box, "mxGeometry", {"x": "60", "y": "250", "width": "1480", "height": "210", "as": "geometry"})

    # Kestrel + Security Gateway
    sec_box = ET.SubElement(mx_root, "mxCell", {
        "id": "sec_box",
        "value": "<b>Kestrel Web Server &amp; Middleware Bảo mật:</b> Single-File Portable Windows EXE (Port 5000) | Cookie Authentication | ASP.NET Core Identity (PBKDF2 Password Hash) | Phân quyền 3 vai trò (RBAC: Admin, Staff, Customer) | Anti-CSRF Token | Chặn URL trái phép (403)",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#64748B;fontColor=#0F172A;fontSize=10.5;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(sec_box, "mxGeometry", {"x": "90", "y": "290", "width": "1420", "height": "40", "as": "geometry"})

    # 4 Controller Blocks
    ctrl1 = ET.SubElement(mx_root, "mxCell", {
        "id": "ctrl_auth",
        "value": "<b>AuthController &amp; Account</b><br>• Đăng ký, đăng nhập RBAC<br>• Quản lý thông tin &amp; đổi mật khẩu<br>• Quản lý cấp tài khoản nhân viên",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ctrl1, "mxGeometry", {"x": "90", "y": "345", "width": "330", "height": "95", "as": "geometry"})

    ctrl2 = ET.SubElement(mx_root, "mxCell", {
        "id": "ctrl_movie",
        "value": "<b>Movie &amp; Showtime Controller</b><br>• Tra cứu, lọc phim theo thể loại<br>• Lịch chiếu thời gian thực theo phòng<br>• Quản lý danh mục phim &amp; poster",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ctrl2, "mxGeometry", {"x": "450", "y": "345", "width": "330", "height": "95", "as": "geometry"})

    ctrl3 = ET.SubElement(mx_root, "mxCell", {
        "id": "ctrl_booking",
        "value": "<b>Booking &amp; Seat Controller</b><br>• Khởi tạo đơn đặt vé &amp; giữ ghế<br>• Quản lý giỏ hàng combo F&B<br>• Tính tiền sau voucher &amp; tạo VietQR",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ctrl3, "mxGeometry", {"x": "810", "y": "345", "width": "330", "height": "95", "as": "geometry"})

    ctrl4 = ET.SubElement(mx_root, "mxCell", {
        "id": "ctrl_ticket",
        "value": "<b>Ticket &amp; Scanner Controller</b><br>• API xác thực mã QR vé (&lt;2s)<br>• Cập nhật trạng thái vé IsUsed<br>• Lịch sử vé dạng Cinema Pass",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ctrl4, "mxGeometry", {"x": "1170", "y": "345", "width": "340", "height": "95", "as": "geometry"})

    # ==========================================
    # TẦNG 3: BUSINESS LOGIC & CORE SERVICES
    # ==========================================
    t3_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier3",
        "value": "TẦNG 3: XỬ LÝ NGHIỆP VỤ & DỊCH VỤ NỀN (BUSINESS LOGIC & CORE SERVICES)",
        "style": "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=0;fillColor=#1E293B;strokeColor=#CBD5E1;fontColor=#FFFFFF;fontSize=11.5;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t3_box, "mxGeometry", {"x": "60", "y": "500", "width": "1480", "height": "170", "as": "geometry"})

    srv1 = ET.SubElement(mx_root, "mxCell", {
        "id": "srv_seathold",
        "value": "<b>SeatHoldEngine</b><br>• Khóa ghế 10 phút thời gian thực<br>• Kiểm tra tranh chấp (Race Condition)<br>• Cơ chế Pessimistic/Optimistic Lock",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(srv1, "mxGeometry", {"x": "90", "y": "545", "width": "260", "height": "105", "as": "geometry"})

    srv2 = ET.SubElement(mx_root, "mxCell", {
        "id": "srv_worker",
        "value": "<b>SeatHoldTimeoutWorker</b><br>• Background Hosted Service<br>• Chu kỳ quét tự động mỗi 30s<br>• Tự động nhả ghế quá hạn về Trống",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#1E293B;strokeWidth=1.5;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(srv2, "mxGeometry", {"x": "380", "y": "545", "width": "260", "height": "105", "as": "geometry"})

    srv3 = ET.SubElement(mx_root, "mxCell", {
        "id": "srv_qr",
        "value": "<b>QrSecurityService</b><br>• Sinh chuỗi Token ngẫu nhiên (SHA256)<br>• Mã hóa thư viện QRCoder<br>• Chống làm giả &amp; tái sử dụng mã vé",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(srv3, "mxGeometry", {"x": "670", "y": "545", "width": "260", "height": "105", "as": "geometry"})

    srv4 = ET.SubElement(mx_root, "mxCell", {
        "id": "srv_vietqr",
        "value": "<b>VietQrService</b><br>• Sinh mã VietQR động Napas 247<br>• Nhúng số tiền sau voucher<br>• Tạo nội dung chuyển khoản tự động",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(srv4, "mxGeometry", {"x": "960", "y": "545", "width": "260", "height": "105", "as": "geometry"})

    srv5 = ET.SubElement(mx_root, "mxCell", {
        "id": "srv_email",
        "value": "<b>EmailNotificationService</b><br>• MailKit Client (SMTP:587 TLS)<br>• Tạo mẫu thẻ vé điện tử HTML sắc nét<br>• Đính kèm ảnh QR &amp; gửi 100% về Gmail",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(srv5, "mxGeometry", {"x": "1250", "y": "545", "width": "260", "height": "105", "as": "geometry"})

    # ==========================================
    # TẦNG 4: DATA ACCESS LAYER & PERSISTENCE
    # ==========================================
    t4_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier4",
        "value": "TẦNG 4: TRUY XUẤT DỮ LIỆU &amp; CƠ SỞ DỮ LIỆU (DATA ACCESS LAYER - EF CORE 10 &amp; DUAL-DATABASE)",
        "style": "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=0;fillColor=#334155;strokeColor=#CBD5E1;fontColor=#FFFFFF;fontSize=11.5;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t4_box, "mxGeometry", {"x": "60", "y": "710", "width": "920", "height": "170", "as": "geometry"})

    db_ef = ET.SubElement(mx_root, "mxCell", {
        "id": "db_ef",
        "value": "<b>Entity Framework Core 10 (ApplicationDbContext)</b><br>Quản lý truy vấn LINQ, Transaction Scope, Migrations, quan hệ 14 bảng chuẩn 3NF",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#64748B;fontColor=#0F172A;fontSize=10.5;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(db_ef, "mxGeometry", {"x": "90", "y": "750", "width": "860", "height": "35", "as": "geometry"})

    db_mysql = ET.SubElement(mx_root, "mxCell", {
        "id": "db_mysql",
        "value": "<b>Primary DB: MySQL / MariaDB 10.11</b><br>• Cổng kết nối 3306, utf8mb4_unicode_ci<br>• 14 bảng dữ liệu thực thể quan hệ chặt chẽ<br>• Lưu trữ tài khoản, phim, vé, hóa đơn, bắp nước",
        "style": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#FFFFFF;strokeColor=#1E293B;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(db_mysql, "mxGeometry", {"x": "130", "y": "795", "width": "350", "height": "75", "as": "geometry"})

    db_sqlite = ET.SubElement(mx_root, "mxCell", {
        "id": "db_sqlite",
        "value": "<b>Fallback DB: SQLite (app.db Embedded)</b><br>• Tự động kích hoạt khi mất kết nối MySQL<br>• Đảm bảo Single Portable EXE khởi chạy ngay<br>• Bảo toàn dữ liệu kiểm thử cục bộ",
        "style": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(db_sqlite, "mxGeometry", {"x": "540", "y": "795", "width": "350", "height": "75", "as": "geometry"})

    # ==========================================
    # TẦNG 5: EXTERNAL THIRD-PARTY SERVICES
    # ==========================================
    t5_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier5",
        "value": "TẦNG 5: DỊCH VỤ BÊN THỨ BA (EXTERNAL SERVICES)",
        "style": "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;html=0;fillColor=#1E293B;strokeColor=#CBD5E1;fontColor=#FFFFFF;fontSize=11.5;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t5_box, "mxGeometry", {"x": "1020", "y": "710", "width": "520", "height": "170", "as": "geometry"})

    ext_vietqr = ET.SubElement(mx_root, "mxCell", {
        "id": "ext_vietqr",
        "value": "<b>VietQR API (Napas 247)</b><br>Cổng chuyển khoản liên ngân hàng tự động",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ext_vietqr, "mxGeometry", {"x": "1050", "y": "755", "width": "460", "height": "35", "as": "geometry"})

    ext_smtp = ET.SubElement(mx_root, "mxCell", {
        "id": "ext_smtp",
        "value": "<b>Google Gmail SMTP Server</b><br>smtp.gmail.com:587 TLS gửi vé điện tử tự động",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ext_smtp, "mxGeometry", {"x": "1050", "y": "798", "width": "460", "height": "35", "as": "geometry"})

    ext_yt = ET.SubElement(mx_root, "mxCell", {
        "id": "ext_yt",
        "value": "<b>YouTube CDN &amp; IFrame Player</b><br>Truyền phát trailer video điện ảnh chất lượng cao",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#475569;fontColor=#0F172A;fontSize=10;align=center;verticalAlign=middle;fontFamily=Helvetica;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(ext_yt, "mxGeometry", {"x": "1050", "y": "840", "width": "460", "height": "32", "as": "geometry"})

    # ==========================================
    # CÁC ĐƯỜNG KẾT NỐI (EDGES & FLOWS)
    # ==========================================
    # 1. Clients -> Server
    e1 = ET.SubElement(mx_root, "mxCell", {
        "id": "edge_client_server",
        "value": "HTTPS / JSON RESTful APIs / HTML Forms",
        "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=#475569;strokeWidth=1.5;fontColor=#475569;fontSize=10;align=center;verticalAlign=bottom;",
        "edge": "1", "parent": "1", "source": "client_staff", "target": "sec_box"
    })
    ET.SubElement(e1, "mxGeometry", {"relative": "1", "as": "geometry"})

    # 2. Controllers -> Services
    e2 = ET.SubElement(mx_root, "mxCell", {
        "id": "edge_ctrl_srv",
        "value": "Dependency Injection (DI Call)",
        "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=#475569;strokeWidth=1.5;fontColor=#475569;fontSize=10;align=center;verticalAlign=bottom;",
        "edge": "1", "parent": "1", "source": "ctrl_booking", "target": "srv_seathold"
    })
    ET.SubElement(e2, "mxGeometry", {"relative": "1", "as": "geometry"})

    # 3. Services -> EF Core
    e3 = ET.SubElement(mx_root, "mxCell", {
        "id": "edge_srv_ef",
        "value": "LINQ / DbContext Queries",
        "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=#475569;strokeWidth=1.5;fontColor=#475569;fontSize=10;align=center;verticalAlign=bottom;",
        "edge": "1", "parent": "1", "source": "srv_worker", "target": "db_ef"
    })
    ET.SubElement(e3, "mxGeometry", {"relative": "1", "as": "geometry"})

    # 4. Services -> External Services
    e4 = ET.SubElement(mx_root, "mxCell", {
        "id": "edge_srv_ext",
        "value": "SMTP:587 / VietQR API HTTP",
        "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=#475569;strokeWidth=1.5;fontColor=#475569;fontSize=10;align=center;verticalAlign=bottom;",
        "edge": "1", "parent": "1", "source": "srv_email", "target": "ext_smtp"
    })
    ET.SubElement(e4, "mxGeometry", {"relative": "1", "as": "geometry"})

    # Footer note
    note = ET.SubElement(mx_root, "mxCell", {
        "id": "footer_note",
        "value": "MÔ HÌNH KIẾN TRÚC PHÂN TẦNG HIỆN ĐẠI (N-TIER ARCHITECTURE) KẾT HỢP DỊCH VỤ CHẠY NỀN VÀ TÍCH HỢP ĐA DỊCH VỤ NGOÀI",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=#CBD5E1;fillColor=#F8FAFC;fontFamily=Helvetica;fontSize=10.5;fontColor=#475569;rounded=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(note, "mxGeometry", {"x": "380", "y": "900", "width": "840", "height": "28", "as": "geometry"})

    raw_xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    return raw_xml_str

def compress_for_drawio(xml_str):
    url_encoded = urllib.parse.quote(xml_str, safe='')
    compressed_bytes = zlib.compress(url_encoded.encode('utf-8'), 9)[2:-4]
    b64_encoded = base64.b64encode(compressed_bytes).decode('utf-8')
    return f"""<mxfile host="app.diagrams.net" modified="2026-10-22T07:30:00.000Z" agent="Mozilla/5.0" version="24.0.0" type="device">
  <diagram id="cine_architecture" name="Kiến Trúc Hệ Thống CineManagement">
    {b64_encoded}
  </diagram>
</mxfile>"""

def generate_files():
    raw_xml_str = build_drawio_xml()

    # 1. File plain XML
    with open("CineManagement_System_Architecture_plain.xml", "w", encoding="utf-8") as f:
        f.write(raw_xml_str)
    print("[1] Đã tạo file uncompressed XML: CineManagement_System_Architecture_plain.xml")

    # 2. File .drawio chuẩn nén Base64-Deflate
    drawio_content = compress_for_drawio(raw_xml_str)
    with open("CineManagement_System_Architecture.drawio", "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print("[2] Đã tạo file draw.io chuẩn nén: CineManagement_System_Architecture.drawio")

    # 3. File HTML Viewer
    import json
    json_xml = json.dumps(raw_xml_str)
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sơ đồ Thiết kế Kiến trúc Hệ thống - CineManagement</title>
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #1E293B;
            color: #F8FAFC;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0 0 8px 0;
            font-size: 22px;
            color: #F8FAFC;
            font-weight: 700;
        }}
        .header p {{
            margin: 0;
            color: #94A3B8;
            font-size: 13px;
        }}
        .viewer-card {{
            background: #FFFFFF;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            padding: 10px;
            overflow: auto;
            max-width: 98vw;
            margin: 0 auto;
        }}
        .mxgraph {{
            min-height: 850px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SƠ ĐỒ THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE DIAGRAM)</h1>
        <p>Hệ thống Quản lý và Đặt vé Rạp chiếu phim (Cinema Management System – CineManagement)</p>
    </div>
    <div class="viewer-card">
        <div class="mxgraph" style="max-width:100%;border:1px solid #E2E8F0;" data-mxgraph='{{"highlight":"#000000","nav":true,"resize":true,"toolbar":"zoom layers tags","edit":"_blank","xml":{json_xml}}}'></div>
    </div>
</body>
</html>
"""
    with open("CineManagement_System_Architecture_Viewer.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[3] Đã tạo file Trình xem Web: CineManagement_System_Architecture_Viewer.html")

def render_preview_image():
    """Vẽ ảnh PNG độ phân giải cao phong cách tối giản thanh lịch"""
    fig, ax = plt.subplots(figsize=(20.0, 14.0), dpi=220)
    ax.set_xlim(0, 20.0)
    ax.set_ylim(0, 14.0)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Tiêu đề
    ax.text(10.0, 13.5, "SƠ ĐỒ THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE DIAGRAM)",
            ha='center', va='center', fontsize=17, fontweight='bold', color='#0F172A')
    ax.text(10.0, 13.1, "Hệ thống Quản lý và Đặt vé Rạp chiếu phim trực tuyến (CineManagement)",
            ha='center', va='center', fontsize=12, fontstyle='italic', color='#475569')

    # ==========================
    # TẦNG 1: PRESENTATION TIER
    # ==========================
    # Khung bao Tầng 1
    ax.add_patch(FancyBboxPatch((0.6, 10.4), 18.8, 2.3, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    # Header Tầng 1
    ax.add_patch(FancyBboxPatch((0.6, 12.25), 18.8, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#1E293B", ec="#1E293B", lw=1.0))
    ax.text(10.0, 12.47, "TẦNG 1: GIAO DIỆN NGƯỜI DÙNG & THIẾT BỊ ĐẦU CUỐI (PRESENTATION TIER)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

    # 3 Box con
    # Box 1.1 Khách hàng
    ax.add_patch(FancyBboxPatch((0.9, 10.55), 5.7, 1.55, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#FFFFFF", ec="#475569", lw=1.2))
    ax.text(1.1, 11.85, "Khách hàng (Customer Web Client)", fontsize=10.5, fontweight='bold', color='#0F172A')
    c1_txt = "• Web Responsive (Tailwind CSS v4, ES6 Fetch)\n• Tra cứu phim, lịch chiếu, xem trailer YouTube\n• Sơ đồ chọn ghế động, đếm ngược giữ ghế 10:00\n• Đặt bắp nước F&B, áp voucher & thanh toán VietQR"
    ax.text(1.1, 11.15, c1_txt, fontsize=8.8, color='#334155', linespacing=1.3)

    # Box 1.2 Nhân viên
    ax.add_patch(FancyBboxPatch((7.15, 10.55), 5.7, 1.55, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#FFFFFF", ec="#475569", lw=1.2))
    ax.text(7.35, 11.85, "Nhân viên soát vé (Staff Mobile Scanner)", fontsize=10.5, fontweight='bold', color='#0F172A')
    c2_txt = "• Mobile Web Camera Scanner (html5-qrcode)\n• Quét mã QR soát vé tại cửa phòng (< 2 giây/vé)\n• Tự động đổi trạng thái vé sang Đã soát vé (IsUsed)\n• Ngăn chặn vé giả, vé quá hạn hoặc đã qua cổng"
    ax.text(7.35, 11.15, c2_txt, fontsize=8.8, color='#334155', linespacing=1.3)

    # Box 1.3 Quản trị viên
    ax.add_patch(FancyBboxPatch((13.4, 10.55), 5.7, 1.55, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#FFFFFF", ec="#475569", lw=1.2))
    ax.text(13.6, 11.85, "Quản trị viên (Admin Portal Dashboard)", fontsize=10.5, fontweight='bold', color='#0F172A')
    c3_txt = "• Dashboard điều hành tập trung hoạt động rạp\n• Quản lý danh mục phim, upload 15 poster, trailer\n• Cấu hình phòng chiếu & ma trận ghế tự động\n• Lập lịch suất chiếu tối ưu & Báo cáo doanh thu"
    ax.text(13.6, 11.15, c3_txt, fontsize=8.8, color='#334155', linespacing=1.3)

    # Mũi tên Tầng 1 -> Tầng 2
    ax.annotate("", xy=(10.0, 9.7), xytext=(10.0, 10.4),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#475569", lw=1.6))
    ax.text(10.0, 10.05, "Giao thức HTTPS / JSON RESTful APIs / Cookie Auth",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#475569',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    # ==========================
    # TẦNG 2: WEB APPLICATION TIER
    # ==========================
    ax.add_patch(FancyBboxPatch((0.6, 6.7), 18.8, 2.95, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    ax.add_patch(FancyBboxPatch((0.6, 9.2), 18.8, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#334155", ec="#334155", lw=1.0))
    ax.text(10.0, 9.42, "TẦNG 2: MÁY CHỦ ỨNG DỤNG & ĐIỀU PHỐI (WEB APPLICATION & API TIER - .NET 10 ASP.NET CORE)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

    # Thanh Kestrel Server + Middleware Security
    ax.add_patch(FancyBboxPatch((0.9, 8.45), 18.2, 0.65, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#F1F5F9", ec="#64748B", lw=1.0))
    ax.text(10.0, 8.87, "Kestrel Web Server (Port 5000 / Single Portable Windows EXE)",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(10.0, 8.62, "Cookie Authentication  |  ASP.NET Core Identity (PBKDF2 Password Hashing)  |  RBAC (Admin, Staff, Customer)  |  Anti-CSRF  |  403 Forbidden Filter",
            ha='center', va='center', fontsize=8.8, color='#475569')

    # 4 Controller Boxes
    ctrl_data = [
        ("AuthController & Account", "• Đăng ký, đăng nhập RBAC\n• Hồ sơ & Đổi mật khẩu\n• Cấp tài khoản nhân viên"),
        ("Movie & Showtime Ctrl", "• Tra cứu & Lọc phim\n• Lịch chiếu theo phòng\n• Quản lý 15 poster, trailer"),
        ("Booking & Seat Ctrl", "• Khởi tạo đơn & Giữ ghế\n• Giỏ hàng combo bắp nước\n• Áp voucher & VietQR"),
        ("Ticket & Scanner Ctrl", "• API xác thực QR (<2s)\n• Cập nhật trạng thái vé\n• Lịch sử Cinema Pass")
    ]
    cx_starts = [0.9, 5.55, 10.2, 14.85]
    cw = 4.25
    for idx, (ctitle, cdesc) in enumerate(ctrl_data):
        cx = cx_starts[idx]
        ax.add_patch(FancyBboxPatch((cx, 6.85), cw, 1.45, boxstyle="round,pad=0.03,rounding_size=0.06",
                                    fc="#FFFFFF", ec="#475569", lw=1.1))
        ax.text(cx + 0.2, 8.08, ctitle, fontsize=9.8, fontweight='bold', color='#0F172A')
        ax.text(cx + 0.2, 7.45, cdesc, fontsize=8.4, color='#334155', linespacing=1.3)

    # Mũi tên Tầng 2 -> Tầng 3
    ax.annotate("", xy=(10.0, 6.0), xytext=(10.0, 6.7),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#475569", lw=1.6))
    ax.text(10.0, 6.35, "In-process Dependency Injection (DI Service Calls)",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#475569',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    # ==========================
    # TẦNG 3: BUSINESS LOGIC SERVICES
    # ==========================
    ax.add_patch(FancyBboxPatch((0.6, 3.8), 18.8, 2.15, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    ax.add_patch(FancyBboxPatch((0.6, 5.5), 18.8, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#1E293B", ec="#1E293B", lw=1.0))
    ax.text(10.0, 5.72, "TẦNG 3: XỬ LÝ NGHIỆP VỤ & DỊCH VỤ NỀN (BUSINESS LOGIC & CORE SERVICES)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

    # 5 Service Boxes
    srv_data = [
        ("SeatHoldEngine", "• Khóa ghế 10p thời gian thực\n• Chống xung đột đồng thời\n• Cơ chế Lock an toàn"),
        ("SeatHoldWorker (Hosted)", "• Background Hosted Service\n• Quét định kỳ mỗi 30s\n• Tự nhả ghế quá hạn 10p"),
        ("QrSecurityService", "• Sinh Token ngẫu nhiên\n• Mã hóa thư viện QRCoder\n• Ngăn vé giả & quét lại"),
        ("VietQrService", "• Sinh mã VietQR Napas 247\n• Tự khớp số tiền voucher\n• Cú pháp nội dung chuẩn"),
        ("EmailNotificationService", "• MailKit (smtp.gmail.com:587)\n• Mẫu vé HTML Cinema Pass\n• Gửi 100% về Gmail")
    ]
    sx_starts = [0.9, 4.6, 8.3, 12.0, 15.7]
    sw = 3.4
    for idx, (stitle, sdesc) in enumerate(srv_data):
        sx = sx_starts[idx]
        bg = "#F1F5F9" if idx == 1 else "#FFFFFF"
        border_w = 1.4 if idx == 1 else 1.1
        border_c = "#1E293B" if idx == 1 else "#475569"
        ax.add_patch(FancyBboxPatch((sx, 3.95), sw, 1.45, boxstyle="round,pad=0.03,rounding_size=0.06",
                                    fc=bg, ec=border_c, lw=border_w))
        ax.text(sx + 0.15, 5.18, stitle, fontsize=9.2, fontweight='bold', color='#0F172A')
        ax.text(sx + 0.15, 4.55, sdesc, fontsize=8.0, color='#334155', linespacing=1.3)

    # Mũi tên Tầng 3 xuống Tầng 4 (DAL)
    ax.annotate("", xy=(5.8, 3.1), xytext=(5.8, 3.8),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#475569", lw=1.6))
    ax.text(5.8, 3.45, "EF Core 10 / LINQ Queries / Transactions",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#475569',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    # Mũi tên Tầng 3 sang Tầng 5 (External Services)
    ax.annotate("", xy=(15.5, 3.1), xytext=(15.5, 3.8),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#475569", lw=1.6))
    ax.text(15.5, 3.45, "SMTP TLS :587 / VietQR API HTTP",
            ha='center', va='center', fontsize=8.8, fontweight='bold', color='#475569',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    # ==========================
    # TẦNG 4: DATA ACCESS TIER (BÊN TRÁI)
    # ==========================
    ax.add_patch(FancyBboxPatch((0.6, 0.6), 11.0, 2.45, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    ax.add_patch(FancyBboxPatch((0.6, 2.6), 11.0, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#334155", ec="#334155", lw=1.0))
    ax.text(6.1, 2.82, "TẦNG 4: TRUY XUẤT DỮ LIỆU & CSDL (DATA ACCESS - EF CORE 10 & DUAL-DATABASE)",
            ha='center', va='center', fontsize=10.2, fontweight='bold', color='#FFFFFF')

    # EF Core Bar
    ax.add_patch(FancyBboxPatch((0.9, 1.95), 10.4, 0.55, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#F1F5F9", ec="#64748B", lw=1.0))
    ax.text(6.1, 2.22, "Entity Framework Core 10 (ApplicationDbContext) - Quản lý quan hệ 14 bảng chuẩn 3NF",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#0F172A')

    # Primary DB MySQL
    ax.add_patch(FancyBboxPatch((0.9, 0.75), 5.0, 1.1, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#FFFFFF", ec="#1E293B", lw=1.3))
    ax.text(1.1, 1.6, "Primary DB: MySQL 10.11", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(1.1, 1.15, "• Cổng 3306, utf8mb4_unicode_ci\n• 14 bảng quan hệ chuẩn 3NF đầy đủ PK/FK\n• Lưu phim, phòng, lịch, vé, tài chính",
            fontsize=8.0, color='#334155', linespacing=1.25)

    # Fallback DB SQLite
    ax.add_patch(FancyBboxPatch((6.3, 0.75), 5.0, 1.1, boxstyle="round,pad=0.03,rounding_size=0.06",
                                fc="#FFFFFF", ec="#475569", lw=1.2))
    ax.text(6.5, 1.6, "Fallback DB: SQLite (app.db)", fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(6.5, 1.15, "• Tự động chuyển tiếp khi ngắt MySQL\n• Giữ cho Single Portable EXE luôn chạy\n• Bảo tồn dữ liệu qua các lần khởi động",
            fontsize=8.0, color='#334155', linespacing=1.25)

    # ==========================
    # TẦNG 5: EXTERNAL SERVICES (BÊN PHẢI)
    # ==========================
    ax.add_patch(FancyBboxPatch((12.0, 0.6), 7.4, 2.45, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc="#F8FAFC", ec="#CBD5E1", lw=1.2))
    ax.add_patch(FancyBboxPatch((12.0, 2.6), 7.4, 0.45, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc="#1E293B", ec="#1E293B", lw=1.0))
    ax.text(15.7, 2.82, "TẦNG 5: DỊCH VỤ BÊN THỨ BA (EXTERNAL SERVICES)",
            ha='center', va='center', fontsize=10.2, fontweight='bold', color='#FFFFFF')

    # 3 Dịch vụ ngoài
    ext_items = [
        ("VietQR Gateway (Napas 247)", "Cổng thanh toán liên ngân hàng tự động"),
        ("Google Gmail SMTP Server", "smtp.gmail.com:587 TLS gửi vé điện tử"),
        ("YouTube CDN & IFrame", "Lưu trữ và phát trailer điện ảnh bản quyền")
    ]
    ey_starts = [1.95, 1.35, 0.75]
    for idx, (etitle, edesc) in enumerate(ext_items):
        ey = ey_starts[idx]
        ax.add_patch(FancyBboxPatch((12.3, ey), 6.8, 0.52, boxstyle="round,pad=0.03,rounding_size=0.06",
                                    fc="#FFFFFF", ec="#475569", lw=1.0))
        ax.text(12.5, ey + 0.34, etitle, fontsize=9.0, fontweight='bold', color='#0F172A')
        ax.text(12.5, ey + 0.12, edesc, fontsize=7.8, color='#475569')

    # Chú thích chân trang
    ax.text(10.0, 0.2, "MÔ HÌNH KIẾN TRÚC PHÂN TẦNG HIỆN ĐẠI (N-TIER SYSTEM ARCHITECTURE) - HỆ THỐNG CINEMANAGEMENT",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#64748B')

    plt.tight_layout()
    output_png = os.path.join("diagrams", "fig_kientruc_hethong.png")
    plt.savefig(output_png, dpi=220, bbox_inches='tight')
    plt.close()
    print(f"[4] Đã tạo thành công ảnh kiến trúc hệ thống: {output_png}")

if __name__ == "__main__":
    generate_files()
    render_preview_image()
