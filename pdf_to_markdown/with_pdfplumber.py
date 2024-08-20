""" pdf to markdown with pdfplumber """
from collections import Counter
from typing import List
import pdfplumber

def extract_lines(pdf_path):
    """ extract lines """

    font_size_counter = Counter()

    line_metadatas = []
    lines = []

    line_id = 0

    with pdfplumber.open(pdf_path) as pdf:
        for i in range(len(pdf.pages)):
            # lines1 = pdf.pages[i].extract_text().split('\n')
            chars = pdf.pages[i].chars

            last_bottom = -1

            tmp_counter = Counter()
            line_content = ""

            for char in chars:
                if char["top"] > last_bottom:
                    if line_id > 0:

                        cur_font_size = 0

                        if tmp_counter:
                            cur_font_size = tmp_counter.most_common()[0][0]

                        line_metadatas.append({
                            "font_size": cur_font_size,
                            "page": pdf.pages[i].page_number,
                            "line_id": line_id,
                            "file_path": pdf_path
                        })
                        lines.append(line_content + "\n")
                        line_content = ""

                        font_size_counter[cur_font_size] += 1

                        tmp_counter.clear()

                    line_id += 1

                line_content += char["text"]
                tmp_counter[char["size"]] += 1
                last_bottom = char["bottom"]
            cur_font_size = 0

            if tmp_counter:
                cur_font_size = tmp_counter.most_common()[0][0]
            line_metadatas.append({
                "font_size": cur_font_size,
                "page": pdf.pages[i].page_number,
                "line_id": line_id+1,
                "file_path": pdf_path
            })
            lines.append(line_content + "\n")

        most_common_sizes = tmp_counter.most_common()
        font_size_counter[most_common_sizes[0][0]] += 1

#    for line in lines:
#        print("-----")
#        print(line)

#    print(font_size_counter.most_common())

#    print(font_size_counter.items())

    repeated_sizes = [size for size, count in font_size_counter.items() if count > 0]

    repeated_sizes.sort(reverse=True)
    header_sizes = []

    for i in range(6):
        if i >= len(repeated_sizes) or repeated_sizes[i] == 0:
            break
        header_sizes.append(repeated_sizes[i])

#    print(header_sizes)

    return lines, line_metadatas, header_sizes

def add_hash_to_header_lines(lines, line_metadatas, header_sizes):
    """ add hash to header lines """

    md_pages = []

    page_content = ""
    last_page = -1

    for i in range(len(lines)):

        cur_font_size = line_metadatas[i]["font_size"]
        # print("cur_font_size: ")
        # print(cur_font_size)
        cur_page = line_metadatas[i]["page"]

        if last_page != -1 and cur_page != last_page:
            md_pages.append({
                "text": page_content,
                "metadata": {
                    "file_path": line_metadatas[i]["file_path"],
                    "page": last_page
                },
                "line_id": line_metadatas[i]["line_id"]
            })
            page_content = ""

        if cur_font_size in header_sizes:
            number_of_hashes = header_sizes.index(cur_font_size) + 1
            for _ in range(number_of_hashes):
                lines[i] = "#" + lines[i]
            # print(lines[i])

        page_content += lines[i]

        last_page = cur_page

    return md_pages


def pdf_to_markdown(file_name: str) -> List[dict]:
    input_file = "data/" + file_name + ".pdf"
    lines, line_metadatas, header_sizes = extract_lines(input_file)

    result = add_hash_to_header_lines(lines, line_metadatas, header_sizes)

    return result


if __name__ == "__main__":
    pdf_to_markdown("game")
