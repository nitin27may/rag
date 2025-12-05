---
layout: default
title: Troubleshooting
nav_order: 8
permalink: /troubleshooting/
---

# Troubleshooting Guide
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

This guide helps you diagnose and resolve common issues with the Comprehensive RAG System.

## Installation Issues

### Backend Installation Problems

#### Python Environment Issues

**Issue**: Error installing dependencies.
```
ERROR: Could not install packages due to an OSError: [WinError 5]
```

**Solution**:
- Run the command prompt or terminal as administrator
- Use a virtual environment
- Check for version conflicts in `requirements.txt`
- Try installing dependencies one by one

#### Database Connection Issues

**Issue**: Cannot connect to the database.
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Solutions**:
1. Verify the database is running
2. Check connection credentials in `.env`
3. Ensure the database exists
4. Check network connectivity and firewall settings
5. If using Docker, ensure services can communicate

#### PGVector Issues

**Issue**: Error with PGVector extension.
```
ERROR: extension "vector" does not exist
```

**Solutions**:
1. Ensure PostgreSQL has the pgvector extension installed
2. If using Docker, use `pgvector/pgvector:pg16` or similar image
3. Run `CREATE EXTENSION vector;` in PostgreSQL
4. Verify DATABASE_URL connection string is correct

### Frontend Installation Problems

**Issue**: Node.js package installation fails.

**Solutions**:
1. Clear npm cache: `npm cache clean --force`
2. Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
3. Check for Node.js version compatibility
4. Try using yarn: `yarn install`

**Issue**: Frontend can't connect to backend.

**Solutions**:
1. Verify API URL in `.env.local`
2. Check if backend server is running
3. Check for CORS issues in browser console
4. Verify network connectivity between services

## Document Processing Issues

### Upload Failures

**Issue**: Document upload fails.

**Solutions**:
1. Check file size (max: 50MB)
2. Verify the file format is supported
3. Check storage permissions
4. Verify MinIO/S3 connectivity
5. Check disk space

### Processing Errors

**Issue**: Document shows "Processing Error" status.

**Solutions**:
1. Check logs for specific error details
2. Verify document format is not corrupted
3. For PDFs: ensure they're not password-protected
4. For images: check they're not too low resolution for OCR
5. Try processing a simpler document to isolate the issue

**Issue**: Document processed but no content extracted.

**Solutions**:
1. Ensure document contains extractable text (not just images)
2. For image-based PDFs, OCR may have failed - check OCR settings
3. Verify the parser for the file type is working properly
4. Try a different format for the same document

### Vector Store Issues

**Issue**: Document indexed but not appearing in search results.

**Solutions**:
1. Verify document chunks were properly vectorized
2. Check if document ID filtering is working correctly
3. Try rebuilding the vector store index
4. Verify embedding model is working correctly

## Query Issues

### No Results Found

**Issue**: Queries return "I couldn't find any relevant information."

**Solutions**:
1. Verify documents have been properly indexed
2. Try simpler, more direct queries
3. Check if you're filtering to a specific collection that doesn't contain relevant documents
4. Verify vector search is working by checking logs

### Incorrect Answers

**Issue**: System provides answers that don't match document content.

**Solutions**:
1. Check that the vector search is retrieving relevant documents (review logs)
2. Adjust the number of retrieved documents (`top_k` parameter)
3. Verify prompt template is properly instructing the LLM
4. Try querying against a specific document with known content

### Slow Response Times

**Issue**: Queries take a long time to respond.

**Solutions**:
1. Check network latency between components
2. Reduce the number of documents being retrieved
3. Verify database and vector store performance
4. Monitor CPU/memory usage during queries
5. Consider upgrading hardware resources

## API Issues

### Authentication Errors

**Issue**: API returns 401 Unauthorized.

**Solutions**:
1. Verify API key is correct
2. Check if API key is being sent in the correct header
3. Verify API key hasn't expired
4. Check if there are IP restrictions

### Rate Limiting

**Issue**: API returns 429 Too Many Requests.

**Solutions**:
1. Implement request throttling in your client
2. Reduce request frequency
3. Batch operations when possible
4. Contact administrator for increased limits if needed

## WebSocket Issues

### Connection Problems

**Issue**: WebSocket connections fail or timeout.

**Solutions**:
1. Verify WebSocket server is running
2. Check for firewall blocking WebSocket traffic
3. Verify client WebSocket implementation
4. Check for proxy interference

![WebSocket Test](../screenshots/web-socket-test.png)

## System Health Issues

### Component Status Errors

**Issue**: Health check shows components in unhealthy state.

![Health Check](../screenshots/healthcheck.png)

**Solutions**:
1. Check specific component error messages in health check
2. Restart the affected component
3. Verify component configuration
4. Check logs for detailed error information

### Memory Issues

**Issue**: System crashes with out-of-memory errors.

**Solutions**:
1. Monitor memory usage with tools like `top` or Task Manager
2. Increase available memory
3. Optimize large document processing
4. Implement batching for large operations
5. Check for memory leaks in custom code

## Configuration Issues

### Environment Variables

**Issue**: System behaves unexpectedly due to configuration problems.

**Solutions**:
1. Verify all required environment variables are set
2. Check for typos in environment variable names
3. Ensure values are in the correct format
4. Restart services after changing environment variables

### LLM API Issues

**Issue**: LLM-related errors (OpenAI, Azure).

**Solutions**:
1. Check API key validity and quota
2. Verify network connectivity to API provider
3. Check for model availability/deprecation
4. Review prompt for token limit exceedance

## Docker Issues

### Container Startup Problems

**Issue**: Docker containers fail to start.

**Solutions**:
1. Check Docker logs: `docker-compose logs`
2. Verify port conflicts (`netstat -ano | findstr PORT`)
3. Check disk space for Docker volumes
4. Ensure Docker has enough resources allocated

### Container Communication Issues

**Issue**: Services in containers can't communicate.

**Solutions**:
1. Check Docker network configuration
2. Verify service names are used as hostnames
3. Check exposed ports and port mappings
4. Ensure containers are on the same network

## Backup and Recovery

### Data Loss Prevention

In case of data corruption or accidental deletion:

1. Regularly backup:
   - Database data
   - Vector store collections
   - Document storage
   - Configuration files

2. Recovery procedure:
   - Restore database from backup
   - Restore document files
   - Rebuild vector indices if necessary

## Getting Support

If you still face issues after trying these solutions:

1. Check detailed logs:
   - Backend: `logs/backend.log`
   - Frontend: Browser console
   - Docker: `docker-compose logs`

2. Enable debug logging:
   ```
   LOG_LEVEL=debug python run.py
   ```

3. Contact support with:
   - Detailed error description
   - System configuration
   - Relevant log snippets
   - Steps to reproduce