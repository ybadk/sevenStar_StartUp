"""
Utility functions for Seven Star Startup Application
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import pandas as pd
from config import DB_FILE, INDUSTRIES


def load_database():
    """Load database from JSON file or create new one"""
    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except Exception as e:
            print(f"Error loading database: {e}")
            data = {}
    else:
        data = {}

    # Ensure required keys exist
    if 'repos' not in data:
        data['repos'] = {}
    if 'video_uploads' not in data:
        data['video_uploads'] = []
    if 'video_requests' not in data:
        data['video_requests'] = []
    
    return data


def save_database(data):
    """Save database to JSON file"""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving database: {e}")
        return False


def export_to_csv(data, export_path=None):
    """Export repository data to CSV format"""
    if export_path is None:
        export_path = Path(DB_FILE.parent) / f"repos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    repos = data.get('repos', {})
    if not repos:
        return None
    
    try:
        with open(export_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'name', 'owner', 'repo', 'description', 'industry',
                         'stars', 'app_stars', 'user_rating', 'github_url', 'source', 'created_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for repo_id, repo_data in repos.items():
                row = {field: repo_data.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        return str(export_path)
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return None


def export_to_json(data, export_path=None):
    """Export all data to JSON format"""
    if export_path is None:
        export_path = Path(DB_FILE.parent) / f"full_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(export_path)
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return None


def get_repository_stats(data):
    """Calculate statistics about repositories"""
    repos = list(data.get('repos', {}).values())
    
    if not repos:
        return {}
    
    df = pd.DataFrame(repos)
    
    stats = {
        'total_repos': len(repos),
        'unique_industries': len(df['industry'].unique()),
        'avg_stars': float(df['stars'].mean()) if 'stars' in df.columns else 0,
        'avg_rating': float(df['user_rating'].dropna().mean()) if 'user_rating' in df.columns else 0,
        'total_app_stars': int(df['app_stars'].sum()) if 'app_stars' in df.columns else 0,
        'rated_repos': len(df[df['user_rating'].notna()]) if 'user_rating' in df.columns else 0,
        'by_industry': df.groupby('industry').size().to_dict() if 'industry' in df.columns else {},
    }
    
    return stats


def get_industry_insights(data):
    """Get insights about industry distribution"""
    repos = list(data.get('repos', {}).values())
    df = pd.DataFrame(repos)
    
    if df.empty or 'industry' not in df.columns:
        return {}
    
    industry_data = df.groupby('industry').agg({
        'id': 'count',
        'stars': 'mean',
        'user_rating': 'mean',
        'app_stars': 'sum'
    }).rename(columns={'id': 'count'})
    
    return industry_data.to_dict('index')


def validate_repo_data(repo_data):
    """Validate repository data structure"""
    required_fields = ['id', 'name', 'owner', 'repo', 'github_url', 'industry', 'stars']
    
    for field in required_fields:
        if field not in repo_data:
            return False, f"Missing required field: {field}"
    
    if repo_data['stars'] < 0:
        return False, "Stars cannot be negative"
    
    if '/' not in repo_data['name']:
        return False, "Repo name must be in owner/repo format"
    
    return True, "Valid"


def sanitize_filename(filename):
    """Sanitize filename for safe file storage"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:255]  # Limit filename length


def get_pagination_params(total_items, page, items_per_page=20):
    """Calculate pagination parameters"""
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    return {
        'total_pages': total_pages,
        'current_page': page,
        'start_idx': start_idx,
        'end_idx': end_idx,
        'items_per_page': items_per_page
    }


def search_repositories(repos, query, fields=['name', 'description']):
    """Search repositories by query in specified fields"""
    if not query:
        return list(repos.values())
    
    query_lower = query.lower()
    results = []
    
    for repo_id, repo_data in repos.items():
        for field in fields:
            if field in repo_data and query_lower in str(repo_data[field]).lower():
                results.append(repo_data)
                break
    
    return results


def filter_repositories(repos, filters):
    """Filter repositories based on criteria"""
    results = list(repos.values())
    df = pd.DataFrame(results)
    
    if df.empty:
        return []
    
    # Filter by industries
    if 'industries' in filters and filters['industries']:
        df = df[df['industry'].isin(filters['industries'])]
    
    # Filter by minimum stars
    if 'min_stars' in filters and filters['min_stars'] > 0:
        df = df[df['stars'] >= filters['min_stars']]
    
    # Filter by minimum rating
    if 'min_rating' in filters and filters['min_rating'] > 0:
        df = df[df['user_rating'].fillna(0) >= filters['min_rating']]
    
    # Filter by source
    if 'source' in filters and filters['source']:
        df = df[df['source'].isin(filters['source']) if isinstance(filters['source'], list) else df['source'] == filters['source']]
    
    return df.to_dict('records')


def rank_repositories(repos, by='stars', order='desc'):
    """Rank and sort repositories"""
    df = pd.DataFrame(repos)
    
    if df.empty:
        return []
    
    ascending = order.lower() == 'asc'
    df = df.sort_values(by, ascending=ascending)
    
    return df.to_dict('records')
