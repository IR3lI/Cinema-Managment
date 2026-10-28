# -*- coding: utf-8 -*-
"""
Tạo trọn bộ giải pháp sơ đồ ERD Draw.io - PHONG CÁCH TỐI GIẢN (MINIMALIST / MONOCHROME NEUTRAL):
1. CineManagement_Database_ERD.drawio (Định dạng nén chuẩn của diagrams.net - mở 100% không lỗi)
2. CineManagement_Database_ERD_plain.xml (Định dạng XML mở rộng cho các tool import khác)
3. CineManagement_ERD_Viewer.html (Trình xem tương tác HTML mở trực tiếp bằng trình duyệt Web)
4. diagrams/drawio_erd_interface.png (Ảnh chụp trực quan tối giản, thanh lịch, chuẩn học thuật)
"""

import sys
import os
import zlib
import urllib.parse
import base64
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng màu tối giản, chuyên nghiệp (Dark Charcoal & Slate Neutral)
HEADER_COLOR = "#262626"      # Xám đen thanh lịch, đồng bộ cho tất cả các bảng
HEADER_TEXT_COLOR = "#FFFFFF" # Chữ trắng tương phản cao
BORDER_COLOR = "#404040"      # Đường viền bảng
LINE_COLOR = "#4B5563"        # Đường liên kết quan hệ
TEXT_MAIN = "#111827"         # Chữ nội dung trường dữ liệu
TEXT_MUTED = "#6B7280"        # Kiểu dữ liệu mờ hơn
BG_CANVAS = "#FFFFFF"         # Nền canvas trắng sạch sẽ
BG_ROW_ALT = "#F9FAFB"        # Nền hàng xen kẽ

