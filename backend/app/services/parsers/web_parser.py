import logging
import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import html2text
from langchain.schema import Document
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class WebParser:
    """Parser for web pages"""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.html_converter.body_width = 0  # No wrapping
    
    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
    
    def parse_html(self, html_content: str, url: str) -> List[Document]:
        """Parse HTML content into Document objects"""
        try:
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Get title
            title = soup.title.string if soup.title else urlparse(url).netloc
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                element.decompose()
            
            # Convert to markdown
            text = self.html_converter.handle(str(soup))
            
            # Split into chunks - simple implementation
            chunks = self._split_text(text, chunk_size=3000, overlap=200)
            
            # Create documents
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": "web",
                        "url": url,
                        "title": title,
                        "chunk": i,
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)
            
            return documents
        except Exception as e:
            logger.error(f"Error parsing HTML from {url}: {str(e)}")
            return []
    
    def _split_text(self, text: str, chunk_size: int = 3000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Take a chunk of size chunk_size
            end = start + chunk_size
            
            # If it's not the last chunk, try to find a good split point
            if end < len(text):
                # Try to find a newline to break at
                split_point = text.rfind('\n', start, end)
                
                # If no newline found, try a space
                if split_point == -1 or split_point <= start:
                    split_point = text.rfind(' ', start, end)
                
                # If still no good split found, just split at chunk_size
                if split_point == -1 or split_point <= start:
                    split_point = end
                
                chunks.append(text[start:split_point])
                start = max(split_point, start + chunk_size - overlap)
            else:
                # Last chunk
                chunks.append(text[start:])
                break
        
        return chunks
    
    def parse(self, url: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Main entry point to parse a web page into Document objects
        
        Args:
            url: The URL to parse
            metadata: Optional additional metadata
            
        Returns:
            List of Document objects
        """
        html_content = self.fetch_url(url)
        if not html_content:
            return []
        
        documents = self.parse_html(html_content, url)
        
        # Add any additional metadata
        if metadata:
            for doc in documents:
                doc.metadata.update(metadata)
        
        return documents

# Singleton instance
web_parser = WebParser()
