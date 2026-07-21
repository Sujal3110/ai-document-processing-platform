import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path

# Windows explicit paths (fallback jar PATH nीट set nasel tar)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"

def extract_text_from_image(image_path: str) -> str:
    """Extract text from a single image file."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path: str) -> str:
    """Convert PDF pages to images, then OCR each page."""
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    full_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text += f"\n--- Page {i+1} ---\n{text}"
    return full_text

def process_document(file_path: str) -> str:
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

if __name__ == "__main__":
    text = process_document("data/sample_docs/invoice1.png")
    print(text)