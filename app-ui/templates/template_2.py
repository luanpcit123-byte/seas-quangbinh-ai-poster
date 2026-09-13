import math
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ⚡ Import nền tảng từ base.py
from templates.base import (
    CANVAS_WIDTH, 
    CANVAS_HEIGHT, 
    OUTPUT_DIR, 
    draw_background_image
)

# ============================================================
# BẢNG MÀU CỦA TEMPLATE 2 (Postcard)
# ============================================================
C_BG           = colors.HexColor("#F7F2E8")
C_TITLE        = colors.HexColor("#556B2F")   # Olive Green
C_TEXT         = colors.HexColor("#70543B")
C_LINE         = colors.HexColor("#B8A58A")
C_ACCENT       = colors.HexColor("#C89B3C")
C_STAMP_BG     = colors.Color(.93, .86, .72)
C_ADDRESS_LINE = colors.Color(.7, .6, .5)
C_WHITE        = colors.white


def draw_postmark(c: canvas.Canvas, x: float, y: float) -> None:
    c.setStrokeColor(C_ACCENT)
    c.circle(x, y, 55)
    c.circle(x, y, 49)
    c.setFont("Body", 14)
    c.drawCentredString(x, y+18, "VIET NAM")
    c.drawCentredString(x, y-22, "QUANG BINH")
    for i in range(3):
        yy = y + 20 - i*18
        p = c.beginPath()
        first = True
        for xx in range(int(x+65), int(x+170), 4):
            yw = yy + math.sin(xx/12)*3
            if first:
                p.moveTo(xx, yw)
                first = False
            else:
                p.lineTo(xx, yw)
        c.drawPath(p)


def draw_stamp(c: canvas.Canvas, x: float, y: float) -> None:
    s = 90
    c.setStrokeColor(C_LINE)
    step = 8
    for i in range(12):
        c.rect(x+i*step, y+s, step, 6)
        c.rect(x+i*step, y-6, step, 6)
        c.rect(x-6, y+i*step, 6, step)
        c.rect(x+s, y+i*step, 6, step)
        
    c.setFillColor(C_STAMP_BG)
    c.rect(x, y, s, s, fill=1, stroke=1)
    
    c.setFillColor(C_ACCENT)
    c.setFont("BodyBold", 18)
    c.drawCentredString(x+s/2, y+50, "QB")
    c.setFont("Body", 11)
    c.drawCentredString(x+s/2, y+28, "KỲ")
    c.drawCentredString(x+s/2, y+14, "QUAN")


def generate_pdf(
    bg_path, 
    title: str, 
    subtitle: str, 
    location: str, 
    output_path: str = None
) -> str:
    """
    Hàm render chính của Template 2 (Postcard).
    """
    if not output_path:
        output_path = str(OUTPUT_DIR / "poster_template_2.pdf")

    W, H = CANVAS_WIDTH, CANVAS_HEIGHT
    c = canvas.Canvas(output_path, pagesize=(W, H))

    # ============================================================
    # VẼ NỀN POSTCARD
    # ============================================================
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    margin = 70

    # 1. Outer postcard (Bo tròn 4 góc)
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(3)
    c.roundRect(margin, margin, W-2*margin, H-2*margin, 16)

    # 2. Vùng khung ảnh (Image frame)
    img_x = 110
    img_y = 760
    img_w = 980
    img_h = 880

    # Nền trắng cho khung ảnh
    c.setFillColor(C_WHITE)
    c.roundRect(img_x-12, img_y-12, img_w+24, img_h+24, 10, fill=1, stroke=0)

    # ============================================================
    # 3. CHÈN ẢNH NỀN (Vào trong khung)
    # ============================================================
    draw_background_image(c, bg_path, x=img_x, y=img_y, width=img_w, height=img_h)

    # ============================================================
    # 4. TITLE & SUBTITLE
    # ============================================================
    display_title = title or "TIÊU ĐỀ"
    c.setFillColor(C_TITLE)
    c.setFont("Title", 110)
    c.drawString(110, 620, display_title.upper())

    c.setFillColor(C_ACCENT)
    c.setFont("Body", 34)
    if subtitle:
        c.drawString(115, 575, subtitle)

    # Divider ngang
    c.line(100, 540, 1100, 540)

    # ============================================================
    # 5. QUOTE
    # ============================================================
    c.setFont("Script", 46)
    c.drawString(110, 480, '"Mỗi bước chân đều kể')
    c.drawString(170, 430, 'một câu chuyện phiêu lưu."')

    # ============================================================
    # 6. ADDRESS SECTION (Destination)
    # ============================================================
    # Đường thẳng đứng chia đôi
    c.line(760, 505, 760, 170)
    
    c.setFont("BodyBold", 22)
    c.drawString(800, 470, "DESTINATION")
    
    c.setFont("Body", 20)
    loc = location or "QUẢNG BÌNH - VIỆT NAM"
    c.drawString(800, 435, loc.upper())

    # Kẻ các dòng địa chỉ
    for i in range(4):
        yy = 360 - i*55
        c.setStrokeColor(C_ADDRESS_LINE)
        c.line(800, yy, 1090, yy)

    # ============================================================
    # 7. FOOTER SLOGAN
    # ============================================================
    c.setFont("Script", 54)
    c.setFillColor(C_ACCENT)
    c.drawCentredString(W/2, 95, f"Đến {display_title.title()} - Chạm vào tự do!")

    # ============================================================
    # 8. POSTMARK & STAMP
    # ============================================================
    draw_postmark(c, 900, 220)
    draw_stamp(c, 130, 145)

    c.save()
    
    return output_path