# -*- coding: utf-8 -*-
"""
Script tạo Biểu đồ phân rã chức năng (Functional Decomposition Diagram - FDD / BFD)
chuẩn định dạng draw.io (.drawio) và ảnh minh họa cho dự án CineManagement.
Phong cách tối giản, chuẩn kỹ thuật (Minimalist / Clean Monochrome).
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

# Màu sắc tối giản, sang trọng
COLOR_ROOT = "#1E293B"      # Slate đậm cho gốc hệ thống
COLOR_MODULE = "#334155"    # Slate vừa cho 5 phân hệ cấp 1
COLOR_LEAF_BG = "#FFFFFF"   # Trắng cho các chức năng lá cấp 2
COLOR_LEAF_BORDER = "#475569" # Viền xám mảnh
COLOR_LINE = "#475569"      # Đường rẽ nhánh cây
TEXT_WHITE = "#FFFFFF"
TEXT_DARK = "#0F172A"

def get_bfd_data():
    return {
        "root": {
            "id": "node_root",
            "name": "HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM (CINEMANAGEMENT)",
            "x": 830, "y": 40, "w": 500, "h": 50
        },
        "modules": [
            {
                "id": "mod_1",
                "code": "1.0",
                "name": "QUẢN TRỊ NGƯỜI DÙNG & BẢO MẬT",
                "x": 40, "y": 160, "w": 380, "h": 46,
                "functions": [
                    ("fn_1_1", "1.1 Đăng ký & Đăng nhập hệ thống (RBAC)"),
                    ("fn_1_2", "1.2 Quản lý hồ sơ cá nhân & Đổi mật khẩu"),
                    ("fn_1_3", "1.3 Cấp & Quản lý tài khoản nhân viên (Staff)"),
                    ("fn_1_4", "1.4 Phân quyền bảo mật & Chặn URL trái phép (403)")
                ]
            },
            {
                "id": "mod_2",
                "code": "2.0",
                "name": "QUẢN LÝ PHIM & PHÒNG CHIẾU",
                "x": 460, "y": 160, "w": 380, "h": 46,
                "functions": [
                    ("fn_2_1", "2.1 Quản lý phim, 15 poster & trailer YouTube"),
                    ("fn_2_2", "2.2 Cấu hình phòng chiếu & ma trận ghế ngồi"),
                    ("fn_2_3", "2.3 Lập lịch suất chiếu chống trùng lặp phòng"),
                    ("fn_2_4", "2.4 Tra cứu, tìm kiếm & lọc phim theo thể loại")
                ]
            },
            {
                "id": "mod_3",
                "code": "3.0",
                "name": "ĐẶT VÉ & GIỮ GHẾ THỜI GIAN THỰC",
                "x": 880, "y": 160, "w": 380, "h": 46,
                "functions": [
                    ("fn_3_1", "3.1 Chọn ghế trực quan trên sơ đồ phòng chiếu"),
                    ("fn_3_2", "3.2 Khóa ghế thời gian thực (Hold Seat 10 phút)"),
                    ("fn_3_3", "3.3 Tự động giải phóng ghế hết hạn (Worker 30s)"),
                    ("fn_3_4", "3.4 Thanh toán chuyển khoản ngân hàng VietQR")
                ]
            },
            {
                "id": "mod_4",
                "code": "4.0",
                "name": "SOÁT VÉ QR & DỊCH VỤ VÉ ĐIỆN TỬ",
                "x": 1300, "y": 160, "w": 380, "h": 46,
                "functions": [
                    ("fn_4_1", "4.1 Sinh vé điện tử kèm mã QR Token bảo mật"),
                    ("fn_4_2", "4.2 Tự động gửi vé qua Gmail SMTP đã đăng ký"),
                    ("fn_4_3", "4.3 Quét mã QR soát vé bằng camera điện thoại (<2s)"),
                    ("fn_4_4", "4.4 Lịch sử đặt vé phong cách Thẻ Cinema Pass")
                ]
            },
            {
                "id": "mod_5",
                "code": "5.0",
                "name": "DỊCH VỤ F&B, VOUCHER & BÁO CÁO",
                "x": 1720, "y": 160, "w": 380, "h": 46,
                "functions": [
                    ("fn_5_1", "5.1 Quản lý danh mục & Mua kèm combo bắp nước F&B"),
                    ("fn_5_2", "5.2 Quản lý & Áp dụng mã giảm giá Voucher"),
                    ("fn_5_3", "5.3 Khách hàng đánh giá 1-5 sao & bình luận phim"),
                    ("fn_5_4", "5.4 Dashboard thống kê doanh thu & tỷ lệ lấp đầy rạp")
                ]
            }
        ]
    }

def build_raw_mxgraphmodel():
    data = get_bfd_data()
    mxGraphModel = ET.Element("mxGraphModel", {
        "dx": "2200", "dy": "1200", "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "2200", "pageHeight": "800",
        "background": "#FFFFFF", "math": "0", "shadow": "0"
    })
    root = ET.SubElement(mxGraphModel, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    # Tiêu đề biểu đồ
    title = ET.SubElement(root, "mxCell", {
        "id": "title_banner",
        "value": "BIỂU ĐỒ PHÂN RÃ CHỨC NĂNG (FUNCTIONAL DECOMPOSITION DIAGRAM - BFD)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontFamily=Helvetica;fontSize=16;fontStyle=1;fontColor=#000000;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(title, "mxGeometry", {"x": "630", "y": "5", "width": "900", "height": "30", "as": "geometry"})

    # Nút Gốc (Root)
    r = data["root"]
    root_cell = ET.SubElement(root, "mxCell", {
        "id": r["id"],
        "value": r["name"],
        "style": (
            "rounded=1;whiteSpace=wrap;html=0;fillColor=" + COLOR_ROOT + ";"
            "strokeColor=" + COLOR_ROOT + ";fontColor=#FFFFFF;fontStyle=1;fontSize=13;"
            "align=center;verticalAlign=middle;shadow=0;fontFamily=Helvetica;"
        ),
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(root_cell, "mxGeometry", {
        "x": str(r["x"]), "y": str(r["y"]), "width": str(r["w"]), "height": str(r["h"]), "as": "geometry"
    })

    # Các Module Cấp 1 & Chức năng Cấp 2
    for mod in data["modules"]:
        mod_cell = ET.SubElement(root, "mxCell", {
            "id": mod["id"],
            "value": mod["name"],
            "style": (
                "rounded=1;whiteSpace=wrap;html=0;fillColor=" + COLOR_MODULE + ";"
                "strokeColor=" + COLOR_MODULE + ";fontColor=#FFFFFF;fontStyle=1;fontSize=11.5;"
                "align=center;verticalAlign=middle;shadow=0;fontFamily=Helvetica;"
            ),
            "vertex": "1", "parent": "1"
        })
        ET.SubElement(mod_cell, "mxGeometry", {
            "x": str(mod["x"]), "y": str(mod["y"]), "width": str(mod["w"]), "height": str(mod["h"]), "as": "geometry"
        })

        # Nối từ Root xuống Module Cấp 1
        edge_root = ET.SubElement(root, "mxCell", {
            "id": f"edge_root_{mod['id']}",
            "value": "",
            "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=" + COLOR_LINE + ";strokeWidth=1.6;endArrow=none;",
            "edge": "1", "parent": "1",
            "source": r["id"], "target": mod["id"]
        })
        ET.SubElement(edge_root, "mxGeometry", {"relative": "1", "as": "geometry"})

        # Các chức năng lá (Level 2)
        start_y = 240
        gap_y = 56
        for f_idx, (fn_id, fn_name) in enumerate(mod["functions"]):
            fy = start_y + f_idx * gap_y
            fn_cell = ET.SubElement(root, "mxCell", {
                "id": fn_id,
                "value": fn_name,
                "style": (
                    "rounded=1;whiteSpace=wrap;html=0;fillColor=" + COLOR_LEAF_BG + ";"
                    "strokeColor=" + COLOR_LEAF_BORDER + ";fontColor=" + TEXT_DARK + ";fontSize=11;"
                    "align=left;spacingLeft=12;spacingRight=8;verticalAlign=middle;shadow=0;fontFamily=Helvetica;"
                ),
                "vertex": "1", "parent": "1"
            })
            ET.SubElement(fn_cell, "mxGeometry", {
                "x": str(mod["x"]), "y": str(fy), "width": str(mod["w"]), "height": "42", "as": "geometry"
            })

            # Nối từ Module xuống chức năng lá
            edge_fn = ET.SubElement(root, "mxCell", {
                "id": f"edge_{mod['id']}_{fn_id}",
                "value": "",
                "style": "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=0;strokeColor=" + COLOR_LINE + ";strokeWidth=1.2;endArrow=none;",
                "edge": "1", "parent": "1",
                "source": mod["id"], "target": fn_id
            })
            ET.SubElement(edge_fn, "mxGeometry", {"relative": "1", "as": "geometry"})

    # Legend / Chú thích
    legend = ET.SubElement(root, "mxCell", {
        "id": "legend_node",
        "value": "CẤU TRÚC PHÂN CẤP: [Mức 0] Hệ thống CineManagement  ➔  [Mức 1] 5 Phân hệ nghiệp vụ cốt lõi  ➔  [Mức 2] 20 Chức năng chi tiết (Ánh xạ 21 User Stories)",
        "style": "text;html=0;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=#CBD5E1;fillColor=#F8FAFC;fontFamily=Helvetica;fontSize=11;fontColor=#475569;rounded=1;",
        "vertex": "1", "parent": "1"
    })
    ET.SubElement(legend, "mxGeometry", {"x": "460", "y": "495", "width": "1220", "height": "32", "as": "geometry"})

    return mxGraphModel

def compress_drawio_xml(raw_xml_string):
    encoded = urllib.parse.quote(raw_xml_string, safe='~()*!.\'')
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15, memLevel=8, strategy=0)
    deflated = compressor.compress(encoded.encode('utf-8')) + compressor.flush()
    return base64.b64encode(deflated).decode('utf-8')

def generate_drawio_files():
    model = build_raw_mxgraphmodel()
    raw_xml_str = ET.tostring(model, encoding='utf-8').decode('utf-8')

    # 1. CineManagement_ChucNang_BFD.drawio (Native Base64 Deflate)
    compressed_data = compress_drawio_xml(raw_xml_str)
    native_mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-10-22T06:55:00.000Z",
        "agent": "Antigravity CineManagement",
        "version": "21.6.8",
        "type": "device"
    })
    diag = ET.SubElement(native_mxfile, "diagram", {
        "id": "CineManagement-BFD",
        "name": "Bieu Do Phan Ra Chuc Nang (BFD)"
    })
    diag.text = compressed_data

    tree_native = ET.ElementTree(native_mxfile)
    tree_native.write("CineManagement_ChucNang_BFD.drawio", encoding="utf-8", xml_declaration=True)
    print("[1] Đã tạo file Draw.io: CineManagement_ChucNang_BFD.drawio")

    # 2. CineManagement_ChucNang_BFD_plain.xml (Uncompressed XML)
    plain_mxfile = ET.Element("mxfile", {"host": "app.diagrams.net"})
    diag_plain = ET.SubElement(plain_mxfile, "diagram", {"name": "BFD", "id": "bfd-5-mods"})
    diag_plain.append(model)
    tree_plain = ET.ElementTree(plain_mxfile)
    ET.indent(tree_plain, space="  ")
    tree_plain.write("CineManagement_ChucNang_BFD_plain.xml", encoding="utf-8", xml_declaration=True)
    print("[2] Đã tạo file XML thuần: CineManagement_ChucNang_BFD_plain.xml")

    # 3. CineManagement_ChucNang_BFD_Viewer.html (Trình xem web)
    import json
    json_xml = json.dumps(raw_xml_str)
    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biểu đồ Phân rã Chức năng (BFD) - CineManagement</title>
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
            min-height: 600px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BIỂU ĐỒ PHÂN RÃ CHỨC NĂNG (FUNCTIONAL DECOMPOSITION DIAGRAM - BFD)</h1>
        <p>Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement)</p>
    </div>
    <div class="viewer-card">
        <div class="mxgraph" style="max-width:100%;border:1px solid #E2E8F0;" data-mxgraph='{{"highlight":"#000000","nav":true,"resize":true,"toolbar":"zoom layers tags","edit":"_blank","xml":{json_xml}}}'></div>
    </div>
</body>
</html>
"""
    with open("CineManagement_ChucNang_BFD_Viewer.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[3] Đã tạo file Trình xem Web: CineManagement_ChucNang_BFD_Viewer.html")

