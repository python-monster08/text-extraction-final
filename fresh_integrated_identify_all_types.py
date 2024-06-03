# this script works without argparse and extracts questions of list types, then simple type
# it works on the r_and_a_type extracted dictionary as input for identifying list type questions
# and then works on list_type extracted dictionary to identify simple_type questions
# the script for accessing/ extracting the various parts for list_ 1 and list_2 questions is in
# the module fresh_extract_list_type_1_and_2_parts_ver_1
# Whereas the fresh_extract_list_type_1_and_2_parts_ver_1 uses a copy of the dictionary to extract
# parts based on regex, the current module as on 17 May, 2024 uses list to identify the various
# types of questions
# the function "create_excel_for_dict(data_dict, output_dir, filename_prefix):" ca be imported into other modules to
# create excel with sequence of headers and values the way they exist in that dictionary

import re
from pathlib import Path
import pandas as pd
import ast  # Import ast module for safer evaluation
import importlib.util
from datetime import datetime  # Include this at the top of your script
from openpyxl import load_workbook
from openpyxl.styles import Font
import os
import argparse

from input_validation import validate_yes_no, validate_number

# Global variables declaration
matched_question_numbers_question_part_list_type = []
matched_question_numbers_answer_part_list_type = []

matched_question_numbers_question_part_simple_type = []
matched_question_numbers_answer_part_simple_type = []

# matched_question_numbers_list_type2 = [] # Declare the use of the global variable
# matched_question_numbers_list_type1 = [] # Declare the use of the global varia
matched_question_numbers_for_list_type_1_and_2 = []

# Regex patterns

"""pattern_for_list_type_question_part = re.compile(
    r'(?=.*\b1\b)(?=.*\b2\b)(?=.*\b3\b)(List[-\s]?I|List[-\s]?II|List[-\s]?1|List[-\s]?2|Codes|following pairs|following statements|pairs|given below)',
    re.IGNORECASE
)"""
"""pattern_for_list_type_question_part = re.compile(
    r'(?:following\s+(?:pairs|statements))?'
    r'(?:(?(1)(?=.*\b[1-3]\b)|))(List[-\s]?I|List[-\s]?II|List[-\s]?1|List[-\s]?2|Codes|given below)',
    re.IGNORECASE
)"""
"""pattern_for_list_type_question_part = re.compile(
   r'(List[-\s]?I|List[-\s]?II|List[-\s]?1|List[-\s]?2|Codes|following pairs|following statements|pairs|given below)',
    re.IGNORECASE
)"""
# pattern_for_list_type_question_part = re.compile(r'^(.*?\b1\.\s+.*?\b2\.\s+.*)$',re.IGNORECASE)
# pattern_for_list_type_question_part = re.compile(r'^([\s\S]*?\b1\.\s+[\s\S]*?\b2\.\s+[\s\S]*)$', re.IGNORECASE) # gave 88% matching
# pattern_for_list_type_question_part = re.compile(r'^([\s\S]*?\b1\.\s{1,2}(?:\([\s\S]*?)?\b2\.\s{1,2}(?:\([\s\S]*?)?[\s\S]*)$', re.IGNORECASE)
# pattern_for_list_type_question_part = re.compile(r'^([\s\S]*?\b(?:1\s{0,2}\.|\(1\s{0,2}\)\s{0,2})[\s\S]*?\b(?:2\s{0,2}\.|\(2\s{0,2}\)\s{0,2})[\s\S]*)$', re.IGNORECASE) # 97.5%
# pattern_for_list_type_question_part = re.compile(    r'^([\s\S]*?\b(?:1\s{0,2}\.|\((?:\s{0,2}1\s{0,2})\))[\s\S]*?\b(?:2\s{0,2}\.|\((?:\s{0,2}2\s{0,2})\))[\s\S]*)$',re.IGNORECASE) #97.5%
# pattern_for_list_type_question_part = re.compile(r'^([\s\S]*?\b(?:1\s{0,2}\.|\(\s*1\s*\))[\s\S]*?\b(?:2\s{0,2}\.|\(\s*2\s*\))[\s\S]*)$', re.IGNORECASE) #97.5%
pattern_for_list_type_question_part = re.compile(r'^.*?(?:1\s{0,2}\.|\(\s*1\s*\)).*?(?:2\s{0,2}\.|\(\s*2\s*\)).*', re.IGNORECASE | re.DOTALL)


# pattern_for_list_type_answer_part = re.compile(r'\b(?:1\s*(?:and|or|,)\s*2(?:\s*,\s*3)?)\b.*?\b(?:and|or|both|none|either|neither|)\b')
# pattern_for_list_type_answer_part = re.compile(r'\b(?:(?:A|B|C|D)\s*-\s*[1-5]\s*;\s*){2,4}(?:A|B|C|D)\s*-\s*[1-5]\b')
# pattern_for_list_type_answer_part = re.compile(
#    r'(\b(?:1\s*(?:and|or|,)\s*2(?:\s*,\s*3)?)\b.*?\b(?:and|or|both|none|either|neither)\b)|'
#    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)'
#)
#pattern_for_list_type_answer_part = re.compile(
#    r'(\b(?:1\s*(?:and|or|,)?\s*2\s*(?:and|or|,)?\s*(?:3)?\s*(?:and|or|,)?\b.*?\b(?:and|or|both|none|either|neither)\b))|'
#    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;?\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)'
#)
"""pattern_for_list_type_answer_part = re.compile(
    r'(\b(?:1\s*(?:and|or|,)?\s*2\s*(?:and|or|,)?\s*(?:3)?\s*(?:and|or|,)?\b.*?\b(?:and|or|both|none|either|neither)\b))|'
    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;?\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)|'
    r'(\b[1-4],\s*[1-4],\s*[1-4],\s*[1-4]\b)'
)"""
pattern_for_list_type_answer_part = re.compile(
    r'(\b[1-5]\s*(?:and|or|,|\s|both|neither|none|either|;)\s*.*?[\s\S]*?\b[1-5]\s*(?:and|or|,|\s|both|neither|none|either|;))|'
    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;?\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)|'
    r'(\b[1-4],\s*[1-4],\s*[1-4],\s*[1-4]\b)'
)

# pattern_for_simple_type_question_part = re.compile(r'^(?!.*?(?:1\s{0,2}\.|\(\s*1\s*\)).*?(?:2\s{0,2}\.|\(\s*2\s*\)).*).+', re.IGNORECASE | re.DOTALL)
pattern_for_simple_type_question_part = re.compile(
    r'^(?!.*?(?:1\s{0,2}\.|\(\s*1\s*\)).*?(?:2\s{0,2}\.|\(\s*2\s*\)).*|.*\breason\b.*\bassertion\b.*|.*\bassertion\b.*\breason\b.*).+',
    re.IGNORECASE | re.DOTALL
)

