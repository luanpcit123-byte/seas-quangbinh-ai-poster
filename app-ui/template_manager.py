import importlib
from pathlib import Path
from templates import template_1, template_2, template_3, template_4

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

TEMPLATE_MODULES = {
    "template_1": template_1,
    "template_2": template_2,
    "template_3": template_3,
    "template_4": template_4,
}

def apply_template(
    t_choice: str, 
    bg_path, 
    title: str, 
    subtitle: str, 
    location: str, 
    output_path: str = None
) -> str:
    if not output_path:
        output_path = str(OUTPUT_DIR / f"poster_{t_choice}.pdf")

    target_module = TEMPLATE_MODULES.get(t_choice)
    if not target_module:
        raise ValueError(f"Không tìm thấy template: {t_choice}")
    
    # ⚡ TỰ ĐỘNG RELOAD CODE KHI BẠN SỬA FILE .PY
    importlib.reload(target_module)
    
    render_func = getattr(target_module, "generate_pdf", None) or getattr(target_module, "render", None)
    if not render_func:
        raise AttributeError(f"Module {t_choice} chưa khai báo hàm 'generate_pdf'")
    
    return render_func(bg_path, title, subtitle, location, output_path)