import logging
from typing import Dict, List, Optional, Any, Union
import os

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        self.client = None
        self.collections = {}
        self.embeddings = self._get_embeddings()
    
    def _get_embeddings(self):
        """Initialize embedding model based on configuration"""
        # Check provider configuration
        if settings.EMBEDDING_PROVIDER == "azure":
            # Use Azure OpenAI embeddings if configured
            if all([settings.AZURE_OPENAI_API_KEY, settings.AZURE_OPENAI_ENDPOINT, settings.AZURE_EMBEDDING_DEPLOYMENT]):
                logger.info(f"Using Azure OpenAI embeddings with deployment: {settings.AZURE_EMBEDDING_DEPLOYMENT}")
                return AzureOpenAIEmbeddings(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    azure_deployment=settings.AZURE_EMBEDDING_DEPLOYMENT,
                    api_version=settings.AZURE_OPENAI_API_VERSION
                )
            else:
                logger.warning("Azure OpenAI embedding configuration incomplete. Falling back to alternatives.")
        
        # Use OpenAI embeddings if API key is available
        if settings.OPENAI_API_KEY:
            logger.info(f"Using OpenAI embeddings with model: {settings.EMBEDDING_MODEL}")
            return OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model=settings.EMBEDDING_MODEL
            )
            
        # Fallback to local HuggingFace embeddings if no API key is available
        logger.info(f"Using local HuggingFace embeddings: {settings.EMBEDDING_MODEL_FALLBACK}")
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_FALLBACK
        )
    
    def _get_chroma_client(self):
        """Get or create Chroma client with improved error handling"""
        if self.client is None:
            try:
                logger.info(f"Connecting to ChromaDB at {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")
                
                # Import here to avoid circular import issues
                from chromadb import HttpClient, Client
                from chromadb.config import Settings as ChromaSettings
                
                try:
                    # Try to connect with default tenant
                    self.client = HttpClient(
                        host=settings.CHROMA_HOST,
                        port=settings.CHROMA_PORT,
                        settings=ChromaSettings(
                            allow_reset=True,
                            anonymized_telemetry=False
                        )
                    )
                    
                    # Test the connection
                    self.client.heartbeat()
                    logger.info(f"Connected to ChromaDB successfully")
                    
                except Exception as e:
                    # If the error is about tenant not existing
                    if "tenant" in str(e).lower() and "exist" in str(e).lower():
                        logger.warning(f"Tenant issue detected: {str(e)}")
                        logger.info("Attempting to connect without tenant specifics")
                        
                        # Try with different parameters 
                        self.client = HttpClient(
                            host=settings.CHROMA_HOST,
                            port=settings.CHROMA_PORT,
                            settings=ChromaSettings(
                                allow_reset=True,
                                anonymized_telemetry=False,
                                tenant="default_tenant",  # Explicitly set tenant
                                skip_tenant_validation=True  # Skip validation
                            )
                        )
                    else:
                        # Re-raise if it's a different type of error
                        raise
                        
            except Exception as e:
                logger.error(f"Failed to connect to ChromaDB: {str(e)}")
                # Create a fallback local embedding client if remote fails
                logger.warning("Using fallback local embedding database")
                from chromadb import PersistentClient
                
                # Ensure persist directory exists
                os.makedirs(settings.PERSIST_DIRECTORY, exist_ok=True)
                
                self.client = PersistentClient(
                    path=settings.PERSIST_DIRECTORY
                )
        
        return self.client
    
    def get_collection(self, collection_name: str):
        """Get or create a collection in the vector store"""
        if collection_name not in self.collections:
            client = self._get_chroma_client()
            
            # Check if collection exists already
            existing_collections = client.list_collections()
            collection_exists = any(c.name == collection_name for c in existing_collections)
            
            if not collection_exists:
                logger.info(f"Creating new collection: {collection_name}")
                client.create_collection(name=collection_name)
            
            # Initialize LangChain Chroma wrapper with our collection
            self.collections[collection_name] = Chroma(
                client=client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
        
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
            logger.info(f"Adding {len(documents)} documents to collection '{collection_name}'")
            return collection.add_documents(documents, ids=ids)
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
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
            logger.info(f"Searching for '{query}' in collection '{collection_name}'")
            return collection.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
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
            logger.info(f"Searching for '{query}' with scores in collection '{collection_name}'")
            return collection.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
        except Exception as e:
            logger.error(f"Error searching vector store with scores: {str(e)}")
            raise
    
    def delete(
        self,
        ids: List[str],
        collection_name: str = "documents"
    ) -> None:
        """Delete documents from the vector store"""
        collection = self.get_collection(collection_name)
        
        try:
            logger.info(f"Deleting {len(ids)} documents from collection '{collection_name}'")
            collection.delete(ids=ids)
        except Exception as e:
            logger.error(f"Error deleting documents from vector store: {str(e)}")
            raise


# Singleton instance
vector_store = VectorStore()