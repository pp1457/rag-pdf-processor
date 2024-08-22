from .write_to_csv import write_to_csv
import os

def save_result(final_chunks, method, filename):
    # Ensure the directories exist
    output_dir = f"output/{method}/"
    csv_dir = f"csv/{method}/"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(csv_dir, exist_ok=True)

    # Define file paths
    txt_file_path = os.path.join(output_dir, f"{filename}_{method}.txt")
    csv_file_path = os.path.join(csv_dir, f"{filename}_{method}.csv")

    # Define CSV fields and initialize rows list
    fields = ["chunk_id", "text", "page_range", "line_range", "filename", "embedding"]
    rows = []

    # Open the text file for writing
    with open(txt_file_path, "w", encoding="utf-8") as file:
        # Iterate over the chunks with chunk_id
        for chunk_id, chunk in enumerate(final_chunks, start=1):
            row = [chunk_id]
            file.write(f"\nChunk #{chunk_id}:\n\n")
            for key, value in chunk.items():
                row.append(value)
                # Writing to the text file
                file.write(f"{key.replace('_', ' ').title()}: {value}\n\n")
            
            rows.append(row)
            file.write("\n-----------------------\n")

    # Write the results to a CSV file
    write_to_csv(csv_file_path, fields, rows)
    print(f"CSV result saved as {csv_file_path}")
    print(f"TXT result saved as {txt_file_path}")
