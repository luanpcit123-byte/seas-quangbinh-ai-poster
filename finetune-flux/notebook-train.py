# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "accelerate==1.14.0",
#     "bitsandbytes==0.49.2",
#     "diffusers==0.39.0",
#     "huggingface-hub==1.24.0",
#     "peft==0.19.1",
#     "pillow==12.2.0",
#     "tqdm==4.69.0",
#     "transformers==5.14.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo
    import subprocess

    return mo, subprocess


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🏖️ Đưa Quảng Bình Ra Thế Giới Qua Lăng Kính AI
    ### Dự án hè SEAS 2026 — Fine-tune FLUX.1-dev bằng QLoRA để tạo Poster du lịch Quảng Bình

    Chào các em! 👋

    Đây là notebook hướng dẫn **từng bước** để các em tự tay huấn luyện một mô hình AI "hiểu" được vẻ đẹp
    riêng của quê hương Quảng Bình (ví dụ: đồi cát Quang Phú, động Phong Nha, biển Nhật Lệ...), rồi dùng
    chính mô hình đó để tự động vẽ ra vô số poster du lịch.

    **Quy trình gồm 4 bước lớn** (đúng như trong slide giới thiệu dự án):

    | Bước | Tên | Việc cần làm |
    |---|---|---|
    | 0 | Chuẩn bị | Cài thư viện, chuẩn bị dữ liệu ảnh + caption, đăng nhập Hugging Face |
    | 1 | Nén kiến thức chữ (Text Embeddings) | Biến các câu mô tả (caption) thành các con số máy hiểu được |
    | 2 | Huấn luyện "Não bộ" (QLoRA Fine-tuning) | Dạy cho FLUX.1-dev ghi nhớ đặc trưng của địa danh |
    | 3 | Suy luận (Inference) | Dùng mô hình đã học để vẽ ảnh mới từ prompt |
    | 4 | Sáng tạo Poster (Typography) | Thêm chữ, tiêu đề nghệ thuật lên ảnh để ra Poster hoàn chỉnh |

    > ⚠️ **Lưu ý quan trọng trước khi bắt đầu:**
    > - Việc huấn luyện (Bước 2) có thể mất từ vài chục phút đến vài giờ tùy số bước train — đừng lo nếu nó chạy lâu, cứ để "chạy nền" và làm việc khác.
    > - Đọc kỹ từng ô 📌 **Giải thích** trước khi chạy code — hiểu "vì sao" quan trọng hơn "chạy được".

    ## ✏️ Cách notebook này được tổ chức

    Để các em thực sự **học được** thay vì chỉ bấm Run, notebook chia code thành 2 loại ô:

    - 🟩 **Ô code mẫu** — đã viết sẵn, hầu hết là phần hạ tầng phức tạp (load model lượng tử hoá, vòng lặp
      training chi tiết...). Các em nên **đọc kỹ comment** để hiểu logic, nhưng không cần sửa.
    - ✏️ **Ô BÀI TẬP** — chỉ có sườn (skeleton) + `# TODO` + gợi ý, phần thân quan trọng để **trống**, các em phải
      tự viết. Nếu chưa hoàn thành, cell phía dưới chạy sẽ báo lỗi — đó là dấu hiệu bình thường, không phải notebook bị hỏng!

    Hoàn thiện các bài tập và các phần TODO nhé các em.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧰 Bước 0.1: Cài đặt môi trường

    Chúng ta cần một vài thư viện chuyên dụng của Hugging Face để làm việc với mô hình sinh ảnh (diffusion model)
    và kỹ thuật fine-tuning tiết kiệm bộ nhớ (QLoRA).

    - `diffusers`: chứa kiến trúc & pipeline của FLUX.1-dev (mô hình sinh ảnh).
    - `transformers`: chứa các text encoder (bộ mã hoá văn bản) mà FLUX.1-dev dùng để "đọc hiểu" prompt.
    - `peft`: cài đặt LoRA/QLoRA — kỹ thuật tinh chỉnh mô hình mà không cần train lại toàn bộ.
    - `bitsandbytes`: cho phép nén mô hình về 4-bit/8-bit để tiết kiệm VRAM (bộ nhớ GPU).
    - `accelerate`: giúp code chạy tối ưu trên GPU (và nhiều GPU nếu có).
    - `wandb`: (tuỳ chọn) công cụ theo dõi quá trình train bằng biểu đồ trực quan trên web.

    Chạy ô bên dưới **một lần duy nhất** khi mới mở notebook (hoặc khi Colab bị reset môi trường).
    """)
    return


@app.cell
def _(subprocess):
    # Install required packages with specific versions
    import sys

    def install_packages():
        packages = [
            "diffusers==0.39.0",
            "transformers==5.14.1", 
            "accelerate==1.14.0",
            "peft==0.19.1",
            "bitsandbytes==0.49.2",
            "huggingface-hub==1.24.0",
            "pillow==12.2.0",
            "tqdm==4.69.0",
            "torchvision",
            "wandb",
            "pandas",
            "pyarrow"
        ]

        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Run installation
    install_packages()
    return


@app.cell
def _():
    import torch

    # Kiểm tra xem máy có GPU không — nếu in ra "Không tìm thấy GPU", hãy vào
    # Runtime > Change runtime type > Chọn GPU (trên Google Colab) rồi chạy lại notebook.
    if torch.cuda.is_available():
        print(f"✅ Đã tìm thấy GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Bộ nhớ GPU (VRAM): {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("❌ Không tìm thấy GPU! Notebook này bắt buộc phải chạy trên GPU.")
    return (torch,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📂 Bước 0.2: TODO: Chuẩn bị bộ dữ liệu (Dataset)

    Đây chính là bước **"Gom nhặt Nguyên liệu"** trong slide. AI chỉ giỏi những gì nó được "dạy", vì vậy
    chất lượng dữ liệu ảnh + caption quyết định phần lớn chất lượng kết quả cuối cùng.

    **Cấu trúc thư mục dataset cần chuẩn bị:**

    ```
    quang_phu/                     <- tên thư mục = tên địa danh các em chọn
    ├── 001.jpg                    <- ảnh chất lượng cao (nên >= 10-20 ảnh)
    ├── 001.txt                    <- caption mô tả CHÍNH XÁC nội dung ảnh 001.jpg
    ├── 002.jpg
    ├── 002.txt
    └── ...
    ```

    **Mẹo viết caption tốt (rất quan trọng!):**
    1. Luôn bắt đầu caption bằng một **"trigger word"** — một cụm từ độc nhất, chưa từng tồn tại
       (ví dụ: `qp_dunes`) để AI học cách gắn riêng cụm từ này với đặc trưng của địa danh, không bị nhầm
       với các đồi cát khác nó đã biết trên internet.
       - Ví dụ: `"qp_dunes, quang phu sand dunes, a wide golden sand dune under blue sky, vietnam"`
    2. Mô tả đúng những gì nhìn thấy trong ảnh: góc chụp, ánh sáng, thời tiết, các vật thể xuất hiện...
    3. Đa dạng hoá góc chụp/thời điểm trong ảnh để mô hình học được nhiều biến thể, tránh học "vẹt" một góc duy nhất.

    Sau khi chuẩn bị xong, các em nén thư mục này thành file `.zip` (ví dụ `preprocessed_seas_poster_gen.zip`),
    upload lên môi trường chạy notebook (Colab: kéo thả vào tab Files), rồi chạy ô dưới để giải nén.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🔑 Bước 0.3: Đăng nhập Hugging Face Hub

    `FLUX.1-dev` là một mô hình **"gated"** (giới hạn quyền truy cập) — các em cần:
    1. Có tài khoản tại [huggingface.co](https://huggingface.co).
    2. Vào trang [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) và bấm **"Agree and access repository"**.
    3. Chạy cell login phía dưới

    Việc đăng nhập cũng cần thiết nếu sau này nhóm muốn đẩy (push) LoRA adapter đã train lên Hub để lưu trữ/chia sẻ.
    """)
    return


