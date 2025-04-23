"""
Entry point for Uvicorn when run directly from the backend directory.
This file simply imports and exposes the FastAPI app from the actual module.
"""
import os
import sys
import threading
from pathlib import Path

# Add the current directory to Python path to ensure all modules are accessible
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the actual app
from app.main import app

# This allows running with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    reload = os.getenv("APP_ENV", "development").lower() == "development"
    
    print(f"Starting server at http://{host}:{port}")
    print(f"Application path: {current_dir}")
    
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=reload,
        reload_dirs=[str(current_dir / "app")]
    )
