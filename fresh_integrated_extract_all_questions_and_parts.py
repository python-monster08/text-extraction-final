# this module extracts all the questions from the input text file by first cleaning it,
# then extract first round of questions
# then refine it further, extract question_part, answer_part and all the answer_options
# it creates an excel file finally but we need to
# also re-assess the refine function as it seems to have missed out on
# splitting around (a) instead using an identification pattern
# for this, we need to quantify the outputs achieved after refine
# in practical experience, it was found that after finding a high quality regex for question identification,
# actually, the refining method was doing more harm than good so it has been commented out
# this module needs to be followed by the module fresh_identify_all_types.py


from pathlib import Path
import re
import pandas as pd
import importlib.util
import os
from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
from fresh_text_cleaner import clean_and_correct_pre_process_text, replace_undesirable_characters
import glob
from input_validation import validate_yes_no, validate_number

# refined_questions = {}
questions_dict = {}

def clean_file(input_file_path):
    cleaned_file_path = input_file_path.parent / (input_file_path.stem + '_cleaned.txt')
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    cleaned_text = clean_and_correct_pre_process_text(text, input_file_path)
    with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
        cleaned_file.write(cleaned_text)
    print(f"Cleaned text file '{cleaned_file_path.name}' created in '{cleaned_file_path.parent}'. Press Enter to continue with removing undesirable characters.")
    input()
    return cleaned_file_path


# required to create excel later for the dictionary
def transform_dict(nested_dict):
    flat_list = []
    for key, value_dict in nested_dict.items():
        # Ensure that each dictionary has all the keys to avoid missing columns
        flat_dict = {**value_dict}  # Create a shallow copy to flatten the structure
        flat_list.append(flat_dict)
    return flat_list


def create_excel_from_dict_new(data_dict, output_dir, excel_file_name):
    # Convert dictionary to DataFrame
    # df = pd.DataFrame(data_dict.values())
    # Convert dictionary to DataFrame; ensure 'question_id' is included by using items() and constructing a DataFrame directly
    df = pd.DataFrame([{'question_id': k, **v} for k, v in data_dict.items()])

    # Specify the file path to match the dictionary name
    # file_path = output_dir / f"{filename_prefix}.xlsx"
    # to also handle Hindi data
    file_path = output_dir / f"{excel_file_name}.xlsx"

    # Inform the user about the Excel file creation details before creating it
    print(f"Excel file will be created with the name '{excel_file_name}.xlsx' in the directory '{output_dir}'.")
    # input(f"Press Enter to Continue to create the Excel file for dictionary with Excel file name: {excel_file_name}")

    # Write DataFrame to Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Confirm the creation of the file
    print(f"Excel file has been created and saved in '{file_path}'.")


def write_dictionary(data_dict, file_path, dict_name):
    with open(file_path, 'w', encoding='utf-8') as file:
        # Write the dictionary with a specific name that matches the expected attribute
        file.write(f'{dict_name} = ' + repr(data_dict))
    print(f"Dictionary has been written to {file_path}")


def load_replacement_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dictionary = eval(file.read())
    return dictionary

def extract_question_number(questions):
    question_numbers_first_round = []
    for question in questions:
        # Extract the number from the start of the question
        match = re.match(r"^(\d+)\.", question)
        if match:
            # If a number is found, append it to the list of question numbers
            question_number = int(match.group(1))
            question_numbers_first_round.append(question_number)
        else:
            # If no number is found, append None or some placeholder to indicate a missing number
            question_numbers_first_round.append(None)
    return question_numbers_first_round

