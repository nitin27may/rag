---
layout: default
title: Chunking Strategies
nav_order: 5
permalink: /chunking-strategies/
---

# Chunking Strategies
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This document explains the document chunking strategies available in the RAG system and how to configure them for optimal retrieval performance.

## What is Chunking?

Chunking is the process of splitting documents into smaller, manageable pieces (chunks) before generating embeddings and storing them in the vector database. Effective chunking is crucial for RAG systems because:

- **Better Retrieval**: Smaller, focused chunks lead to more precise semantic search results
- **Context Windows**: LLMs have token limits; chunks must fit within these constraints
- **Relevance**: Well-structured chunks ensure relevant context is retrieved for queries

## Available Strategies

The RAG system supports four chunking strategies:

| Strategy | Description | Best For |
|----------|-------------|----------|
| **recursive** | Splits text recursively using a hierarchy of separators | General-purpose documents |
| **semantic** | Splits based on semantic similarity using embeddings | Varied document types |
| **token** | Splits based on token count | LLM context optimization |
| **sentence** | Splits at sentence boundaries | NLP tasks, Q&A |

### 1. Recursive Character Text Splitting (Default)

The recursive strategy splits text using a hierarchy of separators, trying each in order until chunks are small enough.

**How it works:**
1. First tries to split on `\n\n` (paragraphs)
2. If chunks are still too large, splits on `\n` (lines)
3. Then splits on `. ` (sentences)
4. Finally splits on ` ` (words)
5. Last resort: splits on individual characters

**Configuration:**
```env
CHUNKING_STRATEGY=recursive
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

**Best for:**
- General documents (PDFs, Word docs, text files)
- Documents with clear paragraph structure
- Most use cases

### 2. Semantic Chunking

Semantic chunking uses embeddings to identify natural breakpoints in text based on semantic similarity. It groups semantically related content together.

**How it works:**
1. Generates embeddings for sentences/segments
2. Calculates similarity between adjacent segments
3. Identifies breakpoints where similarity drops significantly
4. Creates chunks at these natural semantic boundaries

**Configuration:**
```env
CHUNKING_STRATEGY=semantic
SEMANTIC_BREAKPOINT_TYPE=percentile
```

**Breakpoint Types:**
- `percentile`: Uses percentile threshold for similarity drops
- `standard_deviation`: Uses standard deviation to detect outliers
- `interquartile`: Uses interquartile range for breakpoint detection
- `gradient`: Uses gradient of similarity scores

**Best for:**
- Documents with flowing narrative
- Technical documentation
- Research papers
- Content where context preservation is critical

**Note:** Semantic chunking requires the embedding model to be configured and is slower than other strategies.

### 3. Token-Based Chunking

Token chunking splits text based on token count rather than character count, ensuring chunks fit within LLM context windows.

**How it works:**
1. Uses tiktoken to count tokens
2. Splits text to ensure each chunk has the specified number of tokens
3. Maintains overlap for context continuity

**Configuration:**
```env
CHUNKING_STRATEGY=token
CHUNK_SIZE=500  # Number of tokens, not characters
CHUNK_OVERLAP=50
```

**Best for:**
- When working with strict token limits
- Optimizing for specific LLM context windows
- Cost optimization (fewer tokens = lower API costs)

**Note:** Token chunking uses the configured `OPENAI_MODEL` or `AZURE_OPENAI_DEPLOYMENT` for tokenization.

### 4. Sentence-Based Chunking

Sentence chunking splits text at sentence boundaries while respecting token limits.

**How it works:**
1. Uses sentence transformers for sentence detection
2. Groups sentences into chunks
3. Ensures chunks don't exceed token limits

**Configuration:**
```env
CHUNKING_STRATEGY=sentence
CHUNK_SIZE=1000
CHUNK_OVERLAP=50
```

**Best for:**
- Q&A systems
- Documents with clear sentence structure
- Legal documents
- Content where sentence integrity is important

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHUNK_SIZE` | 1000 | Maximum size of each chunk (characters or tokens) |
| `CHUNK_OVERLAP` | 200 | Overlap between consecutive chunks |
| `CHUNKING_STRATEGY` | recursive | Strategy: recursive, semantic, token, sentence |
| `SEMANTIC_BREAKPOINT_TYPE` | percentile | Breakpoint type for semantic chunking |
| `MIN_CHUNK_SIZE` | 100 | Minimum chunk size (prevents tiny chunks) |

