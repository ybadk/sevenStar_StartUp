"""
Seven Star Startup - Open Source Investment Marketplace

A community-driven platform where corporate investors and individuals discover,
evaluate, and fund promising open-source projects while they're still on GitHub.

Author: Kgthatso Thooe
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Kgthatso Thooe"
__description__ = "Open Source Investment Marketplace"

from config import APP_CONFIG, INDUSTRIES, VIDEO_TYPES
from utils import (
    load_database,
    save_database,
    export_to_csv,
    export_to_json,
    get_repository_stats,
    get_industry_insights
)

__all__ = [
    'APP_CONFIG',
    'INDUSTRIES',
    'VIDEO_TYPES',
    'load_database',
    'save_database',
    'export_to_csv',
    'export_to_json',
    'get_repository_stats',
    'get_industry_insights'
]