def create_excel_for_questions_extraction_performance(data_dict, folder_path, target, round_number):
    # Define the Excel file path

    excel_file_path = folder_path / 'fresh_extract_all_questions_and_parts_extraction_performance.xlsx'

    # Check if the Excel file already exists
    if excel_file_path.exists():
        old_df = pd.read_excel(excel_file_path)

    else:
        # Explicitly define columns to avoid KeyError later
        old_df = pd.DataFrame(columns=["Sl No", "Round Number", "Date and time",
                                       "No of questions extracted successfully", "%age",
                                       "Questions extracted", "Questions not extracted", "Questions beyond target"])

    # print("DataFrame columns after initialization:", old_df.columns)  # Debugging output

    # Existing DataFrame to collect new data during this function execution
    existing_df = pd.DataFrame(columns=old_df.columns)

    new_rows = []  # List to store all new rows

    # Prepare variables for data aggregation
    questions_extracted = set()
    all_question_numbers = set()

    # Process each question to categorize them
    for question_id, entry in data_dict.items():
        question_number = entry.get("question_number")
        if question_number:
            all_question_numbers.add(question_number)
            if question_number <= target:
                questions_extracted.add(question_number)

    # Questions that were not extracted but should have been
    questions_not_extracted = set(range(1, target + 1)) - questions_extracted
    # Questions that were extracted but are beyond the target
    questions_extracted_beyond_requirement = all_question_numbers - set(range(1, target + 1))

    # Calculate the performance based on extracted fields
    num_questions_extracted = len(questions_extracted)
    total_questions = target
    performance_percentage = (num_questions_extracted / total_questions) * 100 if total_questions > 0 else 0

    new_row = {
        # "Sl No": len(existing_df) + 1,
        "Sl No": len(old_df) + 1,
        "Round Number": round_number,
        "Date and time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "No of questions extracted successfully": num_questions_extracted,
        "%age": performance_percentage,
        "Questions extracted": ', '.join(map(str, sorted(questions_extracted))),
        "Questions not extracted": ', '.join(map(str, sorted(questions_not_extracted))),
        "Questions beyond target": ', '.join(map(str, sorted(questions_extracted_beyond_requirement)))
    }

    # Append the new row to the old DataFrame
    new_row_df = pd.DataFrame([new_row])
    # final_df = pd.concat([old_df, new_row_df], ignore_index=True)
    # to ensure that the new rows (new_row_df) are placed at the beginning of the final_df DataFrame,
    # followed by the existing rows (old_df).
    final_df = pd.concat([new_row_df, old_df], ignore_index=True)

    # print("Final DataFrame before writing to Excel:", final_df)  # Debugging output

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, sheet_name='Assess', index=False)

    print(f"The Excel file has been updated/created at {excel_file_path}")


def extract_all_questions(text, output_dir, base_filename, target):

    # pattern_for_all_questions = r'(\d+\.\s+(?:.* ?(?:\n\s *)?) * ?(?=\(d\)[ ^ a - d] * \n *\d +\.\s |\Z))'
    # pattern_for_all_questions = r'(\d+\.\s+(?:.*?(?:\n\s*)?)*?(?=\(d\)(?:(?!\([abcd]\)).)*\n*\d+\.\s|\Z))'
    pattern_for_all_questions = r'(\d+\.\s+[\s\S]+?(?=\s*\(\w\)\s+[\s\S]*?){3,4}\s*\(\w\)\s+[\s\S]*?(?=\d+\.\s+|\Z))'

    questions = re.findall(pattern_for_all_questions, text)

    if not questions:
        print("No questions extracted. Please check the file content and format.")
        return {}, []

    print(f"Number of questions found initially: {len(questions)}")  # Initial count right after findall

    # After extracting questions
    question_numbers_first_round = extract_question_number(questions)
    # Uncommenting as initialised already at the beginning of the script
    # questions_dict = {}
    output_file_path = output_dir / (base_filename + '_extracted_questions.txt')

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i, question in enumerate(questions, start=1):
            question_num = question_numbers_first_round[i - 1]
            if question_num is not None:
                questions_dict[question_num] = {
                    'question_id': question_num,
                    'question_number': question_num,
                    'question': question.strip(),
                    # 'questions_source_file_hyperlink': str(output_file_path)
                }
                file.write(f"Question {question_num}:\n{question.strip()}\n\n---\n\n")

    print(f"Questions have been written to {output_file_path}")

    # Write dictionary to a .py file
    dict_file_path = output_dir / (base_filename + '_first_round_dict.py')
    dict_name = base_filename + '_first_round_dict'  # This should match the filename without '.py'

    write_dictionary(questions_dict, dict_file_path, dict_name)
    # que_extraction_target = int(input("Please enter the number of questions expected to be extracted :"))
    que_extraction_target = target
    # input(f"The number of questions expected to be extracted is : {que_extraction_target}, press Enter to continue......")

    create_excel_from_dict_new(questions_dict, output_dir, dict_name)

    # input(f"Please check for dictionary created, Press Enter to continue.....")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    create_excel_for_questions_extraction_performance(questions_dict, output_dir, que_extraction_target, 1)

    input(f"Please check excel_for_questions_extraction_performance, Press Enter to continue.....")

    # return questions_dict, question_numbers  # Return both the dictionary and the list of question numbers
    return questions_dict, question_numbers_first_round


