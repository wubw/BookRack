def parse_filename(filename):
    """
    Parse a filename to extract unit name and part name.
    
    Args:
        filename (str): Filename in format "unit_X_PARTNAME" or "unit_X_PARTNAME.md"
                       Can include folder path like "parts/unit_1_AM.md"
    
    Returns:
        tuple: (unit_name, part_name) or (None, None) if parsing fails
    
    Example:
        >>> parse_filename("unit_1_AM")
        ('unit_1', 'AM')
        >>> parse_filename("unit_1_AM.md")
        ('unit_1', 'AM')
        >>> parse_filename("parts/unit_10_BENE.md")
        ('unit_10', 'BENE')
        >>> parse_filename("d:/folder/parts/unit_1_AM.md")
        ('unit_1', 'AM')
    """
    import os
    
    # Extract just the filename without directory path
    basename = os.path.basename(filename)
    
    # Remove file extension if present
    if basename.endswith('.md'):
        basename = basename[:-3]
    
    # Split by underscore
    parts = basename.split('_')
    
    # Need at least 3 parts: "unit", number, and part name
    if len(parts) < 3:
        return None, None
    
    # First two parts form the unit name (e.g., "unit" + "1" = "unit_1")
    if parts[0] == 'unit':
        unit_name = f"{parts[0]}_{parts[1]}"
        # Everything after unit_X is the part name
        part_name = '_'.join(parts[2:])
        return unit_name, part_name
    
    return None, None


def read_blocks_from_part_file(filepath):
    """
    Read a part file and extract blocks separated by empty lines.
    
    Args:
        filepath (str): Path to the part file (e.g., "parts/unit_1_AM.md")
    
    Returns:
        list: List of blocks, where each block is a list of lines (strings)
    
    Example:
        >>> blocks = read_blocks_from_part_file("parts/unit_1_AM.md")
        >>> for i, block in enumerate(blocks):
        ...     print(f"Block {i}: {len(block)} lines")
    """
    from pathlib import Path
    
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    blocks = []
    current_block = []
    
    for line in lines:
        # Check if line is empty (only whitespace or newline)
        if line.strip() == '':
            # If we have accumulated lines, save as a block
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            # Add non-empty line to current block
            current_block.append(line.rstrip('\n'))
    
    # Don't forget the last block if file doesn't end with empty line
    if current_block:
        blocks.append(current_block)
    
    return blocks


def handle_blocks(filepath, blocks, output_file="output.md"):
    """
    Process blocks from a part file and append results to output file.
    
    Args:
        filepath (str): Path to the part file
        blocks (list): List of blocks, where each block is a list of lines
        output_file (str): Path to the output markdown file (default: "output.md")
    
    Returns:
        list: List of headers extracted from blocks before Quiz section
    """
    unit_name, part_name = parse_filename(filepath)
    print(f"\nProcessing {filepath}")
    print(f"  Unit: {unit_name}, Part: {part_name}")
    
    headers = []
    for b in blocks:
        if len(b) <= 1:
            continue
        arr = []
        for line in b:
            if line.startswith('###'):
                c = line.replace('###', '').strip()
                arr.append(c)
            elif line.startswith('##'):
                c = line.replace('##', '').strip()
                arr.append(c)
            elif line.startswith('#'):
                c = line.replace('#', '').strip()
                arr.append(c)
        if arr:
            header = arr[0]
            if header.startswith('Quiz'):
                break
            
            if header == part_name:
                result = header + ": " + ' '.join(arr[1:])
            else:
                translate_words = translate_word(header)
                result = header + ": " + translate_words
            
            headers.append(result)
    
    print(f"  Found {len(headers)} headers: {headers}")
    
    # Append results to output file
    from pathlib import Path
    output_path = Path(output_file)
    
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f"\n## {unit_name} - {part_name}\n\n")
        for header in headers:
            f.write(f"- {header}\n")
        f.write("\n")
    
    return headers


def iterate_parts_folder(parts_folder="parts", output_file="output.md"):
    """
    Iterate all markdown files under parts folder and process their blocks.
    
    Args:
        parts_folder (str): Path to the parts folder (default: "parts")
        output_file (str): Path to the output markdown file (default: "output.md")
    
    Returns:
        None
    """
    from pathlib import Path
    
    parts_path = Path(parts_folder)
    
    if not parts_path.exists():
        print(f"Error: Parts folder not found: {parts_path}")
        return
    
    # Clear output file before starting
    output_path = Path(output_file)
    if output_path.exists():
        output_path.unlink()
    
    # Find all .md files in the parts folder
    md_files = sorted(parts_path.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {parts_folder}")
        return
    
    print(f"Found {len(md_files)} markdown files in {parts_folder}")
    
    # Process each file
    for filepath in md_files:
        blocks = read_blocks_from_part_file(filepath)
        handle_blocks(str(filepath), blocks, output_file)


def translate_word(english_word):
    """
    Translate an English word to Chinese using translation service.
    
    Args:
        english_word (str): English word to translate
    
    Returns:
        str: Chinese translation or empty string if translation fails
    
    Example:
        >>> translate_word("love")
        '爱'
        >>> translate_word("happy")
        '快乐'
    """
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.translate(english_word, src='en', dest='zh-cn')
        return result.text
    except Exception as e:
        print(f"Translation error for '{english_word}': {e}")
        return ""


if __name__ == "__main__":
    iterate_parts_folder()
    #print(translate_word('happy'))