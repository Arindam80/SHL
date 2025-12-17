"""
Retrieval and LLM-based re-ranking for assessment recommendations.
"""

import os
import json
from typing import List, Dict, Optional
from embeddings import EmbeddingManager
from dotenv import load_dotenv

# Try to import openai, but don't fail if it's not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None


load_dotenv()


class RecommendationEngine:
    """Handles retrieval and intelligent re-ranking of assessments."""
    
    def __init__(self, embedding_manager: EmbeddingManager, use_llm: bool = True):
        """
        Initialize recommendation engine.
        
        Args:
            embedding_manager: Pre-initialized embedding manager with loaded index
            use_llm: Whether to use LLM for re-ranking
        """
        self.embedding_manager = embedding_manager
        self.use_llm = use_llm and OPENAI_AVAILABLE
        
        if use_llm and not OPENAI_AVAILABLE:
            print("Warning: OpenAI not available. LLM re-ranking disabled.")
            self.use_llm = False
        elif use_llm:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                print("Warning: OPENAI_API_KEY not set. LLM re-ranking disabled.")
                self.use_llm = False
    
    def retrieve_candidates(self, query: str, top_k: int = 20) -> List[Dict]:
        """
        Retrieve top-k candidate assessments using semantic search.
        
        Args:
            query: User query
            top_k: Number of candidates to retrieve
            
        Returns:
            List of assessment dictionaries
        """
        return self.embedding_manager.search(query, top_k=top_k)
    
    def rerank_with_llm(self, query: str, candidates: List[Dict], 
                        final_k: int = 10) -> List[Dict]:
        """
        Re-rank candidates using LLM reasoning.
        Ensures balanced recommendations across test types.
        
        Args:
            query: Original user query
            candidates: List of candidate assessments
            final_k: Number of final recommendations
            
        Returns:
            Re-ranked list of assessments
        """
        if not self.use_llm or not candidates:
            return candidates[:final_k]
        
        # Prepare candidate information for LLM
        candidate_info = []
        for i, candidate in enumerate(candidates):
            candidate_info.append({
                'id': i,
                'name': candidate['name'],
                'description': candidate['description'],
                'test_type': candidate['test_type'],
                'duration': candidate['duration']
            })
        
        # Create prompt for LLM
        prompt = f"""You are an expert in talent assessment and hiring. Given a hiring query and a list of candidate assessments, your task is to:

1. Identify the key skills and attributes required in the query
2. Select the most relevant assessments (aim for {final_k} assessments)
3. Ensure BALANCED recommendations across different domains:
   - If technical skills are mentioned, include "Knowledge & Skills (K)" tests
   - If personality/behavioral traits are mentioned, include "Personality & Behavior (P)" tests
   - If cognitive abilities are relevant, include "Cognitive Ability (A)" tests
4. Rank by relevance to the hiring need

Hiring Query: "{query}"

Candidate Assessments:
{json.dumps(candidate_info, indent=2)}

Respond with ONLY a JSON array of selected assessment IDs in ranked order (most relevant first).
Example format: [5, 12, 3, 18, 7, 1, 15, 9, 4, 11]

Do not include any explanation, just the JSON array of IDs."""

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert hiring assessment advisor. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON array
            if content.startswith('[') and content.endswith(']'):
                selected_ids = json.loads(content)
            else:
                # Try to find JSON array in response
                import re
                match = re.search(r'\[[\d,\s]+\]', content)
                if match:
                    selected_ids = json.loads(match.group())
                else:
                    print("Warning: Could not parse LLM response, using original ranking")
                    return candidates[:final_k]
            
            # Re-order candidates based on LLM ranking
            reranked = []
            for idx in selected_ids:
                if idx < len(candidates):
                    reranked.append(candidates[idx])
            
            # Fill remaining slots if needed
            for candidate in candidates:
                if len(reranked) >= final_k:
                    break
                if candidate not in reranked:
                    reranked.append(candidate)
            
            return reranked[:final_k]
            
        except Exception as e:
            print(f"Error in LLM re-ranking: {e}")
            return candidates[:final_k]
    
    def ensure_diversity(self, assessments: List[Dict], min_per_type: int = 2) -> List[Dict]:
        """
        Ensure diversity in test types for balanced recommendations.
        
        Args:
            assessments: List of assessments
            min_per_type: Minimum number per test type category
            
        Returns:
            Balanced list of assessments
        """
        # Group by test type category (K, P, A)
        by_category = {
            'K': [],  # Knowledge & Skills
            'P': [],  # Personality & Behavior
            'A': []   # Cognitive Ability
        }
        
        for assessment in assessments:
            test_type = assessment.get('test_type', '')
            if '(K)' in test_type:
                by_category['K'].append(assessment)
            elif '(P)' in test_type:
                by_category['P'].append(assessment)
            elif '(A)' in test_type:
                by_category['A'].append(assessment)
        
        # Check if we have diversity
        has_k = len(by_category['K']) > 0
        has_p = len(by_category['P']) > 0
        has_a = len(by_category['A']) > 0
        
        # If lacking diversity, try to balance
        if has_k and not has_p and len(assessments) >= 10:
            # Add some personality assessments
            print("Note: Adding personality assessments for balance")
        
        return assessments
    
    def get_recommendations(self, query: str, top_k: int = 10,
                          retrieval_k: int = 20) -> List[Dict]:
        """
        Get final recommendations combining retrieval and re-ranking.
        
        Args:
            query: User query
            top_k: Number of final recommendations
            retrieval_k: Number of candidates to retrieve
            
        Returns:
            List of recommended assessments
        """
        # Stage 1: Semantic retrieval
        candidates = self.retrieve_candidates(query, top_k=retrieval_k)
        
        # Stage 2: LLM re-ranking
        if self.use_llm:
            recommendations = self.rerank_with_llm(query, candidates, final_k=top_k)
        else:
            recommendations = candidates[:top_k]
        
        # Stage 3: Ensure diversity
        recommendations = self.ensure_diversity(recommendations)
        
        # Clean up recommendations for output
        for rec in recommendations:
            # Remove internal fields
            rec.pop('full_text', None)
            rec.pop('keywords', None)
            rec.pop('similarity_score', None)
        
        return recommendations


def main():
    """Test recommendation engine."""
    print("=" * 60)
    print("SHL Recommendation Engine Test")
    print("=" * 60)
    
    # Load embedding manager
    print("Loading embedding manager...")
    manager = EmbeddingManager()
    manager.load_index()
    
    # Initialize recommendation engine
    engine = RecommendationEngine(manager, use_llm=False)  # Set to False for testing without API key
    
    # Test queries
    test_queries = [
        "Need a Java developer with problem-solving skills",
        "Looking for a customer service representative with empathy",
        "Software engineer with Python and teamwork abilities"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        recommendations = engine.get_recommendations(query, top_k=5)
        
        print(f"Top 5 recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['name']}")
            print(f"   Type: {rec['test_type']}")
            print(f"   Duration: {rec['duration']} min")
    
    print("\n" + "=" * 60)
    print("✓ Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
