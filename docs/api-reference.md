---
layout: default
title: API Reference
nav_order: 6
permalink: /api-reference/
---

# API Reference
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This document provides detailed information about the REST API endpoints available in the Comprehensive RAG System.

## Base URL

All API endpoints are prefixed with `/api/v1`.

Example: `http://localhost:8000/api/v1`

## Authentication

Currently, the API uses basic API key authentication. Include your API key in the request headers:

```
X-API-Key: your-api-key-here
```

## Documents API

### List Documents

Retrieves all documents in the system.

**Endpoint:** `GET /documents`

**Query Parameters:**
- `skip` (optional): Number of documents to skip (default: 0)
- `limit` (optional): Maximum number of documents to return (default: 100)

**Response:**
```json
[
  {
    "id": "string",
    "filename": "string",
    "title": "string",
    "description": "string",
    "mime_type": "string",
    "source_type": "string",
    "source_path": "string",
    "storage_path": "string",
    "file_size": 0,
    "page_count": 0,
    "doc_metadata": {},
    "is_processed": true,
    "is_indexed": true,
    "processing_error": "string",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z",
    "collection_name": "string"
  }
]
```

### Upload Document

Upload a new document to be processed and indexed.

**Endpoint:** `POST /documents/upload`

**Content Type:** `multipart/form-data`

**Form Parameters:**
- `file`: The file to upload (required)
- `description`: Document description (optional)

**Response:**
```json
{
  "id": "string",
  "status": "string",
  "message": "string",
  "chunk_count": 0,
  "collection": "string"
}
```

### Process Web Page

Add a web page to be processed and indexed.

**Endpoint:** `POST /documents/web`

**Request Body:**
```json
{
  "url": "https://example.com",
  "description": "Example web page"
}
```

**Response:**
```json
{
  "id": "string",
  "status": "string",
  "message": "string"
}
```

### Get Document Details

Retrieve details for a specific document.

**Endpoint:** `GET /documents/{document_id}`

**Path Parameters:**
- `document_id`: The unique document identifier

**Response:**
```json
{
  "id": "string",
  "filename": "string",
  "title": "string",
  "description": "string",
  "mime_type": "string",
  "source_type": "string",
  "source_path": "string",
  "storage_path": "string",
  "file_size": 0,
  "page_count": 0,
  "doc_metadata": {},
  "is_processed": true,
  "is_indexed": true,
  "processing_error": "string",
  "created_at": "2023-01-01T00:00:00.000Z",
  "updated_at": "2023-01-01T00:00:00.000Z",
  "collection_name": "string"
}
```

### Get Document Chunks

Retrieve chunks for a specific document.

**Endpoint:** `GET /documents/{document_id}/chunks`

**Path Parameters:**
- `document_id`: The unique document identifier

**Query Parameters:**
- `skip` (optional): Number of chunks to skip (default: 0)
- `limit` (optional): Maximum number of chunks to return (default: 100)

**Response:**
```json
[
  {
    "id": "string",
    "document_id": "string",
    "chunk_index": 0,
    "content": "string",
    "vector_id": "string",
    "chunk_metadata": {}
  }
]
```

### Delete Document

Delete a document and its chunks.

**Endpoint:** `DELETE /documents/{document_id}`

**Path Parameters:**
- `document_id`: The unique document identifier

**Response:**
```json
{
  "status": "string",
  "message": "string"
}
```

## Query API

### Generate Answer

Generate an answer to a question based on the document repository.

**Endpoint:** `POST /query/generate`

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "collection_names": ["documents", "web_pages"],
  "filter_criteria": {},
  "document_id": "optional-document-id",
  "top_k": 5
}
```

**Response:**
```json
{
  "query": "string",
  "answer": "string",
  "context": "string",
  "documents": [
    {
      "content": "string",
      "metadata": {}
    }
  ],
  "metrics": {
    "total_time_seconds": 0,
    "retrieval_time_seconds": 0,
    "generation_time_seconds": 0,
    "total_documents": 0
  }
}
```

### Query Specific Document

Generate an answer to a question based on a specific document.

**Endpoint:** `POST /query/document/{document_id}/query`

**Path Parameters:**
- `document_id`: The unique document identifier

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "filter_criteria": {},
  "top_k": 5
}
```

