from tqdm import tqdm
from tools.split_lines import split_into_sentences
from pdf_to_markdown.with_pdfplumber import extract_lines
from tools.get_embedding_ollama import get_embedding
from tools.math_utils import cos_sim
from tools.save_result import save_result

def find_break_points(embeddings, reverse_embeddings, k):
    break_points = []
    for i, embedding in enumerate(embeddings):
        if i:
            distance = 1 - cos_sim(reverse_embeddings[i-1], embedding)
            break_points.append((i, distance))

        
    break_points.sort(key=lambda x: x[1], reverse=True)
    return break_points[:k]


def split_text(lines, buffer_size, chunk_number):
    sentences = split_into_sentences(lines)
    embeddings = []
    reverse_embeddings = []

    print("Embedding combined sentences...")
    pbar = tqdm(total=len(sentences))

    for index, sentence in enumerate(sentences):
        combined_sentence = ""
        for i in range(index, min(index + buffer_size, len(sentences))):
            combined_sentence += sentences[i]["text"]
        embeddings.append(get_embedding(combined_sentence))

        if index - buffer_size + 1 >= 0:
            reverse_embeddings.append(embeddings[index - buffer_size + 1])
        else:
            combined_sentence = ""
            for i in range(index, max(index - buffer_size, -1), -1):
                combined_sentence += sentences[i]["text"]
            reverse_embeddings.append(get_embedding(combined_sentence))
        pbar.update(1)

    pbar.close()
    print("Embedding complete")

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
    input_file = "data/" + filename + ".pdf"
    lines, _ = extract_lines(input_file)
    final_chunks = split_text(lines, 3, 30)

    save_result(final_chunks, "semantic", filename)
    

if __name__ == "__main__":
    main()


