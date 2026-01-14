import re
import json
import os
from collections import defaultdict

# Common English stopwords to ignore
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when',
    'at', 'by', 'for', 'from', 'in', 'of', 'on', 'to', 'with',
    'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'it', 'this', 'that', 'these', 'those',
    'i', 'you', 'he', 'she', 'we', 'they',
    'not', 'so', 'as'
}

class Indexer:
    """
    Responsible for tokenizing text, building an inverted index, 
    and saving the data to disk.
    """
    def __init__(self, data_dir='.'):
        self.index_file = os.path.join(data_dir, 'index_data.json')
        self.metadata_file = os.path.join(data_dir, 'metadata.json')
        
        # Inverted index: word -> {doc_id: frequency, ...}
        self.inverted_index = defaultdict(dict)
        
        # Metadata: doc_id -> {url: "...", title: "..." (optional)}
        self.documents = {}
        self.next_doc_id = 0

    def tokenize(self, text):
        """
        Splits text into words, normalizes them, and removes questions/stopwords.
        """
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation/non-alphanumeric chars (keep spaces)
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Split by whitespace
        tokens = text.split()
        # Filter stopwords
        return [t for t in tokens if t not in STOPWORDS]

    def add_document(self, url, content):
        """
        Adds a document to the index.
        """
        doc_id = self.next_doc_id
        self.next_doc_id += 1
        
        self.documents[doc_id] = {'url': url}
        
        tokens = self.tokenize(content)
        term_freqs = defaultdict(int)
        
        for token in tokens:
            term_freqs[token] += 1
            
        for token, freq in term_freqs.items():
            self.inverted_index[token][doc_id] = freq

    def save(self):
        """
        Persists the index and metadata to disk.
        """
        print(f"Saving index with {len(self.inverted_index)} terms and {len(self.documents)} documents...")
        
        with open(self.index_file, 'w') as f:
            json.dump(self.inverted_index, f, indent=2)
            
        with open(self.metadata_file, 'w') as f:
            json.dump(self.documents, f, indent=2)

    def load(self):
        """
        Loads the index and metadata from disk (optional, mostly for Search logic).
        But SearchEngine usually handles loading. 
        This might be useful if we want to support incremental indexing later.
        """
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                self.inverted_index = defaultdict(dict, json.load(f))
        
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.documents = json.load(f)
                # Recover next_doc_id
                if self.documents:
                    # keys in json are strings, convert to int to find max
                    keys = [int(k) for k in self.documents.keys()]
                    self.next_doc_id = max(keys) + 1
