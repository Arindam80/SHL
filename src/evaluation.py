"""
Evaluation metrics for recommendation system.
Implements Mean Recall@K for measuring retrieval quality.
"""

import json
from typing import List, Dict, Tuple
from embeddings import EmbeddingManager
from retrieval import RecommendationEngine


def load_train_dataset(filepath: str = "datasets/train.json") -> List[Dict]:
    """Load labeled training dataset."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def recall_at_k(predicted_urls: List[str], relevant_urls: List[str], k: int) -> float:
    """
    Calculate Recall@K for a single query.
    
    Recall@K = (Number of relevant items in top K) / (Total relevant items)
    
    Args:
        predicted_urls: List of predicted assessment URLs (ranked)
        relevant_urls: List of ground truth relevant URLs
        k: K value for recall calculation
        
    Returns:
        Recall@K score (0 to 1)
    """
    if not relevant_urls:
        return 0.0
    
    # Take top K predictions
    top_k_predictions = predicted_urls[:k]
    
    # Count how many relevant items are in top K
    relevant_found = len(set(top_k_predictions) & set(relevant_urls))
    
    # Calculate recall
    recall = relevant_found / len(relevant_urls)
    
    return recall


def mean_recall_at_k(predictions: List[List[str]], 
                     ground_truths: List[List[str]], 
                     k: int = 10) -> float:
    """
    Calculate Mean Recall@K across all queries.
    
    Args:
        predictions: List of predicted URL lists (one per query)
        ground_truths: List of relevant URL lists (one per query)
        k: K value for recall calculation
        
    Returns:
        Mean Recall@K score (0 to 1)
    """
    if len(predictions) != len(ground_truths):
        raise ValueError("Number of predictions must match number of ground truths")
    
    recalls = []
    for pred, truth in zip(predictions, ground_truths):
        recall = recall_at_k(pred, truth, k)
        recalls.append(recall)
    
    mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
    
    return mean_recall


def evaluate_system(engine: RecommendationEngine, 
                   train_data: List[Dict],
                   k: int = 10,
                   retrieval_k: int = 20) -> Tuple[float, List[Dict]]:
    """
    Evaluate recommendation system on training data.
    
    Args:
        engine: Recommendation engine
        train_data: Training dataset with queries and relevant URLs
        k: K value for recall calculation
        retrieval_k: Number of candidates to retrieve
        
    Returns:
        Tuple of (mean_recall_at_k, detailed_results)
    """
    predictions = []
    ground_truths = []
    detailed_results = []
    
    print(f"Evaluating system on {len(train_data)} queries...")
    print("=" * 60)
    
    for i, item in enumerate(train_data, 1):
        query = item['query']
        relevant_urls = item['relevant_urls']
        
        # Get recommendations
        recommendations = engine.get_recommendations(
            query, 
            top_k=k,
            retrieval_k=retrieval_k
        )
        
        # Extract predicted URLs
        predicted_urls = [rec['url'] for rec in recommendations]
        
        # Calculate recall for this query
        recall = recall_at_k(predicted_urls, relevant_urls, k)
        
        # Store results
        predictions.append(predicted_urls)
        ground_truths.append(relevant_urls)
        
        detailed_results.append({
            'query': query,
            'predicted_urls': predicted_urls,
            'relevant_urls': relevant_urls,
            'recall_at_k': recall,
            'relevant_found': len(set(predicted_urls) & set(relevant_urls)),
            'total_relevant': len(relevant_urls)
        })
        
        # Print progress
        print(f"Query {i}: {query}")
        print(f"  Recall@{k}: {recall:.4f} ({detailed_results[-1]['relevant_found']}/{detailed_results[-1]['total_relevant']} found)")
        
        # Show top 3 predictions
        print(f"  Top 3 predictions:")
        for j, url in enumerate(predicted_urls[:3], 1):
            is_relevant = "✓" if url in relevant_urls else "✗"
            # Extract assessment name from URL
            name = next((rec['name'] for rec in recommendations if rec['url'] == url), "Unknown")
            print(f"    {j}. [{is_relevant}] {name}")
        print()
    
    # Calculate mean recall
    mean_recall = mean_recall_at_k(predictions, ground_truths, k)
    
    print("=" * 60)
    print(f"Mean Recall@{k}: {mean_recall:.4f}")
    print("=" * 60)
    
    return mean_recall, detailed_results


def save_evaluation_results(mean_recall: float, 
                            detailed_results: List[Dict],
                            output_file: str = "experiments/evaluation_results.json"):
    """Save evaluation results to file."""
    import os
    os.makedirs("experiments", exist_ok=True)
    
    results = {
        'mean_recall_at_10': mean_recall,
        'detailed_results': detailed_results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved evaluation results to {output_file}")


def main():
    """Main evaluation function."""
    print("=" * 60)
    print("SHL Recommendation System Evaluation")
    print("=" * 60)
    print()
    
    # Load embedding manager and index
    print("Loading embedding manager...")
    manager = EmbeddingManager()
    manager.load_index()
    print()
    
    # Load training data
    print("Loading training dataset...")
    train_data = load_train_dataset()
    print(f"✓ Loaded {len(train_data)} labeled queries")
    print()
    
    # Baseline evaluation (no LLM re-ranking)
    print("=" * 60)
    print("BASELINE: Semantic Search Only")
    print("=" * 60)
    engine_baseline = RecommendationEngine(manager, use_llm=False)
    baseline_recall, baseline_results = evaluate_system(
        engine_baseline, 
        train_data, 
        k=10,
        retrieval_k=20
    )
    print()
    
    # Save baseline results
    save_evaluation_results(
        baseline_recall, 
        baseline_results,
        "experiments/baseline_results.json"
    )
    
    # Improved evaluation (with LLM re-ranking)
    print("\n" + "=" * 60)
    print("IMPROVED: Semantic Search + LLM Re-ranking")
    print("=" * 60)
    
    # Check if API key is available
    import os
    if os.getenv("OPENAI_API_KEY"):
        engine_improved = RecommendationEngine(manager, use_llm=True)
        improved_recall, improved_results = evaluate_system(
            engine_improved,
            train_data,
            k=10,
            retrieval_k=20
        )
        
        # Save improved results
        save_evaluation_results(
            improved_recall,
            improved_results,
            "experiments/improved_results.json"
        )
        
        # Print comparison
        print("\n" + "=" * 60)
        print("PERFORMANCE COMPARISON")
        print("=" * 60)
        print(f"Baseline Mean Recall@10:  {baseline_recall:.4f}")
        print(f"Improved Mean Recall@10:  {improved_recall:.4f}")
        print(f"Improvement: {improved_recall - baseline_recall:+.4f} ({(improved_recall - baseline_recall) / baseline_recall * 100:+.1f}%)")
        print("=" * 60)
    else:
        print("Note: OPENAI_API_KEY not set. Skipping LLM-based evaluation.")
        print("Using baseline results only.")
    
    print("\n✓ Evaluation complete!")


if __name__ == "__main__":
    main()
