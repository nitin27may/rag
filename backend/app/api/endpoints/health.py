import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.services.vector_store import vector_store
from app.services.object_storage import object_storage
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    """
    Check the health of all system components
    """
    health_status = {
        "status": "ok",
        "services": {}
    }
    
    # Check database health
    try:
        # Use text() to explicitly declare SQL
        db.execute(text("SELECT 1")).scalar()
        health_status["services"]["database"] = {
            "status": "ok",
            "message": "Connected successfully"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status["services"]["database"] = {
            "status": "error",
            "message": str(e)
        }
        health_status["status"] = "error"
    
    # Check vector store health (PGVector)
    try:
        # Test connection by attempting to get a collection
        # This will verify both database connection and pgvector extension
        vector_store.get_collection("documents")
        health_status["services"]["vector_store"] = {
            "status": "ok",
            "message": "PGVector connected successfully"
        }
    except Exception as e:
        logger.error(f"Vector store health check failed: {str(e)}")
        health_status["services"]["vector_store"] = {
            "status": "error",
            "message": str(e)
        }
        health_status["status"] = "error"
    
    # Check object storage health
    try:
        object_storage._get_client()
        health_status["services"]["object_storage"] = {
            "status": "ok",
            "message": "Connected successfully"
        }
    except Exception as e:
        logger.error(f"Object storage health check failed: {str(e)}")
        health_status["services"]["object_storage"] = {
            "status": "error",
            "message": str(e)
        }
        health_status["status"] = "error"
    
    return health_status


@router.get("/config")
async def get_config():
    """
    Get non-sensitive configuration information
    """
    return {
        "project_name": settings.PROJECT_NAME,
        "api_version": settings.API_V1_STR,
        "supported_document_types": settings.SUPPORTED_DOCUMENT_TYPES,
        "supported_image_types": settings.SUPPORTED_IMAGE_TYPES,
        "max_upload_size": settings.MAX_UPLOAD_SIZE,
        "collections": settings.COLLECTIONS,
        "embedding_model": settings.EMBEDDING_MODEL,
        "openai_model": settings.OPENAI_MODEL,
        # Add provider information
        "llm_provider": settings.LLM_PROVIDER,
        "embedding_provider": settings.EMBEDDING_PROVIDER,
    }