pattern_for_simple_type_answer_part = re.compile(
    r'^(?!.*(?:'
    r'\b[1-5]\s*(?:and|or|,|\s|both|neither|none|either|;)\s*.*?[\s\S]*?\b[1-5]\s*(?:and|or|,|\s|both|neither|none|either|;)|'
    r'\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;?\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b|'
    r'\b[1-4],\s*[1-4],\s*[1-4],\s*[1-4]\b'
    r')).+',
    re.IGNORECASE | re.DOTALL
)

"""pattern_for_list_type_2 = re.compile(
    r'^.*?(List\s{0,2}(?:I|1)).*?(List\s{0,2}(?:II|2)).*',
    re.IGNORECASE | re.DOTALL
)"""

# pattern_for_list_type_2 = re.compile(r'^.*?(List\s{0,2}(?:I|1)).*?(List\s{0,2}(?:II|2)).*', re.IGNORECASE | re.DOTALL)
"""pattern_for_list_type_2 = re.compile(
    r'^.*?(List\s{0,2}(?:I|1)).*?(List\s{0,2}(?:II|2)).*',
    re.IGNORECASE | re.DOTALL
)"""

"""pattern_for_list_type_2 = re.compile(
    r'^.*?List\s{0,2}(?:I|1)\b.*?List\s{0,2}(?:II|2)\b.*',
    re.IGNORECASE | re.DOTALL
)"""

"""pattern_for_list_type_2 = re.compile(
    r'^.*?\bList\s{0,2}(I|1)\b.*?\bList\s{0,2}(II|2)\b.*',
    re.IGNORECASE | re.DOTALL
)"""
pattern_for_list_type_2 = re.compile(
    r'^.*?\bList\s*-?\s*(I|1)\b.*?\bList\s*-?\s*(II|2)\b.*',
    re.IGNORECASE | re.DOTALL
)

def load_dictionary(file_name, base_dir_path):
    """ Load a dictionary from a Python file within the specified directory. """

    # Ensure the dictionary name does not include the '.py' extension
    dict_name = file_name if not file_name.endswith('.py') else file_name[:-3]

    dict_path = base_dir_path / f"{file_name}.py"
    if not dict_path.exists():
        print(f"File {dict_path} not found.")
        return {}  # Return an empty dictionary instead of None

    spec = importlib.util.spec_from_file_location(file_name, dict_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Ensure the dictionary name does not include the '.py' extension
    dict_name = file_name if not file_name.endswith('.py') else file_name[:-3]

    # Attempt to get the dictionary
    loaded_dict = getattr(module, dict_name, {})

    # Check if the dictionary is empty and print a message
    if not loaded_dict:
        print(f"Loaded dictionary named '{dict_name}' is empty.")
    else:
        print(f"Loaded dictionary named '{dict_name}' successfully.")

    return loaded_dict

def write_dictionary(data_dict, file_path, dict_name):
    # Construct the full path using base_dir_path
    full_path = Path(file_path)  # Assuming file_path is already the full path including the filename

    # Ensure the directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'{dict_name} = ' + repr(data_dict))
    print(f"Dictionary has been written to {file_path}")

def create_text_from_dictionary(loaded_dictionary, dictionary_name, output_folder_path):
    """
    Create text files from the input dictionary for question and answer parts.
    """
    output_text_file_name_question_part = f"{dictionary_name}_text_created_question_part.txt"
    output_text_file_name_answer_part = f"{dictionary_name}_text_created_answer_part.txt"
    output_text_file_path_question_part = output_folder_path / output_text_file_name_question_part
    output_text_file_path_answer_part = output_folder_path / output_text_file_name_answer_part

    # Create the text file for question parts from the dictionary
    with open(output_text_file_path_question_part, 'w', encoding='utf-8') as file_question_part:
        for question_id, question_info in loaded_dictionary.items():
            file_question_part.write(f"Question ID: {question_id}\n")
            file_question_part.write(f"Question Number: {question_info['question_number']}\n")
            file_question_part.write(f"Content: {question_info['question_part']}\n---\n\n")

    # Create the text file for answer parts from the dictionary
    with open(output_text_file_path_answer_part, 'w', encoding='utf-8') as file_answer_part:
        for question_id, question_info in loaded_dictionary.items():
            file_answer_part.write(f"Question ID: {question_id}\n")
            file_answer_part.write(f"Question Number: {question_info['question_number']}\n")
            file_answer_part.write(f"Content: {question_info['answer_part']}\n")
            file_answer_part.write(f"a) {question_info.get('answer_option_a', 'Not available')}\n")
            file_answer_part.write(f"b) {question_info.get('answer_option_b', 'Not available')}\n")
            file_answer_part.write(f"c) {question_info.get('answer_option_c', 'Not available')}\n")
            file_answer_part.write(f"d) {question_info.get('answer_option_d', 'Not available')}\n---\n\n")

    print(f"Text files created: {output_text_file_path_question_part} and {output_text_file_path_answer_part}")

    return output_text_file_name_question_part, output_text_file_name_answer_part

def create_excel_for_dict(data_dict, output_dir, filename_prefix):
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data_dict.values())

    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Specify the file path to match the dictionary name
    file_path = output_dir / f"{filename_prefix}.xlsx"

    # Inform the user about the Excel file creation details before creating it
    print(f"Excel file will be created with the name '{filename_prefix}.xlsx' in the directory '{output_dir}'.")
    # input("Press Enter to Continue to create the Excel file.")

    # Write DataFrame to Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Confirm the creation of the file
    print(f"Excel file has been created and saved in '{file_path}'.")

