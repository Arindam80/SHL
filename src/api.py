"""
FastAPI backend for SHL Assessment Recommendation System.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from embeddings import EmbeddingManager
from retrieval import RecommendationEngine


# Initialize FastAPI app
app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="Intelligent recommendation system for SHL Individual Test Solutions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class RecommendationRequest(BaseModel):
    """Request model for recommendation endpoint."""
    query: str = Field(..., description="Hiring query, job description, or job URL")
    

class AssessmentResponse(BaseModel):
    """Response model for a single assessment."""
    url: str
    name: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    recommended_assessments: List[AssessmentResponse]


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str


# Global variables for model loading
embedding_manager = None
recommendation_engine = None


@app.on_event("startup")
async def startup_event():
    """Load models and indexes on startup."""
    global embedding_manager, recommendation_engine
    
    print("Loading embedding manager and FAISS index...")
    
    # Use specified model from environment
    model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_manager = EmbeddingManager(model_name=model_name)
    
    # Check if index exists (adjust path since we're in src directory)
    index_path = "../data/embeddings/faiss.index"
    metadata_path = "../data/embeddings/metadata.pkl"
    if os.path.exists(index_path):
        embedding_manager.load_index(index_path=index_path, metadata_path=metadata_path)
        print("✓ Loaded FAISS index successfully")
    else:
        print("Warning: FAISS index not found. Run embeddings.py first.")
        return
    
    # Initialize recommendation engine with LLM disabled by default (saves memory)
    use_llm = os.getenv("USE_LLM_RERANKING", "false").lower() == "true"
    recommendation_engine = RecommendationEngine(embedding_manager, use_llm=use_llm)
    
    if use_llm:
        print("✓ Recommendation engine initialized with LLM re-ranking")
    else:
        print("✓ Recommendation engine initialized (no LLM re-ranking)")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status message indicating service health
    """
    return {"status": "healthy"}


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get assessment recommendations based on query.
    
    Args:
        request: Contains the hiring query
        
    Returns:
        List of recommended assessments
    """
    if recommendation_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Service not ready. Models are still loading."
        )
    
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )
    
    try:
        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(
            query=request.query,
            top_k=10,
            retrieval_k=20
        )
        
        # Format response according to specification
        formatted_assessments = []
        for rec in recommendations:
            # Convert test_type string to list
            test_type_list = [rec['test_type']] if isinstance(rec['test_type'], str) else rec['test_type']
            
            assessment = AssessmentResponse(
                url=rec['url'],
                name=rec['name'],
                adaptive_support=rec['adaptive_support'],
                description=rec['description'],
                duration=rec['duration'],
                remote_support=rec['remote_support'],
                test_type=test_type_list
            )
            formatted_assessments.append(assessment)
        
        return RecommendationResponse(recommended_assessments=formatted_assessments)
    
    except Exception as e:
        print(f"Error processing recommendation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing recommendation: {str(e)}"
        )


@app.get("/api")
async def root():
    """API information endpoint."""
    return {
        "message": "SHL Assessment Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "recommend": "/recommend (POST)"
        }
    }


# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the frontend HTML."""
        index_path = os.path.join(frontend_path, "index.html")
        return FileResponse(index_path)


if __name__ == "__main__":
    # Run the API server
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
