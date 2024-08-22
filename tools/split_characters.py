def split_by_characters(chars, split_characters):

    result = []
    cur = []

    for char in chars:
        cur.append(char)
        if char["text"] in split_characters:
            result.append(cur)
            cur = []
    if cur:
        result.append(cur)

    return result
