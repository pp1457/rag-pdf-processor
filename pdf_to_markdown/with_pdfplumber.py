import pdfplumber
from collections import Counter

def extract_header_fontsize_from_pdf(pdf_path):

    font_size_counter = Counter()

    content = ""

    line_sizes = [0]
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
                        
                        if tmp_counter:
                            line_sizes.append(tmp_counter.most_common()[0][0])
                        else:
                            line_sizes.append(0)

                        font_size_counter[line_sizes[line_id]] += 1

                        tmp_counter.clear()
                        line_content = ""

                    line_id += 1
                    content += "\n"

                tmp_counter[int(char["size"])] += 1
                line_content += char["text"]

                last_bottom = char["bottom"]
                content += char["text"]

        most_common_sizes = tmp_counter.most_common()
        font_size_counter[most_common_sizes[0][0]] += 1
        
    lines = content.splitlines()

#     for line in lines:
#         print("-----")
#         print(line)

    print(font_size_counter.most_common())

    repeated_sizes = [size for size, count in font_size_counter.items() if count > 1]
    repeated_sizes.sort(reverse=True)

    return lines, line_sizes 




def extract_lines_with_font_size(pdf_path, target_font_size):
    lines_with_target_font_size = []

    with pdfplumber.open(pdf_path) as pdf:
        for i in range(len(pdf.pages)):
            words = pdf.pages[i].extract_words(extra_attrs=['fontname', 'size'])
            lines = {}

            for word in words:
                line_num = word['top']
                if line_num not in lines:
                    lines[line_num] = []
                lines[line_num].append(word)

            for line_num, line_words in lines.items():
                line_font_sizes = [word['size'] for word in line_words]
                if target_font_size in line_font_sizes:
                    line_text = ' '.join([word['text'] for word in line_words])
                    lines_with_target_font_size.append(line_text)

    return lines_with_target_font_size



if __name__ == "__main__":
     extract_header_fontsize_from_pdf("data/report.pdf")
