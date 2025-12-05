import logging
from typing import Dict, List, Optional, Any
import os
import ssl
import httpx

# Updated imports for PGVector
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain.schema import Document

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_httpx_client():
    """Create httpx client based on DISABLE_SSL_VERIFICATION env variable.
    
    When DISABLE_SSL_VERIFICATION=true, SSL verification is disabled.
    This is useful for corporate proxy environments with self-signed certificates.
    """
    if settings.DISABLE_SSL_VERIFICATION:
        logger.warning("SSL verification is disabled. This should only be used in development/corporate proxy environments.")
        return httpx.Client(verify=False)
    return httpx.Client()


def get_async_httpx_client():
    """Create async httpx client based on DISABLE_SSL_VERIFICATION env variable."""
    if settings.DISABLE_SSL_VERIFICATION:
        return httpx.AsyncClient(verify=False)
    return httpx.AsyncClient()


class VectorStore:
    """Vector store implementation using PostgreSQL with PGVector extension"""
    
    def __init__(self):
        self.collections = {}
        self.embeddings = self._get_embeddings()
        self.connection_string = self._get_connection_string()
    
    def _get_connection_string(self) -> str:
        """Get PostgreSQL connection string from settings"""
        if settings.DATABASE_URL:
            # Convert PostgresDsn to string
            return str(settings.DATABASE_URL)
        
        # Fallback: construct from individual components
        # Note: These should be provided via environment variables for security
        db_user = os.environ.get("DATABASE_USER")
        db_password = os.environ.get("DATABASE_PASSWORD")
        db_host = os.environ.get("DATABASE_HOST", "localhost")
        db_port = os.environ.get("DATABASE_PORT", "5432")
        db_name = os.environ.get("DATABASE_NAME")
        
        if not db_user or not db_password or not db_name:
            raise ValueError(
                "Database credentials not configured. Please set DATABASE_URL or "
                "DATABASE_USER, DATABASE_PASSWORD, and DATABASE_NAME environment variables."
            )
        
        return f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def _get_embeddings(self):
        """Initialize embedding model based on configuration"""
        # Check provider configuration
        if settings.EMBEDDING_PROVIDER == "azure":
            # Use Azure OpenAI embeddings if configured
            if all([settings.AZURE_OPENAI_API_KEY, settings.AZURE_OPENAI_ENDPOINT, settings.AZURE_EMBEDDING_DEPLOYMENT]):
                try:
                    logger.info(f"Using Azure OpenAI embeddings with deployment: {settings.AZURE_EMBEDDING_DEPLOYMENT}")
                    embeddings = AzureOpenAIEmbeddings(
                        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                        api_key=settings.AZURE_OPENAI_API_KEY,
                        azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT,
                        api_version=settings.AZURE_OPENAI_API_VERSION,
                        model=settings.AZURE_EMBEDDING_DEPLOYMENT,
                        http_client=get_httpx_client(),
                    )
                    # Test the embeddings with a simple string
                    test_embed = embeddings.embed_query("Test embedding")
                    logger.info(f"Azure OpenAI embeddings test successful. Vector dimensions: {len(test_embed)}")
                    return embeddings
                except Exception as e:
                    logger.error(f"Error initializing Azure OpenAI embeddings: {str(e)}")
                    raise RuntimeError(f"Failed to initialize Azure OpenAI embeddings: {str(e)}")
        
        # Use OpenAI embeddings if provider is set to 'openai'
        elif settings.EMBEDDING_PROVIDER == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not configured in the environment but EMBEDDING_PROVIDER is set to 'openai'")
            
            try:
                logger.info(f"Using OpenAI embeddings with model: {settings.EMBEDDING_MODEL}")
                # Use custom httpx client with SSL verification disabled for corporate proxy environments
                embeddings = OpenAIEmbeddings(
                    openai_api_key=settings.OPENAI_API_KEY,
                    model=settings.EMBEDDING_MODEL,
                    http_client=get_httpx_client(),
                )
                # Test the embeddings
                test_embed = embeddings.embed_query("Test embedding")
                logger.info(f"OpenAI embeddings test successful. Vector dimensions: {len(test_embed)}")
                return embeddings
            except Exception as e:
                logger.error(f"Error initializing OpenAI embeddings with model {settings.EMBEDDING_MODEL}: {str(e)}")
                raise RuntimeError(f"Failed to initialize OpenAI embeddings: {str(e)}")
        else:
            # Unknown provider
            raise ValueError(f"Unknown EMBEDDING_PROVIDER: {settings.EMBEDDING_PROVIDER}. Must be 'azure' or 'openai'.")
    
    def get_collection(self, collection_name: str) -> PGVector:
        """Get or create a PGVector collection"""
        if collection_name not in self.collections:
            try:
                logger.info(f"Initializing PGVector collection: {collection_name}")
                
                # Create PGVector store - it will auto-create tables if they don't exist
                self.collections[collection_name] = PGVector(
                    connection=self.connection_string,
                    collection_name=collection_name,
                    embeddings=self.embeddings,
                    use_jsonb=True,
                )
                
                logger.info(f"PGVector collection '{collection_name}' initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize PGVector collection '{collection_name}': {str(e)}")
                raise
        
        return self.collections[collection_name]
    
    def add_documents(
        self, 
        documents: List[Document], 
        collection_name: str = "documents",
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """Add documents to the vector store"""
        collection = self.get_collection(collection_name)
        
        try:
            logger.info(f"Adding {len(documents)} documents to PGVector collection '{collection_name}'")
            return collection.add_documents(documents, ids=ids)
        except Exception as e:
            logger.error(f"Error adding documents to PGVector: {str(e)}")
            raise
    
    def search(
        self, 
        query: str,
        collection_name: str = "documents",
        filter: Optional[Dict[str, Any]] = None,
        k: int = 5
    ) -> List[Document]:
        """Search for documents similar to the query"""
        collection = self.get_collection(collection_name)
        
        try:
            logger.info(f"Searching for '{query}' in PGVector collection '{collection_name}'")
            return collection.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        except Exception as e:
            logger.error(f"Error searching PGVector: {str(e)}")
            raise
    
    def search_with_score(
        self, 
        query: str,
        collection_name: str = "documents",
        filter: Optional[Dict[str, Any]] = None,
        k: int = 5
    ) -> List[tuple[Document, float]]:
        """Search for documents similar to the query and return with similarity scores"""
        collection = self.get_collection(collection_name)
        
        try:
            logger.info(f"Searching for '{query}' with scores in PGVector collection '{collection_name}'")
            return collection.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
        except Exception as e:
            logger.error(f"Error searching PGVector with scores: {str(e)}")
            raise
    
    def delete(
        self,
        ids: List[str],
        collection_name: str = "documents"
    ) -> None:
        """Delete documents from the vector store"""
        collection = self.get_collection(collection_name)
        
        try:
            logger.info(f"Deleting {len(ids)} documents from PGVector collection '{collection_name}'")
            collection.delete(ids=ids)
        except Exception as e:
            logger.error(f"Error deleting documents from PGVector: {str(e)}")
            raise


# Singleton instance
vector_store = VectorStore()
