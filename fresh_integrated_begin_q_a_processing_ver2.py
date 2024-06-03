import subprocess
from pathlib import Path
import shutil
import argparse
import importlib.util
import json

# from input_validation import validate_yes_no, validate_number

# from fresh_integrated_identify_all_types import load_dictionary
def validate_input(prompt, allowed_inputs):
    """Prompt the user for input and ensure it matches allowed inputs."""
    while True:
        user_input = input(prompt)
        if user_input in allowed_inputs or user_input == '':
            return user_input
        else:
            print(f"Invalid input. Please press Enter or type one of {allowed_inputs}.")


def validate_yes_no(prompt):
    """ Prompt the user for a 'Y' or 'N' response and return that response. """
    while True:
        response = input(prompt).strip().upper()
        if response in ['Y', 'N']:
            return response
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")


def validate_number(prompt, min_val=0, max_val=float('inf')):
    """ Prompt the user for a number within a specified range and return that number. """
    max_validation_range = max_val
    while True:
        try:
            number = int(input(prompt))
            if min_val <= number <= max_val:
                return number
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# deleting processed PDFs so those do not interfere later
def move_processed_pdfs(source_folder, dump_folder):
    """
    Move PDF files from the source folder to the dump folder.

    Args:
    source_folder (Path): The source folder containing processed PDFs.
    dump_folder (Path): The destination folder to move PDFs to.
    """

    # Define the path to the dump folder
    # dump_folder = Path(r'C:\Users\PC\Desktop\Question Bank Trials\Dump')
    print(f"The Dump Folder Path is: {dump_folder}")
    # Ensure the dump folder exists
    # dump_folder.mkdir(parents=True, exist_ok=True)

    # Move each PDF in the source folder to the dump folder
    for pdf_file in source_folder.glob('*.pdf'):
        destination = dump_folder / pdf_file.name
        shutil.move(str(pdf_file), str(destination))
        print(f"Moved {pdf_file.name} to {dump_folder}")


# function to check if some PDFs are not left inadvertently
def check_for_remaining_pdfs(folder):
    """
    Check if there are any PDF files left in the given folder and print a message.

    Args:
    folder (Path): The folder to check for remaining PDFs.
    """
    pdf_files = list(folder.glob('*.pdf'))
    pdf_files = list(folder.glob('*.pdf'))
    if not pdf_files:
        print(f"The {folder} on which OCR was done has no PDFs left.")
    else:
        print(f"The {folder} on which OCR was done has {len(pdf_files)} PDF(s) left.")


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

