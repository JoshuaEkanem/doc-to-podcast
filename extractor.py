from pathlib import Path
import fitz  # pymupdf
from docx import Document


def extract_text(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_from_pdf(path)
    elif suffix == ".docx":
        return extract_from_docx(path)
    elif suffix == ".txt":
        return path.read_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def extract_from_pdf(path: Path) -> str:
    text = []
    with fitz.open(str(path)) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text).strip()


def extract_from_docx(path: Path) -> str:
    doc = Document(str(path))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extractor.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    text = extract_text(file_path)

    print(f"\n--- Extracted Text ({len(text)} characters) ---\n")
    print(text[:1000])  # preview first 1000 characters
    print("\n--- End of preview ---")