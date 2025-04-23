import logging
from typing import List, Dict, Any, BinaryIO, Optional
import io

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF

from app.services.parsers.base import BaseParser
from app.core.config import settings

logger = logging.getLogger(__name__)

class PDFParser(BaseParser):
    """Parser for PDF documents using PyMuPDF"""
    
    def __init__(self):
        super().__init__()
        self.supported_mimetypes = ["application/pdf"]
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def parse(self, file_data: BinaryIO, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Parse a PDF document into chunks
        
        Args:
            file_data: File-like object containing the PDF data
            metadata: Optional metadata to include with the document
            
        Returns:
            List of Document objects
        """
        if metadata is None:
            metadata = {}
        
        try:
            # Read the file into memory
            file_bytes = file_data.read()
            
            # Open the PDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            
            # Add document metadata
            metadata["page_count"] = len(doc)
            metadata["format"] = "pdf"
            
            if doc.metadata:
                metadata["title"] = doc.metadata.get("title", "")
                metadata["author"] = doc.metadata.get("author", "")
                metadata["subject"] = doc.metadata.get("subject", "")
                metadata["keywords"] = doc.metadata.get("keywords", "")
            
            # Extract text from each page with page numbers
            texts = []
            for i, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    page_metadata = metadata.copy()
                    page_metadata["page"] = i + 1
                    texts.append(Document(
                        page_content=text,
                        metadata=page_metadata
                    ))
            
            # Split into chunks
            if texts:
                return self.text_splitter.split_documents(texts)
            
            return []
        
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise