import pathlib
import re
from typing import List
from tools.pdf_to_markdown import pdf_to_markdown

def get_md_chunks() -> List[dict]:
    file_name = input("File Name: ")
    save_to_new_file = input("Save to new file? (y/N)")
    output_file = "markdown/" + file_name + ".md"
    md_chunks = pdf_to_markdown(file_name)

    if save_to_new_file == "y":
        md_content = ""
        for chunk in md_chunks:
            md_content += chunk["text"]
        pathlib.Path(output_file).write_bytes(md_content.encode())
        print(f"Saved as {output_file}")
    
    return md_chunks

def contains_strong_text(s):
    # Regular expression to match **strong text**
    pattern = r'\*\*[^*]+\*\*'
    return bool(re.search(pattern, s))

def count_leading_hash(s):
    s = s.lstrip()
    count = 0
    for char in s:
        if char == "#":
            count += 1
        else:
            break

    if count == 0:
        count = 100

    return count

def context(contents) -> str:
    output = ""
    for section in contents:
        output += section

    print(f"Output: {output}")
    return output


def split_text(md_chunks: List[dict]) -> List[dict]:
    final_chunks = []
    
    split_level = int(input("Enter the number of # (between 1 and 4): "))
    split_on_strong = input("Split on **{Strong Text}**? (Y/n)")

    line_id = 0;

    stack = []

    contents = []
    cur_section = ""


    for chunk in md_chunks:

        last_line = ""

        for line in chunk["text"].splitlines():
            line_id += 1
            hash_count = count_leading_hash(line)
            if contains_strong_text(line) and not split_on_strong == "n":
                hash_count = split_level

            if split_level >= hash_count:
                if stack and stack[-1]["lev"] <= hash_count:
                    line_range = (stack[-1]["pos"], line_id - 1)
                    text = context(contents) + cur_section
                    cur_section = line + "\n"

                    final_chunk = {
                        "page_metadata": chunk["metadata"],
                        "toc_items": chunk["toc_items"],
                        "tables": chunk["tables"],
                        "images": chunk["images"],
                        "graphics": chunk["graphics"],
                        "line_range": line_range,
                        "text": text
                    }

                    final_chunks.append(final_chunk)

                    while stack[-1]["lev"] < hash_count:
                        stack.pop()
                        contents.pop()
                else:
                    if stack:
                        contents.append(cur_section)
                        cur_section = line + "\n"
                    stack.append({"pos": line_id, "lev": hash_count})


            else:
                if (last_line.strip() == "" and re.match(r"^\s*-----\s*$", line)) or line.strip() == "":
                    last_line = line
                    continue
                else:
                    last_line = line
                    cur_section += line + "\n"

            last_line = line


    return final_chunks


def main():
    md_chunks = get_md_chunks()
    final_chunks = split_text(md_chunks)

    chunk_id = 0

    for chunk in final_chunks:
        chunk_id += 1
        print(f"\nChunk {chunk_id}: ")
        print(chunk["text"])
        print()
    


if __name__ == "__main__":
    main(); 
