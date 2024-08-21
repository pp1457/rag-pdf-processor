# RAG pdf processor
## Intro
This repository is used for processing pdf for RAG

---


## `pdf_to_markdown`
### `with_pdfplumber.py`
* `extract_lines(pdf_path) -> lines, line_metadatas, header_sizes`
    - `pdf_path` :
Absolute path of the pdf file
    - `lines(List(str))` :
Content of each line
    - `line_metadatas(List(str))` :
Dictionary with the following keys
        - `font_size(int)` : most common font size in this line
        - `page(int)` : page number of this line
        - `line_id(int)` : id of this line
        - `file_path(str)` : file path of this line
    - `header_sizes(List(int))` :
List of header size sorted from big to small
* `add_hash_to_header_lines(lines, line_metadatas, header_sizes) -> md_pages`
    - `lines(List(str))` :
Return value of `extract_lines()`
    - `line_metadatas(List(str))` :
Return value of `extract_lines()`
    - `header_sizes(List(int))` :
Return value of `extract_lines()`

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
* `get_md_pages(filename, save_to_new_file) -> md_pages`
    - `filename(str)` :
Filename without extension like "report" or "game"
    -  `save_to_new_file(str)` :
"y" will save the result as "markdown/filename.md", otherwise will not
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page(page number)

* `split_text(md_pages, split_level, split_on_strong_text) -> final_chunks`
    - `md_pages(List[dict])` :
Output of `get_md_pages`
    - `split_level(int)` :
Let the number be `k`, it will split on header with fewer `#` than k
    - `split_on_strong_text(str)` :
"n" will not split the **strong text**, otherwise will
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk

### `recursive_char.py`
* `split_text(lines, line_metadatas, split_characters, split_empty_line, chunk_size, overlap) -> final_chunks`
    - `lines(List(str))` :
Content of each line
    - `line_metadatas(List(str))` :
Dictionary with the following keys
        - `font_size(int)` : most common font size in this line
        - `page(int)` : page number of this line
        - `line_id(int)` : id of this line
        - `file_path(str)` : file path of this line
    - `split_characters(List(str))` :
List of character to split on
    - `split_empty_line(str)` :
"n" will not split on empty line, otherwise will
    - `chunk_size(int)` :
Expected chunk size, real size will not exceed this
    - `overlap(int)` :
Expected overlap size

---
