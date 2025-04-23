@echo off
mkdir backend\data\raw 2>nul
mkdir backend\data\processed 2>nul
mkdir backend\data\uploads 2>nul
mkdir backend\app\static 2>nul

call rag_env\Scripts\activate.bat
pip install -r requirements.txt