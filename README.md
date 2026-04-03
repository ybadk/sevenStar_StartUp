# 🚀 Seven Star Startup Marketplace

> **Created by Kgthatso Thooe**

> **Invest in open-source unicorns early.** Seven Star Startup is a community-driven platform where corporate investors and individuals discover, evaluate, and fund promising open-source projects while they're still on GitHub.

---

## 🎯 About the Project

Seven Star Startup transforms the way investors identify and support innovative open-source projects. The platform aggregates highly-starred repositories from GitHub, presents them in an interactive marketplace format, and enables investors to:

- **Discover** promising startups and tools across industries
- **Evaluate** projects with community ratings and GitHub metrics
- **Support** projects by starring and rating them on the platform
- **Invest** by contacting project maintainers through the platform
- **Contribute** custom repositories and video pitches

### Key Features

✨ **Marketplace** - Browse open-source projects ranked by GitHub stars and community engagement  
📊 **Metrics Dashboard** - Industry insights and portfolio performance tracking  
🎥 **Video Content** - Upload project pitches and request custom video production  
📝 **Community Submissions** - Add your own repositories to the marketplace  
🏷️ **Smart Filtering** - Discovery by industry, stars, and user ratings  
💾 **Local Data Persistence** - All data stored securely in JSON format  
🎨 **Professional UI** - Clean, modern interface built with Streamlit

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Git**

### Installation

1. **Clone the repository** or navigate to the app directory:

```bash
cd main_repo/sevenStar_StartUp
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

### Running the Application

**Option 1: Streamlit Run**

```bash
streamlit run app.py
```

**Option 2: Batch Script (Windows)**

```bash
run_app.bat
```

**Option 3: Shell Script (macOS/Linux)**

```bash
bash run_app.sh
```

The app will launch in your default browser at `http://localhost:8501`

---

## 📖 How to Use

### 1. **Browse the Marketplace**

- Check out the **Marketplace** tab to see repositories ranked by GitHub stars
- Filter by industry, minimum stars, and community ratings
- Use the search bar to find specific projects
- Click on any project card to view detailed metrics and learning resources

### 2. **Rate & Star Projects**

- Add projects to your portfolio using the **⭐ Add to portfolio** button
- Rate projects on a 0-7 scale using the slider
- Ratings persist locally and help other investors make decisions

### 3. **View Metrics Dashboard**

- Monitor industry coverage and repo distribution
- Track top-rated projects and community momentum
- Export data for investment analysis

### 4. **Submit Your Repository**

- Use the **Submit Repo** tab to add your own open-source project
- Provide GitHub repo name, description, and industry tag
- Your repo will appear in the marketplace for other investors to discover

### 5. **Upload & Request Videos**

- **Upload Video Content**: Share project pitch videos (YouTube links or MP4 uploads)
- **Request Video Production**: Request custom video content creation for projects you're interested in

### 6. **Access Learning Resources**

- Each repo includes recommended study materials
- Links to official documentation, tutorials, and domain knowledge resources

---

## 📊 Data Structure

### Database Schema (`database.json`)

```json
{
  "repos": {
    "repo-key": {
      "id": "owner/repo",
      "owner": "user",
      "repo": "project",
      "name": "owner/project",
      "description": "Project description",
      "github_url": "https://github.com/owner/project",
      "industry": "AI/ML",
      "stars": 15000,
      "app_stars": 42,
      "user_rating": 6.5,
      "source": "seeded|user-submitted|community",
      "manual_tags": ["tag1", "tag2"],
      "created_at": "2025-01-15T10:30:00"
    }
  },
  "video_uploads": [
    {
      "id": "video_1",
      "project_name": "Project Name",
      "presentor": "Team Name",
      "youtube_url": "https://youtube.com/...",
      "video_file": "path/to/file.mp4",
      "thumbnail": "path/to/thumb.jpg",
      "description": "Video description",
      "created_at": "2025-01-15T10:30:00"
    }
  ],
  "video_requests": [
    {
      "id": "req_1",
      "requester": "Name",
      "email": "contact@example.com",
      "target_repo": "owner/repo",
      "requirements": "Video requirements",
      "created_at": "2025-01-15T10:30:00"
    }
  ]
}
```

### Directory Structure

```
sevenStar_StartUp/
├── app.py                 # Main Streamlit application
├── README.md              # Documentation (this file)
├── requirements.txt       # Python dependencies
├── data/
│   ├── database.json      # Local data persistence
│   ├── video_uploads/     # User-uploaded video files
│   └── video_requests/    # Video production requests
└── .gitignore             # Git ignore rules
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the app directory for custom configuration:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true
```

