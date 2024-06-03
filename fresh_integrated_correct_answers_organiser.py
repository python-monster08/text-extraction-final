# it extracts the correct answers from the text file created by the pdf reader module
# and creates a dictionary named f"{filename_prefix}correct_answers_dictionary"

import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
import os

# Initially declare modified_answers as an empty dictionary
modified_answers  = {}
answers_1st_dictionary = {}

# Pattern to remove unwanted text like "Page 1: medieval History"
unwanted_text_pattern = r'(?:Page \d+:[^\n]*\n(?!\d)|^\s*edieval History|^\s*Topicwise Solved Papers|^\s*Medieval History |^\s*Gq |^\s*GED |^\s*Ancient History |^\s*GE» |^\s*HINTS & S$)'
question_number = 9999
marks = 4
negative_marks = 1.33
question_number = 1
answer_number = 1
exam_name = "UPSC"
exam_stage = "Pre"
subject_name = "GS_1"
area_name = "HI"


def remove_spaces_between_lines (input_file_path, output_file_path):
    # Read the lines from the input file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # Remove the spaces between the lines
    lines = [line.strip() for line in lines]

    # Write the processed lines to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in lines:
            output_file.write(line + '\n')  # Add a newline character to each line

def clean_html(text):
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text()
    cleaned_text = cleaned_text.replace('\u2014', '')
    cleaned_text = cleaned_text.replace('&amp;', '&')  # Replace HTML entity for ampersand
    cleaned_text = cleaned_text.replace('&lt;', '<')  # Replace HTML entity for less than
    cleaned_text = cleaned_text.replace('&gt;', '>')  # Replace HTML entity for greater than
    cleaned_text = cleaned_text.replace('&quot;', '"')  # Replace HTML entity for double quotes
    cleaned_text = cleaned_text.replace('&#39;', '\'')  # Replace HTML entity for single quote
    cleaned_text = cleaned_text.replace('&nbsp;', ' ')  # Replace HTML entity for non-breaking space
    cleaned_text = cleaned_text.replace('@d);', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('Il.', '1. ')  # Replace erroneous reading of 1 entity
    cleaned_text = cleaned_text.replace('land2', '1. and 2.')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('@d)', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(@) _)', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('@)', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('()', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(ce)', '(c) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(dd)', '(d) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(@ (i)', '(d) (i) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(() (a))', '(d) (i) ')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('((11) C)', '(ii) C')  # Replace erroneous reading of 1 and 2 entity
    cleaned_text = cleaned_text.replace('(dG))', '(d) ')  # Replace erroneous reading of 1 and 2 entity


    return cleaned_text
def clean_file(input_file_path, output_file_path):
    # Read the content of the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Clean the content
    cleaned_content = clean_html(content)

    # Write the cleaned content to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)


# def process_answers_from_file(file_path, exam_name, exam_stage, subject_name, area_name):
def process_answers_from_file(file_path, exam_name, exam_stage, subject_name, area_name, filename_prefix, subfolder):
    exam_name = exam_name.lower()
    correct_answers_dict_dynamic_name = f"{filename_prefix}correct_answers_dictionary"
    answers_source_file_hyperlink = f"{filename_prefix}slim.txt"
    print(f"answers_source_file_hyperlink is: {answers_source_file_hyperlink}")
    input(f"The answers_source_file_hyperlink is: {answers_source_file_hyperlink}, Press Enter to continue......")

    all_correct_answers = {}  # Correctly initialize all_extracted_questions here
    # the following line is crucial
    # all_correct_answers[
    #   correct_answers_dict_dynamic_name] = {}  # Initialize an empty dict for this particular exam's correct answers

    # before using a string for  directory/ folder/ file path, you should convert it to a Path object first
    subfolder = Path(subfolder)
    dict_file_path = Path(subfolder) / f"{correct_answers_dict_dynamic_name}.py"


    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        # Updated regex to capture the question number, answer choice, and the answer description
        pattern = r'(\d+)\.\s*\(([a-d])\)\s*([\s\S]*?)(?=\n\d+\.\s*\(|\Z)'
        answers_raw = re.findall(pattern, text, flags=re.DOTALL)

        # print(f"The raw answers are {answers_raw}")

    for answer_id, (question_number, correct_answer_choice, answer_text) in enumerate(answers_raw, start=1):
        # answer_cleaned = re.sub(unwanted_text_pattern, '', answer_text)
        # Since the question number and answer choice are already separated, no need for re.split here
        correct_answer_description = ' '.join(answer_text.split())  # Clean up whitespace within the description

        # ensuring question_number to be an integer or 'AAA'
        question_number_str = str(question_number)
        if question_number_str.isdigit():
            question_number = int(question_number_str)
        else:
            question_number = 'AAA'

        # print(f"Answer ID: {answer_id}")
        # print(f"Question Number: {question_number}")
        # print(f"Answer Choice: {answer_choice}")
        # print(f"Answer Description: {answer_description}\n")

        # For answers
        all_correct_answers[answer_id] = {
            "answer_id": answer_id,
            "question_number": question_number,
            "correct_answer_choice": correct_answer_choice,
            "correct_answer_description": correct_answer_description,
            "answers_source_file_hyperlink": answers_source_file_hyperlink if answers_source_file_hyperlink else ''
        }

        # Ask the user to proceed further after the first 5 answers
        if answer_id == 5:
            # user_input = input("Are you satisfied with the above 5 extractions? (y/n) ")
            user_input = 'y'
            if user_input.lower() == 'y':
                print("Continuing processing...")
            else:
                print("Not proceeding further.")
                break  # Exit the loop and stop processing further answers.

    # Writing the questions_extraction_completed_dictionary to a Python file
    # Saving the dictionaries to Python files

    # Define your folder path here
    folder_path = Path(subfolder)

    # Ensure the directory exists
    folder_path.mkdir(parents=True, exist_ok=True)
    dict_file_path = folder_path / f"{correct_answers_dict_dynamic_name}.py"

    # Commenting out the statements for static system
    # with open(folder_path / 'modified_answers.py', 'w', encoding='utf-8') as f:
    #    f.write('modified_answers = ' + repr(modified_answers))

    # Write the dictionary to a Python file
    with open(dict_file_path, 'w', encoding='utf-8', errors='ignore') as file:
        dict_content = repr(all_correct_answers)
        file.write(f'{correct_answers_dict_dynamic_name} = {dict_content}\n')

    print(f"The file '{dict_file_path.name}' has been created in {folder_path}")

    return all_correct_answers


