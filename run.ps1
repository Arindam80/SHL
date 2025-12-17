# SHL Assessment Recommendation System - Quick Start
# Run this script to set up and start the system

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SHL Assessment Recommendation System" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check if data exists
Write-Host "`nChecking data files..." -ForegroundColor Yellow
$dataExists = Test-Path "data\embeddings\faiss.index"

if (-not $dataExists) {
    Write-Host "⚠️  Data not found. Building from scratch..." -ForegroundColor Yellow
    
    Write-Host "`n  1/3 Scraping SHL assessments..." -ForegroundColor Cyan
    python src\scraper.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Scraping failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  2/3 Processing data..." -ForegroundColor Cyan
    python src\data_pipeline.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Data processing failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  3/3 Generating embeddings..." -ForegroundColor Cyan
    python src\embeddings.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Embedding generation failed" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "`n✓ Data build complete!" -ForegroundColor Green
} else {
    Write-Host "✓ Data files found" -ForegroundColor Green
}

# Start the server
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Starting server on http://localhost:5000" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

python start.py
