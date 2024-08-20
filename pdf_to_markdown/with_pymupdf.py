""" pdf to markdown with pymupdf4llm """
from typing import List

import pymupdf4llm

def pdf_to_markdown(file_name) -> List[dict]:
    """ main """
    input_file = "data/" + file_name + ".pdf"

    md_pages = pymupdf4llm.to_markdown(input_file, page_chunks = True)

    return md_pages


if __name__ == "__main__":
    file_name = input("File Name: ")
    print(pdf_to_markdown(file_name))
