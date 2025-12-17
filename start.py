"""
Startup script for SHL Assessment Recommendation System.
Checks if data is built, builds if necessary, then starts the server.
"""

import os
import sys
import subprocess


def check_data_exists():
    """Check if required data files exist."""
    required_files = [
        "data/raw/shl_assessments_raw.json",
        "data/processed/shl_assessments_clean.json",
        "data/embeddings/faiss.index",
        "data/embeddings/metadata.pkl"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            return False, file_path
    return True, None


def build_data():
    """Run scraper, data pipeline, and embeddings generation."""
    print("\n" + "="*60)
    print("Building data from scratch...")
    print("="*60 + "\n")
    
    steps = [
        ("Scraping SHL assessments", "python src/scraper.py"),
        ("Processing data", "python src/data_pipeline.py"),
        ("Generating embeddings", "python src/embeddings.py")
    ]
    
    for step_name, command in steps:
        print(f"\n📦 {step_name}...")
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(f"\n❌ Error during {step_name}")
            sys.exit(1)
        print(f"✓ {step_name} complete")
    
    print("\n" + "="*60)
    print("✓ Data build complete!")
    print("="*60 + "\n")


def start_server():
    """Start the FastAPI server."""
    port = os.getenv("PORT", "5000")
    print("\n" + "="*60)
    print(f"Starting SHL Recommendation System on port {port}...")
    print("="*60 + "\n")
    
    # Change to src directory to run api.py
    os.chdir("src")
    subprocess.run([sys.executable, "api.py"])


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SHL Assessment Recommendation System")
    print("="*60)
    
    # Check if data exists
    data_exists, missing_file = check_data_exists()
    
    if not data_exists:
        print(f"\n⚠️  Missing data file: {missing_file}")
        print("Building data from scratch...\n")
        build_data()
    else:
        print("\n✓ Data files found")
    
    # Start the server
    start_server()
