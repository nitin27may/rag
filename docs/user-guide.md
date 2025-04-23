---
layout: default
title: User Guide
nav_order: 7
permalink: /user-guide/
---

# User Guide
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This guide provides instructions on how to use the Comprehensive RAG System for day-to-day operations.

## Web Interface

### Dashboard Overview

The dashboard provides an overview of your document repository, recent queries, and system health.

![Document List](../screenshots/listofcouments.png)

Key elements include:
- Document summary (total count, processing status)
- Recent activity feed
- Quick access to common actions
- System health indicators

### Document Management

#### Uploading Documents

1. Click **Upload** from the dashboard or document list
2. Select a file from your computer (supported formats: PDF, DOCX, TXT, CSV, XLSX, images)
3. Add an optional description
4. Click **Upload**
5. Wait for processing to complete (this may take some time for large documents)

#### Processing Web Pages

1. Click **Add Web Page** from the dashboard or document list
2. Enter the URL of the web page
3. Add an optional description
4. Click **Process**
5. Wait for processing to complete

#### Managing Documents

From the document list view, you can:
- **View Details**: Click on a document to view its metadata and content
- **View Chunks**: See how a document has been split into chunks
- **Delete**: Remove a document from the system
- **Query**: Ask questions specifically about this document

### Querying Documents

#### Basic Querying

1. Navigate to the **Query** page
2. Enter your question in the input field
3. Click **Ask** or press Enter
4. View the answer, along with source documents and context

#### Advanced Querying Options

- **Collection Selection**: Choose which document collections to search
- **Document Filter**: Limit the search to specific document types
- **Document-Specific Query**: Ask questions about a specific document
- **Response Format**: Choose between concise or detailed responses

### Data Source Management

#### Adding Data Sources

1. Navigate to **Settings** > **Data Sources**
2. Click **Add Data Source**
3. Select the source type (file system, database, website, API)
4. Configure connection details
5. Set sync schedule (if applicable)
6. Click **Save**

#### Managing Data Sources

- **Enable/Disable**: Toggle a data source active state
- **Manual Sync**: Trigger immediate synchronization
- **Edit**: Modify data source configuration
- **Delete**: Remove a data source

## Command-Line Interface

For power users, the system provides a CLI for common operations.

### Installation

```bash
pip install rag-cli
```

### Basic Commands

```bash
# Upload a document
rag-cli upload /path/to/document.pdf --description "Annual Report 2023"

# Query the system
rag-cli query "What is our revenue forecast for 2024?"

# List documents
rag-cli list-documents

# Delete a document
rag-cli delete-document document_id

# Check system status
rag-cli health
```

## API Usage

The system provides a comprehensive REST API for integration with other applications.

### Authentication

```bash
curl -H "X-API-Key: your-api-key-here" http://localhost:8000/api/v1/health
```

### Common API Operations

```bash
# Upload a document
curl -X POST -H "X-API-Key: your-api-key" \
  -F "file=@document.pdf" \
  -F "description=Annual Report 2023" \
  http://localhost:8000/api/v1/documents/upload

# Query the system
curl -X POST -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our revenue forecast for 2024?"}' \
  http://localhost:8000/api/v1/query/generate

# List documents
curl -H "X-API-Key: your-api-key" \
  http://localhost:8000/api/v1/documents
```

For more detailed API information, see the [API Reference](../api-reference/).

## Advanced Features

### Structured Data Extraction

Extract specific data points from unstructured documents:

1. Navigate to **Tools** > **Structured Extraction**
2. Select the document
3. Define the extraction schema (e.g., `{"title": "string", "author": "string", "date": "date"}`)
4. Click **Extract**
5. View and export the extracted data

### Batch Processing

For large document sets:

1. Place documents in a designated watch folder
2. The system will automatically process new files
3. Check the processing status in the dashboard
4. View batch processing logs for details

### Advanced Querying Techniques

- **Use quotes** for exact phrase matching: `"quarterly revenue for Q2 2023"`
- **Boolean operators**: `budget AND forecast NOT preliminary`
- **Filtering by date**: `documents from:2023-01-01 to:2023-12-31`
- **Filtering by type**: `type:pdf quarterly reports`
- **Document-specific**: `docid:abc123 executive summary`

## Best Practices

### Document Preparation

For optimal results:
- Ensure documents are text-searchable (OCR scanned documents if needed)
- Use consistent formatting for similar document types
- Include relevant metadata in document titles and descriptions
- Split very large documents (100+ pages) into logical sections

### Query Formulation

For better answers:
- Be specific in your questions
- Provide context when needed
- Use complete sentences rather than keywords
- Start with broader questions and then refine
- Reference specific document types if you know where the answer might be

### System Maintenance

Periodic maintenance tasks:
- **Purge Unnecessary Documents**: Remove outdated or irrelevant documents
- **Update Data Sources**: Keep external data sources current
- **Monitor Performance**: Check query response times and adjust settings if needed
- **Review Logs**: Periodically check system logs for issues
- **Backup Configuration**: Regularly backup system configuration and data