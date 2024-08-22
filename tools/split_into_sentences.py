def split_into_sentences(lines: List[str], line_metadatas: List[dict]):
    """ split all lines into sentences """

    if split_empty_line != "n":
        lines, line_metadatas = split_empty_lines(lines, line_metadatas)
        split_characters = [""] + split_characters


    page_content = ""
    last_page = -1

    all_chars = []

    for line_id, line in enumerate(lines):
        line = line.strip()
        for char in line:
            all_chars.append({
                "text": char,
                "line_id": line_id,
                "page": line_metadatas[line_id]["page"],
                "filename": line_metadatas[line_id]["file_path"]
            })

