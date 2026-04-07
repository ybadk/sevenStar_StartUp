import streamlit as st
import os
import json
import random
from pathlib import Path
from io import BytesIO
from datetime import datetime
import pandas as pd
import sys

try:
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.metric_cards import style_metric_cards
    HAS_EXTRAS = True
except ImportError:
    HAS_EXTRAS = False

# Add backend modules to path
APP_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(APP_DIR))

try:
    from database_manager import DatabaseManager
    from repo_analyzer import RepoAnalyzer
    from study_recommender import StudyMaterialRecommender
    HAS_MODULES = True
except ImportError:
    HAS_MODULES = False

DATA_DIR = APP_DIR / "data"
VIDEO_UPLOAD_DIR = DATA_DIR / "video_uploads"
VIDEO_REQUEST_DIR = DATA_DIR / "video_requests"
DATA_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_REQUEST_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / "database.json"

# Starred repos live in the sibling top7_project_files folder
_REPO_DATA_DIR = APP_DIR.parent / 'top7_project_files'
STARRED_FILES = [
    _REPO_DATA_DIR / 'starred_repos.txt',
    _REPO_DATA_DIR / 'starred_repos_2.txt',
    _REPO_DATA_DIR / 'starred_repos_3.txt',
]

# Also check in the current directory for starred_repos_2.txt
LOCAL_STARRED_FILES = [
    APP_DIR / 'starred_repos_2.txt',
]

# Initialize modules
if HAS_MODULES:
    db_manager = DatabaseManager(DB_FILE)
    repo_analyzer = RepoAnalyzer()
    study_recommender = StudyMaterialRecommender()


def auto_reload(timeout=85):
    st.markdown(f"""
    <script>
    let lastActivity = Date.now();
    function resetTimer() {{ lastActivity = Date.now(); }}
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    setInterval(function() {{
        if (Date.now() - lastActivity > {timeout*1000}) {{
            window.location.reload();
        }}
    }}, 10000);
    </script>
    """, unsafe_allow_html=True)


def parse_starred_repos():
    repos = {}
    for f in STARRED_FILES:
        if not f.exists():
            continue
        try:
            raw = f.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception:
            continue
        
        for li in raw:
            line = li.strip()
            if not line or line.startswith('#'):
                continue
            if 'https://' in line:
                break
            
            parts = line.split(':', 1)
            fullname = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ''
            
            if '/' not in fullname:
                continue
            
            key = fullname.lower()
            if key in repos:
                continue
            
            try:
                owner, name = fullname.split('/', 1)
                industry = classify_industry(fullname, description) if HAS_MODULES else classify_industry_fallback(fullname, description)
                repos[key] = {
                    'id': key,
                    'owner': owner,
                    'repo': name,
                    'name': fullname,
                    'description': description,
                    'github_url': f'https://github.com/{fullname}',
                    'industry': industry,
                    'stars': random.randint(400, 45000),
                    'app_stars': 0,
                    'user_rating': None,
                    'source': 'seeded',
                    'created_at': datetime.utcnow().isoformat(),
                    'tags': []
                }
            except Exception:
                continue
    
    return repos


def parse_starred_repos_2():
    """Parse starred_repos_2.txt and return a ranked dataframe."""
    repos_data = []
    
    # Check both possible locations
    starred_2_files = STARRED_FILES[1:2] + LOCAL_STARRED_FILES  # starred_repos_2.txt
    
    for f in starred_2_files:
        if not f.exists():
            continue
        try:
            raw = f.read_text(encoding='utf-8', errors='ignore').splitlines()
        except Exception:
            continue
        
        for li in raw:
            line = li.strip()
            if not line or line.startswith('#'):
                continue
            if 'https://' in line:
                break
            
            parts = line.split(':', 1)
            fullname = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 and parts[1].strip() != 'null' else ''
            
            if '/' not in fullname:
                continue
            
            try:
                owner, name = fullname.split('/', 1)
                # Generate random stars for ranking (as in original)
                stars = random.randint(400, 45000)
                
                repos_data.append({
                    'owner': owner,
                    'repo': name,
                    'name': fullname,
                    'description': description,
                    'stars': stars,
                    'github_url': f'https://github.com/{fullname}'
                })
            except Exception:
                continue
    
    # Create dataframe and sort by stars
    df = pd.DataFrame(repos_data)
    if not df.empty:
        df = df.sort_values('stars', ascending=False).reset_index(drop=True)
        df['rank'] = df.index + 1
    return df


def _count_file_repos(path):
    """Count valid owner/repo lines in a starred-repos text file."""
    if not path.exists():
        return 0
    count = 0
    try:
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if 'https://' in line:
                break
            if '/' in line.split(':', 1)[0]:
                count += 1
    except Exception:
        pass
    return count


def parse_starred_repos_3():
    """Parse starred_repos_3.txt and return a clean DataFrame for display."""
    # The file lives next to app.py in sevenStar_StartUp/
    src = APP_DIR / 'starred_repos_3.txt'
    if not src.exists():
        src = STARRED_FILES[2]  # fallback: top7_project_files location
    if not src.exists():
        return pd.DataFrame()
    repos_data = []
    try:
        raw = src.read_text(encoding='utf-8', errors='ignore').splitlines()
    except Exception:
        return pd.DataFrame()
    for li in raw:
        line = li.strip()
        if not line or line.startswith('#'):
            continue
        if 'https://' in line:
            break
        parts = line.split(':', 1)
        fullname = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 and parts[1].strip() not in ('null', '') else ''
        if '/' not in fullname:
            continue
        try:
            owner, repo_name = fullname.split('/', 1)
            industry = (
                classify_industry(fullname, description)
                if HAS_MODULES
                else classify_industry_fallback(fullname, description)
            )
            repos_data.append({
                '#': len(repos_data) + 1,
                'Repository': fullname,
                'Owner': owner,
                'Description': description[:120] + ('…' if len(description) > 120 else ''),
                'Industry': industry,
                'GitHub': f'https://github.com/{fullname}',
            })
        except Exception:
            continue
    return pd.DataFrame(repos_data)


def classify_industry_fallback(name, description):
    low = f"{name} {description}".lower()
    if any(k in low for k in ['ai', 'ml', 'deep', 'neural', 'agent', 'llm']):
        return 'AI/ML'
    if any(k in low for k in ['game', 'anime', 'toolkit', 'media', 'stream']):
        return 'Media/Gaming'
    if any(k in low for k in ['security', 'pentest', 'exploit', 'forensic', 'vuln']):
        return 'Cybersecurity'
    if any(k in low for k in ['cloud', 'aws', 'server', 'infra', 'devops', 'k8s']):
        return 'Cloud/DevOps'
    if any(k in low for k in ['education', 'learn', 'tutorial', 'book']):
        return 'Education'
    if any(k in low for k in ['data', 'db', 'dataset']):
        return 'Data Tools'
    if any(k in low for k in ['web', 'ui', 'frontend', 'design', 'css']):
        return 'Web/UI'
    return 'General Tech'


def classify_industry(name, description):
    if HAS_MODULES:
        return repo_analyzer.classify_industry(name, description)
    return classify_industry_fallback(name, description)


def load_db():
    if DB_FILE.exists():
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except Exception:
            data = {}
    else:
        data = {}

    if 'repos' not in data:
        data['repos'] = {}
    if 'video_uploads' not in data:
        data['video_uploads'] = []
    if 'video_requests' not in data:
        data['video_requests'] = []
    if 'rating_events' not in data:
        data['rating_events'] = []
    return data


