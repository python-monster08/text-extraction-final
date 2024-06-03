import PyPDF2
import os
from pathlib import Path
import argparse
import re

from input_validation import validate_yes_no, validate_number

def extract_text_from_pdf(pdf_path, process_type):
    text = ''
    hints_and_solutions_found = False
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            # modification to handle "Hints " Solutions" or the correct answer portion in the pdf
            # at this stage itself as it otherwise messes up the questions extraction later
            hints_and_solutions_found = False
            for page_number, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if not page_text:
                    print(f"Warning: No text found on page {page_number}")
                text += page_text + '\n'

            # Regex to find "Hints & Solutions" or "Hints And Solutions"
            hints_pattern = r"Hints\s{0,4}(&|And)\s{0,4}Solutions"
            # match = re.search(hints_pattern, text, re.IGNORECASE)
            matches = list(re.finditer(hints_pattern, text, re.IGNORECASE))

            # Print the matches for debugging
            for i, match in enumerate(matches, start=1):
                print(f"Match {i}: Found 'Hints & Solutions' at position {match.start()} to {match.end()}")

            if matches:
                hints_and_solutions_found = True
                if process_type == "Questions":
                    # Keep everything before "Hints & Solutions"
                    # text = text[:match.start()]
                    print("Extracting text before the first match.")
                    print(
                        f"Text before match: {text[:matches[0].start()][:500]}...")  # Print first 500 characters for verification
                    input(f"Please check the Text before match above and Press Enter to continue.....")
                    text = text[:matches[0].start()]
                elif process_type == "Answers":
                    # Keep everything after "Hints & Solutions"
                    # text = text[match.end():]
                    print("Extracting text after the last match.")
                    print(
                        f"Text after match: {text[matches[-1].end():][:500]}...")  # Print first 500 characters for verification
                    input(f"Please check the Text after the match above and Press Enter to continue.....")
                    text = text[matches[-1].end():].strip()

                    # Additionally, trim any leading newlines or whitespace
                    text = text.lstrip()

    except Exception as e:
        print(f"Error reading PDF file: {e}")

    return text, hints_and_solutions_found


def main():
    # Setup argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('pdf_file', help='The path to the PDF file to be processed.')
    parser.add_argument('output_path', help='The path where the extracted text should be saved.')
    parser.add_argument('process_type',
                        help='The type of processing (ques or ans) indicating how to handle "Hints & Solutions".')

    args = parser.parse_args()

    pdf_file_path = Path(args.pdf_file)
    output_path = Path(args.output_path)
    process_type = args.process_type

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"In the function 'fresh_text_extraction_pypdf2.py', pdf_file_path is : {pdf_file_path}\n output_path: {output_path}")
    # input("Check the above in the function 'fresh_text_extraction_pypdf2.py' and Press Enter to continue....")

    # Extract text from the PDF
    # extracted_text = extract_text_from_pdf(pdf_file_path)
    extracted_text, hints_found = extract_text_from_pdf(pdf_file_path, process_type)

    # Write the extracted text to the specified output path
    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    if hints_found:
        print(f"Hints & Solutions section was handled for process type '{process_type}'.")
        print(f"hints_and_solutions_found is: {hints_found}, please check extracted text file")
        input(f"Press Enter to continue....")
    else:
        print("No Hints & Solutions section was found.")

    print(f"Text extracted and saved to {output_path}")

    print(f"Text extracted and saved to {output_path}")


if __name__ == "__main__":
    main()

    # pdf_file_name = input("Enter the name of the PDF file (without the .pdf extension): ")
    # create_directories_and_extract_text(pdf_file_name)

