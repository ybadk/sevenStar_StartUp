# Seven Star Startup - Deployment Guide

## 🚀 Quick Start

### Local Development

**Prerequisites:**

- Python 3.9+
- pip or conda

**Option 1: Bash Script (macOS/Linux)**

```bash
bash run_app.sh
```

**Option 2: Batch Script (Windows)**

```cmd
run_app.bat
```

**Option 3: Python Runner**

```bash
python run_app.py
```

**Option 4: Direct Streamlit**

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📦 Installation

### 1. Virtual Environment Setup

**Using venv:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Using conda:**

```bash
conda create -n seven-star python=3.10
conda activate seven-star
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import streamlit; print(streamlit.__version__)"
```

---

## 🔧 Configuration

### Environment Setup

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` with your settings:

```env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=info
```

### Streamlit Configuration

The app uses `.streamlit/config.toml` for settings:

- Custom theme colors
- Server settings
- Browser behavior
- Client settings

---

## 📊 Data Management

### Database Location

```
main_repo/sevenStar_StartUp/data/
├── database.json          # Main data file
├── video_uploads/         # Uploaded videos
└── video_requests/        # Video requests
```

### Backup Data

```bash
# Backup entire data directory
cp -r data/ data_backup_$(date +%Y%m%d_%H%M%S)/

# Export to CSV (via app Settings tab)
# Export to JSON (via app Settings tab)
```

---

## 🌐 Cloud Deployment

### Streamlit Cloud

1. **Push to GitHub:**

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [https://share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Select repository and branch
   - Set main file: `main_repo/sevenStar_StartUp/app.py`
   - Deploy

### Heroku Deployment

1. **Create Procfile:**

```
web: streamlit run main_repo/sevenStar_StartUp/app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create setup.sh:**

```bash
mkdir -p ~/.streamlit/
echo "[theme]" > ~/.streamlit/config.toml
echo "primaryColor = \"#5e6ad2\"" >> ~/.streamlit/config.toml
```

3. **Deploy:**

```bash
heroku create <app-name>
git push heroku main
```

### Docker Deployment

1. **Create Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main_repo/sevenStar_StartUp/app.py"]
```

2. **Build and run:**

```bash
docker build -t seven-star .
docker run -p 8501:8501 seven-star
```

---

## 🔒 Security Considerations

### For Production:

- ✅ Use environment variables for sensitive data
- ✅ Enable HTTPS
- ✅ Restrict file upload sizes
- ✅ Regular data backups
- ✅ Monitor disk space
- ✅ Set appropriate file permissions

### .env Should Never Be Committed:

```bash
echo ".env" >> .gitignore
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in .env
STREAMLIT_SERVER_PORT=8502

# Or kill process on port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501    # Windows
```

### Memory Issues

```bash
# Increase available memory
streamlit run app.py --logger.level=warning
```

### Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Data Corruption

```bash
# Restore from backup
rm data/database.json
cp data_backup_YYYYMMDD_HHMMSS/database.json data/
```

---

## 📈 Performance

### Optimization Tips:

- Use filters to reduce visible repos
- Clear old video uploads periodically
- Monitor data directory size
- Restart app weekly for memory cleanup

### Monitor Database Size:

```bash
du -sh main_repo/sevenStar_StartUp/data/
```

---

## 📞 Support

**For issues:**

1. Check the Tutorial tab in the app
2. Review logs in terminal output
3. Check `.env` configuration
4. Verify all dependencies installed
5. Review database.json integrity

---

## 🔄 Updates

### Keep Streamlit Updated:

```bash
pip install --upgrade streamlit
```

### Update All Dependencies:

```bash
pip install --upgrade -r requirements.txt
```

---

## 📝 Version Info

- **App Version:** 1.0.0
- **Min Python:** 3.9
- **Min Streamlit:** 1.32.0
- **Created:** April 2026
- **Creator:** Kgthatso Thooe

---

**Happy investing! 🚀**
