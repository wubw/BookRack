
def get_unit_parts(unit_file):
    """
    Extract the parts from a unit markdown file.
    Parts are defined as section headers (### lines) that appear before any Quiz section.
    
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
                    # If the last part is "Words from", merge with current part
                    elif parts and parts[-1] == "Words from":
                        parts[-1] = parts[-1] + ' ' + part_name
                    else:
                        parts.append(part_name)
    
    return parts

if __name__ == "__main__":
    for i in range(1, 31):
    #for i in range(18, 19):
        unit = f'unit_{i}'
        unit_file = f'units/{unit}.md'  # Example unit file path
        parts = get_unit_parts(unit_file)
        print("Extracted parts:", parts)
        output_file = f"part_names/{unit}.md"
            
        # Write unit content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(",".join(parts))

