"""chunk by markdown"""
import pathlib
import re
from typing import List
from rag_pdf_processor.pdf_to_markdown.with_pdfplumber import pdf_to_markdown
from rag_pdf_processor.tools.markdown_utils import contains_strong_text, count_leading_hash
from rag_pdf_processor.tools.save_result import save_result
from rag_pdf_processor.tools.get_embedding import add_embeddings

def get_md_pages(filename, save_to_new_file, header_ratio = 0.09, footer_ratio = 0.91, yes_size_round_up = "Y") -> List[dict]:
    """split pdf into markdown pages"""

    md_pages = pdf_to_markdown(filename, header_ratio, footer_ratio, yes_size_round_up)

    if save_to_new_file == "y":
        output_file = "markdown/" + filename + ".md"
        output_dir = pathlib.Path(output_file).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        md_content = ""
        for page in md_pages:
            md_content += page["text"]
        pathlib.Path(output_file).write_bytes(md_content.encode())
        print(f"Saved as {output_file}")

    return md_pages


def context(contents) -> str:
    """return concatenation of contents"""

    return "".join(contents)


def split_text(md_pages: List[dict], split_level, yes_split_on_strong_text) -> List[dict]:
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

            hash_count = count_leading_hash(line)

            if hash_count > split_level:
                line = line.lstrip("#")

            if contains_strong_text(line) and yes_split_on_strong_text != "n":
                hash_count = split_level

            if line.strip() == "":
                empty_line += 1
            else:
                line_id += 1
                empty_line = 0

            if empty_line >= 2:
                hash_count = 1
                empty_line = -10000000

            if split_level >= hash_count:

                if stack:
                    contents.append(cur_section)

                if line.strip() != "":
                    cur_section = line + "\n"
                else:
                    cur_section = ""

                if stack and stack[-1]["lev"] >= hash_count:

                    line_range = (stack[-1]["line"], line_id - 1)
                    page_range = (stack[-1]["page"], page["metadata"]["page"])
                    text = context(contents)

                    if text.strip() != "":
                        final_chunk = {
                            "text": text,
                            "page_range": page_range,
                            "line_range": line_range,
                            "filename": page["metadata"]["file_path"],
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
    header_ratio = float(input("Header Ratio: ") or 0.09)
    footer_ratio = float(input("Footer Ratio: ") or 0.91)
    yes_size_round_up = (input("Size round up? (Y/n) ") or "Y")
    split_level = int(input("Enter the number of # (between 1 and 6): "))
    yes_split_on_strong_text = input("Split on **{Strong Text}**? (Y/n) ")
    yes_add_embedding = input("Add embedding? (y/N) ")

    model_name = "no"
    if yes_add_embedding == "y":
        model_name = input("Chunk Embedding Model: ")

    md_pages = get_md_pages(filename, save_to_new_file, header_ratio, footer_ratio, yes_size_round_up)

    final_chunks = split_text(md_pages, split_level, yes_split_on_strong_text)

    if yes_add_embedding == "y":
        final_chunks = add_embeddings(final_chunks, model_name)

    chunking_method = "by_markdown|number_of_hash=" + str(split_level)

    save_result(final_chunks, chunking_method, filename, model_name)
        

if __name__ == "__main__":
    main()
