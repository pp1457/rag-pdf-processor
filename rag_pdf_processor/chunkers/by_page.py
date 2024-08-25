from rag_pdf_processor.pdf_to_markdown.with_pdfplumber import extract_lines
from rag_pdf_processor.tools.save_result import save_result
from rag_pdf_processor.tools.get_embedding import add_embeddings

def split_text(pdf_path, header_ratio, footer_ratio):
    lines, _ = extract_lines(pdf_path, header_ratio, footer_ratio)
    
    cur_content = ""
    last_page = 1
    start_line = 1

    chunks = []

    for line in lines:
        if line["page"] != last_page:
            chunks.append({
                "text": cur_content,
                "page_range": (last_page, last_page),
                "line_range": (start_line, line["line_id"] - 1),
                "filename": pdf_path
            })
            start_line = line["line_id"]
            cur_content = ""

        cur_content += line["text"]
        last_page = line["page"]

    chunks.append({
        "text": cur_content,
        "page_range": (last_page, last_page),
        "line_range": (start_line, lines[-1]["line_id"] - 1),
        "filename": pdf_path
    })

    return chunks

def main():
    filename = input("File Name: ")
    input_file = "data/" + filename + ".pdf"

    header_ratio = float(input("Header Ratio: ") or 0.09)
    footer_ratio = float(input("Footer Ratio: ") or 0.91)

    yes_add_embedding = input("Add embedding? (y/N) ")

    model_name = "no"

    if yes_add_embedding == "y":
        model_name = input("Chunk Embedding Model: ")

    final_chunks = split_text(input_file, header_ratio, footer_ratio)


    if yes_add_embedding == "y":
        final_chunks = add_embeddings(final_chunks, model_name)

    chunking_method = "by_page"

    save_result(final_chunks, chunking_method, filename, model_name)


if __name__ == "__main__":
    main()

    

    