# this function create_performance_excel is for displaying identification performance for
# all stages starting from r_and_a_type, then list_type, then simple_type, then
# list_type_1/2 type, it ensures that the new data is written in rows dded before the existing rows
def create_performance_excel(question_dict, answer_dict, base_dir_path, original_dict_name, question_type_identification, targets):
    # input("Now you are in the function create_performance_excel, Press Enter to continue.....................")
    file_name_suffix = "_questions_identification_performance"
    target = targets[question_type_identification]
    """try:
        target = float(input(f"Please enter the target number for {question_type_identification} identification calculation: "))
        if target == 0:
            print("Target cannot be zero. Please enter a valid number.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return"""

    """if question_type_identification == "list_1_and_2_type":
        try:
            target_2 = float(input("Please enter the target number for list_2_type identification calculation: "))
            if target_2 == 0:
                print("Target cannot be zero. Please enter a valid number.")
                return
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return
    else:
        target_2 = target  # Set target_2 equal to target if not list_1_and_2_type"""

    if question_type_identification == "list_1_and_2_type":
        target_2 = targets["target_2"]
    else:
        target_2 = target
    # Extract base file name for new Excel file
    parts = original_dict_name.split('_')
    # new_file_name = '_'.join(parts[:-7]) + "_list_type_identification_performance"
    new_file_name = '_'.join(parts[:-1]) + file_name_suffix
    # new_file_name = original_dict_name
    excel_file_path = base_dir_path / f"{new_file_name}.xlsx"

    # Check if the file exists and load existing data if it does
    if excel_file_path.exists():
        existing_df = pd.read_excel(excel_file_path)
    else:
        existing_df = pd.DataFrame(columns=[
            'sl_num', 'set_in_que', 'numbers_in_que', 'target_1', '% extraction for list type (Questions)',
            'set_in_ans', 'numbers_in_ans', 'target_2', '% extraction for list type (Answers)'
        ])

    # Prepare data for DataFrame
    # Prepare new data for DataFrame
    # if question_dict and answer_dict:  # Check that both dictionaries are not empty
    # attempting to handle list_1_and_2_type also in function create_performance_excel
    # Check if question_dict is not empty and answer_dict is either not empty or question_type_identification is "list_1_and_2_type"
    # if question_dict and (answer_dict or question_type_identification == "list_1_and_2_type"):
    # Check if question_dict is not empty and answer_dict is either not empty or question_type_identification is "list_1_and_2_type"
    # or question_type_identification == "r_and_a_type"
    if question_dict and (answer_dict or question_type_identification in ["list_1_and_2_type", "r_and_a_type"]):

        """new_data = {
            'sl_num': range(len(existing_df) + 1, len(existing_df) + max(len(question_dict), len(answer_dict)) + 1),
            'question_id_in_que': [info['question_id'] for info in question_dict.values()],
            'question_number_in_que': [info['question_number'] for info in question_dict.values()],
            # 'set_in_que': [', '.join(question_dict.keys())] * max(len(question_dict), len(answer_dict)),
            'set_in_que': [', '.join(map(str, question_dict.keys()))] * max(len(question_dict), len(answer_dict)),
            'question_id_in_ans': [info['question_id'] for info in answer_dict.values()],
            'question_number_in_ans': [info['question_number'] for info in answer_dict.values()],
            # 'set_in_ans': [', '.join(answer_dict.keys())] * max(len(question_dict), len(answer_dict)),
            'set_in_ans': [', '.join(map(str, answer_dict.keys()))] * max(len(question_dict), len(answer_dict)),
            '% extraction for list type (Questions)': [len(question_dict.keys()) / target * 100] * max(
                len(question_dict), len(answer_dict)),
            '% extraction for list type (Answers)': [len(answer_dict.keys()) / target * 100] * max(len(question_dict),
                                                                                                   len(answer_dict))
        }"""

        # Fill in gaps if one dictionary is larger than the other
        """for key in ['question_id_in_que', 'question_number_in_que', 'question_id_in_ans', 'question_number_in_ans']:
            while len(new_data[key]) < max(len(question_dict), len(answer_dict)):
                new_data[key].append(None)"""

        numbers_in_que = len(question_dict.keys())
        numbers_in_ans = len(answer_dict.keys()) if answer_dict else 0

        new_data = {
            'sl_num': [1],
            'set_in_que': [', '.join(map(str, question_dict.keys()))],
            'numbers_in_que': [numbers_in_que],
            'target_1': [target],
            '% extraction for list type (Questions)': [len(question_dict.keys()) / target * 100],
            # attempting to handle list_1_and_2_type also in function create_performance_excel where answer_dict is empty
            # 'set_in_ans': ['' if question_type_identification == "list_1_and_2_type" else ', '.join(map(str, answer_dict.keys()))],
            # 'set_in_ans': [', '.join(map(str, answer_dict.keys()))],
            'set_in_ans': [', '.join(map(str, answer_dict.keys()))] if answer_dict else [''],
            'numbers_in_ans': [numbers_in_ans],
            'target_2': [target_2],
            '% extraction for list type (Answers)': [len(answer_dict.keys()) / target * 100]
            # attempting to handle list_1_and_2_type also in function create_performance_excel where answer_dict is empty resulting in
            # (answer_dict.keys()) = 0
            # '% extraction for list type (Answers)': [0 if question_type_identification == "list_1_and_2_type" else len(answer_dict.keys()) / target * 100]
        }

        # Create new DataFrame for the extracted data
        new_df = pd.DataFrame(new_data)

        # Add a row for the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        performance_summary = pd.DataFrame(
            {'sl_num': [f"Extraction Performance for {question_type_identification} at " + current_time]})

        # Append new data to existing DataFrame
        # final_df = pd.concat([existing_df, new_df], ignore_index=True)
        # final_df = pd.concat([final_df, performance_summary], ignore_index=True)

        # Concatenate new data and performance summary
        # final_df = pd.concat([new_df, performance_summary], ignore_index=True)
        # Insert performance summary at the beginning
        # sequence used is to ensure that the new data is written in rows added before the existing rows
        final_df = pd.concat([performance_summary, new_df, existing_df], ignore_index=True)

        # Write the combined DataFrame to Excel
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False)

        print(f"The {new_file_name}.xlsx has been updated/created in the {base_dir_path} folder.")

    else:
        print("One or both dictionaries are empty, no Excel file created.")

# this function create_performance_excel_2 is to use for stages starting from list 1 and list 2 type identification
def create_performance_excel_2(question_dict, base_dir_path, original_dict_name, file_name_suffix, question_type_identification):

    global matched_question_numbers_for_list_type_1_and_2 # Declare as global
    # Split the original_dict_name by hyphens and remove the last 10 parts
    parts = original_dict_name.split('_')
    shortened_name = '_'.join(parts[:-10]) if len(parts) > 10 else original_dict_name
    excel_file_path = os.path.join(base_dir_path, f"{shortened_name}{file_name_suffix}.xlsx")
    # debug print statement
    print("Matched question numbers in the create excel function:", matched_question_numbers_for_list_type_1_and_2)  # Print the matched question numbers here

    # Check if the file exists and load existing data if it does
    if os.path.exists(excel_file_path):
        existing_df = pd.read_excel(excel_file_path)
    else:
        existing_df = pd.DataFrame()

    # Ask user for target number
    try:
        target = float(input(f"Please enter the target number for {question_type_identification} extraction calculation: "))
        if target == 0:
            print("Target cannot be zero. Please enter a valid number.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return

    # Calculate performance
    extraction_performance_questions = len(matched_question_numbers_for_list_type_1_and_2) / target * 100 if target > 0 else 0
    extraction_performance_answers = 0  # Assuming no answer matching is performed in this context

    # Assume you have a dictionary 'matched_dict' with the matched entries
    # matched_dict = load_dictionary(original_dict_name, base_dir_path)  # Load your matched results

    # if matched_dict:
        # Calculation for the extraction performance
        # extraction_performance_questions = (len(matched_dict) / target) * 100
        # extraction_performance_answers = 0  # Assuming no answer matching is performed in this context

    # Prepare new data for DataFrame
    if question_dict: # Check that both dictionaries are not empty
        new_data = {
            'sl_num': list(range(1, len(matched_question_numbers_for_list_type_1_and_2) + 1)),
            'question_id_in_que': " ",  # Assuming no question IDs available
            'question_number_in_que': matched_question_numbers_for_list_type_1_and_2,
            'set_in_que': [', '.join(map(str, matched_question_numbers_for_list_type_1_and_2))] * len(matched_question_numbers_for_list_type_1_and_2),
            'question_id_in_ans': " ",  # Empty since no answer processing
            'question_number_in_ans': " ",  # Empty since no answer processing
            'set_in_ans': " ",  # Empty since no answer processing
            '% extraction for list type (Questions)': extraction_performance_questions,
            '% extraction for list type (Answers)': 0  # No answers processed
        }

        # not required due to the new manner in which new_data is designed
        # Fill in gaps if one dictionary is larger than the other
        # new_data['set_in_que'] *= len(new_data['sl_num'])

        # Create DataFrame from the new data
        new_df = pd.DataFrame(new_data)
        final_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Add a row for the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        performance_summary = pd.DataFrame({'sl_num': [f"Extraction Performance for {question_type_identification} at " + current_time]})
        final_df = pd.concat([final_df, performance_summary], ignore_index=True)

        # Writing to Excel, ensuring no index is written
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False)

        print(f"The {shortened_name}{file_name_suffix}.xlsx has been updated/created in the {base_dir_path} folder.")

