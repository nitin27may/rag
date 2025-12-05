@echo off
echo Setting up RAG backend environment with uv...

:: Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo uv not found. Installing uv...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
)

:: Create directories
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir data\uploads 2>nul
mkdir app\static 2>nul

:: Sync dependencies using pyproject.toml (creates .venv and uv.lock)
echo Syncing dependencies with uv...
uv sync

echo.
echo Environment setup complete!
echo To activate: .venv\Scripts\activate
echo To run: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080