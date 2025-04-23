import logging
from typing import Optional

from app.services.parsers.base import BaseParser
from app.services.parsers.pdf_parser import PDFParser
from app.services.parsers.docx_parser import DocxParser
from app.services.parsers.image_parser import ImageParser
from app.services.parsers.structured_parser import StructuredDataParser
from app.services.parsers.text_parser import TextParser

logger = logging.getLogger(__name__)

class ParserFactory:
    """Factory class to get the appropriate parser for a file type"""
    
    def __init__(self):
        self.parsers = [
            PDFParser(),
            DocxParser(),
            ImageParser(),
            StructuredDataParser(),
            TextParser()
        ]
    
    def get_parser(self, mime_type: str) -> Optional[BaseParser]:
        """
        Get the appropriate parser for a MIME type
        
        Args:
            mime_type: MIME type of the file
            
        Returns:
            Parser instance or None if no matching parser is found
        """
        for parser in self.parsers:
            if parser.supports_mimetype(mime_type):
                return parser
        
        logger.warning(f"No parser found for MIME type: {mime_type}")
        return None


# Singleton instance
parser_factory = ParserFactory()