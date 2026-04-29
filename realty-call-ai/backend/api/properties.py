"""
Property API endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict
import uuid
import json

from models.schemas import PropertyListing, PropertyQueryRequest, PropertyQueryResponse
from rag.pipeline import get_rag_pipeline
from utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/properties", tags=["properties"])

rag = get_rag_pipeline()


@router.post("/search")
async def search_properties(request: PropertyQueryRequest) -> PropertyQueryResponse:
    """Search for properties"""
    try:
        properties, scores = rag.search(request.query, request.filters or {}, request.top_k)
        
        return PropertyQueryResponse(
            results=properties,
            search_query=request.query,
            relevance_scores=scores
        )
    
    except Exception as e:
        logger.error(f"Error searching properties: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/filter")
async def filter_properties(filters: Dict) -> List[PropertyListing]:
    """Filter properties"""
    try:
        results = rag.search_by_filters(filters)
        return results
    
    except Exception as e:
        logger.error(f"Error filtering properties: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add")
async def add_property(property: PropertyListing) -> dict:
    """Add a property to the index"""
    try:
        if not property.id:
            property.id = str(uuid.uuid4())
        
        rag.add_properties([property])
        
        return {
            "status": "success",
            "property_id": property.id,
            "message": "Property added successfully"
        }
    
    except Exception as e:
        logger.error(f"Error adding property: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_properties(file: UploadFile = File(...)) -> dict:
    """Upload properties from JSON file"""
    try:
        content = await file.read()
        data = json.loads(content)
        
        # Handle both array and single object
        properties_data = data if isinstance(data, list) else [data]
        
        properties = [PropertyListing(**p) for p in properties_data]
        rag.add_properties(properties)
        
        return {
            "status": "success",
            "properties_loaded": len(properties),
            "message": f"Loaded {len(properties)} properties"
        }
    
    except Exception as e:
        logger.error(f"Error uploading properties: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/count")
async def get_property_count() -> dict:
    """Get total property count"""
    try:
        return {
            "total_properties": len(rag.properties),
            "index_size": rag.index.ntotal if rag.index else 0
        }
    
    except Exception as e:
        logger.error(f"Error getting count: {e}")
        raise HTTPException(status_code=500, detail=str(e))
