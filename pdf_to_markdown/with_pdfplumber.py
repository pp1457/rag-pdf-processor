""" pdf to markdown with pdfplumber """
from collections import Counter
from typing import List
import pdfplumber

def extract_lines(pdf_path):
    """ extract lines """

    font_size_counter = Counter()

    lines = []

    line_id = 0

    with pdfplumber.open(pdf_path) as pdf:
        for i in range(len(pdf.pages)):
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

                        lines.append({
                            "text": (line_content + "\n"),
                            "font_size": cur_font_size,
                            "page": pdf.pages[i].page_number,
                            "line_id": line_id,
                            "file_path": pdf_path
                        })

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

            lines.append({
                "text": (line_content + "\n"),
                "font_size": cur_font_size,
                "page": pdf.pages[i].page_number,
                "line_id": line_id,
                "file_path": pdf_path
            })


        most_common_sizes = tmp_counter.most_common()

        font_size_counter[most_common_sizes[0][0]] += 1


    repeated_sizes = [size for size, count in font_size_counter.items() if count > 0]

    repeated_sizes.sort(reverse=True)

    header_sizes = []

    for i in range(6):
        if i >= len(repeated_sizes) or repeated_sizes[i] == 0:
            break
        header_sizes.append(repeated_sizes[i])

    return lines, header_sizes

def add_hash_to_header_lines(lines, header_sizes):
    """ add hash to header lines """

    md_pages = []

    page_content = ""
    last_page = -1

    for line in lines:

        cur_font_size = line["font_size"]
        cur_page = line["page"]

        if last_page != -1 and cur_page != last_page:
            md_pages.append({
                "text": page_content,
                "metadata": {
                    "file_path": line["file_path"],
                    "page": last_page
                },
            })
            page_content = ""

        if cur_font_size in header_sizes:
            number_of_hashes = header_sizes.index(cur_font_size) + 1
            for _ in range(number_of_hashes):
                line["text"] = "#" + line["text"]

        page_content += line["text"]

        last_page = cur_page

    return md_pages


def pdf_to_markdown(filename: str) -> List[dict]:
    input_file = "data/" + filename + ".pdf"

    lines, header_sizes = extract_lines(input_file)

    result = add_hash_to_header_lines(lines, header_sizes)

    return result


if __name__ == "__main__":
    pdf_to_markdown("game")
