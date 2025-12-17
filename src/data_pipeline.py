"""
Data pipeline for cleaning and structuring SHL assessment data.
"""

import json
import os
import pandas as pd
from typing import List, Dict
from url_mapper import update_assessment_urls


def load_raw_data() -> List[Dict]:
    """Load raw scraped assessment data."""
    input_path = "data/raw/shl_assessments_raw.json"
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update URLs to match real SHL product catalog
    data = update_assessment_urls(data)
    
    print(f"✓ Loaded {len(data)} raw assessments (URLs mapped to real catalog)")
    return data


def clean_assessment_data(assessments: List[Dict]) -> pd.DataFrame:
    """
    Clean and validate assessment data.
    - Remove duplicates
    - Validate required fields
    - Normalize text fields
    - Handle missing values
    """
    df = pd.DataFrame(assessments)
    
    print(f"Initial records: {len(df)}")
    
    # Remove duplicates based on URL
    df = df.drop_duplicates(subset=['url'], keep='first')
    print(f"After removing duplicates: {len(df)}")
    
    # Validate required fields
    required_fields = ['name', 'url', 'description', 'test_type', 'adaptive_support', 'remote_support', 'duration']
    for field in required_fields:
        if field not in df.columns:
            raise ValueError(f"Missing required field: {field}")
    
    # Remove rows with missing critical data
    df = df.dropna(subset=['name', 'url', 'description'])
    print(f"After removing incomplete records: {len(df)}")
    
    # Normalize text fields
    df['name'] = df['name'].str.strip()
    df['description'] = df['description'].str.strip()
    
    # Ensure duration is integer
    df['duration'] = df['duration'].fillna(30).astype(int)
    
    # Normalize Yes/No fields
    df['adaptive_support'] = df['adaptive_support'].fillna('No')
    df['remote_support'] = df['remote_support'].fillna('Yes')
    
    # Create full text for embedding (combines all relevant fields)
    df['full_text'] = (
        df['name'] + '. ' +
        df['description'] + '. ' +
        'Test type: ' + df['test_type'] + '. ' +
        'Duration: ' + df['duration'].astype(str) + ' minutes.'
    )
    
    # Create searchable keywords (lowercase for matching)
    df['keywords'] = df['full_text'].str.lower()
    
    print(f"✓ Cleaned data: {len(df)} valid assessments")
    return df


def save_processed_data(df: pd.DataFrame):
    """Save processed data to JSON and CSV."""
    os.makedirs("data/processed", exist_ok=True)
    
    # Save as JSON (preserves structure for API)
    json_path = "data/processed/shl_assessments_clean.json"
    df.to_json(json_path, orient='records', indent=2, force_ascii=False)
    print(f"✓ Saved to {json_path}")
    
    # Save as CSV (easy viewing)
    csv_path = "data/processed/shl_assessments_clean.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"✓ Saved to {csv_path}")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Dataset Statistics:")
    print("=" * 60)
    print(f"Total assessments: {len(df)}")
    print(f"\nBy test type:")
    print(df['test_type'].value_counts())
    print(f"\nAdaptive support:")
    print(df['adaptive_support'].value_counts())
    print(f"\nRemote support:")
    print(df['remote_support'].value_counts())
    print(f"\nDuration range: {df['duration'].min()}-{df['duration'].max()} minutes")
    print(f"Average duration: {df['duration'].mean():.1f} minutes")
    print("=" * 60)


def main():
    """Main execution function."""
    print("=" * 60)
    print("SHL Data Pipeline")
    print("=" * 60)
    
    # Load raw data
    raw_data = load_raw_data()
    
    # Clean and structure data
    clean_df = clean_assessment_data(raw_data)
    
    # Save processed data
    save_processed_data(clean_df)
    
    print("\n✓ Data pipeline complete!")


if __name__ == "__main__":
    main()
