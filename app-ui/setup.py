import subprocess
import sys
import os
import urllib.request

def install_libraries():
    """
    Cài đặt các thư viện cần thiết để sinh ảnh bằng FLUX và LoRA.
    Sử dụng các thư viện phổ biến nhất cho tác vụ này.
    """
    print("=== BƯỚC 1: CÀI ĐẶT THƯ VIỆN ===")
    
    # Danh sách các gói cần thiết:
    # - diffusers, transformers, accelerate: Lõi để chạy Hugging Face models
    # - torch, torchvision: Framework PyTorch
    # - bitsandbytes: Để load model ở định dạng 4-bit (tiết kiệm VRAM)
    # - huggingface_hub: Để tải model/LoRA từ Hugging Face
    # - sentencepiece, protobuf: Cần cho các tokenizer của một số model
    packages = [
        "diffusers==0.39.0",
        "transformers==5.14.1", 
        "accelerate>=0.26.0",
        "peft==0.19.1",
        "bitsandbytes==0.49.2",
        "huggingface-hub==1.24.0",
        "pillow==12.2.0",
        "tqdm==4.69.0",
        "torchvision",
        "wandb",
        "pandas",
        "pyarrow",
        "reportlab"
      
    ]
    
    for package in packages:
        print(f"Đang kiểm tra và cài đặt: {package}...")
        # Lệnh này sẽ cài đặt thư viện nếu chưa có, hoặc bỏ qua nếu đã có sẵn
        try:
             subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                   stdout=subprocess.DEVNULL, # Ẩn bớt log cài đặt để console đỡ rối
                                   stderr=subprocess.DEVNULL)
             print(f"  [+] {package} đã sẵn sàng.")
        except subprocess.CalledProcessError:
             print(f"  [-] LỖI: Không thể cài đặt {package}. Hãy kiểm tra kết nối mạng hoặc thử cài thủ công.")

def download_fonts():
    """
    Tạo thư mục 'fonts' và tải các font chữ phục vụ cho việc chèn chữ vào ảnh.
    """
    print("\n=== BƯỚC 2: TẢI FONT CHỮ ===")
    
    os.makedirs("fonts", exist_ok=True) 

    fonts = {
        "NotoSans-Regular.ttf": "https://raw.githubusercontent.com/notofonts/noto-fonts/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
        "NotoSans-Bold.ttf": "https://raw.githubusercontent.com/notofonts/noto-fonts/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf",
        "Anton-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf",
        "GreatVibes-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/greatvibes/GreatVibes-Regular.ttf",
        # --- CÁC FONT VINTAGE CÓ HỖ TRỢ TIẾNG VIỆT ---
        "Bevan-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/bevan/Bevan-Regular.ttf",
        "AlfaSlabOne-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/alfaslabone/AlfaSlabOne-Regular.ttf"
    }

    for filename, url in fonts.items():
        path = os.path.join("fonts", filename)

        if not os.path.exists(path):
            print(f"Đang tải font: {filename}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"  [-] Lỗi tải {filename}: {e}")
        else:
            print(f"Font {filename} đã tồn tại, bỏ qua.")

    print("\nDanh sách font hiện có trong thư mục:")
    print(os.listdir("fonts"))

def main():
    print("BẮT ĐẦU QUÁ TRÌNH SETUP MÔI TRƯỜNG...")
    install_libraries()
    download_fonts()
    print("\nHOÀN TẤT SETUP! BẠN CÓ THỂ CHẠY FILE CHÍNH BÂY GIỜ.")

if __name__ == "__main__":
    main()