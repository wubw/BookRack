# analyze_ebook

PDF ebook analyzer — detects whether a PDF is text-based, scanned images, or mixed
content. Useful for deciding which books in a library need OCR before reading or
indexing.

## Install

```bash
pip install -r requirements.txt
```

## Usage

Run from this folder.

```bash
# Single file — text output
python cli.py path/to/book.pdf

# Single file — JSON output
python cli.py path/to/book.pdf --json

# Batch a directory (recursive) — writes CSV next to the input by default
python cli.py path/to/library

# Batch with explicit CSV output and quiet progress
python cli.py path/to/library -o results.csv -q
```

Exit codes: `0` success, `1` input error, `2` processing error.

## Output

For each PDF the analyzer reports:

- `content_type`: `text` | `scanned` | `mixed`
- `confidence`: 0.0 – 1.0
- Per-PDF statistics: total/avg text per page, image count, image coverage, ratios
  of pages with text vs images.

Heuristics live in `analyzer.py:analyze_pdf` (thresholds on text-per-page and
image-page-ratio).

## Tests

```bash
python -m pytest test_analyze_ebook.py
```
