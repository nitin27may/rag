# Comprehensive RAG System

A Retrieval-Augmented Generation (RAG) system for querying and extracting insights from your documents using LLMs.

## Features

- Document ingestion from files, web pages, and databases
- Vector-based similarity search using ChromaDB
- Question-answering with context from your documents
- Web interface for document management and querying
- RESTful API for integration with other systems
- WebSocket support for real-time updates

## System Requirements

- Python 3.8+ 
- PostgreSQL database (optional, can use SQLite for development)
- MinIO or S3-compatible object storage (optional)
- ChromaDB for vector storage

## Installation

### Prerequisites

1. Install Python 3.8 or higher
2. Install PostgreSQL (optional)
3. Install MinIO (optional)
4. Install ChromaDB (optional for local development)

### Setup Instructions

#### Common Steps (Windows and macOS)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rag.git
   cd rag
   ```

2. Create a virtual environment:
   ```
   python -m venv rag_env
   ```

3. Copy the example environment file and edit it:
   ```
   cp .env.example .env
   ```
   - Edit `.env` with your configuration (database URL, API keys, etc.)

#### Windows Setup

1. Activate the virtual environment:
   ```
   rag_env\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m pip install python-socketio[asyncio] aiohttp websockets
   ```

3. Create required directories:
   ```
   python ensure_directories.py
   ```

4. Start the application:
   ```
   python run.py
   ```

#### macOS/Linux Setup

1. Activate the virtual environment:
   ```
   source rag_env/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m pip install python-socketio[asyncio] aiohttp websockets
   ```

3. Create required directories:
   ```
   python ensure_directories.py
   ```

4. Start the application:
   ```
   python run.py
   ```

## Application Structure

```
rag/
├── app/                    # Application code
│   ├── api/                # API endpoints
│   ├── core/               # Core configuration
│   ├── db/                 # Database models and connection
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   │   ├── connectors/     # Data source connectors
│   │   ├── embeddings/     # Embedding models
│   │   ├── parsers/        # Document parsers
│   │   └── retrieval/      # Retrieval logic
│   └── static/             # Static frontend files
├── data/                   # Data directory
│   ├── processed/          # Processed documents
│   ├── raw/                # Raw documents
│   └── uploads/            # Uploaded files
├── tests/                  # Test files
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Configuration

The system is configured using environment variables in the `.env` file:

- `DATABASE_URL`: Connection string for the database
- `CHROMA_HOST`: ChromaDB host
- `CHROMA_PORT`: ChromaDB port
- `MINIO_URL`: MinIO/S3 URL
- `MINIO_ACCESS_KEY`: MinIO/S3 access key
- `MINIO_SECRET_KEY`: MinIO/S3 secret key
- `OPENAI_API_KEY`: OpenAI API key for embeddings and LLM
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `EMBEDDING_MODEL`: Embedding model to use

## Usage

1. Start the application server:
   ```
   python run.py
   ```

2. Access the web interface at `http://localhost:8000`

3. API documentation is available at `http://localhost:8000/docs`

## API Endpoints

- **Documents**: `/api/v1/documents`
  - `GET`: List all documents
  - `POST`: Upload a document
  - `DELETE /{id}`: Delete a document

- **Query**: `/api/v1/query`
  - `POST /retrieve`: Retrieve relevant documents
  - `POST /generate`: Generate an answer

- **Data Sources**: `/api/v1/datasources`
  - `GET`: List all data sources
  - `POST`: Add a new data source
  - `DELETE /{id}`: Delete a data source

- **Health**: `/api/v1/health`
  - `GET`: Check system health

## WebSockets

The system also supports WebSockets for real-time updates:

- Socket.IO endpoint: `/ws/socket.io`
- Direct WebSocket: `/api/ws`

Use the WebSocket test page at `http://localhost:8000/static/websocket_test.html` to verify connectivity.

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify database credentials in `.env`
   - Check if PostgreSQL is running

2. **MinIO Connection Error**
   - Verify MinIO/S3 credentials in `.env`
   - Check if MinIO is running

3. **WebSocket Connection Error**
   - For Socket.IO issues, ensure `python-socketio[asyncio]` is installed
   - Test connectivity using the WebSocket test page

4. **OpenAI API Key Error**
   - Verify your OpenAI API key in `.env`
   - Check API key permissions

### Debug Mode

Run the application in debug mode to see more detailed logs:

```
LOG_LEVEL=debug python run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
