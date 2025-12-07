# Comprehensive RAG System

A production-ready Retrieval-Augmented Generation (RAG) system that enables intelligent document querying and information extraction using Large Language Models (LLMs). Built with modern technologies for scalability and ease of use.

## 📑 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start with Docker](#-quick-start-with-docker)
- [Local Development Setup](#-local-development-setup)
- [Configuration Guide](#-configuration-guide)
- [Usage Examples](#-usage-examples)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

- **📄 Document Ingestion**: Process multiple file formats (PDF, DOCX, TXT, CSV, XLSX, JSON, images), web pages, and database content
- **🔍 Vector Search**: Semantic similarity search powered by PostgreSQL with PGVector extension
- **🎯 Multi-Document Selection**: Query specific documents or search across all indexed content
- **🗄️ Database Connector**: Direct integration with PostgreSQL, MySQL, and SQLite databases
- **⚡ Hybrid Retrieval**: Combines vector search with keyword filtering for enhanced accuracy
- **💬 Question-Answering**: AI-powered responses based on document context
- **📊 Structured Extraction**: Extract specific data using customizable schemas
- **🎨 Modern Web Interface**: Next.js 15 with React 19 for seamless user experience
- **🔌 RESTful API**: Comprehensive API for system integration
- **📡 WebSocket Support**: Real-time streaming responses
- **💚 Health Monitoring**: Built-in health checks for all components

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[<span style='color:#4F46E5'>Web Browser</span>]
        B[<span style='color:#4F46E5'>API Client</span>]
    end
    
    subgraph "Frontend Layer"
        C[<span style='color:#10B981'>Next.js 15 Frontend<br/>React 19 + TypeScript<br/>Tailwind CSS</span>]
    end
    
    subgraph "API Layer"
        D[<span style='color:#F59E0B'>FastAPI Backend<br/>Python 3.11+</span>]
        E[<span style='color:#F59E0B'>REST Endpoints</span>]
        F[<span style='color:#F59E0B'>WebSocket Server</span>]
    end
    
    subgraph "Service Layer"
        G[<span style='color:#8B5CF6'>Document Processor</span>]
        H[<span style='color:#8B5CF6'>Vector Store Service</span>]
        I[<span style='color:#8B5CF6'>RAG Retriever</span>]
        J[<span style='color:#8B5CF6'>LLM Generator</span>]
        K[<span style='color:#8B5CF6'>Chunking Service</span>]
    end
    
    subgraph "Parser Layer"
        L[<span style='color:#EC4899'>PDF Parser</span>]
        M[<span style='color:#EC4899'>DOCX Parser</span>]
        N[<span style='color:#EC4899'>Image Parser<br/>OCR</span>]
        O[<span style='color:#EC4899'>Web Scraper</span>]
        P[<span style='color:#EC4899'>DB Connector</span>]
    end
    
    subgraph "External Services"
        Q[<span style='color:#06B6D4'>Azure OpenAI /<br/>OpenAI GPT-4</span>]
        R[<span style='color:#06B6D4'>Embedding Model<br/>text-embedding-3-large</span>]
    end
    
    subgraph "Data Layer"
        S[(PostgreSQL<br/>+ PGVector<br/>Vector DB)]
        T[(<span style='color:#14B8A6'>MinIO<br/>S3 Storage</span>)]
    end
    
    A --> C
    B --> D
    C --> D
    D --> E
    D --> F
    E --> G
    E --> I
    G --> K
    K --> L
    K --> M
    K --> N
    G --> O
    G --> P
    G --> H
    H --> S
    G --> T
    I --> H
    I --> J
    J --> Q
    H --> R
    
    style A fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px
    style B fill:#EEF2FF,stroke:#4F46E5,stroke-width:2px
    style C fill:#D1FAE5,stroke:#10B981,stroke-width:3px
    style D fill:#FEF3C7,stroke:#F59E0B,stroke-width:3px
    style E fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px
    style F fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px
    style G fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2px
    style H fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2px
    style I fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2px
    style J fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2px
    style K fill:#EDE9FE,stroke:#8B5CF6,stroke-width:2px
    style L fill:#FCE7F3,stroke:#EC4899,stroke-width:2px
    style M fill:#FCE7F3,stroke:#EC4899,stroke-width:2px
    style N fill:#FCE7F3,stroke:#EC4899,stroke-width:2px
    style O fill:#FCE7F3,stroke:#EC4899,stroke-width:2px
    style P fill:#FCE7F3,stroke:#EC4899,stroke-width:2px
    style Q fill:#CFFAFE,stroke:#06B6D4,stroke-width:2px
    style R fill:#CFFAFE,stroke:#06B6D4,stroke-width:2px
    style S fill:#F0FDFA,stroke:#14B8A6,stroke-width:3px
    style T fill:#F0FDFA,stroke:#14B8A6,stroke-width:3px
```

### Architecture Components

| Layer | Component | Description |
|-------|-----------|-------------|
| **Client** | Web Browser / API Client | User interfaces for interacting with the system |
| **Frontend** | Next.js 15 + React 19 | Modern web interface with TypeScript and Tailwind CSS |
| **API** | FastAPI Backend | Python-based REST and WebSocket API server |
| **Services** | Document Processing | Handles file parsing, chunking, and vector embedding |
| **Services** | RAG Pipeline | Retrieval and generation using LLMs |
| **Parsers** | Multi-Format Support | PDF, DOCX, images (OCR), web scraping, database queries |
| **External** | LLM Providers | Azure OpenAI or OpenAI for embeddings and generation |
| **Data** | PostgreSQL + PGVector | Vector database for semantic search |
| **Storage** | MinIO | S3-compatible object storage for files |

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.11+, FastAPI 0.115+, SQLAlchemy 2.x |
| **Vector Store** | PostgreSQL 17 with pgvector extension |
| **LLM/Embeddings** | Azure OpenAI or OpenAI (GPT-4, text-embedding-3-large) |
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS |
| **Object Storage** | MinIO (S3-compatible) |
| **Package Manager** | uv (10-100x faster than pip) |
| **Containerization** | Docker & Docker Compose |

## 🚀 Quick Start with Docker

The fastest way to get the RAG system running is using Docker Compose. This method automatically sets up all required services (PostgreSQL, MinIO, Backend, Frontend).

### Step 1: Clone the Repository

```bash
git clone https://github.com/nitin27may/rag.git
cd rag
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your preferred text editor
nano .env  # or vim, code, etc.
```

**Required Configuration:**

For **OpenAI**:
```env
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-large
```

For **Azure OpenAI**:
```env
LLM_PROVIDER=azure
EMBEDDING_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-azure-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_API_VERSION=2024-08-06
```

### Step 3: Start All Services

```bash
# Build and start all containers in detached mode
docker compose up -d

# Check if all services are running
docker compose ps
```

You should see all services with status "Up" (healthy):
- `frontend-1` (or `rag-frontend-1` depending on directory name)
- `backend-1`
- `db-1`
- `minio-1`

### Step 4: Access the Application

Once all containers are healthy (may take 1-2 minutes):

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main web interface |
| **Backend API** | http://localhost:8080/docs | Interactive API documentation (Swagger) |
| **Backend ReDoc** | http://localhost:8080/redoc | Alternative API documentation |
| **MinIO Console** | http://localhost:9001 | Object storage admin interface |

**MinIO Login Credentials:** (from .env)
- Username: Value of `MINIO_ACCESS_KEY` (default: `minioadmin` from .env.example)
- Password: Value of `MINIO_SECRET_KEY` (default: `minioadmin` from .env.example)

**Note:** If you don't set these in `.env`, Docker Compose will use fallback defaults: `ragadmin2024` / `ragadminsecret2024`

### Step 5: Verify Installation

Test the health endpoint:
```bash
curl http://localhost:8080/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "minio": "connected",
  "llm": "configured"
}
```

### Managing Docker Services

```bash
# View logs from all services
docker compose logs -f

# View logs from specific service
docker compose logs -f backend
docker compose logs -f frontend

# Stop all services
docker compose down

# Stop and remove all data (⚠️ Warning: deletes database and files)
docker compose down -v

# Restart a specific service
docker compose restart backend

# Rebuild after code changes
docker compose up -d --build
```

## 💻 Local Development Setup

For active development, you may want to run services locally for faster iteration and debugging.

### Prerequisites

Ensure you have the following installed:

| Software | Version | Installation |
|----------|---------|--------------|
| **Python** | 3.11 or higher | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18 or higher | [nodejs.org](https://nodejs.org/) |
| **Docker** | Latest | [docker.com](https://docs.docker.com/get-docker/) |
| **uv** | Latest | See installation below |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |

#### Installing uv (Python Package Manager)

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (with pip):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

### Backend Setup (Detailed)

#### Step 1: Start Required Infrastructure

Start PostgreSQL and MinIO using Docker:

```bash
# From the project root directory
docker compose up -d db minio

# Wait for services to be healthy (~30 seconds)
docker compose ps
```

#### Step 2: Navigate to Backend Directory

```bash
cd backend
```

#### Step 3: Set Up Python Environment

**Option A: Using setup scripts (Recommended)**

**macOS/Linux:**
```bash
chmod +x setup-env.sh
./setup-env.sh
```

**Windows:**
```cmd
setup-env.bat
```

**Option B: Manual setup**

```bash
# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Windows (CMD):
.\.venv\Scripts\activate.bat
```

#### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the .env file
nano .env
```

**Important environment variables for local development:**

```env
# Database (matches docker-compose)
DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb

# MinIO (when using docker compose up -d db minio)
MINIO_URL=localhost:9000
MINIO_ACCESS_KEY=minioadmin        # Use value from .env or docker-compose defaults
MINIO_SECRET_KEY=minioadmin        # Use value from .env or docker-compose defaults
MINIO_SECURE=False

# LLM Provider (OpenAI or Azure)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o

# Embedding Provider
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_MODEL_DIMENSIONS=3072

# Application Settings
LOG_LEVEL=debug
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
CHUNKING_STRATEGY=recursive
```

#### Step 5: Initialize Database

The database will be automatically initialized on first run. You can also run migrations manually:

```bash
# Database tables will be created automatically when you start the server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

#### Step 6: Run the Backend Server

```bash
# With uv (recommended)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Or with activated virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# For debug mode with detailed logs
LOG_LEVEL=debug uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The backend will be available at:
- API: http://localhost:8080
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

#### Step 7: Verify Backend

In a new terminal:
```bash
# Test health endpoint
curl http://localhost:8080/api/v1/health

# Or visit in browser
open http://localhost:8080/docs
```

### Frontend Setup (Detailed)

#### Step 1: Navigate to Frontend Directory

```bash
cd frontend  # from project root
```

#### Step 2: Install Dependencies

```bash
# Install all npm packages
npm install

# Verify installation
npm list --depth=0
```

#### Step 3: Configure Environment Variables

```bash
# Create local environment file
touch .env.local

# Add configuration
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:3000/api
BACKEND_URL=http://localhost:8080
EOF
```

Or manually create `.env.local`:

```env
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:3000/api
BACKEND_URL=http://localhost:8080
```

#### Step 4: Start Development Server

```bash
# Start Next.js development server with Turbopack
npm run dev

# The server will start on http://localhost:3000
```

You should see output similar to:
```
  ▲ Next.js 15.2.4
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.3s
```

#### Step 5: Access the Application

Open your browser and navigate to:
- http://localhost:3000

You should see the RAG system home page with a chat interface.

### Development Workflow

**For Backend Development:**

```bash
cd backend

# Run with auto-reload (changes trigger restart)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Run tests
uv run pytest

# Format code
uv run black app/
uv run isort app/

# Add new dependencies
uv add package-name

# Add dev dependencies
uv add --dev pytest
```

**For Frontend Development:**

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Run production build locally
npm run build
npm start

# Lint code
npm run lint

# Add new dependencies
npm install package-name

# Add dev dependencies
npm install -D package-name
```

### Running Full Stack Locally

1. **Terminal 1** - Start infrastructure:
   ```bash
   docker compose up -d db minio
   ```

2. **Terminal 2** - Start backend:
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

3. **Terminal 3** - Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access**: http://localhost:3000

## 📁 Application Structure

```
rag/
├── backend/                   # Backend API Application
│   ├── app/
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── api.py        # API router configuration
│   │   │   └── endpoints/    # API route handlers
│   │   │       ├── documents.py      # Document management
│   │   │       ├── query.py          # RAG query endpoints
│   │   │       ├── datasource.py     # Data source management
│   │   │       ├── health.py         # Health checks
│   │   │       └── structured_extraction.py
│   │   ├── core/
│   │   │   └── config.py     # Application configuration/settings
│   │   ├── db/
│   │   │   ├── session.py    # Database session management
│   │   │   └── init_db.py    # Database initialization
│   │   ├── models/
│   │   │   └── document.py   # SQLAlchemy database models
│   │   ├── schemas/
│   │   │   └── schemas.py    # Pydantic request/response schemas
│   │   └── services/         # Business logic layer
│   │       ├── document_processor.py  # Document processing
│   │       ├── vector_store.py        # PGVector operations
│   │       ├── object_storage.py      # MinIO operations
│   │       ├── chunking_service.py    # Text chunking strategies
│   │       ├── file_watcher.py        # Auto-import files
│   │       ├── structured_extraction.py
│   │       ├── connectors/            # External data sources
│   │       │   ├── database_connector.py  # DB connectors
│   │       │   └── web_connector.py       # Web scraping
│   │       ├── embeddings/            # Embedding models
│   │       │   └── __init__.py
│   │       ├── parsers/               # Document parsers
│   │       │   ├── base.py           # Base parser class
│   │       │   ├── factory.py        # Parser factory
│   │       │   ├── pdf_parser.py     # PDF processing
│   │       │   ├── docx_parser.py    # Word documents
│   │       │   ├── image_parser.py   # Image OCR
│   │       │   ├── text_parser.py    # Plain text
│   │       │   ├── structured_parser.py  # CSV/Excel/JSON
│   │       │   └── web_parser.py     # HTML/web content
│   │       └── retrieval/            # RAG pipeline
│   │           ├── retriever.py      # Document retrieval
│   │           └── generator.py      # Response generation
│   ├── data/                 # Data directory (uploads, etc.)
│   ├── pyproject.toml       # Python dependencies (uv)
│   ├── requirements.txt     # Pip-compatible dependencies
│   ├── Dockerfile           # Backend container definition
│   ├── setup-env.sh         # Environment setup (Linux/Mac)
│   ├── setup-env.bat        # Environment setup (Windows)
│   └── init-db.sql          # PostgreSQL initialization
│
├── frontend/                 # Frontend Web Application
│   ├── src/
│   │   ├── app/             # Next.js 15 App Router
│   │   │   ├── page.tsx     # Home page (chat interface)
│   │   │   ├── layout.tsx   # Root layout
│   │   │   ├── documents/   # Document management pages
│   │   │   ├── datasources/ # Data source management
│   │   │   └── api/         # API proxy routes
│   │   │       └── [...path]/route.ts  # Catch-all proxy
│   │   ├── components/      # React components
│   │   │   ├── Chat/        # Chat interface components
│   │   │   │   ├── ChatWindow.tsx
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   ├── ChatMessage.tsx
│   │   │   │   └── MetricsPanel.tsx
│   │   │   ├── Documents/   # Document components
│   │   │   │   ├── DocumentList.tsx
│   │   │   │   └── DocumentUpload.tsx
│   │   │   ├── SidePanel/   # Side panel components
│   │   │   │   └── SidePanel.tsx
│   │   │   ├── Navigation/  # Navigation components
│   │   │   │   └── Navbar.tsx
│   │   │   └── Sources/     # Data source components
│   │   └── lib/             # Utilities and helpers
│   │       ├── api.ts       # API client functions
│   │       ├── types.ts     # TypeScript type definitions
│   │       ├── utils.ts     # Utility functions
│   │       └── websocket.ts # WebSocket client
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   ├── tsconfig.json        # TypeScript configuration
│   ├── tailwind.config.ts   # Tailwind CSS configuration
│   ├── next.config.ts       # Next.js configuration
│   └── Dockerfile           # Frontend container definition
│
├── docs/                     # Documentation
│   ├── index.md
│   ├── getting-started.md
│   ├── architecture.md
│   ├── api-reference.md
│   └── troubleshooting.md
│
├── docker-compose.yml        # Docker services orchestration
├── docker-compose.prod.yml   # Production configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

## ⚙️ Configuration Guide

### Complete Environment Variables Reference

All configuration is done through environment variables in the `.env` file. See `.env.example` for the complete template.

#### Core Application Settings

```env
# Application Environment
APP_ENV=development              # development or production
LOG_LEVEL=debug                  # debug, info, warning, error
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32

# Frontend Configuration
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:8080

# Backend Configuration  
BACKEND_PORT=8080
```

#### Database Configuration

```env
# PostgreSQL with PGVector
DATABASE_USER=raguser
DATABASE_PASSWORD=ragpassword
DATABASE_NAME=ragdb
DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb
```

#### Object Storage (MinIO)

```env
MINIO_URL=localhost:9000          # or minio:9000 in Docker
MINIO_ACCESS_KEY=minioadmin       # Should match .env.example
MINIO_SECRET_KEY=minioadmin       # Should match .env.example
MINIO_SECURE=False                # True for HTTPS, False for HTTP
```

#### LLM Provider Configuration

**Option 1: OpenAI**

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o               # or gpt-4, gpt-3.5-turbo

# Embedding Configuration
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_MODEL_DIMENSIONS=3072    # 3072 for large, 1536 for small
```

**Option 2: Azure OpenAI**

```env
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4o    # Your deployment name
AZURE_OPENAI_API_VERSION=2024-08-06

# Azure Embedding Configuration
EMBEDDING_PROVIDER=azure
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
```

#### Document Processing Settings

```env
# Chunking Configuration
CHUNK_SIZE=1000                   # Characters per chunk
CHUNK_OVERLAP=200                 # Overlap between chunks
MIN_CHUNK_SIZE=100                # Minimum chunk size

# Chunking Strategy: recursive, semantic, token, or sentence
CHUNKING_STRATEGY=recursive

# For semantic chunking
SEMANTIC_BREAKPOINT_TYPE=percentile  # percentile, standard_deviation, interquartile, gradient
```

**Chunking Strategies Explained:**

| Strategy | Description | Best For |
|----------|-------------|----------|
| `recursive` | Splits text hierarchically by separators | General-purpose, most documents |
| `semantic` | Splits based on semantic similarity | Maintaining context, varied content |
| `token` | Splits based on token count | Strict token limits, API constraints |
| `sentence` | Splits at sentence boundaries | Conversational content, Q&A |

#### Retrieval Settings

```env
MAX_RETRIEVED_DOCUMENTS=5         # Number of chunks to retrieve per query
```

#### File Management

```env
# Upload Settings
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE=10485760          # 10MB in bytes

# File Watcher (auto-import from MinIO)
ENABLE_FILE_WATCHER=true
FILE_WATCHER_INTERVAL=60          # Check every 60 seconds
```

#### Web Scraping

```env
SCRAPING_TIMEOUT=30               # Seconds before timeout
```

#### SSL/TLS Configuration

```env
# Disable SSL verification (development/corporate proxy only)
DISABLE_SSL_VERIFICATION=false    # Set to true if needed
```

### Getting API Keys

#### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and add to `.env` as `OPENAI_API_KEY`

#### Azure OpenAI

1. Log in to [Azure Portal](https://portal.azure.com/)
2. Create an "Azure OpenAI" resource
3. Deploy models (e.g., gpt-4o, text-embedding-3-large)
4. Go to "Keys and Endpoint" in your resource
5. Copy the key and endpoint to `.env`
6. Use your deployment names for `AZURE_OPENAI_DEPLOYMENT` and `AZURE_EMBEDDING_DEPLOYMENT`

## 📚 API Documentation

The backend provides a comprehensive REST API. Once running, access interactive documentation at:

- **Swagger UI**: http://localhost:8080/docs (Try out API endpoints directly)
- **ReDoc**: http://localhost:8080/redoc (Alternative documentation view)

### API Endpoints Overview

#### Health & Status

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/api/v1/health` | System health check | Status of all components |
| GET | `/health` | Root health endpoint | Simple OK response |

#### Document Management

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/v1/documents/` | List all documents | - |
| GET | `/api/v1/documents/{id}` | Get document details | - |
| POST | `/api/v1/documents/upload` | Upload a file | `multipart/form-data` with file |
| POST | `/api/v1/documents/web` | Index a web page | `{"url": "https://...", "description": "..."}` |
| POST | `/api/v1/documents/database` | Index database query results | Connection string + SQL query |
| DELETE | `/api/v1/documents/{id}` | Delete a document and its chunks | - |

#### Query & Search

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/v1/query/` | RAG query with LLM generation | `{"query": "...", "document_ids": [...]}` |
| POST | `/api/v1/query/search` | Semantic search only (no LLM) | `{"query": "...", "document_ids": [...]}` |

#### Data Sources

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/v1/datasources/` | List all data source configurations | - |
| POST | `/api/v1/datasources/` | Create new data source | Data source configuration |
| PUT | `/api/v1/datasources/{id}` | Update data source | Updated configuration |
| DELETE | `/api/v1/datasources/{id}` | Delete data source | - |

#### Structured Extraction

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/v1/extract/` | Extract structured data from documents | Schema definition + query |

## 💡 Usage Examples

### Using the Web Interface

1. **Upload Documents**
   - Navigate to http://localhost:3000
   - Click "Upload" in the side panel
   - Select files (PDF, DOCX, TXT, CSV, XLSX, JSON, images)
   - Add optional description
   - Click "Upload"

2. **Query Documents**
   - Type your question in the chat input
   - Optionally select specific documents to search
   - Press Enter or click Send
   - View AI-generated response with source citations

3. **Manage Data Sources**
   - Go to "Data Sources" page
   - Add database connections or web URLs
   - Configure auto-sync settings
   - Test connections

### Using the API (cURL Examples)

#### 1. Check System Health

```bash
curl http://localhost:8080/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "minio": "connected",
  "llm": "configured"
}
```

#### 2. Upload a Document

```bash
curl -X POST "http://localhost:8080/api/v1/documents/upload" \
  -F "file=@/path/to/document.pdf" \
  -F "description=Q4 Financial Report"
```

Response:
```json
{
  "id": "doc-abc123",
  "filename": "document.pdf",
  "status": "processing",
  "description": "Q4 Financial Report"
}
```

#### 3. List All Documents

```bash
curl http://localhost:8080/api/v1/documents/
```

#### 4. Query Documents with RAG

```bash
curl -X POST "http://localhost:8080/api/v1/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What were the revenue figures for Q4?",
    "document_ids": ["doc-abc123"]
  }'
```

Response:
```json
{
  "query": "What were the revenue figures for Q4?",
  "answer": "According to the Q4 Financial Report, the revenue was $2.5M...",
  "sources": [
    {
      "document_id": "doc-abc123",
      "chunk_text": "Q4 revenue: $2.5M...",
      "similarity_score": 0.89
    }
  ],
  "metrics": {
    "retrieval_time_seconds": 0.3,
    "generation_time_seconds": 2.1,
    "total_time_seconds": 2.4
  }
}
```

#### 5. Semantic Search Only (No LLM)

```bash
curl -X POST "http://localhost:8080/api/v1/query/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "revenue figures",
    "document_ids": []
  }'
```

#### 6. Index a Web Page

```bash
curl -X POST "http://localhost:8080/api/v1/documents/web" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "description": "Industry Analysis Article"
  }'
```

#### 7. Index Database Query Results

```bash
curl -X POST "http://localhost:8080/api/v1/documents/database" \
  -H "Content-Type: application/json" \
  -d '{
    "connection_string": "postgresql://user:password@host:5432/dbname",
    "query": "SELECT * FROM products WHERE category = '\''electronics'\''",
    "description": "Electronics product catalog"
  }'
```

#### 8. Delete a Document

```bash
curl -X DELETE "http://localhost:8080/api/v1/documents/doc-abc123"
```

### Using Python

```python
import requests

# Configuration
BASE_URL = "http://localhost:8080/api/v1"

# Upload a document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {"description": "My document"}
    response = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
    doc_id = response.json()["id"]

# Query documents
query_data = {
    "query": "What is the main topic?",
    "document_ids": [doc_id]
}
response = requests.post(f"{BASE_URL}/query/", json=query_data)
result = response.json()
print(f"Answer: {result['answer']}")
```

### Using JavaScript/TypeScript

```javascript
// Upload a document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('description', 'My document');

const uploadResponse = await fetch('http://localhost:8080/api/v1/documents/upload', {
  method: 'POST',
  body: formData
});
const { id: docId } = await uploadResponse.json();

// Query documents
const queryResponse = await fetch('http://localhost:8080/api/v1/query/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What is the main topic?',
    document_ids: [docId]
  })
});
const result = await queryResponse.json();
console.log('Answer:', result.answer);
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Docker Services Not Starting

**Problem:** Services fail to start or show unhealthy status

**Solutions:**
```bash
# Check service status
docker compose ps

# View logs for specific service
docker compose logs backend
docker compose logs db
docker compose logs minio

# Restart services
docker compose restart

# Clean restart (removes containers but keeps data)
docker compose down
docker compose up -d

# Full reset (⚠️ deletes all data)
docker compose down -v
docker compose up -d
```

#### 2. Database Connection Errors

**Problem:** `connection refused` or `database does not exist`

**Solutions:**
- Verify PostgreSQL is running: `docker compose ps db`
- Check connection string in `.env`:
  ```env
  DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb
  ```
- For Docker: use `db` as host (not `localhost`)
  ```env
  DATABASE_URL=postgresql://raguser:ragpassword@db:5432/ragdb
  ```
- Wait for database to be healthy (30-60 seconds on first start)
- Check logs: `docker compose logs db`

#### 3. MinIO Connection Errors

**Problem:** `connection refused` or authentication errors

**Solutions:**
- Verify MinIO is running: `docker compose ps minio`
- Check credentials match `.env`:
  ```env
  MINIO_ACCESS_KEY=ragadmin2024
  MINIO_SECRET_KEY=ragadminsecret2024
  ```
- For Docker: use `minio:9000` as endpoint
- For local development: use `localhost:9000`
- Access console: http://localhost:9001 (verify login works)

#### 4. LLM / API Key Errors

**Problem:** `Invalid API key` or `model not found`

**Solutions:**
- **OpenAI:**
  - Verify API key is valid: https://platform.openai.com/api-keys
  - Check account has credits/active subscription
  - Confirm model name is correct (e.g., `gpt-4o`, not `gpt-4-openai`)
  
- **Azure OpenAI:**
  - Verify endpoint URL format: `https://YOUR-RESOURCE.openai.azure.com`
  - Check deployment names match Azure portal exactly
  - Verify API version is supported: `2024-08-06`
  - Ensure resource has deployed models

- **SSL Issues (Corporate Proxy):**
  ```env
  DISABLE_SSL_VERIFICATION=true  # Development only!
  ```

#### 5. Frontend Cannot Connect to Backend

**Problem:** 404 errors or CORS issues

**Solutions:**
- Verify backend is running: `curl http://localhost:8080/api/v1/health`
- Check `.env.local` in frontend:
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:3000/api
  BACKEND_URL=http://localhost:8080
  ```
- For Docker: backend URL should be `http://backend:8080`
- Check browser console for CORS errors
- Restart frontend: `npm run dev`

#### 6. Documents Not Processing

**Problem:** Documents stuck in "processing" status

**Solutions:**
- Check backend logs for errors: `docker compose logs backend`
- Verify file format is supported
- Check file size (default limit: 10MB)
- Ensure MinIO storage is accessible
- Verify embedding model is configured correctly
- Check disk space

#### 7. Poor Search Results

**Problem:** Irrelevant results or no results

**Solutions:**
- Try different chunking strategies in `.env`:
  ```env
  CHUNKING_STRATEGY=semantic  # or recursive, token, sentence
  ```
- Adjust chunk size:
  ```env
  CHUNK_SIZE=500  # Smaller chunks for precise matching
  CHUNK_OVERLAP=100
  ```
- Increase number of retrieved documents:
  ```env
  MAX_RETRIEVED_DOCUMENTS=10
  ```
- Reprocess documents after configuration changes

#### 8. Port Already in Use

**Problem:** `address already in use` error

**Solutions:**
```bash
# Find process using port
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process or change port in .env
BACKEND_PORT=8081
FRONTEND_PORT=3001
```

#### 9. Performance Issues

**Problem:** Slow response times

**Solutions:**
- Use `semantic` chunking for better context
- Reduce `MAX_RETRIEVED_DOCUMENTS` for faster retrieval
- Use smaller embedding model if accuracy allows
- Check database query performance
- Enable database indexing (automatic with PGVector)
- Increase Docker resource limits in `docker-compose.yml`

#### 10. Python/Node Version Issues

**Problem:** Compatibility errors

**Solutions:**
```bash
# Check versions
python --version  # Should be 3.11+
node --version    # Should be 18+

# Use version manager
pyenv install 3.11
nvm install 18
```

### Getting Debug Logs

**Backend (detailed logs):**
```bash
# In .env or as command prefix
LOG_LEVEL=debug

# Run with debug
cd backend
LOG_LEVEL=debug uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

**Docker logs:**
```bash
# All services
docker compose logs -f

# Specific service with timestamps
docker compose logs -f --timestamps backend

# Save logs to file
docker compose logs backend > backend.log 2>&1
```

**Frontend logs:**
```bash
# Check browser console (F12)
# Check terminal where npm run dev is running
```

### Getting Help

If you're still experiencing issues:

1. **Check Documentation:** https://nitin27may.github.io/rag/
2. **Search Issues:** https://github.com/nitin27may/rag/issues
3. **Create New Issue:** Include:
   - Operating system
   - Python/Node versions
   - Docker version (if applicable)
   - Error messages
   - Relevant logs
   - Steps to reproduce

## 📖 Additional Documentation

Full documentation is available at: **[https://nitin27may.github.io/rag/](https://nitin27may.github.io/rag/)**

- [Getting Started Guide](https://nitin27may.github.io/rag/getting-started/)
- [Architecture Details](https://nitin27may.github.io/rag/architecture/)
- [API Reference](https://nitin27may.github.io/rag/api-reference/)
- [Chunking Strategies](https://nitin27may.github.io/rag/chunking-strategies/)
- [RAG Concepts](https://nitin27may.github.io/rag/rag-explained/)
- [User Guide](https://nitin27may.github.io/rag/user-guide/)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/rag.git
   cd rag
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   uv run pytest
   
   # Frontend linting
   cd frontend
   npm run lint
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Wait for review

### Development Guidelines

- Write clear, descriptive commit messages
- Follow Python PEP 8 style guidelines
- Use TypeScript for frontend code
- Add comments for complex logic
- Update README if adding new features
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [LangChain](https://langchain.com/) - LLM application framework
- [PostgreSQL](https://www.postgresql.org/) with [PGVector](https://github.com/pgvector/pgvector) - Vector database
- [MinIO](https://min.io/) - Object storage
- [OpenAI](https://openai.com/) / [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - LLM services

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/nitin27may/rag/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nitin27may/rag/discussions)
- **Documentation:** [Project Docs](https://nitin27may.github.io/rag/)

---

Made with ❤️ by [Nitin Singh](https://github.com/nitin27may)