def create_directories_and_extract_names(pdf_file_name):

    # Assuming the input files will always be in this directory
    # input_base_path = Path(r'C:\Users\PC\Desktop\Question Bank Trials\Input')
    # replacing backslashes (\) with forward slashes (/)
    # input_base_path = Path('C:/Users/PC/Desktop/Question Bank Trials/Input')
    input_base_path = Path('C:/Users/HP/Desktop/Question Bank Trials/Input')

    # Defining the base path and creating the output folder based on user input
    # output_base_path = Path(r'C:\Users\PC\Desktop\Question Bank Trials\batch')
    # replacing backslashes (\) with forward slashes (/)
    output_base_path = Path('C:/Users/HP/Desktop/Question Bank Trials/batch')

    # Splitting the file name input to derive area name, part name, and process type
    # parts = file_name_input.split()
    parts = pdf_file_name.replace('.pdf', '').split('_')
    print("Parts of the file name:")
    for i, part in enumerate(parts):
        print(f"Part {i + 1}: {part}")

    # Assuming the file name format is consistently "AreaName PartName ProcessType ..."
    # Extract area_name, part_name, and process_type from the parts
    # Extracting area_name, part_name, and process_type based on the input format
    if len(parts) >= 9:
        batch_name = '_'.join(parts[0:3]).lower()
        exam_name = parts[3].lower()
        exam_stage = parts[4].lower()
        subject_name = parts[5].lower()
        area_name = parts[6].lower()
        part_name = parts[7].lower()
        process_type_input = parts[8].lower()
 
        # Mapping short form to full form for process type
        process_type_map = {"que": "Questions", "ans": "Answers"}
        process_type = process_type_map.get(process_type_input, "Unknown")
        filename_prefix = f"{batch_name}_{exam_name}_{exam_stage}_{subject_name}_{area_name}_{part_name}_{process_type_input}_"

        # print(f"File Name is {pdf_file_path},Exam Name : {exam_name},Exam Stage : {exam_stage},Subject Name : {subject_name},Area Name: {area_name},Part Name: {part_name},Process Type: {process_type}")

        # output_folder = output_base_path / f"{area_name} {part_name} {process_type}"
        output_folder_1 = output_base_path / f"Batch_{batch_name}"
        output_folder_1.mkdir(parents=True, exist_ok=True)

        output_folder_2 = output_folder_1 / f"Area_{area_name}"
        output_folder_2.mkdir(parents=True, exist_ok=True)

        # Let's use the fifth and sixth parts for the subfolder name
        # subfolder_name = parts[4] + ' ' + parts[5]
        subfolder_name = f"{area_name}_{part_name}"
        subfolder = output_folder_2 / subfolder_name.lower()
        subfolder.mkdir(parents=True, exist_ok=True)

        dump_folder = output_folder_1 / f"Dump"
        dump_folder.mkdir(parents=True, exist_ok=True)


        # print(f"Base Path for input: {input_base_path}, Output Folder: {output_base_path}, Output Folder 1: {output_folder_1}, Output Folder 2: {output_folder_2}, Output subfolder: {subfolder_path}")
        # modifying to let each value be printed on a new line
        print(
            f"Base Path for input: {input_base_path}\nOutput Folder: {output_base_path}\nOutput Folder 1: {output_folder_1}\nOutput Folder 2: {output_folder_2}\nOutput subfolder: {subfolder}")

        # Construct the full path to the PDF file
        pdf_file_path = input_base_path / pdf_file_name
        print(f"PDF File Path is: {pdf_file_path},")

        # Create the text file name without the "Pages X - Y" part
        text_file_name = '_'.join(parts[:9]).lower().replace(' ', '_') + '.txt'
        text_file_path = subfolder / text_file_name
        print(f"the text_file_path is: {text_file_path}")
        print(f"batch_name is: {batch_name}")
        print(f"exam_name is: {exam_name}")
        print(f"exam_stage is: {exam_stage}")
        print(f"subject_name is: {subject_name}")
        print(f"area_name is: {area_name}")
        print(f"part_name is: {part_name}")
        print(f"process_type_input is: {process_type_input}")
        process_type_input = parts[8].lower()

        # with open(text_file_path, 'w', encoding='utf-8') as text_file:
        #    text_file.write(pdf_text)

        # print(f"Text extracted and saved to {text_file_path}")
        # return pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type, process_type_input
        return pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type_input


    else:
        print("Invalid file name format. Please follow the 'AreaName PartName ProcessType ...' format.")
        exit()  # Exit if the format is not followed


