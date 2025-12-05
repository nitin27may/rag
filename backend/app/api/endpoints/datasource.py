import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import DataSource
from app.schemas.schemas import DataSourceCreate, DataSourceResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=DataSourceResponse)
async def create_data_source(
    data_source: DataSourceCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new data source
    """
    try:
        # Check if a data source with the same name exists
        existing = db.query(DataSource).filter(DataSource.name == data_source.name).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Data source with name '{data_source.name}' already exists"
            )
        
        # Create data source
        db_data_source = DataSource(
            name=data_source.name,
            source_type=data_source.source_type,
            connection_details=data_source.connection_details
        )
        
        db.add(db_data_source)
        db.commit()
        db.refresh(db_data_source)
        
        return db_data_source
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error creating data source: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating data source: {str(e)}"
        )


@router.get("/", response_model=List[DataSourceResponse])
async def list_data_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all data sources
    """
    data_sources = db.query(DataSource).offset(skip).limit(limit).all()
    return data_sources


@router.get("/{data_source_id}", response_model=DataSourceResponse)
async def get_data_source(
    data_source_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific data source by ID
    """
    data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
    if not data_source:
        raise HTTPException(
            status_code=404,
            detail=f"Data source not found: {data_source_id}"
        )
    
    return data_source


@router.put("/{data_source_id}", response_model=DataSourceResponse)
async def update_data_source(
    data_source_id: str,
    data_source_update: DataSourceCreate,
    db: Session = Depends(get_db)
):
    """
    Update a data source
    """
    try:
        # Get the data source
        db_data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
        if not db_data_source:
            raise HTTPException(
                status_code=404,
                detail=f"Data source not found: {data_source_id}"
            )
        
        # Check if the name is being changed and if the new name already exists
        if (data_source_update.name != db_data_source.name and
            db.query(DataSource).filter(DataSource.name == data_source_update.name).first()):
            raise HTTPException(
                status_code=400,
                detail=f"Data source with name '{data_source_update.name}' already exists"
            )
        
        # Update data source
        db_data_source.name = data_source_update.name
        db_data_source.source_type = data_source_update.source_type
        db_data_source.connection_details = data_source_update.connection_details
        
        db.commit()
        db.refresh(db_data_source)
        
        return db_data_source
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error updating data source: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating data source: {str(e)}"
        )


@router.delete("/{data_source_id}")
async def delete_data_source(
    data_source_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a data source
    """
    try:
        # Get the data source
        data_source = db.query(DataSource).filter(DataSource.id == data_source_id).first()
        if not data_source:
            raise HTTPException(
                status_code=404,
                detail=f"Data source not found: {data_source_id}"
            )
        
        # Delete the data source
        db.delete(data_source)
        db.commit()
        
        return {"status": "success", "message": f"Data source {data_source_id} deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error deleting data source: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting data source: {str(e)}"
        )