"""Core PDF analysis logic."""

import csv
import io
import json
from pathlib import Path

import fitz  # PyMuPDF


def find_pdf_files(directory: Path) -> list[Path]:
    """Recursively find all PDF files in a directory.

    Args:
        directory: Directory to search

    Returns:
        List of paths to PDF files, sorted alphabetically
    """
    pdf_files = list(directory.rglob("*.pdf"))
    pdf_files.extend(directory.rglob("*.PDF"))
    # Remove duplicates and sort
    pdf_files = sorted(set(pdf_files))
    return pdf_files


def analyze_batch(
    file_paths: list[Path],
    progress_callback: callable = None,
) -> list[dict]:
    """Analyze multiple PDF files.

    Args:
        file_paths: List of paths to PDF files
        progress_callback: Optional callback(current, total, file_path) for progress

    Returns:
        List of analysis results dictionaries
    """
    results = []
    total = len(file_paths)

    for i, file_path in enumerate(file_paths):
        if progress_callback:
            progress_callback(i + 1, total, file_path)

        try:
            result = analyze_pdf(file_path)
            result["path"] = str(file_path)
            result["status"] = "ok"
        except Exception as e:
            result = {
                "file": file_path.name,
                "path": str(file_path),
                "status": "error",
                "error": str(e),
            }

        results.append(result)

    return results


def analyze_page(page: fitz.Page) -> dict:
    """Analyze a single PDF page.

    Args:
        page: PyMuPDF page object

    Returns:
        Dictionary with page analysis results
    """
    # Get text content
    text = page.get_text("text")
    text_length = len(text.strip())

    # Get images
    images = page.get_images(full=True)
    image_count = len(images)

    # Calculate image coverage area
    image_area = 0
    page_rect = page.rect
    page_area = page_rect.width * page_rect.height

    for img in images:
        xref = img[0]
        try:
            img_rect = page.get_image_bbox(img)
            if img_rect:
                image_area += img_rect.width * img_rect.height
        except Exception:
            pass

    image_coverage = (image_area / page_area) if page_area > 0 else 0

    return {
        "text_length": text_length,
        "image_count": image_count,
        "image_coverage": round(image_coverage, 3),
    }


def analyze_pdf(file_path: Path) -> dict:
    """Analyze a PDF file to determine if it's text or scanned.

    Args:
        file_path: Path to PDF file

    Returns:
        Dictionary with analysis results
    """
    doc = fitz.open(str(file_path))

    total_pages = len(doc)
    total_text_length = 0
    total_images = 0
    total_image_coverage = 0
    pages_with_text = 0
    pages_with_images = 0

    page_results = []

    for page_num in range(total_pages):
        page = doc[page_num]
        result = analyze_page(page)
        page_results.append(result)

        total_text_length += result["text_length"]
        total_images += result["image_count"]
        total_image_coverage += result["image_coverage"]

        if result["text_length"] > 50:  # More than 50 chars considered "has text"
            pages_with_text += 1
        if result["image_count"] > 0:
            pages_with_images += 1

    doc.close()

    # Calculate averages
    avg_text_per_page = total_text_length / total_pages if total_pages > 0 else 0
    avg_image_coverage = total_image_coverage / total_pages if total_pages > 0 else 0
    text_page_ratio = pages_with_text / total_pages if total_pages > 0 else 0
    image_page_ratio = pages_with_images / total_pages if total_pages > 0 else 0

    # Determine content type
    # Scanned PDFs typically have: low text, high image coverage, images on most pages
    # Text PDFs typically have: high text, low image coverage

    if avg_text_per_page < 100 and image_page_ratio > 0.8:
        content_type = "scanned"
        confidence = min(1.0, (1 - text_page_ratio) * image_page_ratio)
    elif avg_text_per_page > 500 and text_page_ratio > 0.8:
        content_type = "text"
        confidence = min(1.0, text_page_ratio)
    elif avg_text_per_page > 200 and text_page_ratio > 0.5:
        content_type = "text"
        confidence = text_page_ratio * 0.8
    elif image_page_ratio > 0.7 and avg_text_per_page < 200:
        content_type = "scanned"
        confidence = image_page_ratio * 0.8
    else:
        content_type = "mixed"
        confidence = 0.5

    return {
        "file": file_path.name,
        "total_pages": total_pages,
        "content_type": content_type,
        "confidence": round(confidence, 2),
        "statistics": {
            "total_text_chars": total_text_length,
            "avg_text_per_page": round(avg_text_per_page),
            "total_images": total_images,
            "avg_image_coverage": round(avg_image_coverage, 2),
            "pages_with_text": pages_with_text,
            "pages_with_images": pages_with_images,
            "text_page_ratio": round(text_page_ratio, 2),
            "image_page_ratio": round(image_page_ratio, 2),
        },
    }


