"""chunk by markdown"""
import pathlib
import re
from typing import List
from pdf_to_markdown.with_pdfplumber import pdf_to_markdown
from tools.write_to_csv import write_to_csv

def get_md_pages() -> List[dict]:
    """split pdf into markdown pages"""

    filename = input("File Name: ")
    save_to_new_file = input("Save to new file? (y/N) ")
    output_file = "markdown/" + filename + ".md"
    md_pages = pdf_to_markdown(filename)

    if save_to_new_file == "y":
        md_content = ""
        for page in md_pages:
            md_content += page["text"]
        pathlib.Path(output_file).write_bytes(md_content.encode())
        print(f"Saved as {output_file}")

    return md_pages

def contains_strong_text(s):
    """check if string s contain strong text"""

    # Regular expression to match **strong text**
    pattern = r'\*\*[^*]+\*\*'
    return bool(re.search(pattern, s))

def count_leading_hash(s):
    """count leading hash in string s"""
    s = s.lstrip()
    count = 0
    for char in s:
        if char == "#":
            count += 1
        else:
            break

    if count == 0:
        count = 100

    return count

def context(contents) -> str:
    """return concatenation of contents"""

    output = ""
    for _, content in enumerate(contents):
#        print(contents[i])
#        print("---------")
        output += content

# if contents:
#     for line in contents[-1].splitlines():
#         output += line.lstrip("#")

    return output


def split_text(md_pages: List[dict]) -> List[dict]:
    """split text into chunks based on markdown"""
    final_chunks = []

    split_level = int(input("Enter the number of # (between 1 and 4): "))
    split_on_strong = input("Split on **{Strong Text}**? (Y/n) ")

    line_id = 0

    stack = []

    contents = []
    cur_section = "\n"

    total_pages = len(md_pages)

    empty_line = 0

    for page_index, page in enumerate(md_pages):

        last_line = ""

        lines = page["text"].splitlines()

        if page_index == total_pages - 1:
            lines.append("#")

        for _, line in enumerate(lines):

            line_id += 1

            hash_count = count_leading_hash(line)

            if hash_count > split_level:
                line = line.lstrip("#")

            if contains_strong_text(line) and not split_on_strong == "n":
                hash_count = split_level

            if line.strip() == "":
                empty_line += 1
            else:
                empty_line = 0

            if empty_line >= 2:
                hash_count = 1
                empty_line = -10000000

            if split_level >= hash_count:

                if stack:
                    contents.append(cur_section)
                    cur_section = line + "\n"

                if stack and stack[-1]["lev"] >= hash_count:
                    line_range = (stack[-1]["pos"], line_id - 1)
                    page_range = (stack[-1]["page"], page["metadata"]["page"])
                    text = context(contents)

                    final_chunk = {
                        "filename": page["metadata"]["file_path"],
                        "page_range": page_range,
                        "line_range": line_range,
                        "text": text
                    }

                    final_chunks.append(final_chunk)


                while stack and stack[-1]["lev"] >= hash_count:
                    stack.pop()
                    contents.pop()

                stack.append({
                    "pos": line_id, 
                    "lev": hash_count,
                    "page": page["metadata"].get("page") 
                })
            else:
                if (
                    (last_line.strip() == "" and re.match(r"^\s*-----\s*$", line)) or
                     line.strip() == "" or
                     re.match(r'^\s*(Page\s+\d+|\d+|\d+/\d+)\s*$', line.strip())
                   ):
                    last_line = ""
                    continue
                if line_id == 1:
                    stack.append({"pos": line_id, "lev": 100, "page": page["metadata"]["page"]})
                cur_section += line + "\n"

            last_line = line


    return final_chunks


def main():
    """ main """
    md_pages = get_md_pages()
    final_chunks = split_text(md_pages)

    chunk_id = 0

    with open("output.txt", "w", encoding="utf-8") as file:
        fields = ["Chunk ID", "Text", "Page Range", "Line Range", "Filename"]
        rows = []
        
        for chunk in final_chunks:
            chunk_id += 1
            row = []

            file.write("\n-----------------------\n")
            row.append(chunk_id)
            row.append(chunk["text"])
            row.append(chunk["page_range"])
            row.append(chunk["line_range"])
            row.append(chunk["filename"])

            rows.append(row)

            file.write(f"Chunk {chunk_id}: \n\n")
            file.write("Text: \n")
            file.write(chunk["text"])
            file.write("\n\nPage Range: ")
            file.write(str(chunk["page_range"]))
            file.write("\n\nLine Range: ")
            file.write(str(chunk["line_range"]))
            file.write("\n\nFilename: ")
            file.write(str(chunk["filename"]))

        write_to_csv(f"csv/fubon.csv", fields, rows)


        

if __name__ == "__main__":
    main()