def get_tables_data():
    return [
        # Cột 1: Identity & Users
        {
            "id": "tbl_users", "name": "AspNetUsers", "color": HEADER_COLOR, "x": 60, "y": 90, "w": 320,
            "columns": [
                ("Id", "VARCHAR(255)", True, False),
                ("UserName", "VARCHAR(256)", False, False),
                ("Email", "VARCHAR(256)", False, False),
                ("FullName", "VARCHAR(150)", False, False),
                ("PhoneNumber", "VARCHAR(20)", False, False),
                ("PasswordHash", "LONGTEXT", False, False),
                ("CreatedAt", "DATETIME", False, False),
            ]
        },
        {
            "id": "tbl_staffs", "name": "Staffs", "color": HEADER_COLOR, "x": 60, "y": 400, "w": 320,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("UserId", "VARCHAR(255)", False, True),
                ("Position", "VARCHAR(100)", False, False),
                ("Department", "VARCHAR(100)", False, False),
                ("Salary", "DECIMAL(18,2)", False, False),
                ("IsActive", "TINYINT(1)", False, False),
            ]
        },
        {
            "id": "tbl_reviews", "name": "Reviews", "color": HEADER_COLOR, "x": 60, "y": 680, "w": 320,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("UserId", "VARCHAR(255)", False, True),
                ("MovieId", "INT", False, True),
                ("Rating", "INT", False, False),
                ("Comment", "TEXT", False, False),
                ("CreatedAt", "DATETIME", False, False),
            ]
        },

        # Cột 2: Movies & Rooms
        {
            "id": "tbl_genres", "name": "Genres", "color": HEADER_COLOR, "x": 460, "y": 90, "w": 310,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("Name", "VARCHAR(100)", False, False),
                ("Description", "TEXT", False, False),
            ]
        },
        {
            "id": "tbl_movies", "name": "Movies", "color": HEADER_COLOR, "x": 460, "y": 270, "w": 310,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("GenreId", "INT", False, True),
                ("Title", "VARCHAR(250)", False, False),
                ("DurationMinutes", "INT", False, False),
                ("ReleaseDate", "DATETIME", False, False),
                ("PosterUrl", "VARCHAR(500)", False, False),
                ("Rating", "DECIMAL(3,1)", False, False),
            ]
        },
        {
            "id": "tbl_rooms", "name": "ScreeningRooms", "color": HEADER_COLOR, "x": 460, "y": 590, "w": 310,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("RoomName", "VARCHAR(100)", False, False),
                ("TotalRows", "INT", False, False),
                ("TotalColumns", "INT", False, False),
                ("TotalSeats", "INT", False, False),
                ("ScreenType", "VARCHAR(50)", False, False),
            ]
        },
        {
            "id": "tbl_seats", "name": "Seats", "color": HEADER_COLOR, "x": 460, "y": 870, "w": 310,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("RoomId", "INT", False, True),
                ("RowName", "VARCHAR(5)", False, False),
                ("SeatNumber", "INT", False, False),
                ("SeatType", "VARCHAR(50)", False, False),
            ]
        },

        # Cột 3: Showtimes & HoldSeats
        {
            "id": "tbl_showtimes", "name": "Showtimes", "color": HEADER_COLOR, "x": 850, "y": 90, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("MovieId", "INT", False, True),
                ("RoomId", "INT", False, True),
                ("StartTime", "DATETIME", False, False),
                ("EndTime", "DATETIME", False, False),
                ("BasePrice", "DECIMAL(18,2)", False, False),
                ("Status", "VARCHAR(50)", False, False),
            ]
        },
        {
            "id": "tbl_bookedseats", "name": "BookedSeats (Hold 10m)", "color": HEADER_COLOR, "x": 850, "y": 420, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("ShowtimeId", "INT", False, True),
                ("SeatId", "INT", False, True),
                ("BookingId", "INT", False, True),
                ("Status", "VARCHAR(50)", False, False),
                ("Price", "DECIMAL(18,2)", False, False),
                ("HoldExpiresAt", "DATETIME", False, False),
            ]
        },

        # Cột 4: Bookings & Tickets
        {
            "id": "tbl_bookings", "name": "Bookings", "color": HEADER_COLOR, "x": 1260, "y": 90, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("UserId", "VARCHAR(255)", False, True),
                ("ShowtimeId", "INT", False, True),
                ("BookingCode", "VARCHAR(50)", False, False),
                ("TotalPrice", "DECIMAL(18,2)", False, False),
                ("FinalAmount", "DECIMAL(18,2)", False, False),
                ("PaymentMethod", "VARCHAR(50)", False, False),
                ("PaymentStatus", "VARCHAR(50)", False, False),
                ("CreatedAt", "DATETIME", False, False),
            ]
        },
        {
            "id": "tbl_tickets", "name": "Tickets (QR Code)", "color": HEADER_COLOR, "x": 1260, "y": 470, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("BookingId", "INT", False, True),
                ("BookedSeatId", "INT", False, True),
                ("TicketCode", "VARCHAR(50)", False, False),
                ("QrCodeToken", "VARCHAR(255)", False, False),
                ("Status", "VARCHAR(50)", False, False),
                ("CheckedInAt", "DATETIME", False, False),
            ]
        },
        {
            "id": "tbl_vouchers", "name": "Vouchers", "color": HEADER_COLOR, "x": 1260, "y": 780, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("Code", "VARCHAR(50)", False, False),
                ("DiscountPercent", "INT", False, False),
                ("MaxDiscountAmount", "DECIMAL(18,2)", False, False),
                ("IsActive", "TINYINT(1)", False, False),
            ]
        },

        # Cột 5: Food & Beverage
        {
            "id": "tbl_fooditems", "name": "FoodItems (F&B)", "color": HEADER_COLOR, "x": 1670, "y": 90, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("Name", "VARCHAR(150)", False, False),
                ("Description", "TEXT", False, False),
                ("Price", "DECIMAL(18,2)", False, False),
                ("ImageUrl", "VARCHAR(500)", False, False),
                ("IsAvailable", "TINYINT(1)", False, False),
            ]
        },
        {
            "id": "tbl_bookingfooditems", "name": "BookingFoodItems", "color": HEADER_COLOR, "x": 1670, "y": 400, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("BookingId", "INT", False, True),
                ("FoodItemId", "INT", False, True),
                ("Quantity", "INT", False, False),
                ("UnitPrice", "DECIMAL(18,2)", False, False),
            ]
        }
    ]

