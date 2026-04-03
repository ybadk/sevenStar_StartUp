# 🚀 Seven Star Startup - Open Source Investment Marketplace

**Discover and invest in open-source unicorns early — before they scale.**

Seven Star Startup is a innovative platform that connects corporate investors and individual stakeholders with promising open-source projects on GitHub. By combining GitHub repository data with community voting and engagement metrics, we create a curated marketplace for discovering the next generation of tech innovations.

## 🎯 Platform Overview

Seven Star Startup transforms how the investment community identifies and supports open-source projects:

- **📊 AI-Powered Discovery** - Intelligent repository classification by industry and potential
- **⭐ Community-Driven Ratings** - Crowdsourced project evaluation (0-7 star ratings)
- **📈 Portfolio Tracking** - Monitor and bookmark promising projects
- **🎬 Video Marketing** - Pitch videos and investment presentations
- **🔗 Direct GitHub Integration** - One-click access to repos and contribution guides
- **📚 Smart Study Paths** - Personalized learning resources for each project type

## ✨ Key Features

### 1. **Marketplace (Repository Grid View)**
- Browse 500+ curated open-source projects from GitHub
- Filter by industry, minimum stars, and community rating
- Advanced search across project names and descriptions
- 3-column responsive grid layout with rich project cards
- One-click portfolio additions (⭐ star tracking)

### 2. **Metrics Dashboard**
- **Investment Analytics** - Key metrics: total projects, avg stars, unique industries
- **Industry Distribution** - Visual breakdown of projects by sector
- **Star Analytics** - Average GitHub stars by industry
- **Top Performers** - Highest-rated projects and momentum leaders
- **Strategic Insights** - Market gaps and investment opportunities

### 3. **Repository Submission**
- **Community Features** - Submit your own GitHub repositories
- **Rich Metadata** - Add descriptions, industry tags, and custom URLs
- **Custom Tagging** - Add founder/investor notes and categorization
- **Instant Indexing** - Submitted repos appear immediately in marketplace

### 4. **Video Hub (Upload & Request)**
- **Pitch Video Uploads** - Share project demos, company pitches, investment presentations
- **YouTube Integration** - Embed YouTube videos directly
- **File Uploads** - Support for MP4, MOV, AVI video formats
- **Thumbnails** - Custom video thumbnail images
- **Production Requests** - Commission video creators for custom content
- **Creator Portal** - Producers can browse and bid on video opportunities

### 5. **Educational Resources**
- **Smart Study Recommendations** - AI-generated learning paths based on project type
- **Industry-Specific Guides** - Tailored resources for AI/ML, Web, Cloud, Data, etc.
- **Direct GitHub Links** - Contribution guides and README documentation
- **Multi-Source Learning** - YouTube tutorials, courses, and academic resources

### 6. **Data Persistence**
- **Local JSON Database** - `data/database.json` stores all user interactions
- **No External Dependencies** - Runs completely offline and self-contained
- **Easy Backups** - Single-file database for simple versioning
- **User Data Protection** - All data stays on your server

## 🏗️ Project Structure

```
sevenStar_StartUp/
├── app.py                    # Main Streamlit application
├── database_manager.py        # Database persistence layer
├── repo_analyzer.py          # Industry classification & scoring
├── study_recommender.py      # Learning path generator
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── starred_repos.txt         # Initial dataset (500+ projects)
├── starred_repos_2.txt       # Extended dataset
├── starred_repos_3.txt       # Additional projects
├── README.md                 # This file
├── data/                     # Runtime data directory
│   ├── database.json         # User data persistence
│   ├── video_uploads/        # Uploaded video & thumbnail files
│   └── video_requests/       # Video production requests
└── docs/                     # Documentation (future)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 2GB disk space (for data and video storage)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd sevenStar_StartUp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the platform:**
   - Open your browser to `http://localhost:8501`
   - The app will automatically load marketplace data from starred repos files

### Alternative: Using Run Scripts

**On Windows:**
```bash
run_app.bat
```

**On macOS/Linux:**
```bash
bash run_app.sh
```

## 📊 How It Works

### Data Flow

```
Starred Repos Files (.txt)
         ↓
    Parse & Index
         ↓
    Industry Classification (RepoAnalyzer)
         ↓
   Enrich with User Data (database.json)
         ↓
    Display in Marketplace Grid
         ↓
    User Interactions (stars, ratings, videos)
         ↓
    Persist to database.json
```

### Industry Classification

The `RepoAnalyzer` automatically classifies projects into categories:
- **AI/ML** - Machine learning, neural networks, LLMs, agents
- **Web/UI** - Frontend, React, Vue, Angular, design systems
- **Cloud/DevOps** - Kubernetes, Docker, AWS, infrastructure
- **Data Tools** - Databases, analytics, data warehouses
- **Cybersecurity** - Penetration testing, security tools, forensics
- **Mobile** - Android, iOS, React Native, Flutter
- **Finance** - Payment systems, crypto, trading platforms
- **Education** - Learning platforms, tutorials, courses
- **Media/Gaming** - Graphics, streaming, game engines
- **General Tech** - Other projects

### Rating System

Projects are evaluated on a **0-7 star scale**:
- **0-2 ⭐** - Early-stage, experimental
- **3-4 ⭐** - Solid, established projects
- **5-6 ⭐** - High-quality, production-ready
- **7 ⭐** - Exceptional, market-leading projects

## 👥 User Roles

### For Investors
1. **Browse & Discover** - Filter projects by industry, funding potential
2. **Rate & Review** - Evaluate projects on your standards
3. **Build Portfolio** - Maintain watchlist of promising projects
4. **Watch Videos** - Review project pitches and team videos
5. **Track Metrics** - Monitor industry trends and opportunities

