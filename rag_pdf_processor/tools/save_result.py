from .write_to_csv import write_to_csv
import pathlib

def save_result(final_chunks, method, filename, embedding_model):

    method_dir =method.split('|', 1)[0]
    
    output_dir = pathlib.Path(f"output/{embedding_model}/{method_dir}/")
    csv_dir = pathlib.Path(f"csv/{embedding_model}/{method_dir}/")

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    txt_file_path = output_dir / f"{filename}|{method}.txt"
    csv_file_path = csv_dir / f"{filename}|{method}.csv"

    fields = ["filename", "chunking_method", "embedding_model",  "chunk_id", "page_range", "line_range", "text", "embedding"]

    rows = []

    # Open the text file for writing
    with open(txt_file_path, "w", encoding="utf-8") as file:
        for chunk_id, chunk in enumerate(final_chunks, start=1):

            file.write(f"\nChunk #{chunk_id}:\n\n")
            
            row = {
                "filename": chunk.get("filename", ""),
                "chunking_method": method,
                "embedding_model": chunk.get("embedding_model"),
                "chunk_id": chunk_id,
                "page_range": chunk.get("page_range", ""),
                "line_range": chunk.get("line_range", ""),
                "text": chunk.get("text", ""),
                "embedding": chunk.get("embedding", ""),
            }

            rows.append([value for _, value in row.items()])

            for field in fields:
                value = row.get(field, "")
                file.write(f"{field}: {value}\n\n")

            file.write("\n-----------------------\n")

    write_to_csv(csv_file_path, fields, rows)
    print(f"CSV result saved as {csv_file_path}")
    print(f"TXT result saved as {txt_file_path}")