def write_questions_to_file(questions, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for question in questions:
            file.write(question.strip() + '\n\n---\n\n')
    print(f"Questions have been written to {file_path}")


def extract_answer_options(second_dict, filename_prefix, base_dir_path):
    answer_options_extracted_dict_name = f"{filename_prefix}answer_options_extracted_dictionary"
    answer_options_extracted_dictionary = {}
    total_matches = 0  # Counter for total matches
    current_year = datetime.now().year  # Get the current year
    questions_source_file_hyperlink = f"{filename_prefix}extracted_questions.txt"

    for question_id, question_details in second_dict.items():
        question_text = question_details.get('question', '')
        question_number = question_details.get('question_number', '')
        # questions_source_file_hyperlink = question_details.get('questions_source_file_hyperlink', '')

        # Validate question_number
        if isinstance(question_number, int) and 0 <= question_number <= 10000:
            validated_question_number = question_number
        else:
            validated_question_number = "QQQ"

        # Extract and validate question year
        year_match = re.search(r'\[(\d{4})\s*[-\d]*\]', question_text)
        # using regex suggested by Kamlesh
        # year_match = re.search(r'(\d{4}(?:,\s*\d{4})*\s*-\s*I)', question_text)

        if year_match:
            year = int(year_match.group(1))
            if 1900 <= year <= current_year:
                question_year = year
            else:
                question_year = "YYY"
        else:
            question_year = "YYY"

        # Splitting the question text at point "(a)"
        parts = question_text.split('(a)', 1)
        # commenting out to allow the question_number and year to be removed
        # question_part = parts[0].strip()
        question_part = re.sub(r'^\d+\.\s*', '', parts[0].strip())  # Remove question number
        question_part = re.sub(r'\[\d{4}\s*[-\d]*\]', '', question_part)  # Remove the year part
        answer_part = '(a)' + parts[1].strip() if len(parts) > 1 else ''
        total_matches += 1 if answer_part else 0

        print(f"question_text for the question '{question_number}': '{question_text}'")
        print(f"question_part for the question '{question_number}': '{question_part}'")
        print("---\n")  # Print a separator after each question in the terminal

        # Initializing dictionary to hold answer options
        options = {'a': '', 'b': '', 'c': '', 'd': ''}

        # Using loop method to extract each option
        for option in ['a', 'b', 'c', 'd']:
            option_pattern = r'\(' + option + r'\)\s*(.*?)(?=\([abcd]\)|$)'
            match = re.search(option_pattern, answer_part, flags=re.DOTALL)
            if match:
                options[option] = match.group(1).strip()

        # Updating the dictionary with extracted data with default values if missing
        answer_options_extracted_dictionary[question_id] = {
            "question_id": question_id,
            "question_number": validated_question_number,
            "exam_year": question_year,
            "question": question_details.get('question', ''),
            "question_part": question_part if question_part else '',
            "answer": answer_part if answer_part else '',
            "answer_option_a": options.get('a', ''),
            "answer_option_b": options.get('b', ''),
            "answer_option_c": options.get('c', ''),
            "answer_option_d": options.get('d', ''),
            "answer_part": '',  # Assuming this field is to be manually filled or extracted differently later
            "questions_source_file_hyperlink": questions_source_file_hyperlink if questions_source_file_hyperlink else ''
        }

        # Print all fields for each entry added to the dictionary
        print(
            f"Added to dictionary: question_id: '{question_id}', question_number: '{question_number}', question: '{question_text}', answer: '{answer_part}', answer_option_a: '{options['a']}', answer_option_b: '{options['b']}', answer_option_c: '{options['c']}', answer_option_d: '{options['d']}', questions_source_file_hyperlink: '{questions_source_file_hyperlink}'")

    file_path = base_dir_path / f"{answer_options_extracted_dict_name}.py"

    # Using existing write_dictionary function to save the dictionary
    write_dictionary(answer_options_extracted_dictionary, file_path, answer_options_extracted_dict_name)

    # creating an excel from the dictionary
    # Transform the nested dictionary to a flat list of dictionaries
    flat_data_list = transform_dict(answer_options_extracted_dictionary)
    # Create the Excel file using the flat list
    # excel_file_path = create_excel_from_dict_new(flat_data_list, answer_options_extracted_dict_name, base_dir_path)
    create_excel_from_dict_new(answer_options_extracted_dictionary, base_dir_path, answer_options_extracted_dict_name)

    print(f"Total number of matches found: {total_matches}")  # Print the total number of matches after processing all items
    print(f"The file '{answer_options_extracted_dict_name}.py' has been created in the directory {base_dir_path}")
    return answer_options_extracted_dictionary


def process_input_file(input_file_path, questions_target):
    # Existing code here...
    print("Processing started...")
    # Move all processing code here
    base_dir_path = input_file_path.parent
    base_filename = input_file_path.stem  # Ensure base_filename is properly defined here

    # Dynamic filename prefix for more flexibility
    filename_prefix = f"{base_filename}_"

    # Step 1: Read the original text from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Step 2: Clean the text and write to a new cleaned file
    cleaned_text = clean_and_correct_pre_process_text(original_text, input_file_path)
    cleaned_file_path = input_file_path.parent / (input_file_path.stem + '_cleaned.txt')
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    print(f"Cleaned text file '{cleaned_file_path.name}' created.")

    # Step 3: Replace undesirable characters in the cleaned file and save it as fully cleaned
    fully_cleaned_file_path = replace_undesirable_characters(cleaned_file_path)
    print(f"Fully cleaned text file '{fully_cleaned_file_path.name}' created.")

    # Step 4: Extract questions from the fully cleaned file
    input(f"Press Enter to continue with the extraction of all questions.")
    with open(fully_cleaned_file_path, 'r', encoding='utf-8') as file:
        fully_cleaned_text = file.read()

    # extract_all_questions(fully_cleaned_text, input_file_path.parent, input_file_path.stem)
    questions_dict, question_numbers = extract_all_questions(fully_cleaned_text, input_file_path.parent, input_file_path.stem, questions_target)

    # Step 5: Extract answer options
    # input("Press Enter to continue extracting answer options.")
    answer_options_extracted_dictionary = extract_answer_options(questions_dict, filename_prefix, base_dir_path)

def main():
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    print(f"Now you are in {module_name}")
    # input_to_process_fiat = input("Continue to extract all questions from the text file (y/n): ").strip().lower()
    input("Press Enter to continue to extract all questions from the text file ....... ")
    input_to_process_fiat = 'y'
    parser = argparse.ArgumentParser(description="Extract questions from text files.")
    parser.add_argument("input_file_path", type=str, help="Path to the input text file")
    parser.add_argument("questions_extraction_target", type=int, help="Targeted number of questions to be extracted")
    args = parser.parse_args()

    input_file_path = Path(args.input_file_path)
    questions_extraction_target = args.questions_extraction_target
    if not input_file_path.exists():
        print(f"File not found: {input_file_path}")
        return

    process_input_file(input_file_path, questions_extraction_target)  # Replace the detailed processing code with a function call


if __name__ == "__main__":
    main()