# this function identify_r_and_a_type for only uses the question_part to identify the r_and_a_type questions
def identify_r_and_a_type(targets, module_input_dict_name, input_dictionary, dict_name, base_dir_path):
    """Identify Reason and Assertion type questions."""
    # creating new dictionaries only_matched_dict only for the sake of running create_performance_excel
    only_matched_r_and_a_type_dict = {}
    # Generate the output dictionary name by removing the last two parts and adding '_r_and_a_extracted_dictionary'
    new_dict_name = '_'.join(dict_name.split('_')[:-2]) + "_r_and_a_identified_dictionary"
    output_dictionary = {key: {**val, 'question_type': ''} for key, val in input_dictionary.items()}
    r_and_a_questions_list = []  # Initialize the list to store matching questions

    # Regex pattern to find Reason and Assertion type questions
    # pattern_for_r_and_a_type = re.compile(r'\d+\.\s+Assertion\s*\([A]\):.*?Reason\s*\([R]\):.*?(?=\d+\.|$)', re.DOTALL)
    pattern_for_r_and_a_type = re.compile(r'Assertion\s*\([A]\):.*?Reason\s*\([R]\):.*?(?=\Z)', re.DOTALL)

    # Iterate through dictionary items
    for key, question_info in input_dictionary.items():
        question_text = question_info['question_part']  # Only check the question part
        matches = pattern_for_r_and_a_type.findall(question_text)

        if matches:
            output_dictionary[key]['question_type'] = 'r_and_a_type'  # Update question type for matches
            for match in matches:
                r_and_a_questions_list.append(match)  # Add to list for output and counting
                question_id = question_info['question_id']
                only_matched_r_and_a_type_dict[question_id] = question_info['question_number']
            #    output_dictionary[key] = question_info.copy()  # Copy the whole entry if it's a match

    # Print the number and details of matched questions
    print(f"Found {len(r_and_a_questions_list)} 'Reason and Assertion' type questions:")
    for question in r_and_a_questions_list:
        print(question)

    # Writing matched questions to a text file
    text_file_path = base_dir_path / f"{new_dict_name}_text.txt"
    with open(text_file_path, 'w', encoding='utf-8') as file:
        for question in r_and_a_questions_list:
            file.write(question + '\n\n')
    print(f"Text file created: {text_file_path}")


    # Inform user and ask to continue before writing the dictionary
    print(f"Dictionary for 'r_and_a_type' will be created with the name '{new_dict_name}.py' in the directory '{base_dir_path}'.")
    # input("Press Enter to continue...")

    # Writing matched questions to the dictionary
    # Write dictionary and inform user
    dict_file_path = base_dir_path / f"{new_dict_name}.py"
    write_dictionary(output_dictionary, dict_file_path, new_dict_name)
    # print(f"Dictionary has been written to {dict_file_path}")

    # Commenting out as the provisions to inform user etc are already included in the function create_excel_for_dict
    # Inform user and ask to continue before creating the Excel file
    # print(f"Excel file for 'r_and_a_type' will be created with the name '{new_dict_name}.xlsx' in the directory '{base_dir_path}'.")
    # input("Press Enter to continue...")
    create_excel_for_dict(output_dictionary, base_dir_path, new_dict_name)
    question_type_for_identification = "r_and_a_type"
    # creating a blank dictionary only for the sake of running create_performance_excel
    answer_dict_for_r_and_a_type = {}
    create_performance_excel(only_matched_r_and_a_type_dict, answer_dict_for_r_and_a_type, base_dir_path, module_input_dict_name,
                             question_type_for_identification, targets)

    return output_dictionary, text_file_path


