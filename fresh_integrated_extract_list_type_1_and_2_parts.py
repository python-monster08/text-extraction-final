# earlier hindi_final_scratchpad_for_ist_type_2_parts.py finalised on 27 Apr 2024
# this script hindi_temp_scratchpad_for_list_type_1_and_2_parts_ver_4.py finalised on 5 May, 2024
# works without argparse and works to only extract the different parts of the questions of list_ 1 and list_2 type
# it works on sample text_for_list_1/2_parts, creates a temporary dictionary called temp_question_parts
# and then extracts the parts from the contents temporary dictionary,
# the other portions like r_and_a type are present only because of avoiding errors
# it works successfully even for those questions also which have maximum row only up to C
# it works successfully even for for Hindi processing
# the function extract_list_2_parts uses a simplistic and long method which is less innovative as compared to the
# method used for extract_list_1_parts. this function extract_list_2_parts carries out 15 rounds of processing using three different
# patterns. the 13 patterns cover the entire the range of requirements arising from the various samples
# like A-E. / 1-5. with 0 to 3 whitespaces
# initially it didn't handle (1-5A-E) or (1-5A-EA.) with 0 to 3 whitespaces but this was also solved on 5 May, 2024
# fourteenth round processing to look for and add spaces in question_third_part
# fifteenth round processing is to look for and add spaces in answer options
# finally, it creates a dictionary with the name new_final_dict_name = '_'.join(parts[:-8]) + "_questions_extraction_completed_dictionary"
# this module also adds the fields from the dictionary "other_info_batch " into the final dictionary at the beginning of the


import re
from pathlib import Path
import pandas as pd
import ast  # Import ast module for safer evaluation
import importlib.util
from datetime import datetime  # Include this at the top of your script
from openpyxl import load_workbook
from openpyxl.styles import Font
import os
import copy
from collections import defaultdict
import argparse
import json

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
pattern_for_list_type_question_part = re.compile(r'^.*?(?:1\s{0,2}\.|\(\s*1\s*\)).*?(?:2\s{0,2}\.|\(\s*2\s*\)).*',
                                                 re.IGNORECASE | re.DOTALL)

# pattern_for_list_type_answer_part = re.compile(r'\b(?:1\s*(?:and|or|,)\s*2(?:\s*,\s*3)?)\b.*?\b(?:and|or|both|none|either|neither|)\b')
# pattern_for_list_type_answer_part = re.compile(r'\b(?:(?:A|B|C|D)\s*-\s*[1-5]\s*;\s*){2,4}(?:A|B|C|D)\s*-\s*[1-5]\b')
# pattern_for_list_type_answer_part = re.compile(
#    r'(\b(?:1\s*(?:and|or|,)\s*2(?:\s*,\s*3)?)\b.*?\b(?:and|or|both|none|either|neither)\b)|'
#    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)'
# )
# pattern_for_list_type_answer_part = re.compile(
#    r'(\b(?:1\s*(?:and|or|,)?\s*2\s*(?:and|or|,)?\s*(?:3)?\s*(?:and|or|,)?\b.*?\b(?:and|or|both|none|either|neither)\b))|'
#    r'(\b(?:(?:A|B|C|D)\s*-\s*[1-4]\s*;?\s*){3}(?:A|B|C|D)\s*-\s*[1-4]\b)'
# )
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
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'{dict_name} = ' + repr(data_dict))
    print(f"Dictionary {dict_name}.py has been written to {file_path}")


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


def create_formatted_text_from_dictionary(loaded_dictionary, dictionary_name, output_folder_path):
    """
    Create formatted text files from the input dictionary for question and answer parts.
    """
    output_text_file_name = f"{dictionary_name}_formatted_text.txt"
    output_text_file_path = output_folder_path / output_text_file_name

    # Create the formatted text file from the dictionary
    with open(output_text_file_path, 'w', encoding='utf-8') as file:
        for question_id, question_info in loaded_dictionary.items():
            file.write(f"{question_id}\n")
            file.write(f"{question_info.get('question_part_first_part', 'No content available')}\n")
            file.write(f"List-I ({question_info.get('list_1_name', 'No List-I name')}) ")
            file.write(f"List-II ({question_info.get('list_2_name', 'No List-II name')})\n")

            # Correct the label iteration and dynamic row number for List-II
            for i in range(1, 6):
                list_1_row = question_info.get(f'list_1_row{i}', '')
                list_2_row = question_info.get(f'list_2_row{i}', '')
                if list_1_row or list_2_row:  # Only write rows that have content
                    # Adjusting the index for List-II
                    file.write(f"{chr(64 + i)}. {list_1_row}{' ' * (30 - len(list_1_row))}{i}. {list_2_row}\n")

            file.write(f"{question_info.get('question_part_third_part', '')}\n---\n\n")

    print(f"Formatted text file created at: {output_text_file_path}")

    return output_text_file_name


def create_excel_for_dict(data_dict, output_dir, filename_prefix):
    # Convert dictionary to DataFrame
    # df = pd.DataFrame(data_dict.values())
    # Convert dictionary to DataFrame; ensure 'question_id' is included by using items() and constructing a DataFrame directly
    df = pd.DataFrame([{'question_id': k, **v} for k, v in data_dict.items()])

    # Specify the file path to match the dictionary name
    # file_path = output_dir / f"{filename_prefix}.xlsx"
    # to also handle Hindi data
    file_path = output_dir / f"{filename_prefix}.xlsx"

    # Inform the user about the Excel file creation details before creating it
    print(f"Excel file will be created with the name '{filename_prefix}.xlsx' in the directory '{output_dir}'.")
    # input(f"Press Enter to Continue to create the Excel file for {filename_prefix}")

    # Write DataFrame to Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    # Confirm the creation of the file
    print(f"Excel file has been created and saved in '{file_path}'.")

def assess_list_2_parts_extraction_performance(data_dict, file_path):
    # Calculate extraction performance

    for question_id, entry in data_dict.items():
        fields_extracted = []
        fields_not_extracted = []

        # Define keys_to_evaluate for each question_id inside the loop
        # Exclude question_id and question_text from performance evaluation
        keys_to_evaluate = [key for key in entry if key not in ['question_id', 'question_text']]

        for key, value in entry.items():
            if key not in ['question_id', 'question_text']:
                if isinstance(value, bool) and value:
                    fields_extracted.append(key)
                elif isinstance(value, str) and value.strip():
                    fields_extracted.append(key)
                else:
                    fields_not_extracted.append(key)

        filled_fields = len(fields_extracted)
        total_fields = len(fields_extracted) + len(fields_not_extracted)
        performance_percentage = (filled_fields / total_fields) * 100 if total_fields > 0 else 0
        print(f"Extraction performance for {question_id}: {performance_percentage:.2f}%")
        # Optionally, write performance results to a file in the specified folder_path
        # performance_file = folder_path / "extraction_performance.txt"
        performance_file = file_path
        with open(performance_file, 'a') as f:
            f.write(f"{question_id}: {performance_percentage:.2f}%\n")


def create_excel_for_list_2_parts_extraction_performance(data_dict, folder_path, round_number):
    # Define the Excel file path

    excel_file_path = folder_path / 'list_2_parts_extraction_performance.xlsx'

    # Check if the Excel file already exists
    if excel_file_path.exists():
        old_df = pd.read_excel(excel_file_path)
        if 'question_id' not in old_df.columns:
            # Code to handle the absence of 'question_id'
            print("Column 'question_id' does not exist in the DataFrame.")
            # You might want to initialize the DataFrame with the required columns again
            old_df = pd.DataFrame(columns=["Sl No", "Round Number", "Date and time",
                                           "question_id", "No of fields extracted successfully", "%age",
                                           "Fields extracted", "Fields not extracted"])
    else:
        # Explicitly define columns to avoid KeyError later
        old_df = pd.DataFrame(columns=["Sl No", "Round Number", "Date and time",
                                       "question_id", "No of fields extracted successfully", "%age",
                                       "Fields extracted", "Fields not extracted"])

    print("DataFrame columns after initialization:", old_df.columns)  # Debugging output

    # Existing DataFrame to collect new data during this function execution
    existing_df = pd.DataFrame(columns=old_df.columns)

    new_rows = []  # List to store all new rows
    # Iterating through each question ID and its corresponding data in the dictionary
    for question_id, entry in data_dict.items():
        fields_extracted = []
        fields_not_extracted = []
        # Define keys_to_evaluate for each question_id inside the loop
        keys_to_evaluate = [key for key in data_dict[question_id] if key not in ['question_id', 'question_text']]

        # Determine which fields have valid data
        for key, value in entry.items():
            if key in keys_to_evaluate:
                if isinstance(value, bool) and value:
                    fields_extracted.append(key)
                elif isinstance(value, str) and value.strip():
                    fields_extracted.append(key)
                else:
                    fields_not_extracted.append(key)

        # Calculate the performance based on extracted fields
        filled_fields = len(fields_extracted)
        total_fields = len(keys_to_evaluate)
        performance_percentage = (filled_fields / total_fields) * 100 if total_fields > 0 else 0

        new_row = {
            "Sl No": len(existing_df) + 1,
            "Round Number": round_number,
            "Date and time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question_id": question_id,
            "No of fields extracted successfully": filled_fields,
            "%age": performance_percentage,
            "Fields extracted": ', '.join(fields_extracted),
            "Fields not extracted": ', '.join(fields_not_extracted)
        }
        new_rows.append(new_row)
        # to handle KeyError: 'question_id'
        # Check if there's an existing entry for this question_id and round_number for the same date and time
        # Assuming you want to use the current time for 'entry_datetime'
        entry_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        idx = existing_df[
            (existing_df['question_id'] == question_id) &
            (existing_df['Round Number'] == round_number) &
            (existing_df['Date and time'] == entry_datetime)
            ].index

        # If the entry exists, fetch the serial number
        if not idx.empty:
            serial_number = existing_df.loc[idx[0], 'Sl No']
            second_idx = existing_df[
                (existing_df['Sl No'] == serial_number)
            ].index
            if not second_idx.empty:
                # Update existing row if found
                for col, val in new_row.items():
                    existing_df.at[idx[0], col] = val
            else:
                # Append new row if no matching entry found
                new_row_df = pd.DataFrame([new_row])
                existing_df = pd.concat([existing_df, new_row_df], ignore_index=True)

        # Append new data to the existing DataFrame for this session
        existing_df = pd.concat([existing_df, pd.DataFrame([new_row])], ignore_index=True)

        if not idx.empty:
            # Update existing row if found
            for col, val in new_row.items():
                existing_df.at[idx[0], col] = val
        else:
            # Append new row if no matching entry found
            new_row_df = pd.DataFrame([new_row])
            existing_df = pd.concat([existing_df, new_row_df], ignore_index=True)

    # Combine old DataFrame and new data from this session
    # final_df = pd.concat([old_df, existing_df], ignore_index=True)
    # Convert list of new rows to DataFrame and concatenate with old DataFrame - attempting to prevent multiple
    # rows for same question_id and round and serial
    new_rows_df = pd.DataFrame(new_rows)
    final_df = pd.concat([old_df, new_rows_df], ignore_index=True)
    print("Final DataFrame before writing to Excel:", final_df)  # Debugging output

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        final_df.to_excel(writer, sheet_name='Assess', index=False)

    print(f"The Excel file has been updated/created at {excel_file_path}")


# def add_spaces_and_count_spaces(input_string):
def add_spaces_and_count_spaces(input_string, role):

    def count_spaces(string):

        # This will store the counts of spaces between each pair of words
        space_counts = []

        # Split the string into parts using whitespaces as delimiters
        parts = string.split()

        # If there's only one word or none, there are no spaces to count between words
        if len(parts) <= 1:
            return space_counts

        # Initialize the last index from the end of the first word
        last_index = string.find(parts[0]) + len(parts[0])

        # Iterate through remaining parts
        for part in parts[1:]:
            # Find the start of the next word
            current_index = string.find(part, last_index)

            # Number of spaces is the difference between the current word's start and last word's end
            num_spaces = current_index - last_index

            # Append the number of spaces to the list
            space_counts.append(num_spaces)

            # Update the last_index to the end of the current word
            last_index = current_index + len(part)

        return space_counts

    if role == "count_spaces":
        space_counts = count_spaces(input_string)
        return space_counts

    if role == "add_space":
        # Define the pattern to match each character A-H
        pattern = r'([A-H])'

        # Use re.sub() to replace each match with the same character preceded by 5 spaces
        modified_string = re.sub(pattern, r'     \1', input_string)
        print("Modified string:", modified_string)

        # Print space counts for the original and modified strings
        print("Original string:", input_string)
        print("Space counts in original string:", count_spaces(input_string))
        print("Space counts in modified string:", count_spaces(modified_string))

        return modified_string

    elif role == "count_spaces":
        # Return only the counts of spaces between words in the input string
        space_counts = count_spaces(input_string)
        print("Space counts in input string:", space_counts)
        return space_counts



