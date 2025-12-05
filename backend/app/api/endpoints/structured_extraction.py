import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import StructuredQueryRequest, StructuredQueryResponse
from app.services.structured_extraction import structured_data_extractor

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/structured-extract", response_model=StructuredQueryResponse)
async def extract_structured_data(
    request: StructuredQueryRequest,
    db: Session = Depends(get_db)
):
    """
    Extract structured data from a document based on a provided schema definition.
    
    This endpoint allows you to define a structured data schema and extract matching data
    from a document identified by its unique ID. The extracted data is returned in JSON format.
    
    Example schema definition:
    ```json
    {
        "document_id": "123e4567-e89b-12d3-a456-426614174000",
        "schema_definition": {
            "title": "string",
            "author": "string",
            "publication_date": "date",
            "abstract": "string",
            "keywords": "list",
            "sections": {
                "introduction": "string",
                "methodology": "string",
                "results": "string",
                "conclusion": "string"
            }
        }
    }
    ```
    
    The extraction strategy can be:
    - "auto" (default): Automatic selection of the best strategy
    - "template": Uses a prompt template for extraction
    - "pattern": Uses pattern matching for extraction
    
    You can also provide a custom prompt template to guide the extraction process.
    """
    try:
        # Call the extraction service
        result = structured_data_extractor.extract_structured_data(
            document_id=request.document_id,
            schema_definition=request.schema_definition,
            extraction_strategy=request.extraction_strategy,
            prompt_template=request.prompt_template,
            db=db
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error extracting structured data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting structured data: {str(e)}"
        )