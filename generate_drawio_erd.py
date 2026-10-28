# -*- coding: utf-8 -*-
"""
Script tao so do ERD chuan nhat tren Draw.io:
- Su dung cau truc Container 2-Box (Header Box + Body Box)
- Moi dong thuoc tinh xuong hang bang ky tu xuong dong chuan Draw.io (&#xa;)
- Font chu ky thuat Consolas, can le trai spacingLeft=10
- Khong dung stackLayout hay cac thuoc tinh layout de gay loi tran man hinh
- 1 Mau duy nhat: Header #1E293B, vien #334155, nen trang #FFFFFF
"""

import xml.etree.ElementTree as ET
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_perfect_erd():
    HEADER_BG = "#1E293B"       # Mau duy nhat cho header tat ca cac bang
    HEADER_TEXT = "#FFFFFF"     # Chu trang
    BODY_BG = "#FFFFFF"         # Nen trang
    BODY_TEXT = "#0F172A"       # Chu mau than toi
    BORDER_COLOR = "#334155"    # Duong vien
    LINE_COLOR = "#334155"      # Duong quan he

    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-29T06:10:00.000Z",
        "agent": "Antigravity Draw.io Generator",
        "version": "21.6.8",
        "type": "device"
    })

    diagram = ET.SubElement(mxfile, "diagram", {
        "id": "CineManagement-ERD-Perfect",
        "name": "Database ERD (16 Tables 3NF)"
    })

    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "2400",
        "dy": "1500",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "2600",
        "pageHeight": "1600",
        "background": "#FFFFFF",
        "math": "0",
        "shadow": "0"
    })

    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Tieu de tong the
    title_cell = ET.SubElement(root, "mxCell", {
        "id": "title_banner",
        "value": "SƠ ĐỒ THỰC THỂ CƠ SỞ DỮ LIỆU (DATABASE ERD - 16 BẢNG 3NF)\nHệ thống Quản lý Chuỗi Rạp Chiếu Phim Tập Trung (CineManagement) - MariaDB / MySQL",
        "style": "text;align=center;verticalAlign=middle;resizable=0;points=[];strokeColor=none;fillColor=none;fontFamily=Helvetica;fontSize=15;fontStyle=1;fontColor=#1E293B;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(title_cell, "mxGeometry", {
        "x": "600",
        "y": "20",
        "width": "1200",
        "height": "45",
        "as": "geometry"
    })

    tables = [
        # Cot 1
        {
            "id": "tbl_cinemas",
            "name": "cinemas",
            "x": 60, "y": 80, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "      CinemaCode : VARCHAR(20)",
                "      Name : VARCHAR(150)",
                "      Address : VARCHAR(255)",
                "      City : VARCHAR(100)",
                "      Hotline : VARCHAR(20)",
                "      TotalRooms : INT",
                "      IsActive : TINYINT(1)"
            ]
        },
        {
            "id": "tbl_screeningrooms",
            "name": "screeningrooms",
            "x": 60, "y": 350, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  CinemaId : INT",
                "      RoomName : VARCHAR(100)",
                "      RoomType : VARCHAR(50)",
                "      TotalRows : INT",
                "      TotalColumns : INT",
                "      TotalSeats : INT",
                "      IsActive : TINYINT(1)"
            ]
        },
        {
            "id": "tbl_seattypes",
            "name": "seattypes",
            "x": 60, "y": 630, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "      TypeCode : VARCHAR(20)",
                "      TypeName : VARCHAR(50)",
                "      ColorHex : VARCHAR(10)",
                "      Surcharge : DECIMAL(18,2)",
                "      ColSpan : INT",
                "      IsActive : TINYINT(1)"
            ]
        },
        {
            "id": "tbl_seats",
            "name": "seats",
            "x": 60, "y": 890, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  RoomId : INT",
                "[FK]  SeatTypeId : INT",
                "      GridRow : INT",
                "      GridCol : INT",
                "      RowLabel : VARCHAR(5)",
                "      SeatNumber : INT",
                "      ColSpan : INT",
                "      IsActive : TINYINT(1)"
            ]
        },

        # Cot 2
        {
            "id": "tbl_genres",
            "name": "genres",
            "x": 440, "y": 80, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "      Name : VARCHAR(100)",
                "      Description : TEXT"
            ]
        },
        {
            "id": "tbl_movies",
            "name": "movies",
            "x": 440, "y": 240, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  GenreId : INT",
                "      Title : VARCHAR(250)",
                "      DurationMinutes : INT",
                "      ReleaseDate : DATETIME",
                "      EndDate : DATETIME",
                "      PosterUrl : VARCHAR(500)",
                "      Rating : DECIMAL(3,1)",
                "      AgeRating : VARCHAR(10)"
            ]
        },
        {
            "id": "tbl_showtimes",
            "name": "showtimes",
            "x": 440, "y": 550, "w": 280,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  MovieId : INT",
                "[FK]  RoomId : INT",
                "      StartTime : DATETIME",
                "      EndTime : DATETIME",
                "      Format : VARCHAR(50)",
                "      BasePrice : DECIMAL(18,2)",
                "      Status : VARCHAR(50)"
            ]
        },
        {
            "id": "tbl_showtimeseats",
            "name": "showtimeseats",
            "x": 440, "y": 840, "w": 300,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  ShowtimeId : INT",
                "[FK]  SeatId : INT",
                "      Status : INT (0:Avail, 1:Held, 2:Res)",
                "      Price : DECIMAL(18,2)",
                "      HeldByUserId : VARCHAR(255)",
                "      HoldExpiresAt : DATETIME",
                "      Version : INT [ConcurrencyCheck]",
                "      UpdatedAt : DATETIME"
            ]
        },

        # Cot 3
        {
            "id": "tbl_aspnetroles",
            "name": "aspnetroles",
            "x": 840, "y": 80, "w": 290,
            "columns": [
                "[PK]  Id : VARCHAR(255)",
                "      Name : VARCHAR(256)",
                "      NormalizedName : VARCHAR(256)"
            ]
        },
        {
            "id": "tbl_aspnetusers",
            "name": "aspnetusers",
            "x": 840, "y": 230, "w": 290,
            "columns": [
                "[PK]  Id : VARCHAR(255)",
                "      UserName : VARCHAR(256)",
                "      Email : VARCHAR(256)",
                "      FullName : VARCHAR(150)",
                "      PhoneNumber : VARCHAR(20)",
                "      PasswordHash : LONGTEXT",
                "      CreatedAt : DATETIME"
            ]
        },
        {
            "id": "tbl_bookings",
            "name": "bookings",
            "x": 840, "y": 500, "w": 290,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "      BookingCode : VARCHAR(50)",
                "[FK]  UserId : VARCHAR(255)",
                "[FK]  ShowtimeId : INT",
                "      TotalAmount : DECIMAL(18,2)",
                "      FinalAmount : DECIMAL(18,2)",
                "      Status : VARCHAR(50)",
                "      PaymentStatus : VARCHAR(50)",
                "      CreatedAt : DATETIME"
            ]
        },
        {
            "id": "tbl_tickets",
            "name": "tickets",
            "x": 840, "y": 810, "w": 290,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  BookingId : INT",
                "[FK]  ShowtimeSeatId : INT",
                "      TicketCode : VARCHAR(50)",
                "      Price : DECIMAL(18,2)",
                "      IsPrinted : TINYINT(1) [Guard]",
                "      PrintedAt : DATETIME",
                "      PrintedByUserId : VARCHAR(255)",
                "      ThermalReceiptCode : VARCHAR(50)",
                "      QrPayload : VARCHAR(255)"
            ]
        },

        # Cot 4
        {
            "id": "tbl_fooditems",
            "name": "fooditems / concessions",
            "x": 1230, "y": 80, "w": 290,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "      Name : VARCHAR(150)",
                "      Description : TEXT",
                "      UnitPrice : DECIMAL(18,2)",
                "      ImageUrl : VARCHAR(500)",
                "      IsActive : TINYINT(1)"
            ]
        },
        {
            "id": "tbl_bookingconcessions",
            "name": "bookingconcessions",
            "x": 1230, "y": 310, "w": 290,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  BookingId : INT",
                "[FK]  ConcessionId : INT",
                "      Quantity : INT",
                "      UnitPrice : DECIMAL(18,2)",
                "      TotalPrice : DECIMAL(18,2)"
            ]
        },
        {
            "id": "tbl_payments",
            "name": "payments",
            "x": 1230, "y": 550, "w": 290,
            "columns": [
                "[PK]  Id : INT AUTO_INC",
                "[FK]  BookingId : INT",
                "      TransactionCode : VARCHAR(100)",
                "      PaymentMethod : VARCHAR(50)",
                "      Amount : DECIMAL(18,2)",
                "      Status : VARCHAR(50)",
                "      PaidAt : DATETIME"
            ]
        },
        {
            "id": "tbl_outboxmessages",
            "name": "outboxmessages",
            "x": 1230, "y": 810, "w": 290,
            "columns": [
                "[PK]  Id : VARCHAR(36)",
                "      Type : VARCHAR(100)",
                "      Payload : LONGTEXT",
                "      IsProcessed : TINYINT(1)",
                "      RetryCount : INT",
                "      CreatedAt : DATETIME",
                "      ProcessedAt : DATETIME",
                "      ErrorMessage : TEXT"
            ]
        }
    ]

    header_height = 28
    line_height = 19

    for tbl in tables:
        body_text = "\n".join(tbl["columns"])
        body_height = len(tbl["columns"]) * line_height + 12

        # 1. Header Box
        h_cell = ET.SubElement(root, "mxCell", {
            "id": f"{tbl['id']}_hdr",
            "value": tbl["name"],
            "style": (
                f"rounded=0;whiteSpace=wrap;html=0;fillColor={HEADER_BG};fontColor={HEADER_TEXT};"
                f"strokeColor={BORDER_COLOR};strokeWidth=1.5;fontStyle=1;fontSize=12;fontFamily=Helvetica;"
                f"align=center;verticalAlign=middle;"
            ),
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(h_cell, "mxGeometry", {
            "x": str(tbl["x"]),
            "y": str(tbl["y"]),
            "width": str(tbl["w"]),
            "height": str(header_height),
            "as": "geometry"
        })

        # 2. Body Box
        b_cell = ET.SubElement(root, "mxCell", {
            "id": tbl["id"],
            "value": body_text,
            "style": (
                f"rounded=0;whiteSpace=wrap;html=0;fillColor={BODY_BG};fontColor={BODY_TEXT};"
                f"strokeColor={BORDER_COLOR};strokeWidth=1.5;fontSize=10.5;fontFamily=Consolas;"
                f"align=left;verticalAlign=top;spacingLeft=10;spacingRight=6;spacingTop=6;spacingBottom=6;"
            ),
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(b_cell, "mxGeometry", {
            "x": str(tbl["x"]),
            "y": str(tbl["y"] + header_height),
            "width": str(tbl["w"]),
            "height": str(body_height),
            "as": "geometry"
        })

    # Quan he giua cac bang
    relations = [
        ("rel_cinemas_rooms", "tbl_cinemas", "tbl_screeningrooms_hdr", "1 : N (CinemaId)", 0.5, 1, 0.5, 0),
        ("rel_rooms_seats", "tbl_screeningrooms", "tbl_seats_hdr", "1 : N (RoomId)", 0.5, 1, 0.5, 0),
        ("rel_types_seats", "tbl_seattypes", "tbl_seats_hdr", "1 : N (SeatTypeId)", 0.5, 1, 0.5, 0),
        ("rel_genres_movies", "tbl_genres", "tbl_movies_hdr", "1 : N (GenreId)", 0.5, 1, 0.5, 0),
        ("rel_movies_showtimes", "tbl_movies", "tbl_showtimes_hdr", "1 : N (MovieId)", 0.5, 1, 0.5, 0),
        ("rel_rooms_showtimes", "tbl_screeningrooms", "tbl_showtimes_hdr", "1 : N (RoomId)", 1, 0.5, 0, 0.3),
        ("rel_showtimes_seats", "tbl_showtimes", "tbl_showtimeseats_hdr", "1 : N (ShowtimeId)", 0.5, 1, 0.5, 0),
        ("rel_seats_showtimeseats", "tbl_seats", "tbl_showtimeseats_hdr", "1 : N (SeatId)", 1, 0.5, 0, 0.5),
        ("rel_roles_users", "tbl_aspnetroles", "tbl_aspnetusers_hdr", "N : N", 0.5, 1, 0.5, 0),
        ("rel_users_bookings", "tbl_aspnetusers", "tbl_bookings_hdr", "1 : N (UserId)", 0.5, 1, 0.5, 0),
        ("rel_showtimes_bookings", "tbl_showtimes", "tbl_bookings_hdr", "1 : N (ShowtimeId)", 1, 0.5, 0, 0.3),
        ("rel_bookings_tickets", "tbl_bookings", "tbl_tickets_hdr", "1 : N (BookingId)", 0.5, 1, 0.5, 0),
        ("rel_showtimeseats_tickets", "tbl_showtimeseats", "tbl_tickets_hdr", "1 : 1", 1, 0.5, 0, 0.5),
        ("rel_food_concessions", "tbl_fooditems", "tbl_bookingconcessions_hdr", "1 : N (ConcessionId)", 0.5, 1, 0.5, 0),
        ("rel_bookings_concessions", "tbl_bookings", "tbl_bookingconcessions_hdr", "1 : N (BookingId)", 1, 0.3, 0, 0.5),
        ("rel_bookings_payments", "tbl_bookings", "tbl_payments_hdr", "1 : N (BookingId)", 1, 0.6, 0, 0.5),
        ("rel_bookings_outbox", "tbl_bookings", "tbl_outboxmessages_hdr", "1 : N (BookingId)", 1, 0.8, 0, 0.3),
    ]

    edge_style = (
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=0;"
        f"strokeColor={LINE_COLOR};strokeWidth=1.5;fontFamily=Helvetica;fontSize=10;fontColor=#000000;"
        f"startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;"
    )

    for edge_id, src, tgt, lbl, ex_x, ex_y, en_x, en_y in relations:
        edge = ET.SubElement(root, "mxCell", {
            "id": edge_id,
            "value": lbl,
            "style": f"{edge_style}exitX={ex_x};exitY={ex_y};entryX={en_x};entryY={en_y};",
            "edge": "1",
            "parent": "1",
            "source": src,
            "target": tgt
        })
        ET.SubElement(edge, "mxGeometry", {
            "relative": "1",
            "as": "geometry"
        })

    tree = ET.ElementTree(mxfile)
    output_drawio = "../CineManagement_Database_ERD.drawio"
    tree.write(output_drawio, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Perfect Clean ERD generated: {output_drawio}")

    # Ghi ra tep Viewer HTML
    xml_str = ET.tostring(mxfile, encoding="utf-8").decode("utf-8")
    viewer_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>CineManagement - Database ERD 3NF (Perfect Monochrome)</title>
    <script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; background-color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        .header {{ background: #1E293B; color: #FFFFFF; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; }}
        .btn {{ background: #3B82F6; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-size: 13px; font-weight: bold; }}
        .container {{ width: 100vw; height: calc(100vh - 60px); overflow: hidden; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <span style="font-size: 16px; font-weight: 600;">CineManagement - Database ERD 3NF (16 Bảng - Chuẩn Kỹ Thuật Đơn Sắc)</span>
            <span style="font-size: 12px; color: #94A3B8; margin-left: 12px;">MariaDB 10.11 / MySQL | Port 3306 & 3307</span>
        </div>
        <a class="btn" href="https://app.diagrams.net/#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FIR3lI%2FCinema-Managment%2Fmain%2FCineManagement_Database_ERD.drawio" target="_blank">Mở trên Diagrams.net ↗</a>
    </div>
    <div class="container">
        <div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{xml_str.replace('"', '&quot;')}"></div>
    </div>
</body>
</html>"""
    with open("../CineManagement_ERD_Viewer.html", "w", encoding="utf-8") as f:
        f.write(viewer_html)
    print("[OK] Perfect Viewer HTML generated: ../CineManagement_ERD_Viewer.html")

if __name__ == '__main__':
    build_perfect_erd()
