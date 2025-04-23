from abc import ABC, abstractmethod
from typing import List, Dict, Any, BinaryIO, Optional
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    """Base class for document parsers"""
    
    def __init__(self):
        self.supported_mimetypes = []
    
    @abstractmethod
    def parse(self, file_data: BinaryIO, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Parse a document into a list of Document objects
        
        Args:
            file_data: File-like object containing the file data
            metadata: Optional metadata to include with the document
            
        Returns:
            List of Document objects
        """
        pass
    
    def supports_mimetype(self, mimetype: str) -> bool:
        """Check if the parser supports a given MIME type"""
        return mimetype in self.supported_mimetypes