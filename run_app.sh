#!/bin/bash

# Seven Star Startup - Run Application (macOS/Linux)
# This script sets up the environment and launches the Streamlit app

clear

echo "===================================================="
echo "  Seven Star Startup - Open Source Investment"
echo "  Marketplace"
echo "===================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null ; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Using Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Checking dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi

echo ""
echo "Starting Seven Star Startup..."
echo ""
echo "The app will open in your default browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Streamlit app
streamlit run app.py
