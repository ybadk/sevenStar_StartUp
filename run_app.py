#!/usr/bin/env python
"""
Launcher script for Seven Star Startup Application

This script sets up the environment and launches the Streamlit app.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
app_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(app_dir))

# Set up environment
os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'false')


def main():
    """Launch the Streamlit application"""
    try:
        import streamlit.cli
        
        # Run Streamlit
        sys.argv = ['streamlit', 'run', str(app_dir / 'app.py')]
        streamlit.cli.main()
    except ImportError:
        print("Error: Streamlit not installed. Please install requirements:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching app: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
