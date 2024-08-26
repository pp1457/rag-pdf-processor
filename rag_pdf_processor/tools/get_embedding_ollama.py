import ollama
from tqdm import tqdm

def get_embedding_ollama(s, embedding_model = "mxbai-embed-large"):
    result = ollama.embeddings(model=embedding_model, prompt=s)
    return result["embedding"]

def add_embeddings(chunks, model_name):

    print("Embedding chunks...")

    pbar = tqdm(total=len(chunks))

    for chunk in chunks:
        chunk["embedding"] = get_embedding_ollama(chunk["text"], model_name)
        chunk["embedding_model"] = model_name
        pbar.update(1)
    pbar.close()
    print("Chunks embedding complete")
    return chunks

def main():
    get_embedding_ollama("Hello, I'm Paul", "mxbai-embed-large")

if __name__ == "__main__":
    main()
