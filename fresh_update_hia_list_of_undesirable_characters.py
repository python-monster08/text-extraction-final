import os
import datetime
from pathlib import Path

# Load the existing dictionary
def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        dictionary = eval(content.split('=', 1)[1].strip())
    return dictionary

# Write the updated dictionary to the file
def write_dictionary(dictionary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('hia_list_of_undesirable_characters_for_question_bank = ')
        file.write(repr(dictionary))
    print(f"Dictionary file updated at '{file_path}'")

# Add new unwanted characters to the dictionary
def add_unwanted_characters(input_file_path, dictionary_file_path):
    dictionary = load_dictionary(dictionary_file_path)
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Create a set to store all characters found in the input file
    all_characters = set()

    # Open the output file for writing the characters and their context
    output_file_path = Path(
        r"C:\Users\HP\Desktop\Question Bank Trials\Python Programming\Unwanted Characters etc") / f"unwanted_characters_{input_file_path.stem}.txt"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for char in text:
            if ord(char) > 127:
                all_characters.add(char)
                # Extract the sentence or words around the character
                context = extract_context(text, char)
                print(f"Character: {char} - Unicode: {ord(char)} - Context: {context}")
                output_file.write(f"Character: {char} - Unicode: {ord(char)} - Context: {context}\n")

                if char not in dictionary['unwanted_characters']:
                    dictionary['unwanted_characters'][char] = {
                        "replacement": "",
                        "date_added": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "file_name": input_file_path.name,
                        "source_of_replacement": "",
                        "character_update_number": 1,  # Increment this for each update
                        "replacement_update_number": 0  # Keep this as 0 for new characters
                    }

        write_dictionary(dictionary, dictionary_file_path)

    print(f"All characters found in the input file have been saved to '{output_file_path}'")

# Add replacements to the dictionary
def add_replacements(dictionary_file_path):
    dictionary = load_dictionary(dictionary_file_path)
    for char, details in dictionary['unwanted_characters'].items():
        if details['replacement'] == "":
            print(f"Character: {char} - Unicode: {ord(char)}")
            replacement = input(f"Enter the replacement for '{char}' (leave blank to skip): ")
            if replacement:
                details['replacement'] = replacement
                details['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                details['source_of_replacement'] = "Manual Update"
                details['replacement_update_number'] += 1  # Increment this for each replacement update
        else:
            print(f"Character: {char} - Unicode: {ord(char)} - Existing replacement: {details['replacement']}")
            input("Press Enter to replace with the existing replacement or type a new replacement: ")
            # If the user enters a new replacement, update the dictionary
            new_replacement = input().strip()
            if new_replacement:
                details['replacement'] = new_replacement
                details['date_added'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                details['source_of_replacement'] = "Manual Update"
                details['replacement_update_number'] += 1  # Increment this for each replacement update

    write_dictionary(dictionary, dictionary_file_path)

def extract_context(text, char, window=4):
    index = text.find(char)
    if index == -1:
        return "Character not found in text"

    # Extract words around the character
    words = text.split()
    for i, word in enumerate(words):
        if char in word:
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            return ' '.join(words[start:end])
    return "Context not found"


if __name__ == "__main__":
    action = input("Choose action - 2: Add Unwanted Characters, 3: Add Replacements: ")
    dictionary_file_path = Path(r'C:\Users\HP\Desktop\final project\question_bank_creation_from_pdf\hia_list_of_undesirable_characters_for_question_bank.py')

    if action == "2":
        input_file_name = input("Enter the name of the text file (without the .txt extension): ")
        input_file_path = Path(r"C:\Users\HP\Desktop\Question Bank Trials\Python Programming\Trials\Regex Trials") / (input_file_name + '.txt')
        add_unwanted_characters(input_file_path, dictionary_file_path)
    elif action == "3":
        add_replacements(dictionary_file_path)
    else:
        print("Invalid action selected.")

