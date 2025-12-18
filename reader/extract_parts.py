
def get_part_content_between(unit_file, part_name, next_part_name):
    """
    Extract the content between two specific parts from a unit markdown file.
    The content starts from the SECOND occurrence of part_name 
    and ends at the SECOND occurrence of next_part_name.
    
    Args:
        unit_file (str): Path to the unit markdown file
        part_name (str): Name of the current part
        next_part_name (str): Name of the next part
    
    Returns:
        str: The content between the two parts, or empty string if not found
    """
    with open(unit_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find all occurrences of both parts
    part_occurrences = 0
    next_part_occurrences = 0
    tmp_parts = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        header_text = ''

        if stripped.startswith('###') and not stripped.startswith('###-'):
            header_text = stripped.replace('###', '').strip()
        elif stripped.startswith('##') and not stripped.startswith('##-'):
            header_text = stripped.replace('##', '').strip()   

        # Skip empty or separator lines
        if not header_text or header_text == '-' * len(header_text):
            continue
        
        # Check if this is a simple match (for single-line part names)
        if header_text == part_name:
            part_occurrences = i
        elif header_text == next_part_name:
            next_part_occurrences = i
            if part_occurrences > 0 and next_part_occurrences > part_occurrences:
                tmp_parts.append(''.join(lines[part_occurrences:next_part_occurrences]))
                part_occurrences = 0
                next_part_occurrences = 0
    
    print(f"part_occurrences for '{part_name}': {part_occurrences}")
    print(f"next_part_occurrences for '{next_part_name}': {next_part_occurrences}")
    
    # Extract and return content
    content = '\r\n'.join(tmp_parts)
    return content.strip()


if __name__ == "__main__":
    for i in range(1, 31):
    #for i in range(18, 19):
        unit = f'unit_{i}'
        part_names_file = f'part_names/{unit}.md'  # Example unit file path
        with open(part_names_file, 'r', encoding='utf-8') as f:
            parts = f.read().split(',')
        print("Extracted parts:", parts)

        #continue
        for idx, x in enumerate(parts):
            print(f"Part {idx + 1}: {x}")
            part = parts[idx]
            next_part = parts[idx + 1] if idx + 1 < len(parts) else 'Answers'
            content = get_part_content_between(f'units/{unit}.md', part, next_part)
            #print(f"Content between '{part}' and '{next_part}':\n{content}\n")


            output_file = f"parts/{unit}_{part.replace('/', ',')}.md"
            
            # Write unit content to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
