import os
import pandas as pd
import time
import shutil

# Folder path
folder_path = r'C:\Users\HP\Desktop\Question Bank Trials\Input'
renamed_folder_path = os.path.join(folder_path, 'renamed files for input')
os.makedirs(renamed_folder_path, exist_ok=True)

# Function to validate and process input_file names
def validate_and_process_file(input_file):
    file_path = os.path.join(folder_path, input_file)
    valid_for_renaming = False

    if not (file_path.lower().endswith('.pdf') or file_path.lower().endswith('.txt')):
        file_pdf_or_text = False
        input(f"{input_file} is not a PDF or TXT file. Press Enter to continue....")
        return None, False, None, f"{input_file} is not a PDF or TXT input_file., Press Enter to continue...."
    else:
        file_pdf_or_text = True
        f"{input_file} is a PDF or TXT input_file., Press Enter to continue...."

    parts = input_file.replace('.pdf', '').replace('.txt', '').replace(' ', '_').split('_')
    if len(parts) < 9 or parts[8].lower() not in ['que', 'ans']:
        print(f"len(parts) is: {len(parts)}")
        print(parts)
        file_parts_length = False
        input(f"file_parts_length is: {file_parts_length}, and {input_file} does not meet the naming criteria. Press Enter to continue....")
        return None, False, None, f"{input_file} does not meet the naming criteria., Press Enter to continue...."
    else:
        print(f"len(parts) is: {len(parts)}")
        file_parts_length = True
        f"{input_file} meets the naming criteria., Press Enter to continue...."

    # Create new input_file name with underscores replacing spaces
    new_file_name = '_'.join(parts) + os.path.splitext(input_file)[1]

    if file_pdf_or_text and file_parts_length:
        valid_for_renaming = True

    input(
        f"For the input_file named: {input_file}, file_pdf_or_text is: {file_pdf_or_text}, file_parts_length is: {file_parts_length}, and valid_for_renaming is: {valid_for_renaming}, Press Enter to continue....")
    return input_file, valid_for_renaming, new_file_name, None

def copy_file_with_retry(old_file_path, new_file_path, retries=3, delay=1):
    for attempt in range(retries):
        try:
            shutil.copy2(old_file_path, new_file_path)
            return True
        except PermissionError as e:
            print(f"Attempt {attempt + 1}: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    return False

def rename_files ():
    # List all files in the folder
    all_files = os.listdir(folder_path)

    # Initialize an empty list to store the data
    data = []

    # Iterate through all files
    for file in all_files:
        input_file, valid_for_renaming, new_file_name, error = validate_and_process_file(file)
        if valid_for_renaming and new_file_name:
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(renamed_folder_path, new_file_name)
            if copy_file_with_retry(old_file_path, new_file_path):
                # Add the input_file name and its parts to the data list
                parts = new_file_name.replace('.pdf', '').replace('.txt', '').split('_')
                parts = [part.lower() for part in parts]
                last_part = parts[-1]
                second_last_part = 'pages'
                data.append([new_file_name] + parts[:-1] + [second_last_part, last_part])
                input(
                    f"The input_file named {input_file} for which valid_for_renaming is {valid_for_renaming}, has been renamed to {new_file_name}, Press Enter to continue....")
            else:
                print(f"Failed to rename {file} after multiple attempts.")
        else:
            print(error)

    if data:
        # Convert the data to a DataFrame
        columns = ['PDF/ TXT File Names'] + [f'Part {i + 1}' for i in range(len(max(data, key=len)) - 1)]
        pdf_df = pd.DataFrame(data, columns=columns)

        # Write to Excel input_file in the same folder
        output_path = os.path.join(folder_path, 'PDF_TXT_File_Names_with_Parts.xlsx')
        input(f"Press enter to continue to create excel named: {output_path}")
        pdf_df.to_excel(output_path, index=False)

        print(f'Successfully written PDF/ TXT names and parts to {output_path}')
        print(f'Renamed files moved to {renamed_folder_path}')

    else:
        print("No valid files found to rename.")


def main():
    print(
        "This script will process PDF and TXT files in the specified folder, rename them, and move them to a new directory.")
    proceed = input("Do you want to proceed? (y/n): ").strip().lower()

    if proceed == 'y':
        rename_files()
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
