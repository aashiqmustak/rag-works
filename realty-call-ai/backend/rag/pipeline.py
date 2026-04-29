"""
RAG pipeline with FAISS for property retrieval
"""
import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import faiss
from sentence_transformers import SentenceTransformer
from models.schemas import PropertyListing
from utils.logger import setup_logger
from models.config import settings

logger = setup_logger(__name__)


class RAGPipeline:
    """RAG pipeline for property retrieval using FAISS"""
    
    def __init__(self, index_path: str = None):
        """Initialize RAG pipeline"""
        self.index_path = index_path or settings.faiss_index_path
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.index = None
        self.properties = []
        self.property_metadata = {}
        self._ensure_index_dir()
        self._load_or_create_index()
    
    def _ensure_index_dir(self):
        """Ensure index directory exists"""
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _load_or_create_index(self):
        """Load existing index or create new one"""
        index_file = f"{self.index_path}.index"
        metadata_file = f"{self.index_path}.json"
        
        if os.path.exists(index_file) and os.path.exists(metadata_file):
            try:
                self.index = faiss.read_index(index_file)
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    self.properties = data['properties']
                    self.property_metadata = data['metadata']
                logger.info(f"Loaded FAISS index with {len(self.properties)} properties")
            except Exception as e:
                logger.error(f"Error loading index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create new FAISS index"""
        embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.properties = []
        self.property_metadata = {}
        logger.info("Created new FAISS index")
    
    def add_properties(self, properties: List[PropertyListing]):
        """Add properties to the index"""
        for prop in properties:
            # Create rich text for embedding
            text = f"""
            Property: {prop.title}
            Type: {prop.property_type}
            Location: {prop.location}
            Price: {prop.price}
            Description: {prop.description}
            Bedrooms: {prop.bedrooms}
            Bathrooms: {prop.bathrooms}
            Area: {prop.area_sqft}
            Amenities: {', '.join(prop.amenities)}
            """
            
            # Generate embedding
            embedding = self.embedding_model.encode(text, convert_to_numpy=True)
            
            # Add to FAISS index
            self.index.add(np.array([embedding]))
            
            # Store metadata
            self.properties.append(prop.model_dump())
            self.property_metadata[prop.id] = {
                'title': prop.title,
                'price': prop.price,
                'location': prop.location
            }
        
        # Save index
        self._save_index()
        logger.info(f"Added {len(properties)} properties to index")
    
    def _save_index(self):
        """Save index to disk"""
        try:
            index_file = f"{self.index_path}.index"
            metadata_file = f"{self.index_path}.json"
            
            faiss.write_index(self.index, index_file)
            
            with open(metadata_file, 'w') as f:
                json.dump({
                    'properties': self.properties,
                    'metadata': self.property_metadata
                }, f)
            
            logger.info("FAISS index saved to disk")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def search(self, query: str, top_k: int = 5) -> Tuple[List[PropertyListing], List[float]]:
        """Search for properties"""
        if self.index.ntotal == 0:
            return [], []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query, convert_to_numpy=True)
        
        # Search
        distances, indices = self.index.search(
            np.array([query_embedding]), 
            min(top_k, self.index.ntotal)
        )
        
        results = []
        scores = []
        
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.properties):
                prop_dict = self.properties[idx]
                prop = PropertyListing(**prop_dict)
                results.append(prop)
                
                # Convert distance to similarity score (0-1)
                similarity = 1 / (1 + distance)
                scores.append(float(similarity))
        
        return results, scores
    
    def search_by_filters(self, 
                         filters: Dict) -> List[PropertyListing]:
        """Search properties by filters"""
        results = []
        
        for prop_dict in self.properties:
            prop = PropertyListing(**prop_dict)
            
            # Apply filters
            if 'property_type' in filters and prop.property_type != filters['property_type']:
                continue
            
            if 'min_price' in filters and prop.price < filters['min_price']:
                continue
            
            if 'max_price' in filters and prop.price > filters['max_price']:
                continue
            
            if 'location' in filters and filters['location'].lower() not in prop.location.lower():
                continue
            
            if 'min_bedrooms' in filters and prop.bedrooms < filters['min_bedrooms']:
                continue
            
            if 'max_bedrooms' in filters and prop.bedrooms > filters['max_bedrooms']:
                continue
            
            results.append(prop)
        
        return results
    
    def clear_index(self):
        """Clear the index"""
        self.index = None
        self.properties = []
        self.property_metadata = {}
        self._create_new_index()
        self._save_index()
        logger.info("FAISS index cleared")


# Global RAG instance
rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline"""
    global rag_pipeline
    if rag_pipeline is None:
        rag_pipeline = RAGPipeline()
    return rag_pipeline