@app.cell
def _():
    from huggingface_hub import notebook_login

    notebook_login()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🧩 BƯỚC 1: Tính toán trước Text Embeddings

    ### 📌 Giải thích
    FLUX.1-dev không đọc trực tiếp câu chữ (caption) — nó cần một bước "dịch" caption thành các **vector số**
    (text embeddings) thông qua một text encoder tên là **T5**. Vì text encoder T5 khá nặng, nếu vừa phải chạy
    T5 vừa phải chạy mô hình sinh ảnh cùng lúc trong lúc training sẽ rất tốn VRAM.

    **Giải pháp:** tính (encode) tất cả các embeddings của caption **một lần duy nhất trước khi train**, lưu chúng
    vào một file `.parquet`. Trong lúc training, ta chỉ cần đọc lại file này thay vì chạy lại T5 nhiều lần
    → vừa nhanh hơn, vừa tiết kiệm bộ nhớ GPU hơn rất nhiều.

    Quy trình bước này:
    1. Đọc từng cặp (ảnh, caption) trong dataset.
    2. Đưa caption qua text encoder T5 (được nén 8-bit để tiết kiệm VRAM) → ra `prompt_embeds`.
    3. Lưu toàn bộ embeddings ra file `embeddings_<ten_dia_danh>.parquet`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✏️ BÀI TẬP 1: Viết hàm đọc dataset — `load_dataset`

    **Mục tiêu học được:** thao tác với `pathlib`, đọc/ghi file, xử lý dữ liệu bị thiếu/lỗi — kỹ năng nền tảng
    của mọi pipeline Machine Learning.

    **Đề bài:** hoàn thành hàm `load_dataset(dataset_path, split="train")`, làm các việc sau:
    1. Quét thư mục `dataset_path`, tìm tất cả các file ảnh có phần mở rộng nằm trong `image_extensions`
       (gợi ý: dùng `dataset_dir.iterdir()`, lọc bằng `f.is_file()` và `f.suffix.lower() in image_extensions`,
       nhớ `sorted(...)` để thứ tự luôn cố định).
    2. Với **mỗi ảnh**, tìm file `.txt` cùng tên (gợi ý: `img_path.with_suffix(".txt")`):
       - Nếu file `.txt` **không tồn tại** → in cảnh báo rồi bỏ qua ảnh này (`continue`).
       - Nếu file `.txt` tồn tại nhưng **nội dung rỗng** (sau khi `.strip()`) → in cảnh báo rồi bỏ qua.
       - Nếu hợp lệ → đọc nội dung caption, thêm vào danh sách `samples` dưới dạng
         `{"image": <PIL.Image đã convert("RGB")>, "text": <caption>}`.
    3. Nếu không tìm thấy ảnh nào → `raise FileNotFoundError(...)`.
    4. Nếu không có cặp ảnh-caption hợp lệ nào → `raise ValueError(...)`.
    5. In ra số lượng mẫu đã đọc thành công, rồi trả về `PosterDataset(samples)`.

    > 💡 Gợi ý: `Image.open(img_path).convert("RGB")` để mở và chuẩn hoá ảnh về hệ màu RGB.
    """)
    return


@app.cell
def _():
    import json
    import os
    from pathlib import Path
    from PIL import Image

    def load_dataset(dataset_path, split="train"):
        """Đọc dataset dạng thư mục ảnh + caption (mỗi ảnh 1 file .txt cùng tên)."""
        dataset_dir = Path(dataset_path)
        image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}

        # ----- TODO 1: Quét và sắp xếp tất cả các file ảnh hợp lệ -----
        image_files = sorted(
            [f for f in dataset_dir.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
        ) if dataset_dir.exists() else []

        if not image_files:
            raise FileNotFoundError(f"Không tìm thấy ảnh nào trong '{dataset_dir.resolve()}'. "
                                    f"Kiểm tra lại đường dẫn thư mục hoặc bước giải nén.")

        samples = []
        for img_path in image_files:
            # ----- TODO 2: Tìm file .txt cùng tên & xử lý các trường hợp -----
            txt_path = img_path.with_suffix(".txt")

            # Trường hợp 1: Thiếu file .txt
            if not txt_path.exists():
                print(f"⚠️ Bỏ qua '{img_path.name}': Thiếu file caption .txt tương ứng.")
                continue

            # Đọc nội dung file text
            with open(txt_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()

            # Trường hợp 2: File .txt rỗng
            if not caption:
                print(f"⚠️ Bỏ qua '{img_path.name}': File caption bị rỗng.")
                continue

            # Trường hợp 3: Hợp lệ -> Thêm vào danh sách samples
            try:
                img = Image.open(img_path).convert("RGB")
                samples.append({"image": img, "text": caption})
            except Exception as e:
                print(f"⚠️ Không thể mở ảnh '{img_path.name}': {e}")

        if not samples:
            raise ValueError(
                f"Không có cặp ảnh-caption nào hợp lệ trong {dataset_dir}. "
                f"Các ảnh tìm thấy: {[f.name for f in image_files]}."
            )

        # ----- TODO 3: In ra số lượng mẫu đã đọc thành công -----
        print(f"✅ Đã tải thành công {len(samples)}/{len(image_files)} mẫu dữ liệu từ '{dataset_path}'.")

        return PosterDataset(samples)

    class PosterDataset:
        """Wrapper nhẹ, bắt chước cách dùng của HuggingFace `Dataset` (hỗ trợ len(), for, [idx])."""

        def __init__(self, samples):
            self._samples = samples

        def __len__(self):
            return len(self._samples)

        def __iter__(self):
            return iter(self._samples)

        def __getitem__(self, idx):
            return self._samples[idx]

    return Image, Path, load_dataset, os


@app.cell
def _(load_dataset):
    # ✅ VIỆC CẦN LÀM: đổi đường dẫn cho đúng tên thư mục dữ liệu của nhóm em
    DATASET_PATH = "quang_phu"

    dune = load_dataset(dataset_path=DATASET_PATH)

    # In thử mẫu đầu tiên để kiểm tra: ảnh có hiển thị đúng không, caption có hợp lý không
    print("Caption mẫu đầu tiên:", dune[0]["text"])
    dune[0]["image"]
    return (DATASET_PATH,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1.2. Tính embeddings và lưu ra file `.parquet`

    📌 **Đọc kỹ trước khi chạy:**
    - `load_flux_dev_pipeline()`: chỉ tải phần **text encoder T5** của FLUX.1-dev (không tải phần vẽ ảnh — `transformer=None, vae=None`)
      để tiết kiệm VRAM, vì ở bước này ta chỉ cần "hiểu chữ", chưa cần "vẽ".
    - `quantization_config = BitsAndBytesConfig(load_in_8bit=True)`: nén T5 xuống 8-bit — giảm ~50% VRAM mà chất lượng gần như không đổi.
    - `compute_embeddings()`: chạy từng caption qua T5, thu về 3 thành phần mà FLUX.1-dev cần: `prompt_embeds`, `pooled_prompt_embeds`, `text_ids`.
    - `generate_image_hash()`: tạo một "mã định danh" duy nhất cho mỗi ảnh (dựa trên nội dung ảnh) để sau này
      bước training có thể tra cứu đúng embedding ứng với đúng ảnh.

    ### ✏️ BÀI TẬP 2 : Viết hàm `generate_image_hash`

    **Mục tiêu học được:** khái niệm hashing — biến dữ liệu bất kỳ (ở đây là pixel của ảnh) thành một chuỗi ký
    tự ngắn, duy nhất, dùng làm "khoá tra cứu" (giống như CMND của mỗi ảnh).

    **Đề bài:** hoàn thành hàm `generate_image_hash(image)`, trả về mã băm SHA-256 (dạng hex string) của dữ liệu
    pixel trong `image` (một đối tượng `PIL.Image`).

    > 💡 Gợi ý: `image.tobytes()` trả về dữ liệu pixel thô dạng bytes. Dùng
    > `insecure_hashlib.sha256(...).hexdigest()` để băm.

    ### ✏️ BÀI TẬP 3 : Hoàn thành vòng lặp trong `compute_embeddings`

    **Mục tiêu học được:** cách gọi API của một pipeline sinh ảnh (`encode_prompt`) để lấy embeddings — đây là
    bước cầu nối quan trọng giữa "văn bản" và "mô hình AI".

    **Đề bài:** trong hàm `compute_embeddings`, với mỗi `prompt` trong vòng lặp `for`, hãy gọi
    `pipeline.encode_prompt(...)` để lấy về 3 giá trị `prompt_embeds`, `pooled_prompt_embeds`, `text_ids`, rồi
    append từng giá trị vào đúng danh sách tương ứng (`all_prompt_embeds`, `all_pooled_prompt_embeds`, `all_text_ids`).

    > 💡 Gợi ý: chữ ký hàm cần gọi là
    > `pipeline.encode_prompt(prompt=prompt, prompt_2=None, max_sequence_length=max_sequence_length)`
    > và nó trả về đúng theo thứ tự `(prompt_embeds, pooled_prompt_embeds, text_ids)`.
    """)
    return


