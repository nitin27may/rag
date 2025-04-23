---
layout: default
title: Installation
nav_order: 3
permalink: /installation/
---

# Installation Guide
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This guide provides detailed installation instructions for setting up the Comprehensive RAG System in various environments.

## System Requirements

- **Processor**: 2+ CPU cores recommended
- **Memory**: Minimum 4GB RAM (8GB+ recommended for production)
- **Storage**: 10GB+ free disk space
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)

## Software Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm 9+
- PostgreSQL 13+ (optional, SQLite can be used for development)
- MinIO or S3-compatible storage (optional)
- Docker and Docker Compose (optional)

## Detailed Installation Steps

### Backend Installation

#### Windows Setup

1. Clone the repository:
   ```powershell
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. Create a virtual environment:
   ```powershell
   cd backend
   python -m venv rag_env
   .\rag_env\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   # Additional dependencies for WebSockets
   python -m pip install python-socketio[asyncio] aiohttp websockets
   ```

4. Create required directories:
   ```powershell
   python ensure_directories.py
   # Alternatively, create them manually:
   # mkdir -p data/uploads data/raw data/processed
   ```

5. Configure environment:
   ```powershell
   copy .env.example .env
   # Edit .env with your preferred text editor
   ```

6. Run the setup script (optional):
   ```powershell
   .\setup-env.bat
   ```

7. Start the backend server:
   ```powershell
   python run.py
   # Or use the batch file
   .\run.bat
   ```

#### macOS/Linux Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. Create a virtual environment:
   ```bash
   cd backend
   python -m venv rag_env
   source rag_env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # Additional dependencies for WebSockets
   python -m pip install python-socketio[asyncio] aiohttp websockets
   ```

4. Create required directories:
   ```bash
   python ensure_directories.py
   # Alternatively, create them manually:
   # mkdir -p data/uploads data/raw data/processed
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred text editor
   ```

6. Start the backend server:
   ```bash
   python run.py
   ```

### Frontend Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure the API URL:
   ```bash
   # Create .env.local file
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. For production build:
   ```bash
   npm run build
   npm start
   ```

## Docker Installation

1. Make sure Docker and Docker Compose are installed on your system.

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Build and start all services:
   ```bash
   docker-compose up -d
   ```

5. For rebuilding after changes:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

6. To stop all services:
   ```bash
   docker-compose down
   ```

## Environment Configuration

The `.env` file contains all configuration options. Key settings include:

- `DATABASE_URL`: Connection string for the database
- `CHROMA_HOST` and `CHROMA_PORT`: ChromaDB configuration
- `MINIO_URL`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`: Object storage configuration
- `OPENAI_API_KEY`: Your OpenAI API key for embeddings and generation
- `OPENAI_MODEL`: Model to use (default: gpt-4o)
- `EMBEDDING_MODEL`: Embedding model configuration

## Verifying the Installation

After installation, perform these checks to ensure everything is working:

1. Backend health check: Open `http://localhost:8000/api/v1/health`
2. API documentation: Open `http://localhost:8000/docs`
3. Frontend access: Open `http://localhost:3000`
4. WebSocket test: Open `http://localhost:8000/static/simple_websocket.html`

Your system is properly installed if all these endpoints are accessible.

## Next Steps

After installation, see the [User Guide](../user-guide/) to learn how to use the system.