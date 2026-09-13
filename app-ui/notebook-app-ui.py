# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "diffusers==0.40.0",
#     "huggingface-hub==1.24.0",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", app_title="", auto_download=["html"])


@app.cell
def _():
    import os
    import subprocess
    import sys
    import io
    import marimo as mo

    return io, mo, os, subprocess, sys


@app.cell
def _(os, subprocess, sys):

    # Kiểm tra xem file setup có tồn tại trong cùng thư mục không
    setup_file = "setup.py"

    if os.path.exists(setup_file):
        print(f"Đang gọi chạy file {setup_file} để chuẩn bị môi trường...")
        # Gọi file 00_setup.py chạy thông qua Python
        result = subprocess.run([sys.executable, setup_file], capture_output=False)

        if result.returncode == 0:
            print("Môi trường đã sẵn sàng!")
        else:
            print("Lỗi trong quá trình chạy setup. Vui lòng kiểm tra lại.")
    else:
        print(f"Không tìm thấy file {setup_file}, bỏ qua bước setup.")
    return


@app.cell
def _():
    # #Đăng nhập vào Hugging face
    # from huggingface_hub import notebook_login

    # notebook_login()
    return


@app.cell
def _(mo, os):

    from huggingface_hub import login


    # Thử lấy token từ biến môi trường
    env_token = os.getenv("HF_TOKEN")

    # Sử dụng mo.state để lưu trữ token an toàn
    get_token, set_token = mo.state(env_token)

    if env_token:
        # Nếu có biến môi trường, tự động login
        login(token=env_token)
        login_ui = mo.md("✅ **Hệ thống:** Đã kết nối Hugging Face tự động (qua biến môi trường).")
    else:
        # Hàm này sẽ được gọi khi bấm nút
        def process_login(btn_click):
            if token_input.value:
                login(token=token_input.value)
                set_token(token_input.value) # Lưu token vào state

        # Tạo giao diện
        token_input = mo.ui.text(label="Hugging Face Token:", kind="password", full_width=True)
        login_btn = mo.ui.run_button(label="🔑 Đăng Nhập", on_change=process_login)
    
        # Kiểm tra trạng thái từ mo.state() thay vì đọc từ UI
        current_token = get_token()
    
        if current_token:
            login_ui = mo.md("✅ **Hệ thống:** Đăng nhập thành công!")
        else:
            login_ui = mo.vstack([
                mo.md("⚠️ **Hệ thống:** Vui lòng nhập token Hugging Face để tải Model:"),
                token_input,
                login_btn
            ])
    return get_token, login_ui


@app.cell
def _(get_token, mo):
    from core_model import load_flux_pipeline, generate_poster_bg
    from template_manager import apply_template 

    # 1. Khởi tạo State giữ ảnh
    get_bg, set_bg = mo.state(None)

    # 2. KHÓA CHẶN: Dùng get_token() thay vì biến thông thường
    if not get_token():
        pipeline = None
        mo.stop(True, mo.md("⏳ Đang chờ xác thực Hugging Face..."))
    else:
        lora_repo_id = "kTon/quangbinh-flux-lora" 
        pipeline = load_flux_pipeline(lora_repo_id)
    return apply_template, generate_poster_bg, get_bg, pipeline, set_bg


@app.cell
def _(generate_poster_bg, mo, pipeline, set_bg):
    prompt_input = mo.ui.text_area(
        label="Mô tả cảnh vật:", 
        value="" 
    )

    def handle_generate(btn_click):
        # Dùng pipeline đã tải từ cell trước đó
        if pipeline and prompt_input.value: 
            with mo.status.spinner("Đang chạy GPU sinh ảnh nền (20-30s)..."):
                raw_img = generate_poster_bg(
                    pipeline=pipeline, 
                    user_prompt=prompt_input.value, 
                    width=512, 
                    height=768, 
                    num_steps=28
                )
                # Cập nhật state NGAY TRONG HÀM NÀY
                set_bg(raw_img)
            
    gen_btn = mo.ui.run_button(
        label="🚀 TẠO ẢNH NỀN", 
        on_change=handle_generate
    )
    return gen_btn, prompt_input