@app.cell
def _(DATASET_PATH, load_dataset, torch):
    import pandas as pd
    from huggingface_hub.utils import insecure_hashlib
    from tqdm.auto import tqdm
    from transformers import T5EncoderModel, BitsAndBytesConfig

    from diffusers import FluxPipeline


    MAX_SEQ_LENGTH = 77
    OUTPUT_PATH = f"embeddings_{DATASET_PATH.strip('/').split('/')[-1]}.parquet"
    MODEL_ID = "black-forest-labs/FLUX.1-dev"


    def generate_image_hash(image):
        """Tạo mã hash duy nhất cho một ảnh dựa trên dữ liệu pixel của nó.

        TODO (Bài tập 2): trả về mã băm SHA-256 (hex string) của image.tobytes().
        """
        return insecure_hashlib.sha256(image.tobytes()).hexdigest()


    def load_flux_dev_pipeline():
        """Chỉ tải text encoder (T5) của FLUX.1-dev, nén 8-bit để tiết kiệm VRAM."""
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        text_encoder = T5EncoderModel.from_pretrained(
            MODEL_ID,
            subfolder="text_encoder_2",
            quantization_config=quantization_config,
            device_map="auto",
        )
        # transformer=None, vae=None -> KHÔNG tải phần vẽ ảnh, chỉ cần phần đọc hiểu văn bản
        pipeline = FluxPipeline.from_pretrained(
            MODEL_ID, text_encoder_2=text_encoder, transformer=None, vae=None, device_map="balanced"
        )
        return pipeline


    @torch.no_grad()
    def compute_embeddings(pipeline, prompts, max_sequence_length):
        """Chạy từng caption qua text encoder để lấy embeddings tương ứng."""
        all_prompt_embeds = []
        all_pooled_prompt_embeds = []
        all_text_ids = []
        for prompt in tqdm(prompts, desc="Đang mã hoá caption thành embeddings"):
            # ----- TODO (Bài tập 3): gọi pipeline.encode_prompt(...) và append kết quả vào 3 list ở trên -----
            prompt_embeds, pooled_prompt_embeds, text_ids = pipeline.encode_prompt(
        prompt=prompt,
        prompt_2=None,
        max_sequence_length=max_sequence_length,
    )
            all_prompt_embeds.append(prompt_embeds)
            all_pooled_prompt_embeds.append(pooled_prompt_embeds)
            all_text_ids.append(text_ids)

        max_memory = torch.cuda.max_memory_allocated() / 1024 / 1024 / 1024
        print(f"Bộ nhớ GPU tối đa đã dùng ở bước này: {max_memory:.3f} GB")
        return all_prompt_embeds, all_pooled_prompt_embeds, all_text_ids


    def run():
        dataset = load_dataset(DATASET_PATH)
        # Dùng dict để map: mã hash của ảnh -> caption (giúp tránh trùng lặp và dễ tra cứu sau này)
        image_prompts = {generate_image_hash(sample["image"]): sample["text"] for sample in dataset}
        all_prompts = list(image_prompts.values())
        print(f"Số lượng caption sẽ mã hoá: {len(all_prompts)}")

        pipeline = load_flux_dev_pipeline()
        all_prompt_embeds, all_pooled_prompt_embeds, all_text_ids = compute_embeddings(
            pipeline, all_prompts, MAX_SEQ_LENGTH
        )

        # Gom kết quả thành bảng dữ liệu (DataFrame)
        data = []
        for i, (image_hash, _) in enumerate(image_prompts.items()):
            data.append((image_hash, all_prompt_embeds[i], all_pooled_prompt_embeds[i], all_text_ids[i]))

        embedding_cols = ["prompt_embeds", "pooled_prompt_embeds", "text_ids"]
        df = pd.DataFrame(data, columns=["image_hash"] + embedding_cols)

        # Chuyển tensor -> list số thực để lưu được vào file parquet
        for col in embedding_cols:
            df[col] = df[col].apply(lambda x: x.cpu().float().numpy().flatten().tolist())

        df.to_parquet(OUTPUT_PATH)
        print(f"✅ Đã lưu {len(df)} embeddings vào file '{OUTPUT_PATH}'")

        # Dọn bộ nhớ GPU sau khi dùng xong text encoder, chuẩn bị chỗ trống cho bước training
        del pipeline, dataset, image_prompts, all_prompts
        del all_prompt_embeds, all_pooled_prompt_embeds, all_text_ids, df
        torch.cuda.empty_cache()

    return BitsAndBytesConfig, FluxPipeline, T5EncoderModel, pd, tqdm


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ### 📚 Kiến thức nền: LoRA & QLoRA là gì?

    **LoRA (Low-Rank Adaptation):** thay vì cập nhật toàn bộ ma trận trọng số $W$ khổng lồ của mô hình gốc
    (hàng tỷ tham số), LoRA chỉ học hai ma trận nhỏ hơn nhiều là $A$ và $B$, sao cho phần cập nhật
    $\Delta W = B A$. Ở đây $r$ (gọi là *rank*) nhỏ hơn rất nhiều so với kích thước gốc, nghĩa là số tham số
    cần huấn luyện giảm đi rất nhiều lần → train nhanh hơn, tốn ít bộ nhớ hơn. $\alpha$ là hệ số co giãn, quyết
    định mức ảnh hưởng của phần học thêm (LoRA) so với mô hình gốc.

    <p align="center">
      <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/peft/lora_diagram.png"
           alt="Minh hoạ LoRA chèn 2 ma trận rank thấp quanh 1 ma trận trọng số đã đóng băng"
           width="550"/>
    </p>

    **QLoRA:** kết hợp LoRA với **lượng tử hoá (quantization)** — tải mô hình gốc ở định dạng nén 4-bit
    (thường dùng `bitsandbytes`) để giảm mạnh dung lượng bộ nhớ cần thiết, sau đó chỉ train các adapter LoRA
    (ở FP16/BF16) trên nền mô hình đã nén đó. Nhờ vậy, ta có thể fine-tune một mô hình khổng lồ như FLUX.1
    ngay trên GPU phổ thông (như GPU miễn phí của Colab) thay vì cần GPU máy chủ đắt tiền.

    Một vài kỹ thuật tối ưu bộ nhớ khác mà notebook này áp dụng:

    | Kỹ thuật | Tác dụng |
    |---|---|
    | **8-bit Optimizer (AdamW8bit)** | Optimizer thường lưu trạng thái ở FP32 rất tốn bộ nhớ; bản 8-bit giảm ~75% bộ nhớ optimizer mà vẫn ổn định. |
    | **Gradient Checkpointing** | Không lưu toàn bộ activation trong forward pass, mà tính lại một phần khi cần ở backward pass — đổi thời gian tính toán lấy bộ nhớ. |
    | **Cache Latents** | Mã hoá trước tất cả ảnh qua VAE thành *latent* rồi lưu lại, để trong lúc train không phải chạy VAE lặp lại nhiều lần, đồng thời có thể "giải phóng" VAE khỏi GPU sau khi cache xong. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 📚 Kiến thức nền: LoRA & QLoRA là gì?

    **LoRA (Low-Rank Adaptation):** thay vì cập nhật toàn bộ ma trận trọng số $W$ khổng lồ của mô hình gốc
    (hàng tỷ tham số), LoRA chỉ học hai ma trận nhỏ hơn nhiều là $A$ và $B$, sao cho phần cập nhật
    $\Delta W = B A$. Ở đây $r$ (gọi là *rank*) nhỏ hơn rất nhiều so với kích thước gốc, nghĩa là số tham số
    cần huấn luyện giảm đi rất nhiều lần → train nhanh hơn, tốn ít bộ nhớ hơn. $\alpha$ là hệ số co giãn, quyết
    định mức ảnh hưởng của phần học thêm (LoRA) so với mô hình gốc.

    <p align="center">
      <img src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/peft/lora_diagram.png"
           alt="Minh hoạ LoRA chèn 2 ma trận rank thấp quanh 1 ma trận trọng số đã đóng băng"
           width="550"/>
    </p>

    **QLoRA:** kết hợp LoRA với **lượng tử hoá (quantization)** — tải mô hình gốc ở định dạng nén 4-bit
    (thường dùng `bitsandbytes`) để giảm mạnh dung lượng bộ nhớ cần thiết, sau đó chỉ train các adapter LoRA
    (ở FP16/BF16) trên nền mô hình đã nén đó. Nhờ vậy, ta có thể fine-tune một mô hình khổng lồ như FLUX.1
    ngay trên GPU phổ thông (như GPU miễn phí của Colab) thay vì cần GPU máy chủ đắt tiền.

    Một vài kỹ thuật tối ưu bộ nhớ khác mà notebook này áp dụng:

    | Kỹ thuật | Tác dụng |
    |---|---|
    | **8-bit Optimizer (AdamW8bit)** | Optimizer thường lưu trạng thái ở FP32 rất tốn bộ nhớ; bản 8-bit giảm ~75% bộ nhớ optimizer mà vẫn ổn định. |
    | **Gradient Checkpointing** | Không lưu toàn bộ activation trong forward pass, mà tính lại một phần khi cần ở backward pass — đổi thời gian tính toán lấy bộ nhớ. |
    | **Cache Latents** | Mã hoá trước tất cả ảnh qua VAE thành *latent* rồi lưu lại, để trong lúc train không phải chạy VAE lặp lại nhiều lần, đồng thời có thể "giải phóng" VAE khỏi GPU sau khi cache xong. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🏋️ BƯỚC 2: Huấn luyện QLoRA Adapter

    ### 📌 Giải thích tổng quan
    Đây là "trái tim" của dự án — nơi mô hình thực sự **học** đặc trưng của địa danh Quảng Bình.

    Quy trình training (đã được viết sẵn để chạy trực tiếp trong notebook, không cần chạy script ngoài) gồm các bước:
    1. Tải `FLUX.1-dev` ở dạng **nén 4-bit (NF4)**.
    2. Gắn (attach) các **lớp LoRA** vào các khối attention của transformer (`to_k, to_q, to_v, to_out.0`) — đây
       là những phần duy nhất sẽ được cập nhật trong lúc train, phần còn lại của mô hình được "đóng băng" (freeze).
    3. Cache toàn bộ latent ảnh qua VAE trước khi train.
    4. Vòng lặp training: mỗi bước sẽ (a) thêm nhiễu vào ảnh, (b) yêu cầu mô hình dự đoán lại phần nhiễu đó dựa
       trên caption, (c) so sánh dự đoán với nhiễu thật để tính loss, rồi cập nhật các trọng số LoRA.
    5. Lưu checkpoint định kỳ và lưu trọng số LoRA cuối cùng vào thư mục `output_dir`.

    > ⏱️ **Về thời gian & số bước train (`max_train_steps`):** Trong notebook demo này ta để
    > mặc định thấp hơn để các em thấy kết quả nhanh. Có thể tăng dần: train 100-150 bước trước để kiểm tra mọi
    > thứ chạy ổn, sau đó tăng lên 300-700 bước để có kết quả đẹp hơn.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.1. (Tuỳ chọn) Theo dõi quá trình train bằng Weights & Biases

    `wandb` giúp vẽ biểu đồ loss theo thời gian thực trên web, rất hữu ích để biết mô hình có đang học tốt không.

    > 🔒 **Lưu ý bảo mật:** Khi chia sẻ notebook thì cần xóa API key — vì bất kỳ ai đọc được key đó cũng có thể đăng nhập vào tài khoản wandb của em!

    Nếu nhóm không muốn dùng wandb, có thể bỏ qua ô này và đổi `report_to = "wandb"` thành `report_to = "none"`
    trong cấu hình training ở phần dưới.
    """)
    return


@app.cell
def _():
    import wandb

    # Lấy API key miễn phí tại: https://wandb.ai/authorize
    wandb.login(key="")

    # Nếu không muốn dùng wandb, comment dòng trên lại và đặt report_to="none" ở TrainingConfig bên dưới.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ✏️ BÀI TẬP 4: Hoàn thành `collate_fn`

    **Mục tiêu học được:** khái niệm **batch** trong deep learning — vì sao ta phải "gộp" nhiều mẫu dữ liệu lẻ
    thành một khối tensor duy nhất trước khi đưa vào mô hình, và cách dùng `torch.stack`.

    **Đề bài:** `DataLoader` sẽ gọi hàm `collate_fn(examples)` với `examples` là một **list các dict** (mỗi dict
    là kết quả của `dataset[i]`, xem lớp `DreamBoothDataset` phía dưới). Hãy hoàn thành hàm để:
    1. Gộp toàn bộ `ex["instance_images"]` của các phần tử trong `examples` thành 1 tensor duy nhất bằng
       `torch.stack(...)`, sau đó ép kiểu `.float()` và `.to(memory_format=torch.contiguous_format)`.
    2. Gộp tương tự cho `ex["prompt_embeds"]` và `ex["pooled_prompt_embeds"]`.
    3. Với `text_ids`: gộp bằng `torch.stack(...)` rồi **chỉ lấy phần tử đầu tiên `[0]`** — vì trong dataset này,
       `text_ids` giống hệt nhau cho mọi mẫu (không phụ thuộc vào ảnh/caption cụ thể), nên không cần giữ cả batch.
    4. Trả về đúng 1 dict với 4 khoá: `"pixel_values"`, `"prompt_embeds"`, `"pooled_prompt_embeds"`, `"text_ids"`.

    > 💡 Gợi ý: `torch.stack([x1, x2, x3])` biến 1 list gồm N tensor cùng shape thành 1 tensor có thêm chiều batch
    > ở đầu (shape `(N, ...)`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2. Script training đầy đủ

    Đọc các chú thích (comment) tiếng Việt trong từng phần để hiểu code đang làm gì. Ô này đã viết sẵn gần như
    toàn bộ (xem lý do ở trên) — **trừ hàm `collate_fn` ở Bài tập 4**, các em cần hoàn thành phần đó trước khi
    chạy được training. Các tham số cấu hình (số bước train, learning rate, kích thước ảnh...) nằm ở
    `TrainingConfig` cuối ô, ngay phía dưới ô này.
    """)
    return


