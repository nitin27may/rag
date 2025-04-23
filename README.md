# Comprehensive RAG System

A Retrieval-Augmented Generation (RAG) system for querying and extracting insights from your documents using LLMs.

## Features

- **Document Ingestion**: Process files (PDF, DOCX, TXT, CSV, XLSX, images), web pages, and database content
- **Vector Search**: Semantic similarity search using ChromaDB with embedding models
- **Hybrid Retrieval**: Combine vector search with keyword filtering for more relevant results
- **Question-Answering**: Generate accurate responses based on context from your documents
- **Structured Extraction**: Extract specific data from documents using customizable schemas
- **Modern Web Interface**: React-based UI for document management and querying
- **RESTful API**: Comprehensive API for integration with other systems
- **WebSocket Support**: Real-time updates and notifications
- **Multiple Data Sources**: Connect to file systems, databases, websites, and APIs
- **Health Monitoring**: System health checks for all components

## System Requirements

- Python 3.8+ 
- PostgreSQL database (optional, can use SQLite for development)
- MinIO or S3-compatible object storage (optional)
- ChromaDB for vector storage
- Node.js and npm for frontend development

## Installation

### Prerequisites

1. Install Python 3.8 or higher
2. Install PostgreSQL (optional)
3. Install MinIO (optional)
4. Install ChromaDB (optional for local development)
5. Install Node.js and npm for frontend

### Backend Setup

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

4. Activate the virtual environment:
   - Windows: `rag_env\Scripts\activate`
   - macOS/Linux: `source rag_env/bin/activate`

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Create required directories:
   ```
   mkdir -p data/uploads data/raw data/processed
   ```

7. Start the backend:
   ```
   python run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set the environment variable for the API URL:
   - Create `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8080`

4. Start the development server:
   ```
   npm run dev
   ```

5. Access the frontend at `http://localhost:3000`

## Docker Setup

1. Make sure Docker and Docker Compose are installed
2. Configure environment variables in `docker-compose.yml`
3. Build and start the containers:
   ```
   docker-compose up -d
   ```

## Application Structure

```
rag/
├── backend/                   # Backend application
│   ├── app/                   # Application code
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Core configuration
│   │   ├── db/                # Database models and connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── static/            # Static files
│   ├── data/                  # Data directory
│   ├── tests/                 # Test files
│   ├── .env                   # Environment variables
│   └── requirements.txt       # Python dependencies
├── frontend/                  # Frontend application
│   ├── public/                # Public assets
│   ├── src/                   # Source code
│   │   ├── app/               # Next.js app directory
│   │   ├── components/        # React components
│   │   └── lib/               # Utility functions and types
│   ├── .env.local             # Local environment variables
│   └── package.json           # Node.js dependencies
└── docker-compose.yml         # Docker configuration
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
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o)
- `EMBEDDING_MODEL`: Embedding model to use
- Check `.env.example` for all available configuration options

## Usage

### Document Management

1. **Upload Documents**: Use the web interface to upload files or add web pages
2. **View Documents**: Browse and manage your uploaded documents
3. **Data Sources**: Configure external data sources for automatic ingestion

### Querying Documents

1. **Chat Interface**: Use the chat interface to ask questions about your documents
2. **Document Retrieval**: View which documents were used to generate answers
3. **Performance Metrics**: See retrieval and generation metrics for each query

### Structured Data Extraction

Extract specific data from documents using a schema definition:

```json
{
  "document_id": "your-document-id",
  "schema_definition": {
    "title": "string",
    "author": "string",
    "publication_date": "date",
    "abstract": "string",
    "keywords": "list"
  }
}
```

## API Endpoints

- **Documents**: `/api/v1/documents`
  - `GET`: List all documents
  - `POST /upload`: Upload a document
  - `POST /web`: Process a web page
  - `DELETE /{id}`: Delete a document

- **Query**: `/api/v1/query`
  - `POST /retrieve`: Retrieve relevant documents
  - `POST /generate`: Generate an answer

- **Data Sources**: `/api/v1/datasources`
  - `GET`: List all data sources
  - `POST`: Add a new data source
  - `DELETE /{id}`: Delete a data source

- **Extraction**: `/api/v1/extraction/structured-extract`
  - `POST`: Extract structured data from documents

- **Health**: `/api/v1/health`
  - `GET`: Check system health

## WebSockets

The system supports WebSockets for real-time updates:

- WebSocket endpoint: `/api/ws`
- Test page: `/websocket`

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify database credentials in `.env`
   - Check if PostgreSQL is running

2. **MinIO Connection Error**
   - Verify MinIO/S3 credentials in `.env`
   - Check if MinIO is running

3. **OpenAI API Key Error**
   - Verify your OpenAI API key in `.env`
   - Check API key permissions

### Debug Mode

Run the application in debug mode for more detailed logs:

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