# this function identify_list_type works on both the question_part and the answer_part to identify the
# list_type questions. firstly, it works on the question_part and then on the answer_part using the
# default mode with file_type being either question_part or answer_part and creates two dictionaries
# and then in the union mode, combines the two dictionaries, with the final dictionary created
# including all questions from the original data_dict with the question_type field updated to 'list_type'
# based on the union of matched question numbers.
def identify_list_type(targets, module_input_dict_name, data_dict, pattern, dict_name, base_dir_path, file_type, operation_mode='default'):
    matched_dict = {}  # This will store all matches with their original data
    match_count = 0
    # for creating the union of question_numbers identified and creating the final output dictionary
    global matched_question_numbers_question_part_list_type  # Declare the use of the global variable
    global matched_question_numbers_answer_part_list_type  # Declare the use of the global variable

    if operation_mode != 'union':  # Only perform matching if not in union mode
        # Iterate through each item in the dictionary to apply the pattern
        for question_id, info in data_dict.items():
            if file_type == "question_part":
                current_text = info['question_part']
            else:
                current_text = "\n".join([info.get(f'answer_option_{chr(97 + i)}', 'Not available') for i in range(4)])

            if pattern.search(current_text):
                match_count += 1
                # Retrieve the question_number from the dictionary entry
                question_number = info.get('question_number', 'Not available')

                print(f"Match found in {file_type} file for Question ID {question_id} and Question Number {question_number}:")
                print(current_text + "\n---\n")
                matched_dict[question_id] = info

                # for creating the union of question_numbers identified and creating the final output dictionary
                if file_type == "question_part":
                    matched_question_numbers_question_part_list_type.append(question_number)
                elif file_type == "answer_part":
                    matched_question_numbers_answer_part_list_type.append(question_number)

        # print(f"Found {match_count} matches in {file_type} file.")

        # Regular operation: Write dictionary and Excel for part files
        # dict_file_name = f"{dict_name}_list_type_questions_{file_type}_dictionary"
        # dict_path = base_dir_path / f"{dict_file_name}.py"
        # excel_path = base_dir_path / f"{dict_file_name}.xlsx"

        # question_part_dict_file_name = f"{dict_name}_list_type_from_question_part.py"
        question_part_dict_file_name = f"{dict_name}_list_type_from_question_part"
        answer_part_dict_file_name = f"{dict_name}_list_type_from_answer_part"

        if file_type == "question_part":
            dict_file_name = question_part_dict_file_name
        else:
            dict_file_name = answer_part_dict_file_name

        dict_path = base_dir_path / f"{dict_file_name}.py"
        excel_path = base_dir_path / f"{dict_file_name}.xlsx"

        # write the basic dictionaries created
        write_dictionary(matched_dict, dict_path, dict_file_name)

        # write the excel files corresponding to the basic dictionaries created
        df = pd.DataFrame.from_dict(matched_dict, orient='index')
        df.to_excel(excel_path, index=False)
        print(f"Dictionary and Excel file created for {file_type} at {dict_path} and {excel_path}")

        # write the text files corresponding to the basic dictionaries created
        # Create additional text files after dictionaries and Excels are done
        # question_text_file_path = base_dir_path / f"{dict_name}_{file_type}_from_question_parts.txt"
        # answer_text_file_path = base_dir_path / f"{dict_name}_{file_type}_from_answer_parts.txt"
        question_text_file_path = base_dir_path / f"{question_part_dict_file_name}.txt"
        answer_text_file_path = base_dir_path / f"{answer_part_dict_file_name}.txt"

        with open(question_text_file_path, 'w', encoding='utf-8') as q_file, \
                open(answer_text_file_path, 'w', encoding='utf-8') as a_file:
            for id, content in matched_dict.items():
                # Write to question parts text file
                q_file.write(f"Question ID: {id}\n")
                q_file.write(f"Question Number: {content['question_number']}\n")
                q_file.write(f"Content: {content['question_part']}\n")
                q_file.write("---\n\n")
                # Write to answer parts text file if applicable
                if 'answer_part' in content:
                    a_file.write(f"Question ID: {id}\n")
                    a_file.write(f"Question Number: {content['question_number']}\n")
                    a_file.write(f"Content: {content['answer_part']}\n")
                    a_file.write("---\n\n")

        print(f"Text files created at {question_text_file_path} and {answer_text_file_path}")

        # create the performance excel
        if file_type == 'answer_part':
            # question_dict_file = f"{dict_name}_list_type_questions_question_part_dictionary"
            # print(f"the dict_file_name is :{question_dict_file}")
            # input("Press Enter to continue...")
            # answer_dict_file = f"{dict_name}_list_type_questions_answer_part_dictionary"
            # print(f"the dict_file_name is :{answer_dict_file}")
            # input("Press Enter to continue...")
            # question_dict = load_dictionary(question_dict_file, base_dir_path)
            # answer_dict = load_dictionary(answer_dict_file, base_dir_path)
            # create_performance_excel(question_dict, answer_dict, base_dir_path, dict_name)
            # create_performance_excel(question_dict, answer_dict, base_dir_path, dict_name, "_list_type_identification_performance")
            print(f"Loading Question Dictionary from {question_part_dict_file_name}")
            question_dict = load_dictionary(question_part_dict_file_name, base_dir_path)
            print(f"Loading Answer Dictionary from {answer_part_dict_file_name}")
            answer_dict = load_dictionary(answer_part_dict_file_name, base_dir_path)
            # input(f"For list_type please check the above and Press Enter to continue to create performance excel....")

            # print(f"Loaded Question Dictionary: {question_dict}")
            # print(f"Loaded Answer Dictionary: {answer_dict}")

            # input(f"For list_type please check the above and Press Enter to continue....")

            if not question_dict or not answer_dict:
                print("One or both dictionaries are empty, cannot proceed to performance excel creation.")
                return

            # create_performance_excel(question_dict, answer_dict, base_dir_path, dict_name, "_simple_type_identification_performance")
            question_type_for_identification = "list_type"
            # input(f"For list_type please check the above and Press Enter to continue to create performance excel....")
            create_performance_excel(question_dict, answer_dict, base_dir_path, module_input_dict_name,
                                     question_type_for_identification, targets)

    elif operation_mode == 'union':
        # Operation to handle after both question_part and answer_part have been processed
        matched_question_numbers_list_type = list(
            set(matched_question_numbers_question_part_list_type) | set(matched_question_numbers_answer_part_list_type))
        print("Union of matched question numbers:", matched_question_numbers_list_type)
        # new_dict_name = '_'.join(dict_name.split('_')[:-2]) + "_list_type_identified_dictionary"
        new_dict_name = dict_name
        # new_dict_name = f"{dict_name}_list_type_extracted_dictionary"
        new_dict_path = base_dir_path / f"{new_dict_name}.py"
        """new_dict = {
            key: {**val, 'question_type': 'list_type' if val['question_number'] in matched_question_numbers_list_type else ''} for
            key, val in data_dict.items()}"""
        # ensuring that all the questions in the input dictionary are processed with question_type of only the identified questions
        # getting marked as 'list_type'
        new_dict = {
            key: {**val,
                  'question_type': 'list_type' if val['question_number'] in matched_question_numbers_list_type and not val.get(
                      'question_type') else val.get('question_type', '')} for key, val in data_dict.items()
        }
        write_dictionary(new_dict, new_dict_path, new_dict_name)
        create_excel_for_dict(new_dict, base_dir_path, new_dict_name)

        return new_dict, new_dict_path  # Ensure you return both the dictionary and a relevant file path or similar

# similar to the function identify_list_type this function identify_simple_type works on both the question_part and
# the answer_part to identify the simple_type questions. firstly, it works on the question_part and then on the answer_part using the
# default mode with file_type being either question_part or answer_part and creates two dictionaries
# and then in the union mode, combines the two dictionaries, with the final dictionary created
# including all questions from the original data_dict with the question_type field updated to 'simple_type' based on the
# union of matched question numbers.

