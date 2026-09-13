# 🏖️ FLUX.1-dev QLoRA Fine-tuning & Poster Generator App

[![Hugging Face LoRA Model](https://img.shields.io/badge/🤗%20Hugging%20Face-LoRA%20Model-yellow.svg)](https://huggingface.co/luannguyen1345/quang-phu-lora-flux)
[![Framework: Marimo](https://img.shields.io/badge/UI_Framework-Marimo-blue.svg)](https://marimo.io)
[![Model: FLUX.1](https://img.shields.io/badge/Base_Model-FLUX.1--dev-orange.svg)](https://huggingface.co/black-forest-labs/FLUX.1-dev)

Dự án này là một quy trình MLOps End-to-End: từ việc fine-tune mô hình sinh ảnh FLUX.1-dev bằng kỹ thuật QLoRA để học đặc trưng địa danh du lịch Quảng Bình, Việt Nam, cho đến việc xây dựng web app tương tác bằng Marimo để tự động sinh ảnh AI và xuất poster PDF.

<p align="center">
  <img src="demo.png">
  <br>
  <i>(Ghi chú: bạn nên thay URL ảnh demo này bằng hình ảnh poster thực tế sau khi push project)</i>
</p>

## 🌟 Điểm nổi bật

- QLoRA Fine-Tuning: Huấn luyện thành công mô hình FLUX.1-dev trên GPU phổ thông bằng cách nén 4-bit (NF4) và Low-Rank Adaptation, tối ưu hóa VRAM.
- Pre-computed Embeddings: Tối ưu hóa quá trình train bằng cách trích xuất và cache Text Embeddings qua T5 Encoder trước khi chạy vòng lặp Diffusion, giảm tải bộ nhớ đáng kể.
- Reactive Web UI (Marimo): Xây dựng giao diện ứng dụng với Marimo – framework Python reactive hiện đại, thay thế cho Streamlit/Gradio.
- PDF Typography & Templating: Tự động ghép nối nền AI sinh ra với hệ thống typography (PIL + ReportLab) để xuất file PDF chất lượng cao.
- Secure API Management: Quản lý an toàn Hugging Face Token thông qua biến môi trường (.env) và UI State tích hợp.

## 📁 Cấu trúc repository

```text
.
├── README.md
├── requirements.txt

├── app-ui/
│   ├── app_ui.py                 # Giao diện web chính bằng Marimo
│   ├── core_model.py            # Logic nặng: load model + generate background
│   ├── setup.py                 # Download font chữ, cài đặt phụ trợ
│   ├── template_manager.py      # Quản lý template + typography + PDF
│   ├── templates/               # Thư mục chứa các file template poster
│   └── ...
├── finetune-flux/
│   ├── notebook-train.py        # Notebook / script train QLoRA
│   ├── dataset/
│   │   └── quang_phu/           # Dữ liệu ảnh + caption dùng để fine-tune
│   └── ...
├── assets/                      # Ảnh demo, tài nguyên tĩnh nếu có
└── .env                         # Local config (không push lên GitHub)
```

Lưu ý: Cấu trúc thực tế của dự án đang được tổ chức theo 2 phần chính:

- app-ui: chứa toàn bộ giao diện và logic sinh poster
- finetune-flux: chứa pipeline fine-tuning mô hình và dataset dùng để huấn luyện lên Hugging Face

## 🚀 Hướng dẫn sử dụng: Giao diện tạo Poster (App UI)

### 1. Chuẩn bị môi trường

Khởi tạo môi trường ảo và cài đặt thư viện:

```bash
python -m venv .venv
source .venv/bin/activate    # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Cấu hình Hugging Face Token

FLUX.1-dev yêu cầu cấp quyền từ Hugging Face.

- Tạo file `.env` ở thư mục gốc của dự án.
- Thêm token Hugging Face (quyền Read) của bạn:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxx
```

Nếu bỏ qua bước này, giao diện App sẽ tự động hiển thị ô nhập token cho bạn.

### 3. Khởi chạy ứng dụng

Khởi chạy giao diện bằng lệnh Marimo:

```bash
marimo run app_ui.py
```

Hoặc nếu bạn đang trong thư mục `app-ui`:

```bash
cd app-ui
marimo run app_ui.py
```

### 4. Quy trình sử dụng

1. Truy cập `http://localhost:2777` trên trình duyệt.
2. Nhập mô tả cảnh vật, ví dụ: `qp_dunes, quang phu sand dunes...`.
3. Chọn template văn bản mà bạn muốn dùng cho poster.
4. Bấm nút `🚀 TẠO ẢNH NỀN`.
5. Mô hình sẽ xử lý trong nền (~20–30 giây).
6. Khi hoàn tất, bấm vào nút `⬇️ TẢI POSTER PDF`.
7. Trình duyệt sẽ mở ra tab mới để hiển thị toàn bộ poster đã hoàn chỉnh, bạn có thể xem hoặc tải xuống máy.

## 🛠️ Hướng dẫn: Tự fine-tune mô hình (Notebook Training)

Dự án cung cấp sẵn một notebook chi tiết để bạn có thể tự huấn luyện LoRA của riêng mình.

Mở giao diện notebook:

```bash
marimo edit notebook_train.py
```

Nếu đang trong thư mục `finetune-flux`:

```bash
cd finetune-flux
marimo edit notebook-train.py
```

### Quy trình train (chi tiết có trong file)

1. Đọc dataset (ảnh + caption).
2. Mã hóa caption thành embeddings (T5 Encoder 8-bit) và lưu ra file `.parquet`.
3. Gắn LoRA adapter vào các Transformer blocks của FLUX.
4. Chạy vòng lặp train QLoRA với cấu hình 4-bit, gradient checkpointing.
5. Upload lên Hugging Face Hub.

> ⚠️ LƯU Ý QUAN TRỌNG KHI UPLOAD
>
> Phần notebook training không sử dụng file `.env` hay giao diện web. Ở cell cuối cùng (cell đẩy model lên Hugging Face), bạn bắt buộc phải tự điền Hugging Face Token có quyền Write trực tiếp vào biến `HF_TOKEN = "hf_..."` trong code.
>
> Tuyệt đối không lưu và đẩy `notebook-train.py` lên GitHub khi đã điền token thật của bạn vào đó để tránh bị lộ tài khoản.
>
> Tham khảo kết quả LoRA của dự án tại: [Hugging Face Repo](https://huggingface.co/luannguyen1345/quang-phu-lora-flux)

## 🧠 Kiến trúc và logic chính

### app-ui

Thư mục `app-ui` đóng vai trò là giao diện người dùng, bao gồm:

- `app_ui.py`: giao diện chính để nhập mô tả, chọn template và sinh poster
- `core_model.py`: đóng gói toàn bộ logic nặng thành các hàm sạch như:
  - `load_flux_pipeline()`
  - `generate_poster_bg()`
- `template_manager.py`: xử lý typography, layout và tạo file PDF
- `setup.py`: download font chữ và các dependency cần thiết
- `templates/`: chứa các mẫu poster / bố cục chữ và hình nền

### finetune-flux

Thư mục `finetune-flux` là nơi lưu trữ quy trình train LoRA:

- `notebook-train.py`: notebook hoặc script train mô hình với FLUX.1-dev
- `dataset/quang_phu/`: bộ dữ liệu ảnh và caption về địa danh Quảng Bình để fine-tune mô hình

## ✅ Mục tiêu dự án

- Tạo ra một model tùy chỉnh cho phong cách và cảnh quan đặc trưng của Quảng Bình
- Phát triển app sinh poster AI nhanh, dễ dùng và có thể mở rộng cho nhiều địa danh khác nhau
- Tích hợp đầy đủ quy trình từ training đến deployment theo mô hình MLOps cơ bản

## 📌 Ghi chú

- Dữ liệu ảnh mẫu không được đính kèm trong repository để tối ưu dung lượng
- Bạn nên lưu thông tin nhạy cảm như Hugging Face Token trong file `.env` và thêm nó vào `.gitignore`
- Tùy vào cấu hình máy, thời gian xử lý có thể thay đổi

## 🔗 Tài liệu tham khảo

- [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)
- [Marimo](https://marimo.io)
- [LoRA / QLoRA](https://huggingface.co/docs/peft/index)
- [Hugging Face Hub](https://huggingface.co)

---

Nếu bạn muốn, tôi có thể tiếp tục viết thêm phiên bản README ngắn gọn hơn cho GitHub, hoặc phiên bản chuyên nghiệp hơn theo chuẩn portfolio / AI project showcase.
