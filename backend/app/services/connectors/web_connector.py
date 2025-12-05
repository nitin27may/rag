import logging
import requests
from typing import Dict, Any, List, Optional, Union
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from langchain.schema import Document

from app.services.parsers.web_parser import web_parser

logger = logging.getLogger(__name__)

class WebConnector:
    """Connector for web content"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Fetch content from a URL
        
        Args:
            url: URL to fetch
            timeout: Timeout in seconds
            
        Returns:
            HTML content or None if the request fails
        """
        try:
            logger.info(f"Fetching URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
    
    def process_url(self, url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a URL and convert it to documents
        
        Args:
            url: URL to process
            metadata: Optional metadata to include
            
        Returns:
            Dictionary with processing results
        """
        try:
            logger.info(f"Processing URL: {url}")
            
            # Use the web parser to extract content
            documents = web_parser.parse(url, metadata)
            
            if not documents:
                return {
                    "status": "error",
                    "error": "No content could be extracted from the URL"
                }
            
            return {
                "status": "success",
                "documents": documents,
                "document_count": len(documents),
                "url": url,
                "metadata": metadata or {}
            }
            
        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

# Singleton instance
web_connector = WebConnector()