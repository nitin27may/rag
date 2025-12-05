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
    load_dotenv()


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
    DATABASE_URL: Optional[str] = None
    
    # Vector Database Settings (for pgvector)
    VECTOR_DB_TYPE: str = "pgvector"  # pgvector or chroma
    VECTOR_DIMENSIONS: int = 3072
    
    # Collections configuration
    COLLECTIONS: Dict[str, str] = {
        "documents": "documents",
        "images": "images",
        "web_pages": "web_pages"
    }
    
    # MinIO Object Storage
    MINIO_URL: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_DATA_DIR: str = os.environ.get("MINIO_DATA_DIR", "../storage/minio")
    
    # File Watcher Settings
    ENABLE_FILE_WATCHER: bool = os.environ.get("ENABLE_FILE_WATCHER", "true").lower() == "true"
    FILE_WATCHER_INTERVAL: int = int(os.environ.get("FILE_WATCHER_INTERVAL", "60"))
    
    # LLM Provider Settings
    LLM_PROVIDER: Literal["openai", "azure"] = "openai"
    
    # OpenAI Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = ""
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    
    # Embedding Settings
    EMBEDDING_PROVIDER: Literal["openai", "azure"] = "openai"
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    AZURE_EMBEDDING_DEPLOYMENT: str = ""
    EMBEDDING_MODEL_DIMENSIONS: int = 3072
    
    # SSL Configuration (for corporate proxy environments)
    DISABLE_SSL_VERIFICATION: bool = os.environ.get("DISABLE_SSL_VERIFICATION", "false").lower() == "true"
    
    # Document Processing / Chunking Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    CHUNKING_STRATEGY: Literal["recursive", "semantic", "token", "sentence"] = "recursive"
    # Separators for recursive chunking (used when CHUNKING_STRATEGY is "recursive")
    CHUNK_SEPARATORS: List[str] = ["\n\n", "\n", ". ", " ", ""]
    # For semantic chunking - breakpoint threshold type
    SEMANTIC_BREAKPOINT_TYPE: Literal["percentile", "standard_deviation", "interquartile", "gradient"] = "percentile"
    # Minimum chunk size (prevents very small chunks)
    MIN_CHUNK_SIZE: int = 100
    
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