def get_relations_data():
    return [
        ("rel_genres_movies", "tbl_genres", "tbl_movies", "1 : N (GenreId)", 0.5, 1, 0.5, 0),
        ("rel_movies_showtimes", "tbl_movies", "tbl_showtimes", "1 : N (MovieId)", 1, 0.3, 0, 0.3),
        ("rel_rooms_showtimes", "tbl_rooms", "tbl_showtimes", "1 : N (RoomId)", 1, 0.3, 0, 0.7),
        ("rel_rooms_seats", "tbl_rooms", "tbl_seats", "1 : N (RoomId)", 0.5, 1, 0.5, 0),
        ("rel_users_staffs", "tbl_users", "tbl_staffs", "1 : 1 (UserId)", 0.5, 1, 0.5, 0),
        ("rel_users_reviews", "tbl_users", "tbl_reviews", "1 : N (UserId)", 0.3, 1, 0.3, 0),
        ("rel_movies_reviews", "tbl_movies", "tbl_reviews", "1 : N (MovieId)", 0, 0.8, 1, 0.3),
        ("rel_showtimes_bookedseats", "tbl_showtimes", "tbl_bookedseats", "1 : N (ShowtimeId)", 0.5, 1, 0.5, 0),
        ("rel_seats_bookedseats", "tbl_seats", "tbl_bookedseats", "1 : N (SeatId)", 1, 0.5, 0, 0.8),
        ("rel_users_bookings", "tbl_users", "tbl_bookings", "1 : N (UserId)", 1, 0.2, 0, 0.2),
        ("rel_showtimes_bookings", "tbl_showtimes", "tbl_bookings", "1 : N (ShowtimeId)", 1, 0.5, 0, 0.5),
        ("rel_bookings_bookedseats", "tbl_bookings", "tbl_bookedseats", "1 : N (BookingId)", 0, 0.7, 1, 0.3),
        ("rel_bookings_tickets", "tbl_bookings", "tbl_tickets", "1 : N (BookingId)", 0.5, 1, 0.5, 0),
        ("rel_bookedseats_tickets", "tbl_bookedseats", "tbl_tickets", "1 : 1 (BookedSeatId)", 1, 0.6, 0, 0.5),
        ("rel_bookings_bfi", "tbl_bookings", "tbl_bookingfooditems", "1 : N (BookingId)", 1, 0.5, 0, 0.3),
        ("rel_fooditems_bfi", "tbl_fooditems", "tbl_bookingfooditems", "1 : N (FoodItemId)", 0.5, 1, 0.5, 0),
    ]

