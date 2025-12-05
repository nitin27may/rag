import logging
from typing import Optional

from app.services.parsers.document_parser import document_parser
from app.services.parsers.image_parser import image_parser
from app.services.parsers.text_parser import text_parser
from app.services.parsers.web_parser import web_parser

logger = logging.getLogger(__name__)

class ParserFactory:
    """Factory for document parsers"""
    
    def get_parser(self, mime_type: str):
        """
        Get the appropriate parser for the given MIME type
        
        Args:
            mime_type: MIME type of the document
            
        Returns:
            Parser instance
        """
        # For application/pdf and similar document types
        if mime_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            logger.debug(f"Using document parser for MIME type: {mime_type}")
            return document_parser
        
        # For text-based documents
        elif mime_type.startswith('text/') or mime_type == 'application/json':
            logger.debug(f"Using text parser for MIME type: {mime_type}")
            return text_parser
        
        # For images
        elif mime_type.startswith('image/'):
            logger.debug(f"Using image parser for MIME type: {mime_type}")
            return image_parser
        
        # For web URLs
        elif mime_type == 'text/html' or mime_type == 'application/web':
            logger.debug(f"Using web parser for MIME type: {mime_type}")
            return web_parser
        
        else:
            logger.warning(f"No parser available for MIME type: {mime_type}")
            return None
    
    def get_parser_for_url(self):
        """Get a parser specifically for URLs"""
        return web_parser

# Singleton instance
parser_factory = ParserFactory()
