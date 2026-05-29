"""Command-line interface for PDF ebook analysis."""

import argparse
import sys
from pathlib import Path

from analyzer import (
    analyze_pdf,
    analyze_batch,
    find_pdf_files,
    format_results,
    write_results_csv,
)


def validate_input(input_path: Path) -> str | None:
    """Validate input file or directory.

    Args:
        input_path: Path to input file or directory

    Returns:
        Error message if invalid, None if valid
    """
    if not input_path.exists():
        return f"Path not found: {input_path}"

    if input_path.is_file() and input_path.suffix.lower() != ".pdf":
        return f"Not a PDF file: {input_path} (expected .pdf extension)"

    return None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Arguments to parse (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="analyze-ebook",
        description="Analyze PDF to detect if content is text or scanned images",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input PDF file or directory (directories are searched recursively)",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output CSV file for batch results (required for directory input)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (single file only)",
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output (batch mode)",
    )

    return parser.parse_args(argv)


def print_progress(current: int, total: int, file_path: Path) -> None:
    """Print progress for batch processing.

    Args:
        current: Current file number (1-indexed)
        total: Total number of files
        file_path: Path to current file
    """
    print(f"[{current}/{total}] Analyzing: {file_path.name}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Main entry point.

    Args:
        argv: Command-line arguments

    Returns:
        Exit code (0=success, 1=input error, 2=processing error)
    """
    args = parse_args(argv)

    # Validate input
    error = validate_input(args.input)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Single file mode
    if args.input.is_file():
        try:
            results = analyze_pdf(args.input)
            output_format = "json" if args.json else "text"
            print(format_results(results, output_format))
        except Exception as e:
            print(f"Error during analysis: {e}", file=sys.stderr)
            return 2
        return 0

    # Directory mode
    if args.input.is_dir():
        # Find all PDF files
        pdf_files = find_pdf_files(args.input)

        if not pdf_files:
            print(f"No PDF files found in: {args.input}", file=sys.stderr)
            return 1

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            output_path = args.input / "ebook_analysis.csv"

        if not args.quiet:
            print(f"Found {len(pdf_files)} PDF file(s)", file=sys.stderr)
            print(f"Output: {output_path}", file=sys.stderr)
            print("", file=sys.stderr)

        # Progress callback
        progress_callback = None if args.quiet else print_progress

        # Analyze all files
        try:
            results_list = analyze_batch(pdf_files, progress_callback=progress_callback)
        except Exception as e:
            print(f"Error during batch analysis: {e}", file=sys.stderr)
            return 2

        # Write CSV
        try:
            write_results_csv(results_list, output_path)
        except Exception as e:
            print(f"Error writing CSV: {e}", file=sys.stderr)
            return 2

        # Summary
        ok_count = sum(1 for r in results_list if r.get("status") == "ok")
        error_count = len(results_list) - ok_count

        # Count by content type
        text_count = sum(1 for r in results_list if r.get("content_type") == "text")
        scanned_count = sum(1 for r in results_list if r.get("content_type") == "scanned")
        mixed_count = sum(1 for r in results_list if r.get("content_type") == "mixed")

        if not args.quiet:
            print("", file=sys.stderr)
            print(f"Complete: {ok_count} succeeded, {error_count} failed", file=sys.stderr)
            print(f"  Text-based: {text_count}", file=sys.stderr)
            print(f"  Scanned: {scanned_count}", file=sys.stderr)
            print(f"  Mixed: {mixed_count}", file=sys.stderr)
            print(f"Results saved to: {output_path}", file=sys.stderr)

        return 0 if error_count == 0 else 2

    return 1


if __name__ == "__main__":
    sys.exit(main())