def format_results(results: dict, output_format: str = "text") -> str:
    """Format analysis results for output.

    Args:
        results: Analysis results dictionary
        output_format: "text" or "json"

    Returns:
        Formatted string
    """
    if output_format == "json":
        return json.dumps(results, indent=2)

    # Text format
    content_type = results["content_type"].upper()
    confidence_pct = int(results["confidence"] * 100)
    stats = results["statistics"]

    lines = [
        f"File: {results['file']}",
        f"Pages: {results['total_pages']}",
        "",
        f"Content Type: {content_type} ({confidence_pct}% confidence)",
        "",
        "Statistics:",
        f"  Total text characters: {stats['total_text_chars']:,}",
        f"  Avg text per page: {stats['avg_text_per_page']:,} chars",
        f"  Total images: {stats['total_images']}",
        f"  Avg image coverage: {int(stats['avg_image_coverage'] * 100)}%",
        f"  Pages with text: {stats['pages_with_text']}/{results['total_pages']} ({int(stats['text_page_ratio'] * 100)}%)",
        f"  Pages with images: {stats['pages_with_images']}/{results['total_pages']} ({int(stats['image_page_ratio'] * 100)}%)",
    ]

    # Add recommendation
    lines.append("")
    if results["content_type"] == "scanned":
        lines.append("Recommendation: This PDF appears to be scanned images. Consider using OCR to extract text.")
    elif results["content_type"] == "text":
        lines.append("Recommendation: This PDF contains extractable text. No OCR needed.")
    else:
        lines.append("Recommendation: This PDF has mixed content (both text and scanned pages).")

    return "\n".join(lines)


def results_to_csv_row(results: dict) -> dict:
    """Flatten results dictionary to a single-level dict for CSV.

    Args:
        results: Analysis results dictionary

    Returns:
        Flattened dictionary suitable for CSV row
    """
    row = {
        "file": results.get("file", ""),
        "path": results.get("path", ""),
        "status": results.get("status", "ok"),
        "total_pages": results.get("total_pages", ""),
        "content_type": results.get("content_type", ""),
        "confidence": results.get("confidence", ""),
    }

    if results.get("status") == "error":
        row["error"] = results.get("error", "")
    else:
        stats = results.get("statistics", {})
        row["total_text_chars"] = stats.get("total_text_chars", "")
        row["avg_text_per_page"] = stats.get("avg_text_per_page", "")
        row["total_images"] = stats.get("total_images", "")
        row["avg_image_coverage"] = stats.get("avg_image_coverage", "")
        row["pages_with_text"] = stats.get("pages_with_text", "")
        row["pages_with_images"] = stats.get("pages_with_images", "")
        row["text_page_ratio"] = stats.get("text_page_ratio", "")
        row["image_page_ratio"] = stats.get("image_page_ratio", "")

    return row


def format_results_csv(results_list: list[dict]) -> str:
    """Format batch results as CSV string.

    Args:
        results_list: List of analysis results dictionaries

    Returns:
        CSV formatted string
    """
    if not results_list:
        return ""

    columns = [
        "file",
        "path",
        "status",
        "total_pages",
        "content_type",
        "confidence",
        "total_text_chars",
        "avg_text_per_page",
        "total_images",
        "avg_image_coverage",
        "pages_with_text",
        "pages_with_images",
        "text_page_ratio",
        "image_page_ratio",
    ]

    # Check if any errors occurred
    has_errors = any(r.get("status") == "error" for r in results_list)
    if has_errors:
        columns.append("error")

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()

    for results in results_list:
        row = results_to_csv_row(results)
        writer.writerow(row)

    return output.getvalue()


def write_results_csv(results_list: list[dict], output_path: Path) -> None:
    """Write batch results to CSV file.

    Args:
        results_list: List of analysis results dictionaries
        output_path: Path to output CSV file
    """
    csv_content = format_results_csv(results_list)
    output_path.write_text(csv_content, encoding="utf-8")
