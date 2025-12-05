from fastapi import APIRouter
from app.api.endpoints import documents, query, health, structured_extraction
from app.api.endpoints import datasource as datasources

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(datasources.router, prefix="/datasources", tags=["datasources"])
api_router.include_router(structured_extraction.router, prefix="/extraction", tags=["extraction"])