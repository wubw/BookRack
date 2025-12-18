import os
from pathlib import Path


def check_parts_integrity(parts_folder='parts'):
    """
    Check all files in the parts folder for integrity.
    Report error if any file has content less than 3 lines.
    
    Args:
        parts_folder (str): Path to the parts folder
    
    Returns:
        tuple: (pass_count, fail_count, failed_files)
    """
    parts_path = Path(parts_folder)
    
    if not parts_path.exists():
        print(f"Error: Parts folder '{parts_folder}' does not exist.")
        return 0, 0, []
    
    pass_count = 0
    fail_count = 0
    failed_files = []
    
    # Get all files in the parts folder
    files = sorted(parts_path.glob('*.md'))
    
    if not files:
        print(f"No markdown files found in '{parts_folder}'")
        return 0, 0, []
    
    print(f"Checking {len(files)} files in '{parts_folder}'...\n")
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')
            line_count = len(lines)
        
        if line_count < 3:
            fail_count += 1
            failed_files.append((file_path.name, line_count))
            print(f"❌ FAIL: {file_path.name} - Only {line_count} line(s)")
        else:
            pass_count += 1
            print(f"✓ PASS: {file_path.name} - {line_count} lines")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total files: {len(files)}")
    print(f"  Passed: {pass_count}")
    print(f"  Failed: {fail_count}")
    
    if failed_files:
        print(f"\nFailed files:")
        for filename, line_count in failed_files:
            print(f"  - {filename}: {line_count} line(s)")
    
    print(f"{'='*60}")
    
    return pass_count, fail_count, failed_files


if __name__ == "__main__":
    check_parts_integrity()
