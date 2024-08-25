import os
from tqdm import tqdm
from dotenv import load_dotenv
from openai import AzureOpenAI

def get_embedding_openai(doc, model_name):
    load_dotenv()
     
    client = AzureOpenAI(
      api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
      api_version = "2024-02-01",
      azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
    )

    response = client.embeddings.create(
        input = doc,
        model= model_name
    )

    return response.data[0].embedding

def add_embeddings(chunks, model_name):

    print("Embedding chunks...")
    pbar = tqdm(total=len(chunks))
    for chunk in chunks:
        chunk["embedding"] = get_embedding(chunk["text"], model_name)
        chunk["embedding_model"] = model_name
        pbar.update(1)
    pbar.close()
    print("Chunks embedding complete")
    return chunks


def main():
    get_embedding("Apple")

if __name__ == "__main__":
    main()
