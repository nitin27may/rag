import logging
from typing import List, Dict, Any, BinaryIO, Optional
import pandas as pd
import json
import io

from langchain.schema import Document

from app.services.parsers.base import BaseParser
from app.services.chunking_service import chunking_service

logger = logging.getLogger(__name__)

class StructuredDataParser(BaseParser):
    """Parser for structured data formats (CSV, Excel, JSON)"""
    
    def __init__(self):
        super().__init__()
        self.supported_mimetypes = [
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/json"
        ]
        # Use centralized chunking service
        self.chunking_service = chunking_service
    
    def _parse_csv(self, file_data: BinaryIO, metadata: Dict[str, Any]):
        """Parse CSV data"""
        try:
            # Load CSV into DataFrame
            df = pd.read_csv(file_data)
            
            # Add metadata
            metadata["format"] = "csv"
            metadata["columns"] = df.columns.tolist()
            metadata["row_count"] = len(df)
            
            return self._process_dataframe(df, metadata)
        
        except Exception as e:
            logger.error(f"Error parsing CSV: {str(e)}")
            raise
    
    def _parse_excel(self, file_data: BinaryIO, metadata: Dict[str, Any]):
        """Parse Excel data"""
        try:
            # Load Excel into DataFrame(s)
            excel_file = pd.ExcelFile(file_data)
            sheet_names = excel_file.sheet_names
            
            metadata["format"] = "excel"
            metadata["sheets"] = sheet_names
            
            documents = []
            
            # Process each sheet
            for sheet in sheet_names:
                df = excel_file.parse(sheet)
                
                sheet_metadata = metadata.copy()
                sheet_metadata["sheet"] = sheet
                sheet_metadata["columns"] = df.columns.tolist()
                sheet_metadata["row_count"] = len(df)
                
                documents.extend(self._process_dataframe(df, sheet_metadata))
            
            return documents
        
        except Exception as e:
            logger.error(f"Error parsing Excel: {str(e)}")
            raise
    
    def _parse_json(self, file_data: BinaryIO, metadata: Dict[str, Any]):
        """Parse JSON data"""
        try:
            # Load JSON
            json_data = json.load(file_data)
            
            metadata["format"] = "json"
            
            # Convert to DataFrame if possible
            if isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict):
                df = pd.DataFrame(json_data)
                metadata["row_count"] = len(df)
                metadata["columns"] = df.columns.tolist()
                return self._process_dataframe(df, metadata)
            
            # Otherwise, just use the raw JSON as text
            json_text = json.dumps(json_data, indent=2)
            
            document = Document(
                page_content=json_text,
                metadata=metadata
            )
            
            return self.chunking_service.split_documents([document])
        
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            raise
    
    def _process_dataframe(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> List[Document]:
        """Process a DataFrame into Document objects"""
        documents = []
        
        # Strategy 1: Convert the entire DataFrame to a string representation
        if len(df) <= 50:  # For small DataFrames, include the full table
            full_text = df.to_string(index=False)
            full_metadata = metadata.copy()
            full_metadata["representation"] = "full_table"
            
            documents.append(Document(
                page_content=full_text,
                metadata=full_metadata
            ))
        
        # Strategy 2: Process row by row for more detailed access
        batch_size = 20  # Process rows in batches
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            # Convert batch to text
            batch_text = batch.to_string(index=False)
            
            batch_metadata = metadata.copy()
            batch_metadata["row_range"] = f"{i}-{min(i+batch_size-1, len(df)-1)}"
            batch_metadata["representation"] = "batch"
            
            documents.append(Document(
                page_content=batch_text,
                metadata=batch_metadata
            ))
        
        # Strategy 3: Include column descriptions with sample values
        column_text = "Column descriptions:\n"
        for column in df.columns:
            sample_values = df[column].dropna().sample(min(3, len(df))).tolist()
            sample_text = ", ".join([str(val) for val in sample_values])
            column_text += f"- {column}: Sample values: {sample_text}\n"
        
        column_metadata = metadata.copy()
        column_metadata["representation"] = "columns"
        
        documents.append(Document(
            page_content=column_text,
            metadata=column_metadata
        ))
        
        # Split documents if they're too large
        result = []
        for doc in documents:
            result.extend(self.chunking_service.split_documents([doc]))
        
        return result
    
    def parse(self, file_data: BinaryIO, metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Parse structured data into documents
        
        Args:
            file_data: File-like object containing the structured data
            metadata: Optional metadata to include with the document
            
        Returns:
            List of Document objects
        """
        if metadata is None:
            metadata = {}
        
        mime_type = metadata.get("mime_type", "")
        
        if mime_type == "text/csv":
            return self._parse_csv(file_data, metadata)
        
        elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return self._parse_excel(file_data, metadata)
        
        elif mime_type == "application/json":
            return self._parse_json(file_data, metadata)
        
        else:
            logger.error(f"Unsupported MIME type for structured parser: {mime_type}")
            raise ValueError(f"Unsupported MIME type: {mime_type}")