@app.cell
def _(mo, prompt_input):
    prompt_text = prompt_input.value.lower()

    # 1. Logic tự nhận diện từ khóa
    if "pn_cave" in prompt_text:
        def_t, def_s, def_l = "PHONG NHA", "Kỳ quan đệ nhất động", "Quảng Bình"
    elif "qp_dunes" in prompt_text:
        def_t, def_s, def_l = "QUANG PHÚ", "Vẻ đẹp cát vàng", "Quảng Bình"
    else:
        def_t, def_s, def_l = "", "", ""

    # 2. Tạo các ô nhập liệu (cho full_width=True để kéo dài bằng nhau)
    title_input = mo.ui.text(value=def_t, full_width=True)
    subtitle_input = mo.ui.text(value=def_s, full_width=True)
    location_input = mo.ui.text(value=def_l, full_width=True)

    template_selector = mo.ui.dropdown(
        options={
            "Không dùng": "none",
            "Mẫu 1": "template_1",
            "Mẫu 2": "template_2",
            "Mẫu 3": "template_3",
            "Mẫu 4": "template_4"
        },
        value="Mẫu 1",
        full_width=True
    )

    # 3. Dùng Flexbox thuần: Triệt tiêu hoàn toàn màu sọc bảng và ép thẳng lề trái
    form_inputs = mo.md(f"""
    <div style="display: flex; flex-direction: column; gap: 6px; width: 100%;">
        <div style="display: flex; align-items: center; justify-content: flex-start; gap: 8px;">
            <span style="width: 75px; min-width: 75px; font-weight: 600; text-align: left; font-size: 14px;">Tiêu đề:</span>
            <div style="flex: 1;">{title_input}</div>
        </div>
        <div style="display: flex; align-items: center; justify-content: flex-start; gap: 8px;">
            <span style="width: 75px; min-width: 75px; font-weight: 600; text-align: left; font-size: 14px;">Phụ đề:</span>
            <div style="flex: 1;">{subtitle_input}</div>
        </div>
        <div style="display: flex; align-items: center; justify-content: flex-start; gap: 8px;">
            <span style="width: 75px; min-width: 75px; font-weight: 600; text-align: left; font-size: 14px;">Địa điểm:</span>
            <div style="flex: 1;">{location_input}</div>
        </div>
        <div style="display: flex; align-items: center; justify-content: flex-start; gap: 8px;">
            <span style="width: 75px; min-width: 75px; font-weight: 600; text-align: left; font-size: 14px;">Template:</span>
            <div style="flex: 1;">{template_selector}</div>
        </div>
    </div>
    """)
    return (
        form_inputs,
        location_input,
        subtitle_input,
        template_selector,
        title_input,
    )


@app.cell
def _(
    apply_template,
    get_bg,
    io,
    location_input,
    mo,
    subtitle_input,
    template_selector,
    title_input,
):


    current_bg = get_bg()

    if current_bg is None:
        preview_output = mo.md("") 
    else:
        t_choice = template_selector.value
        t_title = title_input.value.strip() or "TIEU DE"
        t_sub = subtitle_input.value.strip() or "PHU DE"
        t_loc = location_input.value.strip() or "DIA DIEM"

        if t_choice == "none":
            # ==========================================
            # KHÔNG DÙNG TEMPLATE (Chỉ hiện ảnh nền gốc)
            # ==========================================
            preview_img = current_bg 
            img_byte_arr = io.BytesIO()
            preview_img.save(img_byte_arr, format='PNG')
            png_bytes = img_byte_arr.getvalue()

            download_btn = mo.download(
                data=png_bytes,
                filename=f"Anh_Goc_{t_title}.png",
                label="⬇️ TẢI ẢNH GỐC (PNG)",
                mimetype="image/png"
            )
            download_buttons = mo.hstack([download_btn], justify="center")
            preview_output = mo.vstack([download_buttons, preview_img], align="center")

        else:
            # ==========================================
            # CÓ TEMPLATE: HIỂN THỊ TRỰC TIẾP PDF (DÙNG mo.pdf)
            # ==========================================
            pdf_path = apply_template(t_choice, current_bg, t_title, t_sub, t_loc)

            # 1. Đọc file PDF vừa tạo
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            # 2. Dùng mo.pdf() để preview file PDF (Hiển thị đầy đủ text, bố cục)
            pdf_preview = mo.pdf(
                src=io.BytesIO(pdf_bytes), # SỬA Ở ĐÂY
                width="100%", 
                height="800px" 
            )

            # 3. Nút tải nguyên bản file PDF
            download_pdf = mo.download(
                data=pdf_bytes,
                filename=f"Poster_{t_title}.pdf",
                label="⬇️ TẢI POSTER PDF",
                mimetype="application/pdf"
            )

            # 4. Gom nút bấm và bản preview
            download_buttons = mo.hstack([download_pdf], justify="center")
            preview_output = mo.vstack([download_buttons, pdf_preview], align="center", gap=2)
    return (preview_output,)


@app.cell
def _(form_inputs, gen_btn, login_ui, mo, preview_output, prompt_input):
    controls = mo.vstack([
        mo.md("### 🔑 0. Xác thực hệ thống"),
        login_ui,  # Form đăng nhập từ cell trên sẽ hiện ở đây
        mo.md("---"),
        mo.md("### ⚙️ 1. Sinh ảnh bằng AI"),
        prompt_input,
        gen_btn,
        mo.md("---"),
        mo.md("### ✍️ 2. Nhập thông tin & Template"),
        form_inputs 
    ], gap=1)

    app_layout = mo.hstack(
        [controls, preview_output], 
        widths=[1, 2], 
        gap=4
    )

    # Gọi tên biến ở dòng cuối cùng để Marimo in giao diện ra màn hình
    app_layout
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
