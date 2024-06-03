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

# Add new fields to the dictionary
def add_new_fields(dictionary_file_path):
    dictionary = load_dictionary(dictionary_file_path)
    for char, details in dictionary['unwanted_characters'].items():
        details['character_update_number'] = 0
        details['character_add_source'] = details.get('file_used', 'ChatGPT4')
        details['character_add_date'] = details.get('date_added', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        details['replacement_update_number'] = 0 if char != '¬' else 1  # Set to 1 only for the character "¬"
        details['replacement_add_source'] = details.get('file_used', 'ChatGPT4')
        details['replacement_add_date'] = details.get('date_added', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        del details['file_used']
        del details['date_added']

    write_dictionary(dictionary, dictionary_file_path)

if __name__ == "__main__":
    input("Press Enter to continue to add new fields to the existing dictionary 'hia_list_of_undesirable_characters_for_question_bank.py'...")
    # dictionary_file_path = Path(r'C:\Users\PC\PycharmProjects\question_bank_creation_from_pdf\hia_list_of_undesirable_characters_for_question_bank.py')
    dictionary_file_path = Path('C:/Users/HP/Desktop/Question Bank Trials/hia_list_of_undesirable_characters_for_question_bank.py')

    add_new_fields(dictionary_file_path)
