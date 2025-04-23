# setup_env.py
import subprocess
import sys
import os
from pathlib import Path

def setup_environment():
    # Define paths
    venv_path = Path("rag_env")
    requirements_path = Path("requirements.txt")
    
    # Check if virtual environment exists
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "rag_env"])
    
    # Determine the pip path
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip"
    else:
        pip_path = venv_path / "bin" / "pip"
    
    # Install requirements
    if requirements_path.exists():
        print("Installing requirements...")
        subprocess.run([str(pip_path), "install", "-r", str(requirements_path)])
    
    # Create required directories
    directories = ["data/raw", "data/processed", "data/uploads", "app/static"]
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
    
    print("Environment setup complete!")

if __name__ == "__main__":
    setup_environment()