def build_raw_mxgraphmodel():
    mxGraphModel = ET.Element("mxGraphModel", {
        "dx": "2200", "dy": "1400", "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "2200", "pageHeight": "1300",
        "background": "#FFFFFF", "math": "0", "shadow": "0"
    })
    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Tiêu đề biểu đồ - Tối giản, thanh lịch
    title = ET.SubElement(root, "mxCell", {
        "id": "title_banner",
        "value": "SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (DATABASE ERD - 14 BẢNG)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Helvetica;fontSize=18;fontStyle=1;fontColor=#000000;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(title, "mxGeometry", {"x": "550", "y": "15", "width": "900", "height": "35", "as": "geometry"})

    sub_title = ET.SubElement(root, "mxCell", {
        "id": "sub_title_banner",
        "value": "Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement) | MySQL 10.11 / MariaDB (Port 3306, utf8mb4)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Helvetica;fontSize=12;fontStyle=2;fontColor=#555555;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(sub_title, "mxGeometry", {"x": "550", "y": "45", "width": "900", "height": "25", "as": "geometry"})

    tables = get_tables_data()
    row_h = 24
    header_h = 28

    for tbl in tables:
        h = header_h + len(tbl["columns"]) * row_h
        table_style = (
            f"swimlane;fontStyle=1;align=center;verticalAlign=top;"
            f"childLayout=stackLayout;horizontal=1;startSize={header_h};"
            f"horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;"
            f"collapsible=1;marginBottom=0;whiteSpace=wrap;html=0;"
            f"fillColor={tbl['color']};fontColor={HEADER_TEXT_COLOR};strokeColor={BORDER_COLOR};"
            f"strokeWidth=1.5;fontSize=12;fontFamily=Helvetica;shadow=0;rounded=1;"
        )
        tbl_cell = ET.SubElement(root, "mxCell", {
            "id": tbl["id"], "value": tbl["name"], "style": table_style,
            "vertex": "1", "parent": "1"
        })
        ET.SubElement(tbl_cell, "mxGeometry", {
            "x": str(tbl["x"]), "y": str(tbl["y"]), "width": str(tbl["w"]), "height": str(h), "as": "geometry"
        })

        for idx, (col_name, col_type, is_pk, is_fk) in enumerate(tbl["columns"]):
            col_id = f"{tbl['id']}_{col_name.lower()}"
            prefix = "[PK] " if is_pk else "[FK] " if is_fk else "      "
            val = f"{prefix}{col_name} : {col_type}"
            bg = "#FFFFFF" if idx % 2 == 0 else BG_ROW_ALT
            font_color = "#000000" if is_pk else "#374151" if is_fk else "#1F2937"

            cell_style = (
                f"text;strokeColor=none;fillColor={bg};align=left;verticalAlign=middle;"
                f"spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;"
                f"points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=0;"
                f"fontColor={font_color};fontSize=11;fontFamily=Helvetica;"
            )
            c_elem = ET.SubElement(root, "mxCell", {
                "id": col_id, "value": val, "style": cell_style,
                "vertex": "1", "parent": tbl["id"]
            })
            ET.SubElement(c_elem, "mxGeometry", {
                "y": str(header_h + idx * row_h), "width": str(tbl["w"]), "height": str(row_h), "as": "geometry"
            })

    relations = get_relations_data()
    edge_style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;"
        f"strokeColor={LINE_COLOR};strokeWidth=1.5;fontFamily=Helvetica;fontSize=10;fontColor=#4B5563;"
        "startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;"
    )

    for edge_id, src, tgt, lbl, ex_x, ex_y, en_x, en_y in relations:
        edge = ET.SubElement(root, "mxCell", {
            "id": edge_id, "value": lbl,
            "style": f"{edge_style}exitX={ex_x};exitY={ex_y};entryX={en_x};entryY={en_y};",
            "edge": "1", "parent": "1", "source": src, "target": tgt
        })
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})

    # Legend tối giản
    legend = ET.SubElement(root, "mxCell", {
        "id": "legend",
        "value": "CHÚ THÍCH: [PK] Khóa chính (Primary Key) | [FK] Khóa ngoại (Foreign Key) | Ký hiệu quan hệ Crow's Foot: ||―< (1 : N)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=#D1D5DB;fillColor=#FFFFFF;fontFamily=Helvetica;fontSize=11;fontColor=#4B5563;rounded=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(legend, "mxGeometry", {"x": "600", "y": "1180", "width": "800", "height": "32", "as": "geometry"})

    return mxGraphModel

def compress_drawio_xml(raw_xml_string):
    encoded = urllib.parse.quote(raw_xml_string, safe='~()*!.\'')
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15, memLevel=8, strategy=0)
    deflated = compressor.compress(encoded.encode('utf-8')) + compressor.flush()
    return base64.b64encode(deflated).decode('utf-8')

def generate_drawio_files():
    model = build_raw_mxgraphmodel()
    raw_xml_str = ET.tostring(model, encoding='utf-8').decode('utf-8')

    # 1. CineManagement_Database_ERD.drawio (Native Base64 Deflate)
    compressed_data = compress_drawio_xml(raw_xml_str)
    native_mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-22T05:45:00.000Z",
        "agent": "Antigravity CineManagement",
        "version": "21.6.8",
        "type": "device"
    })
    diag = ET.SubElement(native_mxfile, "diagram", {
        "id": "CineManagement-ERD",
        "name": "Database ERD (14 Tables)"
    })
    diag.text = compressed_data

    tree_native = ET.ElementTree(native_mxfile)
    tree_native.write("CineManagement_Database_ERD.drawio", encoding="utf-8", xml_declaration=True)
    print("[1] Đã tạo file Draw.io tối giản chuẩn: CineManagement_Database_ERD.drawio")

    # 2. CineManagement_Database_ERD_plain.xml (Uncompressed XML)
    plain_mxfile = ET.Element("mxfile", {"host": "app.diagrams.net"})
    diag_plain = ET.SubElement(plain_mxfile, "diagram", {"name": "Database ERD", "id": "erd-14"})
    diag_plain.append(model)
    tree_plain = ET.ElementTree(plain_mxfile)
    ET.indent(tree_plain, space="  ")
    tree_plain.write("CineManagement_Database_ERD_plain.xml", encoding="utf-8", xml_declaration=True)
    print("[2] Đã tạo file XML thuần: CineManagement_Database_ERD_plain.xml")

    # 3. CineManagement_ERD_Viewer.html (Trình xem web tương tác trực tiếp)
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sơ đồ Database ERD - CineManagement (Draw.io Viewer)</title>
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
            min-height: 800px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (DATABASE ERD - 14 BẢNG)</h1>
        <p>Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement) | MySQL 10.11 / MariaDB</p>
    </div>
    <div class="viewer-card">
        <div class="mxgraph" style="max-width:100%;border:1px solid #E2E8F0;" data-mxgraph='{{"highlight":"#000000","nav":true,"resize":true,"toolbar":"zoom layers tags","edit":"_blank","xml":{json_xml_str()}}}'></div>
    </div>
</body>
</html>
"""
    with open("CineManagement_ERD_Viewer.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[3] Đã tạo file Trình xem Web: CineManagement_ERD_Viewer.html")

def json_xml_str():
    import json
    model = build_raw_mxgraphmodel()
    raw = ET.tostring(model, encoding='utf-8').decode('utf-8')
    return json.dumps(raw)

def generate_preview_image():
    # Tạo hình ảnh trực quan tối giản (Clean Neutral / Monochrome)
    fig, ax = plt.subplots(figsize=(24.0, 15.0), dpi=200)
    ax.set_xlim(0, 24.0)
    ax.set_ylim(0, 15.0)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title tối giản
    ax.text(12.0, 14.5, "SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (DATABASE ERD - 14 BẢNG)",
            ha='center', va='center', fontsize=20, fontweight='bold', color='#111827')
    ax.text(12.0, 14.1, "Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement) | MySQL 10.11 / MariaDB (Port 3306)",
            ha='center', va='center', fontsize=12.5, fontstyle='italic', color='#4B5563')

    tables = get_tables_data()
    sx = 23.0 / 2100.0
    sy = 13.0 / 1200.0

    table_boxes = {}

    for tbl in tables:
        mx = tbl["x"] * sx + 0.5
        my_top = 13.6 - (tbl["y"] * sy)
        mw = tbl["w"] * sx
        mh = (28 + len(tbl["columns"]) * 24) * sy
        my_bottom = my_top - mh

        table_boxes[tbl["id"]] = (mx, my_bottom, mw, mh, my_top)

        # Body background - Trắng, viền xám đen tối giản
        ax.add_patch(FancyBboxPatch((mx, my_bottom), mw, mh, boxstyle="round,pad=0.03,rounding_size=0.08",
                                    fc='#FFFFFF', ec=BORDER_COLOR, lw=1.5))
        # Header box - Xám đen #262626 thanh lịch
        header_h_mpl = 28 * sy
        ax.add_patch(FancyBboxPatch((mx, my_top - header_h_mpl), mw, header_h_mpl,
                                    boxstyle="round,pad=0.03,rounding_size=0.08",
                                    fc=HEADER_COLOR, ec=BORDER_COLOR, lw=1.5))
        ax.text(mx + mw/2, my_top - header_h_mpl/2, tbl["name"],
                ha='center', va='center', fontsize=11.5, fontweight='bold', color=HEADER_TEXT_COLOR)

        # Columns
        row_h_mpl = 24 * sy
        for idx, (col_name, col_type, is_pk, is_fk) in enumerate(tbl["columns"]):
            row_y = my_top - header_h_mpl - (idx + 0.5) * row_h_mpl
            prefix = "[PK] " if is_pk else "[FK] " if is_fk else "      "
            p_color = '#000000' if is_pk else '#374151' if is_fk else '#1F2937'
            weight = 'bold' if (is_pk or is_fk) else 'normal'

            # Row alternating bg
            if idx % 2 == 1:
                ax.add_patch(plt.Rectangle((mx + 0.04, row_y - row_h_mpl*0.45), mw - 0.08, row_h_mpl*0.9,
                                           fc=BG_ROW_ALT, ec='none'))

            ax.text(mx + 0.12, row_y, f"{prefix}{col_name}", fontsize=9.0, fontweight=weight, color=p_color, va='center')
            ax.text(mx + mw - 0.12, row_y, col_type, fontsize=8.0, fontstyle='italic', color=TEXT_MUTED, ha='right', va='center')

    # Draw relations
    relations = get_relations_data()
    for rel_id, src, tgt, lbl, ex_x, ex_y, en_x, en_y in relations:
        if src in table_boxes and tgt in table_boxes:
            b_src = table_boxes[src]
            b_tgt = table_boxes[tgt]
            p1 = (b_src[0] + ex_x * b_src[2], b_src[4] - ex_y * b_src[3])
            p2 = (b_tgt[0] + en_x * b_tgt[2], b_tgt[4] - en_y * b_tgt[3])

            mid_x = (p1[0] + p2[0]) / 2
            ax.plot([p1[0], mid_x, mid_x, p2[0]], [p1[1], p1[1], p2[1], p2[1]],
                    color=LINE_COLOR, lw=1.4, linestyle='-')
            ax.plot(p2[0], p2[1], marker='o', markersize=3.0, color=LINE_COLOR)

    # Legend tối giản
    ax.add_patch(FancyBboxPatch((4.5, 0.4), 15.0, 0.55, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc='#FFFFFF', ec='#D1D5DB', lw=1.0))
    ax.text(12.0, 0.67,
            "[PK] Khóa chính   |   [FK] Khóa ngoại   |   Quan hệ chuẩn Crow's Foot: ||―< (1 : N)   |   MySQL 10.11 utf8mb4",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#4B5563')

    out_img = os.path.join("diagrams", "drawio_erd_interface.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=200, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[4] Đã xuất ảnh giao diện Draw.io tối giản: {out_img}")

if __name__ == "__main__":
    generate_drawio_files()
    generate_preview_image()
