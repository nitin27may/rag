#!/bin/bash
set -e

echo "Setting up RAG backend environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create directories
mkdir -p data/raw data/processed data/uploads app/static

# Sync dependencies using pyproject.toml (creates .venv and uv.lock)
echo "Syncing dependencies with uv (this is fast!)..."
uv sync

echo ""
echo "✅ Environment setup complete!"
echo ""
echo "To activate: source .venv/bin/activate"
echo "To run: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