# the function extract_list_2_parts uses a simplistic and long method which is less innovative as compared to the
# method used for extract_list_1_parts. this function extract_list_2_parts carries out 13 rounds of processing using three different
# patterns. these 13 patterns cover the entire the range of requirements arising from the various samples
# like A-E. / 1-5. with 0 to 3 whitespaces
# initially it didn't handle (1-5A-E) or (1-5A-EA.) with 0 to 3 whitespaces but this was also solved on 5 May, 2024
# similarly, presently it works well also for those lists having first column row upto C.
# this function also adds the fields from the dictionary "other_info_batch " into the final dictionary at it's beginning
# def extract_list_2_parts(input_data_dict, temp_dict_name, base_dir_path):
def extract_list_2_parts(input_data_dict, temp_dict_name, base_dir_path, other_info_batch):
    # input("Press Enter to continue extract list 2 parts...")
    # output_path = Path(r'C:\Users\PC\Desktop\Question Bank Trials\Python Programming\Trials\Regex Trials\Hindi Trials\list_1_type_parts_extraction_performance.txt')
    # if not output_path.exists():
    #     output_path.touch()

    # Ensure the directory exists
    base_dir_path.mkdir(parents=True, exist_ok=True)

    # print(f"the question_text parsed is :'{question_text}")

    # Create a dynamically named dictionary
    # input("Press Enter to continue create temporary dictionary...")
    dynamic_dict_name_list_2_parts = f"list_2_temp_question_parts_{temp_dict_name}"

    # Initialize dictionary
    dynamic_dict_name_list_2_parts = {}

    dict_excel_name = f"list_2_temp_question_parts_{temp_dict_name}"
    dict_excel_file_path = base_dir_path/ dict_excel_name

    performance_excel_name = f"list_2_performance_excel_{temp_dict_name}"
    performance_excel_file_path = base_dir_path / performance_excel_name

    recording_text_file_name = f"list_2_temp_question_parts_{temp_dict_name}"
    recording_text_file_path = base_dir_path/ recording_text_file_name

    # Assume data_dict structure is known and each entry contains keys like 'question_type', 'question_sub_type', etc.
    for question_id, info in input_data_dict.items():
        # Copy all existing fields
        dynamic_dict_name_list_2_parts[question_id] = info.copy()

        # Initial dictionary setup for each question
        # Now add or modify specific fields
        dynamic_dict_name_list_2_parts[question_id].update({
            'question_part_first_part': info.get('question_part_first_part', '').strip(),
            'list_1_present': info.get('list_1_present', False),
            'list_2_present': info.get('list_2_present', False),
            'list_1_name': info.get('list_1_name', '').strip(),
            'list_2_name': info.get('list_2_name', '').strip(),
            'list_1_row1': info.get('list_1_row1', '').strip(),
            'list_2_row1': info.get('list_2_row1', '').strip(),
            'list_1_row2': info.get('list_1_row2', '').strip(),
            'list_2_row2': info.get('list_2_row2', '').strip(),
            'list_1_row3': info.get('list_1_row3', '').strip(),
            'list_2_row3': info.get('list_2_row3', '').strip(),
            'list_1_row4': info.get('list_1_row4', '').strip(),
            'list_2_row4': info.get('list_2_row4', '').strip(),
            'list_1_row5': info.get('list_1_row5', '').strip(),
            'list_2_row5': info.get('list_2_row5', '').strip(),
            'question_part_third_part': info.get('question_part_third_part', '').strip(),
            'list_1_entries': info.get('list_1_entries', []),
            'list_2_entries': info.get('list_2_entries', []),
            'part_before_list_2': info.get('part_before_list_2', '').strip(),
            'second_stage_text_to_process': info.get('second_stage_text_to_process', '').strip(),
            'third_stage_text_to_process': info.get('third_stage_text_to_process', '').strip(),
            'fourth_stage_text_to_process': info.get('fourth_stage_text_to_process', '').strip(),
            'fifth_stage_text_to_process': info.get('fifth_stage_text_to_process', '').strip(),
            'sixth_stage_text_to_process': info.get('sixth_stage_text_to_process', '').strip(),
            'seventh_stage_text_to_process': info.get('seventh_stage_text_to_process', '').strip(),
            'eighth_stage_text_to_process': info.get('eighth_stage_text_to_process', '').strip(),
            'ninth_stage_text_to_process': info.get('ninth_stage_text_to_process', '').strip(),
            'tenth_stage_text_to_process': info.get('tenth_stage_text_to_process', '').strip(),
            'eleventh_stage_text_to_process': info.get('eleventh_stage_text_to_process', '').strip(),
            'twelfth_stage_text_to_process': info.get('twelfth_stage_text_to_process', '').strip(),
            'thirteenth_stage_text_to_process': info.get('thirteenth_stage_text_to_process', '').strip(),
            'fourteenth_stage_text_to_process': info.get('fourteenth_stage_text_to_process', '').strip(),
            'fifteenth_stage_text_to_process': info.get('fifteenth_stage_text_to_process', '').strip(),
            'sixteenth_stage_text_to_process': info.get('sixteenth_stage_text_to_process', '').strip(),

            # 'batch_name': info.get('batch_name', '').strip(),
            # 'exam_name': info.get('exam_name', '').strip(),
            # 'exam_stage': info.get('exam_stage', '').strip(),
            # 'marks': info.get('marks', '').strip(),
            # 'negative_marks': info.get('negative_marks', '').strip(),
            'questions_source_file_hyperlink': info.get('questions_source_file_hyperlink', '').strip(),
            # 'test_series': info.get('test_series', '').strip(),
            # 'reference': info.get('reference', '').strip(),
            'type_of_question': info.get('type_of_question', '').strip(),
            'question_type': info.get('question_type', '').strip(),
            'question_sub_type': info.get('question_sub_type', '').strip(),
            'correct_answer_choice': info.get('correct_answer_choice', '').strip(),
            'correct_answer_description': info.get('correct_answer_description', '').strip(),

        })
        # Update with values from other_info_batch
        dynamic_dict_name_list_2_parts[question_id].update({
            # 'pdf_file_path': other_info_batch.get('pdf_file_path', ''),
            # 'output_folder_1': other_info_batch.get('output_folder_1', ''),
            # 'output_folder_2': other_info_batch.get('output_folder_2', ''),
            # 'subfolder': other_info_batch.get('subfolder', ''),
            # 'filename_prefix': other_info_batch.get('filename_prefix', ''),
            # 'dump_folder': other_info_batch.get('dump_folder', ''),
            # 'process_type': other_info_batch.get('process_type', ''),
            'exam_name': other_info_batch.get('exam_name', ''),
            'exam_stage': other_info_batch.get('exam_stage', ''),
            'subject_name': other_info_batch.get('subject_name', ''),
            'area_name': other_info_batch.get('area_name', ''),
            'part_name': other_info_batch.get('part_name', ''),
            # 'text_file_path': other_info_batch.get('text_file_path', ''),
            'batch_name': other_info_batch.get('batch_name', ''),
            # 'process_type_input': other_info_batch.get('process_type_input', ''),
            'type_of_question': other_info_batch.get('type_of_question', ''),
            # need to add str to handling numbers in marls and negative_marks
            'marks': str(other_info_batch.get('marks', '')),
            'negative_marks': str(other_info_batch.get('negative_marks', '')),

        })


    filename_prefix = "temp_dict_name"  # Prefix for the Excel file name

    # excel_file_path = Path(r'C:\Users\PC\Desktop\Question Bank Trials\Python Programming\Trials\Regex Trials\Hindi Trials')
    # excel_file_path = output_path
    # folder_path = excel_file_path
    # create_excel_for_dict_for_list_parts(dynamic_dict_name_list_2_parts, dict_excel_file_path, filename_prefix)
    # create_excel_for_dict_for_list_parts(dynamic_dict_name_list_2_parts, base_dir_path, dict_excel_name):
    # create_excel_for_dict_for_list_parts(dynamic_dict_name_list_2_parts, base_dir_path, dict_excel_name)


    # first round processing
    # first round processing to look for second instance of List I and split around the second match
    # Preparing things for first round processing
    # Create a copy of the dictionary for iteration to avoid modifying it during the loop
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)

    # defining patterns
    # pattern_to_find_list_1 = re.compile(r"(List[-\s]*[1I](?![I]))", re.IGNORECASE)
    # modifying pattern to handle occurrences of Hindi
    # pattern_to_find_list_1 = re.compile(r"List\s*[-–—]\s*[I1](?=\s|$|\s*[\(\[]|[^a-zA-Z0-9_])", re.IGNORECASE) # pattern insisting on the presence of any of three types of dash characters: a hyphen, an en dash, or an em dash.
    pattern_to_find_list_1 = re.compile(r"List\s*[-–— ]?\s*[I1](?=\s|$|\s*[\(\[]|[^a-zA-Z0-9_])",
                                        re.IGNORECASE)  # pattern also adding a blank space in addition and no longer insisting presence of any of three types of dash characters: a hyphen, an en dash, or an em dash.

    pattern_to_find_list_2 = re.compile(r"List[-\s]*(2|II)\b",
                                        re.IGNORECASE)  # successful pattern for List 2/II identification

    # pattern_to_find_list_2 = re.compile(r"(List[-\s]*[2II])", re.IGNORECASE)
    # pattern_to_find_list_2 = re.compile(r"List[-\s]*(2|II)", re.IGNORECASE)
    pattern_to_find_list_2 = re.compile(r"List[-\s]*(2|II)\b", re.IGNORECASE)

    pattern_to_find_list_name = re.compile(r"\(([^)]+)\)")  # Added regex pattern to find list name

    # also keeping things ready for second round processing
    all_second_stages = []  # To store all second stage texts for round two processing
    all_third_stages = []  # To store all second stage texts for round two processing

    # first round processing each part using specific patterns
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                'list_1_present': entry.get('list_1_present', False),
                'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            # commenting out as temp_question_parts_hindi_also is structured with keys like question_id_1, question_id_2, etc.,
            # each mapping to a dictionary that contains the actual question_part.
            # Extract question_text from temp_question_parts_hindi_also dictionary
            # question_text = temp_question_parts_hindi_also.get('question_text', '')
            question_text = entry['question_part']  # Corrected line to access the actual question text

            output_text = f"For first round processing, using regex pattern for pattern_to_find_list_1: {pattern_to_find_list_1.pattern}\n"
            # input(f"Please check the question_text to be processed: {question_text}, Press Enter to continue")

            # matches = pattern_to_find_list_1.finditer(question_text)
            matches = list(pattern_to_find_list_1.finditer(question_text))  # Convert to list immediately
            # print(matches)
            # input()
            num_matches = len(list(matches))
            # for those cases where there is only one occurrence of List I
            if num_matches >= 1:
                # Handle the case where only one match is found
                selected_match = matches[0] if num_matches == 1 else matches[1]
                start_index = selected_match.start()
                end_index = selected_match.end()

                # Splitting text around the match found
                first_part = question_text[:start_index].strip()
                second_part = question_text[end_index:].strip()

                print("Parts found after splitting:")
                print(f"Part 1: {first_part}")
                print(f"Part 2: {second_part}")

                print("Text found to be matching:", pattern_to_find_list_1.findall(question_text))
                # Displaying matches and surrounding text
                for idx, match in enumerate(pattern_to_find_list_1.finditer(question_text), start=1):
                    start = match.start()
                    end = match.end()
                    text_before = question_text[max(0, start - 20):start].split()[-4:]
                    text_after = question_text[end:min(len(question_text), end + 20)].split()[:4]
                    print(f"{idx} match of List I:", match.group())
                    print("Text before match:", " ".join(text_before))
                    print("Text after match:", " ".join(text_after))
                    print()

                list_2_question_parts['list_1_present'] = True
                print(f"list_2_present is: '{list_2_question_parts['list_1_present']}'")

                list_2_question_parts['question_part_first_part'] = first_part
                print(f"question_part_first_part is: '{list_2_question_parts['question_part_first_part']}'")

                list_2_question_parts['second_stage_text_to_process'] = second_part
                print(f"second_stage_text_to_process is: '{list_2_question_parts['second_stage_text_to_process']}'")

                all_second_stages.append(list_2_question_parts)  # Collecting second stage texts

                output_text += "Segment details:\n"
                output_text += f"Question part first part: {list_2_question_parts['question_part_first_part']}\n"
                output_text += f"List 1 present: {list_2_question_parts['list_1_present']}\n"
                output_text += f"Second stage text to process: {list_2_question_parts['second_stage_text_to_process']}\n\n"

                print("Question part first part:", list_2_question_parts['question_part_first_part'])
                print("List 1 present:", list_2_question_parts['list_1_present'])
                print("Second stage text to process:", list_2_question_parts['second_stage_text_to_process'])

                num_extracted_fields = 3  # This value needs to be adjusted based on actual logic
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment, {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
            # for those cases where there are two occurrences of List I
            elif num_matches >= 2:
                second_match = matches[1]  # Get the second match
                start_index = second_match.start()
                end_index = second_match.end()

                # Splitting text around the second match
                first_part = question_text[:start_index].strip()
                second_part = question_text[end_index:].strip()
                # parts = re.split(pattern_to_find_list_1, question_text, maxsplit=2)

                print("Parts found after splitting:")
                for idx, part in enumerate(parts):
                    print(f"Part {idx + 1}: {part.strip()}")

                print("Text found to be matching:", pattern_to_find_list_1.findall(question_text))
                # Displaying matches and surrounding text
                for idx, match in enumerate(pattern_to_find_list_1.finditer(question_text), start=1):
                    start = match.start()
                    end = match.end()
                    text_before = question_text[max(0, start - 20):start].split()[-4:]
                    text_after = question_text[end:min(len(question_text), end + 20)].split()[:4]
                    # print(f"{idx} match of List I:", match.group())
                    # print("Text before match:", " ".join(text_before))
                    # print("Text after match:", " ".join(text_after))
                    # print()

                list_2_question_parts['list_1_present'] = True
                # print(f"list_2_present is: '{list_2_question_parts['list_1_present']}']")

                # list_2_question_parts['question_part_first_part'] = parts[0].strip() + parts[1].strip()
                list_2_question_parts['question_part_first_part'] = first_part
                # print(f"question_part_first_part is: '{list_2_question_parts['question_part_first_part']}']")

                # list_2_question_parts['second_stage_text_to_process'] = parts[2].strip() if len(parts) > 2 else ""
                list_2_question_parts['second_stage_text_to_process'] = second_part
                # print(f"second_stage_text_to_process is: '{list_2_question_parts['second_stage_text_to_process']}']")

                all_second_stages.append(list_2_question_parts)  # Collecting second stage texts

                output_text += "Segment details:\n"
                output_text += f"Question part first part: {list_2_question_parts['question_part_first_part']}\n"
                output_text += f"List 1 present: {list_2_question_parts['list_1_present']}\n"
                output_text += f"Second stage text to process: {list_2_question_parts['second_stage_text_to_process']}\n\n"

                print("Question part first part:", list_2_question_parts['question_part_first_part'])
                print("List 1 present:", list_2_question_parts['list_1_present'])
                print("Second stage text to process:", list_2_question_parts['second_stage_text_to_process'])

                num_extracted_fields = 3  # This value needs to be adjusted based on actual logic
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment, {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)

            # After first round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

        else:
            print(f"For first round processing no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After first round processing is complete for all items
    # After processing, writing to a file for first round processing
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after first round processing has been updated/ created in the directory: '{base_dir_path}'")

    # After processing, assessing and writing to a file for first round processing
    # for assessment of extraction after every round, here first round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    round_number = 1  # Update with your current round number
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, round_number)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_first_round")

    # Second round processing
    # Second round processing to look for first instance of List II and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # defining patterns
    pattern_to_find_list_2 = re.compile(r"List[-\s]*(2|II)\b", re.IGNORECASE)
    pattern_to_find_list_name = re.compile(r"\(([^)]+)\)")  # Added regex pattern to find list name

    # also keeping things ready for third round processing
    all_second_stages = []  # To store all second stage texts for round two processing
    all_third_stages = []  # To store all third stage texts for round two processing
    # input("Press Enter to continue to second round processing...")
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                'list_1_present': entry.get('list_1_present', False),
                'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            question_text = entry['second_stage_text_to_process']  # Corrected line to access the actual question text

            output_text = f"For second round processing, using regex pattern for pattern_to_find_list_2: {pattern_to_find_list_2.pattern}\n"

            # Directly using the question_text variable:
            match = pattern_to_find_list_2.search(question_text)
            if match:
                parts = question_text.split(match.group(0), 1)

                print("Parts found after splitting:")
                for idx, part in enumerate(parts):
                    print(f"Part {idx + 1}: {part.strip()}")
                list_2_question_parts['part_before_list_2'] = parts[0].strip()
                list_2_question_parts['list_2_present'] = True
                list_2_question_parts['third_stage_text_to_process'] = parts[1].strip() if len(parts) > 1 else ""

                # New block to find list name
                name_match = pattern_to_find_list_name.search(list_2_question_parts['part_before_list_2'])
                if name_match:
                    list_2_question_parts['list_1_name'] = name_match.group(1).strip()
                else:
                    list_2_question_parts['list_1_name'] = " "  # Set to a single space if no match

                output_text += "Segment details (Second Stage):\n"
                output_text += f"Part before List 2: {list_2_question_parts['part_before_list_2']}\n"
                output_text += f"List 2 present: {list_2_question_parts['list_2_present']}\n"
                output_text += f"Third stage text to process: {list_2_question_parts['third_stage_text_to_process']}\n"
                output_text += f"List 1 name: {list_2_question_parts['list_1_name']}\n\n"

                print("Results of second stage processing 2-2-2-2-2-2-2-2-2-2-2-2-2-2-2-2")
                print(f"Results for question_id: '{question_id}'")
                print("second_stage_text_to_process:", list_2_question_parts['second_stage_text_to_process'])
                print("Part before List 2:", list_2_question_parts['part_before_list_2'])
                print("List 2 present:", list_2_question_parts['list_2_present'])
                print("Third stage text to process:", list_2_question_parts['third_stage_text_to_process'])
                print("List 1 name:", list_2_question_parts['list_1_name'])

                num_extracted_fields = 4  # Adjusted for additional field
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment (Second Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
            else:
                print("No match found for List 2.")

            # After second round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)
        else:
            print(f"For second round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After second round processing is complete for all items
    # for assessment of extraction after every round, here after second round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 2)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_second_round")

    # Write to the text file after second round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{base_dir_path}'after second round processing has been updated/ created in the directory: '{base_dir_path}'")

    # Third round processing
    # Third round processing to look for first instance of "A." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for fourth round processing
    all_fourth_stages = []  # To store all third stage texts for round two processing
    # input("Press Enter to continue to third round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            # Initialize or reset the dictionary for each segment
            third_round_question_text = entry['third_stage_text_to_process']
            print(f"For question_id :{question_id}, the third_stage_text_to_process is: {third_round_question_text}")
            # Reset parts at the start of each iteration
            third_round_parts = []
            # Initialize the match object to None
            third_round_match = None
            # defining patterns
            # pattern_to_find_A = re.compile(r"\bA(\.|\s{1,2}\.)\b")
            # pattern_to_find_A = re.compile(r"A(\s{0,2}\.)")  # working perfect with A-E. / 1-5. with 0 to 3 whitespaces but doesn't yet handle  (1-5A-E) or (1-5A-EA.) with 0 to 3 whitespaces
            pattern_to_find_A = re.compile(
                r"\(\s{0,3}A\s{0,3}\)\s{0,2}\.?|A\s{0,2}\.")  # modifying the pattern to handle parentheses also
            pattern_to_find_A = re.compile(r"\(\s{0,3}A\s{0,3}\)\s{0,2}\.?|A\s{0,2}\.")
            pattern_to_find_list_name = re.compile(r"\(([^)]+)\)")  # Added regex pattern to find list name

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            third_round_question_text = entry['third_stage_text_to_process']  # Access the actual third_round_question_text
            print(f"For question_id :{question_id}, the third_stage_text_to_process is:{third_round_question_text}")
            output_text = f"For third round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_A: {pattern_to_find_A}\n"
            output_text = f"For third round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_list_name: {pattern_to_find_list_name}\n"

            third_round_match = pattern_to_find_A.search(third_round_question_text)
            if third_round_match:
                third_round_parts = third_round_question_text.split(third_round_match.group(0), 1)
                print("Parts found after splitting:")
                for idx, part in enumerate(third_round_parts):
                    print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found for pattern_to_find_A.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if third_round_parts:
                list_2_question_parts['part_before_A'] = third_round_parts[0].strip()
                print(f"For question_id :{question_id}, part_before_A is: {list_2_question_parts['part_before_A']}")
                list_2_question_parts['fourth_stage_text_to_process'] = third_round_parts[1].strip() if len(
                    parts) > 1 else ""
                print(
                    f"For question_id :{question_id}, fourth_stage_text_to_process is: {list_2_question_parts['fourth_stage_text_to_process']}")

                name_matches = list(pattern_to_find_list_name.finditer(list_2_question_parts['part_before_A']))
                if name_matches:
                    print(f"For question_id :{question_id}, there are {len(name_matches)} matches found.")
                    for match in name_matches:
                        print(f"Match found: {match.group(1)}")

                    num_name_matches = len(list(name_matches))
                    if num_name_matches == 1:
                        # One match found
                        print(
                            f"For question_id :{question_id}, there is {num_name_matches} match, which is: {name_matches}")
                        list_2_question_parts['list_2_name'] = name_matches[0].group(
                            1).strip()  # Extract text inside parentheses

                    elif num_name_matches >= 2:
                        # Two or more matches found, use the first two
                        print(
                            f"For question_id :{question_id}, there are {num_name_matches} matches, which are: {name_matches}")
                        list_2_question_parts['list_1_name'] = name_matches[0].group(
                            1).strip()  # Extract text inside first pair of parentheses
                        list_2_question_parts['list_2_name'] = name_matches[1].group(
                            1).strip()  # Extract text inside second pair of parentheses

                    print(f"the matches for pattern_to_find_list_name are given above, Press Enter to continue ...")
                    # input()

                    print(f" The list_2_question_parts['list_2_name'] is : {list_2_question_parts['list_2_name']}")
                    print(f" The list_2_question_parts['list_1_name'] is : {list_2_question_parts['list_1_name']}")
                    print(f"the list_2_name and list_1_name are given above, Press Enter to continue ...")
                    # input()

            # list_2_question_parts['part_before_A'] = parts[0].strip()
            # print(f"For question_id :{question_id}, part_before_A is: {list_2_question_parts['part_before_A']}")
            # list_2_question_parts['fourth_stage_text_to_process'] = parts[1].strip() if len(parts) > 1 else ""

            output_text += "Segment details (Third Stage):\n"
            output_text += f"part_before_A: {list_2_question_parts['part_before_A']}\n"
            output_text += f"list_1_name: {list_2_question_parts['list_1_name']}\n"
            output_text += f"Fourth stage text to process: {list_2_question_parts['fourth_stage_text_to_process']}\n"
            output_text += f"list_2_name: {list_2_question_parts['list_2_name']}\n\n"

            print("Results of third stage processing 3-3-3-3-3-3-3-3-3-3-3-3-3-3-3-3")
            print(f"Results for question_id: '{question_id}'")
            print("third_stage_text_to_process:", list_2_question_parts['third_stage_text_to_process'])
            print("part_before_A:", list_2_question_parts['part_before_A'])
            print("list_1_name:", list_2_question_parts['list_1_name'])
            print("Fourth stage text to process:", list_2_question_parts['fourth_stage_text_to_process'])
            print("list_2_name:", list_2_question_parts['list_2_name'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (Third Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            start_position = third_round_match.end()
            # After third round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of third round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For third round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After third round processing is complete for all items
    # for assessment of extraction after every round, here after third round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 3)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_third_round")

    # Write to the text file after third round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after third round processing has been updated/ created in the directory: '{base_dir_path}'")

    # Fourth round processing
    # Fourth round processing to look for first instance of "1." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for fifth round processing
    all_fifth_stages = []  # To store all fifth stage texts for round 5 processing
    # input("Press Enter to continue to fourth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            fourth_round_question_text = entry['fourth_stage_text_to_process']
            print(f"For question_id :{question_id}, the fourth_stage_text_to_process is: {fourth_round_question_text}")
            # Reset parts at the start of each iteration
            fourth_round_parts = []
            # Initialize the match object to None
            fourth_round_match = None
            # defining patterns
            # pattern_to_find_A = re.compile(r"A(\s{0,2}\.)")
            # pattern_to_find_A = re.compile(r"\(\s{0,3}A\s{0,3}\)\s{0,2}\.?|A\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_1 = re.compile(r"1(\s{0,2}\.)")
            pattern_to_find_1 = re.compile(
                r"\(\s{0,3}1\s{0,3}\)\s{0,2}\.?|1\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            fourth_round_question_text = entry[
                'fourth_stage_text_to_process']  # Access the actual fourth_round_question_text
            print(f"For question_id :{question_id}, the fourth_stage_text_to_process is:{fourth_round_question_text}")
            output_text = f"For fourth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_A: {pattern_to_find_1}\n"

            fourth_round_match = pattern_to_find_1.search(fourth_round_question_text)
            if fourth_round_match:
                fourth_round_parts = fourth_round_question_text.split(fourth_round_match.group(0), 1)
                print("Parts found after splitting:")
                for idx, part in enumerate(fourth_round_parts):
                    print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found in fourth round for pattern_to_find_1.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if fourth_round_parts:
                list_2_question_parts['list_1_row1'] = fourth_round_parts[0].strip()
                print(f"For question_id :{question_id}, list_1_row1 is: {list_2_question_parts['list_1_row1']}")
                # list_2_question_parts['fifth_stage_text_to_process'] = fourth_round_parts[1].strip() if len(parts) > 1 else ""
                list_2_question_parts['fifth_stage_text_to_process'] = fourth_round_parts[1].strip() if len(
                    list_2_question_parts) > 1 else ""
                print(
                    f"For question_id :{question_id}, fifth_stage_text_to_process is: {list_2_question_parts['fifth_stage_text_to_process']}")

            output_text += "Segment details (Fourth Stage):\n"
            output_text += f"list_1_row1: {list_2_question_parts['list_1_row1']}\n"
            output_text += f"fifth_stage_text_to_process: {list_2_question_parts['fifth_stage_text_to_process']}\n"

            print("Results of fourth stage processing 4-4-4-4-4-4-4-4-4-4-4-4-4-4-4-4")
            print(f"Results for question_id: '{question_id}'")
            print("fourth_stage_text_to_process:", list_2_question_parts['fourth_stage_text_to_process'])
            print("fifth_stage_text_to_process:", list_2_question_parts['fifth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (Fourth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After fourth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of fourth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For fourth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After fourth round processing is complete for all items
    # for assessment of extraction after every round, here after fourth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 4)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_fourth_round")

    # Write to the text file after fourth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after fourth processing has been updated/ created in the directory: '{base_dir_path}'")

    # Fifth round processing
    # Fifth round processing to look for first instance of "B." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for sixth round processing
    all_sixth_stages = []  # To store all sixth stage texts for round two processing
    # input("Press Enter to continue to fifth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            fifth_round_question_text = entry['fifth_stage_text_to_process']
            print(f"For question_id :{question_id}, the fifth_stage_text_to_process is: {fifth_round_question_text}")
            # Reset parts at the start of each iteration
            fifth_round_parts = []
            # Initialize the match object to None
            fifth_round_match = None
            # defining patterns
            # pattern_to_find_A = re.compile(r"A(\s{0,2}\.)")
            # pattern_to_find_A = re.compile(r"\(\s{0,3}A\s{0,3}\)\s{0,2}\.?|A\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_1 = re.compile(r"1(\s{0,2}\.)")
            pattern_to_find_1 = re.compile(
                r"\(\s{0,3}1\s{0,3}\)\s{0,2}\.?|1\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_B = re.compile(r"B(\s{0,2}\.)")
            pattern_to_find_B = re.compile(
                r"\(\s{0,3}B\s{0,3}\)\s{0,2}\.?|B\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            fifth_round_question_text = entry[
                'fifth_stage_text_to_process']  # Access the actual fifth_round_question_text
            print(f"For question_id :{question_id}, the fifth_stage_text_to_process is:{fifth_round_question_text}")
            output_text = f"For fifth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_B: {pattern_to_find_B}\n"

            fifth_round_match = pattern_to_find_B.search(fifth_round_question_text)
            if fifth_round_match:
                fifth_round_parts = fifth_round_question_text.split(fifth_round_match.group(0), 1)
                print("fifth round parts found after splitting:")
                for idx, part in enumerate(fifth_round_parts):
                    print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found in fifth round for pattern_to_find_B.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if fifth_round_parts:
                list_2_question_parts['list_2_row1'] = fifth_round_parts[0].strip()
                print(f"For question_id :{question_id}, list_2_row1 is: {list_2_question_parts['list_2_row1']}")
                # list_2_question_parts['sixth_stage_text_to_process'] = fifth_round_parts[1].strip() if len(parts) > 1 else ""
                list_2_question_parts['sixth_stage_text_to_process'] = fifth_round_parts[1].strip() if len(
                    list_2_question_parts) > 1 else ""
                print(
                    f"For question_id :{question_id}, sixth_stage_text_to_process is: {list_2_question_parts['sixth_stage_text_to_process']}")

            output_text += "Segment details (fifth Stage):\n"
            output_text += f"list_2_row1: {list_2_question_parts['list_1_row1']}\n"
            output_text += f"sixth_stage_text_to_process: {list_2_question_parts['sixth_stage_text_to_process']}\n"

            print("Results of fifth stage processing 5-5-5-5-5-5-5-5-5-5-5-5-5-5-5-5")
            print(f"Results for question_id: '{question_id}'")
            print("list_2_row1:", list_2_question_parts['list_2_row1'])
            print("sixth_stage_text_to_process:", list_2_question_parts['sixth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (fifth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After fifth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of fifth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For fifth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After fifth round processing is complete for all items
    # for assessment of extraction after every round, here after fifth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 5)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_fifth_round")

    # Write to the text file after fifth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after fifth processing has been updated/ created in the directory: '{base_dir_path}'")

    # Sixth round processing
    # Sixth round processing to look for first instance of "2." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for seventh round processing
    all_seventh_stages = []  # To store all seventh stage texts for round two processing
    # input("Press Enter to continue to sixth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            sixth_round_question_text = entry['sixth_stage_text_to_process']
            # print(f"For question_id :{question_id}, the sixth_stage_text_to_process is: {sixth_round_question_text}")
            # Reset parts at the start of each iteration
            sixth_round_parts = []
            # Initialize the match object to None
            sixth_round_match = None
            # defining patterns
            # pattern_to_find_B = re.compile(r"B(\s{0,2}\.)")
            # pattern_to_find_B = re.compile(r"\(\s{0,3}B\s{0,3}\)\s{0,2}\.?|B\s{0,2}\.")  # modifying the pattern to handle parentheses also
            pattern_to_find_2 = re.compile(r"2(\s{0,2}\.)")
            pattern_to_find_2 = re.compile(
                r"\(\s{0,3}2\s{0,3}\)\s{0,2}\.?|2\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            sixth_round_question_text = entry[
                'sixth_stage_text_to_process']  # Access the actual sixth_round_question_text
            print(f"For question_id :{question_id}, the sixth_stage_text_to_process is:{sixth_round_question_text}")
            output_text = f"For sixth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_2: {pattern_to_find_2}\n"

            sixth_round_match = pattern_to_find_2.search(sixth_round_question_text)
            if sixth_round_match:
                sixth_round_parts = sixth_round_question_text.split(sixth_round_match.group(0), 1)
                # print("sixth round parts found after splitting:")
                # for idx, part in enumerate(sixth_round_parts):
                #    print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found in sixth round for pattern_to_find_2.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if sixth_round_parts:
                list_2_question_parts['list_1_row2'] = sixth_round_parts[0].strip()
                print(f"For question_id :{question_id}, list_1_row2 is: {list_2_question_parts['list_1_row2']}")
                list_2_question_parts['seventh_stage_text_to_process'] = sixth_round_parts[1].strip() if len(
                    list_2_question_parts) > 1 else ""
                print(
                    f"For question_id :{question_id}, seventh_stage_text_to_process is: {list_2_question_parts['sixth_stage_text_to_process']}")

            output_text += "Segment details (sixth Stage):\n"
            output_text += f"list_1_row2: {list_2_question_parts['list_1_row2']}\n"
            output_text += f"seventh_stage_text_to_process: {list_2_question_parts['seventh_stage_text_to_process']}\n"

            print("Results of sixth stage processing 6-6-6-6-6-6-6-6-6-6-6-6-6-6-6-6")
            print(f"Results for question_id: '{question_id}'")
            print("list_1_row2:", list_2_question_parts['list_1_row2'])
            print("seventh_stage_text_to_process:", list_2_question_parts['seventh_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (sixth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After sixth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of sixth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For sixth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After sixth round processing is complete for all items
    # for assessment of extraction after every round, here after sixth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 6)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_sixth_round")

    # Write to the text file after sixth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after sixth processing has been updated/ created in the directory: '{base_dir_path}'")

    # seventh round processing
    # Seventh round processing to look for first instance of "C." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for eighth round processing
    all_eighth_stages = []  # To store all eighth stage texts for round two processing
    # input("Press Enter to continue to seventh round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            seventh_round_question_text = entry['seventh_stage_text_to_process']
            # print(f"For question_id :{question_id}, the seventh_stage_text_to_process is: {seventh_round_question_text}")
            # Reset parts at the start of each iteration
            seventh_round_parts = []
            # Initialize the match object to None
            seventh_round_match = None
            # defining patterns
            # pattern_to_find_2 = re.compile(r"2(\s{0,2}\.)")
            # pattern_to_find_2 = re.compile(r"\(\s{0,3}2\s{0,3}\)\s{0,2}\.?|2\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_C = re.compile(r"C(\s{0,2}\.)")
            pattern_to_find_C = re.compile(
                r"\(\s{0,3}C\s{0,3}\)\s{0,2}\.?|C\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            seventh_round_question_text = entry[
                'seventh_stage_text_to_process']  # Access the actual seventh_round_question_text
            # print(f"For question_id :{question_id}, the seventh_stage_text_to_process is:{seventh_round_question_text}")
            output_text = f"For seventh round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_C: {pattern_to_find_C}\n"

            seventh_round_match = pattern_to_find_C.search(seventh_round_question_text)
            if seventh_round_match:
                seventh_round_parts = seventh_round_question_text.split(seventh_round_match.group(0), 1)
                # print("seventh round parts found after splitting:")
                # for idx, part in enumerate(seventh_round_parts):
                # print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found in seventh round for pattern_to_find_C.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if seventh_round_parts:
                list_2_question_parts['list_2_row2'] = seventh_round_parts[0].strip()
                # print(f"For question_id :{question_id}, list_2_row1 is: {list_2_question_parts['list_2_row1']}")
                # list_2_question_parts['eighth_stage_text_to_process'] = seventh_round_parts[1].strip() if len(parts) > 1 else ""
                list_2_question_parts['eighth_stage_text_to_process'] = seventh_round_parts[1].strip() if len(
                    list_2_question_parts) > 1 else ""
                # print(f"For question_id :{question_id}, eighth_stage_text_to_process is: {list_2_question_parts['eighth_stage_text_to_process']}")

            output_text += "Segment details (seventh Stage):\n"
            output_text += f"list_2_row2: {list_2_question_parts['list_2_row2']}\n"
            output_text += f"eighth_stage_text_to_process: {list_2_question_parts['eighth_stage_text_to_process']}\n"

            print("Results of seventh stage processing 7-7-7-7-7-7-7-7-7-7-7-7-7-7-7-7")
            print(f"Results for question_id: '{question_id}'")
            print("list_2_row2:", list_2_question_parts['list_2_row2'])
            print("eighth_stage_text_to_process:", list_2_question_parts['eighth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (seventh Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After seventh round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of seventh round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For seventh round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After seventh round processing is complete for all items
    # for assessment of extraction after every round, here after seventh round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 7)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_seventh_round")

    # Write to the text file after seventh round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after seventh round processing has been updated/ created in the directory: '{base_dir_path}'")

    # eighth round processing
    # eighth round processing to look for first instance of "3." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for ninth round processing
    all_ninth_stages = []  # To store all ninth stage texts for round two processing
    # input("Press Enter to continue to eighth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            eighth_round_question_text = entry['eighth_stage_text_to_process']
            # print(f"For question_id :{question_id}, the eighth_stage_text_to_process is: {eighth_round_question_text}")
            # Reset parts at the start of each iteration
            eighth_round_parts = []
            # Initialize the match object to None
            eighth_round_match = None
            # defining patterns
            # pattern_to_find_C = re.compile(r"C(\s{0,2}\.)")
            # pattern_to_find_C = re.compile(r"\(\s{0,3}C\s{0,3}\)\s{0,2}\.?|C\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_3 = re.compile(r"3(\s{0,2}\.)")
            pattern_to_find_3 = re.compile(
                r"\(\s{0,3}3\s{0,3}\)\s{0,2}\.?|3\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            eighth_round_question_text = entry[
                'eighth_stage_text_to_process']  # Access the actual eighth_round_question_text
            # print(f"For question_id :{question_id}, the eighth_stage_text_to_process is:{eighth_round_question_text}")
            output_text = f"For eighth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_3: {pattern_to_find_3}\n"

            eighth_round_match = pattern_to_find_3.search(eighth_round_question_text)
            if eighth_round_match:
                eighth_round_parts = eighth_round_question_text.split(eighth_round_match.group(0), 1)
                # print("eighth round parts found after splitting:")
                # for idx, part in enumerate(eighth_round_parts):
                # print(f"Part {idx + 1}: {part.strip()}")

            else:
                print("No match found in eighth round for pattern_to_find_3.")
                continue  # Skip to the next iteration if no match is found

            # Handling the results if parts were successfully created
            if eighth_round_parts:
                list_2_question_parts['list_1_row3'] = eighth_round_parts[0].strip()
                # print(f"For question_id :{question_id}, list_1_row3 is: {list_2_question_parts['list_1_row3']}")
                # list_2_question_parts['ninth_stage_text_to_process'] = eighth_round_parts[1].strip() if len(parts) > 1 else ""
                list_2_question_parts['ninth_stage_text_to_process'] = eighth_round_parts[1].strip() if len(
                    list_2_question_parts) > 1 else ""
                # print(f"For question_id :{question_id}, ninth_stage_text_to_process is: {list_2_question_parts['ninth_stage_text_to_process']}")

            output_text += "Segment details (eighth Stage):\n"
            output_text += f"list_1_row3: {list_2_question_parts['list_1_row3']}\n"
            output_text += f"ninth_stage_text_to_process: {list_2_question_parts['ninth_stage_text_to_process']}\n"

            print("Results of eighth stage processing 8-8-8-8-8-8-8-8-8-8-8-8-8-8-8-8")
            print(f"Results for question_id: '{question_id}'")
            print("list_1_row3:", list_2_question_parts['list_1_row3'])
            print("ninth_stage_text_to_process:", list_2_question_parts['ninth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (eighth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After eighth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of eighth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For eighth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After eighth round processing is complete for all items
    # for assessment of extraction after every round, here after eighth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 8)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_eighth_round")

    # Write to the text file after eighth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after eighth round processing has been updated/ created in the directory: '{base_dir_path}'")

    # ninth round processing
    # ninth round processing to look for first instance of "D." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for tenth round processing
    all_tenth_stages = []  # To store all tenth stage texts for round two processing
    # input("Press Enter to continue to ninth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            ninth_round_question_text = entry['ninth_stage_text_to_process']
            # print(f"For question_id :{question_id}, the ninth_stage_text_to_process is: {ninth_round_question_text}")
            # Reset parts at the start of each iteration
            ninth_round_parts = []
            # Initialize the match object to None
            ninth_round_match = None
            # defining patterns
            # pattern_to_find_3 = re.compile(r"3(\s{0,2}\.)")
            # pattern_to_find_3 = re.compile(r"\(\s{0,3}3\s{0,3}\)\s{0,2}\.?|3\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_D = re.compile(r"D(\s{0,2}\.)")
            pattern_to_find_D = re.compile(
                r"\(\s{0,3}D\s{0,3}\)\s{0,2}\.?|D\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            ninth_round_question_text = entry[
                'ninth_stage_text_to_process']  # Access the actual ninth_round_question_text
            # print(f"For question_id :{question_id}, the ninth_stage_text_to_process is:{ninth_round_question_text}")
            output_text = f"For ninth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_D: {pattern_to_find_D}\n"

            ninth_round_match = pattern_to_find_D.search(ninth_round_question_text)
            if ninth_round_match:
                ninth_round_parts = ninth_round_question_text.split(ninth_round_match.group(0), 1)
                # print("ninth round parts found after splitting:")
                # for idx, part in enumerate(ninth_round_parts):
                # print(f"Part {idx + 1}: {part.strip()}")
                # Handling the results if parts were successfully created
                if ninth_round_parts:
                    list_2_question_parts['list_2_row3'] = ninth_round_parts[0].strip()
                    # print(f"For question_id :{question_id}, list_2_row3 is: {list_2_question_parts['list_2_row3']}")
                    # list_2_question_parts['tenth_stage_text_to_process'] = ninth_round_parts[1].strip() if len(parts) > 1 else ""
                    list_2_question_parts['tenth_stage_text_to_process'] = ninth_round_parts[1].strip() if len(
                        list_2_question_parts) > 1 else ""
                    # print(f"For question_id :{question_id}, tenth_stage_text_to_process is: {list_2_question_parts['tenth_stage_text_to_process']}")

            else:
                # D not found, abnormal flow
                print("No match found in ninth round for pattern_to_find_D.")
                # case of no row D in List I but need to extract list_2_row3 and maybe a row 4 in List II
                print("Proceed to ninth_round_skip_D_match and find 4.")
                # Reset parts at the start of each iteration
                ninth_round_skip_D_parts = []
                # Initialize the match object to None
                ninth_round_skip_D_match = None
                pattern_to_find_4 = re.compile(r"4(\s{0,2}\.)")
                # pattern_to_find_E = re.compile(r"E(\s{0,2}\.)")
                ninth_round_skip_D_match_4 = pattern_to_find_4.search(ninth_round_question_text)
                if ninth_round_skip_D_match_4:
                    # case of no row D in List I but a row 4 in List II
                    list_2_question_parts['tenth_stage_text_to_process'] = ""
                    print(f"ninth_round_skip_D_match_4: {ninth_round_skip_D_match_4}")
                    # input(f"tenth_round_skip_4_match_E: {tenth_round_skip_4_match_E}, Press Enter to continue....")
                    ninth_round_skip_D_parts = ninth_round_question_text.split(ninth_round_skip_D_match_4.group(0), 1)
                    # print("tenth round parts found after splitting:")
                    # for idx, part in enumerate(tenth_round_parts):
                    # print(f"Part {idx + 1}: {part.strip()}")
                    if ninth_round_skip_D_parts:
                        list_2_question_parts['list_2_row3'] = ninth_round_skip_D_parts[0].strip()
                        # print(f"For question_id :{question_id}, list_2_row3 is: {list_2_question_parts['list_2_row3']}")
                        # as we are handling the tenth_stage_text_to_process here itself
                        list_2_question_parts['eleventh_stage_text_to_process'] = ninth_round_skip_D_parts[
                            1].strip() if len(
                            parts) > 1 else ""
                        # print(f"For question_id :{question_id}, eleventh_stage_text_to_process is: {list_2_question_parts['eleventh_stage_text_to_process']}")
                        print(
                            f"list_2_row3: {list_2_question_parts['list_2_row3']}, tenth_stage_text_to_process: {list_2_question_parts['tenth_stage_text_to_process']}, eleventh_stage_text_to_process: {list_2_question_parts['eleventh_stage_text_to_process']},Press Enter to continue....")
                        # input(f"list_2_row3: {list_2_question_parts['list_2_row3']}, tenth_stage_text_to_process: {list_2_question_parts['tenth_stage_text_to_process']}, eleventh_stage_text_to_process: {list_2_question_parts['eleventh_stage_text_to_process']},Press Enter to continue....")
                    else:
                        # as end of question
                        list_2_question_parts['eleventh_stage_text_to_process'] = ""
                else:
                    #  # case of no row D in List I and no row 4 in List II thereby meaning the end of the question
                    # but need to extract list_2_row3
                    print("Proceed to find question_third_part_match and list_2_row3")
                    # input("Proceed to find question_third_part_match and list_2_row3., Press Enter to continue....")
                    # Initialize the match object to None
                    question_third_part_match_in_round_9 = None
                    # pattern_to_find_colon = re.compile(r"^(.*):.*$", re.MULTILINE)
                    # Adjusted pattern to optionally capture content after the colon if it exists
                    # pattern_to_find_colon = re.compile(r"^(.*?):(.*?)$", re.MULTILINE)
                    # Regex to find the position of the first colon
                    pattern_to_find_colon = re.compile(r":")
                    question_third_part_match_in_round_9 = pattern_to_find_colon.search(ninth_round_question_text)
                    if question_third_part_match_in_round_9:
                        # Initialize ninth_round_number_of_lines_before_colon
                        ninth_round_number_of_lines_before_colon = 0

                        # Position of the first colon
                        ninth_round_colon_index_ = question_third_part_match_in_round_9.start()

                        # Extract everything before the colon
                        part_before_colon = ninth_round_question_text[:ninth_round_colon_index_]
                        # Extract everything after the colon, including all characters and new lines
                        part_after_colon = ninth_round_question_text[
                                           ninth_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                        print(f"For question_id: {question_id}, ninth_round_question_text: {ninth_round_question_text}")
                        print(
                            f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, ninth_round_colon_index_ is: {ninth_round_colon_index_}")

                        # Split the entire text into lines to enable identifying the line containing the colon
                        all_lines_ninth_round = ninth_round_question_text.split('\n')

                        # Use enumerate to find the line index where the colon exists
                        ninth_round_colon_line_index = -1
                        for i, line in enumerate(all_lines_ninth_round):
                            print(f"Line number/ index: {i} is: {line}")
                            if ':' in line:
                                ninth_round_colon_line_index = i

                        print(f"all_lines_ninth_round are: {all_lines_ninth_round}")

                        # Now split 'part_before_colon' into lines
                        ninth_round_only_lines_before_colon = part_before_colon.split('\n')

                        # Ensure only non-empty lines are kept and strip them
                        ninth_round_only_lines_before_colon = [line.strip() for line in
                                                               ninth_round_only_lines_before_colon if line.strip()]

                        # Use enumerate to loop through each line and its index
                        for index, line_before_colon in enumerate(ninth_round_only_lines_before_colon):
                            print(f"Only for lines_before_colon, line number {index}: {line_before_colon}")
                        print(f"all lines_before_colon are: {ninth_round_only_lines_before_colon}")

                        ninth_round_number_of_lines_before_colon = len(ninth_round_only_lines_before_colon)
                        print(
                            f"ninth_round_number_of_lines_before_colon is: {ninth_round_number_of_lines_before_colon}")

                        # Assign the text from the line before the line containing the colon to 'list_2_row3'
                        list_2_row3 = ""
                        for line in ninth_round_only_lines_before_colon[:-1]:
                            list_2_row3 += line + "\n"
                        list_2_question_parts[
                            'list_2_row3'] = list_2_row3.strip()  # to remove the last newline added from the loop
                        print("Manually concatenated text:", list_2_row3)

                        # Remove the text from 'list_2_row3' from 'ninth_round_question_text' and assign to 'question_part_third_part'
                        list_2_question_parts['question_part_third_part'] = ninth_round_question_text.replace(
                            list_2_row3, '')

                        print("list_2_row3:", list_2_question_parts['list_2_row3'])
                        print(
                            f"For question_id {question_id}, question_part_third_part is : {list_2_question_parts['question_part_third_part']}")

                        # End of question processing
                        list_2_question_parts['tenth_stage_text_to_process'] = ""
                        list_2_question_parts['eleventh_stage_text_to_process'] = ""

                        # Output for verification
                        print("Apparently, the question ends here")
                        input(f"Press Enter to continue processing in ninth Stage.....' ")
                    else:
                        print("No colon found in the text.")

            output_text += "Segment details (ninth Stage):\n"
            output_text += f"list_2_row3: {list_2_question_parts['list_2_row3']}\n"
            output_text += f"tenth_stage_text_to_process: {list_2_question_parts['tenth_stage_text_to_process']}\n"

            print("Results of ninth stage processing 9-9-9-9-9-9-9-9-9-9-9-9-9-9-9-9")
            print(f"Results for question_id: '{question_id}'")
            print("list_2_row3:", list_2_question_parts['list_2_row3'])
            print("tenth_stage_text_to_process:", list_2_question_parts['tenth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (ninth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After ninth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of ninth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For ninth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After ninth round processing is complete for all items
    # for assessment of extraction after every round, here after ninth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 9)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_ninth_round")

    # Write to the text file after ninth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after ninth round processing has been updated/ created in the directory: '{base_dir_path}'")

    # tenth round processing
    # tenth round processing to look for first instance of "4." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for eleventh round processing
    all_eleventh_stages = []  # To store all eleventh stage texts for round two processing
    # input("Press Enter to continue to tenth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            tenth_round_question_text = entry['tenth_stage_text_to_process']
            # print(f"For question_id :{question_id}, the tenth_stage_text_to_process is: {tenth_round_question_text}")
            # Reset parts at the start of each iteration
            tenth_round_parts = []
            # Initialize the match object to None
            tenth_round_match = None
            # defining patterns
            # pattern_to_find_D = re.compile(r"D(\s{0,2}\.)")
            # pattern_to_find_D = re.compile(r"\(\s{0,3}D\s{0,3}\)\s{0,2}\.?|D\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_4 = re.compile(r"4(\s{0,2}\.)")
            pattern_to_find_4 = re.compile(
                r"\(\s{0,3}4\s{0,3}\)\s{0,2}\.?|4\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            tenth_round_question_text = entry[
                'tenth_stage_text_to_process']  # Access the actual tenth_round_question_text
            # print(f"For question_id :{question_id}, the tenth_stage_text_to_process is:{tenth_round_question_text}")
            output_text = f"For tenth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_4: {pattern_to_find_4}\n"

            tenth_round_match = pattern_to_find_4.search(tenth_round_question_text)
            if tenth_round_match:
                tenth_round_parts = tenth_round_question_text.split(tenth_round_match.group(0), 1)
                # print("tenth round parts found after splitting:")
                # for idx, part in enumerate(tenth_round_parts):
                # print(f"Part {idx + 1}: {part.strip()}")
                # Handling the results if parts were successfully created
                if tenth_round_parts:
                    list_2_question_parts['list_1_row4'] = tenth_round_parts[0].strip()
                    # print(f"For question_id :{question_id}, list_1_row4 is: {list_2_question_parts['list_1_row4']}")
                    # list_2_question_parts['eleventh_stage_text_to_process'] = tenth_round_parts[1].strip() if len(parts) > 1 else ""
                    list_2_question_parts['eleventh_stage_text_to_process'] = tenth_round_parts[1].strip() if len(
                        list_2_question_parts) > 1 else ""
                    # print(f"For question_id :{question_id}, eleventh_stage_text_to_process is: {list_2_question_parts['eleventh_stage_text_to_process']}")

            else:
                # 4 not found, abnormal flow
                print("No match found in tenth round for pattern_to_find_4.")
                # case of no row 4 in List I but need to extract list_1_row4 and maybe a row 5 in List II
                print("Proceed to tenth_round_skip_4_match and find E.")
                # Reset parts at the start of each iteration
                tenth_round_skip_4_parts = []
                # Initialize the match object to None
                tenth_round_skip_4_match = None
                pattern_to_find_E = re.compile(r"E(\s{0,2}\.)")
                tenth_round_skip_4_match_E = pattern_to_find_E.search(tenth_round_question_text)
                if tenth_round_skip_4_match_E:
                    # case of no row 4 in List II but a row 5 in List I
                    list_2_question_parts['eleventh_stage_text_to_process'] = ""
                    print(f"tenth_round_skip_e_match_5: {tenth_round_skip_4_match_E}")
                    # input(f"tenth_round_skip_4_match_E: {tenth_round_skip_4_match_E}, Press Enter to continue....")
                    tenth_round_skip_4_parts = tenth_round_question_text.split(tenth_round_skip_4_match_E.group(0), 1)
                    # print("eleventh round parts found after splitting:")
                    # for idx, part in enumerate(eleventh_round_parts):
                    # print(f"Part {idx + 1}: {part.strip()}")
                    if tenth_round_skip_4_parts:
                        list_2_question_parts['list_1_row4'] = tenth_round_skip_4_parts[0].strip()
                        # print(f"For question_id :{question_id}, list_1_row4 is: {list_2_question_parts['list_1_row4']}")
                        # as we are handling the eleventh_stage_text_to_process here itself
                        list_2_question_parts['twelfth_stage_text_to_process'] = tenth_round_skip_4_parts[
                            1].strip() if len(
                            parts) > 1 else ""
                        # print(f"For question_id :{question_id}, twelfth_stage_text_to_process is: {list_2_question_parts['twelfth_stage_text_to_process']}")
                        print(
                            f"list_1_row4: {list_2_question_parts['list_1_row4']}, eleventh_stage_text_to_process: {list_2_question_parts['eleventh_stage_text_to_process']}, twelfth_stage_text_to_process: {list_2_question_parts['twelfth_stage_text_to_process']},Press Enter to continue....")
                        # input(f"list_1_row4: {list_2_question_parts['list_1_row4']}, eleventh_stage_text_to_process: {list_2_question_parts['eleventh_stage_text_to_process']}, twelfth_stage_text_to_process: {list_2_question_parts['twelfth_stage_text_to_process']},Press Enter to continue....")
                    else:
                        # as end of question
                        list_2_question_parts['twelfth_stage_text_to_process'] = ""
                else:
                    #  # case of no row 4 in List II and no row E in List II thereby meaning the end of the question
                    # but need to extract list_2_row4
                    print("Proceed to find question_third_part_match and list_1_row4")
                    # input("Proceed to find question_third_part_match and list_1_row4., Press Enter to continue....")
                    # Initialize the match object to None
                    question_third_part_match_in_round_10 = None
                    # pattern_to_find_colon = re.compile(r"^(.*):.*$", re.MULTILINE)
                    # Adjusted pattern to optionally capture content after the colon if it exists
                    # pattern_to_find_colon = re.compile(r"^(.*?):(.*?)$", re.MULTILINE)
                    # Regex to find the position of the first colon
                    pattern_to_find_colon = re.compile(r":")
                    question_third_part_match_in_round_10 = pattern_to_find_colon.search(tenth_round_question_text)
                    if question_third_part_match_in_round_10:
                        # Initialize tenth_round_number_of_lines_before_colon
                        tenth_round_number_of_lines_before_colon = 0

                        # Position of the first colon
                        tenth_round_colon_index_ = question_third_part_match_in_round_10.start()

                        # Extract everything before the colon
                        part_before_colon = tenth_round_question_text[:tenth_round_colon_index_]
                        # Extract everything after the colon, including all characters and new lines
                        part_after_colon = tenth_round_question_text[
                                           tenth_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                        print(f"For question_id: {question_id}, tenth_round_question_text: {tenth_round_question_text}")
                        print(
                            f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, tenth_round_colon_index_ is: {tenth_round_colon_index_}")

                        # Split the entire text into lines to enable identifying the line containing the colon
                        all_lines_tenth_round = tenth_round_question_text.split('\n')

                        # Use enumerate to find the line index where the colon exists
                        tenth_round_colon_line_index = -1
                        for i, line in enumerate(all_lines_tenth_round):
                            print(f"Line number/ index: {i} is: {line}")
                            if ':' in line:
                                tenth_round_colon_line_index = i

                        print(f"all_lines_tenth_round are: {all_lines_tenth_round}")

                        # Now split 'part_before_colon' into lines
                        tenth_round_only_lines_before_colon = part_before_colon.split('\n')

                        # Ensure only non-empty lines are kept and strip them
                        tenth_round_only_lines_before_colon = [line.strip() for line in
                                                               tenth_round_only_lines_before_colon if line.strip()]

                        # Use enumerate to loop through each line and its index
                        for index, line_before_colon in enumerate(tenth_round_only_lines_before_colon):
                            print(f"Only for lines_before_colon, line number {index}: {line_before_colon}")
                        print(f"all lines_before_colon are: {tenth_round_only_lines_before_colon}")

                        tenth_round_number_of_lines_before_colon = len(tenth_round_only_lines_before_colon)
                        print(
                            f"tenth_round_number_of_lines_before_colon is: {tenth_round_number_of_lines_before_colon}")

                        # Assign the text from the line before the line containing the colon to 'list_1_row4'
                        list_1_row4 = ""
                        for line in tenth_round_only_lines_before_colon[:-1]:
                            list_1_row4 += line + "\n"
                        list_2_question_parts[
                            'list_1_row4'] = list_1_row4.strip()  # to remove the last newline added from the loop
                        print("Manually concatenated text:", list_1_row4)

                        # Remove the text from 'list_1_row4' from 'tenth_round_question_text' and assign to 'question_part_third_part'
                        list_2_question_parts['question_part_third_part'] = tenth_round_question_text.replace(
                            list_1_row4, '')

                        print("list_1_row4:", list_2_question_parts['list_1_row4'])
                        print(
                            f"For question_id {question_id}, question_part_third_part is : {list_2_question_parts['question_part_third_part']}")

                        # End of question processing
                        list_2_question_parts['eleventh_stage_text_to_process'] = ""
                        list_2_question_parts['twelfth_stage_text_to_process'] = ""

                        # Output for verification
                        print("Apparently, the question ends here")
                        input(f"Press Enter to continue processing in tenth Stage.....' ")
                    else:
                        print("No colon found in the text.")


            output_text += "Segment details (tenth Stage):\n"
            output_text += f"list_1_row4: {list_2_question_parts['list_1_row4']}\n"
            output_text += f"eleventh_stage_text_to_process: {list_2_question_parts['eleventh_stage_text_to_process']}\n"

            print("Results of tenth stage processing 10-10-10-10-10-10-10-10-10-10-10-10-10-10-10-10")
            print(f"Results for question_id: '{question_id}'")
            print("list_1_row4:", list_2_question_parts['list_1_row4'])
            print("eleventh_stage_text_to_process:", list_2_question_parts['eleventh_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (tenth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After tenth round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of tenth round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For tenth round processing no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After tenth round processing is complete for all items
    # for assessment of extraction after every round, here after tenth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 10)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_tenth_round")

    # Write to the text file after tenth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after tenth round processing has been updated/ created in the directory: '{base_dir_path}'")

    # eleventh round processing
    # eleventh round processing to look for first instance of "E." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for twelfth round processing
    all_twelfth_stages = []  # To store all twelfth stage texts for round two processing
    # input("Press Enter to continue to eleventh round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            eleventh_round_question_text = entry['eleventh_stage_text_to_process']
            # print(f"For question_id :{question_id}, the eleventh_stage_text_to_process is: {eleventh_round_question_text}")
            # Reset parts at the start of each iteration
            eleventh_round_parts = []
            # Initialize the match object to None
            eleventh_round_match = None
            # defining patterns
            # pattern_to_find_4 = re.compile(r"4(\s{0,2}\.)")
            # pattern_to_find_4 = re.compile(r"\(\s{0,3}4\s{0,3}\)\s{0,2}\.?|4\s{0,2}\.")  # modifying the pattern to handle parentheses also
            # pattern_to_find_E = re.compile(r"E(\s{0,2}\.)")
            pattern_to_find_E = re.compile(
                r"\(\s{0,3}E\s{0,3}\)\s{0,2}\.?|E\s{0,2}\.")  # modifying the pattern to handle parentheses also

            # Initialize or reset the dictionary for each segment
            list_2_question_parts = {
                # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                # 'list_1_present': entry.get('list_1_present', False),
                # 'list_2_present': entry.get('list_2_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_2_name': entry.get('list_2_name', '').strip(),
                # 'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_2_row1': entry.get('list_2_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_2_row2': entry.get('list_2_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_2_row3': entry.get('list_2_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_2_row4': entry.get('list_2_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
                'list_2_row5': entry.get('list_2_row5', '').strip(),
            }

            eleventh_round_question_text = entry[
                'eleventh_stage_text_to_process']  # Access the actual eleventh_round_question_text
            # print(f"For question_id :{question_id}, the eleventh_stage_text_to_process is:{eleventh_round_question_text}")
            output_text = f"For eleventh round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_E: {pattern_to_find_E}\n"

            eleventh_round_match = pattern_to_find_E.search(eleventh_round_question_text)
            if eleventh_round_match:
                # E found, normal flow
                eleventh_round_parts = eleventh_round_question_text.split(eleventh_round_match.group(0), 1)
                # print("eleventh round parts found after splitting:")
                # for idx, part in enumerate(eleventh_round_parts):
                # print(f"Part {idx + 1}: {part.strip()}")
                # Handling the results if parts were successfully created
                if eleventh_round_parts:
                    list_2_question_parts['list_2_row4'] = eleventh_round_parts[0].strip()
                    # print(f"For question_id :{question_id}, list_2_row4 is: {list_2_question_parts['list_2_row4']}")
                    # list_2_question_parts['twelfth_stage_text_to_process'] = eleventh_round_parts[1].strip() if len(parts) > 1 else ""
                    list_2_question_parts['twelfth_stage_text_to_process'] = eleventh_round_parts[1].strip() if len(
                        list_2_question_parts) > 1 else ""
                    # print(f"For question_id :{question_id}, twelfth_stage_text_to_process is: {list_2_question_parts['twelfth_stage_text_to_process']}")

            else:
                # E not found, abnormal flow
                # list_2_question_parts['twelfth_stage_text_to_process'] = eleventh_round_question_text
                print("No match found in eleventh round for pattern_to_find_E.")
                # case of no row E in List I but need to extract list_2_row4 and maybe a row 5 in List II
                print("Proceed to eleventh_round_skip_e_match and find 5.")
                # input("Proceed to eleventh_round_skip_e_match and find 5., Press Enter to continue....")
                # Reset parts at the start of each iteration
                eleventh_round_skip_e_parts = []
                # Initialize the match object to None
                eleventh_round_skip_e_match = None
                pattern_to_find_5 = re.compile(r"5(\s{0,2}\.)")
                eleventh_round_skip_e_match_5 = pattern_to_find_5.search(eleventh_round_question_text)
                if eleventh_round_skip_e_match_5:
                    # case of no row E in List I but a row 5 in List II
                    list_2_question_parts['twelfth_stage_text_to_process'] = ""
                    print(f"eleventh_round_skip_e_match_5: {eleventh_round_skip_e_match_5}")
                    # input(f"eleventh_round_skip_e_match_5: {eleventh_round_skip_e_match_5}, Press Enter to continue....")
                    eleventh_round_skip_e_parts = eleventh_round_question_text.split(eleventh_round_skip_e_match_5.group(0),
                                                                                     1)
                    # print("twelfth round parts found after splitting:")
                    # for idx, part in enumerate(twelfth_round_parts):
                    # print(f"Part {idx + 1}: {part.strip()}")
                    if eleventh_round_skip_e_parts:
                        list_2_question_parts['list_2_row4'] = eleventh_round_skip_e_parts[0].strip()
                        # print(f"For question_id :{question_id}, list_2_row4 is: {list_2_question_parts['list_2_row4']}")
                        # as we are handling the twelfth_stage_text_to_process here itself

                        list_2_question_parts['thirteenth_stage_text_to_process'] = eleventh_round_skip_e_parts[
                            1].strip() if len(
                            parts) > 1 else ""
                        # print(f"For question_id :{question_id}, twelfth_stage_text_to_process is: {list_2_question_parts['twelfth_stage_text_to_process']}")
                        print(
                            f"list_2_row4: {list_2_question_parts['list_2_row4']}, twelfth_stage_text_to_process: {list_2_question_parts['twelfth_stage_text_to_process']}, thirteenth_stage_text_to_process: {list_2_question_parts['thirteenth_stage_text_to_process']},Press Enter to continue....")
                        # input(f"list_2_row4: {list_2_question_parts['list_2_row4']}, twelfth_stage_text_to_process: {list_2_question_parts['twelfth_stage_text_to_process']}, thirteenth_stage_text_to_process: {list_2_question_parts['thirteenth_stage_text_to_process']},Press Enter to continue....")
                    else:
                        # as end of question
                        list_2_question_parts['thirteenth_stage_text_to_process'] = ""
                else:
                    # case of no row E in List I and no row 5 in List II thereby meaning the end of the question
                    # but need to extract list_2_row4
                    print("Proceed to find question_third_part_match and list_2_row4")
                    # input("Proceed to find question_third_part_match and list_2_row4., Press Enter to continue....")
                    # Initialize the match object to None
                    question_third_part_match_in_round_11 = None
                    # pattern_to_find_colon = re.compile(r"^(.*):.*$", re.MULTILINE)
                    # Adjusted pattern to optionally capture content after the colon if it exists
                    # Regex to find the position of the first colon
                    pattern_to_find_colon = re.compile(r":")
                    question_third_part_match_in_round_11 = pattern_to_find_colon.search(eleventh_round_question_text)
                    if question_third_part_match_in_round_11:
                        # Initialise eleventh_round_number_of_lines_before_colon
                        eleventh_round_number_of_lines_before_colon = 0

                        # Position of the first colon
                        eleventh_round_colon_index_ = question_third_part_match_in_round_11.start()

                        # Extract everything before the colon
                        part_before_colon = eleventh_round_question_text[:eleventh_round_colon_index_]
                        # print(f"part_before_colon is: {part_before_colon}")

                        # Extract everything after the colon, including all characters and new lines
                        part_after_colon = eleventh_round_question_text[eleventh_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                        print(f"For question_id: {question_id}, eleventh_round_question_text: {eleventh_round_question_text}")
                        print(
                            f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, eleventh_round_colon_index_ is: {eleventh_round_colon_index_}")

                        # Split the entire text into lines to enable identify the line containing the colon
                        all_lines_eleventh_round = eleventh_round_question_text.split('\n')

                        # Using enumerate() to get both index and find the line index where the colon exists
                        # use of -1 It provides a default value that indicates a colon hasn't been found yet. -1 is often used
                        # in programming to represent an invalid index or a "not found" condition because array indices
                        # in most programming languages start at 0.
                        eleventh_round_colon_line_index = -1
                        for i, line in enumerate(all_lines_eleventh_round):
                            print(f"Line number/ index: {i} is: {line}")
                            if ':' in line:
                                eleventh_round_colon_line_index = i

                        print(f"all_lines_eleventh_round are: {all_lines_eleventh_round}")

                        # Now split 'part_before_colon' into lines
                        eleventh_round_only_lines_before_colon = part_before_colon.split('\n')

                        # Ensure only non-empty lines are kept and strip them
                        eleventh_round_only_lines_before_colon = [line.strip() for line in
                                                                  eleventh_round_only_lines_before_colon if
                                                                  line.strip()]

                        # Use enumerate to loop through each line and its index
                        for index, line_before_colon in enumerate(eleventh_round_only_lines_before_colon):
                            print(f"Only for lines_before_colon, line number {index}: {line_before_colon}")
                        print(f"all lines_before_colon are: {eleventh_round_only_lines_before_colon}")

                        eleventh_round_number_of_lines_before_colon = len(eleventh_round_only_lines_before_colon)
                        print(f"eleventh_round_number_of_lines_before_colon is: {eleventh_round_number_of_lines_before_colon}")

                        # Assign the text from the line before the line containing the colon to 'list_2_row4'
                        list_2_row4 = ""
                        for line in eleventh_round_only_lines_before_colon[:-1]:
                            list_2_row4 += line + "\n"

                        list_2_question_parts['list_2_row4'] = list_2_row4.strip()  # to remove the last newline added from the loop
                        print("Manually concatenated text:", list_2_row4)

                        # Remove the text from 'list_2_row4' from 'eleventh_round_question_text' and assign to 'question_part_third_part'
                        list_2_question_parts['question_part_third_part'] = eleventh_round_question_text.replace(list_2_row4, '')

                        print("list_2_row4:", list_2_question_parts['list_2_row4'])
                        print(f"For question_id {question_id}, question_part_third_part is : {list_2_question_parts['question_part_third_part']}")

                        # as end of question
                        list_2_question_parts['twelfth_stage_text_to_process'] = ""
                        list_2_question_parts['thirteenth_stage_text_to_process'] = ""

                        # Output for verification
                        # print(f"For question_id : {question_id}, Question Part Third Part:, {list_2_question_parts['question_part_third_part']}")
                        print("Apparently, the question ends here")
                        # input(f"Press Enter to continue processing in eleventh Stage.....' ")
                    else:
                        print("No colon found in the text.")

            output_text += "Segment details (eleventh Stage):\n"
            output_text += f"list_1_row4: {list_2_question_parts['list_2_row4']}\n"
            output_text += f"twelfth_stage_text_to_process: {list_2_question_parts['twelfth_stage_text_to_process']}\n"

            print("Results of eleventh stage processing 11-11-11-11-11-11-11-11-11-11-11-11-11-11-11-11")
            print(f"Results for question_id: '{question_id}'")
            print("list_2_row4:", list_2_question_parts['list_2_row4'])
            print("twelfth_stage_text_to_process:", list_2_question_parts['twelfth_stage_text_to_process'])

            num_extracted_fields = 4  # Adjusted for additional field
            performance = num_extracted_fields / 31 * 100
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"For question segment (eleventh Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
            output_text += log_entry
            print(log_entry)
            # After eleventh round, append the processed data back to the original dictionary
            dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

            loop_count = loop_count + 1
            print(f" the loop_count at the end of eleventh round for question_id: {question_id} is :{loop_count}")
            # input("Press Enter to continue...")
        else:
            print(f"For eleventh round processing no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After eleventh round processing is complete for all items
    # for assessment of extraction after every round, here after eleventh round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 11)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_eleventh_round")

    # Write to the text file after eleventh round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after eleventh round processing has been updated/ created in the directory: '{base_dir_path}'")

    # twelfth round processing
    # twelfth round processing will happen only case E is found in Round 11
    # twelfth round processing to look for first instance of "5." and split around the first match
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # also keeping things ready for thirteenth round processing
    all_thirteenth_stages = []  # To store all thirteenth stage texts for round two processing
    # input("Press Enter to continue to twelfth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            twelfth_round_question_text = entry['twelfth_stage_text_to_process']
            if twelfth_round_question_text:
                # print(f"For question_id :{question_id}, the twelfth_stage_text_to_process is: {twelfth_round_question_text}")
                # Reset parts at the start of each iteration
                twelfth_round_parts = []
                # Initialize the match object to None
                twelfth_round_match = None
                # defining patterns
                # pattern_to_find_E = re.compile(r"E(\s{0,2}\.)")
                # pattern_to_find_E = re.compile(r"\(\s{0,3}E\s{0,3}\)\s{0,2}\.?|E\s{0,2}\.")  # modifying the pattern to handle parentheses also
                # pattern_to_find_5 = re.compile(r"5(\s{0,2}\.)")
                pattern_to_find_5 = re.compile(
                    r"\(\s{0,3}5\s{0,3}\)\s{0,2}\.?|5\s{0,2}\.")  # modifying the pattern to handle parentheses also

                # Initialize or reset the dictionary for each segment
                list_2_question_parts = {
                    # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                    # 'list_1_present': entry.get('list_1_present', False),
                    # 'list_2_present': entry.get('list_2_present', False),
                    'list_1_name': entry.get('list_1_name', '').strip(),
                    'list_2_name': entry.get('list_2_name', '').strip(),
                    # 'list_1_entries': entry.get('list_1_entries', []),
                    'list_2_entries': entry.get('list_2_entries', []),
                    # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                    # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                    'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                    'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                    'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                    'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                    'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                    'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                    'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                    'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                    'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                    'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                    'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                    'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                    'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                    'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                    'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                    'list_1_row1': entry.get('list_1_row1', '').strip(),
                    'list_2_row1': entry.get('list_2_row1', '').strip(),
                    'list_1_row2': entry.get('list_1_row2', '').strip(),
                    'list_2_row2': entry.get('list_2_row2', '').strip(),
                    'list_1_row3': entry.get('list_1_row3', '').strip(),
                    'list_2_row3': entry.get('list_2_row3', '').strip(),
                    'list_1_row4': entry.get('list_1_row4', '').strip(),
                    'list_2_row4': entry.get('list_2_row4', '').strip(),
                    'list_1_row5': entry.get('list_1_row5', '').strip(),
                    'list_2_row5': entry.get('list_2_row5', '').strip(),
                }

                twelfth_round_question_text = entry[
                    'twelfth_stage_text_to_process']  # Access the actual twelfth_round_question_text
                # print(f"For question_id :{question_id}, the twelfth_stage_text_to_process is:{twelfth_round_question_text}")
                output_text = f"For twelfth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_5: {pattern_to_find_5}\n"
                twelfth_round_match = pattern_to_find_5.search(twelfth_round_question_text)
                if twelfth_round_match:
                    twelfth_round_parts = twelfth_round_question_text.split(twelfth_round_match.group(0), 1)
                    # print("twelfth round parts found after splitting:")
                    # for idx, part in enumerate(twelfth_round_parts):
                    # print(f"Part {idx + 1}: {part.strip()}")
                    if twelfth_round_parts:
                        # Handling the results if parts were successfully created
                        list_2_question_parts['list_1_row5'] = twelfth_round_parts[0].strip()
                        # print(f"For question_id :{question_id}, list_1_row5 is: {list_2_question_parts['list_1_row5']}")
                        list_2_question_parts['thirteenth_stage_text_to_process'] = twelfth_round_parts[1].strip() if len(
                            list_2_question_parts) > 1 else ""
                        # print(f"For question_id :{question_id}, thirteenth_stage_text_to_process is: {list_2_question_parts['thirteenth_stage_text_to_process']}")

                    else:
                        list_2_question_parts['thirteenth_stage_text_to_process'] = twelfth_round_question_text
                else:
                    # possible case of no row 5 in List II
                    print("No match found in twelfth round for pattern_to_find_5.")
                    print("Apparently, the question ends here, extracting question_third_part_match")
                    # Initialize the match object to None
                    question_third_part_match_in_round_12 = None
                    # pattern_to_find_colon = re.compile(r"^(.*):\s*$")
                    # Adjusted pattern to optionally capture content after the colon if it exists
                    # Regex to find the position of the first colon
                    # Regex to find the position of the first colon
                    pattern_to_find_colon = re.compile(r":")
                    question_third_part_match_in_round_12 = pattern_to_find_colon.search(twelfth_round_question_text)
                    if question_third_part_match_in_round_12:
                        # Initialize twelfth_round_number_of_lines_before_colon
                        twelfth_round_number_of_lines_before_colon = 0

                        # Position of the first colon
                        twelfth_round_colon_index_ = question_third_part_match_in_round_12.start()

                        # Extract everything before the colon
                        part_before_colon = twelfth_round_question_text[:twelfth_round_colon_index_]
                        # Extract everything after the colon, including all characters and new lines
                        part_after_colon = twelfth_round_question_text[
                                           twelfth_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                        print(
                            f"For question_id: {question_id}, twelfth_round_question_text: {twelfth_round_question_text}")
                        print(
                            f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, twelfth_round_colon_index_ is: {twelfth_round_colon_index_}")

                        # Split the entire text into lines to enable identifying the line containing the colon
                        all_lines_twelfth_round = twelfth_round_question_text.split('\n')

                        # Use enumerate to find the line index where the colon exists
                        twelfth_round_colon_line_index = -1
                        for i, line in enumerate(all_lines_twelfth_round):
                            print(f"Line number/ index: {i} is: {line}")
                            if ':' in line:
                                twelfth_round_colon_line_index = i

                        print(f"all_lines_twelfth_round are: {all_lines_twelfth_round}")

                        # Now split 'part_before_colon' into lines
                        twelfth_round_only_lines_before_colon = part_before_colon.split('\n')

                        # Ensure only non-empty lines are kept and strip them
                        twelfth_round_only_lines_before_colon = [line.strip() for line in
                                                                 twelfth_round_only_lines_before_colon if
                                                                 line.strip()]

                        # Use enumerate to loop through each line and its index
                        for index, line_before_colon in enumerate(twelfth_round_only_lines_before_colon):
                            print(f"Only for lines_before_colon, line number {index}: {line_before_colon}")
                        print(f"all lines_before_colon are: {twelfth_round_only_lines_before_colon}")

                        twelfth_round_number_of_lines_before_colon = len(twelfth_round_only_lines_before_colon)
                        print(
                            f"twelfth_round_number_of_lines_before_colon is: {twelfth_round_number_of_lines_before_colon}")

                        # Assign the text from the line before the line containing the colon to 'list_1_row5'
                        list_1_row5 = ""
                        for line in twelfth_round_only_lines_before_colon[:-1]:
                            list_1_row5 += line + "\n"
                        list_2_question_parts[
                            'list_1_row5'] = list_1_row5.strip()  # to remove the last newline added from the loop
                        print("Manually concatenated text:", list_1_row5)

                        # Remove the text from 'list_1_row5' from 'twelfth_round_question_text' and assign to 'question_part_third_part'
                        list_2_question_parts['question_part_third_part'] = twelfth_round_question_text.replace(
                            list_1_row5, '')

                        print("list_1_row5:", list_2_question_parts['list_1_row5'])
                        print(
                            f"For question_id {question_id}, question_part_third_part is : {list_2_question_parts['question_part_third_part']}")

                        # End of question processing
                        list_2_question_parts['thirteenth_stage_text_to_process'] = ""
                        list_2_question_parts['fourteenth_stage_text_to_process'] = ""

                        # Output for verification
                        print("Apparently, the question ends here")
                        input(f"Press Enter to continue processing in twelfth Stage.....' ")
                    else:
                        print("No colon found in the text.")

                output_text += "Segment details (twelfth Stage):\n"
                output_text += f"list_1_row5: {list_2_question_parts['list_1_row5']}\n"
                output_text += f"thirteenth_stage_text_to_process: {list_2_question_parts['thirteenth_stage_text_to_process']}\n"

                print("Results of twelfth stage processing 12-12-12-12-12-12-12-12-12-12-12-12-12-12-12-12")
                print(f"Results for question_id: '{question_id}'")
                print("list_1_row5:", list_2_question_parts['list_1_row5'])
                print("thirteenth_stage_text_to_process:", list_2_question_parts['thirteenth_stage_text_to_process'])

                num_extracted_fields = 4  # Adjusted for additional field
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment (twelfth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
                # After twelfth round, append the processed data back to the original dictionary
                dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

                loop_count = loop_count + 1
                print(f" the loop_count at the end of twelfth round for question_id: {question_id} is :{loop_count}")
                # input("Press Enter to continue...")
            else:
                print(f"The twelfth_stage_text_to_process to is blank or: ' {twelfth_round_question_text} '")
                print("Apparently, the question ends here")
        else:
            print(f"For twelfth round processing, no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After twelfth round processing is complete for all items
    # for assessment of extraction after every round, here after twelfth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 12)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_twelfth_round")

    # Write to the text file after twelfth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    with open(recording_text_file_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{recording_text_file_path}'after twelfth round processing has been updated/ created in the directory: '{base_dir_path}'")

    # thirteenth round processing
    # thirteenth round processing to look for question_part_third_part
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # input("Press Enter to continue to thirteenth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            thirteenth_round_question_text = entry['thirteenth_stage_text_to_process']
            print(
                f"For question_id : {question_id}, the thirteenth_round_question_text is: {thirteenth_round_question_text}")
            # input()
            if thirteenth_round_question_text:
                thirteenth_round_question_text = entry['thirteenth_stage_text_to_process']
                print(
                    f"For question_id : {question_id}, the thirteenth_round_question_text is: {thirteenth_round_question_text}")
                # input()
                # Initialize or reset the dictionary for each segment
                list_2_question_parts = {
                    # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                    # 'list_1_present': entry.get('list_1_present', False),
                    # 'list_2_present': entry.get('list_2_present', False),
                    'list_1_name': entry.get('list_1_name', '').strip(),
                    'list_2_name': entry.get('list_2_name', '').strip(),
                    # 'list_1_entries': entry.get('list_1_entries', []),
                    'list_2_entries': entry.get('list_2_entries', []),
                    # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                    # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                    'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                    'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                    'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                    'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                    'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                    'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                    'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                    'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                    'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                    'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                    'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                    'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                    'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                    'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                    'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                    'list_1_row1': entry.get('list_1_row1', '').strip(),
                    'list_2_row1': entry.get('list_2_row1', '').strip(),
                    'list_1_row2': entry.get('list_1_row2', '').strip(),
                    'list_2_row2': entry.get('list_2_row2', '').strip(),
                    'list_1_row3': entry.get('list_1_row3', '').strip(),
                    'list_2_row3': entry.get('list_2_row3', '').strip(),
                    'list_1_row4': entry.get('list_1_row4', '').strip(),
                    'list_2_row4': entry.get('list_2_row4', '').strip(),
                    'list_1_row5': entry.get('list_1_row5', '').strip(),
                    'list_2_row5': entry.get('list_2_row5', '').strip(),
                }

                output_text = f"For thirteenth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_colon: {pattern_to_find_colon}\n"
                # print(f"For question_id :{question_id}, the thirteenth_stage_text_to_process is: {thirteenth_round_question_text}")
                # Initialize the match object to None
                question_third_part_match_in_round_13 = None
                # pattern_to_find_colon = re.compile(r"^(.*):.*$", re.MULTILINE)
                # Adjusted pattern to optionally capture content after the colon if it exists
                # pattern_to_find_colon = re.compile(r"^(.*?):(.*?)$", re.MULTILINE)
                # Regex to find the position of the first colon
                pattern_to_find_colon = re.compile(r":")
                # Search for the pattern in the question text
                question_third_part_match_in_round_13 = pattern_to_find_colon.search(thirteenth_round_question_text)
                if question_third_part_match_in_round_13:
                    # Initialize thirteenth_round_number_of_lines_before_colon
                    thirteenth_round_number_of_lines_before_colon = 0

                    # Position of the first colon
                    thirteenth_round_colon_index_ = question_third_part_match_in_round_13.start()

                    # Extract everything before the colon
                    part_before_colon = thirteenth_round_question_text[:thirteenth_round_colon_index_]
                    # Extract everything after the colon, including all characters and new lines
                    part_after_colon = thirteenth_round_question_text[
                                       thirteenth_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                    print(
                        f"For question_id: {question_id}, thirteenth_round_question_text: {thirteenth_round_question_text}")
                    print(
                        f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, thirteenth_round_colon_index_ is: {thirteenth_round_colon_index_}")

                    # Split the entire text into lines to enable identifying the line containing the colon
                    all_lines_thirteenth_round = thirteenth_round_question_text.split('\n')

                    # Use enumerate to find the line index where the colon exists
                    thirteenth_round_colon_line_index = -1
                    for i, line in enumerate(all_lines_thirteenth_round):
                        print(f"Line number/ index: {i} is: {line}")
                        if ':' in line:
                            thirteenth_round_colon_line_index = i

                    print(f"all_lines_thirteenth_round are: {all_lines_thirteenth_round}")

                    # Now split 'part_before_colon' into lines
                    thirteenth_round_only_lines_before_colon = part_before_colon.split('\n')

                    # Ensure only non-empty lines are kept and strip them
                    thirteenth_round_only_lines_before_colon = [line.strip() for line in
                                                                thirteenth_round_only_lines_before_colon if
                                                                line.strip()]

                    # Use enumerate to loop through each line and its index
                    for index, line_before_colon in enumerate(thirteenth_round_only_lines_before_colon):
                        print(f"Only for lines_before_colon, line number {index}: {line_before_colon}")
                    print(f"all lines_before_colon are: {thirteenth_round_only_lines_before_colon}")

                    thirteenth_round_number_of_lines_before_colon = len(thirteenth_round_only_lines_before_colon)
                    print(
                        f"thirteenth_round_number_of_lines_before_colon is: {thirteenth_round_number_of_lines_before_colon}")

                    # Assign the text from the line before the line containing the colon to 'list_2_row5'
                    list_2_row5 = ""
                    for line in thirteenth_round_only_lines_before_colon[:-1]:
                        list_2_row5 += line + "\n"
                    list_2_question_parts[
                        'list_2_row5'] = list_2_row5.strip()  # to remove the last newline added from the loop
                    print("Manually concatenated text:", list_2_row5)

                    # Remove the text from 'list_2_row5' from 'thirteenth_round_question_text' and assign to 'question_part_third_part'
                    list_2_question_parts['question_part_third_part'] = thirteenth_round_question_text.replace(
                        list_2_row5, '')

                    print("list_2_row5:", list_2_question_parts['list_2_row5'])
                    print(
                        f"For question_id {question_id}, question_part_third_part is : {list_2_question_parts['question_part_third_part']}")

                    # End of question processing
                    list_2_question_parts['fourteenth_stage_text_to_process'] = ""
                    list_2_question_parts['fifteenth_stage_text_to_process'] = ""

                    # Output for verification
                    print("Apparently, the question ends here")
                    # input(f"Press Enter to continue processing in thirteenth Stage.....' ")

                else:
                    print("No match found in thirteenth round for pattern_to_find_colon.")
                    continue  # Skip to the next iteration if no match is found

                # Output for verification
                print("List 2 Row 5:", list_2_question_parts.get('list_2_row5', 'Not found'))
                print("Question Part Third Part:", list_2_question_parts['question_part_third_part'])
                print("Apparently, the question ends here")
                output_text += "Segment details (thirteenth Stage):\n"
                output_text += f"question_part_third_part: {list_2_question_parts['question_part_third_part']}\n"

                print("Results of thirteenth stage processing 13-13-13-13-13-13-13-13-13-13-13-13-13-13-13-13")
                print(f"Results for question_id: '{question_id}'")
                print("Question Part Third Part:", list_2_question_parts['question_part_third_part'])
                print("Apparently, the question ends here")

                num_extracted_fields = 4  # Adjusted for additional field
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment (tenth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
                # After tenth round, append the processed data back to the original dictionary
                dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

                # create formatted text file from dictionary
                # base_dir_path = Path("C:/Users/PRATIK HAJELA/Desktop/Question Bank Trials/Python Programming/Trials/Regex Trials/Hindi Trials")
                file_name = "temp_question_parts_hindi_also"  # Assuming this is the name of your Python file without the .py extension
                loaded_dict = load_dictionary(file_name,
                                              base_dir_path)  # Ensure load_dictionary function is correctly implemented and used
                create_formatted_text_from_dictionary(loaded_dict, file_name, base_dir_path)

                loop_count = loop_count + 1
                print(f" the loop_count at the end of tenth round for question_id: {question_id} is :{loop_count}")
                # input("Press Enter to continue...")

            else:

                print(f"There is no thirteenth_round_question_text or it is: ' {thirteenth_round_question_text} '")
        else:
            print(f"For thirteenth round no question_sub_type of list_2 type found, Press Enter to continue.............")

    # After thirteenth round processing is complete for all items
    # for assessment of extraction after every round, here after thirteenth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 13)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_thirteenth_round")

    # fourteenth round processing
    # fourteenth round processing to look add spaces in question_third_part
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # input("Press Enter to continue to fourteenth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            fourteenth_round_question_text = entry['question_part_third_part']
            print(
                f"For question_id : {question_id}, the fourteenth_round_question_text is: {fourteenth_round_question_text}")
            # input()
            if fourteenth_round_question_text:
                print(f"For question_id : {question_id}, the the fourteenth_round_question_text is: {fourteenth_round_question_text}")
                # input()
                # Initialize or reset the dictionary for each segment
                list_2_question_parts = {
                    # 'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                    # 'list_1_present': entry.get('list_1_present', False),
                    # 'list_2_present': entry.get('list_2_present', False),
                    'list_1_name': entry.get('list_1_name', '').strip(),
                    'list_2_name': entry.get('list_2_name', '').strip(),
                    # 'list_1_entries': entry.get('list_1_entries', []),
                    'list_2_entries': entry.get('list_2_entries', []),
                    # 'part_before_list_2': entry.get('part_before_list_2', '').strip(),
                    # 'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                    'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                    'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                    'question_part_third_part_1': entry.get('question_part_third_part_1', '').strip(),
                    'question_part_third_part_2': entry.get('question_part_third_part_2', '').strip(),
                    'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                    'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                    'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                    'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                    'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                    'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                    'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                    'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                    'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                    'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                    'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                    'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                    'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                    'list_1_row1': entry.get('list_1_row1', '').strip(),
                    'list_2_row1': entry.get('list_2_row1', '').strip(),
                    'list_1_row2': entry.get('list_1_row2', '').strip(),
                    'list_2_row2': entry.get('list_2_row2', '').strip(),
                    'list_1_row3': entry.get('list_1_row3', '').strip(),
                    'list_2_row3': entry.get('list_2_row3', '').strip(),
                    'list_1_row4': entry.get('list_1_row4', '').strip(),
                    'list_2_row4': entry.get('list_2_row4', '').strip(),
                    'list_1_row5': entry.get('list_1_row5', '').strip(),
                    'list_2_row5': entry.get('list_2_row5', '').strip(),
                }

                # Initialize the match object to None
                question_third_part_match_in_round_14 = None
                # pattern_to_find_colon = re.compile(r"^(.*):.*$", re.MULTILINE)
                # Adjusted pattern to optionally capture content after the colon if it exists
                # pattern_to_find_colon = re.compile(r"^(.*?):(.*?)$", re.MULTILINE)
                pattern_to_find_colon = re.compile(r":")
                # print(f"For question_id :{question_id}, the fourteenth_round_question_text_to_process is:{fourteenth_round_question_text}")
                output_text = f"For fourteenth round processing and loop_count {loop_count}, using regex pattern for pattern_to_find_colon: {pattern_to_find_colon}\n"
                initial_question_part_third_part = list_2_question_parts['question_part_third_part']
                print(f"For fourteenth round processing for question_id: {question_id}, question_part_third_part is: {initial_question_part_third_part}")
                # matches_for_question_third_part_match_in_round_14 = list(pattern_to_find_colon.finditer(fourteenth_round_question_text))
                question_third_part_match_in_round_14 = pattern_to_find_colon.search(fourteenth_round_question_text)
                if question_third_part_match_in_round_14:
                    # Initialize fourteenth_round_number_of_lines_before_colon
                    fourteenth_round_number_of_lines_before_colon = 0

                    # Position of the first colon
                    fourteenth_round_colon_index_ = question_third_part_match_in_round_14.start()

                    # Extract everything before the colon
                    part_before_colon = fourteenth_round_question_text[:fourteenth_round_colon_index_]
                    # Extract everything after the colon, including all characters and new lines
                    part_after_colon = fourteenth_round_question_text[
                                       fourteenth_round_colon_index_ + 1:]  # '+1' to skip the colon itself

                    print(
                        f"For question_id: {question_id}, fourteenth_round_question_text: {fourteenth_round_question_text}")
                    print(
                        f"For question_id: {question_id}, part_before_colon is: {part_before_colon}, part_after_colon is: {part_after_colon}, fourteenthh_round_colon_index_ is: {fourteenth_round_colon_index_}")

                    revised_part_after_colon = add_spaces_and_count_spaces(part_after_colon, "add_space")
                    # Combine parts with the colon for 'question_part_third_part' and correctly format the final string
                    list_2_question_parts['question_part_third_part'] = f"{part_before_colon}:\n{revised_part_after_colon}"


                # After fourteenth round, append the processed data back to the original dictionary
                dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

                # input(f"Check the dictionary contents and press Enter to continue....")

                # adding to output text for creating text file of assessment record
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                output_text += f"\n"
                output_text += f"Date and Time of processing is: {current_time}\n"
                output_text += f"\n"
                output_text += f"question_id {question_id} details:\n"
                output_text += f"\n"
                output_text += f"Pattern used is pattern 1 i.e {pattern_to_find_colon}\n"
                output_text += f"Question part third part initially was: {initial_question_part_third_part}\n"
                output_text += f"After adding spaces, the revised question_part_third_part: {list_2_question_parts['question_part_third_part']}\n\n"
                output_text += f"\n"
                output_text += f"--------\n"
                print("Results of fourteenth stage processing 14-14-14-14-14-14-14-14-14-14-14-14-14-14-14-14")
                print(f"Results for question_id: '{question_id}'")
                print("Question Part Third Part:", list_2_question_parts['question_part_third_part'])

                num_extracted_fields = 4  # Adjusted for additional field
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment (fourteenth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
                print(output_text)
                # input("Are you satisfied with the fourteenth round, Press Enter to continue.....")
            else:

                print(f"No Question Part Third Part, Press Enter to continue.............")


    # After fourteenth round processing is complete for all items
    # for assessment of extraction after every round, here after fourteenth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 14)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_fourteenth_round")

    # Creating a .py file for the data_dict after the fourteenth round
    # Name of the dictionary variable in the .py file
    # Filename for the Python file, ensuring it ends with .py
    dict_name = f"list_2_temp_question_parts_{temp_dict_name}.py"
    # Full path including the filename
    file_path = base_dir_path / dict_name
    # Call the function to write the dictionary to a Python file
    # write_dictionary(dynamic_dict_name_list_2_parts, file_path, dict_name)

    # Write to the text file after fourteenth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    # After fourteenth round processing is complete for all items

    print("Writing to file:", output_text)
    recording_text_file_path = recording_text_file_path.with_suffix(
        '.txt')  # Ensure the file has a .txt extension

    # Open the existing file in read mode and read its contents, no longer using 'a' for appending
    # Before attempting to read the file, check if it exists
    # Check if the file exists
    if recording_text_file_path.exists():
        # Read existing contents if the file exists
        with open(recording_text_file_path, 'r', encoding='utf-8') as file:
            existing_contents = file.read()
        # Write the new text followed by the existing contents
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text + existing_contents)
    else:
        # If the file does not exist, just create it and write the new text
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

    print(output_text)

    # fifteenth round processing
    # fifteenth round processing to look add spaces in answer options
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_2_parts)
    # print(data_dict_copy)
    # input(f"Please see above the contents of the dictionary data_dict_copy, Press Enter to continue....")
    input("Press Enter to continue to fifteenth round processing...")
    loop_count = 1
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_2":
            output_text = ''
            # fifteenth_round_answer = entry['answer_part']
            fifteenth_round_answer = entry['answer']
            initial_fifteenth_round_answer = fifteenth_round_answer
            print(f"For question_id : {question_id}, the fifteenth_round_answer is: {fifteenth_round_answer}")
            # input()
            if fifteenth_round_answer:
                # Initialize or reset the dictionary for each segment
                list_2_question_parts = {
                    'question': entry.get('question', '').strip(),
                    'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                    'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                    'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                    "answer": entry.get('answer_part', '').strip(),
                    "answer_option_a": entry.get('answer_option_a', '').strip(),
                    "answer_option_b": entry.get('answer_option_b', '').strip(),
                    "answer_option_c": entry.get('answer_option_c', '').strip(),
                    "answer_option_d": entry.get('answer_option_d', '').strip(),

                }

                # Initialize the temp_answer_options_list and answer_options_complete
                temp_answer_options_list = []
                answer_options_complete = False

                # Creating the list of answer options
                temp_answer_options_list = [
                    list_2_question_parts['answer_option_a'],
                    list_2_question_parts['answer_option_b'],
                    list_2_question_parts['answer_option_c'],
                    list_2_question_parts['answer_option_d']
                ]

                # Printing the list to verify its contents
                print(temp_answer_options_list)

                # Creating a list that checks if each answer option is not blank
                check_system_for_temp_answer_options_list = [
                    1 if list_2_question_parts[f'answer_option_{option}'].strip() else 0 for option in
                    ['a', 'b', 'c', 'd']
                ]

                # Printing the list to verify its contents
                print(check_system_for_temp_answer_options_list)

                # Checking if all values are 1 in check_system_for_temp_answer_options_list
                answer_options_complete = all(value == 1 for value in check_system_for_temp_answer_options_list)

                # Printing the result to verify
                print("Answer options complete:", answer_options_complete)

                # if not answer_options_complete:
                # Create a report for each answer option including the content and space counts
                # Create a report for each answer option including the content and space counts
                report = []
                for option_label in ['a', 'b', 'c', 'd']:
                    option_content = list_2_question_parts[f'answer_option_{option_label}']
                    if option_content:  # Only process non-empty options
                        initial_space_counts = add_spaces_and_count_spaces(option_content, "count_spaces")
                        report.append((f"Before adding spaces, answer_option_{option_label}", option_content, initial_space_counts))
                        print(f"Before adding spaces, answer_option_{option_label}", option_content, initial_space_counts)

                        # Update the option content in the dictionary after adding spaces
                        list_2_question_parts[f'answer_option_{option_label}'] = add_spaces_and_count_spaces(option_content, "add_space")

                        # Recalculate space counts after spaces are added
                        revised_space_counts = add_spaces_and_count_spaces(
                            list_2_question_parts[f'answer_option_{option_label}'], "count_spaces")
                        report.append((f"After adding spaces, answer_option_{option_label}", list_2_question_parts[f'answer_option_{option_label}'], revised_space_counts))
                        print(f"After adding spaces, answer_option_{option_label}", list_2_question_parts[f'answer_option_{option_label}'], revised_space_counts)
                    else:
                        report.append((f"answer_option_{option_label}", "Blank option", []))
                        print(f"answer_option_{option_label}", "Blank option", [])

                # Print the report
                for item in report:
                    print(f"For question_id:{question_id}, {item[0]}, {item[1]}, {' '.join(map(str, item[2])) if item[2] else 'No spaces'}")

                # Just for printing the revised fields for output verification
                for option_label in ['a', 'b', 'c', 'd']:
                    revised_option_content = list_2_question_parts[f'answer_option_{option_label}']
                    if revised_option_content:  # Only process non-empty options
                        print(f"For question_id: {question_id}, initial_fifteenth_round_answer: {initial_fifteenth_round_answer}")
                        print(f"For question_id: {question_id}, after processing, list_2_question_parts['answer_option_{option_label}'] is: {list_2_question_parts[f'answer_option_{option_label}']}")


                # input(f"For question_id:{question_id}, Please check the above and Press Enter to continue......")

                # revised_part_after_colon = add_spaces_and_count_spaces(part_after_colon)
                # Combine parts with the colon for 'question_part_third_part' and correctly format the final string
                # list_2_question_parts['question_part_third_part'] = f"{part_before_colon}:\n{revised_part_after_colon}"

                # After fifteenth round, append the processed data back to the original dictionary
                dynamic_dict_name_list_2_parts[question_id].update(list_2_question_parts)

                # input(f"Check the dictionary contents after processing in fifiteenth round and press Enter to continue....")

                # adding to output text for creating text file of assessment record
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                output_text += f"\n"
                output_text += f"Date and Time of processing is: {current_time}\n"
                output_text += f"\n"
                output_text += f"question_id {question_id} details:\n"
                output_text += f"\n"
                # output_text += f"Answer part third part initially was: {initial_question_part_third_part}\n"
                # output_text += f"After adding spaces, the revised question_part_third_part: {list_2_question_parts['question_part_third_part']}\n\n"
                output_text += f"\n"
                output_text += f"--------\n"
                print("Results of fifteenth stage processing 15-15-15-15-15-15-15-15-15-15-15-15-15-15-15-15")
                print(f"Results for question_id: '{question_id}'")
                # print("Question Part Third Part:", list_2_question_parts['question_part_third_part'])

                num_extracted_fields = 4  # Adjusted for additional field
                performance = num_extracted_fields / 31 * 100
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"For question segment (fifteenth Round Stage), {num_extracted_fields} fields extracted out of 18 which is {performance:.2f}% - {current_time}\n"
                output_text += log_entry
                print(log_entry)
                print(output_text)
                # input("Are you satisfied with the fifteenth round, Press Enter to continue.....")
            else:

                print(f"No Question Part Third Part, Press Enter to continue.............")

    # After fifteenth round processing is complete for all items
    # for assessment of extraction after every round, here after fifteenth round
    assess_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, performance_excel_file_path)
    create_excel_for_list_2_parts_extraction_performance(dynamic_dict_name_list_2_parts, base_dir_path, 15)
    create_excel_for_dict(dynamic_dict_name_list_2_parts, base_dir_path, f"{temp_dict_name}_fifteenth_round")

    # Creating a .py file for the data_dict after the fifteenth round
    # Name of the dictionary variable in the .py file
    # Filename for the Python file, ensuring it ends with .py
    dict_name = f"list_2_temp_question_parts_{temp_dict_name}.py"
    # Full path including the filename
    file_path = base_dir_path / dict_name
    # Call the function to write the dictionary to a Python file
    write_dictionary(dynamic_dict_name_list_2_parts, file_path, dict_name)

    # Split the temp_dict_name to generate the new_final_dict_name
    parts = temp_dict_name.split('_')
    new_final_dict_name = '_'.join(parts[:-8]) + "_questions_extraction_completed_dictionary"
    new_dict_file_name = f"{new_final_dict_name}.py"

    # Assuming the new dictionary to be created is empty for now, you can modify as needed
    # new_final_dict = {}
    # Copy contents to the new dictionary
    new_final_dict = dict(dynamic_dict_name_list_2_parts)  # Copying the contents

    # Full path including the filename
    new_file_path = base_dir_path / new_dict_file_name

    # Write the new dictionary to a Python file
    write_dictionary(new_final_dict, new_file_path, new_final_dict_name)
    create_excel_for_dict(new_final_dict, base_dir_path, f"{new_final_dict_name}")

    # Write to the text file after fifteenth round processing is complete
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    # After fifteenth round processing is complete for all items

    print("Writing to file:", output_text)
    recording_text_file_path = recording_text_file_path.with_suffix(
        '.txt')  # Ensure the file has a .txt extension

    # Open the existing file in read mode and read its contents, no longer using 'a' for appending
    # Before attempting to read the file, check if it exists
    # Check if the file exists
    if recording_text_file_path.exists():
        # Read existing contents if the file exists
        with open(recording_text_file_path, 'r', encoding='utf-8') as file:
            existing_contents = file.read()
        # Write the new text followed by the existing contents
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text + existing_contents)
    else:
        # If the file does not exist, just create it and write the new text
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

    print(output_text)

    # If you need to return or use this updated dictionary:
    # return data_dict
    return dynamic_dict_name_list_2_parts, new_final_dict

# this function will check in list_type_1 questions whether a question is complete from the point of view
# of any empty list_1_row
def is_question_complete(data_dict, question_id):
    # Retrieve the specific question dictionary using the question_id
    question_data = data_dict.get(question_id)

    # If the question_id is not found, assume it is not complete
    if question_data is None:
        return False  # Corrected to return False because there's no data to check

    # Initialize question_complete to False at the beginning of the check
    question_data['question_complete'] = False  # Set to False initially

    # Get the maximum row number for list1
    max_row = question_data.get('question_part_list1_max_row', 0)
    temp_list_for_question_complete = []

    # Check if each list_1_row{i} from 1 to max_row is not empty
    for i in range(1, max_row + 1):
        row_key = f'list_1_row{i}'
        row_content = question_data.get(row_key, "")  # Get the content of the row, defaulting to an empty string
        if row_content:
            temp_list_for_question_complete.append(1)  # Append 1 if the row is not empty
        else:
            temp_list_for_question_complete.append(0)  # Append 0 if the row is empty

    # Check if there are any 0s in the list, indicating incomplete fields
    if 0 in temp_list_for_question_complete:
        question_data['question_complete'] = False
    else:
        question_data['question_complete'] = True

    return question_data['question_complete']



# the function extract_list_1_parts uses a slightly more innovative method as compared to the simplistic and long
# method used for extract_list_2_parts. this function extract_list_1_parts carries out 3 rounds of processing using three different
# patterns. these 3 patterns cover the entire (almost) range of requirements arising from the various samples
# like 1-5A-E. 1. with 0 to 3 whitespaces or # and (1-5A-E) or (1-5A-EA.) with 0 to 3 whitespaces
def extract_list_1_parts(input_data_dict, temp_dict_name, base_dir_path):
# def extract_list_1_parts(question_text):

    # Ensure the directory exists
    base_dir_path.mkdir(parents=True, exist_ok=True)

    # print(f"the question_text parsed is :'{question_text}")

    # Create a dynamically named dictionary
    # dynamic_dict_name = f"list_1_temp_question_parts_{temp_dict_name}"
    dynamic_dict_name_list_1_parts = f"list_1_temp_question_parts_{temp_dict_name}"

    # Initialize dictionary
    dynamic_dict_name_list_1_parts = {}
    dynamic_dict_name_list_1_parts_file_path = base_dir_path / f"list_1_temp_question_parts_{temp_dict_name}"

    # dynamic_question_parts = {}
    # dynamic_dict_name = {}

    dict_excel_name = f"list_1_temp_question_parts_{temp_dict_name}"
    dict_excel_file_path = base_dir_path / dict_excel_name

    performance_excel_name = f"list_1_performance_excel_{temp_dict_name}"
    performance_excel_file_path = base_dir_path / performance_excel_name

    recording_text_file_name = f"list_1_temp_question_parts_{temp_dict_name}"
    recording_text_file_path = base_dir_path / recording_text_file_name

    # Regular expression pattern to match separators
    # separator_pattern = r"\n\s*-{10,}\s*\n"

    # Split the text into parts using the separator pattern
    # parts = re.split(separator_pattern, question_text)

    # print(f"the question_text parsed is :'{question_text}")
    # input("Press Enter to continue create temporary dictionary for list1 parts...")

    # Initialize dictionary to store question parts
    # list_1_temp_question_parts_hindi_also = {}
    # list_1_temp_question_parts = {}
    # Initialize dictionary to store all dynamically named question parts dictionaries
    # all_question_parts = {}

    # Regular expression pattern to match separators
    # separator_pattern = r"\n\s*-{10,}\s*\n"

    # Split the text into parts using the separator pattern
    # parts = re.split(separator_pattern, question_text)

    # Assume data_dict structure is known and each entry contains keys like 'question_type', 'question_sub_type', etc.
    for question_id, info in input_data_dict.items():
        # Copy all existing fields
        dynamic_dict_name_list_1_parts[question_id] = info.copy()
        # Initial dictionary setup for each question
        # Now add or modify specific fields
        dynamic_dict_name_list_1_parts[question_id].update({
            'list_1_row1': info.get('list_1_row1', '').strip(),
            'list_1_row2': info.get('list_1_row2', '').strip(),
            'list_1_row3': info.get('list_1_row3', '').strip(),
            'list_1_row4': info.get('list_1_row4', '').strip(),
            'list_1_row5': info.get('list_1_row5', '').strip(),
            'question_part_list1_max_row': info.get('question_part_list1_max_row', 0),
            'question_complete': info.get('question_complete', False),
            'list_1_entries': info.get('list_1_entries', []),
            'second_stage_text_to_process': info.get('second_stage_text_to_process', ''),
            'third_stage_text_to_process': info.get('third_stage_text_to_process', ''),
            'fourth_stage_text_to_process': info.get('fourth_stage_text_to_process', ''),
            'fifth_stage_text_to_process': info.get('fifth_stage_text_to_process', ''),
            'sixth_stage_text_to_process': info.get('sixth_stage_text_to_process', ''),
            'seventh_stage_text_to_process': info.get('seventh_stage_text_to_process', ''),
            'eighth_stage_text_to_process': info.get('eighth_stage_text_to_process', ''),
            'ninth_stage_text_to_process': info.get('ninth_stage_text_to_process', ''),
            'tenth_stage_text_to_process': info.get('tenth_stage_text_to_process', ''),
            'eleventh_stage_text_to_process': info.get('eleventh_stage_text_to_process', ''),
            'twelfth_stage_text_to_process': info.get('twelfth_stage_text_to_process', ''),
            'thirteenth_stage_text_to_process': info.get('thirteenth_stage_text_to_process', ''),
            'fourteenth_stage_text_to_process': info.get('fourteenth_stage_text_to_process', ''),
            'fifteenth_stage_text_to_process': info.get('fifteenth_stage_text_to_process', ''),
            'sixteenth_stage_text_to_process': info.get('sixteenth_stage_text_to_process', ''),
        })

    # print(f"Temporary dictionary {dynamic_dict_name_list_1_parts} has been created based on the temp_dict_name : '{temp_dict_name}' 'passed as parameter.")

    # Filter out empty parts and create a dictionary
    # list_1_temp_question_parts_hindi_also = {f"question_id_{idx}": {'question_part': part.strip()} for idx, part in
    #                                         enumerate(parts) if
    #                                         part.strip()}

    # Adding additional fields to each item in the dictionary
    """for item in list_1_temp_question_parts_hindi_also.values():
        item.update({
            'question_type': 'list_type',
            'question_sub_type': 'list_type_1',
            'question_part_list1_max_row': 0,
            'question_complete': False,
            'question_part_first_part': '',
            'list_1_row1': '',
            'list_1_row2': '',
            'list_1_row3': '',
            'list_1_row4': '',
            'list_1_row5': '',
            'question_part_third_part': '',
            'list_1_entries': [],
            'second_stage_text_to_process': '',
            'third_stage_text_to_process': '',
            'fourth_stage_text_to_process': '',
            'fifth_stage_text_to_process': '',
            'sixth_stage_text_to_process': '',
            'seventh_stage_text_to_process': '',
            'eighth_stage_text_to_process': '',
            'ninth_stage_text_to_process': '',
            'tenth_stage_text_to_process': '',
            'eleventh_stage_text_to_process': '',
            'twelfth_stage_text_to_process': '',
            'thirteenth_stage_text_to_process': '',
            'fourteenth_stage_text_to_process': '',
            'fifteenth_stage_text_to_process': '',
            'sixteenth_stage_text_to_process': '',

        })"""

    # for idx, part in enumerate(parts):
    #     print(f"Part {idx + 1}: {part.strip()}")

    # input("Check parts printed and press Enter second time to continue first time creation of temporary dictionary list_1_temp_question_parts_hindi_also...")

    # data_dict = list_1_temp_question_parts_hindi_also  # This should be the dictionary created earlier
    filename_prefix = dict_excel_name  # Prefix for the Excel file name

    excel_file_path = dict_excel_file_path

    # folder_path = excel_file_path
    # create_excel_for_dict_for_list_parts(dynamic_dict_name_list_1_parts, excel_file_path, filename_prefix)

    # list_1_parts extraction will work in 3 rounds
    # first round will look for 1-5A-E and a dot with up to 3 whitespaces
    # second round will look for 1-5A-E surrounded by parentheses and a dot with up to 3 whitespaces
    # third round will look for 1-5A-E surrounded by parentheses and no dot with up to 3 whitespaces

    # Preparing things for the first round
    # Create a copy of the dictionary for iteration to avoid modifying it during the loop
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_1_parts)

    # Initialising the output_text at the beginning
    output_text = ""  # Ensure this is at the beginning of the function or before the loop starts.

    # To handle entries starting from A-E, define the mapping at the start to return number
    number_mapping = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5'}

    # Define the pattern outside the loop
    # patterns handling properly the occurrences of Hindi

    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL)
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL)
    # modifying pattern to handle parentheses
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)(?:\(?([1-5])\)?\s{0,3}\.?)(.*?)(?=(?:\s\(?[1-5]\)?\s{0,3}\.?|$))", re.DOTALL)
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL)
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))", re.DOTALL)
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL) # perfect for numbers without parentheses
    # modifying the perfect pattern to allow for A-E in addition to 1-5
    pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
    # modifying pattern to handle parentheses
    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))", re.DOTALL)
    pattern_to_find_list_1_parts_2 = re.compile(
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))",
        re.DOTALL)  # perfect for numbers and parentheses but requires a dot
    # modifying pattern to handle parentheses without the dot
    pattern_to_find_list_1_parts_3 = re.compile(
        r"\(\s{0,3}([1-5A-E])\s{0,3}(?:[\.\s]\s{0,2})?\)\s*((?:[^\)]*?))(?=\s*\(\s{0,3}[1-5A-E]\s{0,3}(?:[\.\s]\s{0,2})?\)\s*|$)",
        re.DOTALL)  # seems to work perfect with parentheses without dot
    """pattern_to_find_list_1_parts = re.compile(
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?(.*?)(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))|"
        r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
        re.DOTALL
    )"""
    """pattern_to_find_list_1_parts = re.compile(
        r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))|"  # First option
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))|"  # Second option
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\)?|$))",
        # Third option
        re.DOTALL
    )"""
    # Define the patterns for different rounds in a dictionary
    patterns = {
        1: pattern_to_find_list_1_parts_1,
        2: pattern_to_find_list_1_parts_2,
        3: pattern_to_find_list_1_parts_3
    }

    pattern_descriptions = {
        1: "perfect for numbers 1-5 and letters A-E without parentheses",
        2: "perfect for numbers and parentheses but requires a dot",
        3: "seems to work perfect with parentheses without dot"
    }

    # User input for pattern selection
    # pattern_number = int(input("Please choose the pattern_number from 1, 2, 3: "))
    # current_pattern = patterns[pattern_number]
    # Get description for the current pattern
    # current_description = pattern_descriptions[pattern_number]
    # input("Please press Enter to start first round processing for list_1 parts extraction.......")

    pattern_round = 1
    # first round processing each part using specific pattern
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_1":
            output_text = ''
            # Initialize or reset the dictionary for each segment
            list_1_question_parts = {
                'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                'question_type': entry.get('question_type', '').strip(),
                'question_sub_type': entry.get('question_sub_type', '').strip(),
                'question_part_list1_max_row': entry.get('question_part_list1_max_row', 0),
                'question_complete': entry.get('question_complete', False),
                'list_1_present': entry.get('list_1_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
            }

            pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                        re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
            # pattern_to_find_list_1_parts_2 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))", re.DOTALL)  # perfect for numbers and parentheses but requires a dot
            # pattern_to_find_list_1_parts_3 = re.compile(r"\(\s{0,3}([1-5A-E])\s{0,3}(?:[\.\s]\s{0,2})?\)\s*((?:[^\)]*?))(?=\s*\(\s{0,3}[1-5A-E]\s{0,3}(?:[\.\s]\s{0,2})?\)\s*|$)", re.DOTALL)  # seems to work perfect with parentheses without dot
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\)?\s*(.*?)(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}\)?|$))", re.DOTALL)
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?\s*((?:[^\)]*?))(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))", re.DOTALL) # seems to work perfect with parentheses without dot

            # Extract question_text from temp_question_parts_hindi_also dictionary
            # question_text = temp_question_parts_hindi_also.get('question_text', '')
            question_text = entry['question_part']  # Corrected line to access the actual question text

            # initial test match to see extraction and matches/ groups/ parts
            matches_for_list_1_parts_pattern_1 = list(pattern_to_find_list_1_parts_1.finditer(question_text))
            # printing the matches
            for index, match_for_list_1_parts_pattern_1 in enumerate(matches_for_list_1_parts_pattern_1, start=1):
                number = match_for_list_1_parts_pattern_1.group(1) if match_for_list_1_parts_pattern_1.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_1.group(2) if match_for_list_1_parts_pattern_1.group(
                    2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number:  # If the first group was None, check the next group
                    number = match_for_list_1_parts_pattern_1.group(3) if match_for_list_1_parts_pattern_1.group(
                        3) is not None else ''
                if not content and len(
                        match_for_list_1_parts_pattern_1.groups()) > 3:  # If the second group was None and there are more groups
                    content = match_for_list_1_parts_pattern_1.group(4) if match_for_list_1_parts_pattern_1.group(
                        4) is not None else ''

                number = number.strip()
                content = content.strip()

            # Initialize the variables last_row_number, last_row_content/ last_list_1_row_with_question_third_part and match_contents before the loop
            last_row_number = 0
            last_row_content = ""
            last_list_1_row_with_question_third_part = ""
            match_for_list_1_parts_pattern_1_contents = []
            # Iterate over matches to collect their details
            # to find out last_row_number
            for match_for_list_1_parts_pattern_1 in matches_for_list_1_parts_pattern_1:
                number = match_for_list_1_parts_pattern_1.group(1).strip() if match_for_list_1_parts_pattern_1.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_1.group(2).strip() if match_for_list_1_parts_pattern_1.group(
                    2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number and len(
                        match_for_list_1_parts_pattern_1.groups()) >= 3:  # Check the third group only if it exists
                    number = match_for_list_1_parts_pattern_1.group(3).strip() if match_for_list_1_parts_pattern_1.group(
                        3) is not None else ''
                if not content and len(
                        match_for_list_1_parts_pattern_1.groups()) > 3:  # Check the fourth group only if it exists
                    content = match_for_list_1_parts_pattern_1.group(4).strip() if match_for_list_1_parts_pattern_1.group(
                        4) is not None else ''

                # Convert letters to numbers if necessary
                if number in number_mapping:
                    number = int(number_mapping[number])  # Convert letters to numbers
                else:
                    try:
                        number = int(number)  # Try converting directly if already a number
                    except ValueError:
                        # print(f"Failed to convert number: {number}")
                        continue  # Skip this iteration if conversion fails

                match_for_list_1_parts_pattern_1_contents.append((number, content))
                # print(f"Match {number}: content: {content}")

            # Sort by number to ensure correct order
            match_for_list_1_parts_pattern_1_contents.sort()

            # Finding the highest valid number and previous row's content
            # Extract last row details
            if match_for_list_1_parts_pattern_1_contents:
                last_row_number, last_row_content = match_for_list_1_parts_pattern_1_contents[-1]
                print(f"Last row number: {last_row_number}, Last row content: {last_row_content}")
            else:
                print("No matches found for last_row_number.")
                # setting the value of question_complete in case there is no match
                list_1_question_parts['question_complete'] = False

            list_1_question_parts[f'question_part_list1_max_row'] = last_row_number
            # input(f"for question_id: {question_id}, the last_row_number is: {last_row_number}, Press Enter to continue.....")

            # commenting out as temp_question_parts_hindi_also is structured with keys like question_id_1, question_id_2, etc.,
            # each mapping to a dictionary that contains the actual question_part.

            # commenting out as this statement is equivalent to initialising the output_text, need to use += instead of only =
            # output_text = f"For first round processing, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1: {pattern_to_find_list_1_parts.pattern}\n"
            output_text += f"For first round processing, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1_parts_1\n"
            # input(f"Please check the question_text to be processed: {question_text}, Press Enter to continue")

            # now starting matching to get the actual values of list_1_parts
            # Find all matches and populate the dictionary
            for match_for_list_1_parts_pattern_1 in pattern_to_find_list_1_parts_1.finditer(question_text):
                # for match_for_list_1_parts in pattern_to_find_list_1_parts.finditer(question_text):

                # Initialize variables for number and content
                number = None
                content = None
                number = match_for_list_1_parts_pattern_1.group(1).strip() if match_for_list_1_parts_pattern_1.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_1.group(2).strip() if match_for_list_1_parts_pattern_1.group(
                    2) is not None else ''

                # Further processing only if both are valid
                if number is not None and content:
                    # Ensure 'content' is a string and strip it
                    # content = content.strip()
                    # Convert letter to number if applicable
                    if number and number in number_mapping:
                        number = number_mapping[number]
                    # Assign content to the correct dictionary key based on number
                    # input(f"Processing for match number: {number} and content: {content}. Press Enter to continue...")
                    list_1_question_parts[f'list_1_row{number}'] = content
                    if int(number) == int(last_row_number):
                        # input(f"Processing for last_row_number: {last_row_number} and last_row_content: {last_row_content}. Press Enter to continue...")
                        # pattern_for_E_or_5 = re.compile(r"(?:\(?\s{0,3}(E|5)\s{0,3}\.?\s{0,3}\)?)")
                        # pattern_for_D_or_4 = re.compile(r"(?:\(?\s{0,3}(D|4)\s{0,3}\.?\s{0,3}\)?)")
                        if last_row_content:
                            if last_row_number > 0:
                                parts = list_1_question_parts[f'list_1_row{last_row_number}'].split('\n', 1)
                                if len(parts) == 2:
                                    # Update the row content to only include text before the newline
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    # Assign the content after the newline to 'question_part_third_part'
                                    list_1_question_parts['question_part_third_part'] = parts[1].strip()
                                else:
                                    # If there's no newline, assign the whole text to the row and clear 'question_part_third_part'
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    list_1_question_parts['question_part_third_part'] = ''
                        else:
                            print("No content available in the last row.")

                    # After the loop, remove all matched text from the original question_text
                    cleaned_question_text = re.sub(pattern_to_find_list_1_parts_1, "", question_text).strip()
                    # Remaining text as first part
                    list_1_question_parts['question_part_first_part'] = cleaned_question_text.strip()

            # Completeness check directly after processing
            question_complete = False  # Assume complete and check for any empty fields
            max_row = last_row_number
            # input(f"First Round for question_id :{question_id}, the last_row_number is {last_row_number}, and press Enter to continue..")
            temp_list_for_question_complete_first_round = []
            for i in range(1, max_row + 1):
                row_key = f'list_1_row{i}'
                row_content = list_1_question_parts[row_key]  # Get the content of the row, defaulting to an empty string
                if row_content:
                    temp_list_for_question_complete_first_round.append(1)  # Append 1 if the row is not empty
                    # input(f"for question_id: {question_id}, for row_key: {row_key}, list_1_question_parts.get('list_1_row{i}') is: {row_content}")
                else:
                    temp_list_for_question_complete_first_round.append(0)  # Append 0 if the row is empty

            # Check if there are any 0s in the list, indicating incomplete fields
            if 0 in temp_list_for_question_complete_first_round:
                list_1_question_parts['question_complete'] = False
            else:
                list_1_question_parts['question_complete'] = True

            if last_row_number == 0:
                list_1_question_parts['question_complete'] = False

            # print(f"Completeness status after first round for question_id: {question_id}, {list_1_question_parts['question_complete']}, and last_row_number {list_1_question_parts['question_part_list1_max_row']}")
            # input("Check the completeness status above after first round for question_id: {question_id} , Press Enter to continue")

            # After first round, append the processed data back to the original dictionary
            dynamic_dict_name_list_1_parts[question_id].update(list_1_question_parts)

            # input(f"Check the dictionary contents and press Enter to continue....")

            # print("Contents of list_1_question_parts after processing current entry:")
            # print(list_1_question_parts)  # This will print the dictionary after each question part is processed

            # adding to output text for creating text file of assessment record
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_text += f"\n"
            output_text += f"Date and Time of processing is: {current_time}\n"
            output_text += f"\n"
            output_text += f"question_id {question_id} details:\n"
            output_text += f"\n"
            output_text += f"Pattern used is pattern 1 i.e {pattern_to_find_list_1_parts_1}\n"
            output_text += f"Question part first part: {list_1_question_parts['question_part_first_part']}\n"
            if last_row_number > 0:  # Check before accessing dictionary with last_row_number
                output_text += f"For question_id : {question_id}, the list_1 last row is: {list_1_question_parts[f'list_1_row{last_row_number}']}, and question_part_third_part is :{list_1_question_parts['question_part_third_part']}\n"
                for i in range(1, last_row_number + 1):
                    row_key = f'list_1_row{i}'  # Construct the key name dynamically
                    output_text += f"{row_key}: {list_1_question_parts.get(row_key, 'Not available')}\n"
            else:
                output_text += "No valid row numbers found.\n"
            output_text += f"question_part_third_part: {list_1_question_parts['question_part_third_part']}\n\n"
            output_text += f"\n"
            output_text += f"--------\n"
        else:

            print(f"No question_sub_type of list_1 type found, Press Enter to continue.............")
    # After first round processing is complete for all items
    # After processing, writing to a file for first round processing
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    # After populating the dictionary with all matches

    print("Writing to file:", output_text)
    print("Writing to file:", output_text)
    recording_text_file_path = recording_text_file_path.with_suffix('.txt')  # Ensure the file has a .txt extension

    # Open the existing file in read mode and read its contents, no longer using 'a' for appending
    # Before attempting to read the file, check if it exists
    # Check if the file exists
    if recording_text_file_path.exists():
        # Read existing contents if the file exists
        with open(recording_text_file_path, 'r', encoding='utf-8') as file:
            existing_contents = file.read()
        # Write the new text followed by the existing contents
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text + existing_contents)
    else:
        # If the file does not exist, just create it and write the new text
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

    # print(output_text)

    # print(f"All processing data has been combined and written to {recording_text_file_path}")
    """with open(output_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{output_path}'after first round processing has been updated/ created in the directory: '{folder_path}'")"""

    # After processing, creating excel for first round processing
    create_excel_for_dict(dynamic_dict_name_list_1_parts, base_dir_path, f"{dict_excel_name}_list_1_parts_pattern_round_1")
    # Debug print after first round processing, for question_complete and last_row_number
    for question_id, entry in dynamic_dict_name_list_1_parts.items():
        # After processing, check if the question is complete
        # question_complete = is_question_complete(data_dict, question_id)  # This checks completeness based on updated data in list_1_question_parts
        print(
            f"For question_id: {question_id},value of 'question_complete' in data dict is: {entry.get('question_complete', False)}, and last_row_number {entry.get('question_part_list1_max_row')}")

    # input(f"after First Round, please check the above entries for 'question_complete' in the dictionary {data_dict_name}, Press Enter to continue")
    # input(f"after First Round, please check the above entries for 'question_complete' in the dictionary, Press Enter to continue")



    # Preparing things for the second round
    # Create a copy of the dictionary for iteration to avoid modifying it during the loop
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_1_parts)

    # Initialising the output_text at the beginning
    output_text = ""  # Ensure this is at the beginning of the function or before the loop starts.

    # To handle entries starting from A-E, define the mapping at the start to return number
    number_mapping = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5'}

    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL) # perfect for numbers without parentheses
    # modifying the perfect pattern to allow for A-E in addition to 1-5
    pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
    # modifying pattern to handle parentheses
    pattern_to_find_list_1_parts_2 = re.compile(
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))",
        re.DOTALL)  # perfect for numbers and parentheses but requires a dot
    # modifying pattern to handle parentheses without the dot
    pattern_to_find_list_1_parts_3 = re.compile(
        r"\(\s{0,3}([1-5A-E])\s{0,3}(?:[\.\s]\s{0,2})?\)\s*((?:[^\)]*?))(?=\s*\(\s{0,3}[1-5A-E]\s{0,3}(?:[\.\s]\s{0,2})?\)\s*|$)",
        re.DOTALL)  # seems to work perfect with parentheses without dot

    # Define the mapping for patterns for different rounds in a dictionary
    patterns = {
        1: pattern_to_find_list_1_parts_1,
        2: pattern_to_find_list_1_parts_2,
        3: pattern_to_find_list_1_parts_3
    }
    pattern_descriptions = {
        1: "perfect for numbers 1-5 and letters A-E without parentheses",
        2: "perfect for numbers and parentheses but requires a dot",
        3: "seems to work perfect with parentheses without dot"
    }

    # User input for pattern selection
    # pattern_number = int(input("Please choose the pattern_number from 1, 2, 3: "))
    # current_pattern = patterns[pattern_number]
    # Get description for the current pattern
    # current_description = pattern_descriptions[pattern_number]

    pattern_round = 2
    # second round processing each part using specific pattern
    list_of_question_ids_for_second_stage = []
    for question_id, entry in data_dict_copy.items():
        # Get the value of question_complete, defaulting to False if it's not found
        question_complete = entry.get('question_complete', False)
        if not question_complete:  # Check if the question is incomplete
            list_of_question_ids_for_second_stage.append(question_id)

        # print(f" for question_id: {question_id}, the value for question_complete is : {question_complete}")
    print(list_of_question_ids_for_second_stage)
    # input("Please check above the question_ids being taken up for second round processing for list_1 parts extraction, Press Enter to continue... ")

    for question_id, entry in data_dict_copy.items():
        # Initialize or reset the dictionary for each segment
        # processing only fot those questions which are incomplete i.e having any of list_1_row as empty
        if entry.get('question_sub_type') == "list_type_1" and not is_question_complete(dynamic_dict_name_list_1_parts, question_id):
            list_1_question_parts = {
                'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                'question_type': entry.get('question_type', '').strip(),
                'question_sub_type': entry.get('question_sub_type', '').strip(),
                'question_part_list1_max_row': entry.get('question_part_list1_max_row', 0),
                'question_complete': entry.get('question_complete', False),
                'list_1_present': entry.get('list_1_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
            }

            pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                        re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
            pattern_to_find_list_1_parts_2 = re.compile(
                r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))",
                re.DOTALL)  # perfect for numbers and parentheses but requires a dot
            pattern_to_find_list_1_parts_3 = re.compile(
                r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?\s*((?:[^\)]*?))(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))",
                re.DOTALL)  # seems to work perfect with parentheses without dot
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\)?\s*(.*?)(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}\)?|$))", re.DOTALL)
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?\s*((?:[^\)]*?))(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))", re.DOTALL) # seems to work perfect with parentheses without dot

            # initial test match to see extraction and matches/ groups/ parts
            """matches_for_list_1_parts_pattern_2 = list(pattern_to_find_list_1_parts_2.finditer(question_text))
            # printing the matches
            for index, match_for_list_1_parts_pattern_2 in enumerate(matches_for_list_1_parts_pattern_2, start=1):
                number = match_for_list_1_parts_pattern_2.group(1) if match_for_list_1_parts_pattern_2.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_2.group(2) if match_for_list_1_parts_pattern_2.group(
                    2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number:  # If the first group was None, check the next group
                    number = match_for_list_1_parts_pattern_2.group(3) if match_for_list_1_parts_pattern_2.group(
                        3) is not None else ''
                if not content and len(
                        match_for_list_1_parts_pattern_2.groups()) > 3:  # If the second group was None and there are more groups
                    content = match_for_list_1_parts_pattern_2.group(4) if match_for_list_1_parts_pattern_2.group(
                        4) is not None else ''

                number = number.strip()
                content = content.strip()

                if number and content:
                    print(f"Match {index}: number: {number}, content: {content}")"""

            # Initialize the variables last_row_number, last_row_content/ last_list_1_row_with_question_third_part and match_contents before the loop
            last_row_number = 0
            last_row_content = ""
            last_list_1_row_with_question_third_part = ""
            match_contents_list_1_parts_pattern_2 = []

            # Extract question_text from temp_question_parts_hindi_also dictionary
            # question_text = temp_question_parts_hindi_also.get('question_text', '')
            question_text = entry['question_part']  # Corrected line to access the actual question text

            # Iterate over matches to collect their details
            # to find out last_row_number
            matches_for_list_1_parts_pattern_2 = list(pattern_to_find_list_1_parts_2.finditer(question_text))
            for match_for_list_1_parts_pattern_2 in matches_for_list_1_parts_pattern_2:
                number = match_for_list_1_parts_pattern_2.group(1).strip() if match_for_list_1_parts_pattern_2.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_2.group(2).strip() if match_for_list_1_parts_pattern_2.group(
                    2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number and len(
                        match_for_list_1_parts_pattern_2.groups()) >= 3:  # Check the third group only if it exists
                    number = match_for_list_1_parts_pattern_2.group(
                        3).strip() if match_for_list_1_parts_pattern_2.group(3) is not None else ''
                if not content and len(
                        match_for_list_1_parts_pattern_2.groups()) > 3:  # Check the fourth group only if it exists
                    content = match_for_list_1_parts_pattern_2.group(
                        4).strip() if match_for_list_1_parts_pattern_2.group(4) is not None else ''

                # Print match details if both number and content are present
                if number and content:
                    print(f"Match: number: {number}, content: {content}")

                # Convert letters to numbers if necessary
                if number in number_mapping:
                    number = int(number_mapping[number])  # Convert letters to numbers
                else:
                    try:
                        number = int(number)  # Try converting directly if already a number
                    except ValueError:
                        print(f"Failed to convert number: {number}")
                        continue  # Skip this iteration if conversion fails

                match_contents_list_1_parts_pattern_2.append((number, content))
                print(f"Match {number}: content: {content}")

            # Sort by number to ensure correct order
            match_contents_list_1_parts_pattern_2.sort()

            # Finding the highest valid number and previous row's content
            # Extract last and previous row details
            if match_contents_list_1_parts_pattern_2:
                last_row_number, last_row_content = match_contents_list_1_parts_pattern_2[-1]
                # print(f"Last row number: {last_row_number}, Last row content: {last_row_content}")
            else:
                print("No matches found for last_row_number.")
                # setting the value of question_complete in case there is no match
                list_1_question_parts['question_complete'] = False

            list_1_question_parts[f'question_part_list1_max_row'] = last_row_number
            # input(f"for question_id: {question_id}, the last_row_number is: {last_row_number} and last_row_content: {last_row_content}, Press Enter to continue.....")

            # commenting out as this statement is equivalent to initialising the output_text, need to use += instead of only =
            # output_text = f"For first round processing, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1: {pattern_to_find_list_1_parts.pattern}\n"
            output_text += f"For second round processing, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1_parts_2{round}\n"
            # input(f"Please check the question_text to be processed: {question_text}, Press Enter to continue")

            # now starting matching to get the values of list_1_parts
            # Find all matches and populate the dictionary
            for match_for_list_1_parts_pattern_2 in pattern_to_find_list_1_parts_2.finditer(question_text):
                # for match_for_list_1_parts in pattern_to_find_list_1_parts.finditer(question_text):

                # Initialize variables for number and content
                number = None  # Reset to ensure it doesn't carry over from a previous iteration
                content = None  # Reset for the same reason
                number = match_for_list_1_parts_pattern_2.group(1).strip() if match_for_list_1_parts_pattern_2.group(
                    1) is not None else ''
                content = match_for_list_1_parts_pattern_2.group(2).strip() if match_for_list_1_parts_pattern_2.group(
                    2) is not None else ''
                # input(f"number: {number}, content: {content}.Press Enter to continue...")

                # Further processing only if both are valid
                if number is not None and content:
                    # Convert letter to number if applicable
                    # Check if the number is a letter and map it to a number, or keep it if it's already a number
                    if number and number in number_mapping:
                        number = number_mapping[number]
                    # Assign content to the correct dictionary key based on number
                    # input(f"Processing for match number: {number} and content: {content}. Press Enter to continue...")
                    list_1_question_parts[f'list_1_row{number}'] = content

                    if int(number) == int(last_row_number):
                        # input(f"Processing for last_row_number: {last_row_number} and last_row_content: {last_row_content}. Press Enter to continue...")
                        # pattern_for_E_or_5 = re.compile(r"(?:\(?\s{0,3}(E|5)\s{0,3}\.?\s{0,3}\)?)")
                        # pattern_for_D_or_4 = re.compile(r"(?:\(?\s{0,3}(D|4)\s{0,3}\.?\s{0,3}\)?)")
                        if last_row_content:
                            if last_row_number > 0:
                                parts = list_1_question_parts[f'list_1_row{last_row_number}'].split('\n', 1)
                                if len(parts) == 2:
                                    # Update the row content to only include text before the newline
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    # Assign the content after the newline to 'question_part_third_part'
                                    list_1_question_parts['question_part_third_part'] = parts[1].strip()
                                else:
                                    # If there's no newline, assign the whole text to the row and clear 'question_part_third_part'
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    list_1_question_parts['question_part_third_part'] = ''
                        else:
                            print("No content available in the last row.")

                    # After the loop, remove all matched text from the original question_text
                    cleaned_question_text = re.sub(pattern_to_find_list_1_parts_2, "", question_text).strip()
                    # Remaining text as first part
                    list_1_question_parts['question_part_first_part'] = cleaned_question_text.strip()

            # Completeness check directly after processing
            question_complete = False  # Assume complete and check for any empty fields
            max_row = last_row_number
            # input(f"First Round for question_id :{question_id}, the last_row_number is {last_row_number}, and press Enter to continue..")
            temp_list_for_question_complete_second_round = []
            if entry.get('question_sub_type') == "list_type_1":
                for i in range(1, max_row + 1):
                    row_key = f'list_1_row{i}'
                    row_content = list_1_question_parts[
                        row_key]  # Get the content of the row, defaulting to an empty string
                    if row_content:
                        temp_list_for_question_complete_second_round.append(1)  # Append 1 if the row is not empty
                        # input(f"for question_id: {question_id}, for row_key: {row_key}, list_1_question_parts.get('list_1_row{i}') is: {row_content}")
                    else:
                        temp_list_for_question_complete_second_round.append(0)  # Append 0 if the row is empty

                # Check if there are any 0s in the list, indicating incomplete fields
                if 0 in temp_list_for_question_complete_second_round:
                    list_1_question_parts['question_complete'] = False
                else:
                    list_1_question_parts['question_complete'] = True

                if last_row_number == 0:
                    list_1_question_parts['question_complete'] = False

                list_1_question_parts['question_complete'] = question_complete
            # print(f"Final completeness status after second round for list_1 parts extraction for question_id: {question_id}, {list_1_question_parts['question_complete']}, and last_row_number {list_1_question_parts['question_part_list1_max_row']} ")
            # input("Check the final completeness status above after second round for question_id: {question_id} , Press Enter to continue")

            # After second round, append the processed data back to the original dictionary
            dynamic_dict_name_list_1_parts[question_id].update(list_1_question_parts)
            # input(f"Check the dictionary contents and press Enter to continue....")

            # print("Contents of list_1_question_parts after processing current entry:")
            # print(list_1_question_parts)  # This will print the dictionary after each question part is processed

            # adding to output text for creating text file of assessment record
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_text += f"\n"
            output_text += f"Date and Time of processing is: {current_time}\n"
            output_text += f"\n"
            output_text += f"Pattern used is pattern_2 i.e {pattern_to_find_list_1_parts_2}\n"
            output_text += f"\n"
            output_text += f"question_id {question_id} details:\n"
            output_text += f"Question part first part: {list_1_question_parts['question_part_first_part']}\n"
            if last_row_number > 0:  # Check before accessing dictionary with last_row_number
                output_text += f"For question_id : {question_id}, the list_1 last row is: {list_1_question_parts[f'list_1_row{last_row_number}']}, and question_part_third_part is :{list_1_question_parts['question_part_third_part']}\n"
                for i in range(1, last_row_number + 1):
                    row_key = f'list_1_row{i}'  # Construct the key name dynamically
                    output_text += f"{row_key}: {list_1_question_parts.get(row_key, 'Not available')}\n"
            else:
                output_text += "No valid row numbers found.\n"
            output_text += f"question_part_third_part: {list_1_question_parts['question_part_third_part']}\n\n"
            output_text += f"\n"
            output_text += f"--------\n"
        else:
            print(f"All questions of list 1 type are already complete")
    # After second round processing is complete for all items
    # After processing, writing to a file for second round processing
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    # After populating the dictionary with all matches

    print("Writing to file:", output_text)
    recording_text_file_path = recording_text_file_path.with_suffix('.txt')  # Ensure the file has a .txt extension
    # Open the existing file in read mode and read its contents, no longer using 'a' for appending
    # Before attempting to read the file, check if it exists
    if recording_text_file_path.exists():
        with open(recording_text_file_path, 'r', encoding='utf-8') as file:
            existing_contents = file.read()
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text + existing_contents)
    else:
        # If the file does not exist, create it and write the new text
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

    # print(f"Updated or created file at: {recording_text_file_path}")
    # print(output_text)

    # print(f"All processing data has been combined and written to {recording_text_file_path}")
    """with open(output_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
        file.write(output_text)
        print(
            f"the text file '{output_path}'after second round processing has been updated/ created in the directory: '{folder_path}'")"""

    # After processing, creating excel for second round processing
    create_excel_for_dict(dynamic_dict_name_list_1_parts, base_dir_path, f"{dict_excel_name}_list_1_parts_pattern_round_2")

    for question_id, entry in dynamic_dict_name_list_1_parts.items():
        # After processing, check if the question is complete
        # question_complete = is_question_complete(data_dict, question_id)  # This checks completeness based on updated data in list_1_question_parts
        print(f"For question_id: {question_id},value of 'question_complete' in data dict is: {entry.get('question_complete', False)}, and last_row_number {entry.get('question_part_list1_max_row')}")

    # input("After second round for list_1 parts extraction, please check the above entries for 'question_complete' in dictionary {data_dict_name}, after First Round in data dict, Press Enter to continue")

    # Preparing things for the third round
    # Create a copy of the dictionary for iteration to avoid modifying it during the loop
    # data_dict_copy = data_dict.copy()
    data_dict_copy = copy.deepcopy(dynamic_dict_name_list_1_parts)

    # Initialising the output_text at the beginning
    output_text = ""  # Ensure this is at the beginning of the function or before the loop starts.

    # To handle entries starting from A-E, define the mapping at the start to return number
    number_mapping = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5'}

    # pattern_to_find_list_1_parts = re.compile(r"(?<=\s)([1-5])\s{0,3}\.(.*?)(?=(?:\s[1-5]\s{0,3}\.|$))", re.DOTALL) # perfect for numbers without parentheses
    # modifying the perfect pattern to allow for A-E in addition to 1-5
    pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
    # modifying pattern to handle parentheses
    pattern_to_find_list_1_parts_2 = re.compile(
        r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))",
        re.DOTALL)  # perfect for numbers and parentheses but requires a dot
    # modifying pattern to handle parentheses without the dot
    pattern_to_find_list_1_parts_3 = re.compile(
        r"\(\s{0,3}([1-5A-E])\s{0,3}(?:[\.\s]\s{0,2})?\)\s*((?:[^\)]*?))(?=\s*\(\s{0,3}[1-5A-E]\s{0,3}(?:[\.\s]\s{0,2})?\)\s*|$)",
        re.DOTALL)  # seems to work perfect with parentheses without dot

    # Define the mapping for patterns for different rounds in a dictionary
    patterns = {
        1: pattern_to_find_list_1_parts_1,
        2: pattern_to_find_list_1_parts_2,
        3: pattern_to_find_list_1_parts_3
    }
    pattern_round = 3
    # before third round processing informing about the incomplete question_ids to be taken up fpr processing
    list_of_question_ids_for_third_stage = []
    for question_id, entry in data_dict_copy.items():
        if entry.get('question_sub_type') == "list_type_1":
            # Get the value of question_complete, defaulting to False if it's not found
            question_complete = entry.get('question_complete', False)
            if not question_complete:  # Check if the question is incomplete
                list_of_question_ids_for_third_stage.append(question_id)

            # print(f" for question_id: {question_id}, the value for question_complete is : {question_complete}")
    print(list_of_question_ids_for_third_stage)
    # input("Please check above the question_ids being taken up for third round processing for list_1 parts extraction, Press Enter to continue... ")

    # third round processing each part using specific pattern
    for question_id, entry in data_dict_copy.items():
        # Initialize or reset the dictionary for each segment
        # processing only fot those questions which are incomplete i.e having any of list_1_row as empty
        if entry.get('question_sub_type') == "list_type_1" and not is_question_complete(dynamic_dict_name_list_1_parts, question_id):
            list_1_question_parts = {
                'question_part_first_part': entry.get('question_part_first_part', '').strip(),
                'question_type': entry.get('question_type', '').strip(),
                'question_sub_type': entry.get('question_sub_type', '').strip(),
                'question_part_list1_max_row': entry.get('question_part_list1_max_row', 0),
                'question_complete': entry.get('question_complete', False),
                'list_1_present': entry.get('list_1_present', False),
                'list_1_name': entry.get('list_1_name', '').strip(),
                'list_1_entries': entry.get('list_1_entries', []),
                'list_2_entries': entry.get('list_2_entries', []),
                'second_stage_text_to_process': entry.get('second_stage_text_to_process', '').strip(),
                'third_stage_text_to_process': entry.get('third_stage_text_to_process', '').strip(),
                'question_part_third_part': entry.get('question_part_third_part', '').strip(),
                'fourth_stage_text_to_process': entry.get('fourth_stage_text_to_process', '').strip(),
                'fifth_stage_text_to_process': entry.get('fifth_stage_text_to_process', '').strip(),
                'sixth_stage_text_to_process': entry.get('sixth_stage_text_to_process', '').strip(),
                'seventh_stage_text_to_process': entry.get('seventh_stage_text_to_process', '').strip(),
                'eighth_stage_text_to_process': entry.get('eighth_stage_text_to_process', '').strip(),
                'ninth_stage_text_to_process': entry.get('ninth_stage_text_to_process', '').strip(),
                'tenth_stage_text_to_process': entry.get('tenth_stage_text_to_process', '').strip(),
                'eleventh_stage_text_to_process': entry.get('eleventh_stage_text_to_process', '').strip(),
                'twelfth_stage_text_to_process': entry.get('twelfth_stage_text_to_process', '').strip(),
                'thirteenth_stage_text_to_process': entry.get('thirteenth_stage_text_to_process', '').strip(),
                'fourteenth_stage_text_to_process': entry.get('fourteenth_stage_text_to_process', '').strip(),
                'fifteenth_stage_text_to_process': entry.get('fifteenth_stage_text_to_process', '').strip(),
                'sixteenth_stage_text_to_process': entry.get('sixteenth_stage_text_to_process', '').strip(),
                'list_1_row1': entry.get('list_1_row1', '').strip(),
                'list_1_row2': entry.get('list_1_row2', '').strip(),
                'list_1_row3': entry.get('list_1_row3', '').strip(),
                'list_1_row4': entry.get('list_1_row4', '').strip(),
                'list_1_row5': entry.get('list_1_row5', '').strip(),
            }

            pattern_to_find_list_1_parts_1 = re.compile(r"(?<=\s)([1-5A-E])\s{0,3}\.(.*?)(?=(?:\s[1-5A-E]\s{0,3}\.|$))",
                                                        re.DOTALL)  # perfect for numbers 1-5 and letters A-E without parentheses
            pattern_to_find_list_1_parts_2 = re.compile(
                r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\.\s*\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\.\s*\)?|$))",
                re.DOTALL)  # perfect for numbers and parentheses but requires a dot
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\)?\s*(.*?)(?=(?:\s(?:\(\s{0,3})?[1-5A-E]\s{0,3}\)?|$))", re.DOTALL)  # supposed to work with parentheses without dot
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}\)?\s*(.*?)(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}\)?|$))", re.DOTALL)
            # pattern_to_find_list_1_parts_3 = re.compile(r"(?<=\s)(?:\(\s{0,3})?([1-5A-E])\s{0,3}(?:\.\s*)?\)?\s*((?:[^\)]*?))(?=\s*(?:\(\s{0,3}[1-5A-E]\s{0,3}(?:\.\s*)?\)?|$))", re.DOTALL) # had seemed to work perfect with parentheses without dot but was also capturing standalone A-E
            pattern_to_find_list_1_parts_3 = re.compile(
                r"\(\s{0,3}([1-5A-E])\s{0,3}(?:[\.\s]\s{0,2})?\)\s*((?:[^\)]*?))(?=\s*\(\s{0,3}[1-5A-E]\s{0,3}(?:[\.\s]\s{0,2})?\)\s*|$)",
                re.DOTALL)  # seems to work perfect with parentheses without dot

            # Extract question_text from temp_question_parts_hindi_also dictionary
            # question_text = temp_question_parts_hindi_also.get('question_text', '')
            question_text = entry['question_part']  # Corrected line to access the actual question text
            # initial test match to see extraction and matches/ groups/ parts
            matches = list(pattern_to_find_list_1_parts_3.finditer(question_text))
            # printing the matches
            for index, match in enumerate(matches, start=1):
                number = match.group(1) if match.group(1) is not None else ''
                content = match.group(2) if match.group(2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number:  # If the first group was None, check the next group
                    number = match.group(3) if match.group(3) is not None else ''
                if not content and len(match.groups()) > 3:  # If the second group was None and there are more groups
                    content = match.group(4) if match.group(4) is not None else ''

                number = number.strip()
                content = content.strip()

                if number and content:
                    print(f"Match {index}: number: {number}, content: {content}")

            # Initialize the variables last_row_number, last_row_content/ last_list_1_row_with_question_third_part and match_contents before the loop
            last_row_number = 0
            last_row_content = ""
            last_list_1_row_with_question_third_part = ""
            match_contents = []
            # Iterate over matches to collect their details
            for match in matches:
                number = match.group(1).strip() if match.group(1) is not None else ''
                content = match.group(2).strip() if match.group(2) is not None else ''

                # Additional check to handle any other groups that might capture the number or content
                if not number and len(match.groups()) >= 3:  # Check the third group only if it exists
                    number = match.group(3).strip() if match.group(3) is not None else ''
                if not content and len(match.groups()) > 3:  # Check the fourth group only if it exists
                    content = match.group(4).strip() if match.group(4) is not None else ''

                # Print match details if both number and content are present
                if number and content:
                    print(f"Match: number: {number}, content: {content}")

                # Convert letters to numbers if necessary
                if number in number_mapping:
                    number = int(number_mapping[number])  # Convert letters to numbers
                else:
                    try:
                        number = int(number)  # Try converting directly if already a number
                    except ValueError:
                        print(f"Failed to convert number: {number}")
                        continue  # Skip this iteration if conversion fails

                match_contents.append((number, content))
                print(f"Match {number}: content: {content}")

            # Sort by number to ensure correct order
            match_contents.sort()

            # Finding the highest valid number and previous row's content
            # Extract last and previous row details
            if match_contents:
                last_row_number, last_row_content = match_contents[-1]
                # print(f"Last row number: {last_row_number}, Last row content: {last_row_content}")
            else:
                print("No matches found for last_row_number.")
            list_1_question_parts[f'question_part_list1_max_row'] = last_row_number
            # input(f"The last_row_number is: {last_row_number} and last_row_content: {last_row_content}, Press Enter to continue.....")

            # commenting out as temp_question_parts_hindi_also is structured with keys like question_id_1, question_id_2, etc.,
            # each mapping to a dictionary that contains the actual question_part.

            # commenting out as this statement is equivalent to initialising the output_text, need to use += instead of only =
            # output_text = f"For first round processing, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1: {pattern_to_find_list_1_parts.pattern}\n"
            output_text += f"For third round processing for list_1 parts extraction, for question_id : {question_id}, using regex pattern for pattern_to_find_list_1_parts_3{round}\n"
            # input(f"Please check the question_text to be processed: {question_text}, Press Enter to continue")

            # # now starting matching to get the values of list_1_parts
            # Find all matches and populate the dictionary
            for match in matches:

                number = None  # Reset to ensure it doesn't carry over from a previous iteration
                content = None  # Reset for the same reason
                number = match.group(1).strip() if match.group(1) is not None else ''
                content = match.group(2).strip() if match.group(2) is not None else ''
                # input(f"number: {number}, content: {content}.Press Enter to continue...")

                # Further processing only if both are valid
                if number is not None and content:
                    # Convert letter to number if applicable
                    if number in number_mapping:
                        number = int(number_mapping[number])
                    # Assign content to the correct dictionary key based on number
                    # input(f"Processing for match number: {number} and content: {content}. Press Enter to continue...")
                    list_1_question_parts[f'list_1_row{number}'] = content

                    if int(number) == int(last_row_number):
                        # input(f"Processing for last_row_number: {last_row_number} and last_row_content: {last_row_content}. Press Enter to continue...")
                        # pattern_for_E_or_5 = re.compile(r"(?:\(?\s{0,3}(E|5)\s{0,3}\.?\s{0,3}\)?)")
                        # pattern_for_D_or_4 = re.compile(r"(?:\(?\s{0,3}(D|4)\s{0,3}\.?\s{0,3}\)?)")
                        if last_row_content:
                            if last_row_number > 0:
                                parts = list_1_question_parts[f'list_1_row{last_row_number}'].split('\n', 1)
                                if len(parts) == 2:
                                    # Update the row content to only include text before the newline
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    # Assign the content after the newline to 'question_part_third_part'
                                    list_1_question_parts['question_part_third_part'] = parts[1].strip()
                                else:
                                    # If there's no newline, assign the whole text to the row and clear 'question_part_third_part'
                                    list_1_question_parts[f'list_1_row{last_row_number}'] = parts[0].strip()
                                    list_1_question_parts['question_part_third_part'] = ''
                        else:
                            print("No content available in the last row.")

                    # After the loop, remove all matched text from the original question_text
                    cleaned_question_text = re.sub(pattern_to_find_list_1_parts_3, "", question_text).strip()
                    # Remaining text as first part
                    list_1_question_parts['question_part_first_part'] = cleaned_question_text.strip()

            # Completeness check directly after processing of third round
            question_complete = False  # Assume complete and check for any empty fields
            max_row = last_row_number
            # input(f"First Round for question_id :{question_id}, the last_row_number is {last_row_number}, and press Enter to continue..")
            temp_list_for_question_complete_third_round = []
            for i in range(1, max_row + 1):
                row_key = f'list_1_row{i}'
                row_content = list_1_question_parts[
                    row_key]  # Get the content of the row, defaulting to an empty string
                if row_content:
                    temp_list_for_question_complete_third_round.append(1)  # Append 1 if the row is not empty
                    # input(f"for question_id: {question_id}, for row_key: {row_key}, list_1_question_parts.get('list_1_row{i}') is: {row_content}")
                else:
                    temp_list_for_question_complete_third_round.append(0)  # Append 0 if the row is empty

            # Check if there are any 0s in the list, indicating incomplete fields
            if 0 in temp_list_for_question_complete_third_round:
                list_1_question_parts['question_complete'] = False
            else:
                list_1_question_parts['question_complete'] = True

            if last_row_number == 0:
                list_1_question_parts['question_complete'] = False

            # print(f"Final completeness status for list_1 parts extraction for question_id: {question_id}, {list_1_question_parts['question_complete']}")
            # input("Check the final completeness status above after third round for question_id: {question_id} , Press Enter to continue")

            # After first round, append the processed data back to the original dictionary
            dynamic_dict_name_list_1_parts[question_id].update(list_1_question_parts)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_text += f"\n"
            output_text += f"Date and Time of processing is: {current_time}\n"
            output_text += f"\n"
            # output_text += f"Pattern used is {pattern_number} i.e {current_description}\n"
            output_text += f"\n"
            output_text += f"Question is: {question_text.strip()}\n"
            output_text += f"\n"
            output_text += "Details of  for list_1 parts extraction processing:\n" + "\n".join(f"{k}: {v}" for k, v in list_1_question_parts.items())
            output_text += f"\n"
            output_text += f"--------\n"

    # After third round processing is complete for all items
    # After processing, writing to a file for third round processing
    # with open(output_path, 'a') as file:
    # commenting out to handle the UnicodeEncodeError, which typically occurs when Python attempts to save a string
    # containing non-ASCII characters to a file without specifying an appropriate encoding. The default encoding
    # on Windows often doesn't support certain Unicode characters found in languages like Hindi
    # added encoding='utf-8' to the open() function call. This explicitly tells Python to use UTF-8 encoding when
    # writing to the file, which supports a wide range of Unicode characters including those used in Hindi.
    # After populating the dictionary with all matches

    print("Writing to file:", output_text)
    recording_text_file_path = recording_text_file_path.with_suffix('.txt')  # Ensure the file has a .txt extension
    # Open the existing file in read mode and read its contents, no longer using 'a' for appending
    # Before attempting to read the file, check if it exists
    if recording_text_file_path.exists():
        with open(recording_text_file_path, 'r', encoding='utf-8') as file:
            existing_contents = file.read()
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text + existing_contents)
    else:
        # If the file does not exist, create it and write the new text
        with open(recording_text_file_path, 'w', encoding='utf-8') as file:
            file.write(output_text)

    print(f"Updated or created file at: {recording_text_file_path}")
    # print(output_text)
    print(f"All processing data has been combined and written to {recording_text_file_path}")

    # with open(output_path, 'a', encoding='utf-8') as file:  # Add encoding='utf-8'
    #    file.write(output_text)
    #    print(
    #        f"the text file '{output_path}'after third round processing has been updated/ created in the directory: '{folder_path}'")

    # After processing, creating excel for third round processing
    create_excel_for_dict(dynamic_dict_name_list_1_parts, base_dir_path, f"{dict_excel_name}_list_1_parts_pattern_round_3")
    for question_id, entry in dynamic_dict_name_list_1_parts.items():
        # After processing, check if the question is complete
        # question_complete = is_question_complete(data_dict, question_id)  # This checks completeness based on updated data in list_1_question_parts
        print(
            f"For list_1 parts extraction, for question_id: {question_id},value of 'question_complete' in data dict is: {entry.get('question_complete', False)}")

    # input(f"After third round, please check the above entries for 'question_complete' in dictionary {data_dict_name}, Press Enter to continue")
    # input(f"After third round, please check the above entries for 'question_complete' in dictionary, Press Enter to continue")


    # Creating a .py file for the data_dict after the thirteenth round
    # Name of the dictionary variable in the .py file
    # dict_name = "temp_question_list_1_parts_hindi_also"
    # Filename for the Python file, ensuring it ends with .py
    dict_name = f"list_1_temp_question_parts_{temp_dict_name}.py"
    # Full path including the filename
    # file_path = folder_path / filename
    dynamic_dict_name_list_1_parts_file_path = base_dir_path/ dict_name
    # Call the function to write the dictionary to a Python file
    write_dictionary(dynamic_dict_name_list_1_parts, dynamic_dict_name_list_1_parts_file_path, dict_name)

    return dynamic_dict_name_list_1_parts


