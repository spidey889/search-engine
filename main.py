import argparse
import sys
import os

# Ensure we can import modules from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crawler import Crawler
from indexer import Indexer
from search import SearchEngine

def cmd_crawl(args):
    """
    Crawls a list of URLs from a file and indexes them.
    """
    if not os.path.exists(args.url_file):
        print(f"Error: File '{args.url_file}' not found.")
        return

    crawler = Crawler()
    indexer = Indexer()
    
    # Load existing index if we want to add to it, otherwise we start fresh
    # For simplicity in this basic version, we just start fresh or overwrite
    # But let's check if we strictly wanted append? 
    # "Store indexed data locally... include clear comments explaining..."
    # We'll just overwrite for simplicity as per "Basic but real".
    
    print(f"Reading URLs from {args.url_file}...")
    with open(args.url_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    count = 0
    for url in urls:
        result = crawler.fetch_and_parse(url)
        if result:
            print(f"Indexing {url}...")
            indexer.add_document(result['url'], result['content'])
            count += 1
        else:
            print(f"Skipping {url}")
    
    if count > 0:
        indexer.save()
        print("Crawling and indexing completed successfully.")
    else:
        print("No documents were indexed.")

def cmd_search(args):
    """
    Searches the index for a query.
    """
    engine = SearchEngine()
    if not engine.load_index():
        return

    results = engine.search(args.query)
    
    print(f"\nResults for '{args.query}':")
    if results:
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['url']} (Score: {res['score']})")
    else:
        print("No results found.")

def main():
    parser = argparse.ArgumentParser(description="A Basic Search Engine")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Crawl command
    parser_crawl = subparsers.add_parser("crawl", help="Crawl and index a list of URLs")
    parser_crawl.add_argument("url_file", help="Path to a text file containing URLs to crawl (one per line)")
    parser_crawl.set_defaults(func=cmd_crawl)

    # Search command
    parser_search = subparsers.add_parser("search", help="Search the index")
    parser_search.add_argument("query", help="The search query text")
    parser_search.set_defaults(func=cmd_search)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