### Customizing Industry Categories

Edit the `guess_industry()` function in `app.py` to add or modify industry detection rules:

```python
def guess_industry(name, description):
    low = f"{name} {description}".lower()
    if any(k in low for k in ['your', 'keywords']):
        return 'Your Industry'
    # ... more conditions
```

---

## 📈 Features in Detail

### Marketplace Filtering

- **Industry Filter**: Multi-select industries (AI/ML, Security, Cloud/DevOps, etc.)
- **Star Filter**: Minimum GitHub stars threshold
- **Rating Filter**: Minimum community rating (0-7)
- **Search**: Full-text search across repository names and descriptions

### Metrics Dashboard

- **Industry Distribution**: Bar chart showing repo count by sector
- **Top-Rated Projects**: Table of highest-rated repositories
- **Momentum Tracking**: Projects with most platform stars
- **Coverage Analysis**: Identify gaps in industry representation

### Video Management

- **YouTube Integration**: Embed YouTube videos directly
- **File Upload**: Support for MP4, MOV, AVI formats
- **Thumbnails**: Custom preview images for videos
- **Request Tracking**: Manage video production inquiries

### Data Export

All data is stored in human-readable JSON format and can be:

- Backed up to external storage
- Imported to analysis tools
- Shared with team members
- Restored from backups

---

## 🛠️ Technology Stack

| Component         | Technology              |
| ----------------- | ----------------------- |
| **Frontend**      | Streamlit v1.0+         |
| **Data**          | JSON (local file-based) |
| **Python**        | 3.9+                    |
| **UI Components** | Streamlit Extras        |
| **Data Analysis** | Pandas                  |
| **Environment**   | python-dotenv           |

---

## 💡 Development Guide

### Adding New Features

1. **Add a new tab**: Create a new tab in the `tabs = st.tabs([...])` section
2. **Add data fields**: Update the database schema in the tab logic
3. **Persist data**: Ensure `save_db(data)` is called after changes
4. **Test locally**: Run `streamlit run app.py` and verify functionality

### Modifying the UI Theme

Update the CSS in the `st.markdown()` style block:

```python
st.markdown('''
<style>
/* Your custom CSS here */
body { background: linear-gradient(...) !important; }
.repo-card { /* card styling */ }
</style>
''', unsafe_allow_html=True)
```

### Auto-Reload Feature

The app includes a 85-second inactivity timeout for auto-reload. Modify in `auto_reload()` function:

```python
def auto_reload(timeout=85):  # Change 85 to desired seconds
    # ...
```

---

## 📊 Sample Data Sources

The platform includes curated lists of open-source projects from:

- `starred_repos.txt` - AI/ML and general tech projects
- `starred_repos_2.txt` - Security and DevOps tools
- `starred_repos_3.txt` - Creative and Web tools

Add new repositories to any of these files or use the Submit Repo form.

---

## 🐛 Troubleshooting

### "No repos match the filters"

- Lower the minimum stars filter
- Try searching without filters
- Submit new repositories using the Submit Repo tab

### Video playback not working

- Ensure the video file is in a supported format (MP4, MOV, AVI)
- For large files, consider hosting on YouTube instead
- Check browser console for error messages

### Data loss

- Database.json is stored in `data/` directory
- Create regular backups of the `data/` folder
- JSON format allows easy transfer to backup systems

### Performance issues

- Clear browser cache and refresh
- Reduce the number of visible repos using filters
- Monitor available disk space for video uploads

---

## 🤝 Contributing

We welcome contributions! Please:

1. Test your changes locally
2. Ensure data persistence works correctly
3. Follow the existing code style
4. Update documentation if adding features

---

## 📜 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Created By

**Kgthatso Thooe**

Seven Star Startup - _Empowering investors to discover unicorns on GitHub_

---

## 📞 Support & Feedback

For questions, issues, or feature requests:

- Check the Tutorial tab in the app for usage help
- Review the data in `database.json` for debugging
- Test functionality locally before deployment

---

## 🎓 Learning Resources

Each repository in the marketplace includes:

- Links to official GitHub README
- Recommended YouTube tutorials
- Domain-specific learning paths
- Community knowledge graphs

Explore and learn from the projects that interest you most!

---

**Last Updated**: April 2026  
**Version**: 1.0.0
