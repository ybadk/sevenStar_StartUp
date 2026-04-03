# Project Structure Documentation

## Overview

Seven Star Startup is organized as a modular Streamlit application with supporting infrastructure for data management, analytics, and deployment.

---

## Directory Tree

```
main_repo/sevenStar_StartUp/
│
├── 📄 app.py                      # Main Streamlit application
├── 📄 __init__.py                 # Package initialization
│
├── 🔧 Backend Modules:
│   ├── config.py                  # Configuration & constants
│   ├── utils.py                   # Data management utilities
│   ├── analytics.py               # Advanced analytics engine
│   └── run_app.py                 # Standalone launcher
│
├── 📋 Documentation:
│   ├── README.md                  # User guide & features
│   ├── DEPLOYMENT.md              # Deployment instructions
│   ├── STRUCTURE.md               # This file
│
├── ⚙️ Configuration:
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment variables template
│   ├── .gitignore                 # Git ignore rules
│   ├── .streamlit/config.toml     # Streamlit configuration
│
├── 🚀 Launch Scripts:
│   ├── run_app.sh                 # Bash launcher (Linux/macOS)
│   ├── run_app.bat                # Batch launcher (Windows)
│   └── run_app.py                 # Python launcher
│
└── 📦 Data Directory:
    └── data/
        ├── database.json          # Main persistence file
        ├── video_uploads/         # User-uploaded videos
        └── video_requests/        # Video production requests
```

---

## File Descriptions

### Core Application

#### `app.py` (≈1000 lines)

The main Streamlit application file containing:

- **Auto-reload mechanism** - 85-second inactivity timeout
- **Data parsing** - Loads repos from static files and database
- **UI/UX** - Modern dark theme inspired by Linear
- **Tab-based interface:**
  - Marketplace: Browse and rate repos
  - Metrics Dashboard: Analytics and insights
  - Submit Repo: Community contributions
  - Video Upload: Share video content
  - Video Request: Commission video production
  - Settings: Data export/import
  - Tutorial: Getting started guide

#### `config.py` (≈100 lines)

Configuration module providing:

- Directory paths and initialization
- Database file location
- Industry categories (12 categories)
- Video types and ratings scale
- Application metadata
- Constants used throughout the app

#### `utils.py` (≈350 lines)

Utility functions for:

- Database CRUD operations
- CSV/JSON export functionality
- Repository statistics
- Filtering and searching
- Pagination helpers
- Data validation

#### `analytics.py` (≈300 lines)

Advanced analytics engine with:

- `RepositoryAnalytics` class:
  - Summary statistics
  - Industry breakdown
  - Top repos by metric
  - Distribution analysis
  - Health scoring
- `InvestmentAnalytics` class:
  - Portfolio analysis
  - Sector opportunity index
  - Investment recommendations

### Launch & Execution

#### `run_app.py` (≈40 lines)

Python-based launcher that:

- Sets up Python path
- Manages environment
- Launches Streamlit

#### `run_app.sh` (≈45 lines)

Bash launcher for macOS/Linux:

- Creates virtual environment if needed
- Activates venv
- Installs dependencies
- Launches app

#### `run_app.bat` (≈40 lines)

Batch launcher for Windows:

- Python version check
- Dependency verification
- Streamlit launch

### Configuration Files

#### `requirements.txt`

Core dependencies:

- streamlit >= 1.32.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- Pillow >= 9.0.0
- python-dotenv >= 1.0.0

#### `.env.example`

Template for environment variables:

- Streamlit server settings
- Application settings
- Data paths
- Optional API keys

#### `.streamlit/config.toml`

Streamlit-specific configuration:

- Dark theme colors (Linear-inspired)
- Server settings (port, headless mode)
- Client preferences
- Logger configuration

#### `.gitignore`

Protects sensitive files:

- **pycache** and .pyc files
- Virtual environments
- IDE files (.vscode, .idea)
- Environment files (.env)
- Data and upload directories
- Generated artifacts

### Documentation

#### `README.md` (≈800 lines)

Comprehensive user guide:

- Feature overview
- Installation instructions
- Usage guide for each tab
- Data structure documentation
- API reference
- Troubleshooting

#### `DEPLOYMENT.md` (≈300 lines)

Deployment guide:

- Quick start options
- Cloud deployment (Streamlit Cloud, Heroku, Docker)
- Configuration
- Backup procedures
- Performance optimization
- Security considerations

#### `STRUCTURE.md`

This file - project organization documentation

---

## Data Flow

```
┌─────────────────────────────────────────┐
│   starred_repos*.txt (Static files)     │
│   User submissions (Submit Repo tab)    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  parse_starred_repos │
        │  enrich_repos()      │
        └──────────────┬───────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │    database.json         │
        │  (Persistent storage)    │
        └──────────────┬───────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    Marketplace    Metrics      Video
    (Display)      (Analytics)   (Content)
```

