import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import QueryRequest, QueryResponse
from app.services.retrieval.retriever import rag_retriever
from app.services.retrieval.generator import rag_generator
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/retrieve", response_model=dict)
async def retrieve_documents(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Retrieve relevant documents for a query without generating an answer
    """
    try:
        # If collection_names is None, use all collections
        collection_names = request.collection_names or settings.COLLECTIONS
        
        # Retrieve documents
        result = rag_retriever.hybrid_search(
            query=request.query,
            collection_names=collection_names,
            filter_criteria=request.filter_criteria,
            top_k=request.top_k or settings.MAX_RETRIEVED_DOCUMENTS,
            db=db
        )
        
        # Format the response
        document_results = []
        for doc in result.get("documents", []):
            document_results.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "query": request.query,
            "documents": document_results,
            "metrics": result.get("metrics", {})
        }
    
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


@router.post("/generate", response_model=QueryResponse)
async def generate_answer(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an answer using RAG
    """
    try:
        # If collection_names is None, use all collections
        collection_names = request.collection_names or settings.COLLECTIONS
        
        # Generate response
        result = rag_generator.generate_response(
            query=request.query,
            collection_names=collection_names,
            filter_criteria=request.filter_criteria,
            db=db
        )
        
        # Format the response
        document_results = []
        for doc in result.get("documents", []):
            document_results.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "query": request.query,
            "answer": result.get("answer", ""),
            "context": result.get("context", ""),
            "documents": document_results,
            "metrics": result.get("metrics", {})
        }
    
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer: {str(e)}"
        )