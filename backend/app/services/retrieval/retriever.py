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
        top_k: int = 5,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            collection_names: Collections to search in
            filter_criteria: Optional filters
            top_k: Number of documents to retrieve
            db: Database session
            
        Returns:
            Dictionary with retrieved documents and context
        """
        start_time = time.time()
        
        # Set default collection names if not provided
        if not collection_names:
            collection_names = settings.COLLECTIONS

        # Store all retrieved documents
        all_documents = []
        all_scores = []
        
        # Search each collection
        for collection_name in collection_names:
            try:
                # Get documents with scores
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
            
            except Exception as e:
                logger.error(f"Error searching collection {collection_name}: {str(e)}")
        
        # Filter out irrelevant documents
        relevant_docs, filtered_docs = self._filter_relevant_documents(query, all_documents, all_scores)
        
        # Generate context from relevant documents
        context = self._generate_context(relevant_docs)
        
        # Log metrics
        retrieval_time = time.time() - start_time
        logger.info(f"Retrieved {len(relevant_docs)}/{len(all_documents)} documents in {retrieval_time:.2f}s")
        
        # If documents were filtered, log the info
        if filtered_docs > 0:
            logger.info(f"Filtered out {filtered_docs} documents deemed irrelevant to the query")
        
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
            
        # 1. Extract key terms from the query
        query_terms = set(self._extract_key_terms(query.lower()))
        if not query_terms:
            return documents, 0
        
        # 2. Define relevance threshold
        score_threshold = 0.5  # Higher value = more strict filtering
        
        # 3. Process each document
        relevant_docs = []
        filtered_count = 0
        
        for doc, score in zip(documents, scores):
            # Convert the score to a relevance score (higher is better)
            # This depends on the vector store's scoring system
            relevance_score = 1.0 - score  # For some stores like ChromaDB, lower score = more similar
            
            # Extract document content
            content = doc.page_content.lower()
            
            # Check for query terms in the content
            term_matches = sum(1 for term in query_terms if term in content)
            term_match_ratio = term_matches / len(query_terms) if query_terms else 0
            
            # Combined relevance score (adjust weights as needed)
            combined_score = (0.7 * relevance_score) + (0.3 * term_match_ratio)
            
            # Add document metadata about relevance for debugging
            doc.metadata["relevance_score"] = float(f"{combined_score:.4f}")
            doc.metadata["vector_similarity"] = float(f"{relevance_score:.4f}")
            doc.metadata["term_match_ratio"] = float(f"{term_match_ratio:.4f}")
            
            # Filter based on combined score
            if combined_score >= score_threshold:
                relevant_docs.append(doc)
            else:
                filtered_count += 1
        
        # Sort by relevance score (highest first)
        relevant_docs = sorted(
            relevant_docs, 
            key=lambda x: x.metadata.get("relevance_score", 0), 
            reverse=True
        )
        
        # Limit to top_k
        return relevant_docs[:settings.MAX_RETRIEVED_DOCUMENTS], filtered_count
    
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
        top_k: int = 5,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Hybrid search - combining vector search with keyword filtering
        
        Args:
            query: User query
            collection_names: Collections to search in
            filter_criteria: Optional filters
            top_k: Number of documents to retrieve
            db: Database session
            
        Returns:
            Dictionary with retrieved documents and metrics
        """
        # For now, we just use the vector search
        # In a more advanced implementation, this would combine vector search with keyword-based retrieval
        return self.retrieve_for_rag(query, collection_names, filter_criteria, top_k, db)


# Singleton instance
rag_retriever = RAGRetriever()