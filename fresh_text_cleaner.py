import re
from bs4 import BeautifulSoup
import os
from pathlib import Path

import warnings
# Suppress BeautifulSoup's MarkupResemblesLocatorWarning
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
warnings.filterwarnings("ignore")


unwanted_text_pattern = r'(?:^Page \d+:[^\n]*\n|^\s*Page \d+\s*\n|^\s*Unit - A: History of India\s*\n|^\s*Ancient History\s*\n|^\s*edieval History|^\s*Topicwise Solved Papers|^\s*Medieval History |^\s*Gq |^\s*GED |^\s*GE»|\s*\|\s*Unit - A: Histo|\s*\|\s*Unit - A: History)'

def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        dictionary = eval(content.split('=', 1)[1].strip())
    return dictionary

def clean_and_correct_question_text(text):
    # Check for empty strings and return immediately to avoid unnecessary processing
    if text is None:
        return None  # Or return an empty string if that's more appropriate for your use case

    # Use BeautifulSoup to remove HTML tags and entities
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()

    # Encode and decode to remove non-ASCII characters added on 7 Apr 2024
    cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')

    # General replacement for variations of "l." with "1."
    # cleaned_text = re.sub(r'\b[l1]\.\s*', '1. ', cleaned_text)

    return cleaned_text
