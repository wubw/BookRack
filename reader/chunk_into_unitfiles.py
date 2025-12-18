import re
import os
from pathlib import Path


def separate_markdown_by_units(input_file, output_dir='units'):
    """
    Separate a markdown file into multiple files based on '# Unit x' headers.
    
    Args:
        input_file (str): Path to the input markdown file
        output_dir (str): Directory where unit files will be saved (default: 'units')
    
    Returns:
        list: List of created file paths
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Pattern to match "# Unit x" where x is a number (1-30)
    unit_pattern = re.compile(r'^# Unit (\d+)$', re.MULTILINE)
    
    # Find all unit headers and their positions
    matches = list(unit_pattern.finditer(content))
    
    if not matches:
        print("No unit headers found in the file.")
        return []
    
    created_files = []
    processed_units = set()  # Track which units we've already processed
    
    # Process each unit
    for i, match in enumerate(matches):
        unit_number = match.group(1)
        
        # Skip if we've already processed this unit number
        if unit_number in processed_units:
            print(f"Skipping duplicate: Unit {unit_number}")
            continue
        
        processed_units.add(unit_number)
        start_pos = match.start()
        
        # Determine end position (start of next unit or end of file)
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # Extract unit content
        unit_content = content[start_pos:end_pos].rstrip()
        
        # Create output filename
        output_file = output_path / f"unit_{unit_number}.md"
        
        # Write unit content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(unit_content)
        
        created_files.append(str(output_file))
        print(f"Created: {output_file}")
    
    print(f"\nTotal units created: {len(created_files)}")
    return created_files


def get_unit_parts(unit_file):
    """
    Extract the parts from a unit markdown file.
    Parts are defined as section headers (### lines) that appear before any Quiz section.
    If a part name starts with a lowercase letter, it's merged with the previous part.
    
    Args:
        unit_file (str): Path to the unit markdown file
    
    Returns:
        list: List of part names (strings)
    """
    parts = []
    
    with open(unit_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Stop when we encounter a Quiz line
            if 'Quiz' in line and line.startswith('#'):
                break
            
            # Extract section headers (### lines) but skip separators
            if line.startswith('###') and line != '###' and not line.startswith('###-'):
                # Remove the ### prefix and any trailing whitespace
                part_name = line.replace('###', '').strip()
                if part_name and part_name != '-' * len(part_name):  # Skip lines that are just dashes
                    # If part name starts with lowercase and we have previous parts, merge with last part
                    if part_name and part_name[0].islower() and parts:
                        parts[-1] = parts[-1] + ' ' + part_name
                    else:
                        parts.append(part_name)
    
    return parts


def main():
    """
    Main function to run the separator with command line arguments or defaults.
    """
    import sys
    
#    if len(sys.argv) < 2:
#        print("Usage: python chunk_into_unitfiles.py <input_file> [output_dir]")
#        print("Example: python chunk_into_unitfiles.py output.md units")
#        return
    
    #input_file = sys.argv[1]
    #output_dir = sys.argv[2] if len(sys.argv) > 2 else 'units'
    input_file = "output.md"
    output_dir = "units"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    separate_markdown_by_units(input_file, output_dir)


if __name__ == "__main__":
    main()