### For Project Owners
1. **Get Discovered** - Submit your project for investor exposure
2. **Build Community** - Engage with platform users and supporters
3. **Pitch to Investors** - Upload video pitches and presentations
4. **Request Producers** - Commission video content for marketing
5. **Track Engagement** - Monitor ratings and portfolio adds

### For Video Producers
1. **Find Opportunities** - Browse video production requests
2. **Bid on Projects** - Propose your services with portfolio
3. **Upload Content** - Share finished videos to platform
4. **Build Network** - Connect with project owners and investors
5. **Monetize Expertise** - Earn from production requests

## 🎓 Study Recommendations

The platform provides intelligent study material recommendations based on project type:

### Example: AI/ML Projects
- Official GitHub README & documentation
- YouTube tutorials and walkthroughs
- Deep learning fundamentals courses
- Research papers and academic resources
- Community showcases and real-world applications

### Example: Web/UI Projects
- HTML/CSS/JavaScript fundamentals
- React/Vue component libraries
- Responsive design patterns
- Performance optimization guides
- Accessibility best practices

All recommendations are dynamically generated based on the project's industry classification.

## 💾 Database Schema

### Repositories (``database.json` - repos)
```json
{
  "repo_id": {
    "id": "owner/repo",
    "name": "owner/repo",
    "owner": "owner",
    "repo": "repo",
    "description": "Project description",
    "github_url": "https://github.com/owner/repo",
    "industry": "AI/ML",
    "stars": 5000,
    "app_stars": 45,
    "user_rating": 6.5,
    "source": "seeded|user-submitted|community",
    "tags": ["python", "ml", "tensorflow"],
    "created_at": "2025-04-03T14:30:00Z"
  }
}
```

### Video Uploads
```json
{
  "id": "video_1",
  "project_name": "Project Name",
  "presentor": "Presenter Name",
  "youtube_url": "https://youtube.com/watch?v=...",
  "video_file": "/path/to/video.mp4",
  "thumbnail": "/path/to/thumb.jpg",
  "description": "Video description",
  "created_at": "2025-04-03T14:30:00Z"
}
```

### Video Requests
```json
{
  "id": "req_1",
  "requester": "Name",
  "email": "email@example.com",
  "target_repo": "owner/repo",
  "video_type": "Demo|Tutorial|Pitch",
  "requirements": "Detailed requirements",
  "status": "pending|in-progress|completed",
  "created_at": "2025-04-03T14:30:00Z"
}
```

## ⚙️ Configuration

Edit `config.py` to customize:
- Auto-reload timeout
- Industry categories
- Default filters
- Video file size limits
- Study recommendation templates

## 🔧 Development

### Project Architecture

**Frontend (Streamlit)**
- `app.py` - Main application UI and logic
- Dynamic filtering and search
- Video upload/streaming
- Data visualization with charts

**Backend Modules**
- `database_manager.py` - JSON persistence layer
- `repo_analyzer.py` - Industry classification and scoring
- `study_recommender.py` - Learning path generation

**Data Storage**
- `data/database.json` - All user interactions
- `data/video_uploads/` - Video and thumbnail files
- `data/video_requests/` - Production request metadata

### Extending the Platform

**Add New Industries:**
```python
# In repo_analyzer.py
INDUSTRIES['New Category'] = ['keyword1', 'keyword2', ...]
```

**Add Study Resources:**
```python
# In study_recommender.py
DOMAIN_RESOURCES['New Category'] = [resource templates...]
```

**Customize Filtering:**
Edit the Streamlit sidebar in `app.py` to add new filter types.

## 📈 Performance & Scalability

- **500+ Projects Indexed** - Fast pagination and filtering
- **Real-time Sorting** - Sort by stars, ratings, momentum
- **Search Engine** - Full-text search across names and descriptions
- **Video Streaming** - Supports MP4, MOV, YouTube embedding
- **Responsive Design** - Works on desktop, tablet, mobile

**Scaling Considerations:**
- Database supports 10,000+ repositories
- For larger datasets, migrate to PostgreSQL
- Cache frequently accessed data
- Implement CDN for video distribution

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Permission denied" when saving videos
**Solution:** Ensure `data/` and subdirectories have write permissions:
```bash
chmod -R 755 data/
```

### Issue: "Address already in use" on port 8501
**Solution:** Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: Videos not playing in browser
**Solution:** Use direct MP4 files or YouTube URLs; some formats require codec installation

## 📝 License & Attribution

**Created by:** Kgthatso Thooe  
**Platform:** Seven Star Startup - Open Source Investment Marketplace  
**License:** Open Source (MIT)

This platform was designed to democratize investment discovery in the open-source ecosystem and empower capital to find innovation.

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- [ ] Authentication & multi-user support
- [ ] API integration with GitHub for real-time data
- [ ] Machine learning models for investment scoring
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced video processing pipeline
- [ ] Blockchain integration for transparent tracking
- [ ] Integration with Crunchbase and AngelList
- [ ] Real-time notifications and alerts

## 🎯 Future Roadmap

- **V2.0** - GitHub API integration for real-time data
- **V2.5** - ML-powered investment scoring model
- **V3.0** - Web platform with user authentication
- **V3.5** - Mobile apps (iOS/Android)
- **V4.0** - Decentralized data with blockchain

## 📞 Support & Contact

For questions, feature requests, or issues:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation and FAQ

---

**Made with ❤️ for the open-source community**

Empowering capital to find innovation. One repository at a time.
