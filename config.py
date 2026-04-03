"""
Configuration module for Seven Star Startup Application
"""

from pathlib import Path
from datetime import datetime

# App directories
ROOT_DIR = Path(__file__).resolve().parents[2]
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
VIDEO_UPLOAD_DIR = DATA_DIR / "video_uploads"
VIDEO_REQUEST_DIR = DATA_DIR / "video_requests"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_REQUEST_DIR.mkdir(parents=True, exist_ok=True)

# Database file
DB_FILE = DATA_DIR / "database.json"

# Data sources
STARRED_FILES = [
    ROOT_DIR / 'starred_repos.txt',
    ROOT_DIR / 'starred_repos_2.txt',
    ROOT_DIR / 'starred_repos_3.txt'
]

# App configuration
APP_CONFIG = {
    'name': 'Seven Star Startup',
    'version': '1.0.0',
    'description': 'Open Source Investment Marketplace',
    'creator': 'Kgthatso Thooe',
    'auto_reload_timeout': 85,
    'max_video_size_mb': 500,
    'supported_video_formats': ['mp4', 'mov', 'avi', 'mkv'],
    'supported_image_formats': ['jpg', 'png', 'jpeg', 'webp'],
}

# Industry categories
INDUSTRIES = [
    'AI/ML',
    'Media/Gaming',
    'Cybersecurity',
    'Cloud/DevOps',
    'Education',
    'Data Tools',
    'Web/UI',
    'Mobile',
    'Blockchain',
    'Finance',
    'Healthcare',
    'General Tech'
]

# Video type options
VIDEO_TYPES = [
    'Explainer',
    'Demo',
    'Tutorial',
    'Pitch',
    'Case Study',
    'Other'
]

# Rating scale
MIN_RATING = 0
MAX_RATING = 7

# Request status
REQUEST_STATUSES = ['pending', 'in_progress', 'completed', 'rejected']


def get_app_info():
    """Get application info dictionary"""
    return {
        'name': APP_CONFIG['name'],
        'version': APP_CONFIG['version'],
        'created_at': datetime.utcnow().isoformat(),
        'creator': APP_CONFIG['creator']
    }
