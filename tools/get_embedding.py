import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def get_embedding(doc):
    load_dotenv()

    model_name = "text-embedding-ada-002"
     
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

def main():
    get_embedding("Apple")

if __name__ == "__main__":
    main()