def identify_simple_type(targets, module_input_dict_name, data_dict, pattern, dict_name, base_dir_path, file_type, operation_mode='default'):
    base_dir_path = Path(base_dir_path)  # Ensure base_dir_path is a Path object
    matched_dict = {}  # This will store all matches with their original data
    match_count = 0
    # for creating the union of question_numbers identified and creating the final output dictionary
    global matched_question_numbers_question_part_simple_type  # Declare the use of the global variable
    global matched_question_numbers_answer_part_simple_type  # Declare the use of the global variable

    if operation_mode != 'union':  # Only perform matching if not in union mode
        # Iterate through each item in the dictionary to apply the pattern
        # current_text set to either the question_part or concatenated answer_options.
        for question_id, info in data_dict.items():
            if file_type == "question_part":
                # current_text set to the question_part
                current_text = info['question_part']
            else:
                # current_text set to concatenated answer_options.
                if info.get('question_type') != 'r_and_a_type':
                    current_text = "\n".join(
                        [info.get(f'answer_option_{chr(97 + i)}', 'Not available') for i in range(4)])
                else:
                    continue  # Skip the current iteration if question_type is 'r_and_a_type'

            if pattern.search(current_text):
                match_count += 1
                # Retrieve the question_number from the dictionary entry
                question_number = info.get('question_number', 'Not available')

                print(f"Match found in {file_type} file for Question ID {question_id} and Question Number {question_number}:")
                print(current_text + "\n---\n")
                matched_dict[question_id] = info

                # for creating the union of question_numbers identified and creating the final output dictionary
                if file_type == "question_part":
                    matched_question_numbers_question_part_simple_type.append(question_number)
                elif file_type == "answer_part":
                    matched_question_numbers_answer_part_simple_type.append(question_number)

        print(f"Found {match_count} matches in {file_type} file.")

        # Regular operation: Write dictionary and Excel for part files
        # dict_file_name = f"{dict_name}_simple_type_questions_{file_type}_dictionary"
        # dict_name appears to be
        # disha_26_2020_upsc_pre_gs1_history_ancient_que_answer_options_r_and_a_list_type

        # question_part_dict_file_name = f"{dict_name}_simple_type_from_question_part.py"
        simple_type_question_part_dict_file_name = f"{dict_name}_simple_type_from_question_part"
        simple_type_answer_part_dict_file_name = f"{dict_name}_simple_type_from_answer_part"
        print(f"The answer_part_dict_file_name is: {simple_type_answer_part_dict_file_name}")
        print(f"The question_part_dict_file_name is: {simple_type_question_part_dict_file_name}")
        input("In the function, please check the above names and continue.....")

        if file_type == "question_part":
            dict_file_name = simple_type_question_part_dict_file_name
        else:
            dict_file_name = simple_type_answer_part_dict_file_name

        dict_path = base_dir_path / f"{dict_file_name}.py"
        excel_path = base_dir_path / f"{dict_file_name}.xlsx"
        print(matched_dict)
        print(dict_path)
        print(f"{file_type}")
        input(f"Please check the contents of the matched_dict, file_type and dict_path, Press Enter to continue")
        # need to check whether the following command writes both the dictionaries - answer and question part
        write_dictionary(matched_dict, dict_path, dict_file_name)

        # write the excel files corresponding to the basic dictionaries created
        df = pd.DataFrame.from_dict(matched_dict, orient='index')
        df.to_excel(excel_path, index=False)
        print(f"Dictionary and Excel file created for {file_type} at {dict_path} and {excel_path}")

        question_text_file_path = base_dir_path / f"{simple_type_question_part_dict_file_name}.txt"
        answer_text_file_path = base_dir_path / f"{simple_type_answer_part_dict_file_name}.txt"

        with open(question_text_file_path, 'w', encoding='utf-8') as q_file, \
                open(answer_text_file_path, 'w', encoding='utf-8') as a_file:
            for id, content in matched_dict.items():
                # Write to question parts text file
                q_file.write(f"Question ID: {id}\n")
                q_file.write(f"Question Number: {content['question_number']}\n")
                q_file.write(f"Content: {content['question_part']}\n")
                q_file.write("---\n\n")
                # Write to answer parts text file if applicable
                if 'answer_part' in content:
                    a_file.write(f"Question ID: {id}\n")
                    a_file.write(f"Question Number: {content['question_number']}\n")
                    a_file.write(f"Content: {content['answer_part']}\n")
                    a_file.write("---\n\n")

        print(f"Text files created at {question_text_file_path} and {answer_text_file_path}")
        print(f"For simple_type, question_part_dict_file_name is: {simple_type_question_part_dict_file_name}")

        # create the performance excel
        if file_type == 'answer_part':

            print(f"Loading Question Dictionary from {simple_type_question_part_dict_file_name}")
            question_dict = load_dictionary(simple_type_question_part_dict_file_name, base_dir_path)
            print(f"Loading Answer Dictionary from {simple_type_answer_part_dict_file_name}")
            answer_dict = load_dictionary(simple_type_answer_part_dict_file_name, base_dir_path)

            # print(f"Loaded Question Dictionary: {question_dict}")
            # print(f"Loaded Answer Dictionary: {answer_dict}")

            # input(f"For simple_type please check the above and Press Enter to continue to create performance excel....")

            if not question_dict or not answer_dict:
                print("One or both dictionaries are empty, cannot proceed to performance excel creation.")
                return

            # create_performance_excel(question_dict, answer_dict, base_dir_path, dict_name, "_simple_type_identification_performance")
            question_type_for_identification = "simple_type"
            create_performance_excel(question_dict, answer_dict, base_dir_path, module_input_dict_name, question_type_for_identification, targets)


    elif operation_mode == 'union':
        # Operation to handle after both question_part and answer_part have been processed
        matched_question_numbers_simple_type = list(
            set(matched_question_numbers_question_part_simple_type) | set(matched_question_numbers_answer_part_simple_type))
        print("Union of matched question numbers:", matched_question_numbers_simple_type)
        # new_dict_name = '_'.join(dict_name.split('_')[:-2]) + "_simple_type_extracted_dictionary"
        new_dict_name = dict_name
        # new_dict_name = f"{dict_name}_list_type_extracted_dictionary"
        new_dict_path = base_dir_path / f"{new_dict_name}.py"
        """new_dict = {
            key: {**val, 'question_type': 'list_type' if val['question_number'] in matched_question_numbers else ''} for
            key, val in data_dict.items()}"""
        # ensuring that all the questions in the input dictionary are processed with question_type of only identified questions
        # getting marked as 'simple_type'
        new_dict = {
            key: {**val,
                  'question_type': 'simple_type' if val['question_number'] in matched_question_numbers_simple_type and not val.get(
                      'question_type') else val.get('question_type', '')} for key, val in data_dict.items()
        }
        write_dictionary(new_dict, new_dict_path, new_dict_name)
        create_excel_for_dict(new_dict, base_dir_path, new_dict_name)

        print(f"In the function identify_simple_type, Dictionary and Excel file for Dictionary {new_dict_name} created at {new_dict_path} and {base_dir_path}")

        return new_dict, new_dict_path  # Ensure you return both the dictionary and a relevant file path or similar


