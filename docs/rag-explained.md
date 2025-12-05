---
layout: default
title: RAG Explained
nav_order: 5
permalink: /rag-explained/
---

# RAG Explained: How It Works
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This document provides a detailed explanation of how Retrieval-Augmented Generation (RAG) works in this system, from document ingestion to query answering.

## What is RAG?

Retrieval-Augmented Generation (RAG) is an approach that combines the power of large language models (LLMs) with a retrieval system that fetches relevant information from a knowledge base. This allows the system to:

1. Generate responses based on external, up-to-date information
2. Reduce hallucinations by grounding responses in source documents
3. Provide citations and references for generated content
4. Customize answers to your specific document set

## The RAG Pipeline

Our implementation follows this pipeline:

1. **Document Processing**: Convert documents to a format suitable for retrieval
2. **Indexing**: Create vector embeddings for efficient semantic search
3. **Querying**: Find relevant document chunks for a given query
4. **Context Assembly**: Combine retrieved information into a coherent context
5. **Response Generation**: Generate a natural language response using the context

## Document Processing

Before documents can be used in the RAG system, they go through these steps:

### 1. Text Extraction

The system uses document parsers (based on document type) to extract text:
- PDF files: Text extraction with layout preservation
- Word documents: Text extraction maintaining structure
- Images: OCR processing for text recognition
- Web pages: HTML parsing to extract meaningful content
- Databases: SQL query results structured into text

### 2. Chunking

Long documents are split into smaller, manageable chunks:
- Text is split into chunks of configurable size (default: ~1000 characters)
- Chunks maintain semantic coherence (avoid splitting mid-sentence)
- Overlap between chunks helps maintain context (~10% overlap by default)
- Metadata is preserved for each chunk (source, position, etc.)

### 3. Embedding Generation

Each chunk is converted into a vector embedding:
- The system uses OpenAI's embedding models by default (text-embedding-3-small)
- Alternatively, it can use Azure OpenAI or local models (HuggingFace)
- These embeddings capture the semantic meaning of the text
- Typical embedding dimensions: 1536 for text-embedding-3-small

### 4. Storage

Embeddings and chunks are stored in PostgreSQL:
- **Database**: Stores document metadata, chunk text, and vector embeddings
- **PGVector**: PostgreSQL extension enabling efficient vector similarity search

## Retrieval Process

When a user submits a query, the system performs these steps:

### 1. Query Embedding

The query is converted to a vector embedding using the same embedding model that processed the documents.

### 2. Vector Similarity Search

The system searches for document chunks with similar embeddings:
- PGVector performs a similarity search using cosine similarity
- Results are ranked by relevance (closest vectors)
- Optional filters can narrow search by metadata (document ID, type, etc.)

### 3. Hybrid Search (Optional)

For better results, the system can combine:
- Vector similarity: Semantic understanding
- Keyword matching: Exact term matching
- Re-ranking: Adjusting results based on multiple factors

### 4. Document Filtering

Retrieved documents undergo optional filtering:
- Removing duplicates or near-duplicates
- Removing irrelevant content based on additional metrics
- Limiting the total context size to fit LLM context windows

## Context Assembly

The system builds a context from retrieved chunks:

1. Retrieved chunks are ordered based on:
   - Original document order (when from same document)
   - Relevance score (for chunks from different documents)

2. Chunks are formatted with source information:
   - Document title
   - Page/section information
   - URL/file reference
   
3. The assembled context is structured for LLM comprehension

## Response Generation

The final step uses an LLM to generate a response:

1. A prompt is constructed with:
   - The user's query
   - Assembled context
   - Instructions for response formatting
   - Guidelines for citing sources