def generate_preview_image():
    # Xuất ảnh PNG độ nét cao phong cách tối giản
    fig, ax = plt.subplots(figsize=(24.0, 11.5), dpi=220)
    ax.set_xlim(0, 24.0)
    ax.set_ylim(0, 11.5)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Tiêu đề
    ax.text(12.0, 11.0, "BIỂU ĐỒ PHÂN RÃ CHỨC NĂNG (FUNCTIONAL DECOMPOSITION DIAGRAM - BFD)",
            ha='center', va='center', fontsize=18, fontweight='bold', color='#0F172A')
    ax.text(12.0, 10.6, "Hệ thống Quản lý và Đặt vé Rạp chiếu phim (CineManagement)",
            ha='center', va='center', fontsize=12.5, fontstyle='italic', color='#475569')

    data = get_bfd_data()
    # Tọa độ gốc
    rx, ry, rw, rh = 8.5, 9.4, 7.0, 0.7
    ax.add_patch(FancyBboxPatch((rx, ry), rw, rh, boxstyle="round,pad=0.04,rounding_size=0.1",
                                fc=COLOR_ROOT, ec=COLOR_ROOT, lw=1.5))
    ax.text(rx + rw/2, ry + rh/2, data["root"]["name"],
            ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF')

    # Tọa độ phân hệ Cấp 1 và Cấp 2
    # 5 cột: x = 0.5, 5.2, 9.9, 14.6, 19.3 (width = 4.2 each)
    col_w = 4.2
    col_xs = [0.5, 5.2, 9.9, 14.6, 19.3]
    mod_y = 8.0
    mod_h = 0.65

    # Đường bus ngang nối từ gốc
    root_bottom_center = (rx + rw/2, ry)
    bus_y = 8.9
    ax.plot([root_bottom_center[0], root_bottom_center[0]], [root_bottom_center[1], bus_y],
            color=COLOR_LINE, lw=1.6)
    ax.plot([col_xs[0] + col_w/2, col_xs[-1] + col_w/2], [bus_y, bus_y],
            color=COLOR_LINE, lw=1.6)

    for i, mod in enumerate(data["modules"]):
        cx = col_xs[i]
        # Đường thẳng từ bus xuống module
        mod_top_center = (cx + col_w/2, mod_y + mod_h)
        ax.plot([mod_top_center[0], mod_top_center[0]], [bus_y, mod_top_center[1]],
                color=COLOR_LINE, lw=1.6)

        # Hộp Module Cấp 1
        ax.add_patch(FancyBboxPatch((cx, mod_y), col_w, mod_h, boxstyle="round,pad=0.03,rounding_size=0.08",
                                    fc=COLOR_MODULE, ec=COLOR_MODULE, lw=1.4))
        ax.text(cx + col_w/2, mod_y + mod_h/2, mod["name"],
                ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')

        # Nối và vẽ các chức năng lá Cấp 2
        # Đường nhánh dọc xuống các lá
        branch_x = cx + col_w/2
        leaf_start_y = 6.9
        leaf_h = 0.58
        leaf_gap = 0.85

        lowest_leaf_y = leaf_start_y - (len(mod["functions"]) - 1) * leaf_gap
        ax.plot([branch_x, branch_x], [mod_y, lowest_leaf_y + leaf_h/2],
                color=COLOR_LINE, lw=1.3)

        for f_idx, (fn_id, fn_name) in enumerate(mod["functions"]):
            fy = leaf_start_y - f_idx * leaf_gap
            
            # Hộp chức năng lá
            ax.add_patch(FancyBboxPatch((cx, fy), col_w, leaf_h, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        fc=COLOR_LEAF_BG, ec=COLOR_LEAF_BORDER, lw=1.2))
            ax.text(cx + 0.16, fy + leaf_h/2, fn_name,
                    ha='left', va='center', fontsize=8.6, color=TEXT_DARK, fontweight='bold')

    # Legend
    ax.add_patch(FancyBboxPatch((4.0, 3.2), 16.0, 0.55, boxstyle="round,pad=0.03,rounding_size=0.08",
                                fc='#F8FAFC', ec='#CBD5E1', lw=1.0))
    ax.text(12.0, 3.47,
            "CẤU TRÚC PHÂN CẤP: [Mức 0] Hệ thống CineManagement  ➔  [Mức 1] 5 Phân hệ nghiệp vụ cốt lõi  ➔  [Mức 2] 20 Chức năng chi tiết (Ánh xạ 21 User Stories)",
            ha='center', va='center', fontsize=10.5, color='#475569', fontweight='bold')

    out_img = os.path.join("diagrams", "fig_chucnang_bfd.png")
    plt.tight_layout()
    plt.savefig(out_img, dpi=220, bbox_inches='tight', facecolor='#FFFFFF')
    plt.close()
    print(f"[4] Đã xuất ảnh biểu đồ: {out_img}")

if __name__ == "__main__":
    generate_drawio_files()
    generate_preview_image()
