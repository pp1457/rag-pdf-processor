from typing import List
from pdf_to_markdown.with_pdfplumber import extract_lines
from tools.save_result import save_result
from tools.get_embedding import add_embeddings
from tools.split_characters import split_by_characters
from tools.split_lines import split_on_empty_lines
from tools.transform_to_chunk import transform_to_chunk


def recursive_char(chars: List[dict], split_characters: List[str], chunk_size, overlap):
    """ recursive char text splitters """

    tmp_chunks = []

    if len(chars) > chunk_size:
        tmp_chunks = split_by_characters(chars, [split_characters[0]])
    else:
        return [chars]

    last_overlap = []
    output = []

    for tmp_chunk in tmp_chunks:

        combine_chunk = last_overlap + tmp_chunk

        if overlap < len(tmp_chunk):
            last_overlap = tmp_chunk[len(tmp_chunk) - overlap: len(tmp_chunk)]
        else:
            last_overlap = []
            overlap = 0

        tmp_result = recursive_char(combine_chunk, split_characters[1:], chunk_size, overlap)

        for final_chunk in tmp_result:
            output.append(final_chunk)

    return output
    

def split_text(lines: List[dict], split_characters: List[str], yes_split_empty_line, chunk_size, overlap):
    """ split text by recursive char """

    if yes_split_empty_line != "n":
        lines = split_on_empty_lines(lines)
        split_characters = [""] + split_characters

    all_chars = []

    for line in lines:
        for char in line["text"]:
            all_chars.append({
                "text": char,
                "line_id": line["line_id"],
                "page": line["page"],
                "filename": line["file_path"]
            })

    split_results = recursive_char(all_chars, split_characters, chunk_size, overlap)

    chunks = []

    for chunk in split_results:
        chunks.append(transform_to_chunk(chunk))

    return chunks


def main():
    """ main """

    filename = input("File Name: ")
    input_file = "data/" + filename + ".pdf"

    lines, _ = extract_lines(input_file)

    yes_split_empty_line = input("Split empty line? (Y/n) ")
    chunk_size = int(input("Chunk Size: "))
    overlap = int(input("Overlap Size: "))

    final_chunks = split_text(lines, ["。", ".", "\n", "  ", " "], yes_split_empty_line, chunk_size, overlap)

    yes_add_embedding = input("Add embedding? (y/N) ")

    if yes_add_embedding == "y":
        final_chunks = add_embeddings(final_chunks)

    save_result(final_chunks, "recursive_char", filename)


if __name__ == "__main__":
    main()
