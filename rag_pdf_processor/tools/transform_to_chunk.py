def content(chars):
    """ content """
    output = "".join(char["text"] for char in chars)
    return output

def transform_to_chunk(chars):
    """ transform from chars to chunks """

    text = content(chars)

    final_chunk = {
        "text": text,
        "page_range": (chars[0]["page"], chars[-1]["page"]),
        "line_range": (chars[0]["line_id"], chars[-1]["line_id"]),
        "filename": chars[0]["filename"],
    }

    return final_chunk
