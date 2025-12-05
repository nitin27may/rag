import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text
from io import StringIO

from langchain.schema import Document

from app.services.chunking_service import chunking_service

logger = logging.getLogger(__name__)

class DatabaseConnector:
    """Connector for retrieving data from databases"""
    
    def __init__(self):
        # Use centralized chunking service
        self.chunking_service = chunking_service
    
    def _create_engine(self, connection_string: str):
        """Create a SQLAlchemy engine for the database"""
        try:
            return create_engine(connection_string)
        except Exception as e:
            logger.error(f"Error creating database engine: {str(e)}")
            raise
    
    def execute_query(
        self, 
        connection_string: str, 
        query: str
    ) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a DataFrame
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            
        Returns:
            Pandas DataFrame with query results
        """
        try:
            logger.info(f"Executing query on database")
            
            engine = self._create_engine(connection_string)
            
            # Execute query and get results
            with engine.connect() as connection:
                result = connection.execute(text(query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            return df
        
        except Exception as e:
            logger.error(f"Error executing database query: {str(e)}")
            raise
    
    def get_table_schema(
        self, 
        connection_string: str, 
        table_name: str
    ) -> Dict[str, Any]:
        """
        Get schema information for a table
        
        Args:
            connection_string: Database connection string
            table_name: Name of the table
            
        Returns:
            Dictionary with table schema information
        """
        try:
            logger.info(f"Getting schema for table: {table_name}")
            
            engine = self._create_engine(connection_string)
            
            # Execute query to get table schema
            schema_query = f"""
            SELECT 
                column_name, 
                data_type, 
                character_maximum_length, 
                is_nullable
            FROM 
                information_schema.columns
            WHERE 
                table_name = '{table_name}'
            ORDER BY 
                ordinal_position
            """
            
            with engine.connect() as connection:
                result = connection.execute(text(schema_query))
                columns = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            return {
                "table_name": table_name,
                "columns": columns.to_dict(orient="records")
            }
        
        except Exception as e:
            logger.error(f"Error getting table schema: {str(e)}")
            raise
    
    def list_tables(
        self, 
        connection_string: str
    ) -> List[str]:
        """
        List all tables in the database
        
        Args:
            connection_string: Database connection string
            
        Returns:
            List of table names
        """
        try:
            logger.info(f"Listing tables in database")
            
            engine = self._create_engine(connection_string)
            
            # Query depends on database type
            if "postgresql" in connection_string:
                query = """
                SELECT 
                    table_name 
                FROM 
                    information_schema.tables 
                WHERE 
                    table_schema = 'public'
                ORDER BY 
                    table_name
                """
            elif "mysql" in connection_string:
                query = """
                SELECT 
                    table_name 
                FROM 
                    information_schema.tables 
                WHERE 
                    table_schema = DATABASE()
                ORDER BY 
                    table_name
                """
            elif "sqlite" in connection_string:
                query = """
                SELECT 
                    name AS table_name 
                FROM 
                    sqlite_master 
                WHERE 
                    type = 'table'
                ORDER BY 
                    name
                """
            else:
                raise ValueError(f"Unsupported database type in connection string: {connection_string}")
            
            with engine.connect() as connection:
                result = connection.execute(text(query))
                tables = [row[0] for row in result]
            
            return tables
        
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            raise
    
    def data_to_documents(
        self, 
        df: pd.DataFrame, 
        source_info: Dict[str, Any]
    ) -> List[Document]:
        """
        Convert DataFrame to Document objects
        
        Args:
            df: DataFrame with data
            source_info: Dictionary with source information
            
        Returns:
            List of Document objects
        """
        documents = []
        
        # Strategy 1: Convert the entire DataFrame to a string representation
        if len(df) <= 50:  # For small DataFrames, include the full table
            full_text = df.to_string(index=False)
            
            metadata = {
                "source_type": "database",
                "representation": "full_table",
                **source_info
            }
            
            documents.append(Document(
                page_content=full_text,
                metadata=metadata
            ))
        
        # Strategy 2: Process in batches for large tables
        batch_size = 20
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            
            batch_text = batch.to_string(index=False)
            
            metadata = {
                "source_type": "database",
                "representation": "batch",
                "row_range": f"{i}-{min(i+batch_size-1, len(df)-1)}",
                **source_info
            }
            
            documents.append(Document(
                page_content=batch_text,
                metadata=metadata
            ))
        
        # Strategy 3: Include column descriptions
        column_text = "Table columns:\n"
        for column in df.columns:
            sample_values = df[column].dropna().sample(min(3, len(df))).tolist()
            sample_text = ", ".join([str(val) for val in sample_values])
            column_text += f"- {column}: Sample values: {sample_text}\n"
        
        metadata = {
            "source_type": "database",
            "representation": "columns",
            **source_info
        }
        
        documents.append(Document(
            page_content=column_text,
            metadata=metadata
        ))
        
        # Split documents if they're too large
        result = []
        for doc in documents:
            result.extend(self.chunking_service.split_documents([doc]))
        
        return result


# Singleton instance
database_connector = DatabaseConnector()