def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _safe_int(val, default=0):
    """Convert *val* to int safely.

    Handles all the cases that bare ``int()`` cannot:
    - ``None``           → *default*
    - ``float('nan')``   → *default*  (pandas uses NaN for missing numeric data;
                                        NaN is *truthy* so ``nan or 0`` still = nan)
    - numpy / pandas NA  → *default*
    - anything else that raises → *default*
    """
    try:
        return default if pd.isna(val) else int(val)
    except (TypeError, ValueError):
        return default


def enrich_repos(external_repos, persisted):
    for rid, repo in external_repos.items():
        if rid in persisted:
            # preserve app stars and ratings
            persisted_row = persisted[rid]
            repo['app_stars'] = persisted_row.get('app_stars', 0)
            repo['user_rating'] = persisted_row.get('user_rating')
            repo['stars'] = max(repo.get('stars', 0), persisted_row.get('stars', repo.get('stars', 0)))
            repo['source'] = persisted_row.get('source', repo['source'])
            repo['manual_tags'] = persisted_row.get('manual_tags', [])
        else:
            repo['manual_tags'] = []
            persisted[rid] = repo
    # include user-submitted repos that may not be in the static list
    for rid, saved in list(persisted.items()):
        if rid not in external_repos:
            saved.setdefault('id', rid)
            saved.setdefault('source', 'community')
            saved.setdefault('app_stars', 0)
            saved.setdefault('user_rating', None)
            saved.setdefault('created_at', datetime.utcnow().isoformat())
    return persisted


_STUDY_PATHS = {
    'AI/ML': [
        '📖 fast.ai Practical Deep Learning (free) — https://course.fast.ai',
        '📖 Andrej Karpathy Neural Networks: Zero to Hero — YouTube playlist',
        '📖 Hugging Face NLP/LLM Course — https://huggingface.co/learn',
        '📖 deeplearning.ai Short Courses — https://learn.deeplearning.ai',
    ],
    'Cybersecurity': [
        '📖 TryHackMe — https://tryhackme.com (beginner-friendly labs)',
        '📖 Hack The Box Academy — https://academy.hackthebox.com',
        '📖 OWASP Testing Guide — https://owasp.org/www-project-web-security-testing-guide/',
        '📖 CS50 Cybersecurity — https://cs50.harvard.edu/cybersecurity/',
    ],
    'Cloud/DevOps': [
        '📖 AWS Cloud Practitioner Essentials (free) — https://explore.skillbuilder.aws',
        '📖 Docker Getting Started — https://docs.docker.com/get-started/',
        '📖 Kubernetes Official Tutorial — https://kubernetes.io/docs/tutorials/',
        '📖 GitHub Actions Quickstart — https://docs.github.com/actions/quickstart',
    ],
    'Education': [
        '📖 MIT OpenCourseWare — https://ocw.mit.edu',
        '📖 Khan Academy — https://www.khanacademy.org',
        '📖 Open edX — https://openedx.org',
        '📖 Coursera Audit Free Courses — https://www.coursera.org',
    ],
    'Data Tools': [
        '📖 Mode SQL Tutorial — https://mode.com/sql-tutorial/',
        '📖 Pandas User Guide — https://pandas.pydata.org/docs/user_guide/',
        '📖 dbt Fundamentals — https://courses.getdbt.com/courses/fundamentals',
        '📖 Apache Spark Official Docs — https://spark.apache.org/docs/latest/',
    ],
    'Web/UI': [
        '📖 The Odin Project (full-stack) — https://www.theodinproject.com',
        '📖 MDN Web Docs — https://developer.mozilla.org',
        '📖 Tailwind CSS Docs — https://tailwindcss.com/docs',
        '📖 Frontend Mentor Challenges — https://www.frontendmentor.io',
    ],
    'Media/Gaming': [
        '📖 Unity Learn — https://learn.unity.com',
        '📖 Godot Docs Tutorials — https://docs.godotengine.org/en/stable/tutorials/',
        '📖 FFmpeg Beginner Guide — https://ffmpeg.org/documentation.html',
        '📖 Game Dev Roadmap — https://roadmap.sh/game-developer',
    ],
    'General Tech': [
        '📖 The Missing Semester (CLI, Git, tools) — https://missing.csail.mit.edu',
        '📖 roadmap.sh — https://roadmap.sh (pick your path)',
        '📖 Open Source Guide — https://opensource.guide',
        '📖 GitHub Skills — https://skills.github.com',
    ],
}


def recommend_study_material(repo_item):
    base = repo_item.get('name', repo_item.get('repo', ''))
    industry = repo_item.get('industry', 'General Tech')
    domain_paths = _STUDY_PATHS.get(industry, _STUDY_PATHS['General Tech'])
    return [
        f"🔗 Start here: {base} official README & Wiki on GitHub",
        f"▶️ YouTube: search '{base} tutorial' or '{industry} open source'",
    ] + domain_paths[:3]