@app.cell
def _(
    BitsAndBytesConfig,
    FluxPipeline,
    Path,
    load_dataset,
    os,
    pd,
    torch,
    tqdm,
):
    import copy
    import math
    import logging
    import hashlib
    import numpy as np
    from PIL.ImageOps import exif_transpose
    from torchvision import transforms
    from torch.utils.data import Dataset, DataLoader

    import transformers
    import diffusers
    from diffusers import (
        AutoencoderKL,
        FlowMatchEulerDiscreteScheduler,
        FluxTransformer2DModel
    )
    from diffusers.optimization import get_scheduler
    from diffusers.training_utils import (
        cast_training_params,
        compute_density_for_timestep_sampling,
        compute_loss_weighting_for_sd3,
        free_memory,
    )
    from diffusers.utils import convert_unet_state_dict_to_peft
    from diffusers.utils.torch_utils import is_compiled_module

    from accelerate import Accelerator, DistributedType
    from accelerate.logging import get_logger
    from accelerate.utils import DistributedDataParallelKwargs, ProjectConfiguration, set_seed

    from peft import LoraConfig, prepare_model_for_kbit_training
    from peft.utils import get_peft_model_state_dict
    import bitsandbytes as bnb

    logger = get_logger(__name__)

    # ==========================================
    # 0. DỌN BỘ NHỚ TRƯỚC KHI TRAIN
    # ==========================================
    import gc

    gc.collect()                          # Dọn rác Python
    if torch.cuda.is_available():
        torch.cuda.empty_cache()          # Dọn cache CUDA, giải phóng VRAM còn sót từ bước trước


    # ==========================================
    # 1. DATASET & DATALOADER
    # ==========================================
    class DreamBoothDataset(Dataset):
        """Dataset dùng cho training: đọc ảnh + tra cứu embedding đã tính sẵn ở Bước 1 (theo hash ảnh)."""

        def __init__(self, dataset_path, embeddings_path, width, height, max_sequence_length=77):
            self.width = width
            self.height = height
            self.max_sequence_length = max_sequence_length
            self.embeddings_path = Path(embeddings_path)

            if not self.embeddings_path.exists():
                raise ValueError(
                    "Không tìm thấy file `embeddings_path`. Hãy đảm bảo đã chạy xong Bước 1 (run()) trước khi train."
                )

            # Tải dataset và tính hash của từng ảnh để map đúng với embedding tương ứng
            dataset = load_dataset(dataset_path, split="train")
            self.instance_images = [sample["image"] for sample in dataset]
            self.image_hashes = [hashlib.sha256(img.tobytes()).hexdigest() for img in self.instance_images]

            self.pixel_values = self._apply_transforms()
            self.data_dict = self._map_embeddings()
            self._length = len(self.instance_images)

        def __len__(self):
            return self._length

        def __getitem__(self, index):
            idx = index % len(self.instance_images)
            hash_key = self.image_hashes[idx]
            prompt_embeds, pooled_prompt_embeds, text_ids = self.data_dict[hash_key]

            return {
                "instance_images": self.pixel_values[idx],
                "prompt_embeds": prompt_embeds,
                "pooled_prompt_embeds": pooled_prompt_embeds,
                "text_ids": text_ids,
            }

        def _apply_transforms(self):
            # Resize + crop ảnh về đúng kích thước train, chuẩn hoá giá trị pixel về [-1, 1]
            transform = transforms.Compose([
                transforms.Resize((self.height, self.width), interpolation=transforms.InterpolationMode.BILINEAR),
                transforms.RandomCrop((self.height, self.width)),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5]),
            ])

            pixel_values = []
            for image in self.instance_images:
                image = exif_transpose(image)  # sửa ảnh bị xoay sai hướng do metadata EXIF của điện thoại
                if image.mode != "RGB":
                    image = image.convert("RGB")
                pixel_values.append(transform(image))
            return pixel_values

        def _map_embeddings(self):
            # Đọc lại file .parquet đã tạo ở Bước 1, dựng dict tra cứu: hash ảnh -> (embeddings)
            df = pd.read_parquet(self.embeddings_path)
            data_dict = {}
            for _, row in df.iterrows():
                prompt_embeds = torch.from_numpy(np.array(row["prompt_embeds"]).reshape(self.max_sequence_length, 4096))
                pooled_prompt_embeds = torch.from_numpy(np.array(row["pooled_prompt_embeds"]).reshape(768))
                text_ids = torch.from_numpy(np.array(row["text_ids"]).reshape(77, 3))

                data_dict[row["image_hash"]] = (prompt_embeds, pooled_prompt_embeds, text_ids)
            return data_dict


    def collate_fn(examples):
        """Gộp nhiều sample lẻ thành 1 batch để đưa vào mô hình cùng lúc."""
        # 1. Gộp ảnh pixel_values, ép kiểu float và tối ưu bộ nhớ contiguous
        pixel_values = torch.stack([ex["instance_images"] for ex in examples])
        pixel_values = pixel_values.to(
            memory_format=torch.contiguous_format
        ).float()

        # 2. Gộp các vector embeddings văn bản
        prompt_embeds = torch.stack([ex["prompt_embeds"] for ex in examples])
        pooled_prompt_embeds = torch.stack(
            [ex["pooled_prompt_embeds"] for ex in examples]
        )

        # 3. Gộp text_ids và chỉ lấy phần tử đầu tiên [0] vì chúng giống hệt nhau
        text_ids = torch.stack([ex["text_ids"] for ex in examples])[0]

        # 4. Trả về dictionary chứa đủ 4 khóa
        return {
            "pixel_values": pixel_values,
            "prompt_embeds": prompt_embeds,
            "pooled_prompt_embeds": pooled_prompt_embeds,
            "text_ids": text_ids,
        }


    # ==========================================
    # 2. CÁC HÀM HỖ TRỢ
    # ==========================================
    def setup_models(args):
        """Khởi tạo Scheduler, VAE và Transformer (nén 4-bit NF4 để tiết kiệm VRAM)."""
        noise_scheduler = FlowMatchEulerDiscreteScheduler.from_pretrained(args.pretrained_model_name, subfolder="scheduler")
        vae = AutoencoderKL.from_pretrained(args.pretrained_model_name, subfolder="vae")

        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )
        transformer = FluxTransformer2DModel.from_pretrained(
            args.pretrained_model_name,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.float16,
        )
        return noise_scheduler, vae, transformer


    def apply_lora_to_transformer(transformer, args):
        """Đóng băng toàn bộ transformer gốc, chỉ gắn thêm các lớp LoRA có thể học được."""
        transformer = prepare_model_for_kbit_training(transformer, use_gradient_checkpointing=False)
        transformer.requires_grad_(False)  # đóng băng 100% trọng số gốc

        if args.gradient_checkpointing:
            transformer.enable_gradient_checkpointing()

        lora_config = LoraConfig(
            r=args.rank,                                  # rank càng cao -> học được nhiều chi tiết hơn, nhưng tốn tài nguyên hơn
            lora_alpha=args.rank,
            init_lora_weights="gaussian",
            target_modules=["to_k", "to_q", "to_v", "to_out.0"],  # chỉ gắn LoRA vào các lớp attention
        )
        transformer.add_adapter(lora_config)
        print(f"Tham số có thể train: {transformer.num_parameters(only_trainable=True):,} "
              f"/ Tổng tham số mô hình: {transformer.num_parameters():,}")
        return transformer


    def cache_latents(vae, dataloader, accelerator):
        """Chạy VAE 1 lần để mã hoá tất cả ảnh training thành latent, rồi giải phóng VAE khỏi VRAM."""
        vae.requires_grad_(False)
        vae.to(accelerator.device, dtype=torch.float16)

        latents_cache = []
        for batch in tqdm(dataloader, desc="Đang cache VAE latents"):
            with torch.no_grad():
                pixel_values = batch["pixel_values"].to(accelerator.device, dtype=torch.float16)
                latents_cache.append(vae.encode(pixel_values).latent_dist)

        del vae
        free_memory()
        return latents_cache


    # ==========================================
    # 3. VÒNG LẶP TRAINING CHÍNH
    # ==========================================
    def main(args):
        # --- Khởi tạo môi trường huấn luyện (Accelerator lo việc mixed-precision, logging, multi-GPU...) ---
        accelerator = Accelerator(
            gradient_accumulation_steps=args.gradient_accumulation_steps,
            mixed_precision=args.mixed_precision,
            log_with=args.report_to,
            project_config=ProjectConfiguration(
                project_dir=args.output_dir,
                logging_dir=Path(args.output_dir, "logs"),
            ),
            kwargs_handlers=[DistributedDataParallelKwargs(find_unused_parameters=True)],
        )

        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.INFO)
        if accelerator.is_main_process:
            os.makedirs(args.output_dir, exist_ok=True)
        if args.seed is not None:
            set_seed(args.seed)  # cố định seed để kết quả có thể tái lập

        # --- Chuẩn bị Dataset & DataLoader ---
        train_dataset = DreamBoothDataset(
            dataset_path=args.dataset_path,
            embeddings_path=args.embeddings_path,
            width=args.width,
            height=args.height,
        )
        train_dataloader = DataLoader(train_dataset, batch_size=args.train_batch_size, shuffle=True, collate_fn=collate_fn)

        # --- Chuẩn bị Model & gắn LoRA ---
        noise_scheduler, vae, transformer = setup_models(args)
        vae_config = vae.config
        transformer = apply_lora_to_transformer(transformer, args)

        if args.mixed_precision == "fp16":
            cast_training_params([transformer], dtype=torch.float32)

        # --- Cache latents (giải phóng VAE khỏi GPU ngay sau khi cache xong) ---
        latents_cache = cache_latents(vae, train_dataloader, accelerator)

        # --- Optimizer 8-bit & Scheduler tốc độ học ---
        optimizer = bnb.optim.AdamW8bit(
            [{"params": [p for p in transformer.parameters() if p.requires_grad], "lr": args.learning_rate}],
            betas=(0.9, 0.999),
            weight_decay=0.0001,
            eps=1e-08,
        )

        num_update_steps_per_epoch = math.ceil(len(train_dataloader) / args.gradient_accumulation_steps)
        args.max_train_steps = args.max_train_steps or (args.num_train_epochs * num_update_steps_per_epoch)
        args.num_train_epochs = math.ceil(args.max_train_steps / num_update_steps_per_epoch)

        lr_scheduler = get_scheduler("constant", optimizer=optimizer, num_warmup_steps=0, num_training_steps=args.max_train_steps)

        transformer, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
            transformer, optimizer, train_dataloader, lr_scheduler
        )

        # --- Cấu hình tracker (wandb) & hook lưu checkpoint ---
        if accelerator.is_main_process:
            accelerator.init_trackers("dreambooth-flux-dev-lora", config=vars(args))

        def save_model_hook(models, weights, output_dir):
            if accelerator.is_main_process:
                for model in models:
                    model_to_save = accelerator.unwrap_model(model)
                    model_to_save = model_to_save._orig_mod if is_compiled_module(model_to_save) else model_to_save
                    lora_layers = get_peft_model_state_dict(model_to_save)
                    FluxPipeline.save_lora_weights(output_dir, transformer_lora_layers=lora_layers, text_encoder_lora_layers=None)
                    if weights:
                        weights.pop()

        accelerator.register_save_state_pre_hook(save_model_hook)

        # ==========================
        # VÒNG LẶP TRAINING
        # ==========================
        global_step = 0
        progress_bar = tqdm(range(args.max_train_steps), desc="Đang huấn luyện", disable=not accelerator.is_local_main_process)

        def get_sigmas(timesteps, n_dim=4, dtype=torch.float32):
            sigmas = noise_scheduler.sigmas.to(device=accelerator.device, dtype=dtype)
            schedule_timesteps = noise_scheduler.timesteps.to(accelerator.device)
            step_indices = [(schedule_timesteps == t).nonzero().item() for t in timesteps.to(accelerator.device)]
            sigma = sigmas[step_indices].flatten()
            while len(sigma.shape) < n_dim:
                sigma = sigma.unsqueeze(-1)
            return sigma

        for epoch in range(args.num_train_epochs):
            for step, batch in enumerate(train_dataloader):
                with accelerator.accumulate([transformer]):
                    # 1. Lấy latent đã cache sẵn, áp dụng hệ số scale của VAE
                    model_input = latents_cache[step].sample()
                    model_input = (model_input - vae_config.shift_factor) * vae_config.scaling_factor
                    model_input = model_input.to(dtype=torch.float16)
                    bsz = model_input.shape[0]

                    # 2. Tạo nhiễu ngẫu nhiên và trộn vào ảnh theo một mức độ (timestep) ngẫu nhiên
                    #    -> đây là bản chất của "diffusion": học cách "khử nhiễu"
                    noise = torch.randn_like(model_input)
                    u = compute_density_for_timestep_sampling("none", bsz, 0.0, 1.0, 1.29)
                    indices = (u * noise_scheduler.config.num_train_timesteps).long()
                    timesteps = noise_scheduler.timesteps[indices].to(device=model_input.device)

                    sigmas = get_sigmas(timesteps, n_dim=model_input.ndim, dtype=model_input.dtype)
                    noisy_model_input = (1.0 - sigmas) * model_input + sigmas * noise

                    # 3. Đưa dữ liệu về đúng định dạng mà FLUX cần (pack thành chuỗi "patch")
                    packed_noisy_model_input = FluxPipeline._pack_latents(
                        noisy_model_input, model_input.shape[0], model_input.shape[1], model_input.shape[2], model_input.shape[3]
                    )
                    latent_image_ids = FluxPipeline._prepare_latent_image_ids(
                        model_input.shape[0], model_input.shape[2] // 2, model_input.shape[3] // 2, accelerator.device, torch.float16
                    )

                    unwrapped_transformer = accelerator.unwrap_model(transformer)
                    guidance = torch.tensor([args.guidance_scale], device=accelerator.device).expand(bsz) if unwrapped_transformer.config.guidance_embeds else None

                    # 4. Forward pass: mô hình cố dự đoán phần nhiễu đã thêm vào, dựa trên caption (prompt_embeds)
                    model_pred = transformer(
                        hidden_states=packed_noisy_model_input,
                        timestep=timesteps / 1000,
                        guidance=guidance,
                        pooled_projections=batch["pooled_prompt_embeds"].to(accelerator.device, dtype=torch.float16),
                        encoder_hidden_states=batch["prompt_embeds"].to(accelerator.device, dtype=torch.float16),
                        txt_ids=batch["text_ids"].to(accelerator.device, dtype=torch.float16),
                        img_ids=latent_image_ids,
                        return_dict=False,
                    )[0]

                    # 5. Tính loss = sai khác giữa nhiễu dự đoán và nhiễu thật
                    vae_scale_factor = 2 ** (len(vae_config.block_out_channels) - 1)
                    model_pred = FluxPipeline._unpack_latents(
                        model_pred, model_input.shape[2] * vae_scale_factor, model_input.shape[3] * vae_scale_factor, vae_scale_factor
                    )

                    weighting = compute_loss_weighting_for_sd3("none", sigmas)
                    target = noise - model_input
                    loss = torch.mean(
                        (weighting.float() * (model_pred.float() - target.float()) ** 2).reshape(target.shape[0], -1), 1
                    ).mean()

                    # 6. Lan truyền ngược & cập nhật trọng số LoRA (chỉ LoRA được cập nhật, phần gốc vẫn đóng băng)
                    accelerator.backward(loss)
                    if accelerator.sync_gradients:
                        accelerator.clip_grad_norm_(transformer.parameters(), 1.0)
                    optimizer.step()
                    lr_scheduler.step()
                    optimizer.zero_grad()

                # --- Cập nhật thanh tiến trình & lưu checkpoint định kỳ ---
                if accelerator.sync_gradients:
                    progress_bar.update(1)
                    global_step += 1

                    if global_step % args.checkpointing_steps == 0 and accelerator.is_main_process:
                        save_path = os.path.join(args.output_dir, f"checkpoint-{global_step}")
                        accelerator.save_state(save_path)
                        print(f"💾 Đã lưu checkpoint tại bước {global_step}: {save_path}")

                logs = {"loss": loss.detach().item(), "lr": lr_scheduler.get_last_lr()[0]}
                progress_bar.set_postfix(**logs)
                accelerator.log(logs, step=global_step)

                if global_step >= args.max_train_steps:
                    break

        # ==========================
        # LƯU KẾT QUẢ CUỐI CÙNG
        # ==========================
        accelerator.wait_for_everyone()
        if accelerator.is_main_process:
            model_to_save = accelerator.unwrap_model(transformer)
            transformer_lora_layers = get_peft_model_state_dict(model_to_save)
            FluxPipeline.save_lora_weights(args.output_dir, transformer_lora_layers=transformer_lora_layers, text_encoder_lora_layers=None)
            print(f"✅ Đã lưu trọng số LoRA cuối cùng vào: {args.output_dir}")

        if torch.cuda.is_available():
            print(f"Bộ nhớ GPU tối đa đã dùng trong lúc train: {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

        accelerator.end_training()

    return FluxTransformer2DModel, gc, main


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🌟 Thử thách nâng cao (không bắt buộc): `_apply_transforms`

    Nếu nhóm còn thời gian và muốn thử sức thêm, hãy thử tự viết lại phương thức `DreamBoothDataset._apply_transforms`
    ở trên (đang được cho sẵn) mà **không nhìn code mẫu**: pipeline resize → random crop → chuyển thành tensor →
    chuẩn hoá về khoảng `[-1, 1]`. Đây là một pipeline tiền xử lý ảnh rất phổ biến trong Computer Vision, đáng để
    luyện tập thêm ngoài giờ học.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3. Cấu hình & bắt đầu training

    📌 **Các tham số các em có thể điều chỉnh** (giải thích ngay trong comment bên cạnh mỗi dòng):

    - `max_train_steps`: số bước train — bắt đầu thấp (~100) để test nhanh, sau đó tăng dần (300-700) khi đã chắc chắn mọi thứ chạy ổn.
    - `num_train_epochs`: số lần mô hình đi qua toàn bộ tập dữ liệu. Nếu đã đặt `max_train_steps` thì tham số này thường không còn tác dụng, vì quá trình train sẽ dừng khi đạt đủ số bước.
    - `rank`: rank của LoRA — mặc định 4 là khá nhỏ (nhẹ, nhanh); có thể thử tăng lên 8 hoặc 16 nếu muốn mô hình học chi tiết hơn (nhưng sẽ tốn VRAM và thời gian hơn).
    - `learning_rate`: tốc độ học — nếu để quá cao, mô hình có thể học "quá đà" (overfitting) hoặc mất ổn định.
    - `width`, `height`: kích thước ảnh dùng để train — càng lớn càng tốn VRAM.
    """)
    return


@app.cell
def _(main, torch):
    class TrainingConfig:
        pretrained_model_name = "black-forest-labs/FLUX.1-dev"

        # ✅ VIỆC CẦN LÀM: đổi các đường dẫn dataset_path, embeddings_path, output_dir này cho khớp với dataset & tên địa danh của nhóm em
        dataset_path = '/marimo/quang_phu/'                     # thư mục ảnh + caption (đã tạo ở Bước 0.2)
        embeddings_path = "/marimo/embeddings_quang_phu.parquet"                    # file .parquet đã tạo ở Bước 1
        output_dir = f"quang_phu_lora_flux_nf4"      # nơi lưu trọng số LoRA sau khi train xong

        mixed_precision = "fp16"
        width = 768
        height = 768
        train_batch_size = 1
        learning_rate = 1e-4
        guidance_scale = 1.0
        report_to = None          # đổi thành "none" nếu không dùng wandb ở Bước 2.1
        gradient_accumulation_steps = 4
        gradient_checkpointing = True
        rank = 4                      # rank LoRA: thử tăng lên 8/16 nếu muốn học chi tiết hơn
        num_train_epochs = 1
        max_train_steps = 300         # ⬅️ bắt đầu với số nhỏ để test, sau đó tăng dần (vd: 300-700)
        seed = 0
        checkpointing_steps = 100

    config = TrainingConfig()

    main(config)
    torch.cuda.empty_cache()
    return (config,)


@app.cell
def _():
    #Up lên hugging face
    from huggingface_hub import HfApi, login

    # 1. Đăng nhập với Write Token
    HF_TOKEN = "hf_XXXX"  # 👈 Thay bằng token của bạn
    login(token=HF_TOKEN)

    # 2. Cấu hình thông tin Upload
    repo_id = "User/quang-phu-lora-flux"  # 👈 Thay 'username' bằng tên tài khoản HF của bạn
    folder_path = "quang_phu_lora_flux_nf4"  # Thư mục output_dir đã cài đặt trong TrainingConfig

    # 3. Tạo Repo trên Hugging Face và Upload
    api = HfApi()
    api.create_repo(repo_id=repo_id, exist_ok=True, private=False)

    api.upload_folder(
        folder_path=folder_path,
        repo_id=repo_id,
        repo_type="model",
    )

    print(f"✅ Đã upload thành công LoRA lên: https://huggingface.co/{repo_id}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🎨 BƯỚC 3: Suy luận (Inference) — Vẽ ảnh với mô hình đã fine-tune

    ### 📌 Giải thích
    Sau khi train xong, ta đã có trọng số LoRA lưu trong thư mục `lora_path`. Bây giờ ta sẽ:
    1. Tải lại `FLUX.1-dev` gốc (vẫn ở dạng nén 4-bit để tiết kiệm VRAM khi chạy trên GPU nhỏ).
    2. Vẽ một ảnh **TRƯỚC khi nạp LoRA** (`before_lora.png`) — đây là những gì FLUX.1-dev "biết" từ trước, thường
       là một đồi cát chung chung, không đúng đặc trưng Quang Phú.
    3. Nạp trọng số LoRA vừa train (`pipeline.load_lora_weights(...)`).
    4. Vẽ lại **CÙNG một prompt, cùng seed** nhưng **SAU khi nạp LoRA** (`after_lora.png`) để so sánh trực tiếp.

    Chú ý: prompt dùng để test phải chứa đúng **trigger word** mà nhóm đã dùng khi viết caption (ví dụ `qp_dunes`),
    nếu không mô hình sẽ không biết "kích hoạt" phần kiến thức mới đã học.

    Ô inference dưới đây được cho sẵn đầy đủ (đây là lúc "gặt hái thành quả" sau khi đã vượt qua các bài tập ở
    Bước 1 & 2!) — các em chỉ cần đổi `prompt` cho đúng trigger word/mô tả của nhóm mình.
    """)
    return