def identify_list_type_1_and_2(targets, module_input_dict_name, data_dict, pattern, dict_name, base_dir_path, operation_mode='default'):
    global matched_question_numbers_for_list_type_1_and_2  # Declare as global
    # creating new dictionaries only_matched_dict only for the sake of running create_performance_excel
    only_matched_list_2_dict = {}
    only_matched_list_1_dict = {}
    matched_dict = {}
    match_count = 0
    # matched_question_numbers_for_list_type_1_and_2 = []  # To store matched question numbers

    if operation_mode == 'default':
        for question_id, info in data_dict.items():
            if info.get('question_type') == 'list_type':
                current_text = info['question_part']
                if pattern and pattern.search(current_text):
                    match_count += 1
                    info['question_sub_type'] = 'list_type_2'
                    matched_question_numbers_for_list_type_1_and_2.append(info['question_number'])  # Collect question numbers
                    only_matched_list_2_dict[question_id] = info
                else:
                    info['question_sub_type'] = 'list_type_1'
                    only_matched_list_1_dict = {}
            else:
                # this modification was found essential as it was discovered that final dictionary created by this function
                # "identify_list_type_1_and_2" which is also the final dictionary created by this module
                # "fresh_integrated_identify_all_types.py" doesn't contain the field "question_sub_type" for all questions
                # but for only those questions which have their field "question_sub_type" = 'list_type'.
                info['question_sub_type'] = info['question_type']
                # info['question_sub_type'] = ''  # Ensure all questions have the question_sub_type field

            matched_dict[question_id] = info

        print(f"Found {match_count} matches.")
        # debug print statement
        # print("Matched question numbers in the identify function:", matched_question_numbers_for_list_type_1_and_2)  # Print the matched question numbers here
        new_dict_name = f"{dict_name}_only_list_1_and_2_type_dictionary"
        dict_path = base_dir_path / f"{new_dict_name}.py"
        excel_path = base_dir_path / f"{new_dict_name}.xlsx"

        write_dictionary(matched_dict, dict_path, new_dict_name)
        df = pd.DataFrame.from_dict(matched_dict, orient='index')
        df.to_excel(excel_path, index=False)
        print(f"In the function identify_list_type_1_and_2, Dictionary and Excel file only for list_1 and list_2_type created at {dict_path} and {excel_path}")

        # Create a new dictionary name based on the base directory and modified naming scheme
        parts = dict_name.split('_')
        new_dict_name = '_'.join(parts[:-11]) + "_all_types_identified_dictionary"
        dict_path = base_dir_path / f"{new_dict_name}.py"
        excel_path = base_dir_path / f"{new_dict_name}.xlsx"

        # Joining information from matched_dict and data_dict into new_dict
        new_dict = {}
        for question_id, info in data_dict.items():
            # Check if the question_id is in matched_dict to determine question_sub_type and question_complete
            if question_id in matched_dict:
                sub_type = matched_dict[question_id]['question_sub_type']
                # question_complete is being set to False for better functioning of the script of the next module
                # "fresh_integrated_extract_list_type_1_and_2_parts.py"
                question_complete = False  # Set to False if question_id is found in matched_dict
            else:
                sub_type = info['question_type']  # Fallback to question_type if not found in matched_dict
                question_complete = True  # Set to True if question_id is not in matched_dict

            # Update new_dict with information from data_dict and additional fields
            new_dict[question_id] = {**info, 'question_sub_type': sub_type, 'question_complete': question_complete}

        """for question_id, info in data_dict.items():
            sub_type = matched_dict[question_id]['question_sub_type'] if question_id in matched_dict else info[
                'question_type']
            new_dict[question_id] = {**info, 'question_sub_type': sub_type}"""

        # write_dictionary(new_dict, dict_path, new_dict_name)
        df = pd.DataFrame.from_dict(new_dict, orient='index')
        df.to_excel(excel_path, index=False)
        create_excel_for_dict(new_dict, base_dir_path, new_dict_name)
        print(f"Dictionary and Excel file Dictionary {new_dict_name}for created at {dict_path} and {excel_path}")
        # create performance excel using create_performance_excel
        question_type_for_identification = "list_1_and_2_type"
        # creating a blank dictionary only for the sake of running create_performance_excel
        answer_dict = {}
        create_performance_excel(only_matched_list_2_dict, only_matched_list_1_dict, base_dir_path, module_input_dict_name, question_type_for_identification, targets)


    elif operation_mode == 'union':
        # Operation to handle after both question_part and answer_part have been processed
        # Assume that `data_dict` now holds the consolidated results to be further processed
        print("Processing union of results...")
        parts = dict_name.split('_')

        new_dict_name = f"{dict_name}_consolidated_dictionary"
        new_dict_path = base_dir_path / f"{new_dict_name}.py"
        write_dictionary(data_dict, new_dict_path, new_dict_name)
        print(f"Consolidated dictionary created at {new_dict_path}")

        question_dict = load_dictionary(new_dict_name, base_dir_path)
        # Update the performance excel file post union processing
        # create_performance_excel_2(question_dict, base_dir_path, dict_name, "_list_type_1_and_2_performance")
        question_type_for_identification = "list_1_and_2_type"
        # commenting out as the function create_performance_excel is already giving the same output
        # create_performance_excel_2(question_dict, base_dir_path, dict_name, "_list_type_1_and_2_performance", question_type_for_identification)


        return data_dict, new_dict_path  # Ensure you return both the dictionary and a relevant file path or similar


def main():

    module_name = os.path.splitext(os.path.basename(__file__))[0]
    print(f"Now you are in {module_name}")
    # input_to_process_fiat = input("Continue to create text files and identify r_and_a_type and other type questions from dictionary (y/n): ").strip().lower()
    input("Press Enter to continue to create text files and identify r_and_a_type and other type questions from dictionary ..... ")
    input_to_process_fiat = 'y'
    # processed_dict = None  # Initialize to None to handle scope
    # dict_name_used_for_excel = None  # Initialize a variable to hold the dictionary name

    if input_to_process_fiat == 'y':

        parser = argparse.ArgumentParser(description="Identify question types from dictionary.")
        parser.add_argument("dictionary_name", type=str, help="Name of the dictionary module to process")
        parser.add_argument("subfolder", type=str, help="Folder where the dictionary module is located")
        parser.add_argument("--targets", type=str, help="JSON string of targets for different question types", required=True)
        args = parser.parse_args()

        dict_folder = Path(args.subfolder)
        input_dict_name = args.dictionary_name
        dict_folder.mkdir(parents=True, exist_ok=True)
        module_input_dict_name = input_dict_name
        targets = ast.literal_eval(args.targets)


        # input("Please enter the name of the dictionary")

        print(f"input_dict_name is: {input_dict_name}, and dict_folder is: {dict_folder}")
        # input("Press Enter to continue....")
        if not dict_folder.exists():
            print(f"Folder not found: {dict_folder}")
            return

        process_data(input_dict_name, dict_folder, module_input_dict_name, targets)

