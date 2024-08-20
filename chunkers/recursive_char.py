import pdfplumber
from typing import List

def extract_chars(pdf_path):
    line_id = 0
    all_chars = []

    with pdfplumber.open(pdf_path) as pdf:
        for i in range(len(pdf.pages)):
            chars = pdf.pages[i].extract_text(layout=True)

            print(len(chars.split("\n\n")))

#            last_bottom = -1
#
#            for char in chars:
#                if char["top"] > last_bottom:
#                    line_id += 1
#                char["line"] = line_id
#                all_chars.append(char)

    return all_chars

def main():
    file_name = input("File Name: ")
    input_file = "data/" + file_name + ".pdf"
    all_chars = extract_chars(input_file)
    cnt = 0

    content = ""
    for char in all_chars:
        content += char["text"]

    print(content)



if __name__ == "__main__":
    main()
