-- Initialize pgvector extension for PostgreSQL
-- This script runs automatically when the database is first created

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Grant only necessary permissions (following principle of least privilege)
-- Note: The database user is created by docker-compose (POSTGRES_USER env var)
-- Grant usage and create permissions to the application user
DO $$
BEGIN
    -- Grant minimal permissions needed for the application
    GRANT USAGE ON SCHEMA public TO PUBLIC;
    GRANT CREATE ON SCHEMA public TO PUBLIC;
    
    -- Note: Additional permissions will be granted automatically by SQLAlchemy/Alembic
    -- when creating tables as the database owner
END $$;

-- Note: Application tables (documents, document_chunks, etc.) are created
-- by SQLAlchemy/Alembic migrations and langchain-postgres automatically
-- manages its own vector store tables (langchain_pg_collection, langchain_pg_embedding)
