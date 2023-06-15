import itertools
import datetime
import random
import sys
import time

ascii_art = '''     ╔╗  ╔╗        ╔╗        ╔╗ 
     ║║ ╔╝╚╗       ║║       ╔╝╚╗
╔══╗ ║║ ╚╗╔╝╔══╗╔═╗║║ ╔╗╔══╗╚╗╔╝
╚ ╗║ ║║  ║║ ║╔╗║║╔╝║║ ╠╣║══╣ ║║ 
║╚╝╚╗║╚╗ ║╚╗║║═╣║║ ║╚╗║║╠══║ ║╚╗
╚═══╝╚═╝ ╚═╝╚══╝╚╝ ╚═╝╚╝╚══╝ ╚═╝
                                
                                '''

creator = "Created by h3iko (https://medium.com/@h3iko)"
twitter = "Twitter: @undefined_npc"

print(ascii_art)
print(creator)
print(twitter)
print("")

time.sleep(5)

def read_passwords_from_file(file_path):
    with open(file_path, "r") as file:
        passwords = file.read().splitlines()
    return passwords

def shuffle_passwords(passwords_list):
    random.shuffle(passwords_list)

def generate_variations(password):
    variations = []
    
    variations.append(password)
    
    generic_variations = [password.capitalize(), password.upper(), password.lower()]
    generic_variations.extend([password + ext for ext in ["123", "2023", "!", "@", "&", "?"]])
    variations.extend(generic_variations)

    l33t_variations = [
        password.replace("a", "4").replace("e", "3").replace("i", "1").replace("o", "0").replace("a", "@"),
        password.replace("a", "4").replace("e", "3").replace("i", "1").replace("o", "0"),
        password.replace("a", "4").replace("e", "3").replace("i", "1"),
        password.replace("a", "4").replace("e", "3"),
        password.replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0"),
        password.replace("a", "@").replace("e", "3").replace("i", "1"),
        password.replace("a", "@").replace("e", "3")
    ]
    variations.extend(l33t_variations)
    
    case_variations = [password.lower(), password.upper(), password.capitalize()]
    variations.extend(case_variations)
    
    current_year = datetime.datetime.now().year
    date_variations = []
    for year_offset in range(-10, 11):
        date_variations.append(password + str(current_year + year_offset))
        date_variations.append(str(current_year + year_offset) + password)
    variations.extend(date_variations)
    
    symbols = ["!", "@", "#", "$", "%", "&"]
    symbol_variations = [password + symbol for symbol in symbols]
    symbol_variations.extend([symbol + password for symbol in symbols])
    variations.extend(symbol_variations)
    
    return variations

def generate_all_variations(passwords_list):
    all_variations = []
    for password in passwords_list:
        variations = generate_variations(password)
        all_variations.extend(variations)
    return all_variations

def add_leet_variations(variations):
    leet_variations = []
    for variation in variations:
        for r in range(1, min(len(variation), 4)):
            for subset in itertools.combinations(range(len(variation)), r):
                leet_variation = variation
                for i in subset:
                    leet_variation = leet_variation[:i] + leet_variation[i].replace("a", "4").replace("e", "3").replace("i", "1").replace("o", "0") + leet_variation[i+1:]
                leet_variations.append(leet_variation)
    return leet_variations

def add_layer_to_variations(passwords_list):
    layered_variations = []
    for password in passwords_list:
        variations = generate_variations(password)
        for variation in variations:
            if variation not in layered_variations:
                layered_variations.append(variation)
                
    leet_variations = add_leet_variations(layered_variations)
    layered_variations.extend(leet_variations)
    
    return layered_variations

def translate_leetspeak(variation):
    leet_to_normal = {
        "4": "a",
        "3": "e",
        "1": "i",
        "0": "o",
        "@": "a"
    }
    translated_variations = set()
    translated_variations.add(variation)
    for leet, normal in leet_to_normal.items():
        translated_variations.add(variation.replace(leet, normal))
    return translated_variations

def generate_smart_variations(passwords_list):
    smart_variations = []
    for password in passwords_list:
        variations = generate_variations(password)
        smart_variations.extend(variations)
        
        for r in range(2, min(len(password), 5)):
            for subset in itertools.combinations(range(len(password)), r):
                custom_variation = list(password)
                for i in subset:
                    custom_variation[i] = random.choice(["@", "3", "1", "0"])
                smart_variations.append("".join(custom_variation))
    
    return smart_variations

def check_passwords(passwords_list):
    checked_passwords = []
    for password in passwords_list:
        has_symbols = any(c.isalnum() == False for c in password)
        if has_symbols:
            translations = set()
            for variation in passwords_list:
                if variation != password:
                    translations |= translate_leetspeak(variation)
            checked_passwords.extend(list(translations))
        checked_passwords.append(password)
    return checked_passwords

def count_lines_in_file(file_path):
    try:
        with open(file_path, "r") as file:
            line_count = sum(1 for line in file)
        print(f"Passwords generated : {line_count}")
    except FileNotFoundError:
        print(f"File '{file_path}' doesn't exist.")
    except IOError:
        print(f"Error while reading the file '{file_path}'.")
        
def print_help_menu():
    print("Usage :")
    print("python3 alterlist.py <password_file>")
    print("")

if len(sys.argv) != 2:
    print("Error : No password file.")
    print_help_menu()
    sys.exit(1)

print("Let me cook...")
passwords_file = sys.argv[1]

passwords = read_passwords_from_file(passwords_file)

if not passwords:
    print("Error : Password file is empty.")
    sys.exit(1)

shuffle_passwords(passwords)

checked_passwords = check_passwords(passwords)

smart_variations = generate_smart_variations(checked_passwords)

layered_variations = add_layer_to_variations(smart_variations)

output_file = "combined.txt"
with open(output_file, "w") as file:
    file.write("\n".join(layered_variations))

    
count_lines_in_file("combined.txt")

print("Passwords has been stored in", output_file)