### Example Configurations

#### High-Precision Retrieval
```env
CHUNKING_STRATEGY=semantic
CHUNK_SIZE=500
CHUNK_OVERLAP=100
SEMANTIC_BREAKPOINT_TYPE=percentile
```

#### Cost-Optimized
```env
CHUNKING_STRATEGY=token
CHUNK_SIZE=256
CHUNK_OVERLAP=25
```

#### General Purpose (Default)
```env
CHUNKING_STRATEGY=recursive
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

#### Q&A Focused
```env
CHUNKING_STRATEGY=sentence
CHUNK_SIZE=800
CHUNK_OVERLAP=50
```

## Chunk Size Guidelines

Choosing the right chunk size depends on your use case:

| Chunk Size | Pros | Cons | Use Case |
|------------|------|------|----------|
| Small (256-500) | More precise retrieval | Less context per chunk | Specific Q&A |
| Medium (500-1000) | Balanced | Good default | General purpose |
| Large (1000-2000) | More context | Less precise | Summarization |

### Overlap Guidelines

- **10-20% of chunk size**: Good default for most cases
- **Higher overlap**: Better context continuity, more storage
- **Lower overlap**: Less redundancy, may lose context

## Provider-Specific Notes

### OpenAI

When using OpenAI as the LLM provider:
```env
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
```

The `OPENAI_MODEL` is used for token-based chunking tokenization.

### Azure OpenAI

When using Azure OpenAI:
```env
LLM_PROVIDER=azure
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

The system automatically maps Azure deployment names to tiktoken-compatible model names:
- `gpt-4o` / `gpt4o` → `gpt-4o`
- `gpt-4-turbo` / `gpt4-turbo` → `gpt-4-turbo`
- `gpt-4` / `gpt4` → `gpt-4`
- `gpt-35-turbo` / `gpt-3.5-turbo` → `gpt-3.5-turbo`

## Programmatic Usage

You can also create custom chunking configurations programmatically:

```python
from app.services.chunking_service import ChunkingService, ChunkingConfig

# Use default settings
chunking_service = ChunkingService()
chunks = chunking_service.split_text(text)

# Custom configuration
config = ChunkingConfig(
    chunk_size=500,
    chunk_overlap=50,
    strategy="semantic",
    breakpoint_threshold_type="percentile"
)
custom_service = ChunkingService(config)
chunks = custom_service.split_text(text)

# Factory method for specific strategy
token_service = ChunkingService.create_with_strategy(
    strategy="token",
    chunk_size=256,
    chunk_overlap=25
)
```

## Best Practices

1. **Start with defaults**: The recursive strategy with 1000/200 chunk/overlap works well for most cases

2. **Test with your data**: Different document types may benefit from different strategies

3. **Consider your queries**: If users ask specific questions, smaller chunks help; for summarization, larger chunks are better

4. **Monitor retrieval quality**: If retrieval results are poor, try adjusting chunk size or strategy

5. **Balance precision vs. context**: Smaller chunks = more precise, larger chunks = more context

6. **Use semantic chunking for complex documents**: When document structure varies, semantic chunking preserves context better

7. **Token chunking for cost optimization**: When API costs are a concern, token-based chunking ensures efficient use of context windows

## Troubleshooting

### Retrieval returns irrelevant results
- Try smaller chunk sizes
- Consider semantic chunking
- Increase overlap

### Lost context in responses
- Increase chunk size
- Increase overlap
- Try semantic chunking

### High API costs
- Use token-based chunking
- Reduce chunk size
- Reduce retrieved document count (`MAX_RETRIEVED_DOCUMENTS`)

### Slow processing
- Use recursive (fastest) instead of semantic
- Reduce chunk size for large documents

## API Reference

The chunking configuration can be inspected via the API:

```bash
# Get current chunking configuration
curl http://localhost:8080/api/v1/health
```

The response includes chunking configuration details in the system info.
