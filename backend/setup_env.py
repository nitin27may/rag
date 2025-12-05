# setup_env.py
import subprocess
import sys
import os
from pathlib import Path
import shutil

def check_uv_installed():
    """Check if uv is installed"""
    return shutil.which("uv") is not None

def setup_environment():
    """Setup Python environment using uv sync"""
    pyproject_path = Path("pyproject.toml")
    
    # Check/install uv
    if not check_uv_installed():
        print("uv not found. Please install it first:")
        print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("  or: brew install uv")
        sys.exit(1)
    
    # Check for pyproject.toml
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found!")
        sys.exit(1)
    
    # Sync dependencies with uv (creates .venv and uv.lock automatically)
    print("Syncing dependencies with uv (this is fast!)...")
    subprocess.run(["uv", "sync"], check=True)
    
    # Create required directories
    directories = ["data/raw", "data/processed", "data/uploads", "app/static"]
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    print("\n✅ Environment setup complete!")
    print("\nTo activate the environment:")
    if sys.platform == "win32":
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")
    print("\nTo run the server:")
    print("  uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080")

if __name__ == "__main__":
    setup_environment()