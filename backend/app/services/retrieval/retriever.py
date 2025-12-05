import logging
import time
from typing import List, Dict, Any, Optional
import re

from langchain.schema import Document
from sqlalchemy.orm import Session

from app.services.vector_store import vector_store
from app.models.document import QueryLog
from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGRetriever:
    """Service to retrieve relevant documents for RAG"""
    
    def __init__(self):
        self.vector_store = vector_store
    
    def retrieve_for_rag(
        self, 
        query: str,
        collection_names: Optional[List[str]] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
        document_id: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            collection_names: Collections to search in
            filter_criteria: Optional filters
            document_id: Optional specific document ID to filter by (single)
            document_ids: Optional list of document IDs to filter by (multiple)
            top_k: Number of documents to retrieve
            db: Database session
            
        Returns:
            Dictionary with retrieved documents and context
        """
        start_time = time.time()
        
        # Set default collection names if not provided
        if not collection_names:
            # Default to using only the documents collection
            if isinstance(settings.COLLECTIONS, dict) and "documents" in settings.COLLECTIONS:
                collection_names = [settings.COLLECTIONS["documents"]]
            else:
                # Get collection names from settings (handling both list and dict formats)
                if isinstance(settings.COLLECTIONS, dict):
                    collection_names = list(settings.COLLECTIONS.values())
                else:
                    collection_names = settings.COLLECTIONS
                
        logger.info(f"Searching in collections: {collection_names}")
        
        # Handle document filtering - support both single and multiple document IDs
        if not filter_criteria:
            filter_criteria = {}
            
        # If document_ids (multiple) is provided, use $in operator
        if document_ids and len(document_ids) > 0:
            logger.info(f"Filtering by document IDs: {document_ids}")
            filter_criteria["document_id"] = {"$in": document_ids}
        # If only single document_id is provided, use it directly
        elif document_id:
            logger.info(f"Filtering by document ID: {document_id}")
            filter_criteria["document_id"] = document_id

        # Store all retrieved documents
        all_documents = []
        all_scores = []
        
        # Search each collection
        for collection_name in collection_names:
            try:
                # Get documents with scores
                logger.info(f"Searching collection '{collection_name}' for query: '{query}'")
                docs_with_scores = vector_store.search_with_score(
                    query=query,
                    collection_name=collection_name,
                    filter=filter_criteria,
                    k=top_k
                )
                
                if docs_with_scores:
                    # Add documents and their relevance scores
                    for doc, score in docs_with_scores:
                        all_documents.append(doc)
                        all_scores.append(score)
                        logger.debug(f"Found document with score {score}: {doc.page_content[:50]}...")
                    logger.info(f"Found {len(docs_with_scores)} documents in collection '{collection_name}'")
                else:
                    logger.info(f"No documents found in collection '{collection_name}'")
            
            except Exception as e:
                logger.error(f"Error searching collection {collection_name}: {str(e)}")
                import traceback
                logger.error(f"Search error traceback: {traceback.format_exc()}")
        
        # Skip filtering entirely - just return all found documents
        # This ensures we'll always have documents to work with
        relevant_docs = all_documents
        filtered_docs = 0
        
        # If we have too many documents, take only the top ones based on vector similarity
        if len(relevant_docs) > settings.MAX_RETRIEVED_DOCUMENTS:
            # Sort by vector similarity score (lower is better in most embeddings)
            paired_docs = sorted(zip(relevant_docs, all_scores), key=lambda pair: pair[1])
            # Take only the top MAX_RETRIEVED_DOCUMENTS
            relevant_docs = [doc for doc, _ in paired_docs[:settings.MAX_RETRIEVED_DOCUMENTS]]
            filtered_docs = len(all_documents) - len(relevant_docs)
        
        # Generate context from relevant documents
        context = self._generate_context(relevant_docs)
        
        # Log metrics
        retrieval_time = time.time() - start_time
        logger.info(f"Retrieved {len(relevant_docs)}/{len(all_documents)} documents in {retrieval_time:.2f}s")
        
        # If documents were filtered, log the info
        if filtered_docs > 0:
            logger.info(f"Limited to top {len(relevant_docs)} documents out of {len(all_documents)}")
            
        # If no documents were found, log a warning
        if len(relevant_docs) == 0:
            logger.warning(f"No documents found for query: '{query}'")
        
        return {
            "documents": relevant_docs,
            "context": context,
            "metrics": {
                "retrieval_time_seconds": retrieval_time,
                "total_documents": len(relevant_docs),
                "filtered_documents": filtered_docs
            }
        }
    
    def _filter_relevant_documents(self, query: str, documents: List[Document], scores: List[float]) -> tuple[List[Document], int]:
        """
        Filter documents based on relevance to the query
        
        Args:
            query: The original query
            documents: List of retrieved documents
            scores: Corresponding relevance scores
            
        Returns:
            Tuple of (filtered_documents, num_filtered)
        """
        if not documents:
            return [], 0
            
        # Simply return all documents - no filtering
        # We're disabling filtering to ensure results are returned
        return documents, 0
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text, filtering out common words"""
        # Very basic stopwords list - expand as needed
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'if', 'of', 'at', 'by', 'for', 
                    'with', 'about', 'to', 'from', 'in', 'on', 'is', 'was', 'were', 'be',
                    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'what',
                    'where', 'when', 'who', 'how', 'why', 'which', 'me', 'you', 'he', 'she',
                    'it', 'we', 'they', 'this', 'that', 'these', 'those', 'i', 'am', 'are'}
        
        # Clean and tokenize
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        words = [word for word in text.split() if word.lower() not in stopwords and len(word) > 2]
        
        return words
    
    def _generate_context(self, documents: List[Document]) -> str:
        """
        Generate context text from documents
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Context text for RAG
        """
        context = ""
        
        # Check if there are documents to process
        if not documents:
            return context
        
        # Group documents by source for better readability
        source_to_docs = {}
        for doc in documents:
            # Determine source key
            source_key = self._get_source_identifier(doc)
            
            if source_key not in source_to_docs:
                source_to_docs[source_key] = []
                
            source_to_docs[source_key].append(doc)
        
        # Build context string with source blocks
        for source_key, docs in source_to_docs.items():
            # Sort documents by chunk index if available
            docs = sorted(docs, key=lambda x: x.metadata.get("chunk", 0))
            
            # Add source header
            context += f"[Source: {source_key}]\n"
            
            # Add document contents
            for doc in docs:
                context += doc.page_content + "\n\n"
        
        return context.strip()
    
    def _get_source_identifier(self, doc: Document) -> str:
        """Get a clean source identifier from a document"""
        if hasattr(doc, 'metadata'):
            metadata = doc.metadata
            # Try common identifier fields (filename, url, title, etc.)
            if "filename" in metadata:
                return metadata["filename"]
            elif "url" in metadata:
                # Clean up URL to look nicer
                return metadata["url"].split("?")[0].rstrip("/")
            elif "title" in metadata:
                return metadata["title"]
            elif "source" in metadata:
                return metadata["source"]
            
            # If no good identifier, generate one
            return f"Document {metadata.get('id', 'unknown')}"
        
        return "Unknown Source"

    def hybrid_search(
        self, 
        query: str,
        collection_names: Optional[List[str]] = None,
        filter_criteria: Optional[Dict[str, Any]] = None,
        document_id: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
        top_k: int = 5,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Hybrid search - combining vector search with keyword filtering
        
        Args:
            query: User query
            collection_names: Collections to search in
            filter_criteria: Optional filters
            document_id: Optional specific document ID to filter by (single)
            document_ids: Optional list of document IDs to filter by (multiple)
            top_k: Number of documents to retrieve
            db: Database session
            
        Returns:
            Dictionary with retrieved documents and metrics
        """
        # For now, we just use the vector search
        # In a more advanced implementation, this would combine vector search with keyword-based retrieval
        return self.retrieve_for_rag(query, collection_names, filter_criteria, document_id, document_ids, top_k, db)


# Singleton instance
rag_retriever = RAGRetriever()