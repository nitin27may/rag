import logging
import json
from typing import Dict, Any, List, Optional, Union
from sqlalchemy.orm import Session
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError
import traceback

from app.models.document import Document, DocumentChunk
from app.services.retrieval.retriever import rag_retriever
from app.services.vector_store import vector_store
from app.schemas.schemas import StructuredDataField

logger = logging.getLogger(__name__)

class StructuredDataExtractor:
    """Service for extracting structured data from documents"""
    
    def __init__(self):
        self.default_prompt_template = """
        You are an AI assistant tasked with extracting structured information from text documents.
        
        Extract the following information from the text:
        {schema_instructions}
        
        Return the extracted data in a valid JSON object with the exact keys specified above.
        If a value cannot be determined, use null or an empty value of the appropriate type.
        Do not include any explanations, only the JSON object.
        
        Here is the text:
        {document_text}
        """
        
    def _create_schema_instructions(self, schema_definition: Dict[str, Any]) -> str:
        """Convert schema definition to human-readable instructions"""
        instructions = []
        
        for field_name, field_info in schema_definition.items():
            if isinstance(field_info, dict):
                # Handle nested objects
                if "type" in field_info:
                    field_type = field_info["type"]
                    description = field_info.get("description", "")
                    instructions.append(f"- {field_name}: ({field_type}) {description}")
                else:
                    nested_instructions = []
                    for nested_field, nested_info in field_info.items():
                        if isinstance(nested_info, dict) and "type" in nested_info:
                            nested_type = nested_info["type"]
                            nested_desc = nested_info.get("description", "")
                            nested_instructions.append(f"  - {nested_field}: ({nested_type}) {nested_desc}")
                        else:
                            nested_instructions.append(f"  - {nested_field}: {nested_info}")
                    
                    instructions.append(f"- {field_name}: (object) containing:")
                    instructions.extend(nested_instructions)
            else:
                # Simple field
                instructions.append(f"- {field_name}: ({field_info})")
        
        return "\n".join(instructions)
    
    def _combine_document_chunks(self, chunks: List[DocumentChunk]) -> str:
        """Combine document chunks into a single text document"""
        # Sort chunks by index to maintain document order
        sorted_chunks = sorted(chunks, key=lambda x: x.chunk_index)
        combined_text = "\n\n".join([chunk.content for chunk in sorted_chunks])
        return combined_text
    
    def _extract_data_using_llm(
        self, 
        document_text: str, 
        schema_definition: Dict[str, Any],
        prompt_template: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extract structured data using the LLM"""
        from app.services.retrieval.generator import rag_generator
        
        schema_instructions = self._create_schema_instructions(schema_definition)
        
        # Use custom template if provided, otherwise use default
        template = prompt_template if prompt_template else self.default_prompt_template
        prompt = template.format(
            schema_instructions=schema_instructions,
            document_text=document_text
        )
        
        # Call the LLM to extract data
        result = rag_generator.call_llm(prompt)
        
        # Parse the response as JSON
        try:
            # Try to extract JSON from the response
            if result.startswith("```json"):
                result = result.split("```json")[1]
                if "```" in result:
                    result = result.split("```")[0]
            elif result.startswith("```"):
                result = result.split("```")[1]
                if "```" in result:
                    result = result.split("```")[0]
            
            # Clean the result
            result = result.strip()
            
            # Parse JSON
            extracted_data = json.loads(result)
            return extracted_data
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
            logger.error(f"Response was: {result}")
            # Fall back to a more structured approach
            return self._fallback_extraction_with_pydantic(result, schema_definition)
    
    def _fallback_extraction_with_pydantic(
        self, 
        result: str, 
        schema_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback method for extraction using pydantic"""
        try:
            # Try to convert raw text to JSON using a more lenient approach
            # This is a simplified implementation - would need more robust parsing in production
            data = {}
            for field_name in schema_definition.keys():
                if f'"{field_name}"' in result or f"'{field_name}'" in result:
                    parts = result.split(f'"{field_name}"')
                    if len(parts) < 2:
                        parts = result.split(f"'{field_name}'")
                    
                    if len(parts) >= 2:
                        value_part = parts[1].strip().strip(':').strip()
                        if value_part.startswith('"') or value_part.startswith("'"):
                            end_quote = value_part[0]
                            end_idx = value_part[1:].find(end_quote) + 1
                            if end_idx > 0:
                                data[field_name] = value_part[1:end_idx]
            
            return data
            
        except Exception as e:
            logger.error(f"Fallback extraction failed: {str(e)}")
            # Return empty dict as last resort
            return {}
    
    def extract_structured_data(
        self, 
        document_id: str, 
        schema_definition: Dict[str, Any],
        extraction_strategy: str = "auto",
        prompt_template: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Extract structured data from a document
        
        Args:
            document_id: ID of the document to extract data from
            schema_definition: Definition of the structured data to extract
            extraction_strategy: Strategy to use for extraction
            prompt_template: Custom prompt template
            db: Database session
            
        Returns:
            Dictionary containing extracted data and metadata
        """
        start_time = __import__('time').time()
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            logger.error(f"Document not found: {document_id}")
            return {
                "document_id": document_id,
                "data": {},
                "metadata": {"error": "Document not found"},
                "fields": [],
                "extraction_metrics": {
                    "status": "error",
                    "error": "Document not found"
                }
            }
        
        try:
            # Get document chunks
            chunks = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document_id
            ).all()
            
            if not chunks:
                logger.warning(f"No chunks found for document: {document_id}")
                return {
                    "document_id": document_id,
                    "data": {},
                    "metadata": {
                        "filename": document.filename,
                        "mime_type": document.mime_type
                    },
                    "fields": [],
                    "extraction_metrics": {
                        "status": "error",
                        "error": "No document chunks found"
                    }
                }
            
            # Combine chunks into a single document
            document_text = self._combine_document_chunks(chunks)
            
            # Extract data based on selected strategy
            extracted_data = {}
            
            if extraction_strategy == "auto" or extraction_strategy == "template":
                extracted_data = self._extract_data_using_llm(
                    document_text=document_text,
                    schema_definition=schema_definition,
                    prompt_template=prompt_template
                )
            elif extraction_strategy == "pattern":
                # This would implement pattern-based extraction (regex, etc.)
                # Simplified implementation for now
                extracted_data = self._extract_data_using_llm(
                    document_text=document_text,
                    schema_definition=schema_definition,
                    prompt_template=prompt_template
                )
            
            # Convert extracted data to StructuredDataField format
            fields = []
            for field_name, field_value in extracted_data.items():
                fields.append(
                    StructuredDataField(
                        name=field_name,
                        value=field_value,
                        confidence=1.0,  # Default confidence
                        source_text=None  # Would require more work to extract source text
                    )
                )
            
            end_time = __import__('time').time()
            execution_time = end_time - start_time
            
            return {
                "document_id": document_id,
                "data": extracted_data,
                "metadata": {
                    "filename": document.filename,
                    "mime_type": document.mime_type,
                    "doc_metadata": document.doc_metadata
                },
                "fields": fields,
                "extraction_metrics": {
                    "status": "success",
                    "extraction_time_ms": int(execution_time * 1000),
                    "extraction_strategy": extraction_strategy
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting structured data: {str(e)}")
            logger.error(traceback.format_exc())
            
            return {
                "document_id": document_id,
                "data": {},
                "metadata": {
                    "filename": document.filename if document else None,
                    "mime_type": document.mime_type if document else None
                },
                "fields": [],
                "extraction_metrics": {
                    "status": "error",
                    "error": str(e)
                }
            }


# Create a singleton instance
structured_data_extractor = StructuredDataExtractor()