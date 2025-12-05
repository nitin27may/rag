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

- Python 3.11 or higher
- Node.js 18+ and npm 9+
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- PostgreSQL 13+ with pgvector extension
- MinIO or S3-compatible storage (optional)
- Docker and Docker Compose (recommended)

## Detailed Installation Steps

### Backend Installation

#### Windows Setup

1. Clone the repository:
   ```powershell
   git clone https://github.com/nitin27may/rag.git
   cd rag
   ```

2. Install uv package manager:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. Run the setup script:
   ```powershell
   cd backend
   .\setup-env.bat
   ```
   This creates a `.venv` environment and installs all dependencies using uv.

4. Configure environment:
   ```powershell
   copy .env.example .env
   # Edit .env with your preferred text editor
   ```

5. Start the backend server:
   ```powershell
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

#### macOS/Linux Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/nitin27may/rag.git
   cd rag
   ```

2. Install uv package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Run the setup script:
   ```bash
   cd backend
   ./setup-env.sh
   ```
   This creates a `.venv` environment and installs all dependencies using uv.

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred text editor
   ```

5. Start the backend server:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
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
   echo "NEXT_PUBLIC_API_URL=http://localhost:3000/api" > .env.local
   echo "BACKEND_URL=http://localhost:8080" >> .env.local
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

## Docker Installation (Recommended)

1. Make sure Docker and Docker Compose are installed on your system.

2. Clone the repository:
   ```bash
   git clone https://github.com/nitin27may/rag.git
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

### LLM Configuration (Azure OpenAI)
```env
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### LLM Configuration (OpenAI)
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-3-small
```

### Database & Storage
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ragdb
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

## Verifying the Installation

After installation, perform these checks to ensure everything is working:

1. Backend health check: Open `http://localhost:8080/api/v1/health`
2. API documentation: Open `http://localhost:8080/docs`
3. Frontend access: Open `http://localhost:3000`
4. MinIO Console: Open `http://localhost:9001`

Your system is properly installed if all these endpoints are accessible.

## Next Steps

After installation, see the [User Guide](../user-guide/) to learn how to use the system.