@app.cell
def _(FluxPipeline, FluxTransformer2DModel, T5EncoderModel, config, gc, torch):
    from diffusers import BitsAndBytesConfig as DiffusersBitsAndBytesConfig
    from transformers import BitsAndBytesConfig as TransformersBitsAndBytesConfig

    ckpt_id = "black-forest-labs/FLUX.1-dev"
    lora_path = config.output_dir          # thư mục LoRA vừa train ở Bước 2
    bnb_4bit_compute_dtype = torch.float16

    # 1. Cấu hình lượng tử hoá (giống lúc train) để tải mô hình gốc gọn nhẹ hơn
    nf4_config = DiffusersBitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=bnb_4bit_compute_dtype,
    )
    quant_config = TransformersBitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    # 2. Tải transformer (mô hình vẽ ảnh) + text encoder
    transformer = FluxTransformer2DModel.from_pretrained(
        ckpt_id, subfolder="transformer", quantization_config=nf4_config, torch_dtype=torch.float16
    )
    text_encoder = T5EncoderModel.from_pretrained(
        ckpt_id, subfolder="text_encoder_2", quantization_config=quant_config, torch_dtype=torch.float16
    )

    # 3. Khởi tạo pipeline suy luận đầy đủ
    pipeline = FluxPipeline.from_pretrained(
        ckpt_id, transformer=transformer, text_encoder_2=text_encoder, torch_dtype=bnb_4bit_compute_dtype
    )

    del text_encoder, transformer
    gc.collect()
    torch.cuda.empty_cache()

    pipeline.to("cuda")

    # ✅ VIỆC CẦN LÀM: đổi prompt cho đúng trigger word + mô tả địa danh của nhóm em
    prompt = "qp_dunes, quang phu sand dunes, sand dunes in vietnam"

    # ==========================================
    # VẼ ẢNH TRƯỚC KHI NẠP LORA
    # ==========================================
    print("Đang vẽ ảnh TRƯỚC khi nạp LoRA...")
    generator_before = torch.Generator(device="cpu").manual_seed(0)  # cố định seed để so sánh công bằng

    image_before = pipeline(
        prompt, num_inference_steps=28, guidance_scale=3.5, height=768, width=512, generator=generator_before
    ).images[0]

    image_before.save("before_lora.png")
    print(f"Bộ nhớ GPU đã dùng (trước LoRA): {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

    # ==========================================
    # NẠP TRỌNG SỐ LORA VỪA TRAIN
    # ==========================================
    print("\nĐang nạp trọng số LoRA...")
    pipeline.load_lora_weights(lora_path)

    # ==========================================
    # VẼ ẢNH SAU KHI NẠP LORA
    # ==========================================
    print("Đang vẽ ảnh SAU khi nạp LoRA...")
    generator_after = torch.Generator(device="cpu").manual_seed(0)   # cùng seed với ảnh "trước" để so sánh 1:1

    image_after = pipeline(
        prompt, num_inference_steps=28, guidance_scale=3.5, height=768, width=512, generator=generator_after
    ).images[0]

    image_after.save("after_lora.png")
    print(f"Bộ nhớ GPU đã dùng (sau LoRA): {torch.cuda.max_memory_reserved() / 1024**3:.3f} GB")

    # Hiển thị 2 ảnh cạnh nhau để so sánh
    (image_before, image_after)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## TODO🥇 3.1. Thử nghiệm nhiều prompt khác nhau

    Bây giờ mô hình đã "biết" đặc trưng địa danh, hãy thử sáng tạo bằng cách thay đổi phần còn lại của prompt
    (thời tiết, ánh sáng, góc chụp...) trong khi vẫn giữ nguyên trigger word — đây chính là lúc các em có thể
    sáng tạo tự do để tìm ra những bức ảnh đẹp nhất làm Poster!
    """)
    return


@app.cell
def _():
    ## Viết code thử nghiệm ở đây các em nhé
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    # 🖋️ BƯỚC 4: Sáng tạo Poster — Thêm Typography hoàn thiện

    ### 📌 Giải thích
    Đây là bước cuối cùng được nhắc tới trong slide dự án: *"Dùng Prompt Engineering để AI vẽ hình ảnh. Cuối
    cùng, thêm Typography nghệ thuật bằng code Python để tạo ra tấm Poster hoàn chỉnh."*

    Ảnh AI vẽ ra ở Bước 3 mới chỉ là **nền (background)**. Để biến nó thành một tấm **Poster du lịch thực sự**,
    ta cần dùng thư viện `Pillow (PIL)` để chèn thêm:
    - Một lớp phủ mờ (gradient overlay) phía dưới để chữ dễ đọc hơn khi đặt trên ảnh.
    - Tiêu đề lớn (tên địa danh).
    - Phụ đề / khẩu hiệu quảng bá.
    - (Tuỳ chọn) logo hoặc tên chương trình ở góc ảnh.

    ### ✏️ BÀI TẬP 5 (Sáng tạo, không có đáp án "đúng" duy nhất): Hoàn thành `make_poster`

    **Mục tiêu học được:** vẽ hình bằng `PIL.ImageDraw`, xử lý toạ độ, và — quan trọng nhất — tự thiết kế bố cục
    poster theo phong cách riêng của nhóm. Đây là bài tập **mở**, không có một đáp án duy nhất;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## TODO: dựa vào code mẫu ở phía dưới, hãy viết lại hàm `add_poster_text` sao cho kết quả phần chữ của Poster được đẹp và nghệ thuật hơn
    """)
    return


