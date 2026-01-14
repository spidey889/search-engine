import urllib.request
import urllib.parse
from html.parser import HTMLParser
import re
import time

class TextExtractor(HTMLParser):
    """
    A simple HTML parser to extract text content from HTML.
    It ignores scripts and styles.
    """
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_tags = {'script', 'style', 'head', 'title', 'meta', '[document]'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.ignore_tags:
            content = data.strip()
            if content:
                self.text_parts.append(content)

    def get_text(self):
        return " ".join(self.text_parts)

class Crawler:
    """
    Simple crawler to fetch pages and extract text.
    """
    def __init__(self, delay=1.0):
        self.delay = delay
        self.visited = set()

    def fetch_and_parse(self, url):
        """
        Fetches the URL, extracts text, and returns it.
        Returns None if fetch fails.
        """
        if url in self.visited:
            return None
        
        print(f"Crawling: {url}")
        self.visited.add(url)
        time.sleep(self.delay)  # Be polite

        try:
            # Add a User-Agent so we don't look like a bot (some sites block empty UA)
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'MiniSearchEngine/1.0'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: Status {response.status}")
                    return None
                
                charset = response.info().get_param('charset') or 'utf-8'
                html_content = response.read().decode(charset, errors='ignore')
                
                extractor = TextExtractor()
                extractor.feed(html_content)
                text_content = extractor.get_text()
                
                return {
                    'url': url,
                    'content': text_content,
                    'raw_html': html_content # kept for debugging or advanced features
                }

        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return None
