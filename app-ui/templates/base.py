import os
import math
from pathlib import Path
from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

# ============================================================
# CẤU HÌNH ĐƯỜNG DẪN DÙNG CHUNG
# ============================================================
CURRENT_DIR = Path(__file__).parent  # Thư mục templates/
ROOT_DIR = CURRENT_DIR.parent        # Thư mục gốc dự án
FONTS_DIR = ROOT_DIR / "fonts"
OUTPUT_DIR = ROOT_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# ĐĂNG KÝ FONT CHUNG (Chỉ thực hiện 1 lần duy nhất)
# ============================================================
_fonts_registered = False

def init_fonts():
    global _fonts_registered
    if not _fonts_registered:
        try:
            pdfmetrics.registerFont(TTFont("Title", str(FONTS_DIR / "Anton-Regular.ttf")))
            pdfmetrics.registerFont(TTFont("Body", str(FONTS_DIR / "NotoSans-Regular.ttf")))
            pdfmetrics.registerFont(TTFont("BodyBold", str(FONTS_DIR / "NotoSans-Bold.ttf")))
            pdfmetrics.registerFont(TTFont("Script", str(FONTS_DIR / "GreatVibes-Regular.ttf")))
            _fonts_registered = True
        except Exception as e:
            print(f"[Warning] Lỗi đăng ký font trong base: {e}")

# Gọi đăng ký font ngay khi module base được nạp
init_fonts()

# ============================================================
# HẰNG SỐ KÍCH THƯỚC CHUẨN
# ============================================================
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1800

# ============================================================
# HÀM VẼ ẢNH NỀN AN TOÀN TUYỆT ĐỐI
# ============================================================
def draw_background_image(c, bg, x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, preserve_aspect=False):
    """
    Hàm vẽ ảnh nền an toàn cho cả PIL.Image, String Path, và Pathlib.
    Không bao giờ gây lỗi TypeError với os.path.exists.
    """
    if bg is None:
        return

    try:
        # Trường hợp 1: Ảnh PIL (RAM)
        if isinstance(bg, Image.Image):
            img_reader = ImageReader(bg)
            c.drawImage(img_reader, x, y, width=width, height=height, preserveAspectRatio=preserve_aspect)
        
        # Trường hợp 2: Đường dẫn File (string/Path)
        elif isinstance(bg, (str, Path)):
            if os.path.exists(bg):
                c.drawImage(str(bg), x, y, width=width, height=height, preserveAspectRatio=preserve_aspect)
            else:
                print(f"[Warning] File ảnh không tồn tại: {bg}")
        
        # Trường hợp 3: Fallback các dạng stream khác
        else:
            img_reader = ImageReader(bg)
            c.drawImage(img_reader, x, y, width=width, height=height, preserveAspectRatio=preserve_aspect)
    except Exception as e:
        print(f"[Error] Không thể vẽ ảnh nền: {e}")