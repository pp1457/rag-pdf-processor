from .write_to_csv import write_to_csv
import os

def save_result(final_chunks, method, filename):
    chunk_id = 0

    directory_path = f"output/{method}/"
    os.makedirs(directory_path, exist_ok=True)
    directory_path = f"csv/{method}/"
    os.makedirs(directory_path, exist_ok=True)

    with open(f"output/{method}/{filename}.txt", "w", encoding="utf-8") as file:
        fields = ["Chunk ID", "Text", "Page Range", "Line Range", "Filename"]
        rows = []
        
        for chunk in final_chunks:

            row = []
            row.append(chunk_id)
            row.append(chunk["text"])
            row.append(chunk["page_range"])
            row.append(chunk["line_range"])
            row.append(chunk["filename"])
            rows.append(row)

            chunk_id += 1

            file.write("\n-----------------------\n")

            file.write(f"Chunk {chunk_id}: \n\n")
            file.write("Text: \n")
            file.write(chunk["text"])
            file.write("\n\nPage Range: ")
            file.write(str(chunk["page_range"]))
            file.write("\n\nLine Range: ")
            file.write(str(chunk["line_range"]))
            file.write("\n\nFilename: ")
            file.write(str(chunk["filename"]))

        write_to_csv(f"csv/{method}/{filename}.csv", fields, rows)
        print(f"CSV result saved as csv/{method}/{filename}.csv")
        print(f"TXT result saved as output/{method}/{filename}.txt")

