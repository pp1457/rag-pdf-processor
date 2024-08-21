"""chunk by markdown"""
import pathlib
import re
from typing import List
from pdf_to_markdown.with_pdfplumber import pdf_to_markdown
from tools.markdown_utils import contains_strong_text, count_leading_hash
from tools.save_result import save_result

def get_md_pages(filename, save_to_new_file) -> List[dict]:
    """split pdf into markdown pages"""

    output_file = "markdown/" + filename + ".md"
    md_pages = pdf_to_markdown(filename)

    if save_to_new_file == "y":
        md_content = ""
        for page in md_pages:
            md_content += page["text"]
        pathlib.Path(output_file).write_bytes(md_content.encode())
        print(f"Saved as {output_file}")

    return md_pages


def context(contents) -> str:
    """return concatenation of contents"""

    return "".join(contents)


def split_text(md_pages: List[dict], split_level, split_on_strong_text) -> List[dict]:
    """split text into chunks based on markdown"""

    final_chunks = []
    stack = []
    contents = []


    total_pages = len(md_pages)

    empty_line = 0
    line_id = 0

    cur_section = ""

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

            if contains_strong_text(line) and split_on_strong_text != "n":
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

                    line_range = (stack[-1]["line"], line_id - 1)
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
                    "line": line_id, 
                    "lev": hash_count,
                    "page": page["metadata"]["page"] 
                })

            else:

                if (
                    (last_line.strip() == "" and re.match(r"^\s*-----\s*$", line)) or
                    (line.strip() == "") or
                    (re.match(r'^\s*(Page\s+\d+|\d+|\d+/\d+)\s*$', line.strip()))
                   ):
                    
                    last_line = ""
                    continue

                if line_id == 1:
                    stack.append({
                        "line": line_id,
                        "lev": 100,
                        "page": page["metadata"]["page"]
                    })

                cur_section += line + "\n"

            last_line = line

    return final_chunks



def main():
    """ main """
    filename = input("File Name: ")
    save_to_new_file = input("Save to new file? (y/N) ")
    md_pages = get_md_pages(filename, save_to_new_file)

    split_level = int(input("Enter the number of # (between 1 and 4): "))
    split_on_strong_text = input("Split on **{Strong Text}**? (Y/n) ")

    final_chunks = split_text(md_pages, split_level, split_on_strong_text)

    save_result(final_chunks, "by_markdown", filename)
        

if __name__ == "__main__":
    main()
