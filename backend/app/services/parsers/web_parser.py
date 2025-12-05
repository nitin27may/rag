import logging
import os
import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import html2text
from langchain.schema import Document
from urllib.parse import urlparse

from app.services.chunking_service import chunking_service
from app.core.config import settings

logger = logging.getLogger(__name__)

# Check if SSL verification should be disabled (for corporate proxy environments)
DISABLE_SSL_VERIFICATION = os.environ.get("DISABLE_SSL_VERIFICATION", "false").lower() == "true"

class WebParser:
    """Parser for web pages"""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = True
        self.html_converter.ignore_tables = False
        self.html_converter.body_width = 0  # No wrapping
        # Use centralized chunking service
        self.chunking_service = chunking_service
    
    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """Fetch content from a URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Use SSL verification setting (disabled for corporate proxy environments)
            verify_ssl = not DISABLE_SSL_VERIFICATION
            if not verify_ssl:
                logger.warning("SSL verification is disabled for web requests. This should only be used in development/corporate proxy environments.")
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=headers, timeout=timeout, verify=verify_ssl)
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
            
            # Use chunking service for splitting text
            chunks = self.chunking_service.split_text(text)
            
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
