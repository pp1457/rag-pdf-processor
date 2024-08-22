import ollama

def get_embedding(s):
    result = ollama.embeddings(model='mxbai-embed-large', prompt=s)
    return result["embedding"]

def main():
    get_embedding("Hello, I'm Paul")

if __name__ == "__main__":
    main()
