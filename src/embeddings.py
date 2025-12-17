"""
Embedding generation and FAISS vector database setup.
"""

import json
import os
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict
from tqdm import tqdm


class EmbeddingManager:
    """Manages embedding generation and vector database operations."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding manager.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.assessments = None
        
        print(f"✓ Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def load_assessments(self, filepath: str = "data/processed/shl_assessments_clean.json"):
        """Load processed assessment data."""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.assessments = json.load(f)
        
        print(f"✓ Loaded {len(self.assessments)} assessments")
        return self.assessments
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            batch_size: Batch size for encoding
            
        Returns:
            numpy array of embeddings
        """
        print(f"Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )
        
        print(f"✓ Generated embeddings with shape: {embeddings.shape}")
        return embeddings
    
    def build_faiss_index(self, embeddings: np.ndarray):
        """
        Build FAISS index for similarity search.
        
        Args:
            embeddings: numpy array of embeddings
        """
        print("Building FAISS index...")
        
        # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        print(f"✓ FAISS index built with {self.index.ntotal} vectors")
    
    def save_index(self, index_path: str = "data/embeddings/faiss.index",
                   metadata_path: str = "data/embeddings/metadata.pkl"):
        """Save FAISS index and metadata."""
        os.makedirs("data/embeddings", exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        print(f"✓ Saved FAISS index to {index_path}")
        
        # Save metadata
        metadata = {
            'assessments': self.assessments,
            'embedding_dim': self.embedding_dim,
            'model_name': 'all-MiniLM-L6-v2'
        }
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✓ Saved metadata to {metadata_path}")
    
    def load_index(self, index_path: str = "data/embeddings/faiss.index",
                   metadata_path: str = "data/embeddings/metadata.pkl"):
        """Load FAISS index and metadata."""
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        print(f"✓ Loaded FAISS index with {self.index.ntotal} vectors")
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        self.assessments = metadata['assessments']
        self.embedding_dim = metadata['embedding_dim']
        
        print(f"✓ Loaded metadata with {len(self.assessments)} assessments")
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Search for similar assessments given a query.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            List of assessment dictionaries with similarity scores
        """
        # Generate query embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype('float32')
        
        # Search in FAISS
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Prepare results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.assessments):
                assessment = self.assessments[idx].copy()
                assessment['similarity_score'] = float(score)
                results.append(assessment)
        
        return results


def main():
    """Main execution function."""
    print("=" * 60)
    print("SHL Embedding Generation & Vector Database Setup")
    print("=" * 60)
    
    # Initialize embedding manager
    manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
    
    # Load assessments
    assessments = manager.load_assessments()
    
    # Extract texts for embedding
    texts = [a['full_text'] for a in assessments]
    
    # Generate embeddings
    embeddings = manager.generate_embeddings(texts)
    
    # Build FAISS index
    manager.build_faiss_index(embeddings)
    
    # Save index and metadata
    manager.save_index()
    
    # Test search
    print("\n" + "=" * 60)
    print("Testing Search Functionality")
    print("=" * 60)
    
    test_query = "Need a Java developer with problem solving skills"
    print(f"Query: {test_query}")
    
    results = manager.search(test_query, top_k=5)
    
    print(f"\nTop 5 results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']} (score: {result['similarity_score']:.4f})")
        print(f"   Type: {result['test_type']}")
        print(f"   URL: {result['url']}")
    
    print("\n" + "=" * 60)
    print("✓ Embedding generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
