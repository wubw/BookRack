"""Tests for analyze_ebook module."""

import tempfile
from pathlib import Path


def test_parse_args_minimal():
    """Test parsing minimal arguments."""
    from cli import parse_args

    args = parse_args(["input.pdf"])

    assert args.input == Path("input.pdf")
    assert args.json is False


def test_parse_args_json():
    """Test parsing with JSON flag."""
    from cli import parse_args

    args = parse_args(["book.pdf", "--json"])

    assert args.input == Path("book.pdf")
    assert args.json is True


def test_validate_input_file_not_found():
    """Test validation rejects missing files."""
    from cli import validate_input

    result = validate_input(Path("nonexistent.pdf"))

    assert result is not None
    assert "not found" in result.lower()


def test_validate_input_not_pdf():
    """Test validation rejects non-PDF files."""
    from cli import validate_input

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"not a pdf")
        path = Path(f.name)

    try:
        result = validate_input(path)
        assert result is not None
        assert "pdf" in result.lower()
    finally:
        path.unlink()


def test_format_results_text():
    """Test text formatting of results."""
    from analyzer import format_results

    results = {
        "file": "test.pdf",
        "total_pages": 10,
        "content_type": "text",
        "confidence": 0.95,
        "statistics": {
            "total_text_chars": 50000,
            "avg_text_per_page": 5000,
            "total_images": 5,
            "avg_image_coverage": 0.1,
            "pages_with_text": 10,
            "pages_with_images": 3,
            "text_page_ratio": 1.0,
            "image_page_ratio": 0.3,
        },
    }

    output = format_results(results, "text")

    assert "test.pdf" in output
    assert "TEXT" in output
    assert "95%" in output
    assert "50,000" in output


def test_format_results_json():
    """Test JSON formatting of results."""
    import json
    from analyzer import format_results

    results = {
        "file": "test.pdf",
        "total_pages": 10,
        "content_type": "scanned",
        "confidence": 0.85,
        "statistics": {
            "total_text_chars": 100,
            "avg_text_per_page": 10,
            "total_images": 10,
            "avg_image_coverage": 0.9,
            "pages_with_text": 1,
            "pages_with_images": 10,
            "text_page_ratio": 0.1,
            "image_page_ratio": 1.0,
        },
    }

    output = format_results(results, "json")
    parsed = json.loads(output)

    assert parsed["content_type"] == "scanned"
    assert parsed["confidence"] == 0.85


def test_format_results_scanned_recommendation():
    """Test recommendation for scanned PDFs."""
    from analyzer import format_results

    results = {
        "file": "scanned.pdf",
        "total_pages": 5,
        "content_type": "scanned",
        "confidence": 0.9,
        "statistics": {
            "total_text_chars": 50,
            "avg_text_per_page": 10,
            "total_images": 5,
            "avg_image_coverage": 0.95,
            "pages_with_text": 0,
            "pages_with_images": 5,
            "text_page_ratio": 0.0,
            "image_page_ratio": 1.0,
        },
    }

    output = format_results(results, "text")

    assert "OCR" in output


def test_format_results_text_recommendation():
    """Test recommendation for text PDFs."""
    from analyzer import format_results

    results = {
        "file": "text.pdf",
        "total_pages": 5,
        "content_type": "text",
        "confidence": 0.95,
        "statistics": {
            "total_text_chars": 25000,
            "avg_text_per_page": 5000,
            "total_images": 2,
            "avg_image_coverage": 0.05,
            "pages_with_text": 5,
            "pages_with_images": 2,
            "text_page_ratio": 1.0,
            "image_page_ratio": 0.4,
        },
    }

    output = format_results(results, "text")

    assert "No OCR needed" in output


def test_main_file_not_found(capsys):
    """Test main returns error for missing file."""
    from cli import main

    exit_code = main(["nonexistent.pdf"])

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err.lower()


def test_main_not_pdf(capsys):
    """Test main returns error for non-PDF."""
    from cli import main

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"not a pdf")
        path = f.name

    try:
        exit_code = main([path])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "pdf" in captured.err.lower()
    finally:
        Path(path).unlink()


def test_parse_args_directory():
    """Test parsing directory input with output option."""
    from cli import parse_args

    args = parse_args(["./ebooks", "-o", "results.csv"])

    assert args.input == Path("./ebooks")
    assert args.output == Path("results.csv")


def test_parse_args_quiet():
    """Test parsing quiet flag."""
    from cli import parse_args

    args = parse_args(["./ebooks", "-q"])

    assert args.quiet is True


def test_validate_input_directory():
    """Test validation accepts directories."""
    from cli import validate_input

    with tempfile.TemporaryDirectory() as tmpdir:
        result = validate_input(Path(tmpdir))
        assert result is None  # None means valid


def test_find_pdf_files_empty_dir():
    """Test find_pdf_files with empty directory."""
    from analyzer import find_pdf_files

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_files = find_pdf_files(Path(tmpdir))
        assert pdf_files == []


def test_results_to_csv_row():
    """Test flattening results to CSV row."""
    from analyzer import results_to_csv_row

    results = {
        "file": "test.pdf",
        "path": "/path/to/test.pdf",
        "status": "ok",
        "total_pages": 100,
        "content_type": "text",
        "confidence": 0.95,
        "statistics": {
            "total_text_chars": 50000,
            "avg_text_per_page": 500,
            "total_images": 10,
            "avg_image_coverage": 0.1,
            "pages_with_text": 100,
            "pages_with_images": 10,
            "text_page_ratio": 1.0,
            "image_page_ratio": 0.1,
        },
    }

    row = results_to_csv_row(results)

    assert row["file"] == "test.pdf"
    assert row["content_type"] == "text"
    assert row["total_text_chars"] == 50000


def test_results_to_csv_row_error():
    """Test flattening error results to CSV row."""
    from analyzer import results_to_csv_row

    results = {
        "file": "bad.pdf",
        "path": "/path/to/bad.pdf",
        "status": "error",
        "error": "Invalid PDF",
    }

    row = results_to_csv_row(results)

    assert row["file"] == "bad.pdf"
    assert row["status"] == "error"
    assert row["error"] == "Invalid PDF"


def test_format_results_csv():
    """Test CSV formatting of batch results."""
    from analyzer import format_results_csv

    results_list = [
        {
            "file": "text.pdf",
            "path": "/path/to/text.pdf",
            "status": "ok",
            "total_pages": 100,
            "content_type": "text",
            "confidence": 0.95,
            "statistics": {
                "total_text_chars": 50000,
                "avg_text_per_page": 500,
                "total_images": 10,
                "avg_image_coverage": 0.1,
                "pages_with_text": 100,
                "pages_with_images": 10,
                "text_page_ratio": 1.0,
                "image_page_ratio": 0.1,
            },
        },
        {
            "file": "scanned.pdf",
            "path": "/path/to/scanned.pdf",
            "status": "ok",
            "total_pages": 50,
            "content_type": "scanned",
            "confidence": 0.9,
            "statistics": {
                "total_text_chars": 100,
                "avg_text_per_page": 2,
                "total_images": 50,
                "avg_image_coverage": 0.95,
                "pages_with_text": 2,
                "pages_with_images": 50,
                "text_page_ratio": 0.04,
                "image_page_ratio": 1.0,
            },
        },
    ]

    csv_output = format_results_csv(results_list)

    assert "file,path,status" in csv_output
    assert "text.pdf" in csv_output
    assert "scanned.pdf" in csv_output
    assert "text" in csv_output
    assert "scanned" in csv_output


def test_format_results_csv_empty():
    """Test CSV formatting with empty results."""
    from analyzer import format_results_csv

    csv_output = format_results_csv([])

    assert csv_output == ""


def test_write_results_csv(tmp_path):
    """Test writing CSV to file."""
    from analyzer import write_results_csv

    results_list = [
        {
            "file": "test.pdf",
            "path": "/path/to/test.pdf",
            "status": "ok",
            "total_pages": 10,
            "content_type": "text",
            "confidence": 0.95,
            "statistics": {
                "total_text_chars": 5000,
                "avg_text_per_page": 500,
                "total_images": 2,
                "avg_image_coverage": 0.05,
                "pages_with_text": 10,
                "pages_with_images": 2,
                "text_page_ratio": 1.0,
                "image_page_ratio": 0.2,
            },
        },
    ]

    output_path = tmp_path / "results.csv"
    write_results_csv(results_list, output_path)

    assert output_path.exists()
    content = output_path.read_text()
    assert "test.pdf" in content
    assert "text" in content


def test_main_directory_no_pdfs(capsys):
    """Test main with directory containing no PDFs."""
    from cli import main

    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code = main([tmpdir])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "no pdf files" in captured.err.lower()
