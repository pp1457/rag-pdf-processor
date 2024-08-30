from typing import List
from rag_pdf_processor.pdf_to_markdown.with_pdfplumber import extract_lines
from rag_pdf_processor.tools.save_result import save_result
from rag_pdf_processor.tools.get_embedding_openai import add_embeddings
from rag_pdf_processor.tools.split_characters import split_by_characters
from rag_pdf_processor.tools.split_lines import split_on_empty_lines
from rag_pdf_processor.tools.transform_to_chunk import transform_to_chunk


def recursive_char(
    chars: List[dict],
    split_characters: List[str],
    chunk_size,
    overlap
):
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
            last_overlap = tmp

        tmp_result = recursive_char(combine_chunk, split_characters[1:], chunk_size, overlap)

        for final_chunk in tmp_result:
            output.append(final_chunk)

    return output
    
def split_text(
    input_path,
    header_ratio = 0.09,
    footer_ratio = 0.91,
    split_characters = ["。", "\n", "  ",  ",", ".", " "],
    yes_split_empty_line = "Y",
    chunk_size = 1000,
    overlap = 100,
    yes_add_embedding = "N",
    chunk_embedding_model = "no-embedding"
):
    """ split text by recursive char """


    lines, _ = extract_lines(
        input_path,
        header_ratio,
        footer_ratio
    )

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

    if yes_add_embedding == "y":
        chunks = add_embeddings(chunks, chunk_embedding_model)

    return chunks


def main():
    """ main """

    filename = input("File Name: ")
    input_path = "data/" + filename + ".pdf"
    header_ratio = float(input("Header Ratio: ") or 0.09)
    footer_ratio = float(input("Footer Ratio: ") or 0.91)

    yes_split_empty_line = input("Split on empty line? (Y/n) ")
    chunk_size = int(input("Chunk Size: "))
    overlap = int(input("Overlap Size: "))

    yes_add_embedding = input("Add embedding? (y/N) ")
    chunk_embedding_model = "no-embedding"
    if yes_add_embedding == "y":
        chunk_embedding_model = input("Chunk Embedding Model: ")

    final_chunks = split_text(
        input_path,
        header_ratio,
        footer_ratio,
        ["。", "\n", "  ",  ",", ".", " "],
        yes_split_empty_line,
        chunk_size,
        overlap,
        yes_add_embedding,
        chunk_embedding_model
    )


    chunking_method = "recursive_char|chunk_size=" + str(chunk_size) + "|overlap_size=" + str(overlap)

    save_result(
        final_chunks,
        chunking_method,
        filename,
        chunk_embedding_model
    )

if __name__ == "__main__":
    main()
