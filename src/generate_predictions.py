"""
Generate predictions for test dataset and output to CSV.
"""

import json
import csv
from embeddings import EmbeddingManager
from retrieval import RecommendationEngine


def load_test_dataset(filepath: str = "datasets/test.json"):
    """Load unlabeled test dataset."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def generate_predictions(engine: RecommendationEngine, test_data: list, top_k: int = 10):
    """
    Generate predictions for test dataset.
    
    Args:
        engine: Recommendation engine
        test_data: List of test queries
        top_k: Number of recommendations per query
        
    Returns:
        List of (query, url) tuples
    """
    predictions = []
    
    print(f"Generating predictions for {len(test_data)} test queries...")
    print("=" * 60)
    
    for i, item in enumerate(test_data, 1):
        query = item['query']
        
        print(f"\nQuery {i}: {query}")
        
        # Get recommendations
        recommendations = engine.get_recommendations(
            query,
            top_k=top_k,
            retrieval_k=20
        )
        
        # Add each recommendation as a separate row
        for rec in recommendations:
            predictions.append((query, rec['url']))
        
        print(f"  Generated {len(recommendations)} recommendations")
    
    print("\n" + "=" * 60)
    print(f"Total predictions: {len(predictions)}")
    print("=" * 60)
    
    return predictions


def save_predictions_to_csv(predictions: list, output_file: str = "predictions.csv"):
    """
    Save predictions to CSV in the required format.
    
    Format:
    Query,Assessment_url
    
    Args:
        predictions: List of (query, url) tuples
        output_file: Output CSV file path
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(['Query', 'Assessment_url'])
        
        # Write predictions
        for query, url in predictions:
            writer.writerow([query, url])
    
    print(f"✓ Saved {len(predictions)} predictions to {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("SHL Test Dataset Prediction Generator")
    print("=" * 60)
    print()
    
    # Load embedding manager and index
    print("Loading embedding manager...")
    manager = EmbeddingManager()
    manager.load_index()
    print()
    
    # Initialize recommendation engine
    import os
    use_llm = bool(os.getenv("OPENAI_API_KEY"))
    engine = RecommendationEngine(manager, use_llm=use_llm)
    
    if use_llm:
        print("✓ Using LLM re-ranking for predictions")
    else:
        print("✓ Using semantic search only (no LLM)")
    print()
    
    # Load test dataset
    test_data = load_test_dataset()
    
    # Generate predictions
    predictions = generate_predictions(engine, test_data, top_k=10)
    
    # Save to CSV
    save_predictions_to_csv(predictions)
    
    print("\n✓ Prediction generation complete!")


if __name__ == "__main__":
    main()
