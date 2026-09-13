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
# BẢNG MÀU CỦA TEMPLATE 3 (Vintage / Retro Style)
# ============================================================
C_SAND       = colors.Color(232/255, 216/255, 186/255)       # Vàng cát nền dưới
C_TEAL_DARK  = colors.Color(27/255, 75/255, 97/255)        # Xanh ngọc đậm (Viền, chữ)
C_TEAL_LIGHT = colors.Color(106/255, 156/255, 168/255)     # Xanh ngọc nhạt (Sóng)
C_ORANGE     = colors.Color(217/255, 83/255, 43/255)       # Cam đất (Chữ, Ribbon)
C_CREAM      = colors.Color(245/255, 240/255, 225/255)       # Trắng kem (Đổ bóng chữ)

def generate_pdf(
    bg_path, 
    title: str, 
    subtitle: str, 
    location: str, 
    output_path: str = None
) -> str:
    """
    Hàm render chuẩn của Template 3.
    """
    if not output_path:
        output_path = str(OUTPUT_DIR / "poster_template_3.pdf")

    W, H = CANVAS_WIDTH, CANVAS_HEIGHT
    c = canvas.Canvas(output_path, pagesize=(W, H))

    # ============================================================
    # 0. CHÈN ẢNH NỀN (Sử dụng hàm an toàn từ base)
    # ============================================================
    draw_background_image(c, bg_path, x=0, y=0, width=W, height=H)

    # ============================================================
    # 1. VẼ KHUNG VIỀN VINTAGE (Vintage Border)
    # ============================================================
    MARGIN = 40
    c.setStrokeColor(C_TEAL_DARK)
    
    # Viền ngoài (mỏng)
    c.setLineWidth(2)
    c.rect(MARGIN, MARGIN, W - 2*MARGIN, H - 2*MARGIN)
    
    # Viền trong (dày)
    MARGIN_IN = 55
    c.setLineWidth(4)
    c.rect(MARGIN_IN, MARGIN_IN, W - 2*MARGIN_IN, H - 2*MARGIN_IN)

    # Góc trang trí (Bo cung ở 4 góc)
    R = 25
    c.setLineWidth(3)
    c.arc(MARGIN_IN, H - MARGIN_IN - 2*R, MARGIN_IN + 2*R, H - MARGIN_IN, 90, 90) # Góc trái trên
    c.arc(W - MARGIN_IN - 2*R, H - MARGIN_IN - 2*R, W - MARGIN_IN, H - MARGIN_IN, 0, 90) # Góc phải trên
    c.arc(MARGIN_IN, MARGIN_IN, MARGIN_IN + 2*R, MARGIN_IN + 2*R, 180, 90) # Góc trái dưới
    c.arc(W - MARGIN_IN - 2*R, MARGIN_IN, W - MARGIN_IN, MARGIN_IN + 2*R, 270, 90) # Góc phải dưới

    # Đàn chim bay (Góc phải trên)
    c.setLineWidth(2)
    c.setStrokeColor(C_TEAL_DARK)
    for bx, by in [(950, 1650), (1030, 1680), (1080, 1620)]:
        p = c.beginPath()
        p.moveTo(bx, by)
        p.curveTo(bx+10, by+15, bx+20, by+15, bx+30, by)
        p.curveTo(bx+40, by+15, bx+50, by+15, bx+60, by-5)
        c.drawPath(p, fill=0, stroke=1)

    # ============================================================
    # 2. HEADER: TIÊU ĐỀ CHÍNH
    # ============================================================
    CENTER_X = W / 2
    
    # Chữ "Khám phá"
    c.setFont('Script', 70)
    c.setFillColor(C_TEAL_DARK)
    c.drawCentredString(CENTER_X, H - 180, "Khám phá")
    
    # Tia trang trí 2 bên chữ "Khám phá"
    c.setLineWidth(2)
    c.line(CENTER_X - 180, H - 150, CENTER_X - 130, H - 160)
    c.line(CENTER_X - 180, H - 170, CENTER_X - 140, H - 170)
    c.line(CENTER_X + 130, H - 160, CENTER_X + 180, H - 150)
    c.line(CENTER_X + 140, H - 170, CENTER_X + 180, H - 170)

    # Hàm vẽ chữ có viền offset (tạo hiệu ứng 3D/Retro)
    def draw_retro_text(text, y, font, size, fill_color):
        if not text: return
        c.setFont(font, size)
        # Lớp bóng/viền kem ở dưới
        c.setFillColor(C_CREAM)
        c.drawCentredString(CENTER_X - 6, y - 6, text)
        c.drawCentredString(CENTER_X + 6, y + 6, text)
        c.drawCentredString(CENTER_X + 6, y - 6, text)
        c.drawCentredString(CENTER_X - 6, y + 6, text)
        # Lớp màu chính ở trên
        c.setFillColor(fill_color)
        c.drawCentredString(CENTER_X, y, text)

    # Xử lý tự động cắt đôi Tiêu đề thành 2 hàng cho chuẩn layout Vintage
    title_text = (title or "ĐỒI CÁT QUANG PHÚ").upper()
    words = title_text.split()
    
    if len(words) >= 2:
        mid = len(words) // 2
        title1 = " ".join(words[:mid])
        title2 = " ".join(words[mid:])
        draw_retro_text(title1, H - 380, 'Title', 220, C_ORANGE)
        draw_retro_text(title2, H - 580, 'Title', 250, C_TEAL_DARK)
    else:
        # Nếu chỉ có 1 từ, in chính giữa
        draw_retro_text(title_text, H - 480, 'Title', 250, C_ORANGE)

    # ============================================================
    # 3. RIBBON (Dải băng chứa địa điểm)
    # ============================================================
    ry = H - 690
    rw = 500 # Chiều rộng ruy băng
    rh = 70  # Chiều cao ruy băng
    
    c.setFillColor(C_ORANGE)
    c.setStrokeColor(C_CREAM)
    c.setLineWidth(3)
    
    # Đuôi ruy băng trái
    c.line(CENTER_X - rw/2 - 40, ry + 15, CENTER_X - rw/2 + 20, ry + 15)
    p = c.beginPath()
    p.moveTo(CENTER_X - rw/2 + 20, ry + rh - 20)
    p.lineTo(CENTER_X - rw/2 - 60, ry + rh - 20)
    p.lineTo(CENTER_X - rw/2 - 20, ry + rh/2)
    p.lineTo(CENTER_X - rw/2 - 60, ry + 10)
    p.lineTo(CENTER_X - rw/2 + 20, ry + 10)
    c.drawPath(p, fill=1, stroke=1)

    # Đuôi ruy băng phải
    p = c.beginPath()
    p.moveTo(CENTER_X + rw/2 - 20, ry + rh - 20)
    p.lineTo(CENTER_X + rw/2 + 60, ry + rh - 20)
    p.lineTo(CENTER_X + rw/2 + 20, ry + rh/2)
    p.lineTo(CENTER_X + rw/2 + 60, ry + 10)
    p.lineTo(CENTER_X + rw/2 - 20, ry + 10)
    c.drawPath(p, fill=1, stroke=1)

    # Thân ruy băng chính
    c.rect(CENTER_X - rw/2, ry, rw, rh, fill=1, stroke=1)
    
    # Chữ trong Ribbon
    loc_text = (location or "CHƯA CÓ ĐỊA ĐIỂM").upper()
    c.setFillColor(colors.white)
    c.setFont('BodyBold', 40)
    c.drawCentredString(CENTER_X, ry + 20, f"• {loc_text} •")

    # ============================================================
    # 4. SUBTITLE DƯỚI RIBBON
    # ============================================================
    sub_text = subtitle or "Hành trình trở về với thiên nhiên nguyên sơ"
    c.setFillColor(C_TEAL_DARK)
    c.setFont('Script', 55)
    c.drawCentredString(CENTER_X, H - 780, sub_text)

    # ============================================================
    # 5. FOOTER WAVES (Tạo lớp sóng cát và nước biển ở đáy)
    # ============================================================
    def draw_wave(base_y, amplitude, frequency, phase, color):
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, base_y)
        for x in range(0, W + 10, 10):
            y = base_y + math.sin((x + phase) / frequency) * amplitude
            p.lineTo(x, y)
        p.lineTo(W, 0)
        p.close()
        c.setFillColor(color)
        c.drawPath(p, fill=1, stroke=0)

    # Sóng lớp sau
    draw_wave(350, 40, 90, 0, C_TEAL_DARK)
    # Sóng lớp giữa
    draw_wave(300, 35, 120, 150, C_TEAL_LIGHT)
    
    # Sóng cát màu vàng
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, 450)
    p.curveTo(300, 350, 500, 550, W, 250) 
    p.lineTo(W, 0)
    p.close()
    c.setFillColor(C_SAND)
    c.drawPath(p, fill=1, stroke=0)

    # Vẽ lại viền ở đè lên phần sóng (để giữ layout đóng khung)
    c.setStrokeColor(C_TEAL_DARK)
    c.setFillColor(colors.white)
    c.setLineWidth(4)
    c.rect(MARGIN_IN, MARGIN_IN, W - 2*MARGIN_IN, H - 2*MARGIN_IN, fill=0, stroke=1)
    c.setLineWidth(2)
    c.rect(MARGIN, MARGIN, W - 2*MARGIN, H - 2*MARGIN, fill=0, stroke=1)

    # ============================================================
    # 6. CỘT THÔNG TIN BÊN TRÁI FOOTER
    # ============================================================
    # 6. CỘT THÔNG TIN BÊN TRÁI FOOTER
    features = [
    "KHUNG CẢNH THIÊN NHIÊN HÙNG VĨ", # Thay cho sống ảo
    "KHÔNG GIAN NGUYÊN SƠ, YÊN BÌNH", # Thay cho bình minh/hoàng hôn
    "TRẢI NGHIỆM KHÁM PHÁ ĐỘC ĐÁO",   # Thay cho trượt cát
    "ĐIỂM ĐẾN KHÔNG THỂ BỎ LỠ"        # Giữ nguyên ý
    ]
    
    icon_x = 100
    text_x = 160
    start_y = 350
    gap = 70

    c.setFillColor(C_TEAL_DARK)
    c.setStrokeColor(C_TEAL_DARK)
    c.setFont('BodyBold', 26)

    for i, feature in enumerate(features):
        y = start_y - i * gap
        
        # Vẽ Icon giả lập đơn giản
        c.setLineWidth(3)
        if i == 0: # Camera
            c.roundRect(icon_x-20, y-10, 40, 28, 3, fill=0, stroke=1)
            c.circle(icon_x, y+4, 8, fill=0, stroke=1)
            c.circle(icon_x+12, y+10, 2, fill=1, stroke=0)
        elif i == 1: # Sun & Sea
            c.arc(icon_x-15, y, icon_x+15, y+30, 0, 180)
            c.line(icon_x-22, y, icon_x+22, y)
            c.line(icon_x-20, y-8, icon_x+20, y-8)
            for j in range(3):
                angle = math.radians(45 + j*45)
                c.line(icon_x + math.cos(angle)*18, y + math.sin(angle)*18,
                       icon_x + math.cos(angle)*26, y + math.sin(angle)*26)
        elif i == 2: # Mountain
            p = c.beginPath()
            p.moveTo(icon_x-20, y-10)
            p.lineTo(icon_x-5, y+15)
            p.lineTo(icon_x+5, y)
            p.lineTo(icon_x+15, y+10)
            p.lineTo(icon_x+25, y-10)
            c.drawPath(p, fill=0, stroke=1)
            c.line(icon_x-20, y-10, icon_x+25, y-10)
        elif i == 3: # Pin location
            c.circle(icon_x, y+5, 10, fill=0, stroke=1)
            p = c.beginPath()
            p.moveTo(icon_x-9, y+1)
            p.lineTo(icon_x, y-15)
            p.lineTo(icon_x+9, y+1)
            c.drawPath(p, fill=1, stroke=0)

        # Chữ Text
        c.drawString(text_x, y - 6, feature)

    # ============================================================
    # 7. CON DẤU TRÒN BÊN PHẢI (STAMP)
    # ============================================================
    cx, cy = 950, 230
    R_stamp = 160

    # Khung con dấu (2 lớp)
    c.setFillColor(C_SAND)
    c.setStrokeColor(C_CREAM)
    c.setLineWidth(10)
    c.circle(cx, cy, R_stamp, fill=1, stroke=1)
    
    c.setStrokeColor(C_TEAL_DARK)
    c.setLineWidth(3)
    c.circle(cx, cy, R_stamp - 5, fill=0, stroke=1)
    c.setLineWidth(1)
    c.circle(cx, cy, R_stamp - 15, fill=0, stroke=1)

    # Vẽ đồi cát cách điệu bên trong stamp
    p = c.beginPath()
    p.moveTo(cx - 140, cy - 50)
    p.curveTo(cx - 50, cy + 20, cx, cy - 30, cx + 140, cy - 60)
    p.lineTo(cx + 140, cy - 140)
    p.lineTo(cx - 140, cy - 140)
    c.setFillColor(C_ORANGE)
    c.drawPath(p, fill=1, stroke=0)

    p = c.beginPath()
    p.moveTo(cx - 140, cy - 100)
    p.curveTo(cx - 50, cy - 20, cx + 50, cy - 10, cx + 140, cy - 120)
    p.lineTo(cx + 140, cy - 140)
    p.lineTo(cx - 140, cy - 140)
    c.setFillColor(C_TEAL_DARK)
    c.drawPath(p, fill=1, stroke=0)

    # Mặt trời trong stamp
    c.setFillColor(C_CREAM)
    c.circle(cx - 60, cy - 10, 25, fill=1, stroke=0)

    # Chữ trong Stamp
    c.setFillColor(C_ORANGE)
    c.setFont('Script', 75)
    
    stamp_loc = loc_text.title() if len(loc_text) <= 12 else "Đi là mê!"
    c.drawCentredString(cx, cy + 40, stamp_loc)
    
    c.setFillColor(C_TEAL_DARK)
    c.setFont('Title', 65)
    c.drawCentredString(cx, cy - 20, "ĐI LÀ MÊ!")

    c.save()
    return output_path