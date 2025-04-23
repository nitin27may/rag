import logging
import os
from typing import List, Dict, Any, BinaryIO, Optional
import uuid
from io import BytesIO
import mimetypes

from sqlalchemy.orm import Session
from langchain.schema import Document

from app.models.document import Document as DBDocument, DocumentChunk
from app.services.parsers.factory import parser_factory
from app.services.vector_store import vector_store
from app.services.object_storage import object_storage
from app.core.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Service to process and index documents"""
    
    def process_file(
        self, 
        file: BinaryIO, 
        filename: str, 
        mime_type: str, 
        description: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Process a file, parse it, and store it in the vector database
        
        Args:
            file: File-like object containing the file data
            filename: Original filename
            mime_type: MIME type of the file
            description: Optional description of the file
            db: Database session
            
        Returns:
            Dictionary with information about the processed document
        """
        try:
            logger.info(f"Processing file: {filename} with MIME type: {mime_type}")
            
            # Generate a unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Create object name for storage
            file_extension = os.path.splitext(filename)[1].lower()
            if not file_extension:
                # Try to get extension from MIME type
                ext = mimetypes.guess_extension(mime_type)
                if ext:
                    file_extension = ext
            
            object_name = f"{doc_id}{file_extension}"
            
            # Save file to object storage
            file.seek(0)  # Ensure we're at the start of the file
            storage_path = object_storage.upload_file(
                file_data=file,
                object_name=object_name,
                content_type=mime_type
            )
            
            # Create database record
            db_document = DBDocument(
                id=doc_id,
                filename=filename,
                title=os.path.splitext(filename)[0],
                description=description,
                mime_type=mime_type,
                source_type="file",
                storage_path=storage_path,
                is_processed=False,
                is_indexed=False,
                doc_metadata={
                    "filename": filename,
                    "mime_type": mime_type,
                }
            )
            
            if db:
                db.add(db_document)
                db.commit()
                db.refresh(db_document)
            
            # Parse the document
            file.seek(0)  # Reset file pointer
            
            # Get appropriate parser
            parser = parser_factory.get_parser(mime_type)
            if not parser:
                logger.warning(f"No parser available for MIME type: {mime_type}")
                if db:
                    db_document.processing_error = f"No parser available for MIME type: {mime_type}"
                    db.commit()
                
                return {
                    "id": doc_id,
                    "status": "error",
                    "error": f"No parser available for MIME type: {mime_type}"
                }
            
            # Parse the document
            parsed_documents = parser.parse(file, db_document.doc_metadata)
            
            if not parsed_documents:
                logger.warning(f"No content extracted from document: {filename}")
                if db:
                    db_document.processing_error = "No content extracted from document"
                    db.commit()
                
                return {
                    "id": doc_id,
                    "status": "warning",
                    "message": "Document processed but no content was extracted"
                }
            
            # Store chunks in the database
            if db:
                for i, doc in enumerate(parsed_documents):
                    chunk = DocumentChunk(
                        document_id=doc_id,
                        chunk_index=i,
                        content=doc.page_content,
                        chunk_metadata=doc.metadata  # Changed from 'metadata' to 'chunk_metadata'
                    )
                    db.add(chunk)
                
                db_document.is_processed = True
                db.commit()
            
            # Determine the collection based on the document type
            collection_name = "documents"
            if mime_type.startswith("image/"):
                collection_name = "images"
            
            # IMPORTANT: Add document_id to each document's metadata before storing in vector database
            for doc in parsed_documents:
                if not doc.metadata:
                    doc.metadata = {}
                doc.metadata["document_id"] = doc_id
            
            # Store in vector database
            vector_ids = vector_store.add_documents(
                documents=parsed_documents,
                collection_name=collection_name
            )
            
            # Update chunk vector IDs in the database
            if db and vector_ids:
                for i, vector_id in enumerate(vector_ids):
                    chunk = db.query(DocumentChunk).filter(
                        DocumentChunk.document_id == doc_id,
                        DocumentChunk.chunk_index == i
                    ).first()
                    
                    if chunk:
                        chunk.vector_id = vector_id
                
                db_document.is_indexed = True
                db_document.collection_name = collection_name
                db.commit()
            
            return {
                "id": doc_id,
                "status": "success",
                "chunk_count": len(parsed_documents),
                "collection": collection_name
            }
        
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            
            if db and 'db_document' in locals():
                db_document.processing_error = str(e)
                db.commit()
            
            return {
                "id": doc_id if 'doc_id' in locals() else None,
                "status": "error",
                "error": str(e)
            }
    
    def process_url(
        self, 
        url: str, 
        description: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Process a URL, scrape its content, and store it in the vector database
        
        Args:
            url: URL to scrape and process
            description: Optional description
            db: Database session
            
        Returns:
            Dictionary with information about the processed document
        """
        try:
            logger.info(f"Processing URL: {url}")
            
            # Use web scraper to get content (we'll implement this later)
            # For now, we'll just return a placeholder
            return {
                "status": "not_implemented",
                "message": "URL processing not yet implemented"
            }
        
        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def process_database(
        self,
        connection_string: str,
        query: str,
        description: Optional[str] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Process data from a database, extract it, and store it in the vector database
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            description: Optional description
            db: Database session
            
        Returns:
            Dictionary with information about the processed document
        """
        try:
            logger.info(f"Processing database query")
            
            # Connect to database and execute query (we'll implement this later)
            # For now, we'll just return a placeholder
            return {
                "status": "not_implemented",
                "message": "Database processing not yet implemented"
            }
        
        except Exception as e:
            logger.error(f"Error processing database: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def delete_document(self, document_id: str, db: Session) -> Dict[str, Any]:
        """
        Delete a document and its chunks from storage and vector database
        
        Args:
            document_id: ID of the document to delete
            db: Database session
            
        Returns:
            Dictionary with status information
        """
        try:
            logger.info(f"Deleting document: {document_id}")
            
            # Get the document
            document = db.query(DBDocument).filter(DBDocument.id == document_id).first()
            
            if not document:
                return {
                    "status": "error",
                    "error": f"Document not found: {document_id}"
                }
            
            # Get the document chunks
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
            
            # Delete from vector store
            vector_ids = [chunk.vector_id for chunk in chunks if chunk.vector_id]
            if vector_ids:
                vector_store.delete(
                    ids=vector_ids,
                    collection_name=document.collection_name or "documents"
                )
            
            # Delete from object storage if it exists
            if document.storage_path:
                try:
                    bucket, object_name = document.storage_path.split('/', 1)
                    object_storage.delete_file(object_name=object_name, bucket_name=bucket)
                except Exception as e:
                    logger.warning(f"Error deleting file from storage: {str(e)}")
            
            # Delete from database
            db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
            db.delete(document)
            db.commit()
            
            return {
                "status": "success",
                "message": f"Document {document_id} deleted successfully"
            }
        
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Singleton instance
document_processor = DocumentProcessor()