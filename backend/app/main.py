import logging
import os
import sys
import threading
import traceback
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import uvicorn

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging with more detailed information for WebSockets
logging.basicConfig(
    level=logging.DEBUG if os.getenv("LOG_LEVEL", "").lower() == "debug" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("app.main")

# Get the absolute path to the static directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

# Check if static directory exists and create it if not
if not os.path.exists(STATIC_DIR):
    logger.warning(f"Static directory not found at {STATIC_DIR}, creating it now")
    try:
        os.makedirs(STATIC_DIR, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create static directory: {str(e)}")

from app.api.api import api_router
from app.core.config import settings
from app.db.session import get_db
from app.db.init_db import init_db, init_default_datasources

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # For development, allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Simple direct WebSocket endpoint that works without Socket.IO
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("Connected to RAG API via WebSocket")
        while True:
            data = await websocket.receive_text()
            logger.info(f"WebSocket message received: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files using absolute path
logger.info(f"Mounting static files from: {STATIC_DIR}")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    logger.error(f"Static directory still does not exist at {STATIC_DIR}")

# Redirect root to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Add root health check for Kubernetes/load balancers
@app.get("/health", include_in_schema=False)
async def root_health():
    return {"status": "ok"}

# Global reference to the file watcher thread
file_watcher_thread = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize resources on startup
    """
    logger.info("Starting up application...")
    
    # Initialize database
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
    
    # Initialize default data sources
    try:
        logger.info("Initializing default data sources...")
        init_default_datasources()
        logger.info("Default data sources initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing default data sources: {str(e)}")

    # Ensure uploads directory exists
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        logger.info(f"Created uploads directory at {settings.UPLOAD_DIR}")
    except Exception as e:
        logger.error(f"Error creating uploads directory: {str(e)}")
    
    # Start file watcher if enabled
    if settings.ENABLE_FILE_WATCHER:
        start_file_watcher()

def start_file_watcher():
    """Start the file watcher in a separate thread"""
    global file_watcher_thread
    
    try:
        # Re-import the file_watcher to ensure it's using the correct database connection
        import importlib
        from app.services import file_watcher as fw_module
        importlib.reload(fw_module)
        from app.services.file_watcher import file_watcher
        
        # Ensure the file watcher's database table is correctly initialized
        file_watcher.init_db()
        
        # Ensure the MinIO data directory exists
        minio_dir = os.path.abspath(settings.MINIO_DATA_DIR)
        if not os.path.exists(minio_dir):
            logger.warning(f"MinIO data directory not found at {minio_dir}, creating it now")
            os.makedirs(minio_dir, exist_ok=True)
            for bucket in ["documents", "images", "raw"]:
                os.makedirs(os.path.join(minio_dir, bucket), exist_ok=True)
        
        # Check if file watcher is already running
        if file_watcher_thread and file_watcher_thread.is_alive():
            logger.info("File watcher is already running")
            return
            
        logger.info(f"Starting file watcher for directory: {minio_dir}")
        file_watcher_thread = threading.Thread(
            target=file_watcher.run_watcher,
            args=(settings.FILE_WATCHER_INTERVAL,),
            daemon=True,
            name="FileWatcherThread"
        )
        file_watcher_thread.start()
        logger.info("File watcher started successfully")
        
    except Exception as e:
        logger.error(f"Error starting file watcher: {str(e)}")
        logger.error(f"File watcher stacktrace: {traceback.format_exc()}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up resources on shutdown
    """
    logger.info("Shutting down application...")
    
    # File watcher thread will automatically terminate as it's a daemon thread

if __name__ == "__main__":
    # Run the application with Uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )