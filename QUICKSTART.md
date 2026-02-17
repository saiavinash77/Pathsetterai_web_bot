# Quick Start Guide - Pathsetter Alfred

Get the chatbot running in 5 minutes!

---

## 🚀 Local Development (Windows)

### 1. Setup (First Time Only)
```bash
# Open PowerShell in project folder
cd c:\Users\sai avinash\OneDrive\Desktop\pathsetter-webai

# Create virtual environment
python -m venv venv

# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your Groq API key
# (Copy from .env.example and replace with actual key)
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 2. Ingest Knowledge Base (First Time Only)
```bash
python -m app.ingest
```

### 3. Run the App
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Open in Browser
```
http://localhost:8000
```

---

## 🐳 Using Docker (One Command!)

```bash
docker build -t pathsetter-alfred .
docker run -e GROQ_API_KEY=your_key_here -p 8000:8000 pathsetter-alfred
```

Then open: `http://localhost:8000`

---

## 📤 Push to GitHub

```bash
# First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/pathsetter-webai.git
git push -u origin main

# Future updates
git add .
git commit -m "Update description"
git push
```

→ See [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) for detailed steps

---

## ☁️ Deploy to Cloud (Pick One)

### Railway.app (Easiest)
1. Go to railway.app
2. Click "New Project" → "GitHub Repo"
3. Select this repo
4. Add `GROQ_API_KEY` secret
5. Done! Auto-deploys on every git push

### Render.com
1. Go to render.com
2. Click "New Web Service"
3. Connect GitHub repo
4. Add environment variables
5. Deploy!

### Heroku
```bash
heroku login
heroku create pathsetter-alfred
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

→ See [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md) for all platforms

---

## 📚 Full Documentation

- **[README.md](README.md)** - Complete project guide
- **[DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md)** - All deployment platforms
- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - API integration details
- **[GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md)** - GitHub + deployment steps

---

## 🐛 Common Issues

**Issue:** `GROQ_API_KEY not set`
→ Make sure `.env` file exists with your key

**Issue:** Port 8000 in use
→ Use different port: `uvicorn app.main:app --port 8001`

**Issue:** "Module not found"
→ Activate venv: `venv\Scripts\activate`

---

## ✨ What You Get

- 💬 AI chatbot that answers Pathsetter questions
- 🔍 Instant semantic search using vector DB
- ⚡ Ultra-fast Groq LLM (5x faster than OpenAI)
- 🎨 Beautiful modern web interface
- 🐳 Production-ready Docker container
- ☁️ One-click cloud deployment

---

**Happy chatting!** 🤖
