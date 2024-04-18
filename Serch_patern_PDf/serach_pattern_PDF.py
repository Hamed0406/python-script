import fitz  # PyMuPDF
import os
import argparse

def search_pdfs(root_directory, pattern):
    results_path = os.path.join(root_directory, "search_results.txt")
    with open(results_path, "a") as results_file:  # Open the results file in append mode
        for root, dirs, files in os.walk(root_directory):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(root, file)
                    try:
                        doc = fitz.open(pdf_path)
                        for page in doc:
                            text = page.get_text()
                            if pattern in text:
                                print(f"Pattern found in {pdf_path}")
                                results_file.write(f"Pattern found in {pdf_path}\n")
                                # Write the surrounding text of the pattern to the results file
                                start = text.find(pattern)
                                end = start + len(pattern)
                                # Capture more context around the pattern, adjust numbers as needed
                                context = text[max(0, start-30):min(end+30, len(text))]
                                results_file.write(f"Context: {context}\n\n")
                        doc.close()
                    except Exception as e:
                        print(f"Failed to read {pdf_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Search for a pattern in all PDF files within a specified directory and log results.")
    parser.add_argument("directory", type=str, help="The root directory to search for PDF files.")
    parser.add_argument("pattern", type=str, help="The pattern to search for within the PDF files.")
    args = parser.parse_args()

    search_pdfs(args.directory, args.pattern)

if __name__ == "__main__":
    main()

