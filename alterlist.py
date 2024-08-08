import itertools
import datetime
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ascii_art = '''     ╔╗  ╔╗        ╔╗        ╔╗ 
     ║║ ╔╝╚╗       ║║       ╔╝╚╗
╔══╗ ║║ ╚╗╔╝╔══╗╔═╗║║ ╔╗╔══╗╚╗╔╝
╚ ╗║ ║║  ║║ ║╔╗║║╔╝║║ ╠╣║══╣ ║║ 
║╚╝╚╗║╚╗ ║╚╗║║═╣║║ ║╚╗║║╠══║ ║╚╗
╚═══╝╚═╝ ╚═╝╚══╝╚╝ ╚═╝╚╝╚══╝ ╚═╝
                                
                                '''

creator = "Created by h3iko (https://medium.com/@h3iko)"
print(ascii_art)
print(creator)
print("")

def read_passwords_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            passwords = file.read().splitlines()
        return passwords
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)
    except IOError:
        print(f"Error: Could not read the file {file_path}.")
        sys.exit(1)

def leet_variations(password):
    leet_map = {
        'a': ['a', '@', '4'],
        'e': ['e', '3'],
        'i': ['i', '1'],
        'o': ['o', '0'],
        'l': ['l', '1'],
        't': ['t', '7'],
        's': ['s', '5']
    }
    
    def replace_chars(chars):
        if chars:
            first, rest = chars[0], chars[1:]
            for replacement in leet_map.get(first, [first]):
                for combo in replace_chars(rest):
                    yield replacement + combo
        else:
            yield ''
    
    return list(replace_chars(password))

def generate_variations(password, current_year):
    variations = set()

    cases = set(map(''.join, itertools.product(*([char.lower(), char.upper()] for char in password))))

    leet_variations_set = set()
    for case in cases:
        leet_variations_set.update(leet_variations(case))

    symbols = ["!", "@", "#", "$", "%", "&"]
    years = [str(current_year + offset) for offset in range(-10, 11)]

    for variation in leet_variations_set:
        variations.add(variation)

        for symbol in symbols:
            variations.add(variation + symbol)

        for symbol1, symbol2 in itertools.combinations(symbols, 2):
            variations.add(variation + symbol1 + symbol2)

        for suffix in itertools.chain(symbols, years):
            variations.add(variation + suffix)
            variations.add(suffix + variation)

        for symbol in symbols:
            for year in years:
                variations.add(variation + symbol + year)
                variations.add(symbol + year + variation)
                variations.add(year + symbol + variation)

    return list(variations)

def generate_all_variations(passwords_list):
    all_variations = set()
    current_year = datetime.datetime.now().year
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_variations, pw, current_year) for pw in passwords_list]
        for future in as_completed(futures):
            all_variations.update(future.result())
    return list(all_variations)

def print_help_menu():
    print("""
    Usage:
        python3 script.py --input <password_file> --output <output_file>
    
    Options:
        --input   : Path to the input file containing passwords (required)
        --output  : Path to the output file where variations will be stored (required)
    """)

def main():
    parser = argparse.ArgumentParser(description='Password variation generator.', add_help=False)
    parser.add_argument('--input', help='Path to the input file containing passwords', required=True)
    parser.add_argument('--output', help='Path to the output file where variations will be stored', required=True)
    args = parser.parse_args()

    if not args.input or not args.output:
        print("Error: Missing required arguments.")
        print_help_menu()
        sys.exit(1)

    passwords = read_passwords_from_file(args.input)

    if not passwords:
        print("Error: List file is empty.")
        sys.exit(1)

    print("Let me cook...")
    all_variations = generate_all_variations(passwords)

    with open(args.output, "w") as file:
        file.write("\n".join(all_variations))

    count_lines_in_file(args.output)

    print(f"Passwords have been stored in {args.output}")

def count_lines_in_file(file_path):
    try:
        with open(file_path, "r") as file:
            line_count = sum(1 for line in file)
        print(f"Passwords generated: {line_count}")
    except FileNotFoundError:
        print(f"File '{file_path}' doesn't exist.")
    except IOError:
        print(f"Error while reading the file '{file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: No arguments provided.")
        print_help_menu()
        sys.exit(1)
    main()
