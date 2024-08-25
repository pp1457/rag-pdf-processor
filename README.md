# RAG pdf processor
## Intro

This repository is used for processing pdf for RAG

---

## `pdf_to_markdown`
### `with_pdfplumber.py`
* `extract_lines(input_path, header_ratio = 0.09, footer_ratio = 0.91, yes_size_round_up = "Y") -> lines, header_sizes`
    - `input_path(str)` :
Path of the input pdf file
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

* `pdf_to_markdown(input_path, header_ratio = 0.09, footer_ratio = 0.91, yse_size_round_up = "Y") -> md_pages`
    - `input_path(str)` :
Path of the input pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page (page number) 

### `with_pymupdf.py`
* `pdf_to_markdown(input_path) -> md_pages`
    - `filename(str)` :
Path of the input pdf file
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page (page number) 
    
---

## `chunkers`
### `by_markdown.py`
* `get_md_pages(input_path, yes_save_to_new_file, output_path, header_ratio = 0.09, footer_ratio = 0.91, yes_size_round_up = "Y")) -> md_pages`
    - `input_path(str)` :
Path of the input pdf file
    -  `yes_save_to_new_file(str)` :
"y" will save the result to output_path, otherwise will not
    - `output_path(str)` :
Path of the output markdown file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
Ratio of the bottom of page to be excluded, this is optional
    - `md_pages(List[dict])` :
List of pages, each page is a dictionary, contains the following keys
        - `text(str)` : content of the page
        - `metadata(dict)` : dictionary contains file_path, and page (page number)

* ```split_text(input_path, header_ratio = 0.09, footer_ratio = 0.91, yes_save_to_new_file = "N", output_path = "markdown/tmp.md", yes_size_round_up = "Y", split_level = 3, yes_split_on_strong_text = "Y", yes_add_embedding = "N", chunk_embedding_model = "no-embedding") -> final_chunks```
    - `input_path(str)` :
Path of the input pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    -  `yes_save_to_new_file(str)` :
"y" will save the result to output_path, otherwise will not
    - `output_path(str)` :
Path of the output markdown file
    - `yes_size_round_up(str)` :
"n" will keep the original float size, otherwise will round up to 5 decimal
Ratio of the bottom of page to be excluded, this is optional
    - `split_level(int)` :
Let the number be `k`, it will split on header with fewer `#` than k
    - `yes_split_on_strong_text(str)` :
"n" will not split the **strong text**, otherwise will
    - `yes_add_embedding(str)` :
"y" will add the embedding to each chunk, otherwise will not
    - `chunk_embedding_model(str)` :
Embedding model used when yes\_add_embedding is "y"
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk
        - `embedding(List[float])` : embedding of the text (optional)
        - `embedding_model(str)` : embedding model (optional)

### `recursive_char.py`
* `split_text(input_path, header_ratio = 0.09, footer_ratio = 0.91, split_characters = ["。", "\n", "  ",  ",", ".", " "], yes_split_empty_line = "Y", chunk_size = 1000, overlap = 100, yes_add_embedding = "N", chunk_embedding_model = "no-embedding") -> final_chunks`
    - `input_path(str)` :
Path of the input pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `split_characters(List(str))` :
List of character to split on
    - `yes_split_empty_line(str)` :
"n" will not split on empty line, otherwise will
    - `chunk_size(int)` :
Expected chunk size, real size will not exceed this
    - `overlap(int)` :
Expected overlap size
    - `yes_add_embedding(str)` :
"y" will add the embedding to each chunk, otherwise will not
    - `chunk_embedding_model(str)` :
Embedding model used when yes\_add_embedding is "y"
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk
        - `embedding(List[float])` : embedding of the text (optional)
        - `embedding_model(str)` : embedding model (optional)

### `semantic.py`
* `split_text(input_path, header_ratio = 0.09, footer_ratio = 0.91, buffer_size = 3, chunk_number = 30, semantic_embedding_model = "no", yes_add_embedding = "N", chunk_embedding_model = "no-embedding") -> final_chunks`
    - `input_path(str)` :
Path of the input pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `buffer_size(int)` :
Number of sentences combined in a group
    - `chunk_number(int)` :
Number of final chunks
    - `semantic_embedding_model(str)` :
Embedding model used for semantic chunking
    - `yes_add_embedding(str)` :
"y" will add the embedding to each chunk, otherwise will not
    - `chunk_embedding_model(str)` :
Embedding model used when yes\_add_embedding is "y"
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk
        - `embedding(List[float])` : embedding of the text (optional)
        - `embedding_model(str)` : embedding model (optional)

### `by_page.py`
* `split_text(input_path, header_ratio = 0.09, footer_ratio = 0.91, yes_add_embedding = "N", chunk_embedding_model = "no-embedding") -> final_chunks`
    - `input_path(str)` :
Path of the input pdf file
    - `header_ratio(float)` :
Ratio of the top of page to be excluded, this is optional
    - `footer_ratio(float)` :
Ratio of the bottom of page to be excluded, this is optional
    - `yes_add_embedding(str)` :
"y" will add the embedding to each chunk, otherwise will not
    - `chunk_embedding_model(str)` :
Embedding model used when yes\_add_embedding is "y"
    - `final_chunks(List[dict])` :
List of chunks, each chunk is a dictionary, contains the following keys
        - `text(str)` : content of this chunk
        - `filename(str)` : file path of this chunk
        - `page_range((int, int))` : page range of this chunk
        - `line_range((int, int))` : line range of this chunk
        - `embedding(List[float])` : embedding of the text (optional)
        - `embedding_model(str)` : embedding model (optional)
---
