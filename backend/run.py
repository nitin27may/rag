#!/usr/bin/env python
"""
Run script for the RAG API server.
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import uvicorn
import uvicorn

if __name__ == "__main__":
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    reload = os.getenv("APP_ENV", "development").lower() == "development"
    
    print(f"Starting server at http://{host}:{port}")
    print(f"Application path: {current_dir}")
    
    # Run the app with explicit module path
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=[str(current_dir / "app")],
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )