""" pdf to markdown with pymupdf4llm """
from typing import List

import pymupdf4llm

def pdf_to_markdown(input_path) -> List[dict]:
    """ pdf to markdown """

    md_pages = pymupdf4llm.to_markdown(input_path, page_chunks = True)

    return md_pages

def main():
    """ main """

    file_name = input("File Name: ")

    input_path = "data/" + file_name + ".pdf"

    print(pdf_to_markdown(input_path))


if __name__ == "__main__":
    main()
