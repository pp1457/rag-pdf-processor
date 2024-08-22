# RAG pdf processor
## Intro

This repository is used for processing pdf for RAG

---


## `pdf_to_markdown`
### `with_pdfplumber.py`
* `extract_lines(pdf_path, header_ratio = 0.09, footer_ratio = 0.91, yes_size_round_up = "Y") -> lines, header_sizes`
    - `pdf_path(str)` :
Absolute path of the pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
    - `lines(List(dict))` :
Dictionary with the following keys
        - `text`: content of this line
        - `font_size(int)` : most common font size in this line
        - `page(int)` : page number of this line
        - `line_id(int)` : id of this line
        - `file_path(str)` : file path of this line
    - `header_sizes(List(int))` :
List of header size sorted from big to small
* `add_hash_to_header_lines(lines, header_sizes) -> md_pages`
    - `lines(List(str))` :
Return value of `extract_lines()`
    - `header_sizes(List(int))` :
Return value of `extract_lines()`

* `pdf_to_markdown(filename, header_ratio = 0.09, footer_ratio = 0.91, yse_size_round_up = "Y") -> md_pages`
    - `filename(str)` :
Filename without extension like "report" or "game"
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page(page number) 

### `with_pymupdf.py`
* `pdf_to_markdown(filename) -> md_pages`
    - `filename(str)` :
Filename without extension like "report" or "game"
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page(page number) 
    
---

## `chunkers`
### `by_markdown.py`
* `get_md_pages(filename, save_to_new_file, header_ratio = 0.09, footer_ratio = 0.91, yes_size_round_up = "Y")) -> md_pages`
    - `filename(str)` :
Filename without extension like "report" or "game"
    -  `save_to_new_file(str)` :
"y" will save the result as "markdown/filename.md", otherwise will not
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
Ratio of the bottom of page to be excluded, this is optional
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page(page number)

* `split_text(md_pages, split_level, yes_split_on_strong_text) -> final_chunks`
    - `md_pages(List[dict])` :
Output of `get_md_pages`
    - `split_level(int)` :
Let the number be `k`, it will split on header with fewer `#` than k
    - `yes_split_on_strong_text(str)` :
"n" will not split the **strong text**, otherwise will
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk

### `recursive_char.py`
* `split_text(lines, split_characters, yes_split_empty_line, chunk_size, overlap) -> final_chunks`
    - `lines(List(dict))` :
Dictionary with the following keys
        - `text`: content of this line
        - `font_size(int)` : most common font size in this line
        - `page(int)` : page number of this line
        - `line_id(int)` : id of this line
        - `file_path(str)` : file path of this line
    - `split_characters(List(str))` :
List of character to split on
    - `yes_split_empty_line(str)` :
"n" will not split on empty line, otherwise will
    - `chunk_size(int)` :
Expected chunk size, real size will not exceed this
    - `overlap(int)` :
Expected overlap size
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk

### `semantic.py`
* `split_text(lines, buffer_size, chunk_number) -> final_chunks`
    - `lines(List(dict))` :
Dictionary with the following keys
        - `text`: content of this line
        - `font_size(int)` : most common font size in this line
        - `page(int)` : page number of this line
        - `line_id(int)` : id of this line
        - `file_path(str)` : file path of this line
    - `buffer_size(int)` :
Number of sentences combined in a group
    - `chunk_number(int)` :
Number of final chunks
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk
    
---
