import pdfplumber
from typing import List
from pdf_to_markdown.with_pdfplumber import extract_lines
from tools.write_to_csv import write_to_csv

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


def recursive_char(chars, split_characters, chunk_size, overlap):

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

        # print(type(combine_chunk))

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
        else:
            empty_line_count = 0

        if empty_line_count == 2:
            empty_line_count = -10000000
            new_lines.append("")
            new_metadatas.append(line_metadatas[line_id])  # Keep the metadata in sync
        if line.strip() != "":
            new_lines.append(line)
            new_metadatas.append(line_metadatas[line_id])

    return new_lines, new_metadatas

def transform_to_chunk(chars):
    text = ""

    for char in chars:
        text += char["text"]

    final_chunk = {
        "filename": chars[0]["filename"],
        "page_range": (chars[0]["page"], chars[-1]["page"]),
        "line_range": (chars[0]["line_id"], chars[-1]["line_id"]),
        "text": text
    }

    return final_chunk
    

def split_text(lines, line_metadatas, split_characters):
    """ add hash to header lines """

    split_empty = input("Split empty line? (Y/n) ")
    chunk_size = int(input("Chunk Size: "))
    overlap = int(input("Overlap Size: "))

    if split_empty != "n":
        lines, line_metadatas = split_empty_lines(lines, line_metadatas)
        split_characters = [''] + split_characters


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

    # print(split_results)

    chunks = []

    for chunk in split_results:
        chunks.append(transform_to_chunk(chunk))

    return chunks


def main():
    filename = input("File Name: ")
    input_file = "data/" + filename + ".pdf"
    lines, line_metadatas, header_sizes = extract_lines(input_file)
    final_chunks = split_text(lines, line_metadatas, ["。", "\n", "，", " "])

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

        write_to_csv(f"csv/{filename}.csv", fields, rows)


if __name__ == "__main__":
    main()
