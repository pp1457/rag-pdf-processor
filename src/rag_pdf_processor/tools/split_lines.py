from typing import List
from .split_characters import split_by_characters
from .transform_to_chunk import transform_to_chunk

def split_on_empty_lines(lines):
    """ split empty lines """

    new_lines = []
    empty_line_count = 0

    for line in lines:
        if line["text"].strip() == "":
            empty_line_count += 1
            if empty_line_count == 1:
                empty_line_count = -10000000
                line["text"] = ""
                new_lines.append(line)
        else:
            empty_line_count = 0
            new_lines.append(line)

    return new_lines

def split_into_sentences(lines: List[dict]):
    """ split text by recursive char """

    page_content = ""
    last_page = -1

    lines = split_on_empty_lines(lines)

    all_chars = []

    for line in lines:
        for char in line["text"]:
            if char == "\n":
                continue
            all_chars.append({
                "text": char,
                "line_id": line["line_id"],
                "page": line["page"],
                "filename": line["file_path"]
            })

    split_characters = [
        # English sentence-ending punctuation
        # '.', '!', '?', ',',

        # Chinese sentence-ending punctuation
        '。', '！', '？', '，'
    ]

    tmp_results = split_by_characters(all_chars, split_characters)

    sentences = []

    for chars in tmp_results:
        sentence = transform_to_chunk(chars)
        sentences.append(sentence)

    return sentences

    











