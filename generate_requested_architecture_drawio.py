# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import xml.dom.minidom

def create_architecture_drawio():
    root = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-29T04:05:00.000Z",
        "agent": "Antigravity Architecture Generator",
        "version": "21.6.8",
        "type": "device"
    })
    diagram = ET.SubElement(root, "diagram", {
        "id": "CineManagement-Arch",
        "name": "CineManagement Architecture"
    })
    
    model = ET.SubElement(diagram, "mxGraphModel", {
        "dx": "1400", "dy": "900", "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1",
        "pageWidth": "1600", "pageHeight": "1100",
        "background": "#F8FAFC", "math": "0", "shadow": "0"
    })
    
    mx_root = ET.SubElement(model, "root")
    ET.SubElement(mx_root, "mxCell", {"id": "0"})
    ET.SubElement(mx_root, "mxCell", {"id": "1", "parent": "0"})

    # Title
    title = ET.SubElement(mx_root, "mxCell", {
        "id": "title",
        "value": "&lt;b style=&quot;font-size: 20px;&quot;&gt;CINEMANAGEMENT - SYSTEM ARCHITECTURE &amp; COMPONENT FLOW&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;color: #64748B;&quot;&gt;5-Tier Architecture: Client -> ASP.NET Core 10 Web App -> SignalR / Outbox Worker -> MariaDB (cinema_db)&lt;/span&gt;",
        "style": "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(title, "mxGeometry", {"x": "350", "y": "20", "width": "900", "height": "50", "as": "geometry"})

    # ================= TIER 1: CLIENTS =================
    t1_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier1_box",
        "value": "&lt;b&gt;TIER 1: CLIENT PRESENTATION LAYER&lt;/b&gt;",
        "style": "swimlane;fontStyle=1;align=left;spacingLeft=15;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;rounded=1;arcSize=6;fillColor=#FFFFFF;strokeColor=#94A3B8;strokeWidth=2;shadow=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t1_box, "mxGeometry", {"x": "60", "y": "100", "width": "300", "height": "650", "as": "geometry"})

    client_customer = ET.SubElement(mx_root, "mxCell", {
        "id": "client_customer",
        "value": "&lt;b style=&quot;font-size: 14px; color: #0284C7;&quot;&gt;Customer Web Portal&lt;/b&gt;&lt;br&gt;&lt;br&gt;• Razor Pages + Bootstrap 5&lt;br&gt;• 2D CSS Grid Seat Map Matrix&lt;br&gt;• SignalR JavaScript WebSockets&lt;br&gt;• QR Code E-Ticket Viewer",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F9FF;strokeColor=#0284C7;strokeWidth=1.5;align=left;spacingLeft=15;shadow=0;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(client_customer, "mxGeometry", {"x": "80", "y": "150", "width": "260", "height": "160", "as": "geometry"})

    client_staff = ET.SubElement(mx_root, "mxCell", {
        "id": "client_staff",
        "value": "&lt;b style=&quot;font-size: 14px; color: #16A34A;&quot;&gt;Staff Box Office POS Console&lt;/b&gt;&lt;br&gt;&lt;br&gt;• Quầy vé &amp; FnB Upsell (/Counter)&lt;br&gt;• html5-qrcode Camera Scanner&lt;br&gt;• Máy in nhiệt K80 (80mm Thermal)&lt;br&gt;• Chống in vé lậu (Anti-Reprint Guard)",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#16A34A;strokeWidth=1.5;align=left;spacingLeft=15;shadow=0;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(client_staff, "mxGeometry", {"x": "80", "y": "340", "width": "260", "height": "160", "as": "geometry"})

    client_admin = ET.SubElement(mx_root, "mxCell", {
        "id": "client_admin",
        "value": "&lt;b style=&quot;font-size: 14px; color: #D97706;&quot;&gt;Admin Management Studio&lt;/b&gt;&lt;br&gt;&lt;br&gt;• Visual Seat Layout Builder Studio&lt;br&gt;• Cấu hình ma trận hàng/cột &amp; hành lang&lt;br&gt;• Điều phối phim, suất chiếu, phòng&lt;br&gt;• Báo cáo doanh thu &amp; Audit Logs",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#D97706;strokeWidth=1.5;align=left;spacingLeft=15;shadow=0;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(client_admin, "mxGeometry", {"x": "80", "y": "530", "width": "260", "height": "180", "as": "geometry"})

    # ================= TIER 2: ASP.NET CORE 10 APP =================
    t2_box = ET.SubElement(mx_root, "mxCell", {
        "id": "tier2_box",
        "value": "&lt;b&gt;TIER 2 &amp; 3: ASP.NET CORE 10 WEB APPLICATION &amp; BACKGROUND WORKERS&lt;/b&gt;",
        "style": "swimlane;fontStyle=1;align=left;spacingLeft=15;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;rounded=1;arcSize=6;fillColor=#FFFFFF;strokeColor=#6366F1;strokeWidth=2;shadow=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t2_box, "mxGeometry", {"x": "430", "y": "100", "width": "620", "height": "650", "as": "geometry"})

    # Sub-containers in App
    controllers_box = ET.SubElement(mx_root, "mxCell", {
        "id": "controllers_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #4338CA;&quot;&gt;Presentation &amp; API Controllers&lt;/b&gt;&lt;br&gt;&lt;br&gt;• BookingController (/Booking/SelectSeat, /Checkout)&lt;br&gt;• CounterController (/Counter/Index, /PrintThermalTicket)&lt;br&gt;• ScreeningRoomController (/ScreeningRoom/LayoutBuilder)&lt;br&gt;• AccountController (ASP.NET Core Identity RBAC)",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEF2FF;strokeColor=#6366F1;strokeWidth=1.5;align=left;spacingLeft=15;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(controllers_box, "mxGeometry", {"x": "450", "y": "150", "width": "580", "height": "110", "as": "geometry"})

    services_box = ET.SubElement(mx_root, "mxCell", {
        "id": "services_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #059669;&quot;&gt;Business Logic &amp; Concurrency Control Engine&lt;/b&gt;&lt;br&gt;&lt;br&gt;• &lt;b&gt;BookingService&lt;/b&gt;: HoldSeatAsync, ReleaseSeatAsync (IsolationLevel.Serializable)&lt;br&gt;• &lt;b&gt;PaymentService&lt;/b&gt;: ConfirmPaymentAsync, Outbox Message Event Emission&lt;br&gt;• &lt;b&gt;Dual-Concurrency Engine&lt;/b&gt;: Pessimistic DB Locks + Optimistic Version Check (ss.Version++)&lt;br&gt;• &lt;b&gt;SeatLayoutStudio&lt;/b&gt;: Matrix calculation, Sweetbox ColSpan=2 Aisle Guard",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#ECFDF5;strokeColor=#10B981;strokeWidth=1.5;align=left;spacingLeft=15;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(services_box, "mxGeometry", {"x": "450", "y": "280", "width": "580", "height": "130", "as": "geometry"})

    signalr_box = ET.SubElement(mx_root, "mxCell", {
        "id": "signalr_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #7C3AED;&quot;&gt;SignalR Real-Time WebSockets Hub&lt;/b&gt;&lt;br&gt;&lt;br&gt;• &lt;b&gt;SeatBookingHub (/hubs/seat)&lt;/b&gt;&lt;br&gt;• Grouping theo ShowtimeId: Clients.Group(showtime_id)&lt;br&gt;• Real-time Broadcast: &lt;i&gt;SeatStatusChanged&lt;/i&gt; (&lt; 50ms latency)&lt;br&gt;• Đồng bộ tức thì Available / Held / Reserved",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F3FF;strokeColor=#8B5CF6;strokeWidth=1.5;align=left;spacingLeft=15;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(signalr_box, "mxGeometry", {"x": "450", "y": "430", "width": "280", "height": "150", "as": "geometry"})

    workers_box = ET.SubElement(mx_root, "mxCell", {
        "id": "workers_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #B45309;&quot;&gt;Hosted Background Services&lt;/b&gt;&lt;br&gt;&lt;br&gt;• &lt;b&gt;OutboxMessageWorker&lt;/b&gt;:&lt;br&gt;  - Polling bảng outboxmessages mỗi 5s&lt;br&gt;  - Gửi Email vé điện tử qua SMTP Gmail&lt;br&gt;  - Zero Email Loss Guarantee&lt;br&gt;• &lt;b&gt;SeatHoldTimeoutWorker&lt;/b&gt;:&lt;br&gt;  - Giải phóng ghế giữ tạm quá 5 phút&lt;br&gt;  - Kích hoạt SignalR broadcast ghế trống",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFBEB;strokeColor=#F59E0B;strokeWidth=1.5;align=left;spacingLeft=15;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(workers_box, "mxGeometry", {"x": "750", "y": "430", "width": "280", "height": "150", "as": "geometry"})

    # EF Core DbContext
    dbcontext_box = ET.SubElement(mx_root, "mxCell", {
        "id": "dbcontext_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #1E293B;&quot;&gt;Data Access Layer: ApplicationDbContext (EF Core 10)&lt;/b&gt;&lt;br&gt;Pomelo MySQL Provider • Connection Pooling • ACID Transactions • IdentityDbContext",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#64748B;strokeWidth=1.5;align=center;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(dbcontext_box, "mxGeometry", {"x": "450", "y": "610", "width": "580", "height": "60", "as": "geometry"})

    # ================= TIER 4: DATABASE (MARIADB) =================
    t4_box = ET.SubElement(mx_root, "mxCell", {
        "id": "t4_box",
        "value": "&lt;b&gt;TIER 4: DATABASE &amp; MESSAGING PERSISTENCE&lt;/b&gt;",
        "style": "swimlane;fontStyle=1;align=left;spacingLeft=15;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;rounded=1;arcSize=6;fillColor=#FFFFFF;strokeColor=#0EA5E9;strokeWidth=2;shadow=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(t4_box, "mxGeometry", {"x": "1140", "y": "100", "width": "380", "height": "650", "as": "geometry"})

    mariadb_box = ET.SubElement(mx_root, "mxCell", {
        "id": "mariadb_box",
        "value": "&lt;b style=&quot;font-size: 15px; color: #0369A1;&quot;&gt;MariaDB 10.11 InnoDB Server&lt;/b&gt;&lt;br&gt;&lt;span style=&quot;color: #64748B;&quot;&gt;Port 3306 • Database: cinema_db&lt;/span&gt;&lt;br&gt;&lt;br&gt;&lt;b&gt;Core Schema Tables (3NF):&lt;/b&gt;&lt;br&gt;• &lt;b&gt;cinemas&lt;/b&gt; (3 cụm rạp: CS-QT, CS-HBT, CS-BD)&lt;br&gt;• &lt;b&gt;screeningrooms&lt;/b&gt; (Grid ma trận hàng &amp; cột)&lt;br&gt;• &lt;b&gt;seattypes&lt;/b&gt; (Standard, VIP, Couple Sweetbox)&lt;br&gt;• &lt;b&gt;seats&lt;/b&gt; (GridRow, GridCol, ColSpan, RowLabel)&lt;br&gt;• &lt;b&gt;showtimes&lt;/b&gt; (210 suất chiếu đã seed)&lt;br&gt;• &lt;b&gt;showtimeseats&lt;/b&gt; (&lt;b style=&quot;color:#0284C7;&quot;&gt;31,806 bản ghi&lt;/b&gt;, Version concurrency)&lt;br&gt;• &lt;b&gt;bookings&lt;/b&gt; &amp; &lt;b&gt;bookingconcessions&lt;/b&gt;&lt;br&gt;• &lt;b&gt;tickets&lt;/b&gt; (IsPrinted thermal flag, QrPayload)&lt;br&gt;• &lt;b&gt;outboxmessages&lt;/b&gt; (Transactional Outbox events)&lt;br&gt;• &lt;b&gt;payments&lt;/b&gt; &amp; &lt;b&gt;aspnetusers&lt;/b&gt;",
        "style": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#E0F2FE;strokeColor=#0284C7;strokeWidth=1.5;align=left;spacingLeft=25;shadow=0;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(mariadb_box, "mxGeometry", {"x": "1165", "y": "150", "width": "330", "height": "390", "as": "geometry"})

    # External services
    smtp_box = ET.SubElement(mx_root, "mxCell", {
        "id": "smtp_box",
        "value": "&lt;b style=&quot;font-size: 13px; color: #EA4335;&quot;&gt;Google SMTP Mail Server&lt;/b&gt;&lt;br&gt;smtp.gmail.com:587 (TLS/SSL)&lt;br&gt;Nhận dispatch từ OutboxWorker",
        "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF2F2;strokeColor=#EF4444;strokeWidth=1.5;align=center;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(smtp_box, "mxGeometry", {"x": "1165", "y": "570", "width": "330", "height": "80", "as": "geometry"})

    # ================= CONNECTORS =================
    def add_edge(edge_id, source_id, target_id, label, style=""):
        default_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#475569;strokeWidth=1.5;fontSize=11;"
        edge = ET.SubElement(mx_root, "mxCell", {
            "id": edge_id,
            "value": label,
            "style": default_style + style,
            "edge": "1",
            "source": source_id,
            "target": target_id,
            "parent": "1"
        })
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})

    # Client -> Controllers
    add_edge("edge_c1", "client_customer", "controllers_box", "HTTP POST / Hold / Pay", "")
    add_edge("edge_c2", "client_staff", "controllers_box", "POS QR / In vé K80", "")
    add_edge("edge_c3", "client_admin", "controllers_box", "Save Layout Studio", "")

    # Client <-> SignalR
    add_edge("edge_ws", "signalr_box", "client_customer", "WebSockets Real-time Broadcast", "dashed=1;strokeColor=#7C3AED;strokeWidth=2;")
    add_edge("edge_ws2", "signalr_box", "client_staff", "WebSockets Real-time", "dashed=1;strokeColor=#7C3AED;")

    # Controllers -> Services
    add_edge("edge_c_s", "controllers_box", "services_box", "Call Business Services", "")

    # Services -> SignalR
    add_edge("edge_s_hub", "services_box", "signalr_box", "Trigger State Change", "strokeColor=#7C3AED;")

    # Services -> DbContext
    add_edge("edge_s_db", "services_box", "dbcontext_box", "Transaction (Serializable)", "strokeColor=#059669;strokeWidth=2;")

    # DbContext -> MariaDB
    add_edge("edge_db_maria", "dbcontext_box", "mariadb_box", "SQL Queries & Commits", "strokeColor=#0284C7;strokeWidth=2;")

    # Workers -> MariaDB & SMTP
    add_edge("edge_w_maria", "workers_box", "mariadb_box", "Poll outboxmessages (5s)", "strokeColor=#B45309;dashed=1;")
    add_edge("edge_w_smtp", "workers_box", "smtp_box", "Send E-Ticket Mail", "strokeColor=#EA4335;strokeWidth=2;")
    add_edge("edge_w_hub", "workers_box", "signalr_box", "Timeout Seat Release", "strokeColor=#F59E0B;dashed=1;")

    # Format XML nicely
    xml_str = ET.tostring(root, encoding="utf-8")
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")

    output_path = r"c:\Users\admin\Documents\GitHub\Cinema-Managment\CineManagement_Architecture.drawio"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    create_architecture_drawio()
