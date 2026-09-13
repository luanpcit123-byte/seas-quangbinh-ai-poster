import math
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ⚡ Import các thành phần nền tảng từ base.py
from templates.base import (
    CANVAS_WIDTH, 
    CANVAS_HEIGHT, 
    OUTPUT_DIR, 
    draw_background_image
)

# ============================================================
# BẢNG MÀU CỦA TEMPLATE 1
# ============================================================
C_BEIGE  = colors.Color(244/255, 239/255, 230/255)
C_NAVY   = colors.Color(21/255, 48/255, 85/255)
C_BROWN  = colors.Color(100/255, 65/255, 35/255)
C_SHADOW = colors.Color(0, 0, 0, alpha=0.3)
C_WHITE  = colors.white
C_LINE   = colors.Color(200/255, 180/255, 150/255)


def generate_pdf(
    bg_path, 
    title: str, 
    subtitle: str, 
    location: str, 
    output_path: str = None
) -> str:
    if not output_path:
        output_path = str(OUTPUT_DIR / "poster_template_1.pdf")

    W, H = CANVAS_WIDTH, CANVAS_HEIGHT
    c = canvas.Canvas(output_path, pagesize=(W, H))

    # ============================================================
    # 0. CHÈN ẢNH NỀN (An toàn)
    # ============================================================
    draw_background_image(c, bg_path, x=0, y=0, width=W, height=H)

    # ============================================================
    # 1. HEADER & FOOTER MÀU KEM (Sóng nước)
    # ============================================================
    SIDE_MARGIN = 0
    
    # --- Header ---
    c.setFillColor(C_BEIGE)
    c.setStrokeColor(C_BEIGE)
    top_base = H * 0.20
    path = c.beginPath()
    path.moveTo(SIDE_MARGIN, H)
    path.lineTo(W - SIDE_MARGIN, H)
    for x in range(W - SIDE_MARGIN, SIDE_MARGIN - 1, -2):
        y = top_base + math.sin(x / 90) * 10 + math.cos(x / 45) * 5
        path.lineTo(x, H - y)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    
    # --- Footer --- (Đã cố định tọa độ tuyệt đối nằm giữa Location và vạch ngang)
    bottom_base = H - 1360
    path = c.beginPath()
    path.moveTo(SIDE_MARGIN, bottom_base)
    for x in range(SIDE_MARGIN, W - SIDE_MARGIN + 1, 2):
        y = bottom_base + math.sin(x / 75) * 8 + math.cos(x / 38) * 4
        path.lineTo(x, y)
    path.lineTo(W - SIDE_MARGIN, 0)
    path.lineTo(SIDE_MARGIN, 0)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    # ============================================================
    # 2. TOP SECTION
    # ============================================================
    # 1. Chữ "Khám phá" (Đã hạ xuống)
    c.setFillColor(C_BROWN)
    c.setFont('Script', 110)
    c.drawString(100, H - 210, "Khám phá")

    # 2. Tiêu đề chính (Đã hạ xuống để vắt lửng trên giấy rách)
    c.setFillColor(C_NAVY)
    c.setFont('Title', 180) 
    title1_text = (title or "QUẢNG BÌNH").upper()
    c.drawString(120, H - 390, title1_text)

    # 3. Phụ đề (Đã hạ xuống)
    sub_text = subtitle or "Vương quốc của những kỳ quan thiên nhiên"
    sub_y = H - 480
    c.setFillColor(C_SHADOW)
    c.setFont('Body', 34)
    c.drawString(130, sub_y - 3, f"• {sub_text.upper()} •")
    c.setFillColor(C_BROWN)
    c.drawString(130, sub_y, f"• {sub_text.upper()} •")

    # --- STAMP (Con dấu hải quan) ---
    cx, cy = 980, H - 300 # Đã hạ xuống đồng bộ với text
    r = 85
    c.setStrokeColor(C_BROWN)
    c.setLineWidth(3)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setLineWidth(1)
    c.circle(cx, cy, r-8, fill=0, stroke=1)

    c.setFont('Body', 16)
    c.drawCentredString(cx, cy - 55 - 16*0.35, "QUẢNG BÌNH")
    c.drawCentredString(cx, cy + 55 - 16*0.35, "VIỆT NAM")

    c.setLineWidth(2)
    p = c.beginPath()
    p.moveTo(cx - 50, cy - 15)
    p.lineTo(cx - 20, cy + 15)
    p.lineTo(cx + 10, cy - 15)
    p.lineTo(cx + 30, cy + 5)
    p.lineTo(cx + 60, cy - 15)
    c.drawPath(p, fill=1, stroke=0) 

    for i in range(3):
        rl_y_base = cy + 20 - i * 20
        p = c.beginPath()
        first = True
        for x in range(cx + r + 15, cx + r + 180, 5):
            y_w = rl_y_base - math.sin(x / 15) * 6
            if first: 
                p.moveTo(x, y_w)
                first = False
            else: 
                p.lineTo(x, y_w)
        c.drawPath(p, fill=0, stroke=1)

    # ============================================================
    # 3. MIDDLE SECTION (QUOTE)
    # ============================================================
    quote_lines = [
        '"Nơi đất trời', 
        'giao hòa tuyệt mỹ,', 
        'chạm vào tự do', 
        'và bình yên."'
    ]
    q_x, q_y_pillow = 800, 1050 
    font_size, line_height = 55, 75

    c.setFont('Script', font_size)
    c.setFillColor(C_SHADOW)
    for i, line in enumerate(quote_lines):
        c.drawString(q_x + 3, H - (q_y_pillow + i * line_height) - font_size*0.75 - 3, line)
        
    c.setFillColor(C_WHITE)
    for i, line in enumerate(quote_lines):
        c.drawString(q_x, H - (q_y_pillow + i * line_height) - font_size*0.75, line)

    # ============================================================
    # 4. BOTTOM SECTION (Pin, Thông tin địa danh)
    # ============================================================
    rl_bottom_y = H - 1310 
    pin_x, pin_y, r_pin = 120, rl_bottom_y - 5, 18
    
    c.setFillColor(C_BROWN)
    c.setStrokeColor(C_BROWN)
    c.circle(pin_x, pin_y, r_pin, fill=1, stroke=0)
    
    tail = c.beginPath()
    tail.moveTo(pin_x - r_pin * 0.65, pin_y - r_pin * 0.4)
    tail.lineTo(pin_x + r_pin * 0.65, pin_y - r_pin * 0.4)
    tail.lineTo(pin_x, pin_y - r_pin * 2.3)
    tail.close()
    c.drawPath(tail, fill=1, stroke=0)
    
    c.setFillColor(C_BEIGE)
    c.circle(pin_x, pin_y, r_pin * 0.42, fill=1, stroke=0)
    
    text_x = 155
    c.setFillColor(C_BROWN)
    c.setFont("BodyBold", 34)
    c.drawString(text_x, pin_y + 22 - 34 * 0.75, title1_text)
    
    loc_display = (location or "QUẢNG BÌNH - VIỆT NAM").upper()
    c.setFont("Body", 22)
    c.drawString(text_x, pin_y - 20 - 22 * 0.75, loc_display)
    
    c.setStrokeColor(C_LINE)
    c.setLineWidth(1.5)
    c.line(90, rl_bottom_y - 80, W - 90, rl_bottom_y - 80)

    # ============================================================
    # 5. ICONS VÀ CỘT TEXT
    # ============================================================
    spacing, start_x = 280, 200 
    icon_y = rl_bottom_y - 140
    c.setStrokeColor(C_BROWN)
    c.setFillColor(C_BROWN)

    c.setLineWidth(3)
    c.circle(start_x, icon_y, 15, fill=0, stroke=1)
    for i in range(8):
        angle = i * (math.pi / 4)
        c.line(start_x + math.cos(angle)*20, icon_y + math.sin(angle)*20,
               start_x + math.cos(angle)*30, icon_y + math.sin(angle)*30)

    cx = start_x + spacing
    c.roundRect(cx-25, icon_y-18, 50, 36, 5, fill=0, stroke=1)
    c.circle(cx, icon_y, 10, fill=0, stroke=1)
    c.rect(cx-8, icon_y+18, 16, 6, fill=1, stroke=0)

    cx += spacing
    c.line(cx-25, icon_y+10, cx+15, icon_y+10)
    c.arc(cx+5, icon_y+5, cx+25, icon_y+15, 270, 180)
    c.line(cx-15, icon_y, cx+25, icon_y)
    c.arc(cx+15, icon_y-5, cx+35, icon_y+5, 270, 180)
    c.line(cx-20, icon_y-10, cx+5, icon_y-10)
    c.arc(cx-5, icon_y-15, cx+15, icon_y-5, 270, 180)

    cx += spacing
    c.setLineWidth(3)
    c.ellipse(cx-15, icon_y-15, cx-5, icon_y+10, fill=0, stroke=1)
    c.setLineWidth(2)
    c.ellipse(cx-16, icon_y+14, cx-10, icon_y+22, fill=0, stroke=1)
    c.ellipse(cx-9, icon_y+15, cx-5, icon_y+20, fill=0, stroke=1)
    c.setLineWidth(3)
    c.ellipse(cx+5, icon_y-10, cx+15, icon_y+15, fill=0, stroke=1)
    c.setLineWidth(2)
    c.ellipse(cx+10, icon_y+19, cx+16, icon_y+27, fill=0, stroke=1)
    c.ellipse(cx+5, icon_y+20, cx+9, icon_y+25, fill=0, stroke=1)

    cols = [
        ("CẢNH SẮC HOANG SƠ", ["Vẻ đẹp kiệt tác", "ban tặng bởi thiên nhiên."]),
        ("CHECK-IN ĐỘC ĐÁO", ["Lưu giữ những khoảnh khắc", "ấn tượng và đáng nhớ."]),
        ("KHÔNG KHÍ TRONG LÀNH", ["Không gian bình yên,", "thư giãn trọn vẹn."]),
        ("TRẢI NGHIỆM HẤP DẪN", ["Hành trình khám phá", "vô vàn điều bất ngờ."])
    ]

    text_y_rl = icon_y - 50
    for i, (col_title, lines) in enumerate(cols):
        cx = start_x + spacing * i
        c.setFillColor(C_BROWN)
        
        c.setFont('BodyBold', 18) 
        c.drawCentredString(cx, text_y_rl - 18*0.35, col_title)

        c.setFont('Body', 16)
        for j, line in enumerate(lines):
            c.drawCentredString(cx, text_y_rl - 30 - j*22 - 16*0.35, line)

        if i > 0:
            c.setStrokeColor(C_LINE)
            x_line = cx - (spacing / 2)
            c.line(x_line, icon_y + 20, x_line, text_y_rl - 80)

    # ============================================================
    # 6. FOOTER SLOGAN CUỐI TRANG
    # ============================================================
    rl_fy = H - 1680
    display_title = (title or "Quảng Bình").title()
    footer_text = f"Đến {display_title} — Khám phá kỳ quan!"
    
    c.setFont('Script', 60)
    c.setFillColor(C_BROWN)
    
    c.drawCentredString(W/2, rl_fy - 12 - 60*0.35, footer_text)

    # Đã nới rộng tọa độ 2 bên để không đâm vào chữ
    c.setStrokeColor(C_BROWN)
    c.setLineWidth(2)
    c.line(W/2 - 500, rl_fy, W/2 - 400, rl_fy)
    c.line(W/2 + 400, rl_fy, W/2 + 500, rl_fy)

    c.setLineWidth(1)
    c.line(W/2 - 490, rl_fy + 10, W/2 - 410, rl_fy + 10)
    c.line(W/2 + 410, rl_fy + 10, W/2 + 490, rl_fy + 10)

    c.save()
    return output_path