2. The prompt is sent to the LLM (OpenAI's GPT models by default)

3. The LLM generates a response that:
   - Answers the query using information in the context
   - Provides citations to source documents
   - States when information is not available in the context

## Implementation Details

### Vector Store Implementation

Our system uses PostgreSQL with PGVector (via langchain-postgres) as the vector store:

```python
def search_with_score(
    self, 
    query: str,
    collection_name: str = "documents",
    filter: Optional[Dict[str, Any]] = None,
    k: int = 5
) -> List[tuple[Document, float]]:
    """Search for documents similar to the query and return with similarity scores"""
    collection = self.get_collection(collection_name)
    
    try:
        logger.info(f"Searching for '{query}' with scores in collection '{collection_name}'")
        return collection.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter
        )
    except Exception as e:
        logger.error(f"Error searching vector store with scores: {str(e)}")
        raise
```

### Retriever Implementation

The RAGRetriever class handles document retrieval:

```python
def retrieve_for_rag(
    self, 
    query: str,
    collection_names: Optional[List[str]] = None,
    filter_criteria: Optional[Dict[str, Any]] = None,
    document_id: Optional[str] = None,
    top_k: int = 5,
    db: Optional[Session] = None
) -> Dict[str, Any]:
    # ... 
    # Set default collection names if not provided
    # ...
    
    # If document_id is provided, add it to filter criteria
    if document_id:
        logger.info(f"Filtering by document ID: {document_id}")
        if not filter_criteria:
            filter_criteria = {}
        filter_criteria["document_id"] = document_id
    
    # Retrieve documents across collections
    # ...
    
    # Generate context from relevant documents
    context = self._generate_context(relevant_docs)
    
    return {
        "documents": relevant_docs,
        "context": context,
        "metrics": { ... }
    }
```

### Generator Implementation

The RAGGenerator handles response generation:

```python
def generate_response(
    self, 
    query: str,
    collection_names: List[str] = None,
    filter_criteria: Optional[Dict[str, Any]] = None,
    document_id: Optional[str] = None,
    db: Optional[Session] = None
) -> Dict[str, Any]:
    # ... 
    
    # Retrieve relevant context
    retrieval_result = rag_retriever.retrieve_for_rag(
        query=query,
        collection_names=collection_names,
        filter_criteria=filter_criteria,
        document_id=document_id,
        top_k=settings.MAX_RETRIEVED_DOCUMENTS,
        db=db
    )
    
    # Generate prompt and send to LLM
    prompt_template = self._create_prompt_template()
    prompt = prompt_template.format(context=context, query=query)
    
    # Call LLM and return response
    # ...
```

## Advanced Features

### Document-Specific Queries

The system allows querying against specific documents using the document ID:

```
POST /api/v1/query/document/{document_id}/query
```

This routes through a specialized endpoint that filters by document ID:

```python
@router.post("/document/{document_id}/query", response_model=QueryResponse)
async def query_specific_document(
    document_id: str,
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Query against a specific document by its ID
    """
    # Override any document_id in the request body with the one from the path
    request.document_id = document_id
    
    # Reuse the existing generate endpoint logic
    return await generate_answer(request, db)
```

### Query Optimization

To improve retrieval quality, the system:

1. Processes the query to extract key terms
2. Uses hybrid retrieval combining semantic and keyword search
3. Reranks results based on multiple relevance factors
4. Dynamically adjusts the number of retrieved documents based on query complexity

## Performance Considerations

For optimal RAG performance:

1. **Embedding Quality**: Choose appropriate embedding models for your domain
2. **Chunk Size**: Tune chunk size based on document types and query patterns
3. **Retrieval Parameters**: Adjust top-k and filtering based on precision/recall needs
4. **Context Window**: Balance between comprehensive context and LLM token limits
5. **Prompting Strategy**: Refine prompts for more accurate generation

## Troubleshooting Common Issues

1. **Poor Retrieval Quality**:
   - Check embedding model appropriateness
   - Review chunking strategy
   - Adjust similarity thresholds

2. **Slow Response Times**:
   - Optimize vector search (index settings)
   - Implement caching for frequent queries
   - Reduce context size

3. **Inconsistent Answers**:
   - Improve prompt engineering
   - Implement structured output enforcement
   - Add post-processing validation