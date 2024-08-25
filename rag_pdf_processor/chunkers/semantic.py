from tqdm import tqdm
from rag_pdf_processor.pdf_to_markdown.with_pdfplumber import extract_lines
from rag_pdf_processor.tools.split_lines import split_into_sentences
from rag_pdf_processor.tools.get_embedding import get_embedding
from rag_pdf_processor.tools.get_embedding import add_embeddings
from rag_pdf_processor.tools.math_utils import cos_sim
from rag_pdf_processor.tools.save_result import save_result

def find_break_points(embeddings, reverse_embeddings, k):
    break_points = []
    for i, embedding in enumerate(embeddings):
        if i:
            distance = 1 - cos_sim(reverse_embeddings[i-1], embedding)
            break_points.append((i, distance))

        
    break_points.sort(key=lambda x: x[1], reverse=True)
    return break_points[:k]


def split_text(lines, buffer_size, chunk_number, embedding_model):
    sentences = split_into_sentences(lines)
    embeddings = []
    reverse_embeddings = []

    print("Embedding combined sentences...")
    pbar = tqdm(total=len(sentences))

    for index, sentence in enumerate(sentences):
        combined_sentence = ""
        for i in range(index, min(index + buffer_size, len(sentences))):
            combined_sentence += sentences[i]["text"]
        embeddings.append(get_embedding(combined_sentence, embedding_model))

        if index - buffer_size + 1 >= 0:
            reverse_embeddings.append(embeddings[index - buffer_size + 1])
        else:
            combined_sentence = ""
            for i in range(index, max(index - buffer_size, -1), -1):
                combined_sentence += sentences[i]["text"]
            reverse_embeddings.append(get_embedding(combined_sentence, embedding_model))
        pbar.update(1)

    pbar.close()
    print("Combined sentences embedding complete")

    break_points = find_break_points(embeddings, reverse_embeddings, chunk_number - 1)

    break_points.sort(key=lambda x: x[0])

    cur = 0

    final_chunks = []
    start_index = 0
    text = ""

    for index, sentence in enumerate(sentences):
        if cur < len(break_points) and index == break_points[cur][0]:
            cur += 1

            final_chunks.append({
                "text": text,
                "page_range": (sentences[start_index]["page_range"][0], sentences[index]["page_range"][1]),
                "line_range": (sentences[start_index]["line_range"][0], sentences[index]["line_range"][1]),
                "filename": sentence["filename"],
            })
            text = ""
            start_index = index

        text += sentence["text"]

    if text:
        final_chunks.append({
            "text": text,
            "page_range": (sentences[start_index]["page_range"][0], sentences[-1]["page_range"][1]),
            "line_range": (sentences[start_index]["line_range"][0], sentences[-1]["line_range"][1]),
            "filename": sentence["filename"],
        })

    return final_chunks




def main():
    filename = input("File Name: ")
    header_ratio = float(input("Header Ratio: ") or 0.09)
    footer_ratio = float(input("Footer Ratio: ") or 0.91)

    buffer_size = int(input("Buffer Size: "))
    chunk_number = int(input("Chunk Number: "))
    embedding_model = input("Semantic Embedding Model: ")
    input_file = "data/" + filename + ".pdf"


    yes_add_embedding = input("Add embedding? (y/N) ")
    model_name = "no"
    if yes_add_embedding == "y":
        model_name = input("Chunk Embedding Model: ")


    lines, _ = extract_lines(input_file, header_ratio, footer_ratio)

    final_chunks = split_text(lines, buffer_size, chunk_number, embedding_model)

    if yes_add_embedding == "y":
        final_chunks = add_embeddings(final_chunks, model_name)

    chunking_method = "semantic|model=" + str(embedding_model) + "|buffer_size=" + str(buffer_size) + "|chunk_number=" + str(chunk_number)
    save_result(final_chunks, chunking_method, filename, model_name)
    

if __name__ == "__main__":
    main()


