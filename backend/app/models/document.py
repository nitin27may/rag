from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.session import Base
from typing import List, Optional, Dict, Any
import uuid


class Document(Base):
    """Model for storing document metadata"""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    mime_type = Column(String)
    source_type = Column(String)  # file, database, website, etc.
    source_path = Column(String)  # Original path or URL
    storage_path = Column(String)  # Path in MinIO
    file_size = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)
    
    # Metadata
    doc_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid conflict
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    is_indexed = Column(Boolean, default=False)
    processing_error = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    # Vector Store Collection
    collection_name = Column(String, default="documents")


class DocumentChunk(Base):
    """Model for storing document chunks with embeddings"""
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"))
    chunk_index = Column(Integer)
    content = Column(Text)
    
    # Vector embedding stored directly in PostgreSQL using pgvector
    # Note: This column is optional and primarily for reference. The actual vector storage
    # is handled by langchain-postgres PGVector which creates its own tables with
    # configurable dimensions based on EMBEDDING_MODEL_DIMENSIONS setting.
    # Default dimension: 3072 (text-embedding-3-large)
    embedding = Column(Vector(3072), nullable=True)
    
    # For structured data
    column_mapping = Column(JSON, nullable=True)
    
    # For images
    bbox = Column(String, nullable=True)  # Bounding box coordinates
    
    # Metadata - renamed to avoid SQLAlchemy reserved word conflict
    chunk_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata'
    
    # Relationships
    document = relationship("Document", back_populates="chunks")


class DataSource(Base):
    """Model for storing data source configurations"""
    __tablename__ = "data_sources"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    source_type = Column(String)  # file_system, database, website, api
    
    # Connection details as JSON
    connection_details = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Documents from this source
    documents = relationship("Document", primaryjoin="Document.source_path == foreign(DataSource.id)")


class QueryLog(Base):
    """Model for logging queries"""
    __tablename__ = "query_logs"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    query_text = Column(Text)
    
    # Query metadata
    query_type = Column(String)  # semantic, keyword, hybrid
    parameters = Column(JSON, nullable=True)
    
    # Results
    document_ids = Column(JSON, nullable=True)  # List of retrieved document IDs
    
    # Performance metrics
    retrieval_time_ms = Column(Float, nullable=True)
    generation_time_ms = Column(Float, nullable=True)
    total_time_ms = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())