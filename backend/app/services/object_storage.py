import logging
import os
from typing import BinaryIO, Optional, Dict, List
from io import BytesIO
from minio import Minio
from minio.error import S3Error

from app.core.config import settings

logger = logging.getLogger(__name__)


class ObjectStorage:
    def __init__(self):
        self.client = None
        self.buckets = ["documents", "images", "raw", "processed"]
    
    def _get_client(self) -> Minio:
        """Get or create Minio client"""
        if self.client is None:
            try:
                logger.info(f"Connecting to MinIO at {settings.MINIO_URL}")
                self.client = Minio(
                    settings.MINIO_URL,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=settings.MINIO_SECURE
                )
                logger.info("Connected to MinIO successfully")
                
                # Ensure all required buckets exist
                self._ensure_buckets_exist()
            
            except Exception as e:
                logger.error(f"Failed to connect to MinIO: {str(e)}")
                raise
        
        return self.client
    
    def _ensure_buckets_exist(self):
        """Create buckets if they don't exist"""
        client = self._get_client()
        
        for bucket in self.buckets:
            try:
                if not client.bucket_exists(bucket):
                    logger.info(f"Creating bucket: {bucket}")
                    client.make_bucket(bucket)
                    logger.info(f"Bucket created: {bucket}")
            except S3Error as e:
                logger.error(f"Error creating bucket {bucket}: {str(e)}")
                raise
    
    def upload_file(
        self, 
        file_data: BinaryIO, 
        object_name: str, 
        bucket_name: str = "documents",
        content_type: Optional[str] = None
    ) -> str:
        """
        Upload a file to object storage
        
        Args:
            file_data: File-like object containing the file data
            object_name: Name to store the object as
            bucket_name: Bucket to store the object in
            content_type: MIME type of the file
            
        Returns:
            The object path in the format 'bucket/object_name'
        """
        client = self._get_client()
        
        try:
            # Get file size
            file_data.seek(0, os.SEEK_END)
            file_size = file_data.tell()
            file_data.seek(0)
            
            logger.info(f"Uploading file {object_name} to {bucket_name} bucket")
            client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_data,
                length=file_size,
                content_type=content_type
            )
            
            logger.info(f"File uploaded successfully: {object_name}")
            return f"{bucket_name}/{object_name}"
        
        except S3Error as e:
            logger.error(f"Error uploading file to MinIO: {str(e)}")
            raise
    
    def download_file(
        self, 
        object_name: str, 
        bucket_name: str = "documents"
    ) -> BytesIO:
        """
        Download a file from object storage
        
        Args:
            object_name: Name of the object to download
            bucket_name: Bucket the object is stored in
            
        Returns:
            BytesIO object containing the file data
        """
        client = self._get_client()
        
        try:
            logger.info(f"Downloading file {object_name} from {bucket_name} bucket")
            response = client.get_object(
                bucket_name=bucket_name,
                object_name=object_name
            )
            
            # Read the data into a BytesIO object
            data = BytesIO()
            for d in response.stream(32*1024):
                data.write(d)
            data.seek(0)
            
            # Close the response to release resources
            response.close()
            response.release_conn()
            
            return data
        
        except S3Error as e:
            logger.error(f"Error downloading file from MinIO: {str(e)}")
            raise
    
    def delete_file(
        self, 
        object_name: str, 
        bucket_name: str = "documents"
    ) -> bool:
        """
        Delete a file from object storage
        
        Args:
            object_name: Name of the object to delete
            bucket_name: Bucket the object is stored in
            
        Returns:
            True if the file was deleted successfully
        """
        client = self._get_client()
        
        try:
            logger.info(f"Deleting file {object_name} from {bucket_name} bucket")
            client.remove_object(
                bucket_name=bucket_name,
                object_name=object_name
            )
            return True
        
        except S3Error as e:
            logger.error(f"Error deleting file from MinIO: {str(e)}")
            raise
    
    def get_file_info(
        self, 
        object_name: str, 
        bucket_name: str = "documents"
    ) -> Dict:
        """
        Get metadata for a file
        
        Args:
            object_name: Name of the object
            bucket_name: Bucket the object is stored in
            
        Returns:
            Dictionary containing file metadata
        """
        client = self._get_client()
        
        try:
            logger.info(f"Getting info for file {object_name} from {bucket_name} bucket")
            stat = client.stat_object(
                bucket_name=bucket_name,
                object_name=object_name
            )
            
            return {
                "size": stat.size,
                "last_modified": stat.last_modified,
                "content_type": stat.content_type,
                "etag": stat.etag,
                "metadata": stat.metadata
            }
        
        except S3Error as e:
            logger.error(f"Error getting file info from MinIO: {str(e)}")
            raise
    
    def list_files(
        self, 
        prefix: str = "", 
        bucket_name: str = "documents"
    ) -> List[Dict]:
        """
        List files in a bucket
        
        Args:
            prefix: Prefix to filter objects by
            bucket_name: Bucket to list objects from
            
        Returns:
            List of dictionaries containing file metadata
        """
        client = self._get_client()
        
        try:
            logger.info(f"Listing files with prefix '{prefix}' in {bucket_name} bucket")
            objects = client.list_objects(
                bucket_name=bucket_name,
                prefix=prefix,
                recursive=True
            )
            
            return [
                {
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified
                }
                for obj in objects
            ]
        
        except S3Error as e:
            logger.error(f"Error listing files from MinIO: {str(e)}")
            raise


# Singleton instance
object_storage = ObjectStorage()