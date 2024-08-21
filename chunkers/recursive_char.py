import pdfplumber
from typing import List
from pdf_to_markdown.with_pdfplumber import extract_lines
from tools.save_result import save_result

def split(chars, split_character):
    result = []
    cur = []
    for char in chars:
        cur.append(char)
        if char["text"] == split_character:
            result.append(cur)
            cur = []
    if cur:
        result.append(cur)

    return result


def content(chars):
    output = "".join(char["text"] for char in chars)
    return output


def recursive_char(chars: List[dict], split_characters: List[str], chunk_size, overlap):

    tmp_chunks = []

    if len(chars) > chunk_size:
        tmp_chunks = split(chars, split_characters[0])
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
    

def split_empty_lines(lines, line_metadatas):

    new_lines = []
    new_metadatas = []
    empty_line_count = 0

    for line_id, line in enumerate(lines):
        if line.strip() == "":
            empty_line_count += 1
            if empty_line_count == 1:
                empty_line_count = -10000000
                new_lines.append("")
                new_metadatas.append(line_metadatas[line_id])
        else:
            empty_line_count = 0
            new_lines.append(line)
            new_metadatas.append(line_metadatas[line_id])

    return new_lines, new_metadatas

def transform_to_chunk(chars):
    """ transform from chars to chunks """
    text = ""

    for char in chars:
        text += char["text"]

    final_chunk = {
        "text": text,
        "page_range": (chars[0]["page"], chars[-1]["page"]),
        "line_range": (chars[0]["line_id"], chars[-1]["line_id"]),
        "filename": chars[0]["filename"],
    }

    return final_chunk
    

def split_text(lines: List[str], line_metadatas: List[dict], split_characters: List[str], split_empty_line, chunk_size, overlap):
    """ split text by recursive char """

    if split_empty_line != "n":
        lines, line_metadatas = split_empty_lines(lines, line_metadatas)
        split_characters = [""] + split_characters


    page_content = ""
    last_page = -1

    all_chars = []

    for line_id, line in enumerate(lines):
        line = line.strip()
        for char in line:
            all_chars.append({
                "text": char,
                "line_id": line_id,
                "page": line_metadatas[line_id]["page"],
                "filename": line_metadatas[line_id]["file_path"]
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

    lines, line_metadatas, header_sizes = extract_lines(input_file)

    split_empty_line = input("Split empty line? (Y/n) ")
    chunk_size = int(input("Chunk Size: "))
    overlap = int(input("Overlap Size: "))

    final_chunks = split_text(lines, line_metadatas, ["。", ".", "\n", "  ", " "], split_empty_line, chunk_size, overlap)

    save_result(final_chunks, "recursive_char", filename)


if __name__ == "__main__":
    main()
