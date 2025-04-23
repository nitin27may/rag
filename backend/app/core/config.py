import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Literal

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
env_path = Path(__file__).parents[3] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))
else:
    load_dotenv()  # Try to load from backend/.env


class Settings(BaseSettings):
    APP_ENV: str = "development"
    LOG_LEVEL: str = "debug"
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    SECRET_KEY: str = "yoursecretkey"
    PROJECT_NAME: str = "RAG API"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database Settings
    DATABASE_URL: Optional[PostgresDsn] = None
    
    # Vector Database Settings
    VECTOR_DB_PATH: str = "./chroma_db"
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    USE_CHROMA_SERVER: bool = True
    PERSIST_DIRECTORY: str = "./chroma_db"  # Added this for compatibility
    
    # Collections configuration
    COLLECTIONS: Dict[str, str] = {
        "documents": "documents_collection",
        "images": "images_collection"
    }
    
    # MinIO Object Storage
    MINIO_URL: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_DATA_DIR: str = os.environ.get("MINIO_DATA_DIR", "../storage/minio")  # Path to MinIO data directory
    
    # File Watcher Settings
    ENABLE_FILE_WATCHER: bool = os.environ.get("ENABLE_FILE_WATCHER", "true").lower() == "true"
    FILE_WATCHER_INTERVAL: int = int(os.environ.get("FILE_WATCHER_INTERVAL", "60"))  # Seconds
    
    # LLM Provider Settings
    LLM_PROVIDER: Literal["openai", "azure"] = os.environ.get("LLM_PROVIDER", "openai")
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o")
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str = os.environ.get("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    AZURE_OPENAI_API_VERSION: str = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
    
    # Embedding Settings
    EMBEDDING_PROVIDER: Literal["openai", "azure"] = os.environ.get("EMBEDDING_PROVIDER")
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # Updated to latest OpenAI embedding model
    AZURE_EMBEDDING_DEPLOYMENT: str = os.environ.get("AZURE_EMBEDDING_DEPLOYMENT", "")
    EMBEDDING_MODEL_DIMENSIONS: int =  os.environ.get("EMBEDDING_MODEL_DIMENSIONS", "")
    EMBEDDING_MODEL_FALLBACK: str = "sentence-transformers/all-MiniLM-L6-v2"  # Fallback model
    
    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Retrieval Settings
    MAX_RETRIEVED_DOCUMENTS: int = 5
    
    # File Upload Settings
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Supported file types
    SUPPORTED_DOCUMENT_TYPES: List[str] = [
        "pdf", "docx", "doc", "txt", "md", "pptx", "csv", "xlsx"
    ]
    SUPPORTED_IMAGE_TYPES: List[str] = [
        "jpg", "jpeg", "png", "gif", "bmp", "webp"
    ]
    
    # Web Scraping
    SCRAPING_TIMEOUT: int = 30
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"
    )


settings = Settings()