@app.cell
def _(Image):
    from PIL import ImageDraw, ImageFont, ImageFilter

    def add_poster_text(
        image: Image.Image,
        title: str,
        subtitle: str = None,
        tagline: str = None,
        output_path: str = "poster.png"
    ):
        image = image.convert("RGBA")
        W, H = image.size

        def load_font(size, bold=False):
            font_candidates = [
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
            for path in font_candidates:
                try:
                    return ImageFont.truetype(path, size=size)
                except:
                    continue
            return ImageFont.load_default()

        tagline_font  = load_font(int(H * 0.018), bold=False)
        title_font    = load_font(int(H * 0.055), bold=True)   # reduced from 0.095
        divider_font  = load_font(int(H * 0.020), bold=False)
        subtitle_font = load_font(int(H * 0.022), bold=False)

        # --- Bottom gradient overlay ---
        gradient_height = int(H * 0.40)
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for i in range(gradient_height):
            alpha = int(200 * (i / gradient_height) ** 1.5)
            y = H - gradient_height + i
            overlay_draw.rectangle([(0, y), (W, y + 1)], fill=(0, 0, 0, alpha))
        image = Image.alpha_composite(image, overlay)
        draw = ImageDraw.Draw(image)

        def draw_centered(text, font, y, fill=(255, 255, 255), spacing=2, shadow=True):
            # Auto-fit: reduce spacing if text would overflow
            spaced = (" " * spacing).join(text) if spacing > 0 else text
            bbox = draw.textbbox((0, 0), spaced, font=font)
            text_w = bbox[2] - bbox[0]

            # If still too wide, drop spacing entirely
            if text_w > W * 0.85:
                spaced = text
                bbox = draw.textbbox((0, 0), spaced, font=font)
                text_w = bbox[2] - bbox[0]

            x = (W - text_w) // 2
            if shadow:
                for offset in [(2, 2), (3, 3)]:
                    draw.text((x + offset[0], y + offset[1]), spaced, font=font, fill=(0, 0, 0, 120))
            draw.text((x, y), spaced, font=font, fill=fill)
            return bbox[3] - bbox[1]

        # --- Layout from bottom up ---
        padding_bottom = int(H * 0.04)

        # Subtitle
        if subtitle:
            draw_centered(subtitle, subtitle_font,
                          H - padding_bottom - int(H * 0.028),
                          fill=(210, 200, 185), spacing=2)

        # Divider
        divider_y = H - padding_bottom - int(H * 0.065)
        divider_text = "── ✦ ──"
        bbox = draw.textbbox((0, 0), divider_text, font=divider_font)
        draw.text(((W - (bbox[2] - bbox[0])) // 2, divider_y),
                  divider_text, font=divider_font, fill=(200, 180, 140))

        # Title
        title_y = divider_y - int(H * 0.075)
        draw_centered(title, title_font, title_y,
                      fill=(255, 248, 230), spacing=4)  # reduced from 8

        # Tagline
        if tagline:
            tagline_y = title_y - int(H * 0.035)
            draw_centered(tagline.upper(), tagline_font, tagline_y,
                          fill=(190, 165, 110), spacing=5, shadow=False)

        image = image.convert("RGB")
        image.save(output_path, quality=95)
        return image

    return (add_poster_text,)


@app.cell
def _(Image, add_poster_text):
    # ✅ VIỆC CẦN LÀM: đổi title/subtitle cho đúng địa danh & thông điệp quảng bá của nhóm em
    # Usage
    poster = add_poster_text(
        Image.open("after_lora.png"),
        title="QUANG PHU",
        subtitle="Sand Dunes  ·  Quảng Bình, Việt Nam",
        output_path="quang_phu_poster.png"
    )
    poster.save("poster_quang_phu_final.png")
    print("✅ Đã lưu poster hoàn chỉnh: poster_quang_phu_final.png")
    poster
    return


@app.cell
def _():
    ## TODO: viết code tạo ra nhiều Poster hơn từ model đã finetune nữa nào!!! Phần này mình có thể dùng làm kết quả cho phần demo project.
    return


if __name__ == "__main__":
    app.run()
