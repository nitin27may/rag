import logging
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import mimetypes
from urllib.parse import urlparse

from app.db.session import get_db
from app.models.document import Document, DocumentChunk
from app.schemas.schemas import (
    DocumentResponse, 
    DocumentChunkResponse, 
    DocumentCreate, 
    WebScrapingRequest,
    DatabaseQueryRequest,
    ProcessingResponse
)
from app.services.document_processor import document_processor
from app.services.connectors.web_connector import web_connector
from app.services.vector_store import vector_store
from app.services.parsers.factory import parser_factory
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=ProcessingResponse)
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a document to be processed and indexed
    
    Returns:
        ProcessingResponse: A response object containing:
            - id: The unique document ID (important for future reference)
            - status: Success or error status
            - message: Additional information about the processing
            - error: Error details if processing failed
    """
    # Get the file extension
    filename = file.filename
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )
    
    file_ext = os.path.splitext(filename)[1].lower().lstrip('.')
    if not file_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Could not determine file extension for: {filename}"
        )
    
    # Get MIME type from content_type header, or infer from extension
    mime_type = file.content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    
    # Map common extensions to MIME types if detection failed
    EXTENSION_MIME_MAP = {
        'md': 'text/markdown',
        'txt': 'text/plain',
        'csv': 'text/csv',
        'json': 'application/json',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'html': 'text/html',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'yml': 'text/yaml',
    }
    
    # If MIME type is generic, try to infer from extension
    if mime_type == 'application/octet-stream' and file_ext in EXTENSION_MIME_MAP:
        mime_type = EXTENSION_MIME_MAP[file_ext]
        logger.info(f"Inferred MIME type from extension: {file_ext} -> {mime_type}")
    
    logger.info(f"Processing file upload: {filename}, extension: {file_ext}, MIME type: {mime_type}")
    
    # Check if the file extension is supported
    supported_exts = settings.SUPPORTED_DOCUMENT_TYPES + settings.SUPPORTED_IMAGE_TYPES
    if file_ext not in supported_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: .{file_ext}. Supported extensions: {', '.join(supported_exts)}"
        )
    
    # Process the document
    try:
        result = document_processor.process_file(
            file=file.file,
            filename=filename,
            mime_type=mime_type,
            description=description,
            db=db
        )
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        
        # Ensure the document ID is included in the response
        if "id" not in result or not result["id"]:
            logger.warning("Document processed but no ID was returned")
            raise HTTPException(
                status_code=500,
                detail="Document processed but no ID was returned"
            )
            
        return result
    
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.post("/web", response_model=ProcessingResponse)
async def process_web_page(
    request: WebScrapingRequest,
    db: Session = Depends(get_db)
):
    """
    Process a web page and add it to the document store
    """
    try:
        url = str(request.url)
        logger.info(f"Processing web page: {url}")
        
        # Generate a unique ID for the document
        doc_id = str(uuid.uuid4())
        
        # Create URL parsing result
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        path = parsed_url.path
        
        # Create a database record for the web page
        db_document = Document(
            id=doc_id,
            filename=f"{domain}{path}",
            title=domain,
            description=request.description if request.description else f"Web page from {domain}",
            mime_type="text/html",
            source_type="web",
            source_path=url,
            is_processed=False,
            is_indexed=False,
            doc_metadata={
                "url": url,
                "domain": domain,
                "path": path
            }
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Get the web parser
        web_parser = parser_factory.get_parser_for_url()
        
        # Parse the web page
        parsed_documents = web_parser.parse(url, db_document.doc_metadata)
        
        if not parsed_documents:
            logger.warning(f"No content extracted from web page: {url}")
            db_document.processing_error = "No content extracted from web page"
            db_document.is_processed = True  # Mark as processed even with error
            db.commit()
            return ProcessingResponse(
                id=doc_id,
                status="warning",
                message="Web page processed but no content was extracted"
            )
        
        # Process the parsed documents
        from app.models.document import DocumentChunk
        from app.services.vector_store import vector_store
        
        # Store chunks in the database
        for i, doc in enumerate(parsed_documents):
            chunk = DocumentChunk(
                document_id=doc_id,
                chunk_index=i,
                content=doc.page_content,
                chunk_metadata=doc.metadata
            )
            db.add(chunk)
        
        # Store in vector database - use 'web_pages' collection
        collection_name = "web_pages"
        
        # IMPORTANT: Add document_id to each document's metadata before storing in vector database
        for doc in parsed_documents:
            if not doc.metadata:
                doc.metadata = {}
            doc.metadata["document_id"] = doc_id
        
        vector_ids = vector_store.add_documents(
            documents=parsed_documents,
            collection_name=collection_name
        )
        
        # Update chunk vector IDs and mark document as processed
        for i, vector_id in enumerate(vector_ids):
            chunk = db.query(DocumentChunk).filter(
                DocumentChunk.document_id == doc_id,
                DocumentChunk.chunk_index == i
            ).first()
            
            if chunk:
                chunk.vector_id = vector_id
        
        db_document.is_processed = True
        db_document.is_indexed = True
        db_document.collection_name = collection_name
        db.commit()
        
        return ProcessingResponse(
            id=doc_id,
            status="success",
            message=f"Web page processed successfully with {len(parsed_documents)} chunks"
        )
    
    except Exception as e:
        logger.error(f"Error processing web page: {str(e)}")
        return ProcessingResponse(
            status="error",
            error=str(e)
        )


@router.post("/database", response_model=ProcessingResponse)
async def process_database_query(
    request: DatabaseQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Process data from a database and index it
    """
    try:
        # Process the database query
        result = document_processor.process_database(
            connection_string=request.connection_string,
            query=request.query,
            description=request.description,
            db=db
        )
        
        if result.get("status") == "not_implemented":
            raise HTTPException(
                status_code=501,
                detail="Database processing is not yet implemented"
            )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error")
            )
        
        return result
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error processing database query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing database query: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all documents
    """
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {document_id}"
        )
    
    return document


@router.get("/{document_id}/chunks", response_model=List[DocumentChunkResponse])
async def get_document_chunks(
    document_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get chunks for a specific document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {document_id}"
        )
    
    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).offset(skip).limit(limit).all()
    
    return chunks


@router.delete("/{document_id}", response_model=ProcessingResponse)
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a document and its chunks
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {document_id}"
        )
    
    # Delete the document
    result = document_processor.delete_document(document_id, db)
    
    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unknown error")
        )
    
    return result