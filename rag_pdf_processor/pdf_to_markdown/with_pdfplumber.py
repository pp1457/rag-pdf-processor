""" pdf to markdown with pdfplumber """

from collections import Counter
from typing import List
import pdfplumber

def extract_lines(
        input_path,
        header_ratio = 0.09,
        footer_ratio = 0.91,
        yes_size_round_up = "Y"
    ):

    """ extract lines """

    font_size_counter = Counter()
    lines = []
    line_id = 0

    with pdfplumber.open(input_path) as pdf:

        for i in range(len(pdf.pages)):

            page = pdf.pages[i]
            chars = page.chars
            page_height = page.height

            last_bottom = -1
            line_content = ""
            tmp_counter = Counter()

            for char in chars:

                if char["bottom"] < header_ratio * page_height or char["top"] > footer_ratio * page_height:
                    continue

                if char["top"] > last_bottom:
                    if line_id > 0:

                        cur_font_size = 0

                        if tmp_counter:
                            cur_font_size = tmp_counter.most_common(1)[0][0]

                        lines.append({
                            "text": (line_content + "\n"),
                            "font_size": cur_font_size,
                            "page": pdf.pages[i].page_number,
                            "line_id": line_id,
                            "file_path": input_path
                        })

                        line_content = ""

                        font_size_counter[cur_font_size] += 1

                        tmp_counter.clear()

                    line_id += 1

                line_content += char["text"]
                size = char["size"] if yes_size_round_up == "n" else round(char["size"], 5)
                tmp_counter[size] += 1
                last_bottom = char["bottom"]

            cur_font_size = 0

            if tmp_counter:
                cur_font_size = tmp_counter.most_common(1)[0][0]


            font_size_counter[cur_font_size] += 1

            lines.append({
                "text": (line_content + "\n"),
                "font_size": cur_font_size,
                "page": pdf.pages[i].page_number,
                "line_id": line_id,
                "file_path": input_path
            })


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

        if line["text"].strip() != "" and cur_font_size in header_sizes:
            number_of_hashes = header_sizes.index(cur_font_size) + 1
            for _ in range(number_of_hashes):
                line["text"] = "#" + line["text"]

        page_content += line["text"]

        last_page = cur_page

    if page_content:
        md_pages.append({
            "text": page_content,
            "metadata": {
                "file_path": line["file_path"],
                "page": last_page
            },
        })

    return md_pages


def pdf_to_markdown(
        input_path,
        header_ratio = 0.09,
        footer_ratio = 0.91,
        yes_size_round_up = "Y"
):

    lines, header_sizes = extract_lines(input_path, header_ratio, footer_ratio, yes_size_round_up)

    result = add_hash_to_header_lines(lines, header_sizes)

    return result


if __name__ == "__main__":
    print(pdf_to_markdown("fubon"))