def main():

    module_name = os.path.splitext(os.path.basename(__file__))[0]
    input(f"Now you are in {module_name}, Press Enter to continue to extract all list_1 and list_2 parts...")
    # input_to_process_fial = input("Continue to create text files and extract list 1 and list 2 parts from dictionary (y/n): ").strip().lower()
    # input("Press Enter to continue to create text files and extract list 1 and list 2 parts from dictionary, Press Enter to continue..... ")
    input_to_process_fial = 'y'
    # processed_dict = None  # Initialize to None to handle scope
    # dict_name_used_for_excel = None  # Initialize a variable to hold the dictionary name

    if input_to_process_fial == 'y':

        parser = argparse.ArgumentParser(description="Identify question types from dictionary.")
        parser.add_argument("dictionary_name", type=str, help="Name of the dictionary to process")
        parser.add_argument("subfolder", type=str, help="Folder where the dictionary is located")
        parser.add_argument("--other_info_batch", type=str, required=True,
                            help="JSON string of additional information.")
        args = parser.parse_args()

        dict_folder = Path(args.subfolder)
        input_dict_name = args.dictionary_name
        other_info_batch = json.loads(args.other_info_batch)
        print(f"input_dict_name is: {input_dict_name}, and dict_folder is: {dict_folder}")
        # input("Press Enter to continue....")
        if not dict_folder.exists():
            print(f"Folder not found: {dict_folder}")
            return

        process_data(input_dict_name, dict_folder, other_info_batch)

