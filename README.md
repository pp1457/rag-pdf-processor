# RAG pdf processor
## Intro
This repository is used for processing pdf for RAG

---

## chunkers
### `by_markdown.py`
#### `get_md_pages(filename, save_to_new_file) -> md_pages`
##### `filename(str)`
Filename without extension like "report" or "game"
##### `save_to_new_file(str)`
"y" will save the result as "markdown/filename.md", otherwise will not
##### `md_pages(List[dict])`
List of pages, each page is a dictionary, contains the following keys
- text(str) : content of the page
- metadata(dict) : dictionary contains file_path, and page(page number)

#### `split_text(md_pages, split_level, split_on_strong_text) -> final_chunks`
##### `md_pages(List[dict])`
Output of `get_md_pages`
##### `split_level(int)`
Let the number be `k`, it will split on header with fewer `#` than k
##### `split_on_strong_text(str)`
"n" will not split the **strong text**, otherwise will
##### `final_chunks(List[dict])`
List of chunks, each chunk is a dictionary, contains the following keys
- text(str) : content of the chunk
- filename(str) : file path
- page_range((int, int)) : page range of chunk
- line_range((int, int)) : line range of chunk
