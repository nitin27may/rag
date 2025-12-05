# Comprehensive RAG System

A Retrieval-Augmented Generation (RAG) system for querying and extracting insights from your documents using LLMs.

## Features

- **Document Ingestion**: Process files (PDF, DOCX, TXT, CSV, XLSX, JSON, images), web pages, and database content
- **Vector Search**: Semantic similarity search using PostgreSQL with PGVector
- **Multi-Document Selection**: Query specific documents or search across all indexed content
- **Database Connector**: Query and index data directly from PostgreSQL, MySQL, or SQLite databases
- **Hybrid Retrieval**: Combine vector search with keyword filtering for more relevant results
- **Question-Answering**: Generate accurate responses based on context from your documents
- **Structured Extraction**: Extract specific data from documents using customizable schemas
- **Modern Web Interface**: Next.js 15 with React 19 UI for document management and querying
- **RESTful API**: Comprehensive API for integration with other systems
- **WebSocket Support**: Real-time streaming responses
- **Health Monitoring**: System health checks for all components

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy 2.x |
| **Vector Store** | PostgreSQL with pgvector extension |
| **LLM/Embeddings** | Azure OpenAI or OpenAI (GPT-4, text-embedding-3-small) |
| **Frontend** | Next.js 15, React 19, Tailwind CSS |
| **Object Storage** | MinIO (S3-compatible) |
| **Package Manager** | uv (10-100x faster than pip) |

## Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/nitin27may/rag.git
cd rag

# Copy environment file and configure
cp .env.example .env
# Edit .env with your Azure OpenAI or OpenAI credentials

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8080/docs
# MinIO Console: http://localhost:9001
```

## Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (for PostgreSQL and MinIO)

### Backend Setup

```bash
cd backend

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# or: setup-env.bat     # Windows
# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI or OpenAI credentials 

# Run the server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:3000/api" > .env.local
echo "BACKEND_URL=http://localhost:8080" >> .env.local

# Start development server
npm run dev
```

Access the frontend at `http://localhost:3000`

## Application Structure

```
rag/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/     # API route handlers
│   │   ├── core/              # Configuration
│   │   ├── db/                # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   │       ├── connectors/    # Database/web connectors
│   │       ├── parsers/       # Document parsers
│   │       └── retrieval/     # RAG retrieval & generation
│   ├── pyproject.toml         # Python dependencies (uv)
│   └── requirements.txt       # Fallback dependencies
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js app router pages
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities and types
│   └── package.json
├── docker-compose.yml
└── docs/                      # Documentation
```

## Configuration

Key environment variables (see `.env.example` for full list):

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

## API Endpoints

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/documents/` | List all documents |
| POST | `/api/v1/documents/upload` | Upload a file |
| POST | `/api/v1/documents/web` | Index a web page |
| POST | `/api/v1/documents/database` | Index database query results |
| DELETE | `/api/v1/documents/{id}` | Delete a document |

### Query
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/query/` | Query with RAG (supports document selection) |
| POST | `/api/v1/query/search` | Semantic search only |

### Data Sources
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/datasources/` | List data sources |
| POST | `/api/v1/datasources/` | Create data source |
| DELETE | `/api/v1/datasources/{id}` | Delete data source |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | System health check |

## Usage Examples

### Upload a Document
```bash
curl -X POST "http://localhost:8080/api/v1/documents/upload" \
  -F "file=@document.pdf" \
  -F "description=My document"
```

### Query Documents
```bash
curl -X POST "http://localhost:8080/api/v1/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main topic?",
    "document_ids": ["doc-id-1", "doc-id-2"]
  }'
```

### Index Database Content
```bash
curl -X POST "http://localhost:8080/api/v1/documents/database" \
  -H "Content-Type: application/json" \
  -d '{
    "connection_string": "postgresql://user:pass@host:5432/db",
    "query": "SELECT * FROM products LIMIT 100",
    "description": "Product catalog"
  }'
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running with pgvector extension

2. **Azure OpenAI Errors**
   - Check `AZURE_OPENAI_*` environment variables
   - Verify deployment names match your Azure resources
   - For SSL issues in dev: set `DISABLE_SSL_VERIFICATION=true`

3. **MinIO Connection Error**
   - Verify MinIO credentials in `.env`
   - Check if MinIO container is running

### Debug Mode

```bash
LOG_LEVEL=debug uv run uvicorn app.main:app --reload
```

## Documentation

Full documentation available at: [https://nitin27may.github.io/rag/](https://nitin27may.github.io/rag/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.
