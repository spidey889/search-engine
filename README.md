# Basic Search Engine

A simple, readable, and extensible search engine implementation in Python.
Designed to be a clean reference for understanding how search engines work.

## Features

- **Crawler**: Fetches pages and extracts text.
- **Indexer**: Normalizes text and builds an inverted index.
- **Search**: Ranks results using Term Frequency (TF).
- **Storage**: Uses local JSON files for simplicity.

## Components

- `crawler.py`: Fetches URLs and parses HTML.
- `indexer.py`: Tokenizes text, removes stopwords, and manages the index.
- `search.py`: Implements the search ranking logic.
- `main.py`: The CLI runner.

## Quick Start

### 1. Setup
No external dependencies are required. Just ensure you have Python 3 installed.

### 2. Crawl
Create a text file (e.g., `seed_urls.txt`) with URLs to index:
```text
https://www.python.org/
https://en.wikipedia.org/wiki/Search_engine
```

Run the crawler:
```bash
python main.py crawl seed_urls.txt
```
This will create `index_data.json` and `metadata.json`.

### 3. Search
Run a search query:
```bash
python main.py search "python"
```

## How it works

1.  **Crawling**: The crawler downloads HTML, strips tags, and extracts raw text.
2.  **Indexing**: Text is split into tokens. Punctuation is removed, and common "stopwords" (like 'the', 'is') are filtered out.
3.  **Inverted Index**: We build a map where keys are words and values are lists of documents containing those words (along with frequency).
4.  **Searching**: When you search, the engine looks up your keywords in the inverted index, finds matching documents, and adds up the occurrence counts (Term Frequency) to score them.

## Future Improvements (TODO)

- [ ] **Better Ranking**: Implement TF-IDF (Term Frequency-Inverse Document Frequency) to downweight common terms.
- [ ] **Advanced Crawler**: Add link extraction to visit new pages recursively (BFS).
- [ ] **Stemming**: Use a library like `nltk` to reduce words to their root (e.g., "running" -> "run").
- [ ] **Web Interface**: Build a simple Flask/Django app to serve results.
