@echo off
REM SHL Assessment Recommendation System - Quick Start
REM Run this script to set up and start the system

echo.
echo ========================================
echo SHL Assessment Recommendation System
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    exit /b 1
)
echo ✓ Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Check if data exists
echo Checking data files...
if not exist "data\embeddings\faiss.index" (
    echo Warning: Data not found. Building from scratch...
    echo.
    
    echo   1/3 Scraping SHL assessments...
    python src\scraper.py
    if errorlevel 1 (
        echo Error: Scraping failed
        exit /b 1
    )
    
    echo   2/3 Processing data...
    python src\data_pipeline.py
    if errorlevel 1 (
        echo Error: Data processing failed
        exit /b 1
    )
    
    echo   3/3 Generating embeddings...
    python src\embeddings.py
    if errorlevel 1 (
        echo Error: Embedding generation failed
        exit /b 1
    )
    
    echo.
    echo ✓ Data build complete!
) else (
    echo ✓ Data files found
)
echo.

REM Start the server
echo ========================================
echo Starting server on http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python start.py
