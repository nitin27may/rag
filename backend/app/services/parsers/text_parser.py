import logging
import json
from typing import BinaryIO, List, Dict, Any, Optional
from io import TextIOWrapper
import csv
from langchain.schema import Document

logger = logging.getLogger(__name__)

class TextParser:
    """Parser for text-based files"""
    
    def parse_text(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse a text file into Document objects
        
        Args:
            file: File-like object containing text data
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        try:
            # Wrap binary file with TextIOWrapper to handle encoding
            text_file = TextIOWrapper(file, encoding='utf-8')
            text = text_file.read()
            
            # Create text metadata
            text_metadata = {
                "format": "text"
            }
            
            # Combine with passed-in metadata
            if metadata:
                text_metadata.update(metadata)
            
            # Create a document
            document = Document(
                page_content=text,
                metadata=text_metadata
            )
            
            logger.info(f"Parsed text file with {len(text)} characters")
            return [document]
            
        except Exception as e:
            logger.error(f"Error parsing text file: {str(e)}")
            return []
    
    def parse_json(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse a JSON file into Document objects
        
        Args:
            file: File-like object containing JSON data
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        try:
            # Wrap binary file with TextIOWrapper to handle encoding
            text_file = TextIOWrapper(file, encoding='utf-8')
            json_data = json.load(text_file)
            
            # Convert JSON to string for text representation
            text = json.dumps(json_data, indent=2)
            
            # Create JSON metadata
            json_metadata = {
                "format": "json"
            }
            
            # Combine with passed-in metadata
            if metadata:
                json_metadata.update(metadata)
            
            # Create a document
            document = Document(
                page_content=text,
                metadata=json_metadata
            )
            
            logger.info(f"Parsed JSON file")
            return [document]
            
        except Exception as e:
            logger.error(f"Error parsing JSON file: {str(e)}")
            return []
    
    def parse_csv(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse a CSV file into Document objects
        
        Args:
            file: File-like object containing CSV data
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        try:
            # Wrap binary file with TextIOWrapper to handle encoding
            text_file = TextIOWrapper(file, encoding='utf-8')
            csv_reader = csv.reader(text_file)
            
            # Read all rows
            rows = list(csv_reader)
            
            # Convert to text - simple implementation
            text = "\n".join([",".join(row) for row in rows])
            
            # Create CSV metadata
            csv_metadata = {
                "format": "csv",
                "row_count": len(rows),
                "column_count": len(rows[0]) if rows else 0
            }
            
            # Combine with passed-in metadata
            if metadata:
                csv_metadata.update(metadata)
            
            # Create a document
            document = Document(
                page_content=text,
                metadata=csv_metadata
            )
            
            logger.info(f"Parsed CSV file with {len(rows)} rows")
            return [document]
            
        except Exception as e:
            logger.error(f"Error parsing CSV file: {str(e)}")
            return []
    
    def parse(self, file: BinaryIO, metadata: Dict[str, Any] = None) -> List[Document]:
        """
        Parse a text-based file into Document objects based on the file type
        
        Args:
            file: File-like object
            metadata: Optional metadata to add to the documents
            
        Returns:
            List of Document objects
        """
        # Determine file type from metadata
        file_format = metadata.get("mime_type", "") if metadata else ""
        
        if file_format == "application/json":
            return self.parse_json(file, metadata)
        elif file_format == "text/csv":
            return self.parse_csv(file, metadata)
        elif file_format.startswith("text/"):
            return self.parse_text(file, metadata)
        else:
            # Default to text parser
            logger.warning(f"Using default text parser for: {file_format}")
            return self.parse_text(file, metadata)

# Singleton instance
text_parser = TextParser()