---

## Module Dependencies

```
app.py
  ├── streamlit
  ├── pandas
  ├── config.py
  ├── utils.py (optional)
  └── analytics.py (optional)

utils.py
  ├── json
  ├── csv
  ├── pathlib
  ├── pandas
  └── config.py

analytics.py
  ├── pandas
  ├── config.py
  └── collections

config.py
  ├── pathlib
  └── datetime
```

---

## Data Structure

### database.json Schema

```json
{
  "repos": {
    "owner/repo": {
      "id": "owner/repo",
      "owner": "owner",
      "repo": "repo",
      "name": "owner/repo",
      "description": "Repo description",
      "github_url": "https://github.com/owner/repo",
      "industry": "AI/ML",
      "stars": 15000,
      "app_stars": 42,
      "user_rating": 6.5,
      "source": "seeded|user-submitted|community",
      "manual_tags": ["tag1", "tag2"],
      "created_at": "ISO8601 timestamp"
    }
  },
  "video_uploads": [
    {
      "id": "video_1",
      "project_name": "Project",
      "presentor": "Team",
      "youtube_url": "...",
      "video_file": "path/to/file.mp4",
      "thumbnail": "path/to/thumb.jpg",
      "description": "Description",
      "created_at": "ISO8601 timestamp"
    }
  ],
  "video_requests": [
    {
      "id": "req_1",
      "requester": "Name",
      "email": "email@example.com",
      "target_repo": "owner/repo",
      "video_type": "Explainer|Demo|Tutorial|Pitch|Case Study",
      "requirements": "Requirements",
      "created_at": "ISO8601 timestamp",
      "status": "pending|in_progress|completed|rejected"
    }
  ]
}
```

---

## Key Functions

### app.py

- `auto_reload(timeout)` - Inactivity-based page refresh
- `parse_starred_repos()` - Parse static data files
- `guess_industry(name, desc)` - Classify repos
- `load_db()` / `save_db()` - Persistence
- `enrich_repos()` - Merge external + persisted data
- `recommend_study_material()` - Learning resources
- `run_app()` - Main app controller

### utils.py

- `load_database()` / `save_database()`
- `export_to_csv()` / `export_to_json()`
- `get_repository_stats()`
- `search_repositories()` / `filter_repositories()`
- `rank_repositories()`

### analytics.py

- `RepositoryAnalytics.get_summary_stats()`
- `RepositoryAnalytics.get_top_repos()`
- `InvestmentAnalytics.get_sector_opportunity_index()`
- `InvestmentAnalytics.get_investment_recommendations()`

---

## Configuration Points

### Modifiable Settings

1. **Industries** (config.py)

   - Add/remove in INDUSTRIES list
   - Auto-detection rules in guess_industry()

2. **Video Types** (config.py)

   - Update VIDEO_TYPES list

3. **Ratings Scale** (config.py)

   - MIN_RATING, MAX_RATING constants

4. **UI Theme** (app.py, .streamlit/config.toml)

   - Colors, fonts, spacing in CSS
   - Streamlit theme configuration

5. **Auto-reload Timeout** (app.py)
   - Change timeout parameter in auto_reload(85)

---

## Performance Characteristics

- **Load time:** < 5 seconds (initial)
- **Database size:** ~50KB per 100 repos
- **Max recommended repos:** 10,000+
- **Video upload limit:** 500MB (configurable)
- **Memory usage:** ~200MB baseline + repo data

---

## Security Features

- ✅ Local data only - no cloud dependencies
- ✅ UTF-8 safe file handling
- ✅ Path validation for uploads
- ✅ XSS protection via Streamlit
- ✅ Git ignore for secrets
- ✅ .env template for safe config

---

## Extensibility

### Adding New Features

1. **New analytics metric:**

   - Add method to RepositoryAnalytics in analytics.py
   - Call from metrics tab in app.py

2. **New video type:**

   - Update VIDEO_TYPES in config.py
   - Update tabs[4] form in app.py

3. **New industry:**

   - Add to INDUSTRIES in config.py
   - Update guess_industry() logic

4. **New export format:**
   - Add function to utils.py
   - Add option to tabs[5] Settings tab

---

## Development Workflow

```
1. Edit config.py → Constants & paths
2. Edit utils.py → Backend logic
3. Edit analytics.py → New metrics
4. Edit app.py → UI/UX
5. Test locally with run_app.sh/.bat/py
6. Export data to validate
7. Commit changes to Git
8. Deploy to target environment
```

---

## Version Info

- **Version:** 1.0.0
- **Python:** 3.9+
- **Streamlit:** 1.32.0+
- **Status:** Production Ready
- **Last Updated:** April 2026

---

**For questions:** Refer to README.md or DEPLOYMENT.md
