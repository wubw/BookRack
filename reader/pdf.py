
import pymupdf as fitz
from pathlib import Path

def pdf_to_markdown(pdf_path: str, md_path: str):
    doc = fitz.open(pdf_path)
    lines = []

    for page in doc:
        # Extract text with font info
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    if not text:
                        continue
                    size = s.get("size", 10)
                    # Very naive heading heuristic by font size
                    if size >= 20:
                        lines.append(f"# {text}")
                    elif 16 <= size < 20:
                        lines.append(f"## {text}")
                    elif 13 <= size < 16:
                        lines.append(f"### {text}")
                    else:
                        lines.append(text)
        lines.append("")  # blank line between blocks

    md = "\n".join(lines)
    Path(md_path).write_text(md, encoding="utf-8")

if __name__ == "__main__":
    path = "D:\AppsData\Calibre Library\Merriam-Webster\Merriam-Webster's Vocabulary Builder (3)\Merriam-Webster's Vocabulary Bu - Merriam-Webster.pdf"
    pdf_to_markdown(path, "output.md")
