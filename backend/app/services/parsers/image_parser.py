import logging
import os
from typing import BinaryIO, List, Dict, Any, Optional
from io import BytesIO

from PIL import Image
import pytesseract
from langchain.schema import Document

logger = logging.getLogger(__name__)

class ImageParser:
    """Parser for image files with OCR"""
    
    def __init__(self):
        # Configure pytesseract path if needed
        pytesseract_path = os.environ.get("TESSERACT_PATH")
        if pytesseract_path:
            pytesseract.pytesseract.tesseract_cmd = pytesseract_path
    
    def parse_image(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse an image file into Document objects using OCR
        
        Args:
            file: File-like object containing image data
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        try:
            # Copy to BytesIO to ensure seekable
            buffer = BytesIO(file.read())
            
            # Open image with PIL
            logger.info("Parsing image with OCR")
            image = Image.open(buffer)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            
            # Skip if no text was extracted
            if not text.strip():
                logger.warning("No text extracted from image")
                return []
            
            # Create image metadata
            img_metadata = {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode
            }
            
            # Combine with passed-in metadata
            if metadata:
                img_metadata.update(metadata)
            
            # Create a document
            document = Document(
                page_content=text,
                metadata=img_metadata
            )
            
            logger.info(f"Extracted {len(text)} characters from image")
            return [document]
            
        except Exception as e:
            logger.error(f"Error parsing image: {str(e)}")
            return []
    
    def parse(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse an image file into Document objects
        
        Args:
            file: File-like object
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        return self.parse_image(file, metadata)

# Singleton instance
image_parser = ImageParser()