def process_data(dict_name, process_folder, other_info_batch):
    input_dict_name = dict_name
    dict_folder = process_folder
    data_dict = load_dictionary(input_dict_name, dict_folder)
    base_dir_path = process_folder

    # Processing logic here
    # print(f"Processing data from {data_dict}")
    # input("You are now in fresh_integrated_extract_list_type_1_and_2_parts_final.py module, Press Enter to continue to extract all list_1 and list_2 parts...")

    data_dict = load_dictionary(dict_name, base_dir_path)

    if data_dict:
        print(f"Dictionary '{dict_name}' loaded successfully.")
        # Create a new dictionary name based on the base directory and modified naming scheme
        parts = dict_name.split('_')
        new_dict_name_1 = '_'.join(parts[:-5]) + "_type1_extracted_dictionary"
        # input(f"The new_dict_name is {new_dict_name_1}, Press Enter to continue")
        dict_path = base_dir_path / f"{new_dict_name_1}.py"
        excel_path = base_dir_path / f"{new_dict_name_1}.xlsx"
        # processed_dict_list_1_extracted = extract_list_1_parts(data_dict, new_dict_name)
        # processed_dict_list_1_extracted = extract_list_1_parts(data_dict, new_dict_name, base_dir_path)
        processed_dict_list_1_extracted = extract_list_1_parts(data_dict, new_dict_name_1, base_dir_path)
        dict_name_used_for_excel = new_dict_name_1
        # if processed_dict:
        if processed_dict_list_1_extracted:
            print("Lst 1 type parts of questions have been extracted.")

            # Automatically proceed with List 2 part extraction
            input(f"Proceeding with List 2 parts extraction, Press Enter to continue...")
            new_dict_name_2 = '_'.join(dict_name.split('_')[:-4]) + "_type1_and_type2_extracted_dictionary"
            # processed_dict_list_2_extracted = extract_list_2_parts(processed_dict_list_1_extracted, new_dict_name_2, base_dir_path)
            # processed_dict_list_2_extracted, new_final_dict = extract_list_2_parts(processed_dict_list_1_extracted, new_dict_name_2, base_dir_path)
            processed_dict_list_2_extracted, new_final_dict = extract_list_2_parts(processed_dict_list_1_extracted, new_dict_name_2, base_dir_path, other_info_batch)

            if processed_dict_list_2_extracted:
                print("List 2 type parts of questions have been extracted.")
    else:
        print("Error loading or processing the dictionary.")

if __name__ == "__main__":
    main()

