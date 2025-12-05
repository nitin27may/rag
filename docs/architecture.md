---
layout: default
title: System Architecture
nav_order: 4
permalink: /architecture/
---

# System Architecture
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This document explains the architecture of the Comprehensive RAG System, including how the components interact and the data flow through the system.

## High-Level Overview

The RAG system consists of three main components:

1. **Frontend**: A Next.js 15 React application for user interaction
2. **Backend API**: A FastAPI Python application that handles document processing, vector storage, and RAG operations
3. **Data Storage**: PostgreSQL database with pgvector extension for storing documents and embeddings

![System Architecture Diagram](../screenshots/rag-api.png)

## Component Breakdown

### Frontend Architecture

The frontend is built with:
- **Next.js**: React framework for the user interface
- **TypeScript**: For type-safe code
- **TailwindCSS**: For styling components
- **React Hooks**: For state management
- **Axios**: For API communication

Key frontend components include:
- Document upload interface
- Document list and management
- Chat interface for queries
- Visualization of search results and responses
- Admin panel for system configuration

### Backend Architecture

The backend is structured as follows:
- **FastAPI**: For RESTful API and WebSocket endpoints
- **SQLAlchemy**: ORM for database interactions
- **LangChain**: Framework for LLM operations and vector search
- **PostgreSQL + PGVector**: Database with vector extension for storing embeddings
- **MinIO/S3**: Object storage for document files

Key backend components:

#### API Layer
- RESTful endpoints for document management, queries, data extraction
- WebSockets for real-time updates
- Health check and monitoring endpoints

#### Service Layer
- Document processing services
- Vector store services
- Retrieval services
- Generation services
- Extraction services

#### Data Access Layer
- Database models and repositories
- Vector store access
- Object storage access

## Data Flow

### Document Ingestion Flow

1. User uploads a document via frontend or API
2. Document metadata is stored in the database
3. Document file is stored in object storage
4. Document is processed:
   - Text extraction
   - Chunking (configurable strategy - see [Chunking Strategies](/chunking-strategies/))
   - Embedding generation
5. Chunks and embeddings are stored in the vector database
6. Document processing status is updated

### Query Flow

1. User submits a query via frontend or API
2. Query is processed:
   - Query embedding is generated
   - Relevant document chunks are retrieved from vector store
   - Context is assembled from retrieved chunks
   - Query + context is sent to LLM for generation
3. Response is returned to user
4. Query and results are logged

## Detailed Component Diagram

```
┌───────────────┐     ┌────────────────────────────────────┐     ┌──────────────────────┐
│               │     │                                    │     │                      │
│   Frontend    │◄────┤           Backend API              │◄────┤ PostgreSQL + PGVector│
│ (Next.js 15)  │     │           (FastAPI)                │     │ (Documents & Vectors)│
│               │─────►                                    │─────►                      │
└───────────────┘     └────────────────┬───────────────────┘     └──────────────────────┘
                                       │
                                       ▼
                      ┌────────────────┴───────────────────┐
                      │                                    │
                      │         Object Storage             │
                      │          (MinIO/S3)                │
                      │                                    │
                      └────────────────────────────────────┘
                                       │
                                       ▼
                      ┌────────────────┴───────────────────┐
                      │                                    │
                      │         Object Storage             │
                      │          (MinIO/S3)                │
                      │                                    │
                      └────────────────────────────────────┘
```

## Application Structure

The application follows a structured folder organization:

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
│   │   │   ├── connectors/    # Data source connectors
│   │   │   ├── embeddings/    # Embedding models
│   │   │   ├── parsers/       # Document parsers
│   │   │   └── retrieval/     # Retrieval logic
│   │   └── static/            # Static files
│   ├── data/                  # Data directory
│   └── tests/                 # Test files
├── frontend/                  # Frontend application
│   ├── public/                # Public assets
│   ├── src/                   # Source code
│   │   ├── app/               # Next.js app directory
│   │   ├── components/        # React components
│   │   └── lib/               # Utility functions and types
└── docker-compose.yml         # Docker configuration
```

## Key Technologies

- **Python 3.11+**: Backend language
- **TypeScript/JavaScript**: Frontend language
- **FastAPI**: API framework
- **Next.js 15**: React framework
- **LangChain**: LLM framework
- **PostgreSQL + PGVector**: Database with vector search
- **Azure OpenAI / OpenAI**: LLM and embedding provider
- **MinIO/S3**: Object storage
- **Docker**: Containerization
- **uv**: Python package manager

## Scalability Considerations

The system is designed with scalability in mind:

- **Horizontal Scaling**: The API layer can be scaled horizontally
- **Asynchronous Processing**: Document processing happens asynchronously
- **Separation of Concerns**: Clear boundaries between components allow for independent scaling
- **Database Sharding**: PostgreSQL can be sharded for larger deployments
- **Vector Indexing**: PGVector supports HNSW and IVFFlat indexes for efficient similarity search

For extremely large document collections, consider:
- Implementing a document queue system
- Adding a caching layer
- PostgreSQL read replicas
- Batch processing for document ingestion