def clean_and_correct_pre_process_text(text, input_file_path):
    # Rest of the function remains the same

    # Check for empty strings and return immediately to avoid unnecessary processing
    if not text:
        return text

    # Use BeautifulSoup to remove HTML tags and entities
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()

    # Define a list of tuples where each tuple is a (pattern, replacement)
    replacements = [
        ('\u2014', '-'),
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&quot;', '"'),
        ('&#39;', "'"),
        ('&nbsp;', ' '),
        ('@d);', '(d)'),
        ('Il.', '1.'),
        ('land2', '1. and 2.'),
        ('@d)', '(d)'),
        ('(@) _)', '(d)'),
        ('@)', '(d)'),
        ('()', '(d)'),
        ('(ce)', '(c)'),
        ('(dd)', '(d)'),
        ('(@ (i)', '(d) (i)'),
        ('(() (a))', '(d) (i)'),
        ('((11) C)', '(ii) C'),
        ('(dG))', '(d)'),
        ('â€˜', "'"),
        ('â€™', "'"),
        ('â€œ', '"'),
        ('â€', '"'),
        (r'Unit - A: History of India\s*1\s*\n\s*A 2', ''),
        (r'\|\s*', ''),  # Remove '|' followed by optional whitespace
        ('EBD_8342', ''),  # Add this line to remove 'EBD_8342'
        (r'EBD_8342\s*', ''),  # Remove 'EBD_8342' followed by any whitespace including new lines
        (r'Ancient History [A-Z]\d+', ''),  # Remove patterns like Ancient History A3
        (r'\(Cc\)', '(c)'),  # Replace (Cc) with (c)
        ('lndia', 'India'),  # Type 1 correction

        (r'Unit - A: History of India\n1 Ancient History\n\nTopicwise Solved PapersA2', '\n'),
        (r'EBD_8342\n\nAncient History A3\n', '\n'),
        (r'Topicwise Solved PapersA4\n', '\n'),
        (r'EBD_8342\n\nAncient History A5\n', '\n'),
        (r'Topicwise Solved PapersA6\n', '\n'),
        (r'EBD_8342\n\nAncient History A7\n', '\n'),
        (r'Topicwise Solved PapersA8\n', '\n'),
        (r'EBD_8342\n\nAncient History A9\n', '\n'),
        ('Ancient History', ''),  # Remove 'Ancient History'
        ('A 3', ''),  # Remove 'A 3'
        (r'Topicwise Solved PapersA 2', ''),  # Remove 'Topicwise Solved PapersA' followed by a number
        (r'Topicwise Solved PapersA4', ''),  # Remove ''Topicwise Solved PapersA' followed by a number'Topicwise Solved PapersA4'
        (r'Ancient History A5', ''),  # Remove 'Ancient History A5'
        (r'Topicwise Solved PapersA6', ''),  # Remove 'Topicwise Solved PapersA6'
        (r'Ancient History A7', ''),  # Remove 'Ancient History A7'
        (r'Topicwise Solved PapersA8', ''),  # Remove 'Topicwise Solved PapersA8'
        (r'Ancient History A9', ''),  # Remove 'Ancient History A9'
        (r'Ancient History A3', ''),  # Remove 'Ancient History A3'
        (r'Topicwise Solved PapersA4', ''),  # Remove 'Topicwise Solved PapersA4'
        (r'Topicwise Solved Papers', ''),  # Remove 'Topicwise Solved Papers'
        (r'Topicwise Solved PapersA2', ''),  # Remove 'Topicwise Solved PapersA2'
        (r'Ancient History A9\s*', ''),  # Remove 'Ancient History A9' followed by any whitespace including new lines
        (r'EBD_\d+', ''),  # Assuming 'EBD_' followed by any number
        (r'Ancient History [A-Z]\d+', ''),  # Catch 'Ancient History A5', 'Ancient History B3', etc.
        (r'\n+', '\n')  # Normalize newlines in case multiple replacements cause extra line breaks

    ]

    # replacements.append((r'Unit - A: History of India\s*1\s*\n\s*A 2', ''))

    replaced_characters = set()

    # Apply replacements
    for pattern, replacement in replacements:
        if pattern in cleaned_text:
            replaced_characters.add((pattern, replacement))
            print(f"Replacing {pattern} with {replacement}")
            cleaned_text = cleaned_text.replace(pattern, replacement)
            input("Press Enter to continue...")

    # Correction rules for numeric and list patterns
    correction_rules = [
        (r'(\d),(\d)and(\d)', r'\1, \2 and \3'),
        (r'(\d),(\d)', r'\1, \2'),
        (r'(\d),(\d),(\d),(\d)', r'\1, \2, \3, \4'),
        (r'(\d)\s*and(\d)', r'\1 and \2'),  # Separate 'and' from numbers
        (r'(\d)([a-zA-Z])', r'\1 \2'),  # Separate numbers that stick to letters
        (r'([a-zA-Z])(\d)', r'\1 \2'),  # Separate letters that stick to numbers
        (r'land(\d)', r'1 and \1'),  # Replace 'land' with '1 and'
        (r'(\d)and(\d)', r'\1 and \2'),  # Add space between number and 'and'
        (r'(\d);([ABCDabcd])', r'\1; \2'),  # Add a space after the semicolon
    ]

    # Apply each correction rule to the cleaned text
    for pattern, replacement in correction_rules:
        cleaned_text = re.sub(pattern, replacement, cleaned_text)

    # After replacements are done
    if replaced_characters:
        print("The following unwanted characters were replaced:")
        for char, rep in replaced_characters:
            print(f"Character: {char} - Replaced with: {rep}")

        print(
            f"These characters were saved in the file 'unwanted_characters.txt' in the folder '{os.path.dirname(input_file_path)}'")

        with open(os.path.join(os.path.dirname(input_file_path), 'unwanted_characters.txt'), 'a',
                  encoding='utf-8') as f:
            for char, rep in replaced_characters:
                f.write(f"{char} - {rep}\n")

    return cleaned_text

def replace_undesirable_characters(input_file_path):
    dictionary_file_path = Path(r'C:/Users/HP/Desktop/final project/question_bank_creation_from_pdf/hia_list_of_undesirable_characters_for_question_bank.py')
    dictionary = load_dictionary(dictionary_file_path)
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    for char, details in dictionary['unwanted_characters'].items():
        if details['replacement'] != "":
            text = text.replace(char, details['replacement'])

    output_file_path = input_file_path.parent / f"{input_file_path.stem}_fully_cleaned.txt"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

    print(f"Fully cleaned text file '{output_file_path.name}' created in '{output_file_path.parent}'")
    return output_file_path


if __name__ == "__main__":
    folder_path = r"C:\Users\PC\Desktop\Question Bank Trials\Python Programming\Trials\Regex Trials"
    file_name = input("Enter the name of the text file (without the .txt extension): ")
    input_file_path = os.path.join(folder_path, file_name + '.txt')

    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    cleaned_text = clean_and_correct_pre_process_text(original_text)

    print("Cleaned text:", cleaned_text)

    # Save the cleaned text to a new file
    output_file_path = os.path.join(folder_path, f"{file_name}_cleaned.txt")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)
    print(f"Cleaned text saved to {output_file_path}")

