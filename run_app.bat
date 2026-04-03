@echo off
REM Seven Star Startup - Run Application (Windows)
REM This script sets up the environment and launches the Streamlit app

color 0A
title Seven Star Startup - Investment Marketplace

echo.
echo ====================================================
echo   Seven Star Startup - Open Source Investment 
echo   Marketplace
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -q -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
)

echo.
echo Starting Seven Star Startup...
echo.
echo The app will open in your default browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run the Streamlit app
python -m streamlit run app.py

pause
