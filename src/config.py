"""
Configuration settings for SHL Recommendation System.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Main configuration class."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Retrieval Settings
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "20"))
    FINAL_RECOMMENDATIONS = int(os.getenv("FINAL_RECOMMENDATIONS", "10"))
    
    # LLM Settings
    USE_LLM_RERANKING = OPENAI_API_KEY != ""
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500"))
    
    # File Paths
    DATA_RAW_DIR = "data/raw"
    DATA_PROCESSED_DIR = "data/processed"
    DATA_EMBEDDINGS_DIR = "data/embeddings"
    
    RAW_DATA_FILE = os.path.join(DATA_RAW_DIR, "shl_assessments_raw.json")
    PROCESSED_DATA_FILE = os.path.join(DATA_PROCESSED_DIR, "shl_assessments_clean.json")
    FAISS_INDEX_FILE = os.path.join(DATA_EMBEDDINGS_DIR, "faiss.index")
    METADATA_FILE = os.path.join(DATA_EMBEDDINGS_DIR, "metadata.pkl")
    
    TRAIN_DATASET = "datasets/train.json"
    TEST_DATASET = "datasets/test.json"
    PREDICTIONS_OUTPUT = "predictions.csv"
    
    # Scraping Settings
    SHL_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
    MIN_ASSESSMENTS = 377
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if cls.USE_LLM_RERANKING and not cls.OPENAI_API_KEY:
            print("Warning: LLM re-ranking enabled but OPENAI_API_KEY not set")
            cls.USE_LLM_RERANKING = False
        
        return True


# Validate on import
Config.validate()