**Response:** Same as the `/query/generate` endpoint response.

### Retrieve Documents

Retrieve relevant documents for a query without generating an answer.

**Endpoint:** `POST /query/retrieve`

**Request Body:**
```json
{
  "query": "What is the capital of France?",
  "collection_names": ["documents", "web_pages"],
  "filter_criteria": {},
  "document_id": "optional-document-id",
  "top_k": 5
}
```

**Response:**
```json
{
  "documents": [
    {
      "content": "string",
      "metadata": {}
    }
  ],
  "context": "string",
  "metrics": {
    "retrieval_time_seconds": 0,
    "total_documents": 0,
    "filtered_documents": 0
  }
}
```

## Extraction API

### Structured Extraction

Extract structured data from documents based on a schema.

**Endpoint:** `POST /extraction/structured-extract`

**Request Body:**
```json
{
  "document_id": "string",
  "schema_definition": {
    "title": "string",
    "author": "string",
    "publication_date": "date",
    "abstract": "string",
    "keywords": "list"
  }
}
```

**Response:**
```json
{
  "document_id": "string",
  "extracted_data": {
    "title": "Example Document",
    "author": "John Doe",
    "publication_date": "2023-01-01",
    "abstract": "This is an example abstract.",
    "keywords": ["example", "document", "extraction"]
  },
  "confidence_scores": {
    "title": 0.95,
    "author": 0.85,
    "publication_date": 0.75,
    "abstract": 0.9,
    "keywords": 0.8
  }
}
```

## Data Sources API

### List Data Sources

Get all configured data sources.

**Endpoint:** `GET /datasources`

**Response:**
```json
[
  {
    "id": "string",
    "name": "string",
    "source_type": "string",
    "connection_details": {},
    "is_active": true,
    "last_sync": "2023-01-01T00:00:00.000Z",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z"
  }
]
```

### Add Data Source

Add a new data source configuration.

**Endpoint:** `POST /datasources`

**Request Body:**
```json
{
  "name": "Company Wiki",
  "source_type": "website",
  "connection_details": {
    "base_url": "https://wiki.example.com",
    "auth_username": "user",
    "auth_password": "pass"
  }
}
```

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "source_type": "string",
  "is_active": true,
  "created_at": "2023-01-01T00:00:00.000Z"
}
```

### Delete Data Source

Delete a data source configuration.

**Endpoint:** `DELETE /datasources/{datasource_id}`

**Path Parameters:**
- `datasource_id`: The unique data source identifier

**Response:**
```json
{
  "status": "string",
  "message": "string"
}
```

## Health API

### System Health Check

Check the system health and status of all components.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": {
      "status": "healthy",
      "message": "Connected to PostgreSQL with pgvector"
    },
    "vector_store": {
      "status": "healthy",
      "message": "PGVector extension available"
    },
    "object_storage": {
      "status": "healthy",
      "message": "Connected to MinIO"
    },
    "llm": {
      "status": "healthy",
      "message": "Connected to Azure OpenAI API"
    }
  }
}
```

## WebSocket API

The system provides WebSocket endpoints for real-time updates.

### WebSocket Connection

Connect to the WebSocket API:

```
ws://localhost:8000/api/ws
```

### Events

Once connected, you'll receive various events:

- `document_processed`: When a document finishes processing
- `document_indexed`: When a document is indexed in the vector store
- `query_complete`: When a query response is generated
- `system_status`: System health updates

### Event Format

```json
{
  "event": "document_processed",
  "data": {
    "document_id": "string",
    "status": "success",
    "message": "Document processed successfully"
  },
  "timestamp": "2023-01-01T00:00:00.000Z"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid API key
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include detailed information:

```json
{
  "detail": "Error message explaining the issue"
}
```

## Rate Limits

The API has the following rate limits:

- 60 requests per minute for document queries
- 10 requests per minute for document uploads
- 30 requests per minute for other endpoints

When rate limited, you'll receive a `429 Too Many Requests` status code with a `Retry-After` header.