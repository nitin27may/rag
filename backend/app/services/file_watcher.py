import os
import time
import logging
import hashlib
import mimetypes
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from sqlalchemy import Column, String, Integer, Float, DateTime, MetaData, Table, select, insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db, engine
from app.services.document_processor import document_processor
from app.core.config import settings

logger = logging.getLogger(__name__)

class FileWatcher:
    """
    Watches for file changes in the MinIO storage directory and processes new/modified files
    """
    
    def __init__(self):
        self.watch_dir = settings.MINIO_DATA_DIR
        self.buckets = ["documents", "images", "raw"]
        self.processed_dirs = {"processed"}  # Directories to ignore
        self.file_extensions = {
            ".pdf", ".docx", ".xlsx", ".pptx", ".csv", ".txt", ".json", 
            ".md", ".html", ".xml", ".jpg", ".jpeg", ".png"
        }
        self.processed_files_table = None  # Initialize table reference as None
        self.init_db()
        
    def init_db(self):
        """Initialize database table to track processed files"""
        try:
            # Use the engine directly to avoid session management issues
            from sqlalchemy import inspect
            
            # Create metadata object
            metadata = MetaData()
            
            # Define table structure
            table_name = 'file_watcher_processed_files'
            
            # Check if the table already exists
            inspector = inspect(engine)
            
            if not inspector.has_table(table_name):
                # Create the file_watcher_processed_files table in PostgreSQL
                self.processed_files_table = Table(
                    table_name, 
                    metadata,
                    Column('file_path', String, primary_key=True),
                    Column('file_hash', String, nullable=False),
                    Column('size', Integer, nullable=False),
                    Column('last_modified', Float, nullable=False),
                    Column('processed_at', DateTime, nullable=False),
                    Column('document_id', String, nullable=False),
                )
                # Create the table
                metadata.create_all(engine)
                logger.info(f"Created {table_name} table in PostgreSQL database")
            else:
                # If table exists, reference it using metadata reflection
                self.processed_files_table = Table(
                    table_name, 
                    metadata, 
                    autoload_with=engine
                )
                logger.info(f"Using existing {table_name} table in PostgreSQL database")
            
        except Exception as e:
            logger.error(f"Error initializing file watcher table: {str(e)}")
            # Continue without crashing, we'll log errors during runtime
            
    def get_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of a file"""
        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)
            return md5_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {str(e)}")
            return ""
            
    def get_processed_files(self, db: Session) -> Dict[str, Dict]:
        """Get all processed files from database"""
        try:
            # Make sure we have a valid table reference
            if self.processed_files_table is None:
                logger.warning("Table reference is None, reinitializing database connection")
                self.init_db()
                
            if self.processed_files_table is None:
                logger.error("Failed to initialize table reference, returning empty processed files list")
                return {}
                
            # Create a proper SQLAlchemy 2.0 select statement
            query = select(
                self.processed_files_table.c.file_path,
                self.processed_files_table.c.file_hash,
                self.processed_files_table.c.size,
                self.processed_files_table.c.last_modified,
                self.processed_files_table.c.document_id
            )
            
            result = db.execute(query).fetchall()
            
            processed_files = {}
            for row in result:
                file_path = row[0] if isinstance(row, tuple) else row.file_path
                file_hash = row[1] if isinstance(row, tuple) else row.file_hash
                size = row[2] if isinstance(row, tuple) else row.size
                last_modified = row[3] if isinstance(row, tuple) else row.last_modified
                document_id = row[4] if isinstance(row, tuple) else row.document_id
                
                processed_files[file_path] = {
                    "file_hash": file_hash,
                    "size": size,
                    "last_modified": last_modified,
                    "document_id": document_id
                }
            return processed_files
        except SQLAlchemyError as e:
            logger.error(f"Database error getting processed files: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error getting processed files: {str(e)}")
            return {}
            
    def mark_as_processed(self, file_path: str, file_hash: str, size: int, 
                          last_modified: float, document_id: str, db: Session):
        """Mark a file as processed in the database"""
        try:
            # Make sure we have a valid table reference
            if self.processed_files_table is None:
                logger.warning("Table reference is None, reinitializing database connection")
                self.init_db()
                
            if self.processed_files_table is None:
                logger.error("Failed to initialize table reference, cannot mark file as processed")
                return
                
            # Insert or update record in the table
            processed_at = datetime.now()
            
            # Check if the record exists using SQLAlchemy 2.0 syntax
            query = select(self.processed_files_table.c.file_path).where(
                self.processed_files_table.c.file_path == file_path
            )
            existing = db.execute(query).first()
            
            if existing:
                # Update existing record
                stmt = self.processed_files_table.update().where(
                    self.processed_files_table.c.file_path == file_path
                ).values(
                    file_hash=file_hash,
                    size=size,
                    last_modified=last_modified,
                    processed_at=processed_at,
                    document_id=document_id
                )
                db.execute(stmt)
            else:
                # Insert new record
                stmt = insert(self.processed_files_table).values(
                    file_path=file_path,
                    file_hash=file_hash,
                    size=size,
                    last_modified=last_modified,
                    processed_at=processed_at,
                    document_id=document_id
                )
                db.execute(stmt)
                
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error marking file as processed: {str(e)}")
        except Exception as e:
            logger.error(f"Error marking file as processed: {str(e)}")
            
    def is_file_modified(self, file_path: str, processed_files: Dict[str, Dict]) -> bool:
        """Check if a file is new or modified"""
        if not os.path.exists(file_path):
            return False
            
        stat = os.stat(file_path)
        current_size = stat.st_size
        current_mtime = stat.st_mtime
        
        if file_path not in processed_files:
            return True
            
        if (current_size != processed_files[file_path]["size"] or 
            current_mtime > processed_files[file_path]["last_modified"]):
            current_hash = self.get_file_hash(file_path)
            if current_hash != processed_files[file_path]["file_hash"]:
                return True
                
        return False
        
    def scan_directory(self, db: Session) -> List[str]:
        """Scan the directory for new or modified files"""
        processed_files = self.get_processed_files(db)
        modified_files = []
        
        for bucket in self.buckets:
            bucket_dir = os.path.join(self.watch_dir, bucket)
            
            # Skip if bucket directory doesn't exist
            if not os.path.exists(bucket_dir):
                continue
                
            for root, dirs, files in os.walk(bucket_dir):
                # Skip processed directories
                if any(pd in root for pd in self.processed_dirs):
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    _, ext = os.path.splitext(file_path)
                    
                    # Skip system files and non-supported extensions
                    if file.startswith('.') or ext.lower() not in self.file_extensions:
                        continue
                        
                    if self.is_file_modified(file_path, processed_files):
                        modified_files.append(file_path)
                        
        return modified_files
        
    def process_file(self, file_path: str, db: Session) -> Optional[str]:
        """Process a single file using the document processor"""
        try:
            file_name = os.path.basename(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            
            if not mime_type:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.pdf':
                    mime_type = 'application/pdf'
                elif ext in ['.jpg', '.jpeg']:
                    mime_type = 'image/jpeg'
                elif ext == '.png':
                    mime_type = 'image/png'
                elif ext == '.docx':
                    mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                elif ext == '.xlsx':
                    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                elif ext == '.txt':
                    mime_type = 'text/plain'
                else:
                    mime_type = 'application/octet-stream'
            
            # Read file into memory
            with open(file_path, 'rb') as f:
                file_content = BytesIO(f.read())
            
            # Process the file
            logger.info(f"Processing file from storage directory: {file_path}")
            result = document_processor.process_file(
                file=file_content,
                filename=file_name,
                mime_type=mime_type,
                description=f"Auto-processed from storage: {file_path}",
                db=db
            )
            
            if result.get("status") == "success":
                logger.info(f"Successfully processed file: {file_path}, document ID: {result.get('id')}")
                return result.get("id")
            else:
                logger.warning(f"Failed to process file: {file_path}, error: {result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return None
            
    def run_watcher(self, interval: int = 60):
        """Run the file watcher process continuously"""
        logger.info(f"Starting file watcher for directory: {self.watch_dir}")
        
        # Resolve relative path to absolute path
        if not os.path.isabs(self.watch_dir):
            abs_watch_dir = os.path.abspath(self.watch_dir)
            logger.info(f"Resolved relative path to absolute: {abs_watch_dir}")
            self.watch_dir = abs_watch_dir
        
        # Ensure directory exists
        if not os.path.exists(self.watch_dir):
            logger.warning(f"Watch directory does not exist, creating: {self.watch_dir}")
            os.makedirs(self.watch_dir, exist_ok=True)
            for bucket in self.buckets:
                bucket_path = os.path.join(self.watch_dir, bucket)
                if not os.path.exists(bucket_path):
                    os.makedirs(bucket_path, exist_ok=True)
                    logger.info(f"Created bucket directory: {bucket_path}")
        
        while True:
            try:
                # Get database session
                db = next(get_db())
                
                # Scan for modified files
                modified_files = self.scan_directory(db)
                
                if modified_files:
                    logger.info(f"Found {len(modified_files)} new or modified files")
                    
                    for file_path in modified_files:
                        # Process the file
                        document_id = self.process_file(file_path, db)
                        
                        if document_id:
                            # Mark file as processed
                            stat = os.stat(file_path)
                            self.mark_as_processed(
                                file_path=file_path,
                                file_hash=self.get_file_hash(file_path),
                                size=stat.st_size,
                                last_modified=stat.st_mtime,
                                document_id=document_id,
                                db=db
                            )
                else:
                    logger.debug("No new or modified files found")
                    
                # Close the database session
                db.close()
                
            except Exception as e:
                logger.error(f"Error in file watcher: {str(e)}")
                
            # Sleep for the specified interval
            time.sleep(interval)

# Create singleton instance
file_watcher = FileWatcher()