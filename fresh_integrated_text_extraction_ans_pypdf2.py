import PyPDF2
import os
from pathlib import Path
import argparse
import re

def extract_text_from_pdf(pdf_path, process_type):
    text = ''
    hints_and_solutions_found = False
    page_texts = []  # To store text of each page
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_number, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ""  # Ensure page_text is not None
                page_texts.append(page_text)
                if not page_text:
                    print(f"Warning: No text found on page {page_number}")

            # Combine all pages text to apply the regex search on the full text
            full_text = '\n'.join(page_texts)
            input(f"The full_text is {full_text}, Press Enter to continue....")

            # Regex to find "Hints & Solutions" or "Hints And Solutions"
            hints_pattern = r"Hints\s{0,4}(&|And)\s{0,4}Solutions"
            matches = list(re.finditer(hints_pattern, full_text, re.IGNORECASE))

            if matches:
                hints_and_solutions_found = True
                for match in matches:
                    start_index = match.start()
                    # Find the page number by checking the index range
                    cumulative_length = 0
                    for i, page_text in enumerate(page_texts):
                        cumulative_length += len(page_text)
                        if cumulative_length > start_index:
                            page_with_match = i
                            break

                    # Check the number of characters before the match in the page text
                    characters_before_match = start_index - (cumulative_length - len(page_texts[page_with_match]))
                    input(f"The characters_before_match is {characters_before_match}, Press Enter to continue....")

                    # If match is at the beginning of the page
                    if characters_before_match < 10:
                        # Remove "Hints & Solutions" and any preceding text on that page
                        page_texts[page_with_match] = re.sub(r'^.*Hints\s{0,4}(&|And)\s{0,4}Solutions', '',
                                                             page_texts[page_with_match], flags=re.IGNORECASE)
                        if process_type == "Answers":
                            # Skip modifying pages if processing for "Questions"
                            page_texts = page_texts[page_with_match + 1:] if page_with_match < len(
                                page_texts) - 1 else []
                            break

                    # Join page texts based on process type
                    # Join page texts based on process type
                    if process_type == "Questions":
                        text = '\n'.join(page_texts)
                    elif process_type == "Answers":
                        text = '\n'.join(page_texts)

    except Exception as e:
        print(f"Error reading PDF file: {e}")

    return text.strip(), hints_and_solutions_found

def main():
    parser = argparse.ArgumentParser(description='Extract text from a PDF file.')
    parser.add_argument('pdf_file', help='The path to the PDF file to be processed.')
    parser.add_argument('output_path', help='The path where the extracted text should be saved.')
    parser.add_argument('process_type', help='The type of processing (Questions or Answers) indicating how to handle "Hints & Solutions".')

    args = parser.parse_args()

    pdf_file_path = Path(args.pdf_file)
    output_path = Path(args.output_path)
    process_type = args.process_type.capitalize()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    extracted_text, hints_found = extract_text_from_pdf(pdf_file_path, process_type)

    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    if hints_found:
        print(f"Hints & Solutions section was handled for process type '{process_type}'.")
    else:
        print("No Hints & Solutions section was found.")

    print(f"Text extracted and saved to {output_path}")

if __name__ == "__main__":
    main()
