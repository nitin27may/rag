import logging
from typing import List, Dict, Any, BinaryIO, Optional

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.services.parsers.base import BaseParser
from app.core.config import settings

logger = logging.getLogger(__name__)

class TextParser(BaseParser):
    """Parser for plain text documents"""
    
    def __init__(self):
        super().__init__()
        self.supported_mimetypes = [
            "text/plain",
            "text/markdown"
        ]
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def parse(self, file_data: BinaryIO, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Parse a text document into chunks
        
        Args:
            file_data: File-like object containing the text data
            metadata: Optional metadata to include with the document
            
        Returns:
            List of Document objects
        """
        if metadata is None:
            metadata = {}
        
        try:
            # Read the file
            text = file_data.read().decode("utf-8")
            
            # Add metadata
            metadata["format"] = "text"
            if metadata.get("mime_type") == "text/markdown":
                metadata["format"] = "markdown"
            
            if text:
                doc = Document(
                    page_content=text,
                    metadata=metadata
                )
                
                # Split into chunks
                return self.text_splitter.split_documents([doc])
            
            return []
        
        except Exception as e:
            logger.error(f"Error parsing text: {str(e)}")
            raise