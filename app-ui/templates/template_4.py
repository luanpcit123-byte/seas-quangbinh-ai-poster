import math
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ⚡ Kế thừa cấu trúc chuẩn từ base.py
from templates.base import (
    CANVAS_WIDTH, 
    CANVAS_HEIGHT, 
    OUTPUT_DIR, 
    draw_background_image
)

# ============================================================
# BẢNG MÀU CỦA TEMPLATE 4 (Cảm hứng thiên nhiên)
# ============================================================
C_GOLD       = colors.Color(204/255, 163/255, 82/255)       # Vàng đồng
C_OLIVE      = colors.Color(135/255, 149/255, 76/255)       # Xanh rêu (Chữ PHONG NHA)
C_DARK_GREEN = colors.Color(35/255, 48/255, 33/255)         # Xanh lục đậm (Footer, Icon)
C_BEIGE      = colors.Color(228/255, 215/255, 186/255)      # Giấy nhám/kem
C_WHITE      = colors.white

def generate_pdf(
    bg_path, 
    title: str, 
    subtitle: str, 
    location: str, 
    output_path: str = None
) -> str:
    """
    Hàm render chính của Template 4.
    """
    if not output_path:
        output_path = str(OUTPUT_DIR / "poster_template_4.pdf")

    W, H = CANVAS_WIDTH, CANVAS_HEIGHT
    c = canvas.Canvas(output_path, pagesize=(W, H))

    # ============================================================
    # 0. CHÈN ẢNH NỀN (An toàn)
    # ============================================================
    # Tạo nền xám phòng trường hợp không có ảnh nền (Fallback)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    
    # Vẽ ảnh nền đè lên (nếu có)
    draw_background_image(c, bg_path, x=0, y=0, width=W, height=H)

    # ============================================================
    # 1. PHẦN TYPOGRAPHY NỬA TRÊN (LEFT ALIGNED)
    # ============================================================
    LEFT_MARGIN = 80

    # Tiêu đề nhỏ (Script)
    c.setFillColor(C_GOLD)
    c.setFont('Script', 70)
    c.drawString(LEFT_MARGIN, H - 150 + 50, "Khám phá kỳ quan thiên nhiên")

    # Điểm nhấn kim cương nhỏ dưới chữ Script
    diamond_y = H - 180 + 50
    p = c.beginPath()
    p.moveTo(LEFT_MARGIN + 250, diamond_y)
    p.lineTo(LEFT_MARGIN + 260, diamond_y + 10)
    p.lineTo(LEFT_MARGIN + 270, diamond_y)
    p.lineTo(LEFT_MARGIN + 260, diamond_y - 10)
    c.drawPath(p, fill=1, stroke=0)
    
    # Line 2 bên kim cương
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(2)
    c.line(LEFT_MARGIN + 150, diamond_y, LEFT_MARGIN + 230, diamond_y)
    c.line(LEFT_MARGIN + 290, diamond_y, LEFT_MARGIN + 370, diamond_y)

    # Logic tách Tiêu đề (VD: "ĐỘNG PHONG NHA" -> "ĐỘNG" và "PHONG NHA")
    title_text = (title or "ĐỘNG PHONG NHA").upper()
    words = title_text.split()
    if len(words) >= 2:
        t1 = words[0]
        t2 = " ".join(words[1:])
    else:
        t1 = title_text
        t2 = ""

    # Chữ Dòng 1 (Màu trắng ngà - Ví dụ: ĐỘNG)
    c.setFillColor(colors.Color(0.95, 0.95, 0.92))
    c.setFont('Title', 220)
    c.drawString(LEFT_MARGIN, H - 380, t1)

    # Chữ Dòng 2 (Màu xanh rêu - Ví dụ: PHONG NHA)
    if t2:
        c.setFillColor(C_OLIVE)
        c.setFont('Title', 220)
        c.drawString(LEFT_MARGIN, H - 580, t2)

    # Logic Địa điểm
    loc_text = (location or "QUẢNG BÌNH - VIỆT NAM").upper()

    # Banner vệt sơn/giấy rách chứa Location
    banner_y = H - 650
    c.setFillColor(C_GOLD)
    bg_banner = c.beginPath()
    bg_banner.moveTo(LEFT_MARGIN - 20, banner_y + 40)
    bg_banner.lineTo(LEFT_MARGIN + 650, banner_y + 45)  # Kéo dài hơn để chứa text dài
    bg_banner.lineTo(LEFT_MARGIN + 680, banner_y + 20)
    bg_banner.lineTo(LEFT_MARGIN + 640, banner_y - 10)
    bg_banner.lineTo(LEFT_MARGIN - 40, banner_y - 15)
    bg_banner.lineTo(LEFT_MARGIN - 30, banner_y + 15)
    bg_banner.close()
    c.drawPath(bg_banner, fill=1, stroke=0)

    # Text trong banner
    c.setFillColor(C_DARK_GREEN)
    c.setFont('BodyBold', 28)
    c.drawString(LEFT_MARGIN + 20, banner_y + 8, f"— {loc_text} —")

    # Đoạn text Highlight
    text_y = H - 780
    c.setFillColor(C_OLIVE)
    c.setFont('BodyBold', 35)
    c.drawString(LEFT_MARGIN, text_y, "ĐIỂM ĐẾN LÝ TƯỞNG")
    
    c.setFillColor(C_GOLD)
    c.drawString(LEFT_MARGIN, text_y - 45, "QUẢNG BÌNH")

    # Đoạn văn bản mô tả 
    desc_lines = [
        "Nơi tạo hóa ân cần ban tặng vẻ đẹp",
        "nguyên sơ và tráng lệ bậc nhất,",
        "kiến tạo nên những kiệt tác",
        "trường tồn mãi cùng thời gian."
    ]
    c.setFillColor(C_WHITE)
    c.setFont('Body', 24)
    for i, line in enumerate(desc_lines):
        c.drawString(LEFT_MARGIN, text_y - 130 - (i * 35), line)

    # ============================================================
    # 2. FOOTER GIẤY RÁCH MÀU KEM (Mô phỏng đồi núi / giấy xé)
    # ============================================================
    footer_height = H * 0.32
    
    c.setFillColor(C_BEIGE)
    path = c.beginPath()
    path.moveTo(W, 0)
    path.lineTo(0, 0)
    path.lineTo(0, footer_height)
    
    for x in range(0, W + 1, 3):
        y = (
            footer_height
            + math.sin(x / 40) * 12   # Sóng chính
            + math.cos(x / 15) * 6    # Sóng phụ 1 (tạo độ nhiễu)
            + math.sin(x / 8) * 3     # Sóng phụ 2 (tạo răng cưa nhỏ)
        )
        path.lineTo(x, y)
        
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    # Viền đậm nhẹ cho phần rách
    c.setStrokeColorRGB(0.8, 0.75, 0.6)
    c.setLineWidth(1.5)
    path_edge = c.beginPath()
    path_edge.moveTo(0, footer_height)
    for x in range(0, W + 1, 2):
        y = footer_height + math.sin(x/40)*12 + math.cos(x/15)*6 + math.sin(x/8)*3
        if x == 0: path_edge.moveTo(x, y)
        else: path_edge.lineTo(x, y)
    c.drawPath(path_edge, fill=0, stroke=1)

    # ============================================================
    # 3. NỘI DUNG TRÊN NỀN GIẤY KEM
    # ============================================================
    # Logic Subtitle (Dùng cho Quote chữ ký)
    sub_text = subtitle or "Vẻ đẹp nguyên sơ — Trải nghiệm bất tận"
    
    c.setFillColor(C_DARK_GREEN)
    c.setFont('Script', 75)
    c.drawCentredString(W / 2, footer_height - 120, sub_text)

    # Các gạch ngang trang trí nhỏ dưới chữ ký
    diamond_y_2 = footer_height - 150
    c.setStrokeColor(C_DARK_GREEN)
    c.setLineWidth(1)
    c.line(W/2 - 250, diamond_y_2, W/2 + 250, diamond_y_2)
    for dx in [-100, 100]:
        p = c.beginPath()
        p.moveTo(W/2 + dx, diamond_y_2 + 5)
        p.lineTo(W/2 + dx + 5, diamond_y_2)
        p.lineTo(W/2 + dx, diamond_y_2 - 5)
        p.lineTo(W/2 + dx - 5, diamond_y_2)
        c.drawPath(p, fill=1, stroke=0)

    # -- 3 Cột Features --
    # -- 3 Cột Features --
    features = [
    ("KỲ QUAN THIÊN NHIÊN", ["Vẻ đẹp hoang sơ,", "cảnh sắc tráng lệ."]),
    ("DẤU ẤN BẢN ĐỊA", ["Hòa mình vào không gian", "yên bình và tĩnh lặng."]), # Đổi từ sông ngầm
    ("ĐIỂM ĐẾN TUYỆT VỜI", ["Hành trình khám phá", "tràn đầy cảm hứng."])
    ]
    
    col_width = W / 3
    icon_radius = 45
    base_y = footer_height - 280

    for i, (feat_title, lines) in enumerate(features):
        cx = (i * col_width) + (col_width / 2)
        
        c.setFillColor(C_DARK_GREEN)
        c.circle(cx - 120, base_y + 20, icon_radius, fill=1, stroke=0)
        
        c.setFillColor(C_BEIGE)
        if i == 0:
            p = c.beginPath()
            p.moveTo(cx - 145, base_y)
            p.lineTo(cx - 125, base_y + 35)
            p.lineTo(cx - 110, base_y + 10)
            p.lineTo(cx - 95, base_y + 25)
            p.lineTo(cx - 85, base_y)
            c.drawPath(p, fill=1, stroke=0)
        elif i == 1:
            c.setStrokeColor(C_BEIGE)
            c.setLineWidth(4)
            for wave_y in [base_y + 30, base_y + 15, base_y]:
                p = c.beginPath()
                p.moveTo(cx - 145, wave_y)
                p.lineTo(cx - 135, wave_y + 8)
                p.lineTo(cx - 125, wave_y - 2)
                p.lineTo(cx - 115, wave_y + 8)
                p.lineTo(cx - 105, wave_y - 2)
                p.lineTo(cx - 95, wave_y + 8)
                c.drawPath(p, fill=0, stroke=1)
        elif i == 2:
            p = c.beginPath()
            pin_x = cx - 120
            pin_y = base_y + 15
            p.moveTo(pin_x, pin_y - 25)
            p.lineTo(pin_x + 18, pin_y + 5)
            p.arcTo(pin_x - 18, pin_y - 5, pin_x + 18, pin_y + 30, 0, 180)
            p.lineTo(pin_x - 18, pin_y + 5)
            p.close()
            c.drawPath(p, fill=1, stroke=0)
            c.setFillColor(C_DARK_GREEN)
            c.circle(pin_x, pin_y + 12, 6, fill=1, stroke=0)

        # Draw Text
        text_start_x = cx - 50
        c.setFillColor(C_DARK_GREEN)
        c.setFont('BodyBold', 20)
        c.drawString(text_start_x, base_y + 25, feat_title)
        
        c.setFont('Body', 18)
        c.drawString(text_start_x, base_y - 5, lines[0])
        c.drawString(text_start_x, base_y - 30, lines[1])

        if i < 2:
            c.setStrokeColor(C_DARK_GREEN)
            c.setLineWidth(1)
            c.line(cx + (col_width/2), base_y + 50, cx + (col_width/2), base_y - 50)

    # ============================================================
    # 4. THANH BOTTOM BAR MÀU XANH LỤC ĐẬM
    # ============================================================
    bar_height = 160
    c.setFillColor(C_DARK_GREEN)
    c.rect(0, 0, W, bar_height, fill=1, stroke=0)

    # --- Khối Trái: Địa điểm ---
    c.setFillColor(C_GOLD)
    pin_small_x = LEFT_MARGIN
    pin_small_y = 70
    p = c.beginPath()
    p.moveTo(pin_small_x, pin_small_y - 20)
    p.lineTo(pin_small_x + 12, pin_small_y)
    p.arcTo(pin_small_x - 12, pin_small_y - 12, pin_small_x + 12, pin_small_y + 12, 0, 180)
    p.lineTo(pin_small_x - 12, pin_small_y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(C_DARK_GREEN)
    c.circle(pin_small_x, pin_small_y + 4, 4, fill=1, stroke=0)

    c.setFillColor(C_BEIGE)
    c.setFont('BodyBold', 22)
    c.drawString(LEFT_MARGIN + 30, 80, loc_text)
    c.setFont('Body', 20)
    c.drawString(LEFT_MARGIN + 30, 50, "Việt Nam")

    # --- Khối Giữa: Tên Location dạng nghệ thuật ---
    center_y = 80
    c.setFillColor(C_GOLD)
    c.setFont('Script', 70)
    c.drawCentredString(W/2, center_y, title_text.title())
    
    c.setFont('Body', 22)
    c.drawCentredString(W/2, center_y - 45, "VẺ ĐẸP BẤT TẬN")

    # Họa tiết 2 bên
    c.setStrokeColor(C_GOLD)
    c.setLineWidth(1.5)
    c.line(W/2 - 250, center_y + 15, W/2 - 130, center_y + 15)
    c.circle(W/2 - 130, center_y + 15, 3, fill=1, stroke=1)
    
    c.line(W/2 + 130, center_y + 15, W/2 + 250, center_y + 15)
    c.circle(W/2 + 130, center_y + 15, 3, fill=1, stroke=1)

    # --- Khối Phải: Text thay cho QR ---
    RIGHT_MARGIN = W - 80
    qr_x = RIGHT_MARGIN - 300
    qr_y = 45

    c.setFillColor(C_BEIGE)
    c.setFont('BodyBold', 22)
    c.drawString(qr_x + 90, qr_y + 40, "TÌM HIỂU THÊM")
    c.setFont('Body', 18)
    c.drawString(qr_x + 90, qr_y + 15, "quangbinhtourism.vn")

    c.save()
    return output_path