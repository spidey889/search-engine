import json
import os
import re
from collections import defaultdict
from indexer import Indexer

class SearchEngine:
    """
    Handles loading the index and performing searches.
    """
    def __init__(self, data_dir='.'):
        self.index_file = os.path.join(data_dir, 'index_data.json')
        self.metadata_file = os.path.join(data_dir, 'metadata.json')
        self.inverted_index = {}
        self.documents = {}
        self.indexer = Indexer(data_dir=data_dir) # Used for tokenization

    def load_index(self):
        """
        Loads the index and metadata from disk.
        """
        if not os.path.exists(self.index_file) or not os.path.exists(self.metadata_file):
            print("Index not found. Please crawl some data first.")
            return False

        print("Loading index...")
        with open(self.index_file, 'r') as f:
            self.inverted_index = json.load(f)
            
        with open(self.metadata_file, 'r') as f:
            self.documents = json.load(f)
            
        print(f"Loaded {len(self.documents)} documents and {len(self.inverted_index)} terms.")
        return True

    def search(self, query):
        """
        Searches for the query in the index and returns ranked results.
        """
        tokens = self.indexer.tokenize(query)
        if not tokens:
            return []

        # DocID -> Score
        scores = defaultdict(float)
        
        for token in tokens:
            if token in self.inverted_index:
                # Get postings list: {doc_id: freq, ...}
                postings = self.inverted_index[token]
                for doc_id, freq in postings.items():
                    # TF Scoring: Simply sum the frequency of matched terms
                    scores[doc_id] += freq

        # Sort by score descending
        ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        
        results = []
        for doc_id, score in ranked_docs:
            doc_info = self.documents.get(str(doc_id)) # JSON keys are strings
            if doc_info:
                results.append({
                    'url': doc_info['url'],
                    'score': score
                })
        
        return results