def run_app():
    st.set_page_config(page_title='Seven Star Startup', layout='wide', initial_sidebar_state='expanded')
    auto_reload(85)

    st.markdown('''
    <style>
    /* Modern Dark Theme inspired by Linear */
    :root {
        --bg-primary: #08090a;
        --bg-panel: #0f1011;
        --bg-surface: #191a1b;
        --bg-hover: #28282c;
        --text-primary: #f7f8f8;
        --text-secondary: #d0d6e0;
        --text-tertiary: #8a8f98;
        --accent-primary: #5e6ad2;
        --accent-bright: #7170ff;
        --accent-hover: #828fff;
        --border-subtle: rgba(255, 255, 255, 0.05);
        --border-standard: rgba(255, 255, 255, 0.08);
    }

    body, .stApp {
        background: linear-gradient(135deg, #0a0b0d 0%, #0f1011 100%) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, system-ui, Segoe UI, Roboto, sans-serif;
    }

    .main {
        background: transparent !important;
    }

    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.5px;
        color: var(--text-primary) !important;
    }

    /* Repository Cards */
    .repo-card {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-standard) !important;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }

    .repo-card:hover {
        background: #1f2022 !important;
        border-color: var(--accent-bright) !important;
        box-shadow: 0 8px 24px rgba(113, 112, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .repo-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
    }

    .repo-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin: 8px 0;
        line-height: 1.5;
    }

    .repo-meta {
        display: flex;
        gap: 16px;
        margin: 12px 0;
        flex-wrap: wrap;
    }

    .meta-item {
        background: rgba(113, 112, 255, 0.08);
        border: 1px solid var(--border-standard);
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    .metric-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(113, 112, 255, 0.12);
        border: 1px solid var(--accent-bright);
        color: var(--accent-bright);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .chip {
        display: inline-block;
        background: rgba(113, 112, 255, 0.15);
        color: var(--accent-bright);
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 0.78rem;
        margin: 2px;
        border: 1px solid var(--border-subtle);
    }

    .action-button {
        background: var(--accent-primary) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.2s;
    }

    .action-button:hover {
        background: var(--accent-bright) !important;
        box-shadow: 0 4px 12px rgba(113, 112, 255, 0.3);
    }

    .metrics-widget {
        background: var(--bg-surface);
        border: 1px solid var(--border-standard);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }

    .metric-header {
        font-size: 0.9rem;
        color: var(--text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .sidebar-section {
        background: var(--bg-surface);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-panel);
        border-bottom: 1px solid var(--border-standard);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-tertiary);
        border-radius: 0;
        padding: 12px 20px;
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-bright) !important;
        border-bottom: 2px solid var(--accent-bright) !important;
    }

    /* Form elements */
    .stTextInput, .stNumberInput, .stTextArea, .stSelectbox {
        background: var(--bg-surface) !important;
        border-radius: 8px !important;
    }

    .stTextInput > div > input, 
    .stNumberInput > div > input, 
    .stTextArea > textarea,
    .stSelectbox > div > select {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border-standard) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }

    /* Success/Info messages */
    .stSuccess, .stInfo, .stWarning {
        background: rgba(39, 166, 68, 0.15) !important;
        border: 1px solid rgba(39, 166, 68, 0.3) !important;
        border-radius: 8px !important;
        color: #27a644 !important;
    }

    /* Link styling */
    a {
        color: var(--accent-bright) !important;
        text-decoration: none;
        font-weight: 500;
    }

    a:hover {
        color: var(--accent-hover) !important;
        text-decoration: underline;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-hover) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown('# 🚀 Seven Star Startup Marketplace')
    st.markdown('### Discover and invest in open-source unicorns early — before they scale.')
    st.markdown('---')

    data = load_db()
    seeded_repos = parse_starred_repos()
    
    # Add starred_repos_2.txt data to marketplace
    starred_2_df = parse_starred_repos_2()
    starred_2_repos = {}
    for _, row in starred_2_df.iterrows():
        key = row['name'].lower()
        starred_2_repos[key] = {
            'id': key,
            'owner': row['owner'],
            'repo': row['repo'],
            'name': row['name'],
            'description': row['description'],
            'github_url': row['github_url'],
            'industry': classify_industry(row['name'], row['description']) if HAS_MODULES else classify_industry_fallback(row['name'], row['description']),
            'stars': int(row['stars']),
            'app_stars': 0,
            'user_rating': None,
            'source': 'starred_2',
            'created_at': datetime.utcnow().isoformat(),
            'tags': []
        }
    
    # Merge all repos
    all_external_repos = {**seeded_repos, **starred_2_repos}
    all_repos = enrich_repos(all_external_repos, data['repos'])
    data['repos'] = all_repos

    global_repos = list(all_repos.values())

    # safe-cast to numeric — _safe_int handles None, NaN, and invalid values
    for item in global_repos:
        item['stars'] = _safe_int(item.get('stars', 0))
        item['app_stars'] = _safe_int(item.get('app_stars', 0))
        item['user_rating'] = _safe_int(item.get('user_rating'), default=None)

    df = pd.DataFrame(global_repos)
    if df.empty:
        df = pd.DataFrame(columns=['name', 'description', 'industry', 'stars', 'app_stars', 'user_rating'])

    # Sidebar filters
    with st.sidebar:
        st.markdown('### 🔍 Discovery Filters')
        st.markdown('---')
        
        industries = sorted(df['industry'].dropna().unique().tolist())
        filter_industries = st.multiselect('Select Industries', industries, default=industries, key='industry_filter')
        
        st.markdown('**Minimum Metrics**')

        # ── GitHub Stars — data-driven button filter ───────────────────────
        # Compute thresholds from the actual star values in the loaded dataset
        _stars_series = df['stars'].dropna().astype(int) if not df.empty else pd.Series([], dtype=int)
        if len(_stars_series) > 0:

            def _fmt_stars(n):
                return f"{round(n, -3) // 1000}K+" if n >= 1000 else f"{n}+"

            _thresholds = sorted({
                int(round(_stars_series.quantile(0.25) / 500) * 500),
                int(round(_stars_series.quantile(0.50) / 1000) * 1000),
                int(round(_stars_series.quantile(0.75) / 2000) * 2000),
                int(round(_stars_series.quantile(0.90) / 5000) * 5000),
                int(_stars_series.max()),
            })
            _STAR_OPTIONS = {"Any": 0}
            for _t in _thresholds:
                if _t > 0:
                    _lbl = _fmt_stars(_t)
                    if _lbl not in _STAR_OPTIONS:
                        _STAR_OPTIONS[_lbl] = _t
        else:
            _STAR_OPTIONS = {"Any": 0, "1K+": 1000, "5K+": 5000, "10K+": 10000, "20K+": 20000, "40K+": 40000}

        _star_choice = st.radio(
            "⭐ GitHub Stars",
            options=list(_STAR_OPTIONS.keys()),
            horizontal=True,
            index=0,
            key="star_filter",
            help=f"Filter by minimum GitHub stars — dataset range: {_stars_series.min():,}–{_stars_series.max():,}" if len(_stars_series) > 0 else "Filter by minimum GitHub stars",
        )
        min_stars = _STAR_OPTIONS[_star_choice]

        # ── Community Rating — data-driven button filter ───────────────────
        # Show only rating levels that actually have repos rated at or above them
        _rated_series = df['user_rating'].dropna().astype(int) if not df.empty else pd.Series([], dtype=int)
        _rated_counts = {r: int((_rated_series >= r).sum()) for r in range(1, 8)} if len(_rated_series) > 0 else {}
        _RATING_OPTIONS = {"Any": 0}
        for _r in range(1, 8):
            if _rated_counts.get(_r, 0) > 0:
                _RATING_OPTIONS[f"{_r}" if _r == 7 else f"{_r}+"] = _r
        if len(_RATING_OPTIONS) == 1:  # no rated repos yet — show full scale
            _RATING_OPTIONS = {"Any": 0, "1+": 1, "2+": 2, "3+": 3, "4+": 4, "5+": 5, "6+": 6, "7": 7}

        _rating_choice = st.radio(
            "🌟 Community Rating",
            options=list(_RATING_OPTIONS.keys()),
            horizontal=True,
            index=0,
            key="rating_filter",
            help=f"Filter by minimum community rating — {len(_rated_series):,} rated repos in dataset",
        )
        min_rating = _RATING_OPTIONS[_rating_choice]
        
        st.markdown('---')
        search_text = st.text_input('🔎 Search projects', placeholder='Search by name or description', help='Full-text search')
        
        st.markdown('---')
        st.markdown('### 🏆 Top Starred Repos')
        
        # Load and display starred_repos_2.txt data
        starred_df = parse_starred_repos_2()
        if not starred_df.empty:

            # Add user ratings from database
            def get_user_rating(repo_name):
                repo_key = repo_name.lower()
                if repo_key in data['repos']:
                    rating = data['repos'][repo_key].get('user_rating')
                    if rating and rating > 0:
                        return '⭐' * int(rating)
                return '—'
            
            # Display top 10 ranked repos with ratings
            display_df = starred_df.head(10)[['rank', 'name', 'stars', 'description']].copy()
            display_df['rating'] = display_df['name'].apply(get_user_rating)
            display_df = display_df[['rank', 'name', 'stars', 'rating', 'description']]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'rank': st.column_config.NumberColumn('Rank', width='small'),
                    'name': st.column_config.TextColumn('Repository', width='medium'),
                    'stars': st.column_config.NumberColumn('Stars', width='small', format='%d'),
                    'rating': st.column_config.TextColumn('Rating', width='small'),
                    'description': st.column_config.TextColumn('Description', width='large')
                }
            )
        else:
            st.info('No starred repos data found.')
        
        st.markdown('---')
        st.markdown('### 📚 Data Sources')

        _source_meta = [
            (
                'starred_repos.txt',
                STARRED_FILES[0],
                '#5e6ad2',
                'Primary seeded collection',
            ),
            (
                'starred_repos_2.txt',
                STARRED_FILES[1],
                '#3b9eff',
                'Community additions',
            ),
            (
                'starred_repos_3.txt',
                APP_DIR / 'starred_repos_3.txt',
                '#22c55e',
                'Extended AI/OSS library',
            ),
        ]

        for _fname, _fpath, _color, _label in _source_meta:
            _n = _count_file_repos(_fpath)
            _exists = '✅' if _fpath.exists() else '❌'
            st.markdown(
                f"""
<div style="background:#16171a;border-radius:10px;
            padding:10px 14px;margin:5px 0;
            border-left:4px solid {_color}">
  <div style="display:flex;justify-content:space-between;
              align-items:center">
    <span style="font-size:0.78rem;font-weight:600;
                 color:#c9d1d9">📄 {_fname}</span>
    <span style="font-size:0.72rem;color:#6e7681">{_exists}</span>
  </div>
  <div style="font-size:1.8rem;font-weight:700;
              color:{_color};line-height:1.15;margin:3px 0">
    {_n:,}
  </div>
  <div style="font-size:0.72rem;color:#6e7681">{_label}</div>
</div>
""",
                unsafe_allow_html=True,
            )
        
        st.markdown('---')
        col1, col2 = st.sidebar.columns(2)
        with col1:
            total_repos = len(global_repos)
            st.metric('Total Repos', total_repos)
        with col2:
            rated_count = len([r for r in global_repos if r.get('user_rating')])
            st.metric('Rated', rated_count)
        
        st.markdown('---')
        st.markdown('**👨‍💻 Created by Kgthatso Thooe**')
        st.caption('Open Source Investment Platform')

    # Tab view
    tabs = st.tabs([
        'Marketplace', 'Metrics Dashboard', 'Submit Repo',
        'Video Upload', 'Video Request', 'Settings',
        'Tutorial', '📚 Repo Library', '🗳️ Voters Gallery',
    ])

    with tabs[0]:
        if HAS_EXTRAS:
            colored_header(
                label='Open-Source Startup Marketplace',
                description='Ranked by GitHub momentum and community engagement',
                color_name='blue-70',
            )
        else:
            st.markdown('### 📊 Open-Source Startup Marketplace')
            st.markdown('Ranked by GitHub momentum and community engagement')

        filtered = df.copy()
        if filter_industries:
            filtered = filtered[filtered['industry'].isin(filter_industries)]
        filtered = filtered[filtered['stars'] >= min_stars]
        if min_rating > 0:
            filtered = filtered[filtered['user_rating'].fillna(0) >= min_rating]
        if search_text:
            low = search_text.lower()
            name_match = filtered['name'].str.lower().str.contains(low, na=False)
            desc_match = filtered['description'].str.lower().str.contains(low, na=False)
            filtered = filtered[name_match | desc_match]

        filtered = filtered.sort_values(['stars', 'app_stars'], ascending=False)

        if filtered.empty:
            st.info('📭 No repos match the filters. Try relaxing criteria or adding new projects in the Submit Repo tab.')
        else:
            st.markdown(f'**Found {len(filtered)} projects** matching your criteria')
            st.markdown('---')

            cols = st.columns(2)
            for i, row in filtered.reset_index(drop=True).iterrows():
                rank = i + 1
                rank_icon = {1: '🥇', 2: '🥈', 3: '🥉'}.get(rank, f'#{rank}')
                col = cols[i % 2]
                with col:
                    # ── single HTML block: all display-only info ──────────────
                    _raw_rating = row.get('user_rating')
                    # Explicit NaN/None guard — don't rely on nan > 0 being False
                    _r = _safe_int(_raw_rating) if not pd.isna(_raw_rating) else 0
                    rating_display = f"{'⭐' * _r} ({_r}/7)" if _r > 0 else "Not rated"
                    desc = (row.get('description') or 'No description provided')[:200]
                    gh_url = row.get('github_url', '#')
                    industry = row.get('industry', 'General Tech')
                    source = row.get('source', '—')
                    submitted = str(row.get('created_at', ''))[:10] or '—'
                    tags_list = row.get('manual_tags') or row.get('tags') or []
                    tags_str = ', '.join(tags_list) if tags_list else '—'

                    st.markdown(f"""
<div class="repo-card">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
    <span style="font-size:1.5rem">{rank_icon}</span>
    <span class="repo-header" style="flex:1">{row['name']}</span>
    <span class="chip">{industry}</span>
  </div>
  <div class="repo-description">{desc}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin:10px 0 4px">
    <span class="metric-badge">⭐ {_safe_int(row.get('stars', 0)):,} GitHub stars</span>
    <span class="metric-badge">💼 {_safe_int(row.get('app_stars', 0))} portfolio adds</span>
    <span class="metric-badge">🌟 {rating_display}</span>
  </div>
  <hr style="border-color:#2a2b2e;margin:8px 0">
  <table style="width:100%;font-size:0.78rem;color:#9ba3af;border-collapse:collapse">
    <tr>
      <td style="padding:2px 8px 2px 0"><b>Owner</b></td>
      <td>{row.get('owner','—')}</td>
      <td style="padding:2px 8px"><b>Source</b></td>
      <td>{source}</td>
    </tr>
    <tr>
      <td style="padding:2px 8px 2px 0"><b>Submitted</b></td>
      <td>{submitted}</td>
      <td style="padding:2px 8px"><b>Tags</b></td>
      <td>{tags_str}</td>
    </tr>
  </table>
  <div style="margin-top:10px">
    <a href="{gh_url}" target="_blank"
       style="color:#5e6ad2;font-size:0.85rem;text-decoration:none">
      🔗 View on GitHub →
    </a>
  </div>
</div>
""", unsafe_allow_html=True)

                    # ── interactive controls below the card ───────────────────
                    btn_col, rate_col = st.columns([1.2, 1.8])
                    with btn_col:
                        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                        if st.button('💼 Add to Portfolio', key=f"app_star_{row['id']}", use_container_width=True):
                            data['repos'][row['id']]['app_stars'] = data['repos'][row['id']].get('app_stars', 0) + 1
                            save_db(data)
                            st.toast('Added to portfolio! 💼')
                            st.rerun()
                    with rate_col:
                        # _safe_int guards against NaN (pandas stores missing floats
                        # as float('nan'), which is truthy — so `nan or 0` == nan,
                        # and int(nan) raises ValueError on Python 3.12)
                        current_rating = _safe_int(row.get('user_rating'))
                        new_rating = st.select_slider(
                            'Your rating',
                            options=list(range(8)),
                            value=current_rating,
                            format_func=lambda v: '☆ None' if v == 0 else f"{'⭐' * v} ({v}/7)",
                            key=f"rate_slider_{row['id']}",
                        )
                        if new_rating != current_rating:
                            data['repos'][row['id']]['user_rating'] = new_rating
                            # ── Log rating event for Voters Gallery ──────────
                            data['rating_events'].append({
                                'repo_id': row['id'],
                                'repo_name': row['name'],
                                'industry': row.get('industry', 'General Tech'),
                                'github_stars': _safe_int(row.get('stars', 0)),
                                'app_stars': _safe_int(row.get('app_stars', 0)),
                                'rating': new_rating,
                                'previous_rating': current_rating,
                                'github_url': row.get('github_url', '#'),
                                'description': (row.get('description') or '')[:200],
                                'rated_at': datetime.utcnow().isoformat(),
                            })
                            save_db(data)
                            st.toast(f'Rated {new_rating}/7 ⭐')
                            st.rerun()

                    with st.expander('📚 Study Path'):
                        for item in recommend_study_material(row):
                            st.markdown(f'▸ {item}')

                    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        # ── Scrollable starred_repos_3 browser ───────────────────────────────
        st.markdown('---')
        with st.expander('📂 Browse Starred Repos · File 3  (extended library)', expanded=False):
            _df3 = parse_starred_repos_3()
            if _df3.empty:
                st.info('starred_repos_3.txt not found or contains no valid repos.')
            else:
                st.markdown(
                    f'**{len(_df3):,} repositories** indexed from `starred_repos_3.txt`'
                )
                _scroll = st.container(height=450)
                with _scroll:
                    st.dataframe(
                        _df3,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            '#': st.column_config.NumberColumn(
                                '#', width='small'
                            ),
                            'Repository': st.column_config.TextColumn(
                                'Repository', width='medium'
                            ),
                            'Owner': st.column_config.TextColumn(
                                'Owner', width='small'
                            ),
                            'Description': st.column_config.TextColumn(
                                'Description', width='large'
                            ),
                            'Industry': st.column_config.TextColumn(
                                'Industry', width='small'
                            ),
                            'GitHub': st.column_config.LinkColumn(
                                'GitHub', width='small', display_text='🔗 Open'
                            ),
                        },
                    )

    with tabs[1]:
        if HAS_EXTRAS:
            colored_header(
                label='Marketplace Metrics Dashboard',
                description='Sector intelligence for corporate & individual investors',
                color_name='violet-70',
            )
        else:
            st.markdown('### 📈 Marketplace Metrics Dashboard')
            st.markdown('Sector intelligence for corporate & individual investors')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Total Projects', len(df))
        with col2:
            st.metric('Unique Industries', len(set(df['industry'].dropna())))
        with col3:
            avg_stars = int(df['stars'].mean()) if len(df) > 0 else 0
            st.metric('Avg GitHub Stars', f"{avg_stars:,}")
        with col4:
            rated_projects = len(df[df['user_rating'].notna()])
            st.metric('Rated Projects', rated_projects)

        if HAS_EXTRAS:
            style_metric_cards(
                background_color='#191a1b',
                border_left_color='#5e6ad2',
                border_color='#28282c',
                box_shadow=True,
            )

        st.markdown('---')

        # Industry Distribution charts
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**🏭 Industry Coverage**')
            industry_counts = (
                df.groupby('industry').size()
                .reset_index(name='count')
                .sort_values('count', ascending=True)
            )
            if not industry_counts.empty:
                st.bar_chart(industry_counts.set_index('industry')['count'])

        with col2:
            st.markdown('**⭐ Avg Stars by Industry**')
            industry_stars = (
                df.groupby('industry')['stars'].mean()
                .reset_index()
                .sort_values('stars', ascending=True)
            )
            if not industry_stars.empty:
                st.bar_chart(industry_stars.set_index('industry')['stars'])

        st.markdown('---')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**🏆 Top-Rated Projects (0–7 Stars)**')
            top_rated = (
                df.dropna(subset=['user_rating'])
                .sort_values('user_rating', ascending=False)
                .head(10)
            )
            if not top_rated.empty:
                st.dataframe(
                    top_rated[['name', 'industry', 'stars', 'user_rating']],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info('No ratings yet — start rating projects in the Marketplace!')

        with col2:
            st.markdown('**🚀 Platform Momentum (Portfolio Adds)**')
            top_momentum = df.sort_values('app_stars', ascending=False).head(10)
            if not top_momentum.empty:
                st.dataframe(
                    top_momentum[['name', 'industry', 'app_stars', 'user_rating']],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info('No portfolio activity yet.')

        st.markdown('---')
        st.markdown('**💡 Investment Insights**')
        col1, col2, col3 = st.columns(3)

        with col1:
            if len(df) > 0:
                top_industry = df['industry'].value_counts().idxmax()
                top_count = df['industry'].value_counts().max()
                st.info(f'🎯 **Most Active Sector**\n\n{top_industry} · {top_count} projects')

        with col2:
            if len(df) > 0:
                underserved = df['industry'].value_counts().idxmin()
                us_count = df['industry'].value_counts().min()
                st.warning(f'⚠️ **Underserved Opportunity**\n\n{underserved} · only {us_count} project{"s" if us_count != 1 else ""}')

        with col3:
            avg_rating = df['user_rating'].dropna().mean()
            if not pd.isna(avg_rating):
                st.success(f'⭐ **Avg Community Rating**\n\n{avg_rating:.2f} / 7 stars')
            else:
                st.success('⭐ **Avg Community Rating**\n\nNo ratings yet')

    with tabs[2]:
        st.markdown('### 📝 Submit Your Repository')
        st.markdown('Add your open-source project to the marketplace')
        st.markdown('---')

        with st.form('submit_repo_form', border=False):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input('📍 GitHub Repository (owner/repo)', placeholder='e.g., microsoft/vscode', help='Format: owner/repo')
                stars = st.number_input('⭐ GitHub Stars (estimated)', min_value=0, value=100, help='Leave blank if unknown')
            
            with col2:
                industry = st.selectbox('🏭 Industry Category', sorted(set(list(industries) + ['General Tech'])), index=len(sorted(set(list(industries) + ['General Tech']))) - 1)
                github_url = st.text_input('🔗 Custom GitHub URL (optional)', placeholder='Auto-filled if empty')
            
            description = st.text_area('📄 Project Description', placeholder='What does this project do? Why is it promising?', height=100)
            tags = st.text_input('🏷️ Additional Tags (comma-separated)', placeholder='e.g., Python, AI, startup-friendly')
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submit_repo = st.form_submit_button('✨ Add to Marketplace', use_container_width=True)

        if submit_repo:
            if '/' not in full_name:
                st.error('❌ Use owner/repo format')
            else:
                repo_id = full_name.strip().lower()
                if github_url.strip() == '':
                    github_url = f'https://github.com/{repo_id}'

                data['repos'][repo_id] = {
                    'id': repo_id,
                    'owner': repo_id.split('/')[0],
                    'repo': repo_id.split('/')[1],
                    'name': repo_id,
                    'description': description,
                    'industry': industry,
                    'stars': int(stars),
                    'app_stars': 0,
                    'user_rating': None,
                    'github_url': github_url,
                    'source': 'user-submitted',
                    'manual_tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'created_at': datetime.utcnow().isoformat()
                }
                save_db(data)
                st.balloons()
                st.success(f'✅ Repository {repo_id} added successfully!')
                st.rerun()
        
        st.markdown('---')
        st.markdown('**💡 Tips:**')
        st.markdown('- Focus on projects with strong community or investment potential')
        st.markdown('- Accurate descriptions help investors understand your project')
        st.markdown('- Tags improve discoverability')

        # ── Bulk import via starred-repos text file ───────────────────────────
        st.markdown('---')
        if HAS_EXTRAS:
            colored_header(
                label='Bulk Import from Starred Repos File',
                description='Upload a .txt file in the same format as the seeded starred_repos files',
                color_name='green-70',
            )
        else:
            st.markdown('### 📂 Bulk Import from Starred Repos File')

        st.markdown(
            'Upload a plain-text file where each line is `owner/repo: description`. '
            'Lines starting with `#` or blank lines are ignored.'
        )

        with st.expander('📋 View expected format'):
            st.code(
                "# My starred repos\n"
                "microsoft/vscode: Code editor redefined and optimized for building web apps\n"
                "huggingface/transformers: State-of-the-art ML for Pytorch, TensorFlow, and JAX\n"
                "# another comment — ignored\n"
                "fastapi/fastapi: FastAPI framework, high performance, easy to learn",
                language='text',
            )

        uploaded_txt = st.file_uploader(
            'Choose a .txt starred-repos file',
            type=['txt'],
            key='bulk_import_uploader',
            help='Each line: owner/repo: description',
        )

        if uploaded_txt is not None:
            raw_lines = uploaded_txt.read().decode('utf-8', errors='ignore').splitlines()
            preview_repos = []
            skipped = 0
            for li in raw_lines:
                line = li.strip()
                if not line or line.startswith('#'):
                    continue
                if 'https://' in line:
                    break
                parts = line.split(':', 1)
                fullname = parts[0].strip()
                desc = parts[1].strip() if len(parts) > 1 else ''
                if '/' not in fullname:
                    skipped += 1
                    continue
                preview_repos.append({'name': fullname, 'description': desc})

            if not preview_repos:
                st.warning('No valid repo lines found in the uploaded file.')
            else:
                st.success(f'Found **{len(preview_repos)}** repos to import' + (f' ({skipped} lines skipped)' if skipped else ''))
                st.dataframe(
                    pd.DataFrame(preview_repos),
                    use_container_width=True,
                    hide_index=True,
                )

                imp_industry = st.selectbox(
                    '🏭 Assign Industry to all imported repos',
                    sorted(set(list(industries) + ['General Tech'])),
                    key='bulk_industry',
                )

                if st.button('⬆️ Import All to Marketplace', use_container_width=False, key='bulk_import_btn'):
                    added, dupes = 0, 0
                    for pr in preview_repos:
                        fullname = pr['name']
                        key = fullname.lower()
                        if key in data['repos']:
                            dupes += 1
                            continue
                        try:
                            owner, repo_name = fullname.split('/', 1)
                        except ValueError:
                            continue
                        inferred = classify_industry(fullname, pr['description'])
                        data['repos'][key] = {
                            'id': key,
                            'owner': owner,
                            'repo': repo_name,
                            'name': fullname,
                            'description': pr['description'],
                            'industry': inferred if inferred != 'General Tech' else imp_industry,
                            'stars': random.randint(400, 45000),
                            'app_stars': 0,
                            'user_rating': None,
                            'github_url': f'https://github.com/{fullname}',
                            'source': 'bulk-import',
                            'manual_tags': [],
                            'created_at': datetime.utcnow().isoformat(),
                        }
                        added += 1
                    save_db(data)
                    st.balloons()
                    st.success(f'✅ Imported {added} repos!' + (f' ({dupes} duplicates skipped)' if dupes else ''))
                    st.rerun()

    with tabs[3]:
        st.markdown('### 🎬 Upload Video Content')
        st.markdown('Share project pitches, demos, or investment proposals')
        st.markdown('---')

        with st.form('video_upload_form', border=False):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input('📌 Project / Startup Name', placeholder='Your project name')
                presentor = st.text_input('👤 Presenter Name or Team', placeholder='Who is presenting?')
            
            with col2:
                youtube_url = st.text_input('▶️ YouTube URL (optional)', placeholder='https://youtube.com/watch?v=...')
                video_file = st.file_uploader('📹 Upload Video File (MP4/MOV/AVI)', type=['mp4', 'mov', 'avi'])
            
            thumbnail = st.file_uploader('🖼️ Thumbnail Image (optional)', type=['jpg', 'png', 'jpeg'])
            description = st.text_area('📝 Video Description', placeholder='What is this video about?', height=80)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submit_video = st.form_submit_button('🚀 Save Video', use_container_width=True)

        if submit_video:
            if not youtube_url and not video_file:
                st.error('❌ Please provide YouTube URL or upload a video file')
            else:
                stored_file = None
                if video_file:
                    stored_file = VIDEO_UPLOAD_DIR / f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{video_file.name}"
                    with open(stored_file, 'wb') as f:
                        f.write(video_file.read())
                
                thumbnail_path = None
                if thumbnail:
                    thumbnail_path = VIDEO_UPLOAD_DIR / f"thumb_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{thumbnail.name}"
                    with open(thumbnail_path, 'wb') as f:
                        f.write(thumbnail.read())

                data['video_uploads'].append({
                    'id': f"video_{len(data['video_uploads']) + 1}",
                    'project_name': project_name,
                    'presentor': presentor,
                    'youtube_url': youtube_url,
                    'video_file': str(stored_file) if stored_file else None,
                    'thumbnail': str(thumbnail_path) if thumbnail_path else None,
                    'description': description,
                    'created_at': datetime.utcnow().isoformat()
                })
                save_db(data)
                st.balloons()
                st.success('✅ Video content saved!')

        if data['video_uploads']:
            st.markdown('---')
            st.markdown(f'**📚 Uploaded Videos ({len(data["video_uploads"])})**')
            for vid in reversed(data['video_uploads']):
                with st.expander(f"▶️ {vid['project_name']} — by {vid['presentor']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(vid['description'])
                    with col2:
                        st.caption(f"Added: {vid['created_at'][:10]}")
                    
                    if vid['youtube_url']:
                        st.video(vid['youtube_url'])
                    
                    if vid['video_file']:
                        try:
                            st.video(str(vid['video_file']))
                        except Exception as e:
                            st.warning('Could not play uploaded file directly.')
                            st.caption(f'File: {vid["video_file"]}')

    with tabs[4]:
        st.markdown('### 📺 Request Video Production')
        st.markdown('Commission custom video content for projects')
        st.markdown('---')

        with st.form('video_request_form', border=False):
            col1, col2 = st.columns(2)
            with col1:
                requester = st.text_input('👤 Your Name', placeholder='Your name')
                email = st.text_input('📧 Contact Email', placeholder='your@email.com')
            
            with col2:
                target_repo = st.text_input('🎯 Target Project', placeholder='repo-name or owner/repo')
                video_type = st.selectbox('🎬 Video Type', ['Explainer', 'Demo', 'Tutorial', 'Pitch', 'Case Study', 'Other'])
            
            requirements = st.text_area('📝 Your Requirements', placeholder='Describe what you need in this video...', height=100)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                submit_request = st.form_submit_button('✉️ Submit Request', use_container_width=True)

        if submit_request:
            if not requester or not email or not requirements:
                st.error('❌ Please complete all required fields')
            else:
                data['video_requests'].append({
                    'id': f"req_{len(data['video_requests'])+1}",
                    'requester': requester,
                    'email': email,
                    'target_repo': target_repo,
                    'video_type': video_type,
                    'requirements': requirements,
                    'created_at': datetime.utcnow().isoformat(),
                    'status': 'pending'
                })
                save_db(data)
                st.balloons()
                st.success('✅ Video request submitted! Creators will review it soon.')

        if data['video_requests']:
            st.markdown('---')
            st.markdown(f'**📋 Pending Requests ({len(data["video_requests"])})**')
            for req in reversed(data['video_requests']):
                with st.expander(f"📌 {req['target_repo']} ({req['video_type']}) — {req['requester']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write('**Requirements:**')
                        st.write(req['requirements'])
                    with col2:
                        st.metric('Status', req.get('status', 'pending').title())
                    st.caption(f'Contact: {req["email"]} | Submitted: {req["created_at"][:10]}')

    with tabs[5]:
        st.markdown('### ⚙️ Settings & Data Management')
        st.markdown('---')

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('#### 📊 Data Export')
            
            export_format = st.selectbox('Export Format', ['CSV (Repos only)', 'JSON (All data)', 'Both'])
            
            if st.button('📥 Export Data', use_container_width=True):
                try:
                    from utils import export_to_csv, export_to_json
                    
                    files_created = []
                    
                    if export_format in ['CSV (Repos only)', 'Both']:
                        csv_path = export_to_csv(data)
                        if csv_path:
                            files_created.append(csv_path)
                            st.success(f'✅ CSV exported: {Path(csv_path).name}')
                    
                    if export_format in ['JSON (All data)', 'Both']:
                        json_path = export_to_json(data)
                        if json_path:
                            files_created.append(json_path)
                            st.success(f'✅ JSON exported: {Path(json_path).name}')
                    
                    if files_created:
                        st.info(f'Files saved to: {DATA_DIR}')
                        st.code('\\n'.join(files_created))
                except Exception as e:
                    st.error(f'Export failed: {e}')
        
        with col2:
            st.markdown('#### 🔧 Application Settings')
            
            st.metric('Repos in marketplace', len(data['repos']))
            st.metric('Videos uploaded', len(data['video_uploads']))
            st.metric('Video requests pending', len(data['video_requests']))
            
        st.markdown('---')
        st.markdown('#### 🗑️ Data Management')
        
        if st.checkbox('Show advanced options (careful!)', value=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button('🔄 Clear All Ratings', help='Reset all user ratings', use_container_width=True):
                    for repo_id in data['repos']:
                        data['repos'][repo_id]['user_rating'] = None
                    save_db(data)
                    st.success('✅ All ratings cleared!')
                    st.rerun()
            
            with col2:
                if st.button('❌ Reset Portfolio Stars', help='Clear app stars', use_container_width=True):
                    for repo_id in data['repos']:
                        data['repos'][repo_id]['app_stars'] = 0
                    save_db(data)
                    st.success('✅ Portfolio cleared!')
                    st.rerun()
            
            st.warning('⚠️ Destructive actions above cannot be undone.')
        
        st.markdown('---')
        st.markdown('#### 📖 Database Information')
        st.code(f'''
Database location: {DB_FILE}
Data directory: {DATA_DIR}
Video uploads: {VIDEO_UPLOAD_DIR}
Video requests: {VIDEO_REQUEST_DIR}

Total storage: {sum(f.stat().st_size for f in DATA_DIR.rglob('*') if f.is_file()) / 1024 / 1024:.2f} MB
        ''', language='')

    with tabs[6]:
        st.markdown('### 📚 Getting Started Tutorial')
        st.markdown('Learn how to discover and invest in open-source projects')
        st.markdown('---')

        st.markdown('#### 🎯 Step 1: Explore the Marketplace')
        st.markdown('''
        - Navigate to the **Marketplace** tab
        - Browse 100+ curated open-source projects ranked by GitHub stars
        - Use filters (Industry, Star count, Rating) to find projects matching your interests
        - Each card shows GitHub stars, platform engagement, and community ratings
        ''')

        st.markdown('#### ⭐ Step 2: Rate & Star Projects')
        st.markdown('''
        - Click **⭐ Add to Portfolio** to show your support
        - Use the rating slider to rate projects 0-7 stars
        - Your ratings help other investors identify promising opportunities
        - View your portfolio momentum on the Metrics Dashboard
        ''')

        st.markdown('#### 📊 Step 3: Check Metrics Dashboard')
        st.markdown('''
        - See industry distribution and coverage gaps
        - Identify top-rated and trending projects
        - Review average ratings and platform momentum
        - Find investment opportunities in underserved sectors
        ''')

        st.markdown('#### 📝 Step 4: Submit Your Repository')
        st.markdown('''
        - Have an open-source project? Use the **Submit Repo** tab
        - Provide GitHub URL, description, industry tag, and estimated stars
        - Your project will appear in the marketplace for investor discovery
        - Include manual tags to improve visibility
        ''')

        st.markdown('#### 🎬 Step 5: Share Video Content')
        st.markdown('''
        - **Upload Videos**: Share project demos, pitches, or tutorials
        - Support YouTube links and MP4 file uploads
        - Add thumbnails for better visibility
        - Videos showcase your project to potential investors
        ''')

        st.markdown('#### 🎥 Step 6: Request Video Production')
        st.markdown('''
        - Need a professional video for your project?
        - Use **Request Video Production** to commission content creators
        - Specify video type (Explainer, Demo, Tutorial, Pitch, Case Study)
        - Creators review requests and submit proposals
        ''')

        st.markdown('---')
        st.markdown('#### 💡 Pro Tips')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('''
            ✓ **For Investors:**
            - Filter by emerging industries with fewer projects
            - Rate projects thoroughly to build your track record
            - Monitor portfolio momentum on the dashboard
            - Contact project maintainers through their GitHub URLs
            ''')
        with col2:
            st.markdown('''
            ✓ **For Project Owners:**
            - Provide clear, compelling project descriptions
            - Include relevant industry tags for discoverability
            - Upload demo videos to showcase your project live
            - Build community by encouraging ratings and stars
            ''')

        st.markdown('---')
        st.markdown('#### 🔒 Data & Privacy')
        st.markdown('All data is stored locally in JSON format. You can backup or export your data anytime.')

        st.markdown('---')
        st.markdown('**👨‍💻 Created by Kgthatso Thooe** | Seven Star Startup - Open Source Investment Platform')

    # ── Tab 7 : Repo Library ─────────────────────────────────────────────────
    with tabs[7]:
        if HAS_EXTRAS:
            colored_header(
                label='Repo Library · starred_repos_3.txt',
                description='Browse every repo from the extended library, grouped by industry',
                color_name='green-70',
            )
        else:
            st.markdown('### 📚 Repo Library · starred_repos_3.txt')

        _lib_df = parse_starred_repos_3()

        if _lib_df.empty:
            st.warning(
                'starred_repos_3.txt was not found or contains no valid repos. '
                'Make sure the file is in the sevenStar_StartUp folder.'
            )
        else:
            # ── industry colour palette ───────────────────────────────────
            _IND_COLOR = {
                'AI/ML': '#5e6ad2',
                'Cybersecurity': '#ef4444',
                'Cloud/DevOps': '#3b9eff',
                'Education': '#f59e0b',
                'Data Tools': '#8b5cf6',
                'Web/UI': '#06b6d4',
                'Media/Gaming': '#ec4899',
                'General Tech': '#6b7280',
            }

            _industries = sorted(_lib_df['Industry'].unique().tolist())

            # Build sub-tab labels: "All (N)" + one per industry with count
            _sub_labels = [f'🗂️ All  ({len(_lib_df):,})'] + [
                f'{_lib_df[_lib_df["Industry"] == ind].shape[0]}  {ind}'
                for ind in _industries
            ]
            _sub_tabs = st.tabs(_sub_labels)

            # ── card renderer ─────────────────────────────────────────────
            def _card(r):
                color = _IND_COLOR.get(r['Industry'], '#6b7280')
                desc = r['Description'] or ''
                return (
                    f'<div style="background:#16171a;border-radius:12px;'
                    f'padding:14px 16px;border:1px solid #2a2b2e;'
                    f'border-top:3px solid {color};display:flex;'
                    f'flex-direction:column;gap:5px;min-height:160px">'

                    f'<div style="font-size:0.87rem;font-weight:700;'
                    f'color:#e8e8ef;line-height:1.3;word-break:break-word">'
                    f'{r["Repository"]}</div>'

                    f'<div style="font-size:0.71rem;color:#6e7681">'
                    f'👤 {r["Owner"]}</div>'

                    f'<div style="font-size:0.75rem;color:#9ba3af;'
                    f'line-height:1.5;flex:1">{desc}</div>'

                    f'<div style="display:flex;justify-content:space-between;'
                    f'align-items:center;margin-top:auto;padding-top:6px">'
                    f'<span style="font-size:0.68rem;background:{color}22;'
                    f'color:{color};border-radius:20px;padding:2px 8px;'
                    f'font-weight:600">{r["Industry"]}</span>'
                    f'<a href="{r["GitHub"]}" target="_blank" '
                    f'style="font-size:0.75rem;color:#5e6ad2;'
                    f'text-decoration:none">🔗 GitHub →</a>'
                    f'</div></div>'
                )

            def _grid(subset):
                cards_html = ''.join(_card(r) for _, r in subset.iterrows())
                st.markdown(
                    '<div style="display:grid;'
                    'grid-template-columns:repeat(3,1fr);'
                    f'gap:14px;padding:6px 0">{cards_html}</div>',
                    unsafe_allow_html=True,
                )

            # ── All tab ───────────────────────────────────────────────────
            with _sub_tabs[0]:
                st.caption(
                    f'**{len(_lib_df):,} repos** across '
                    f'**{len(_industries)}** industries'
                )
                _grid(_lib_df)

            # ── Per-industry tabs ─────────────────────────────────────────
            for _ti, _ind in enumerate(_industries):
                with _sub_tabs[_ti + 1]:
                    _ind_df = _lib_df[
                        _lib_df['Industry'] == _ind
                    ].reset_index(drop=True)
                    _col = _IND_COLOR.get(_ind, '#6b7280')
                    st.markdown(
                        f'<span style="font-size:0.8rem;'
                        f'background:{_col}22;color:{_col};'
                        f'border-radius:20px;padding:3px 12px;'
                        f'font-weight:600">'
                        f'{len(_ind_df)} repos in {_ind}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown('')
                    _grid(_ind_df)

    # ── Tab 9: Voters Gallery ─────────────────────────────────────────────────
    with tabs[8]:
        if HAS_EXTRAS:
            colored_header(
                label='🗳️ Voters Gallery',
                description='Every rated repo — live record of community judgement',
                color_name='orange-70',
            )
        else:
            st.markdown('### 🗳️ Voters Gallery')
            st.markdown('Every rated repo — live record of community judgement')

        # ── pull the raw events and the current rated-repo snapshot ──────────
        _events: list = data.get('rating_events', [])
        _rated_repos = [
            r for r in global_repos
            if r.get('user_rating') not in (None, 0)
            and not pd.isna(r.get('user_rating') or float('nan'))
        ]
        _rated_df = (
            pd.DataFrame(_rated_repos)
            .sort_values(['user_rating', 'stars'], ascending=False)
            .reset_index(drop=True)
            if _rated_repos else pd.DataFrame()
        )

        # ── Metrics container ─────────────────────────────────────────────────
        st.markdown('#### 📊 Voting Metrics')
        _mc1, _mc2, _mc3, _mc4, _mc5 = st.columns(5)

        _total_events = len(_events)
        _unique_rated = len(_rated_repos)
        _avg_rating = (
            round(sum(e['rating'] for e in _events) / _total_events, 2)
            if _total_events > 0 else 0.0
        )
        # top industry by number of rating events
        _ind_counts: dict = {}
        for _ev in _events:
            _ind_counts[_ev.get('industry', 'General Tech')] = (
                _ind_counts.get(_ev.get('industry', 'General Tech'), 0) + 1
            )
        _top_industry = max(_ind_counts, key=_ind_counts.get) if _ind_counts else '—'
        _last_rated = (
            _events[-1].get('repo_name', '—').split('/')[-1]
            if _events else '—'
        )

        with _mc1:
            st.metric('⚡ Total Votes Cast', _total_events)
        with _mc2:
            st.metric('📦 Repos Rated', _unique_rated)
        with _mc3:
            st.metric('⭐ Avg Vote Score', f"{_avg_rating}/7")
        with _mc4:
            st.metric('🏭 Top Voted Industry', _top_industry)
        with _mc5:
            st.metric('🕐 Last Rated', _last_rated)

        st.markdown('---')

        # ── Rated-repo card gallery ───────────────────────────────────────────
        if _rated_df.empty:
            st.info(
                '🗳️ No repos have been rated yet. '
                'Head to the **Marketplace** tab and rate some repos — '
                'their cards will appear here automatically.'
            )
        else:
            st.markdown(
                f'**{len(_rated_df)} rated repo{"s" if len(_rated_df) != 1 else ""}** '
                f'· sorted by rating then GitHub stars'
            )
            _vcols = st.columns(2)
            for _vi, _vrow in _rated_df.iterrows():
                _vr = _safe_int(_vrow.get('user_rating'))
                _vrating_disp = f"{'⭐' * _vr} ({_vr}/7)" if _vr > 0 else 'Not rated'
                _vdesc = (str(_vrow.get('description') or 'No description provided'))[:200]
                _vgh = _vrow.get('github_url', '#')
                _vind = _vrow.get('industry', 'General Tech')
                _vsrc = _vrow.get('source', '—')
                _vsub = str(_vrow.get('created_at', ''))[:10] or '—'
                _vtags = _vrow.get('manual_tags') or _vrow.get('tags') or []
                _vtags_str = ', '.join(_vtags) if _vtags else '—'
                _vrank = _vi + 1
                _vrank_icon = {1: '🥇', 2: '🥈', 3: '🥉'}.get(_vrank, f'#{_vrank}')

                with _vcols[_vi % 2]:
                    st.markdown(f"""
<div class="repo-card" style="border-left:3px solid #f59e0b">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
    <span style="font-size:1.5rem">{_vrank_icon}</span>
    <span class="repo-header" style="flex:1">{_vrow['name']}</span>
    <span class="chip">{_vind}</span>
  </div>
  <div class="repo-description">{_vdesc}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;margin:10px 0 4px">
    <span class="metric-badge">⭐ {_safe_int(_vrow.get('stars',0)):,} GitHub stars</span>
    <span class="metric-badge">💼 {_safe_int(_vrow.get('app_stars',0))} portfolio adds</span>
    <span class="metric-badge" style="color:#f59e0b;font-weight:700">🌟 {_vrating_disp}</span>
  </div>
  <hr style="border-color:#2a2b2e;margin:8px 0">
  <table style="width:100%;font-size:0.78rem;color:#9ba3af;border-collapse:collapse">
    <tr>
      <td style="padding:2px 8px 2px 0"><b>Owner</b></td>
      <td>{_vrow.get('owner','—')}</td>
      <td style="padding:2px 8px"><b>Source</b></td>
      <td>{_vsrc}</td>
    </tr>
    <tr>
      <td style="padding:2px 8px 2px 0"><b>Added</b></td>
      <td>{_vsub}</td>
      <td style="padding:2px 8px"><b>Tags</b></td>
      <td>{_vtags_str}</td>
    </tr>
  </table>
  <div style="margin-top:10px">
    <a href="{_vgh}" target="_blank"
       style="color:#5e6ad2;font-size:0.85rem;text-decoration:none">
      🔗 View on GitHub →
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
                    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        st.markdown('---')

        # ── Rating event timeline ─────────────────────────────────────────────
        st.markdown('#### 🕐 Rating Event Log')
        if not _events:
            st.caption('No rating events recorded yet.')
        else:
            _recent = list(reversed(_events))  # newest first
            _page_size = 20
            _show_n = st.slider(
                'Events to show', min_value=5,
                max_value=max(5, len(_recent)),
                value=min(_page_size, len(_recent)),
                step=5, key='voter_log_slider',
            )
            for _ev in _recent[:_show_n]:
                _ev_r = _ev.get('rating', 0)
                _ev_prev = _ev.get('previous_rating', 0)
                _ev_stars = '⭐' * _ev_r if _ev_r else '☆ None'
                _ev_delta = (
                    f"↑ from {_ev_prev}" if _ev_r > _ev_prev
                    else (f"↓ from {_ev_prev}" if _ev_r < _ev_prev else '—')
                )
                _ev_ts = str(_ev.get('rated_at', ''))[:16].replace('T', ' ')
                _ev_name = _ev.get('repo_name', '—')
                _ev_ind = _ev.get('industry', '—')
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:12px;'
                    f'padding:7px 12px;margin-bottom:4px;border-radius:8px;'
                    f'background:#13141600;border:1px solid rgba(255,255,255,0.06)">'
                    f'<span style="font-size:0.78rem;color:#6b7280;min-width:130px">{_ev_ts}</span>'
                    f'<span style="font-size:0.82rem;color:#d0d6e0;flex:1">'
                    f'<b>{_ev_name}</b> &nbsp;<span style="color:#6b7280">({_ev_ind})</span></span>'
                    f'<span style="font-size:0.82rem;color:#f59e0b">{_ev_stars} ({_ev_r}/7)</span>'
                    f'<span style="font-size:0.75rem;color:#6b7280;min-width:70px;text-align:right">{_ev_delta}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    save_db(data)


if __name__ == '__main__':
    run_app()
