from typing import List
import pymupdf4llm

def pdf_to_markdown(file_name: str) -> List[dict]:
    input_file = "data/" + file_name + ".pdf"

    md_chunk = pymupdf4llm.to_markdown(input_file, page_chunks = True)

    return md_chunk


if __name__ == "__main__":
    file_name = input("File Name: ")
    print(pdf_to_markdown(file_name))