def load_module(file_name, folder_path):
    file_path = folder_path / file_name
    spec = importlib.util.spec_from_file_location("module.name", str(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_and_return_both_dicts(file_name_prefix, subfolder, questions_extraction_target):
    stripped_file_name_prefix = '_'.join(file_name_prefix.split('_')[:-2]) + '_'

    print(f"The stripped_file_name_prefix is: {stripped_file_name_prefix}, Press Enter to continue....")

    questions_file = f"{stripped_file_name_prefix}que_questions_extraction_completed_dictionary"
    # list_2_temp_question_parts_disha_26_2020_upsc_pre_gs1_history_ancient_que_answer_options_all_type1_and_type2_extracted_dictionary
    answers_file = f"{stripped_file_name_prefix}ans_correct_answers_dictionary"

    questions_path = subfolder / f"{questions_file}.py"
    answers_path = subfolder / f"{answers_file}.py"

    questions_dict_found = questions_path.is_file()
    answers_dict_found = answers_path.is_file()

    questions_dict_name = f"{stripped_file_name_prefix}que_questions_extraction_completed_dictionary"
    answers_dict_name = f"{stripped_file_name_prefix}ans_correct_answers_dictionary"

    if questions_dict_found:
        print(f"The corresponding dictionary namely, {questions_file}.py has been found in the {subfolder}")
    else:
        print(f"The corresponding dictionary namely, {questions_file}.py was not found in the {subfolder}")

    if answers_dict_found:
        print(f"The corresponding dictionary namely, {answers_file}.py has been found in the {subfolder}")
    else:
        print(f"The corresponding dictionary namely, {answers_file}.py was not found in the {subfolder}")

    if questions_dict_found and answers_dict_found:
        # user_input = input("Now that both dictionaries have been created, would you like to join the questions with correct answers y/n? ").strip().lower()
        # input("Now that both dictionaries have been created, Press Enter to join the questions with correct answers .... ")
        print(
            "Now that both dictionaries have been created, continuing to join the questions with correct answers")
        user_input = 'y'
        if user_input == 'y':
            # questions_dict_module = load_module(questions_file, subfolder)
            # answers_dict_module = load_module(answers_file, subfolder)

            # questions_dict = getattr(questions_dict_module, questions_dict_name, None)
            # answers_dict = getattr(answers_dict_module, answers_dict_name, None)
            questions_dict = load_dictionary(questions_dict_name, subfolder)
            answers_dict = load_dictionary(answers_dict_name, subfolder)

            if questions_dict and answers_dict:
                join_questions_with_answers_module = Path(
                    __file__).parent / "fresh_integrated_join_questions_with_correct_answers.py"
                subprocess.run([
                    "python", str(join_questions_with_answers_module),
                    str(subfolder), questions_file, answers_file, file_name_prefix, str(float(questions_extraction_target))
                ])
                # Add the input statement for confirmation
                input("The script for join_questions_with_answers_module has been completed successfully, Press Enter to continue.....")

                # Call the fresh_new_excel_creator_basic.py module
                # Name of the created dictionary
                created_dict_name = f"{stripped_file_name_prefix}questions_with_correct_answers_dictionary"
                # Call the fresh_new_excel_creator_basic.py module
                fresh_new_excel_creator_script_path = Path(__file__).parent / "fresh_integrated_excel_creator_basic.py"
                input(f"Press Enter to continue to the module {fresh_new_excel_creator_script_path} with created_dict_name passed as {created_dict_name}.....")
                subprocess.run([
                    "python", str(fresh_new_excel_creator_script_path), str(subfolder), created_dict_name
                ])

                return True
            else:
                print("One or both dictionaries are empty or not correctly loaded.")
                return False
        else:
            print("Operation cancelled by user.")
            return False
    else:
        print("One or both dictionaries were not found.")
        return False


# def process_pdf(file_name):
def process_pdf(file_name, take_input, questions_extraction_target):
    (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type,
     exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
     process_type_input) = create_directories_and_extract_names(file_name)

    print(
        f"File Name is {pdf_file_path},Exam Name : {exam_name},Exam Stage : {exam_stage},Subject Name : {subject_name},Area Name: {area_name},Part Name: {part_name},Process Type: {process_type}")

    targets = {}
    if take_input:
        targets["questions_extraction_target"] = validate_number("Enter target for questions_extraction_target: ", 0,
                                                                 10000)
    else:
        targets["questions_extraction_target"] = questions_extraction_target

    targets_json = json.dumps(targets)


    if process_type == "Questions":
        pdf_to_text_script_path = Path(__file__).parent / "fresh_integrated_text_extraction_ques_pypdf2.py"
        subprocess.run([
            "python",
            str(pdf_to_text_script_path),
            str(pdf_file_path),
            str(text_file_path),
            str(process_type)
        ])
        print(f"{pdf_to_text_script_path.name} has been executed successfully.")
        # return (process_type, filename_prefix, subfolder, targets_json)

    elif process_type == "Answers":
        pdf_to_text_script_path = Path(__file__).parent / "fresh_integrated_text_extraction_ans_pypdf2.py"
        subprocess.run([
            "python",
            str(pdf_to_text_script_path),
            str(pdf_file_path),
            str(text_file_path),
            str(process_type)
        ])
        print(f"{pdf_to_text_script_path.name} has been executed successfully.")
        # return (process_type, filename_prefix, subfolder, targets_json)


    return (process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path)


# def process_text_file(file_name):
def process_text_file(file_name, take_input, questions_extraction_target):
    file_name = file_name + ".txt"
    # process_type, filename_prefix, subfolder, targets_json = create_directories_and_extract_names(file_name)[:4]
    # process_type, filename_prefix, subfolder, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input = create_directories_and_extract_names(
    #    file_name)[:10]
    (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type,
     exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
     process_type_input) = create_directories_and_extract_names(file_name)

    print(f"File Name is {file_name}, Process Type: {process_type}")
    targets = {}
    if take_input:
        targets["questions_extraction_target"] = validate_number("Enter target for questions_extraction_target: ", 0,
                                                                 10000)
    else:
        targets["questions_extraction_target"] = questions_extraction_target

    targets_json = json.dumps(targets)
    # return (process_type, filename_prefix, subfolder, targets_json)
    return (process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, "")

def extract_all_questions_and_parts(text_file_path, target):
    questions_organiser_script_path = Path(
        __file__).parent / "fresh_integrated_extract_all_questions_and_parts.py"
    text_file_path = str(text_file_path)  # Ensure this is correctly defined and accessible here
    questions_extraction_target = target
    # subprocess command to run the script with the path argument
    subprocess.run([
        "python",
        str(questions_organiser_script_path),
        text_file_path,  # Pass the full path to the text file as an argument
        # questions_extraction_target
        str(target)
    ])


def organize_questions(process_type, filename_prefix, subfolder, targets, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, file_name):
    (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name,
     exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
     process_type_input) = create_directories_and_extract_names(file_name)

    if process_type == "Questions":
        print(
            "Before extracting questions, please check for removal of the unwanted parts like 'Hints and Solutions' etc from the text file created")
        # user_choice = input("Proceed with organising questions? (y/n): ").strip().lower()
        # Collecting targets from the user

        targets["r_and_a_type"] = validate_number("Enter target for r_and_a_type: ", 0, 1000)
        targets["list_type"] = validate_number("Enter target for list_type: ", 0, 1000)
        targets["simple_type"] = validate_number("Enter target for simple_type: ", 0, 1000)
        targets["list_1_and_2_type"] = validate_number("Enter target_1 for list_2_type: ", 0, 1000)
        targets["target_2"] = validate_number("Enter target_2 for list_1_type: ", 0, 1000)
        # targets["r_and_a_type"] = float(input("Enter target for r_and_a_type: "))
        # targets["list_type"] = float(input("Enter target for list_type: "))
        # targets["simple_type"] = float(input("Enter target for simple_type: "))
        # targets["list_1_and_2_type"] = float(input("Enter target_1 for list_2_type: "))
        # targets["target_2"] = float(input("Enter target_2 for list_1_type: "))

        targets_json = json.dumps(targets)
        other_info_batch = {
            # "pdf_file_path": pdf_file_path,
            # "output_folder_1": output_folder_1,
            # "output_folder_2": output_folder_2,
            # "subfolder": subfolder,
            # "filename_prefix": filename_prefix,
            # "dump_folder": dump_folder,
            # "process_type": process_type,
            "exam_name": exam_name,
            "exam_stage": exam_stage,
            "subject_name": subject_name,
            "area_name": area_name,
            "part_name": part_name,
            # "text_file_path": text_file_path,
            "batch_name": batch_name,
            # "process_type_input": process_type_input,
            "type_of_question": input("Enter type_of_question, say mcq : "),
            "marks": input("Enter marks : "),
            "negative_marks": input("Enter negative_marks : ")
        }
        other_info_batch_json = json.dumps(other_info_batch)
        print(f"The data in other_info_batch is {other_info_batch}")
        input(f" Press Enter to continue to proceed with organising questions if you are satisfied with the above data for other_info_batch ....")
        # input("Press Enter to continue to proceed with organising questions.....")
        user_choice_que = 'y'
        if user_choice_que == 'y':
            questions_organiser_script_path = Path(
                 __file__).parent / "fresh_integrated_extract_all_questions_and_parts.py"
            text_file_path = str(text_file_path)  # Ensure this is correctly defined and accessible here
            questions_extraction_target = targets["questions_extraction_target"]

            while True:
                extract_all_questions_and_parts(text_file_path, questions_extraction_target)
                # subprocess command to run the script with the path argument
                """subprocess.run([
                    "python",
                    str(questions_organiser_script_path),
                    text_file_path,  # Pass the full path to the text file as an argument
                    #questions_extraction_target
                    str(targets["questions_extraction_target"])
                ])"""

                print(f"{questions_organiser_script_path.name} has been executed successfully.")
                # To process 'fresh_integrated_identify_all_types.py'
                # user_choice_fiat = input("Proceed to module 'fresh_integrated_identify_all_types.py' for identifying question type questions? (y/n): ").strip().lower()
                # Usage example
                user_decision = validate_input(
                    "Press Enter to re-run the module for questions_extraction, Press 'C' to continue to module 'fresh_integrated_identify_all_types.py' for identifying question types.....",
                    ['C'])

                if user_decision == 'C':
                    print("Exiting the loop of extract_all_questions_and_parts and continuing with the next steps.")
                    break

            # if user_decision == '':
            #     extract_all_questions_and_parts(text_file_path, questions_extraction_target)

            #     print(f"{questions_organiser_script_path.name} has been executed successfully the second time.")

            # elif user_decision == 'C':
            # input("Press Enter to continue to module 'fresh_integrated_identify_all_types.py' for identifying question types .....")
            user_choice_fiat = 'y'
            if user_choice_fiat == 'y':
                identify_types_script_path = Path(
                    __file__).parent / "fresh_integrated_identify_all_types.py"
                # text_file_path = str(text_file_path)  # Ensure this is correctly defined and accessible here
                # Example of how to build the dictionary name dynamically
                dictionary_name = f"{batch_name}_{exam_name}_{exam_stage}_{subject_name}_{area_name}_{part_name}_{process_type_input}_answer_options_extracted_dictionary"

                # subprocess command to run the script with the path argument
                subprocess.run([
                    "python",
                    str(identify_types_script_path),
                    dictionary_name,
                    str(subfolder),
                    "--targets", targets_json
                    # Assuming subfolder_path is correctly defined in the context where this call is made
                ])
                print(f"{identify_types_script_path.name} has been executed successfully.")
                # To process 'fresh_integrated_extract_list_type_1_and_2_parts.py'
                # user_choice_fial = input("Proceed to module 'fresh_integrated_extract_list_type_1_and_2_parts.py'? (y/n): ").strip().lower()
                input("Press Enter to continue to module 'fresh_integrated_extract_list_type_1_and_2_parts.py.....")
                user_choice_fial = 'y'

                if user_choice_fial == 'y':
                    extract_list_parts_script_path = Path(
                        __file__).parent / "fresh_integrated_extract_list_type_1_and_2_parts.py"
                    # text_file_path = str(text_file_path)  # Ensure this is correctly defined and accessible here
                    # Example of how to build the dictionary name dynamically
                    dictionary_name = f"{batch_name}_{exam_name}_{exam_stage}_{subject_name}_{area_name}_{part_name}_{process_type_input}_answer_options_all_types_identified_consolidated_dictionary"

                    # subprocess command to run the script with the path argument
                    subprocess.run([
                        "python",
                        str(extract_list_parts_script_path),
                        dictionary_name,
                        str(subfolder),
                        # Assuming subfolder_path is correctly defined in the context where this call is made
                        "--other_info_batch", other_info_batch_json
                    ])
                    print(f"{extract_list_parts_script_path.name} has been executed successfully.")
                    input("Press Enter to continue to processing answers ...")
                    process_answers(file_name, questions_extraction_target, subfolder)
                else:
                    print("Operation cancelled by user.")
            else:
                print("Operation cancelled by user.")
        else:
            print("Operation cancelled by user.")

def process_answers(file_name, questions_extraction_target, subfolder):
    # Extract the first 8 parts of the file name and add "_ans" to it
    parts = file_name.split('_')
    if len(parts) < 9:
        print("Invalid file name format. Please ensure the file name has at least 9 parts.")
        return

    # Create a pattern to match files with the first 8 parts and "Ans" or "ans" followed by any string
    base_pattern = '_'.join(parts[:8]) + '_ans*'
    search_path = Path(f"C:/Users/HP/Desktop/Question Bank Trials/Input/")
    matched_files = list(search_path.glob(f"{base_pattern}.pdf")) + list(search_path.glob(f"{base_pattern}.PDF"))
    # answer_file_name = '_'.join(parts[:8]) + '_ans_' + '_'.join(parts[9:])
    # answer_file_path = Path(f"C:/Users/HP/Desktop/final project/question_bank_creation_from_pdf/Input/{answer_file_name}.pdf")
    if matched_files:
        answer_file_path = matched_files[0]  # Use the first matched file
        print(
            f"The corresponding answers file '{answer_file_path.name}' has been found. Proceeding with processing answers.")
        # Ensure that we pass the full file name with extension to process_pdf
        (process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name,
         part_name, batch_name, process_type_input, text_file_path) = process_pdf(answer_file_path.stem + '.pdf', False, questions_extraction_target)

        organize_answers(process_type, filename_prefix, subfolder, targets_json, answer_file_path.stem, area_name, part_name, text_file_path, questions_extraction_target)
    else:
        print(f"No corresponding answers file found matching pattern '{base_pattern}'. Please check and try again.")
        return

def organize_answers(process_type, filename_prefix, subfolder, targets_json, file_name_input, area_name, part_name, text_file_path, questions_extraction_target):

    # (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type_input) = create_directories_and_extract_names(file_name)
    # return pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type, process_type_input
    # user_choice = input("Proceed with organising answers? (y/n): ").strip().lower()

    targets = json.loads(targets_json)
    questions_extraction_target = targets["questions_extraction_target"]

    input("Press Enter to proceed with organising answers.....")
    user_choice = 'y'
    if user_choice == 'y':
        # input("Proceed to module 'fresh_answers_organiser.py' for extracting correct answers? Press Enter to continue... ")
        correct_answers_organiser_script_path = Path(__file__).parent / "fresh_integrated_correct_answers_organiser.py"
        # exam_name = f"{area_name}_{part_name}"
        # questions_extraction_target = targets_json["questions_extraction_target"]
        subprocess.run([
            "python",
            str(correct_answers_organiser_script_path),
            str(text_file_path),  # The path to the text file to process
            area_name,
            part_name,
            process_type,
            filename_prefix,  # Prefix for the filenames
            str(subfolder)
        ])

        parser = argparse.ArgumentParser(description="Extract correct answers.")

        print(f"{correct_answers_organiser_script_path.name} has been executed successfully.")
        print(f"The filename_prefix is: {filename_prefix}, Press Enter to continue....")

        # Call the check_and_return_both_dicts function here
        # check_and_return_both_dicts(filename_prefix, subfolder, questions_extraction_target)
        check_and_return_both_dicts(filename_prefix, subfolder, str(questions_extraction_target))

    else:
        print("Operation cancelled by user.")

def main():
    print("Choose an option:")
    print("1. Use PDF and pypdf2")
    print("2. Use PDF and OCR Tesseract with 2 to 1 column")
    print("3. Use text file")
    print("4. Process only Correct Answers from PDF")
    print("5. Option 5")
    print("6. Option 6")
    # choice = input("Enter your choice (1, 2, 3, 4, 5 or 6): ")
    choice = validate_number("Enter your choice (1, 2, 3, 4, 5 or 6): ", min_val=1, max_val=6)

    # targets = {}
    # targets["questions_extraction_target"] = validate_number("Enter target for questions_extraction_target: ", 0, 10000)
    # targets_json = json.dumps(targets)

    if choice in [1, 2]:
        file_name_input = input(
            "Enter the file name without extension (e.g., UPSC_Pre_GS1_History Medieval Que Only Pages 15 - 21): ")
        file_name = file_name_input + ".pdf"  # Add .pdf extension
        # pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type_input = create_directories_and_extract_names(
        #     file_name)
        (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type,
         exam_name,
         exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
         process_type_input) = create_directories_and_extract_names(file_name)

        # initializing questions_extraction_target to None for first call for process_type == "Questions"
        questions_extraction_target = None

        if process_type == "Questions":
            process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path = process_pdf(
            file_name, True, questions_extraction_target)
            # Extract questions_extraction_target from targets_json
            targets = json.loads(targets_json)
            questions_extraction_target = targets["questions_extraction_target"]
        # print(f"File Name is {pdf_file_path},Exam Name : {exam_name},Exam Stage : {exam_stage},Subject Name : {subject_name},Area Name: {area_name},Part Name: {part_name},Process Type: {process_type}")

        elif process_type == "Answers":
            process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path = process_pdf(
                file_name, False, questions_extraction_target)

    elif choice == 3:
        file_name_input = input("Enter the file name without extension (e.g., text_file_name): ")
        file_name = file_name_input + ".txt"
        # pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type_input = create_directories_and_extract_names(
        #     file_name)
        (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type,
         exam_name,
         exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
         process_type_input) = create_directories_and_extract_names(file_name)

        # initializing questions_extraction_target to None for first call for process_type == "Questions"
        questions_extraction_target = None

        if process_type == "Questions":
            process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path = process_text_file(
                file_name, True, questions_extraction_target)
            # Extract questions_extraction_target from targets_json
            targets = json.loads(targets_json)
            questions_extraction_target = targets["questions_extraction_target"]
        # print(f"File Name is {pdf_file_path},Exam Name : {exam_name},Exam Stage : {exam_stage},Subject Name : {subject_name},Area Name: {area_name},Part Name: {part_name},Process Type: {process_type}")

        elif process_type == "Answers":
            process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path = process_text_file(
                file_name, False, questions_extraction_target)

    elif choice == 4:
        file_name_input = input(
            "Enter the file name without extension (e.g., Disha_26_2020_UPSC_Pre_GS1_History_Ancient_Ans_Only Pages 9 - 14): ")
        file_name = file_name_input + ".pdf"  # Add .pdf extension
        # pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type, exam_name, exam_stage, subject_name, area_name, part_name, text_file_path, batch_name, process_type_input = create_directories_and_extract_names(
        #     file_name)
        (pdf_file_path, output_folder_1, output_folder_2, subfolder, filename_prefix, dump_folder, process_type,
         exam_name,
         exam_stage, subject_name, area_name, part_name, text_file_path, batch_name,
         process_type_input) = create_directories_and_extract_names(file_name)

        # initializing questions_extraction_target to None for the only call for process_type == "Answers" as this
        # Option 4 applies only to Answers PDF
        questions_extraction_target = None
        # questions_extraction_target = validate_number("Enter target for questions_extraction_target: ", 0,10000)

        if process_type == "Answers":
            process_type, filename_prefix, subfolder, targets_json, exam_name, exam_stage, subject_name, area_name, part_name, batch_name, process_type_input, text_file_path = process_pdf(
                file_name, True, questions_extraction_target)

    else:
        print(f"Option {choice} is not yet implemented.")
        return

    # brought here to handle inputting the questions_extraction_target only once and enable it's
    # usage in both the functions - organize_answers and organize_questions

    targets = json.loads(targets_json)

    if process_type == "Questions":
        organize_questions(process_type, filename_prefix, subfolder, targets, targets_json, exam_name, exam_stage,
                           subject_name, area_name, part_name, batch_name, process_type_input, file_name_input)

    elif process_type == "Answers":
        # questions_extraction_target = targets["questions_extraction_target"]
        organize_answers(process_type, filename_prefix, subfolder, targets_json, file_name_input, area_name, part_name, text_file_path, questions_extraction_target)



if __name__ == "__main__":
    main()
