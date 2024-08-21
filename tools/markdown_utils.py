import re

def contains_strong_text(s):
    """ check if string s contain strong text """

    # Regular expression to match **strong text**
    pattern = r'\*\*[^*]+\*\*'

    return bool(re.search(pattern, s))

def count_leading_hash(s):
    """ count leading hash in string s """

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
