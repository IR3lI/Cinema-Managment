# -*- coding: utf-8 -*-
"""
Script tạo sơ đồ quan hệ thực thể (Database ERD - 14 Bảng) chuẩn định dạng draw.io (.drawio)
Dự án: Cinema Management System (CineManagement)
Mở được trực tiếp trên: draw.io, diagrams.net, VS Code Draw.io extension
"""

import xml.etree.ElementTree as ET
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_drawio_erd():
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-22T05:30:00.000Z",
        "agent": "Antigravity CineManagement Agent",
        "version": "21.6.8",
        "type": "device"
    })

    diagram = ET.SubElement(mxfile, "diagram", {
        "id": "CineManagement-Database-ERD",
        "name": "Database ERD (14 Tables)"
    })

    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "2200",
        "dy": "1400",
        "grid": "1",
        "gridSize": "10",
        "guides": "1",
        "tooltips": "1",
        "connect": "1",
        "arrows": "1",
        "fold": "1",
        "page": "1",
        "pageScale": "1",
        "pageWidth": "2500",
        "pageHeight": "1400",
        "background": "#F8FAFC",
        "math": "0",
        "shadow": "0"
    })

    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Tiêu đề biểu đồ
    title_cell = ET.SubElement(root, "mxCell", {
        "id": "title_banner",
        "value": "&lt;b style='font-size: 22px;'&gt;SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU (DATABASE ERD - 14 BẢNG)&lt;/b&gt;&lt;br&gt;&lt;span style='font-size: 13px; color: #64748B;'&gt;Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement) | MySQL 10.11 / MariaDB (Port 3306, utf8mb4)&lt;/span&gt;",
        "style": "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Helvetica;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(title_cell, "mxGeometry", {
        "x": "600",
        "y": "25",
        "width": "1200",
        "height": "50",
        "as": "geometry"
    })

    # Định nghĩa 14 bảng dữ liệu
    tables = [
        # Cột 1: Người dùng, Nhân viên, Đánh giá
        {
            "id": "tbl_users",
            "name": "AspNetUsers",
            "color": "#1E3A8A", # Deep Blue
            "x": 60, "y": 100, "w": 330,
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
            "id": "tbl_staffs",
            "name": "Staffs",
            "color": "#1E3A8A",
            "x": 60, "y": 420, "w": 330,
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
            "id": "tbl_reviews",
            "name": "Reviews",
            "color": "#1E3A8A",
            "x": 60, "y": 710, "w": 330,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("UserId", "VARCHAR(255)", False, True),
                ("MovieId", "INT", False, True),
                ("Rating", "INT", False, False),
                ("Comment", "TEXT", False, False),
                ("CreatedAt", "DATETIME", False, False),
            ]
        },

        # Cột 2: Phim, Thể loại, Phòng chiếu, Ghế
        {
            "id": "tbl_genres",
            "name": "Genres",
            "color": "#065F46", # Emerald
            "x": 480, "y": 100, "w": 320,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("Name", "VARCHAR(100)", False, False),
                ("Description", "TEXT", False, False),
            ]
        },
        {
            "id": "tbl_movies",
            "name": "Movies",
            "color": "#065F46",
            "x": 480, "y": 290, "w": 320,
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
            "id": "tbl_rooms",
            "name": "ScreeningRooms",
            "color": "#4338CA", # Indigo
            "x": 480, "y": 620, "w": 320,
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
            "id": "tbl_seats",
            "name": "Seats",
            "color": "#4338CA",
            "x": 480, "y": 910, "w": 320,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("RoomId", "INT", False, True),
                ("RowName", "VARCHAR(5)", False, False),
                ("SeatNumber", "INT", False, False),
                ("SeatType", "VARCHAR(50)", False, False),
            ]
        },

        # Cột 3: Suất chiếu & Khóa giữ ghế 10 phút
        {
            "id": "tbl_showtimes",
            "name": "Showtimes",
            "color": "#0891B2", # Cyan / Ocean
            "x": 890, "y": 100, "w": 340,
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
            "id": "tbl_bookedseats",
            "name": "BookedSeats (Hold 10m)",
            "color": "#0891B2",
            "x": 890, "y": 440, "w": 340,
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

        # Cột 4: Đơn đặt vé, Vé điện tử QR, Voucher
        {
            "id": "tbl_bookings",
            "name": "Bookings",
            "color": "#991B1B", # Crimson / Dark Red
            "x": 1330, "y": 100, "w": 340,
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
            "id": "tbl_tickets",
            "name": "Tickets (QR Code)",
            "color": "#991B1B",
            "x": 1330, "y": 480, "w": 340,
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
            "id": "tbl_vouchers",
            "name": "Vouchers",
            "color": "#991B1B",
            "x": 1330, "y": 800, "w": 340,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("Code", "VARCHAR(50)", False, False),
                ("DiscountPercent", "INT", False, False),
                ("MaxDiscountAmount", "DECIMAL(18,2)", False, False),
                ("IsActive", "TINYINT(1)", False, False),
            ]
        },

        # Cột 5: Bắp nước F&B
        {
            "id": "tbl_fooditems",
            "name": "FoodItems (F&B)",
            "color": "#B45309", # Amber / Orange
            "x": 1770, "y": 100, "w": 340,
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
            "id": "tbl_bookingfooditems",
            "name": "BookingFoodItems",
            "color": "#B45309",
            "x": 1770, "y": 420, "w": 340,
            "columns": [
                ("Id", "INT AUTO_INC", True, False),
                ("BookingId", "INT", False, True),
                ("FoodItemId", "INT", False, True),
                ("Quantity", "INT", False, False),
                ("UnitPrice", "DECIMAL(18,2)", False, False),
            ]
        }
    ]

    row_height = 26
    header_height = 30

    for tbl in tables:
        h = header_height + len(tbl["columns"]) * row_height
        table_style = (
            f"swimlane;fontStyle=1;align=center;verticalAlign=top;"
            f"childLayout=stackLayout;horizontal=1;startSize={header_height};"
            f"horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;"
            f"collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
            f"fillColor={tbl['color']};fontColor=#FFFFFF;strokeColor={tbl['color']};"
            f"strokeWidth=2;fontSize=13;fontFamily=Helvetica;shadow=1;rounded=1;"
        )

        tbl_cell = ET.SubElement(root, "mxCell", {
            "id": tbl["id"],
            "value": f"<b>{tbl['name']}</b>",
            "style": table_style,
            "vertex": "1",
            "parent": "1"
        })
        ET.SubElement(tbl_cell, "mxGeometry", {
            "x": str(tbl["x"]),
            "y": str(tbl["y"]),
            "width": str(tbl["w"]),
            "height": str(h),
            "as": "geometry"
        })

        for idx, (col_name, col_type, is_pk, is_fk) in enumerate(tbl["columns"]):
            col_id = f"{tbl['id']}_{col_name.lower()}"
            if is_pk:
                badge = "&lt;font color='#DC2626'&gt;&lt;b&gt;[PK]&lt;/b&gt;&lt;/font&gt; "
            elif is_fk:
                badge = "&lt;font color='#2563EB'&gt;&lt;b&gt;[FK]&lt;/b&gt;&lt;/font&gt; "
            else:
                badge = "&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp; "

            col_val = f"{badge}<b>{col_name}</b> : &lt;i style='color: #64748B;'&gt;{col_type}&lt;/i&gt;"
            bg_color = "#FFFFFF" if idx % 2 == 0 else "#F8FAFC"
            
            cell_style = (
                f"text;strokeColor=none;fillColor={bg_color};align=left;verticalAlign=middle;"
                f"spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;"
                f"points=[[0,0.5],[1,0.5]];portConstraint=eastwest;html=1;"
                f"fontColor=#0F172A;fontSize=11;fontFamily=Helvetica;"
            )

            c_elem = ET.SubElement(root, "mxCell", {
                "id": col_id,
                "value": col_val,
                "style": cell_style,
                "vertex": "1",
                "parent": tbl["id"]
            })
            ET.SubElement(c_elem, "mxGeometry", {
                "y": str(header_height + idx * row_height),
                "width": str(tbl["w"]),
                "height": str(row_height),
                "as": "geometry"
            })

    relations = [
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

    edge_style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;"
        "strokeColor=#334155;strokeWidth=2;fontFamily=Helvetica;fontSize=10;fontColor=#475569;"
        "startArrow=ERmandOne;startFill=0;endArrow=ERmany;endFill=0;"
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

    legend_box = ET.SubElement(root, "mxCell", {
        "id": "legend_box",
        "value": (
            "&lt;b style='font-size: 13px;'&gt;CHÚ THÍCH PHÂN HỆ VÀ CƠ CHẾ DỮ LIỆU:&lt;/b&gt;&lt;br&gt;"
            "&lt;span style='color: #1E3A8A;'&gt;■ Identity &amp; Users&lt;/span&gt; | "
            "&lt;span style='color: #065F46;'&gt;■ Movies &amp; Genres&lt;/span&gt; | "
            "&lt;span style='color: #4338CA;'&gt;■ Rooms &amp; Seats&lt;/span&gt; | "
            "&lt;span style='color: #0891B2;'&gt;■ Showtimes &amp; Hold 10m&lt;/span&gt; | "
            "&lt;span style='color: #991B1B;'&gt;■ Bookings &amp; Tickets QR&lt;/span&gt; | "
            "&lt;span style='color: #B45309;'&gt;■ Concessions F&amp;B&lt;/span&gt;&lt;br&gt;"
            "&lt;i style='color: #64748B;'&gt;• [PK]: Khóa chính | [FK]: Khóa ngoại | Ký hiệu quan hệ chuẩn Crow's Foot: ||―&amp;lt; (1 : N)&lt;/i&gt;"
        ),
        "style": "html=1;whiteSpace=wrap;rounded=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;align=center;verticalAlign=middle;shadow=0;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(legend_box, "mxGeometry", {
        "x": "480",
        "y": "1150",
        "width": "1190",
        "height": "65",
        "as": "geometry"
    })

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    
    output_path = "CineManagement_Database_ERD.drawio"
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"[OK] Đã tạo thành công file Draw.io: {output_path}")

if __name__ == "__main__":
    build_drawio_erd()
