import re

def extract_names(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract text inside name="...".
    names = re.findall(r'name="(.*?)"', content)

    # Write to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for name in names:
            file.write(name + '\n')

    print(f"Extraction complete. Check '{output_file}' for results.")

# Example usage:
input_path = 'Index.txt'   # Input file path
output_path = 'output.txt' # Output file path

extract_names(input_path, output_path)