def main(text_file_path, text_files_folder, filename_prefix):

    module_name = os.path.splitext(os.path.basename(__file__))[0]
    print(f"Now you are in {module_name}")
    input(f"Press Enter to continue in {module_name} ")

    text_file_path = Path(text_file_path)
    if not text_file_path.is_file():
        print(f"Error: The text file {text_file_path} does not exist or is not a file.")
        return
    all_files_directory = Path(text_files_folder)
    if not all_files_directory.is_dir():
        print(f"Error: The directory {all_files_directory} does not exist or is not a directory.")
        return

    # Now it's safe to use '/' to concatenate paths
    temp_combined_path = all_files_directory / f"{filename_prefix}temp_combined.txt"

    file_name = f"{filename_prefix}temp.txt"
    cleaned_path = all_files_directory / f"{filename_prefix}cleaned.txt"
    slim_path = all_files_directory / f"{filename_prefix}slim.txt"

    print(f"{all_files_directory} is text_files_directory")
    # user_input = input("Should I proceed (y/n) ")
    # input_to_process_fiao = input("Continue to extract correct answers (y/n): ").strip().lower()
    input_to_process_fiao = 'y'
    if input_to_process_fiao == 'y':
        # Combine all text files into a single temporary file
        # Read the file content
        with open(text_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file_text = file.read()

        # Modify the file content
        file_text = re.sub(unwanted_text_pattern, '', file_text, flags=re.MULTILINE)

        # Write the modified content back to the file
        with open(text_file_path, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(f"{file_text}\n")
    else:
        print("Not proceeding further.")
        exit()

    # Inform the user that the unwanted_text_pattern has been removed and ask for input to proceed
    print(f"unwanted_text_pattern removed from f'{file_name}', Please check the file.")
    # user_input = input("Should I proceed with processing the cleaned file? (y/n) ")
    print("Press Enter to proceed with processing the cleaned file...........")
    user_input = 'y'
    if user_input.lower() == 'y':
        # ser_input = input("Should I proceed with removing formatting errors? (y/n) ")
        print("Press Enter to proceed with removing formatting errors.....")
        # Call the clean function
        clean_file(text_file_path, cleaned_path)
        print(f"The cleaned file is saved at: {cleaned_path}")
        # user_input = input("Should I proceed with removing excess space between lines? (y/n) ")
        user_input = 'y'
        if user_input.lower() == 'y':
            remove_spaces_between_lines(cleaned_path, slim_path)
            # user_input = input("Should I proceed with extracting answers? (y/n) ")
            print("Press Enter to proceed with extracting answers.....")
            user_input = 'y'
            if user_input.lower() == 'y':
                process_answers_from_file(slim_path, exam_name, exam_stage, subject_name, area_name, filename_prefix, subfolder)
            else:
                print("Not proceeding further.")
                exit()
        else:
            print("Not proceeding further.")
            exit()
    else:
        print("Not proceeding further.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract correct answers.")
    parser.add_argument("text_file_path", type=str, help="The path to the text file to process.")
    parser.add_argument("area_name", type=str, help="Area name for the content.")
    parser.add_argument("part_name", type=str, help="Part name for the content.")
    parser.add_argument("process_type", type=str, help="Process type: questions or answers.")
    parser.add_argument("filename_prefix", type=str, help="Prefix for the filenames.")
    parser.add_argument("subfolder", type=str, help="Folder to write the processed file to.")
    # parser.add_argument("questions_extraction_target", type=int, help="Targeted number of questions to be extracted")

    args = parser.parse_args()
    text_file_path = Path(args.text_file_path)
    subfolder = args.subfolder
    filename_prefix = args.filename_prefix
    # questions_extraction_target = args.questions_extraction_target


    main(text_file_path, subfolder, filename_prefix)