def process_data(dict_name, process_folder, module_input_dict_name, targets):
    input_dict_name = dict_name
    dict_folder = process_folder
    data_dict = load_dictionary(input_dict_name, dict_folder)
    base_dir_path = process_folder

    # Processing logic here
    # print(f"Processing data from {data_dict}")
    # input("You are now in fresh_integrated_identify_all_types.py module, Press Enter to continue to identify all types of questions starting with r_and_a_type...")
    # base_dir_path = Path(r'C:\Users\PC\Desktop\Question Bank Trials\Python Programming\Trials\Regex Trials\question types')
    # base_dir_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # base_dir_path = input_dict_path
    # dict_name = input("Enter the dictionary file name (without '.py' extension): ")
    # data_dict = load_dictionary(dict_name, base_dir_path)

    if data_dict:
        print(f"Dictionary '{dict_name}' loaded successfully.")
        new_dict_name = '_'.join(dict_name.split('_')[:-2]) + "_r_and_a_identified_dictionary"
        processed_dict, text_file_path = identify_r_and_a_type(targets, module_input_dict_name, data_dict, new_dict_name, base_dir_path)

        if processed_dict:
            print("Reason and Assertion type questions have been identified and extracted.")
            print(f"Dictionary '{dict_name}' loaded successfully.")
            created_file_name_question_part, created_file_name_answer_part = create_text_from_dictionary(data_dict,
                                                                                                         new_dict_name,
                                                                                                         base_dir_path)
            print(
                f"Text files '{created_file_name_question_part}' and '{created_file_name_answer_part}' have been successfully created.")

            # Create a new dictionary name based on the base directory and modified naming scheme
            parts = new_dict_name.split('_')
            new_dict_name_2 = '_'.join(parts[:-2]) + "_list_type_identified_dictionary"

            # Extract list type from loaded dictionary
            print("Processing question part for list type questions...")
            # input("Press Enter to continue...")


            # Convert dictionary question parts into a single string for regex processing
            identify_list_type(targets, module_input_dict_name, processed_dict, pattern_for_list_type_question_part, new_dict_name_2, base_dir_path,
                               "question_part")

            print("Processing answer part for list type answers...")
            # input("Press Enter to continue...")
            # Convert dictionary answer parts into a single string for regex processing
            identify_list_type(targets, module_input_dict_name, processed_dict, pattern_for_list_type_answer_part, new_dict_name_2, base_dir_path,
                               "answer_part")

            print("Processing for creating the output single dictionary after identifying list type...")
            # input("Press Enter to continue...")
            # Now call for processing the union and creating new outputs
            # identify_list_type(data_dict, None, new_dict_name_2, base_dir_path, None, operation_mode='union')
            # processed_dict_list_type = identify_list_type(processed_dict, None, new_dict_name_2, base_dir_path, None, operation_mode='union')
            processed_dict_list_type, created_text_path = identify_list_type(targets, module_input_dict_name, processed_dict, None, new_dict_name_2, base_dir_path, None, operation_mode='union')
            # Now use updated_dict for further processing or output

            if processed_dict_list_type:
                print("List type questions have been identified and extracted.")
                print(f"Dictionary '{new_dict_name_2}' loaded successfully.")
                created_file_name_question_part, created_file_name_answer_part = create_text_from_dictionary(
                    processed_dict_list_type, new_dict_name_2, base_dir_path)
                print(
                    f"Text files '{created_file_name_question_part}' and '{created_file_name_answer_part}' have been successfully created.")

                # Create a new dictionary name based on the base directory and modified naming scheme
                parts = new_dict_name_2.split('_')
                new_dict_name_3 = '_'.join(parts[:-2]) + "_simple_type_identified_dictionary"
                input(f"The new_dict_name_3 for simple_type_identified_dictionary is: {new_dict_name_3}")
                # Extract simple type from loaded dictionary
                print("Processing question part for simple type questions...")
                input("Press Enter to continue processing question part for simple type questions...")
                # Convert dictionary question parts into a single string for regex processing
                identify_simple_type(targets, module_input_dict_name, processed_dict_list_type, pattern_for_simple_type_question_part, new_dict_name_3, base_dir_path,
                                     "question_part")

                print("Processing answer part for simple type answers...")
                input("Press Enter to continue processing answer part for simple type answers......")
                # Convert dictionary answer parts into a single string for regex processing
                identify_simple_type(targets, module_input_dict_name, processed_dict_list_type, pattern_for_simple_type_answer_part, new_dict_name_3, base_dir_path,
                                     "answer_part")

                print("Processing for creating the output single dictionary after identifying simple type ...")
                input("Press Enter to continue processing for creating the output single dictionary after identifying simple type ...")
                # Now call for processing the union and creating new outputs
                # identify_simple_type(data_dict, None, new_dict_name_3, base_dir_path, None, operation_mode='union')
                processed_dict_simple_type, created_text_path = identify_simple_type(targets, module_input_dict_name, processed_dict_list_type, None, new_dict_name_3, base_dir_path, None, operation_mode='union')

                if processed_dict_simple_type:

                    # dict_name = input("Enter the dictionary file name (without '.py' extension): ")
                    # data_dict = load_dictionary(dict_name, base_dir_path)
                    # if data_dict:
                    print(f"Dictionary '{dict_name}' loaded successfully.")
                    created_file_name_question_part, created_file_name_answer_part = create_text_from_dictionary(
                        processed_dict_simple_type,
                        dict_name,
                        base_dir_path)
                    print(
                        f"Text files '{created_file_name_question_part}' and '{created_file_name_answer_part}' have been successfully created.")

                    # Create a new dictionary name based on the base directory and modified naming scheme
                    parts = new_dict_name_3.split('_')
                    new_dict_name_4 = '_'.join(parts[:-2])

                    second_parts = new_dict_name_4.split('_')
                    new_dict_name_5 = '_'.join(parts[:-9]) + "_all_types_identified"

                    # Extract list 1 type and list type 2 from loaded dictionary
                    print("Processing question part for list type questions...")
                    # input("Press Enter to continue...")
                    # Convert dictionary question parts into a single string for regex processing
                    identify_list_type_1_and_2(targets, module_input_dict_name, processed_dict_simple_type, pattern_for_list_type_2, new_dict_name_4, base_dir_path)

                    # Here you might perform additional operations or modifications before calling union
                    print(
                        "Processing for creating the output single dictionary after identifying list_ 1and list_2 type...")
                    # input("Press Enter to continue...")
                    # Now call for processing the union and creating new outputs
                    # identify_list_type_1_and_2(processed_dict_simple_type, None, dict_name, base_dir_path, operation_mode='union')
                    processed_dict_type_1_and_2, created_text_path = identify_list_type_1_and_2(targets, module_input_dict_name, processed_dict_simple_type,None, new_dict_name_5, base_dir_path, operation_mode='union')

                else:
                    print(f"Error loading the dictionary :{processed_dict_simple_type}")
            else:
                print(f"Error loading the dictionary: {processed_dict_list_type}")
        else:
            print(f"Error loading the r_and_a identified dictionary: {processed_dict}")
    else:
        print(f"Error loading the answer options extracted dictionary: {data_dict}")


if __name__ == "__main__":
    main()
