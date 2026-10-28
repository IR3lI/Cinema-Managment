# -*- coding: utf-8 -*-
"""
generate_diagrams.py
Vẽ toàn bộ các sơ đồ kỹ thuật phần mềm chuẩn UML, CSDL MySQL ERD, 
Biểu đồ Use Case, Sequence Diagram và Kiến trúc hệ thống
cho Báo cáo Quản lý Dự án CNTT - Cinema Management System.

PHIÊN BẢN TRẮNG ĐEN (BLACK & WHITE / GRAYSCALE CHUẨN HỌC THUẬT & IN ẤN):
- 100% ĐƠN SẮC TRẮNG ĐEN: Không sử dụng bất kỳ màu sắc nào (không xanh, đỏ, vàng, lục, tím).
- Sử dụng độ tương phản cao: Nền trắng (#FFFFFF), viền và chữ đen (#000000), 
  các mảng phân cấp dùng sắc độ xám trang nhã (#F0F0F0, #E0E0E0, #262626).
- Giữ nguyên cỡ chữ cực lớn (Large Fonts), đường nét sắc cạnh, chống vỡ hình khi in ấn hoặc chèn Word.
- Không chỉnh sửa bất kỳ ảnh chụp màn hình nào trong thư mục screenshots/.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle

# Cấu hình font tiếng Việt và độ phân giải đồ họa cao
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma', 'DejaVu Sans']
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['figure.dpi'] = 260

OUT_DIR = "diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

# BẢNG MÀU ĐƠN SẮC TRẮNG ĐEN (BLACK & WHITE / GRAYSCALE)
BLACK = "#000000"
DARK_GRAY = "#262626"
MID_GRAY = "#555555"
LIGHT_GRAY = "#F0F0F0"
VERY_LIGHT_GRAY = "#F8F8F8"
WHITE = "#FFFFFF"

# Mapping tương thích các biến cũ về thang trắng đen
NAVY = BLACK
BLUE = BLACK
LIGHT_BLUE = LIGHT_GRAY
SLATE = BLACK
LIGHT_SLATE = VERY_LIGHT_GRAY
BORDER_SLATE = BLACK
EMERALD = BLACK
LIGHT_EMERALD = LIGHT_GRAY
AMBER = BLACK
LIGHT_AMBER = LIGHT_GRAY
ROSE = BLACK
LIGHT_ROSE = LIGHT_GRAY
PURPLE = BLACK
LIGHT_PURPLE = LIGHT_GRAY

# ==============================================================================
# 1. HÌNH 1: QUY TRÌNH AGILE SCRUM (TRẮNG ĐEN)
# ==============================================================================
def draw_fig1_scrum():
    fig, ax = plt.subplots(figsize=(13.5, 8.4))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 8.4)
    ax.axis('off')

    # Title
    ax.text(6.75, 7.95, "QUY TRÌNH KHUNG LÀM VIỆC AGILE / SCRUM ÁP DỤNG TRONG DỰ ÁN", 
            ha='center', va='center', fontsize=18, fontweight='bold', color=BLACK)
    ax.text(6.75, 7.48, "Hệ thống Quản lý và Đặt vé Rạp chiếu phim (Cinema Management System)", 
            ha='center', va='center', fontsize=13.5, fontstyle='italic', color=MID_GRAY)

    # 1. Product Backlog
    ax.add_patch(FancyBboxPatch((0.4, 2.5), 2.7, 4.4, boxstyle="round,pad=0.12,rounding_size=0.18",
                                fc=WHITE, ec=BLACK, lw=2.2))
    ax.text(1.75, 6.45, "PRODUCT\nBACKLOG", ha='center', va='center', fontsize=14.5, fontweight='bold', color=BLACK)
    ax.plot([0.65, 2.85], [5.7, 5.7], color=BLACK, lw=1.8)
    ax.text(1.75, 4.25, "• 21 User Stories\n• Định nghĩa INVEST\n• Story Points Poker\n• PO: Lâm Tuấn Kiệt (KL)\n• Mức ưu tiên: Must Have", 
            ha='center', va='center', fontsize=12.2, color=BLACK, linespacing=1.6, fontweight='bold')

    # Arrow 1 -> Sprint Planning
    ax.annotate("", xy=(3.45, 4.7), xytext=(3.1, 4.7),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.6))

    # 2. Sprint Planning
    ax.add_patch(FancyBboxPatch((3.45, 2.8), 2.6, 3.8, boxstyle="round,pad=0.12,rounding_size=0.18",
                                fc=WHITE, ec=BLACK, lw=2.2))
    ax.text(4.75, 6.15, "SPRINT\nPLANNING", ha='center', va='center', fontsize=14.5, fontweight='bold', color=BLACK)
    ax.plot([3.7, 5.8], [5.4, 5.4], color=BLACK, lw=1.8)
    ax.text(4.75, 4.25, "• Chọn User Stories\n• Phân rã Tasks kỹ thuật\n• Cam kết chuẩn DoD\n• Thiết lập Sprint Goal", 
            ha='center', va='center', fontsize=12.2, color=BLACK, linespacing=1.6, fontweight='bold')

    # Arrow 2 -> Sprint Execution
    ax.annotate("", xy=(6.45, 4.7), xytext=(6.05, 4.7),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.6))

    # 3. Sprint Execution & Daily Scrum Loop
    ax.add_patch(FancyBboxPatch((6.45, 2.2), 3.7, 4.9, boxstyle="round,pad=0.12,rounding_size=0.18",
                                fc=VERY_LIGHT_GRAY, ec=BLACK, lw=2.2))
    ax.text(8.3, 6.65, "SPRINT EXECUTION\n(Chu kỳ 1 - 2 Tuần)", ha='center', va='center', fontsize=14.5, fontweight='bold', color=BLACK)
    ax.plot([6.75, 9.85], [5.95, 5.95], color=BLACK, lw=1.8)
    
    # Daily Scrum circle loop
    circle = patches.Circle((8.3, 4.75), 1.05, fc=WHITE, ec=BLACK, lw=2.2, linestyle='--')
    ax.add_patch(circle)
    ax.text(8.3, 4.95, "DAILY SCRUM", ha='center', va='center', fontsize=13, fontweight='bold', color=BLACK)
    ax.text(8.3, 4.5, "15 phút / 24h", ha='center', va='center', fontsize=11.5, fontstyle='italic', color=MID_GRAY)
    
    ax.text(8.3, 3.0, "• Lập trình ASP.NET Core & MySQL\n• Code Review & Quản lý Git PR\n• SM Luyện Đức Chiến (CL) điều phối", 
            ha='center', va='center', fontsize=12.0, color=BLACK, linespacing=1.5, fontweight='bold')

    # Arrow 3 -> Increment
    ax.annotate("", xy=(10.55, 4.7), xytext=(10.15, 4.7),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.6))

    # 4. Product Increment
    ax.add_patch(FancyBboxPatch((10.55, 2.5), 2.6, 4.4, boxstyle="round,pad=0.12,rounding_size=0.18",
                                fc=WHITE, ec=BLACK, lw=2.2))
    ax.text(11.85, 6.45, "PRODUCT\nINCREMENT\n(Chạy được)", ha='center', va='center', fontsize=14.5, fontweight='bold', color=BLACK)
    ax.plot([10.8, 12.9], [5.45, 5.45], color=BLACK, lw=1.8)
    ax.text(11.85, 4.05, "• Bản build EXE độc lập\n• MySQL Port 3306\n• UI Trắng Kem #FAF7F2\n• Tự gửi Gmail & VietQR\n• Đạt 100% chuẩn DoD", 
            ha='center', va='center', fontsize=12.2, color=BLACK, linespacing=1.6, fontweight='bold')

    # Review & Retrospective Box below
    ax.add_patch(FancyBboxPatch((4.5, 0.45), 4.7, 1.45, boxstyle="round,pad=0.12,rounding_size=0.15",
                                fc=WHITE, ec=BLACK, lw=2.0))
    ax.text(6.85, 1.45, "SPRINT REVIEW & RETROSPECTIVE", ha='center', va='center', fontsize=13.5, fontweight='bold', color=BLACK)
    ax.text(6.85, 0.90, "Demo tính năng cho PO • Nghiệm thu User Stories\nHọp cải tiến quy trình & tối ưu hiệu năng nhóm", 
            ha='center', va='center', fontsize=11.5, color=BLACK, linespacing=1.4, fontweight='bold')

    # Feedback arrow from Increment to Retrospective, and Retrospective to Backlog
    ax.plot([11.85, 11.85, 9.2], [2.5, 1.2, 1.2], color=BLACK, lw=2.0, linestyle='-')
    ax.annotate("", xy=(9.2, 1.2), xytext=(9.5, 1.2),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.2))

    ax.plot([4.5, 1.75, 1.75], [1.2, 1.2, 2.5], color=BLACK, lw=2.0, linestyle='-')
    ax.annotate("", xy=(1.75, 2.5), xytext=(1.75, 2.2),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.2))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig1_scrum_process.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 2. HÌNH 2-5: TIẾN ĐỘ JIRA BOARD 4 SPRINT (ẢNH CHỤP GỐC TỪ USER - GIỮ NGUYÊN)
# ==============================================================================
def process_jira_images():
    user_img1 = os.path.join("screenshots_user", "image3.png")
    user_img2 = os.path.join("screenshots_user", "image4.png")
    user_img3 = os.path.join("screenshots_user", "image5.png")
    user_img4 = os.path.join("screenshots_user", "image6.png")

    if os.path.exists(user_img1):
        import shutil
        shutil.copyfile(user_img1, os.path.join(OUT_DIR, "fig2_sprint1_jira.png"))
        shutil.copyfile(user_img2, os.path.join(OUT_DIR, "fig3_sprint2_jira.png"))
        shutil.copyfile(user_img3, os.path.join(OUT_DIR, "fig4_sprint3_jira.png"))
        shutil.copyfile(user_img4, os.path.join(OUT_DIR, "fig5_sprint4_jira.png"))
        print("Copied Jira boards fig2-5 from user document (screenshots untouched)")

# ==============================================================================
# 3. HÌNH 6: BIỂU ĐỒ USE CASE TỔNG THỂ TOÀN HỆ THỐNG (TRẮNG ĐEN)
# ==============================================================================
def draw_fig6_usecase_overall():
    fig, ax = plt.subplots(figsize=(15.5, 11.5))
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 11.5)
    ax.axis('off')

    # Boundary Box
    ax.add_patch(Rectangle((3.1, 0.4), 9.3, 10.6, fc=WHITE, ec=BLACK, lw=2.4))
    ax.text(7.75, 10.65, "HỆ THỐNG QUẢN LÝ VÀ ĐẶT VÉ RẠP CHIẾU PHIM (CINEMA MANAGEMENT)", 
            ha='center', va='center', fontsize=17, fontweight='bold', color=BLACK)

    # Actor drawing
    def draw_actor(x, y, name, sub=""):
        ax.add_patch(patches.Circle((x, y + 0.42), 0.25, fc=WHITE, ec=BLACK, lw=2.2))
        ax.plot([x, x], [y + 0.17, y - 0.32], color=BLACK, lw=2.4)
        ax.plot([x - 0.32, x + 0.32], [y + 0.04, y + 0.04], color=BLACK, lw=2.4)
        ax.plot([x, x - 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.plot([x, x + 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.text(x, y - 0.98, name, ha='center', va='center', fontsize=15, fontweight='bold', color=BLACK)
        if sub:
            ax.text(x, y - 1.25, sub, ha='center', va='center', fontsize=12, fontstyle='italic', color=MID_GRAY)

    draw_actor(1.4, 8.8, "Khách hàng", "Customer")
    draw_actor(1.4, 2.7, "Hệ thống ngầm", "Background Worker")
    draw_actor(14.1, 8.8, "Quản trị viên", "Admin / Manager")
    draw_actor(14.1, 2.7, "Nhân viên rạp", "Cinema Staff")

    def draw_uc(cx, cy, text, w=3.15, h=0.78, fc=WHITE, ec=BLACK):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=12.2, color=BLACK, fontweight='bold')

    # Subsystem 1
    ax.text(7.75, 10.15, "[ Phân hệ 1: Xác thực & Quản trị người dùng ]", ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)
    draw_uc(5.5, 9.45, "Đăng ký tài khoản")
    draw_uc(10.0, 9.45, "Đăng nhập hệ thống")
    draw_uc(5.5, 8.55, "Quản lý hồ sơ cá nhân")
    draw_uc(10.0, 8.55, "Quản lý nhân viên (Admin)")

    # Subsystem 2
    ax.text(7.75, 7.8, "[ Phân hệ 2: Phim, Phòng chiếu & Suất chiếu ]", ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)
    draw_uc(5.5, 7.15, "Tìm kiếm & Lọc phim")
    draw_uc(10.0, 7.15, "Quản lý phim & Trailer")
    draw_uc(5.5, 6.25, "Xem chi tiết & Lịch chiếu")
    draw_uc(10.0, 6.25, "Lập lịch suất chiếu")
    draw_uc(10.0, 5.35, "Thiết lập phòng & Sơ đồ ghế")

    # Subsystem 3
    ax.text(7.75, 4.65, "[ Phân hệ 3: Đặt vé, Giữ ghế 10p & Thanh toán ]", ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)
    draw_uc(5.5, 4.0, "Chọn ghế trên sơ đồ")
    draw_uc(10.0, 4.0, "Khóa ghế 10 phút <<include>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(5.5, 3.1, "Mua combo F&B <<extend>>")
    draw_uc(10.0, 3.1, "Thanh toán VietQR", fc=WHITE, ec=BLACK)
    draw_uc(5.5, 2.2, "Tự động hủy giữ ghế (Timeout)", fc=LIGHT_GRAY, ec=BLACK)

    # Subsystem 4
    ax.text(7.75, 1.55, "[ Phân hệ 4: Soát vé mã QR & Báo cáo thống kê ]", ha='center', va='center', fontsize=14, fontweight='bold', color=BLACK)
    draw_uc(5.5, 0.95, "Gửi vé Gmail tự động <<include>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(10.0, 0.95, "Quét QR soát vé bằng Camera", fc=WHITE, ec=BLACK)

    # Customer Lines
    for uc_x, uc_y in [(5.5, 9.45), (10.0, 9.45), (5.5, 8.55), (5.5, 7.15), (5.5, 6.25), (5.5, 4.0), (5.5, 3.1), (10.0, 3.1)]:
        ax.plot([1.9, uc_x - 1.58], [8.8, uc_y], color=BLACK, lw=1.5)

    # Admin Lines
    for uc_x, uc_y in [(10.0, 9.45), (10.0, 8.55), (10.0, 7.15), (10.0, 6.25), (10.0, 5.35)]:
        ax.plot([13.6, uc_x + 1.58], [8.8, uc_y], color=BLACK, lw=1.5)

    # Staff Lines
    for uc_x, uc_y in [(10.0, 9.45), (10.0, 0.95)]:
        ax.plot([13.6, uc_x + 1.58], [2.7, uc_y], color=BLACK, lw=1.5)

    # Worker Lines
    for uc_x, uc_y in [(5.5, 2.2), (5.5, 0.95)]:
        ax.plot([1.9, uc_x - 1.58], [2.7, uc_y], color=BLACK, lw=1.6, linestyle='--')
    # Worker to Khóa ghế routed cleanly below subtitle
    ax.plot([1.9, 3.1, 7.8, 8.42], [2.7, 3.65, 3.65, 4.0], color=BLACK, lw=1.6, linestyle='--')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig6_usecase_overall.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 4. HÌNH 7: USE CASE PHÂN HỆ 1 - XÁC THỰC & QUẢN TRỊ NGƯỜI DÙNG (TRẮNG ĐEN)
# ==============================================================================
def draw_fig7_usecase_auth():
    fig, ax = plt.subplots(figsize=(12, 7.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.8)
    ax.axis('off')

    ax.add_patch(Rectangle((2.4, 0.5), 7.2, 6.8, fc=WHITE, ec=BLACK, lw=2.4))
    ax.text(6.0, 6.95, "PHÂN HỆ 1: XÁC THỰC & QUẢN TRỊ NGƯỜI DÙNG", ha='center', va='center', fontsize=16.5, fontweight='bold', color=BLACK)

    def draw_actor(x, y, name):
        ax.add_patch(patches.Circle((x, y + 0.42), 0.25, fc=WHITE, ec=BLACK, lw=2.2))
        ax.plot([x, x], [y + 0.17, y - 0.32], color=BLACK, lw=2.4)
        ax.plot([x - 0.32, x + 0.32], [y + 0.04, y + 0.04], color=BLACK, lw=2.4)
        ax.plot([x, x - 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.plot([x, x + 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.text(x, y - 0.98, name, ha='center', va='center', fontsize=15, fontweight='bold', color=BLACK)

    draw_actor(1.2, 4.4, "Khách hàng")
    draw_actor(10.8, 4.4, "Quản trị viên")

    def draw_uc(cx, cy, text, w=3.15, h=0.82, fc=WHITE, ec=BLACK):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=13, color=BLACK, fontweight='bold')

    draw_uc(4.4, 5.8, "Đăng ký tài khoản")
    draw_uc(6.0, 4.5, "Đăng nhập hệ thống")
    draw_uc(6.0, 3.2, "Xác thực & Cấp Cookie\n<<include>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(4.4, 1.8, "Quản lý hồ sơ cá nhân")
    draw_uc(7.6, 1.8, "Đổi mật khẩu\n<<extend>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(7.6, 5.8, "Cấp tài khoản nhân viên\n(Admin RBAC)")

    # Customer links
    ax.plot([1.6, 2.82], [4.4, 5.8], color=BLACK, lw=1.5)
    ax.plot([1.6, 4.42], [4.4, 4.5], color=BLACK, lw=1.5)
    ax.plot([1.6, 2.82], [4.4, 1.8], color=BLACK, lw=1.5)

    # Admin links
    ax.plot([10.4, 7.58], [4.4, 4.5], color=BLACK, lw=1.5)
    ax.plot([10.4, 9.18], [4.4, 5.8], color=BLACK, lw=1.5)

    # Include arrow (Đăng nhập -> Xác thực)
    ax.annotate("", xy=(6.0, 3.61), xytext=(6.0, 4.09),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))
    # Extend arrow (Đổi MK -> Hồ sơ)
    ax.annotate("", xy=(5.98, 1.8), xytext=(6.02, 1.8),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig7_usecase_auth.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 5. HÌNH 8: USE CASE PHÂN HỆ 2 - PHIM, PHÒNG CHIẾU & SUẤT CHIẾU (TRẮNG ĐEN)
# ==============================================================================
def draw_fig8_usecase_movie_showtime():
    fig, ax = plt.subplots(figsize=(12, 8.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    ax.add_patch(Rectangle((2.4, 0.4), 7.2, 7.3, fc=WHITE, ec=BLACK, lw=2.4))
    ax.text(6.0, 7.35, "PHÂN HỆ 2: PHIM, PHÒNG CHIẾU & SUẤT CHIẾU", ha='center', va='center', fontsize=16.5, fontweight='bold', color=BLACK)

    def draw_actor(x, y, name):
        ax.add_patch(patches.Circle((x, y + 0.42), 0.25, fc=WHITE, ec=BLACK, lw=2.2))
        ax.plot([x, x], [y + 0.17, y - 0.32], color=BLACK, lw=2.4)
        ax.plot([x - 0.32, x + 0.32], [y + 0.04, y + 0.04], color=BLACK, lw=2.4)
        ax.plot([x, x - 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.plot([x, x + 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.text(x, y - 0.98, name, ha='center', va='center', fontsize=15, fontweight='bold', color=BLACK)

    draw_actor(1.2, 4.4, "Khách hàng")
    draw_actor(10.8, 4.4, "Quản trị viên")

    def draw_uc(cx, cy, text, w=3.15, h=0.78, fc=WHITE, ec=BLACK):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=12.8, color=BLACK, fontweight='bold')

    draw_uc(4.3, 6.3, "Tìm kiếm phim")
    draw_uc(4.3, 5.0, "Lọc phim theo thể loại")
    draw_uc(4.3, 3.7, "Xem chi tiết & Trailer")
    draw_uc(4.3, 2.4, "Xem lịch chiếu theo ngày")

    draw_uc(7.7, 6.3, "CRUD Phim & Poster")
    draw_uc(7.7, 5.0, "Thiết lập phòng & Ghế")
    draw_uc(7.7, 3.7, "Lập lịch suất chiếu")
    draw_uc(7.7, 2.3, "Kiểm tra xung đột giờ\n<<include>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(7.7, 1.0, "Quản lý danh mục F&B")

    # Links Customer
    for y in [6.3, 5.0, 3.7, 2.4]:
        ax.plot([1.6, 2.72], [4.4, y], color=BLACK, lw=1.5)

    # Links Admin
    for y in [6.3, 5.0, 3.7, 1.0]:
        ax.plot([10.4, 9.28], [4.4, y], color=BLACK, lw=1.5)

    # Include arrow
    ax.annotate("", xy=(7.7, 2.69), xytext=(7.7, 3.31),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig8_usecase_movie_showtime.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 6. HÌNH 9: USE CASE PHÂN HỆ 3 - ĐẶT VÉ, GIỮ GHẾ 10P & THANH TOÁN (TRẮNG ĐEN)
# ==============================================================================
def draw_fig9_usecase_booking():
    fig, ax = plt.subplots(figsize=(12, 8.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    ax.add_patch(Rectangle((2.4, 0.4), 7.2, 7.3, fc=WHITE, ec=BLACK, lw=2.4))
    ax.text(6.0, 7.35, "PHÂN HỆ 3: ĐẶT VÉ, GIỮ GHẾ 10 PHÚT & THANH TOÁN", ha='center', va='center', fontsize=16.5, fontweight='bold', color=BLACK)

    def draw_actor(x, y, name, sub=""):
        ax.add_patch(patches.Circle((x, y + 0.42), 0.25, fc=WHITE, ec=BLACK, lw=2.2))
        ax.plot([x, x], [y + 0.17, y - 0.32], color=BLACK, lw=2.4)
        ax.plot([x - 0.32, x + 0.32], [y + 0.04, y + 0.04], color=BLACK, lw=2.4)
        ax.plot([x, x - 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.plot([x, x + 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.text(x, y - 0.98, name, ha='center', va='center', fontsize=15, fontweight='bold', color=BLACK)
        if sub:
            ax.text(x, y - 1.25, sub, ha='center', va='center', fontsize=12, fontstyle='italic', color=MID_GRAY)

    draw_actor(1.2, 4.4, "Khách hàng")
    draw_actor(10.8, 2.2, "Hệ thống ngầm", "Timeout Worker")

    def draw_uc(cx, cy, text, w=3.15, h=0.78, fc=WHITE, ec=BLACK):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=12.6, color=BLACK, fontweight='bold')

    draw_uc(4.3, 6.2, "Chọn ghế trên sơ đồ")
    draw_uc(7.7, 6.2, "Khóa ghế tạm thời 10p\n<<include>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(4.3, 4.8, "Mua kèm Combo F&B\n<<extend>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(4.3, 3.4, "Áp mã Voucher\n<<extend>>", fc=LIGHT_GRAY, ec=BLACK)
    draw_uc(4.3, 1.8, "Thanh toán VietQR\n(Quét mã QR tiện lợi)", fc=WHITE, ec=BLACK)
    draw_uc(7.7, 1.8, "Tự động hủy giữ ghế\n(Timeout 10 phút)", fc=LIGHT_GRAY, ec=BLACK)

    # Customer links
    ax.plot([1.6, 2.72], [4.4, 6.2], color=BLACK, lw=1.5)
    ax.plot([1.6, 2.72], [4.4, 1.8], color=BLACK, lw=1.5)

    # Worker link
    ax.plot([10.4, 9.28], [2.2, 1.8], color=BLACK, lw=1.6, linestyle='--')

    # Include arrow (Chọn ghế -> Khóa ghế)
    ax.annotate("", xy=(6.12, 6.2), xytext=(5.88, 6.2),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))
    # Extend arrows to Thanh toán
    ax.annotate("", xy=(4.3, 2.19), xytext=(4.3, 3.01),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))
    ax.annotate("", xy=(4.3, 2.19), xytext=(4.3, 4.41),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig9_usecase_booking.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 7. HÌNH 10: USE CASE PHÂN HỆ 4 - SOÁT VÉ QR & BÁO CÁO (TRẮNG ĐEN)
# ==============================================================================
def draw_fig10_usecase_ticket_report():
    fig, ax = plt.subplots(figsize=(13, 8.2))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    ax.add_patch(Rectangle((2.7, 0.4), 7.6, 7.3, fc=WHITE, ec=BLACK, lw=2.4))
    ax.text(6.5, 7.35, "PHÂN HỆ 4: SOÁT VÉ MÃ QR & BÁO CÁO THỐNG KÊ", ha='center', va='center', fontsize=16.5, fontweight='bold', color=BLACK)

    def draw_actor(x, y, name):
        ax.add_patch(patches.Circle((x, y + 0.42), 0.25, fc=WHITE, ec=BLACK, lw=2.2))
        ax.plot([x, x], [y + 0.17, y - 0.32], color=BLACK, lw=2.4)
        ax.plot([x - 0.32, x + 0.32], [y + 0.04, y + 0.04], color=BLACK, lw=2.4)
        ax.plot([x, x - 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.plot([x, x + 0.27], [y - 0.32, y - 0.72], color=BLACK, lw=2.4)
        ax.text(x, y - 0.98, name, ha='center', va='center', fontsize=15, fontweight='bold', color=BLACK)

    draw_actor(1.3, 5.4, "Khách hàng")
    draw_actor(1.3, 2.0, "Hệ thống Gmail")
    draw_actor(11.7, 5.4, "Quản trị viên")
    draw_actor(11.7, 2.0, "Nhân viên rạp")

    def draw_uc(cx, cy, text, w=3.25, h=0.78, fc=WHITE, ec=BLACK):
        ax.add_patch(Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.8))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=12.6, color=BLACK, fontweight='bold')

    draw_uc(4.7, 6.2, "Xem lịch sử đặt vé\n(Cinema Pass)")
    draw_uc(4.7, 4.8, "Đánh giá & Bình luận phim")
    draw_uc(4.7, 2.4, "Tự động gửi vé qua Gmail\n<<include>>", fc=LIGHT_GRAY, ec=BLACK)

    draw_uc(8.3, 6.2, "Xem Dashboard Doanh thu")
    draw_uc(8.3, 4.8, "Thống kê Tỷ lệ lấp đầy rạp")
    draw_uc(8.3, 2.9, "Quét QR soát vé Camera\n(Staff Mobile)")
    draw_uc(8.3, 1.4, "Nhập mã vé thủ công\n<<extend>>", fc=LIGHT_GRAY, ec=BLACK)

    # Links Customer
    ax.plot([1.7, 3.07], [5.4, 6.2], color=BLACK, lw=1.5)
    ax.plot([1.7, 3.07], [5.4, 4.8], color=BLACK, lw=1.5)
    ax.plot([1.7, 3.07], [5.4, 2.4], color=BLACK, lw=1.5)

    # Link Gmail Worker
    ax.plot([1.7, 3.07], [2.0, 2.4], color=BLACK, lw=1.6, linestyle='--')

    # Links Admin
    ax.plot([11.3, 9.93], [5.4, 6.2], color=BLACK, lw=1.5)
    ax.plot([11.3, 9.93], [5.4, 4.8], color=BLACK, lw=1.5)
    ax.plot([11.3, 9.93], [5.4, 2.9], color=BLACK, lw=1.5)

    # Links Staff
    ax.plot([11.3, 9.93], [2.0, 2.9], color=BLACK, lw=1.5)
    ax.plot([11.3, 9.93], [2.0, 1.4], color=BLACK, lw=1.5)

    # Extend arrow (Nhập thủ công -> Quét camera)
    ax.annotate("", xy=(8.3, 2.51), xytext=(8.3, 1.79),
                arrowprops=dict(arrowstyle="->", color=BLACK, lw=2.0, linestyle='--'))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig10_usecase_ticket_report.png")
    fig.savefig(path, dpi=260, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 8. HÌNH 11: BIỂU ĐỒ SEQUENCE ĐẶT VÉ & KHÓA GHẾ 10 PHÚT (TRẮNG ĐEN - FONT LỚN)
# ==============================================================================
def draw_fig11_seq_booking():
    fig, ax = plt.subplots(figsize=(16.8, 10.5))
    ax.set_xlim(0, 16.8)
    ax.set_ylim(0, 10.5)
    ax.axis('off')

    ax.text(8.4, 9.95, "BIỂU ĐỒ SEQUENCE: CHỨC NĂNG ĐẶT VÉ & KHÓA GHẾ TẠM THỜI 10 PHÚT", 
            ha='center', va='center', fontsize=20.0, fontweight='bold', color=BLACK)

    lifelines = [
        ("Khách hàng\n(Browser Client)", 2.0),
        ("Booking\nController", 6.2),
        ("MySQL Database\n(cinema_db)", 10.8),
        ("Timeout Worker\n(Background Service)", 15.1)
    ]

    for name, x in lifelines:
        ax.add_patch(FancyBboxPatch((x - 1.5, 8.7), 3.0, 0.95, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=2.2))
        ax.text(x, 9.18, name, ha='center', va='center', fontsize=15.0, fontweight='bold', color=BLACK)
        ax.plot([x, x], [8.7, 0.55], color=BLACK, lw=1.6, linestyle='--')

    def draw_activation(x, y_start, y_end, color=LIGHT_GRAY):
        ax.add_patch(Rectangle((x - 0.16, y_end), 0.32, y_start - y_end, fc=color, ec=BLACK, lw=1.6))

    draw_activation(2.0, 8.0, 1.4)
    draw_activation(6.2, 7.8, 4.3)
    draw_activation(10.8, 7.4, 4.7)
    draw_activation(15.1, 2.9, 0.9, color="#E0E0E0")

    def draw_msg(x1, x2, y, text, is_reply=False, color=BLACK):
        linestyle = "--" if is_reply else "-"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.2, linestyle=linestyle))
        mid = (x1 + x2) / 2
        ax.text(mid, y + 0.15, text, ha='center', va='bottom', fontsize=14.0, color=BLACK, fontweight='bold')

    draw_msg(2.0, 6.2, 7.8, "1: Click chọn ghế [A05, A06] & 'Tiếp tục'")
    draw_msg(6.2, 10.8, 7.0, "2: BEGIN TRANSACTION & Kiểm tra ghế trống")
    draw_msg(10.8, 6.2, 6.3, "3: Trả về trạng thái: Ghế trống (Available)", is_reply=True)
    draw_msg(6.2, 10.8, 5.5, "4: INSERT BookedSeats (Status='Held', 10 phút)")
    draw_msg(10.8, 6.2, 4.8, "5: COMMIT TRANSACTION thành công", is_reply=True)
    draw_msg(6.2, 2.0, 4.1, "6: HTTP 200 OK { success: true, expires: 10:00 }", is_reply=True)

    # Note Box Countdown
    ax.add_patch(FancyBboxPatch((0.4, 2.7), 3.2, 1.05, boxstyle="round,pad=0.06", fc=LIGHT_GRAY, ec=BLACK, lw=2.0))
    ax.text(2.0, 3.22, "Client đếm ngược\n10:00 -> 00:00", ha='center', va='center', fontsize=14.0, color=BLACK, fontweight='bold')

    # Timeout branch
    draw_msg(15.1, 10.8, 2.6, "7: Quét chu kỳ 30s: Tìm ghế Held quá hạn", color=BLACK)
    draw_msg(10.8, 15.1, 1.9, "8: Phát hiện đơn quá 10 phút chưa thanh toán", is_reply=True, color=BLACK)
    draw_msg(15.1, 10.8, 1.1, "9: UPDATE BookedSeats -> 'Expired' (Nhả ghế)", color=BLACK)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig11_seq_booking.png")
    fig.savefig(path, dpi=280, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 9. HÌNH 12: BIỂU ĐỒ SEQUENCE THANH TOÁN VIETQR & GỬI GMAIL (TRẮNG ĐEN - FONT LỚN)
# ==============================================================================
def draw_fig12_seq_payment_email():
    fig, ax = plt.subplots(figsize=(18.2, 11.5))
    ax.set_xlim(0, 18.2)
    ax.set_ylim(0, 11.5)
    ax.axis('off')

    ax.text(9.1, 10.9, "BIỂU ĐỒ SEQUENCE: THANH TOÁN VIETQR & TỰ ĐỘNG GỬI VÉ QUA GMAIL", 
            ha='center', va='center', fontsize=20.5, fontweight='bold', color=BLACK)

    lifelines = [
        ("Khách hàng\n(Browser Client)", 1.7),
        ("Checkout\nController", 5.4),
        ("Cổng thanh toán\nVietQR Service", 9.2),
        ("MySQL DB\n(cinema_db)", 13.0),
        ("Gmail SMTP\n(Mail Service)", 16.5)
    ]

    for name, x in lifelines:
        ax.add_patch(FancyBboxPatch((x - 1.5, 9.4), 3.0, 1.0, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=2.2))
        ax.text(x, 9.9, name, ha='center', va='center', fontsize=14.5, fontweight='bold', color=BLACK)
        ax.plot([x, x], [9.4, 0.45], color=BLACK, lw=1.6, linestyle='--')

    def draw_msg(x1, x2, y, text, is_reply=False, color=BLACK):
        linestyle = "--" if is_reply else "-"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.2, linestyle=linestyle))
        mid = (x1 + x2) / 2
        ax.text(mid, y + 0.15, text, ha='center', va='bottom', fontsize=13.6, color=BLACK, fontweight='bold')

    draw_msg(1.7, 5.4, 8.6, "1: Chọn VietQR & Áp dụng Voucher")
    draw_msg(5.4, 9.2, 7.8, "2: Tạo mã VietQR (Chuẩn Napas 247)")
    draw_msg(9.2, 5.4, 7.1, "3: Trả về ảnh VietQR & thông tin đơn hàng", is_reply=True)
    draw_msg(5.4, 1.7, 6.4, "4: Hiển thị mã VietQR tại màn hình Checkout", is_reply=True)
    draw_msg(1.7, 5.4, 5.6, "5: Khách quét app & 'Xác nhận thanh toán'")
    draw_msg(5.4, 13.0, 4.8, "6: UPDATE Booking Status='Paid'")
    draw_msg(5.4, 13.0, 4.1, "7: INSERT Tickets (TicketCode, QrToken)")
    draw_msg(13.0, 5.4, 3.4, "8: Lấy Email tài khoản (User.Email)", is_reply=True)
    draw_msg(5.4, 16.5, 2.6, "9: SendEmailAsync (Vé HTML & ảnh QR đính kèm)", color=BLACK)
    draw_msg(16.5, 5.4, 1.9, "10: SMTP 250 OK (Gửi vé thành công)", is_reply=True, color=BLACK)
    draw_msg(5.4, 1.7, 1.1, "11: Chuyển hướng xem Cinema Pass & QR vé", is_reply=True)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig12_seq_payment_email.png")
    fig.savefig(path, dpi=280, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 10. HÌNH 13: BIỂU ĐỒ SEQUENCE NHÂN VIÊN QUÉT MÃ QR SOÁT VÉ (TRẮNG ĐEN - FONT LỚN)
# ==============================================================================
def draw_fig13_seq_scanner():
    fig, ax = plt.subplots(figsize=(16.8, 10.5))
    ax.set_xlim(0, 16.8)
    ax.set_ylim(0, 10.5)
    ax.axis('off')

    ax.text(8.4, 9.95, "BIỂU ĐỒ SEQUENCE: CHỨC NĂNG NHÂN VIÊN QUÉT MÃ QR SOÁT VÉ", 
            ha='center', va='center', fontsize=20.0, fontweight='bold', color=BLACK)

    lifelines = [
        ("Nhân viên\n(Staff)", 2.0),
        ("Scanner UI\n(HTML5 Camera)", 6.0),
        ("Staff Controller\n(ValidateTicket API)", 10.6),
        ("MySQL DB\n(cinema_db)", 15.0)
    ]

    for name, x in lifelines:
        ax.add_patch(FancyBboxPatch((x - 1.5, 8.7), 3.0, 0.95, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=2.2))
        ax.text(x, 9.18, name, ha='center', va='center', fontsize=15.0, fontweight='bold', color=BLACK)
        ax.plot([x, x], [8.7, 0.5], color=BLACK, lw=1.6, linestyle='--')

    def draw_msg(x1, x2, y, text, is_reply=False, color=BLACK):
        linestyle = "--" if is_reply else "-"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.2, linestyle=linestyle))
        mid = (x1 + x2) / 2
        ax.text(mid, y + 0.15, text, ha='center', va='bottom', fontsize=14.0, color=BLACK, fontweight='bold')

    draw_msg(2.0, 6.0, 7.8, "1: Hướng camera điện thoại vào mã QR vé")
    draw_msg(6.0, 6.0, 7.0, "2: html5-qrcode giải mã token bảo mật")
    draw_msg(6.0, 10.6, 6.2, "3: POST /Staff/ValidateTicket { token: '...' }")
    draw_msg(10.6, 15.0, 5.4, "4: SELECT Ticket WHERE QrToken=...")
    draw_msg(15.0, 10.6, 4.7, "5: Trả về vé hợp lệ: Status='Issued'", is_reply=True)
    draw_msg(10.6, 15.0, 4.0, "6: UPDATE Tickets SET Status='CheckedIn'")
    draw_msg(15.0, 10.6, 3.3, "7: Xác nhận cập nhật trạng thái vé thành công", is_reply=True)
    draw_msg(10.6, 6.0, 2.5, "8: HTTP 200 OK { valid: true, seat: 'A05' }", is_reply=True, color=BLACK)
    draw_msg(6.0, 2.0, 1.8, "9: Màn hình báo 'HỢP LỆ' & phát âm thanh BÍP", is_reply=True, color=BLACK)

    # Frame alt check-in again
    ax.add_patch(Rectangle((4.8, 0.55), 10.6, 1.05, fc=LIGHT_GRAY, ec=BLACK, lw=1.6, linestyle=':'))
    ax.text(5.0, 1.35, "[Alt: Vé đã quét trước đó]", fontsize=13.0, fontweight='bold', color=BLACK)
    draw_msg(10.6, 6.0, 0.85, "8b: HTTP 400 { valid: false, reason: 'VÉ ĐÃ SỬ DỤNG' }", is_reply=True, color=BLACK)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig13_seq_scanner.png")
    fig.savefig(path, dpi=280, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 11. HÌNH 14: SƠ ĐỒ QUAN HỆ THỰC THỂ CSDL MYSQL (ERD - TRẮNG ĐEN - FONT LỚN)
# ==============================================================================
def draw_fig14_database_erd():
    fig, ax = plt.subplots(figsize=(23.5, 17.0))
    ax.set_xlim(0, 23.5)
    ax.set_ylim(0, 17.0)
    ax.axis('off')

    ax.text(11.75, 16.5, "SƠ ĐỒ QUAN HỆ THỰC THỂ CƠ SỞ DỮ LIỆU MYSQL (DATABASE ERD - 14 BẢNG)", 
            ha='center', va='center', fontsize=22.5, fontweight='bold', color=BLACK)
    ax.text(11.75, 16.0, "Hệ quản trị CSDL MySQL / MariaDB 10.11 | Port 3306 | Collation: utf8mb4_unicode_ci", 
            ha='center', va='center', fontsize=15.0, fontstyle='italic', color=MID_GRAY)

    def draw_table(x, y, title, columns, width=3.9, height=None, header_color=DARK_GRAY):
        row_h = 0.42
        h = 0.55 + len(columns) * row_h if height is None else height
        ax.add_patch(FancyBboxPatch((x, y - h), width, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                    fc=WHITE, ec=BLACK, lw=2.0))
        # Dark header box with white text
        ax.add_patch(FancyBboxPatch((x, y - 0.55), width, 0.55, boxstyle="round,pad=0.04,rounding_size=0.12",
                                    fc=DARK_GRAY, ec=BLACK, lw=1.6))
        ax.text(x + width/2, y - 0.28, title, ha='center', va='center', fontsize=15.5, fontweight='bold', color=WHITE)

        for i, (col, col_type, is_pk, is_fk) in enumerate(columns):
            cy = y - 0.78 - i * row_h
            prefix = "PK " if is_pk else "FK " if is_fk else "   "
            ax.text(x + 0.14, cy, f"{prefix}{col}", fontsize=13.0, fontweight='bold', color=BLACK)
            ax.text(x + width - 0.14, cy, col_type, ha='right', fontsize=11.8, fontstyle='italic', color=MID_GRAY)
        return (x, y, width, h)

    # 1. AspNetUsers
    draw_table(0.5, 15.2, "AspNetUsers", [
        ("Id", "VARCHAR(255)", True, False),
        ("UserName", "VARCHAR(256)", False, False),
        ("Email", "VARCHAR(256)", False, False),
        ("FullName", "VARCHAR(150)", False, False),
        ("PhoneNumber", "VARCHAR(20)", False, False),
        ("PasswordHash", "LONGTEXT", False, False),
        ("CreatedAt", "DATETIME", False, False)
    ])

    # 2. Staffs
    draw_table(0.5, 10.4, "Staffs", [
        ("Id", "INT AUTO_INC", True, False),
        ("UserId", "VARCHAR(255)", False, True),
        ("Position", "VARCHAR(100)", False, False),
        ("Department", "VARCHAR(100)", False, False),
        ("Salary", "DECIMAL(18,2)", False, False),
        ("IsActive", "TINYINT(1)", False, False)
    ])

    # 3. Reviews
    draw_table(0.5, 6.2, "Reviews", [
        ("Id", "INT AUTO_INC", True, False),
        ("UserId", "VARCHAR(255)", False, True),
        ("MovieId", "INT", False, True),
        ("Rating", "INT", False, False),
        ("Comment", "TEXT", False, False),
        ("CreatedAt", "DATETIME", False, False)
    ])

    # 4. Genres
    draw_table(5.1, 15.2, "Genres", [
        ("Id", "INT AUTO_INC", True, False),
        ("Name", "VARCHAR(100)", False, False),
        ("Description", "TEXT", False, False)
    ])

    # 5. Movies
    draw_table(5.1, 12.2, "Movies", [
        ("Id", "INT AUTO_INC", True, False),
        ("GenreId", "INT", False, True),
        ("Title", "VARCHAR(255)", False, False),
        ("DurationMinutes", "INT", False, False),
        ("ReleaseDate", "DATETIME", False, False),
        ("PosterUrl", "VARCHAR(500)", False, False),
        ("Rating", "DOUBLE", False, False)
    ])

    # 6. ScreeningRooms
    draw_table(5.1, 7.3, "ScreeningRooms", [
        ("Id", "INT AUTO_INC", True, False),
        ("RoomName", "VARCHAR(100)", False, False),
        ("TotalRows", "INT", False, False),
        ("TotalColumns", "INT", False, False),
        ("TotalSeats", "INT", False, False),
        ("ScreenType", "VARCHAR(50)", False, False)
    ])

    # 7. Seats
    draw_table(5.1, 3.2, "Seats", [
        ("Id", "INT AUTO_INC", True, False),
        ("RoomId", "INT", False, True),
        ("RowName", "VARCHAR(5)", False, False),
        ("SeatNumber", "INT", False, False),
        ("SeatType", "VARCHAR(50)", False, False)
    ])

    # 8. Showtimes
    draw_table(9.7, 15.2, "Showtimes", [
        ("Id", "INT AUTO_INC", True, False),
        ("MovieId", "INT", False, True),
        ("RoomId", "INT", False, True),
        ("StartTime", "DATETIME", False, False),
        ("EndTime", "DATETIME", False, False),
        ("BasePrice", "DECIMAL(18,2)", False, False),
        ("Status", "VARCHAR(50)", False, False)
    ])

    # 9. BookedSeats
    draw_table(9.7, 9.8, "BookedSeats", [
        ("Id", "INT AUTO_INC", True, False),
        ("ShowtimeId", "INT", False, True),
        ("SeatId", "INT", False, True),
        ("BookingId", "INT", False, True),
        ("Status", "VARCHAR(50)", False, False),
        ("Price", "DECIMAL(18,2)", False, False),
        ("HoldExpiresAt", "DATETIME", False, False)
    ])

    # 10. Bookings
    draw_table(14.3, 15.2, "Bookings", [
        ("Id", "INT AUTO_INC", True, False),
        ("UserId", "VARCHAR(255)", False, True),
        ("ShowtimeId", "INT", False, True),
        ("BookingCode", "VARCHAR(50)", False, False),
        ("TotalPrice", "DECIMAL(18,2)", False, False),
        ("FinalAmount", "DECIMAL(18,2)", False, False),
        ("PaymentMethod", "VARCHAR(50)", False, False),
        ("PaymentStatus", "VARCHAR(50)", False, False),
        ("CreatedAt", "DATETIME", False, False)
    ])

    # 11. Tickets
    draw_table(14.3, 9.2, "Tickets", [
        ("Id", "INT AUTO_INC", True, False),
        ("BookingId", "INT", False, True),
        ("BookedSeatId", "INT", False, True),
        ("TicketCode", "VARCHAR(50)", False, False),
        ("QrCodeToken", "VARCHAR(255)", False, False),
        ("Status", "VARCHAR(50)", False, False),
        ("CheckedInAt", "DATETIME", False, False)
    ])

    # 12. Vouchers
    draw_table(14.3, 4.5, "Vouchers", [
        ("Id", "INT AUTO_INC", True, False),
        ("Code", "VARCHAR(50)", False, False),
        ("DiscountPercent", "INT", False, False),
        ("MaxDiscountAmount", "DECIMAL(18,2)", False, False),
        ("IsActive", "TINYINT(1)", False, False)
    ])

    # 13. FoodItems
    draw_table(18.9, 15.2, "FoodItems", [
        ("Id", "INT AUTO_INC", True, False),
        ("Name", "VARCHAR(150)", False, False),
        ("Description", "TEXT", False, False),
        ("Price", "DECIMAL(18,2)", False, False),
        ("ImageUrl", "VARCHAR(500)", False, False),
        ("IsAvailable", "TINYINT(1)", False, False)
    ], width=4.1)

    # 14. BookingFoodItems
    draw_table(18.9, 10.4, "BookingFoodItems", [
        ("Id", "INT AUTO_INC", True, False),
        ("BookingId", "INT", False, True),
        ("FoodItemId", "INT", False, True),
        ("Quantity", "INT", False, False),
        ("UnitPrice", "DECIMAL(18,2)", False, False)
    ], width=4.1)

    # Relationships Lines
    def draw_relation(p1, p2, color=BLACK):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=2.0, linestyle='-')
        ax.plot(p2[0], p2[1], marker='o', markersize=5.5, color=color)

    # Users -> Staffs, Bookings, Reviews
    draw_relation((2.45, 11.7), (2.45, 10.4))
    # Route Users -> Bookings safely above table titles
    ax.plot([4.4, 4.4, 14.3, 14.3], [13.8, 15.55, 15.55, 13.8], color=BLACK, lw=2.0)
    ax.plot(14.3, 13.8, marker='o', markersize=5.5, color=BLACK)

    draw_relation((2.45, 7.3), (2.45, 6.2))

    # Genres -> Movies
    draw_relation((7.05, 13.4), (7.05, 12.2))

    # Movies -> Showtimes
    draw_relation((9.0, 10.5), (9.7, 13.2))

    # Rooms -> Seats & Showtimes
    draw_relation((7.05, 4.2), (7.05, 3.2))
    draw_relation((9.0, 5.8), (9.7, 12.0))

    # Showtimes -> BookedSeats
    draw_relation((11.65, 11.7), (11.65, 9.8))

    # Bookings -> Tickets & BookedSeats & BookingFoodItems
    draw_relation((16.25, 10.8), (16.25, 9.2))
    draw_relation((14.3, 11.2), (13.6, 8.2))
    draw_relation((18.2, 13.2), (18.9, 11.4))

    # FoodItems -> BookingFoodItems
    draw_relation((20.95, 12.1), (20.95, 10.4))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig14_database_erd.png")
    fig.savefig(path, dpi=280, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

# ==============================================================================
# 12. HÌNH 15: KIẾN TRÚC PHÂN TẦNG ASP.NET CORE & MYSQL (TRẮNG ĐEN - FONT LỚN)
# ==============================================================================
def draw_fig15_architecture():
    fig, ax = plt.subplots(figsize=(17.5, 11.8))
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 11.8)
    ax.axis('off')

    ax.text(8.75, 11.25, "KIẾN TRÚC PHÂN TẦNG HỆ THỐNG (ASP.NET CORE MVC & MYSQL ARCHITECTURE)", 
            ha='center', va='center', fontsize=21.0, fontweight='bold', color=BLACK)
    ax.text(8.75, 10.75, "Mô hình 3 tầng (Presentation - Business Logic - Data Access) tích hợp Dịch vụ ngoài", 
            ha='center', va='center', fontsize=15.0, fontstyle='italic', color=MID_GRAY)

    # Layer 1: Presentation Layer
    ax.add_patch(FancyBboxPatch((0.5, 8.2), 16.5, 2.15, boxstyle="round,pad=0.1,rounding_size=0.16", fc=LIGHT_GRAY, ec=BLACK, lw=2.4))
    ax.text(1.0, 9.9, "PRESENTATION LAYER (TẦNG GIAO DIỆN)", fontsize=16.5, fontweight='bold', color=BLACK)
    
    boxes1 = [
        ("Razor Views (.cshtml)\nKhách hàng (Trắng kem #FAF7F2)", 1.0, 8.45, 3.7),
        ("Admin Dashboard\nQuản trị phim, phòng, lịch chiếu", 5.1, 8.45, 3.7),
        ("Staff Mobile UI\nHTML5 Camera QR Scanner", 9.2, 8.45, 3.7),
        ("Client Scripting\nTailwind CSS • Alpine.js • Timer", 13.3, 8.45, 3.3)
    ]
    for text, bx, by, bw in boxes1:
        ax.add_patch(FancyBboxPatch((bx, by), bw, 1.15, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=1.6))
        ax.text(bx + bw/2, by + 0.58, text, ha='center', va='center', fontsize=13.5, color=BLACK, fontweight='bold')

    # Arrow L1 -> L2
    ax.annotate("", xy=(8.75, 7.85), xytext=(8.75, 8.2),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=3.0))

    # Layer 2: Business Logic & Application Layer
    ax.add_patch(FancyBboxPatch((0.5, 5.0), 16.5, 2.55, boxstyle="round,pad=0.1,rounding_size=0.16", fc=VERY_LIGHT_GRAY, ec=BLACK, lw=2.4))
    ax.text(1.0, 7.1, "APPLICATION & BUSINESS LOGIC LAYER (TẦNG ĐIỀU KHIỂN & NGHIỆP VỤ)", fontsize=16.5, fontweight='bold', color=BLACK)

    boxes2 = [
        ("MVC Controllers\nBooking, Checkout, Staff,\nAdmin, Movie, Account", 1.0, 5.3, 3.7),
        ("Real-time Seat Engine\nKhóa ghế 10p, Check xung đột,\nTính tiền & Áp Voucher", 5.1, 5.3, 3.7),
        ("Background Worker\nSeatHoldTimeoutWorker\n(Quét tự động chu kỳ 30s)", 9.2, 5.3, 3.7),
        ("Security & Auth\nCookie Authentication,\nIdentity RBAC, Token QR", 13.3, 5.3, 3.3)
    ]
    for text, bx, by, bw in boxes2:
        ax.add_patch(FancyBboxPatch((bx, by), bw, 1.45, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=1.6))
        ax.text(bx + bw/2, by + 0.72, text, ha='center', va='center', fontsize=13.5, color=BLACK, fontweight='bold')

    # Arrow L2 -> L3
    ax.annotate("", xy=(8.75, 4.65), xytext=(8.75, 5.0),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=3.0))

    # Layer 3: Data Access & Infrastructure Layer
    ax.add_patch(FancyBboxPatch((0.5, 2.2), 16.5, 2.25, boxstyle="round,pad=0.1,rounding_size=0.16", fc=LIGHT_GRAY, ec=BLACK, lw=2.4))
    ax.text(1.0, 4.05, "DATA ACCESS & INFRASTRUCTURE LAYER (TẦNG TRUY CẬP DỮ LIỆU)", fontsize=16.5, fontweight='bold', color=BLACK)

    boxes3 = [
        ("Entity Framework Core\nCinemaDbContext • LINQ Queries\nFluent API Configurations", 1.0, 2.5, 3.8),
        ("MySQL Connector\nPomelo.EntityFrameworkCore.MySql\nutf8mb4_unicode_ci • Pooling", 5.2, 2.5, 3.8),
        ("Dual Provider Fallback\nMicrosoft.EntityFrameworkCore.Sqlite\n(Tùy chọn SQLite dự phòng)", 9.4, 2.5, 3.7),
        ("Single-file Publish\nCineManagement.exe (~60MB)\nTự động tích hợp Runtime", 13.5, 2.5, 3.1)
    ]
    for text, bx, by, bw in boxes3:
        ax.add_patch(FancyBboxPatch((bx, by), bw, 1.30, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=1.6))
        ax.text(bx + bw/2, by + 0.65, text, ha='center', va='center', fontsize=13.5, color=BLACK, fontweight='bold')

    # Bottom External Services
    ax.add_patch(FancyBboxPatch((0.5, 0.2), 16.5, 1.7, boxstyle="round,pad=0.1,rounding_size=0.16", fc=VERY_LIGHT_GRAY, ec=BLACK, lw=2.2))
    ax.text(1.0, 1.55, "EXTERNAL SERVICES & STORAGE (HẠ TẦNG LƯU TRỮ VÀ DỊCH VỤ NGOÀI)", fontsize=15.5, fontweight='bold', color=BLACK)

    boxes_ext = [
        ("MySQL / MariaDB Server\nPort 3306 (cinema_db)\nBảo toàn 100% dữ liệu", 1.0, 0.4, 3.8),
        ("Gmail SMTP Server\nsmtp.gmail.com:587 (TLS)\nTự động gửi vé điện tử", 5.2, 0.4, 3.8),
        ("Cổng thanh toán VietQR\nChuẩn Napas 247 tiện lợi\nThanh toán ví / ngân hàng", 9.4, 0.4, 3.7),
        ("Local Static Storage\n/uploads/posters (15 poster)\n/uploads/fnb (Combo)", 13.5, 0.4, 3.1)
    ]
    for text, bx, by, bw in boxes_ext:
        ax.add_patch(FancyBboxPatch((bx, by), bw, 1.0, boxstyle="round,pad=0.06", fc=WHITE, ec=BLACK, lw=1.6))
        ax.text(bx + bw/2, by + 0.50, text, ha='center', va='center', fontsize=13.2, color=BLACK, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, "fig15_architecture.png")
    fig.savefig(path, dpi=280, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {path}")

if __name__ == "__main__":
    print("Bắt đầu sinh toàn bộ các sơ đồ kỹ thuật chuẩn TRẮNG ĐEN (B&W / Grayscale)...")
    draw_fig1_scrum()
    process_jira_images()
    draw_fig6_usecase_overall()
    draw_fig7_usecase_auth()
    draw_fig8_usecase_movie_showtime()
    draw_fig9_usecase_booking()
    draw_fig10_usecase_ticket_report()
    draw_fig11_seq_booking()
    draw_fig12_seq_payment_email()
    draw_fig13_seq_scanner()
    draw_fig14_database_erd()
    draw_fig15_architecture()
    print("HOÀN THÀNH TẤT CẢ SƠ ĐỒ TRẮNG ĐEN THÀNH CÔNG RỰC RỠ!")
