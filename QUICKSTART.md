# 🚀 Quick Start Guide - Seven Star Startup

## One-Minute Setup

### Windows Users

1. Open `run_app.bat` (double-click)
2. Wait for dependencies to install (first time only)
3. Browser opens to `http://localhost:8501` automatically
4. Start exploring! 🎉

### macOS/Linux Users

1. Open terminal in project directory
2. Run: `bash run_app.sh`
3. Browser opens to `http://localhost:8501`
4. Start exploring! 🎉

### Advanced Users

```bash
# Install dependencies manually
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## What to Do First

### 👨‍💼 For Investors

1. Go to **Marketplace** tab
2. Browse the grid of 700+ projects
3. Use filters to find your sector of interest
4. Click **"Add to Portfolio"** (⭐) for projects you like
5. Rate projects (0-7 stars) based on potential
6. Check **Metrics Dashboard** to spot trends

### 🚀 For Project Owners

1. Go to **Submit Repo** tab
2. Enter your GitHub repo (e.g., `owner/repo`)
3. Add description, industry, and tags
4. Click **"Add Repository"**
5. Share your repo link with investors
6. Upload pitch videos in **Upload Video** tab

### 🎥 For Video Producers

1. Check **Request Video** tab for opportunities
2. Review project descriptions and requirements
3. Contact requesters via email
4. Upload finished videos in **Upload Video** tab
5. Tag videos with relevant projects

## Platform Overview

### 📊 Marketplace Tab

- **Filter by Industry** - AI/ML, Web, Cloud, Security, etc.
- **Filter by Stars** - Find projects with momentum
- **Filter by Rating** - User-rated projects (0-7)
- **Search** - Find specific repos by name or description
- **Interact** - Add to portfolio and rate projects

### 📈 Metrics Dashboard

- **Key Stats** - Total projects, industries, average ratings
- **Industry Distribution** - See which sectors are thriving
- **Top Performers** - Best-rated and most-active projects
- **Investment Insights** - Market opportunities and gaps

### 📝 Submit Repo

- Add your GitHub project to the marketplace
- Describe your project and its potential
- Tag it for better discovery
- Get investor attention!

### 🎬 Video Tabs

- **Upload Video** - Share pitches and demos
- **Request Video** - Commission custom video production

### 📖 Tutorial & Help

- Role-specific guides
- FAQ section
- Platform overview

## Data Storage

**Everything is stored locally:**

- User database: `data/database.json`
- Videos: `data/video_uploads/`
- Backup your data folder regularly!

## Tips & Tricks

### 🎯 Finding Great Projects

1. Sort by **user rating** (most rated first)
2. Look for projects with **high GitHub stars** (5000+)
3. Check **portfolio adds** (momentum indicator)
4. Read **learning resources** before investing

### ⭐ Making Your Project Shine

1. Write a **clear description** explaining your vision
2. Use **relevant tags** for better discoverability
3. Upload a **pitch video** in under 3 minutes
4. Link to your **GitHub contributions page**
5. Respond to investor inquiries quickly

### 🎥 Producing Quality Videos

1. Keep videos **under 10 minutes**
2. Use **clear audio** and proper lighting
3. Include project **highlights and metrics**
4. End with **call-to-action** (how to learn more)
5. Upload **HD quality** when possible

## Keyboard Shortcuts

- `Ctrl+F` / `Cmd+F` - Browser search within page
- `Tab` - Navigate between form fields
- `Enter` - Submit forms or select options
- `Escape` - Close modals or expanders

## Frequently Asked Questions

**Q: Is my data safe?**

- A: Yes! Everything is stored locally on your server. No cloud upload.

**Q: Can I back up my data?**

- A: Yes! Copy the `data/` folder to backup all user data and videos.

**Q: How do I contact other users?**

- A: Use the email addresses in video requests. Direct P2P communication is encouraged!

**Q: Can I export my data?**

- A: Yes! The database is plain JSON. Open `data/database.json` with any text editor.

**Q: What video formats are supported?**

- A: MP4, MOV, AVI for uploads. YouTube URLs for embedding.

**Q: Does it work offline?**

- A: Yes! Once running, Streamlit works offline. No internet required for viewing data.

**Q: Can I modify the UI?**

- A: Yes! Edit `app.py` directly or customize CSS in the style section.

**Q: How do I add more projects?**

- A: Edit `starred_repos.txt` or use the **Submit Repo** form.

## Troubleshooting

### ❌ "Streamlit command not found"

**Solution:** Install Streamlit: `pip install -r requirements.txt`

### ❌ "Port 8501 already in use"

**Solution:** Run on different port: `streamlit run app.py --server.port 8502`

### ❌ "Videos won't play"

**Solution:** Ensure MP4 format. Some formats need codec installation.

### ❌ "Database not persisting"

**Solution:** Check `data/` folder permissions. Run as administrator on Windows.

## Support

- **Documentation:** Open `README_FULL.md`
- **Code:** All source is in `app.py` - easy to modify
- **Issues:** Check for error messages in browser console
- **Contributions:** Fork and extend the platform!

## What's Next?

This is just the beginning! Here are planned enhancements:

- [ ] Real-time GitHub API data
- [ ] Machine learning investment scoring
- [ ] Mobile app support
- [ ] Advanced video processing
- [ ] Project licensing filters
- [ ] Investor authentication
- [ ] Analytics export

## Credits

**Created by:** Kgthatso Thooe

**Built with:**

- Streamlit (frontend)
- Python 3.8+
- Community data

**Inspired by:** Open-source innovation and the spirit of early investment.

---

**Ready to get started?** Run the app now and discover amazing projects! 🌟

For more details, read `README_FULL.md` or visit the code repository.
