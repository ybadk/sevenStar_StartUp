import json
from pathlib import Path


class DatabaseManager:
    """Manages database persistence for the Seven Star Startup platform."""

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        """Load database from file."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return self._ensure_keys(data)
            except Exception:
                pass
        return self._get_empty_db()

    def save(self, data):
        """Save database to file."""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

    @staticmethod
    def _ensure_keys(data):
        """Ensure all required keys exist in data."""
        if 'repos' not in data:
            data['repos'] = {}
        if 'video_uploads' not in data:
            data['video_uploads'] = []
        if 'video_requests' not in data:
            data['video_requests'] = []
        return data

    @staticmethod
    def _get_empty_db():
        """Return an empty database structure."""
        return {
            'repos': {},
            'video_uploads': [],
            'video_requests': []
        }
