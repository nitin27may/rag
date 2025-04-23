from typing import Optional, List, Dict, Any, Type, Union
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, create_model, validator


class DocumentBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source_type: str


class DocumentCreate(DocumentBase):
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None


class DocumentUpdate(DocumentBase):
    processed: Optional[bool] = None
    vector_store_id: Optional[str] = None
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata
    processing_error: Optional[str] = None


class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    processed: bool
    vector_store_id: Optional[str] = None
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata
    processing_error: Optional[str] = None

    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    id: str
    filename: str
    title: str
    description: Optional[str] = None
    mime_type: str
    source_type: str
    source_path: Optional[str] = None
    storage_path: Optional[str] = None
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    doc_metadata: Optional[Dict[str, Any]] = None
    is_processed: bool
    is_indexed: bool
    processing_error: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    collection_name: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    vector_id: Optional[str] = None
    chunk_metadata: Optional[Dict[str, Any]] = None  # Changed from 'metadata' to 'chunk_metadata'

    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    query: str
    collection_names: Optional[List[str]] = None
    filter_criteria: Optional[Dict[str, Any]] = None
    document_id: Optional[str] = None  # Added document_id for filtering by specific document
    top_k: Optional[int] = Field(5, ge=1, le=20)


class QueryResponse(BaseModel):
    query: str
    answer: str
    context: Optional[str] = None
    documents: Optional[List[Dict[str, Any]]] = None
    metrics: Dict[str, Any]


class WebScrapingRequest(BaseModel):
    url: HttpUrl
    description: Optional[str] = None


class DatabaseQueryRequest(BaseModel):
    connection_string: str
    query: str
    description: Optional[str] = None


class ProcessingResponse(BaseModel):
    """Response from document processing operations"""
    id: Optional[str] = Field(None, description="The unique document ID - important for future reference")
    status: str = Field(..., description="Status of the operation: 'success', 'error', or 'warning'")
    message: Optional[str] = Field(None, description="Additional information about the processing")
    error: Optional[str] = Field(None, description="Error details if processing failed")
    chunk_count: Optional[int] = Field(None, description="Number of chunks created from the document")
    collection: Optional[str] = Field(None, description="Vector store collection where the document was indexed")


class DataSourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    active: bool = True


class DataSourceCreate(DataSourceBase):
    connection_string: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    connection_string: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata


class DataSourceResponse(BaseModel):
    id: str
    name: str
    source_type: str
    description: Optional[str] = None
    is_active: bool
    connection_details: Optional[Dict[str, Any]] = None
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DataSource(DataSourceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    connection_string: Optional[str] = None
    username: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    doc_metadata: Optional[Dict[str, Any]] = None  # Changed from metadata to doc_metadata
    error: Optional[str] = None

    class Config:
        orm_mode = True


class QueryResult(BaseModel):
    query: str
    result: Optional[str] = None
    documents: Optional[List[Dict[str, Any]]] = None
    execution_time_ms: Optional[int] = None


class StructuredQueryRequest(BaseModel):
    """Request model for structured data extraction from documents"""
    document_id: str = Field(..., description="Unique ID of the document to query")
    schema_definition: Dict[str, Union[str, Dict[str, Any]]] = Field(
        ..., 
        description="Definition of the structured data schema to extract. Key is the field name, value is the field type or nested object."
    )
    extraction_strategy: str = Field(
        "auto", 
        description="Strategy to use for extracting data: 'auto', 'template', 'pattern'"
    )
    prompt_template: Optional[str] = Field(
        None, 
        description="Custom prompt template to guide the extraction"
    )


class StructuredDataField(BaseModel):
    """Model for a single extracted field"""
    name: str
    value: Any
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source_text: Optional[str] = None


class StructuredQueryResponse(BaseModel):
    """Response model for structured data extraction"""
    document_id: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    fields: List[StructuredDataField] = Field(default_factory=list)
    extraction_metrics: Dict[str, Any] = Field(default_factory=dict)