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
from app.services.connectors.database_connector import database_connector
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
                    db_document.is_processed = True  # Mark as processed even with error
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
                    db_document.is_processed = True  # Mark as processed even with error
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
                db_document.is_processed = True  # Mark as processed even with error
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
            
            # Generate a unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Execute the query and get data
            df = database_connector.execute_query(connection_string, query)
            
            if df.empty:
                return {
                    "status": "warning",
                    "message": "Query returned no results"
                }
            
            # Convert DataFrame to LangChain documents
            source_info = {
                "query": query,
                "description": description or f"Database query results",
                "row_count": len(df),
                "columns": df.columns.tolist(),
                "document_id": doc_id
            }
            
            documents = database_connector.data_to_documents(df, source_info)
            
            if not documents:
                return {
                    "status": "warning",
                    "message": "No content could be extracted from query results"
                }
            
            # Create database record for the document
            db_document = DBDocument(
                id=doc_id,
                title=description or f"Database Query: {query[:50]}...",
                description=description,
                source_type="database",
                processed=True,
                doc_metadata={
                    "query": query,
                    "row_count": len(df),
                    "columns": df.columns.tolist()
                }
            )
            db.add(db_document)
            db.flush()
            
            # Store chunks in the database
            for i, doc in enumerate(documents):
                chunk = DocumentChunk(
                    document_id=doc_id,
                    chunk_index=i,
                    content=doc.page_content,
                    chunk_metadata=doc.metadata
                )
                db.add(chunk)
            
            # Add document_id to each document's metadata for vector store
            for doc in documents:
                doc.metadata["document_id"] = doc_id
            
            # Store in vector database
            vector_store.add_documents(
                documents=documents,
                collection_name=settings.COLLECTIONS.get("documents", "documents")
            )
            
            db.commit()
            
            logger.info(f"Successfully processed database query with {len(documents)} chunks")
            
            return {
                "id": doc_id,
                "status": "success",
                "message": f"Successfully indexed {len(df)} rows in {len(documents)} chunks",
                "chunk_count": len(documents),
                "collection": settings.COLLECTIONS.get("documents", "documents")
            }
        
        except Exception as e:
            logger.error(f"Error processing database: {str(e)}")
            if db:
                db.rollback()
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
            
            # Get the document chunks - use chunk IDs as vector IDs
            # In langchain-postgres PGVector, the vector ID is the same as the chunk ID we pass
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).all()
            
            # Delete from vector store using chunk IDs
            chunk_ids = [chunk.id for chunk in chunks]
            if chunk_ids:
                try:
                    vector_store.delete(
                        ids=chunk_ids,
                        collection_name=document.collection_name or "documents"
                    )
                except Exception as e:
                    logger.warning(f"Error deleting vectors from store: {str(e)}")
            
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