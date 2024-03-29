import re

def process_line(line):
    # Remove special characters
    line = re.sub(r'[^\w-]', '', line)
    
    # Replace "_" with "-"
    line = line.replace("_", "-")
    
    # Replace consecutive hyphens with one hyphen
    line = '-'.join(filter(None, line.split('-')))
    
    # Remove leading and trailing hyphens
    line = line.strip('-')
    
    return line

def main(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        processed_line = process_line(line.rstrip('\n'))  # Strip the newline character before processing
        print(processed_line)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    main(input_file)
