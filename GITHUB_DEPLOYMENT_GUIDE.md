# Pathsetter Alfred - GitHub Deployment Guide

This guide walks you through pushing your project to GitHub and setting up deployment.

---

## Step 1: Initialize Git Repository (If Not Already Done)

```bash
cd c:\Users\sai avinash\OneDrive\Desktop\pathsetter-webai

# Initialize git
git init

# Configure Git user (if not already configured)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Pathsetter Alfred AI Chatbot"
```

---

## Step 2: Create GitHub Repository

1. **Go to [github.com](https://github.com)**
2. **Sign in** to your GitHub account
3. **Click the "+" icon** → Select "New repository"
4. **Fill in details:**
   - Repository name: `pathsetter-webai`
   - Description: "AI-powered infrastructure assistant chatbot with RAG"
   - Visibility: **Public** (for easier deployment) or **Private**
   - Initialize: Leave unchecked (we already have files)
5. **Click "Create repository"**

---

## Step 3: Connect Local Repository to GitHub

GitHub will show instructions. Copy the URL (HTTPS or SSH) and run:

```bash
# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/pathsetter-webai.git

# Verify remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/pathsetter-webai.git (fetch)
# origin  https://github.com/YOUR_USERNAME/pathsetter-webai.git (push)
```

---

## Step 4: Push to GitHub

```bash
# Push main branch to GitHub
git branch -M main
git push -u origin main

# You'll be prompted to authenticate:
# - Use GitHub username
# - Use Personal Access Token (not password) - see below
```

### Getting GitHub Personal Access Token (PAT)

If you get auth errors:

1. Go to GitHub → **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Under **Select scopes**, check:
   - ✅ `repo` (Full control of private repositories)
4. Click **"Generate token"** and copy it
5. Use this token as your password when pushing

---

## Step 5: Verify Push Success

```bash
# Check git status
git status
# Should show: "On branch main, nothing to commit"

# View commit history
git log --oneline

# Check GitHub - your repository should show all files
```

---

## Step 6: Set Up GitHub Secrets (For Deployment)

GitHub Secrets allow you to store sensitive data (like API keys) securely.

1. **Go to your GitHub repository**
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**
4. **Name:** `GROQ_API_KEY`
5. **Value:** Paste your Groq API key
6. **Add secret**

Now deployment platforms can access this securely!

---

## Step 7: Deploy to Production

### Option A: Railway.app (Recommended - Easiest)

```bash
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Select "Deploy from GitHub repo"
# 4. Authorize GitHub and select your repo
# 5. Railway auto-detects requirements.txt and Dockerfile
# 6. In Railway dashboard, add variable:
#    - GROQ_API_KEY = your_key
# 7. Railway auto-deploys!
# 8. Get public URL in Railway dashboard
```

**Advantages:**
- ✅ One-click setup
- ✅ Free tier available
- ✅ Auto-deploys on `git push`
- ✅ No configuration needed

### Option B: Render.com

```bash
# 1. Go to https://render.com
# 2. Click "New +"
# 3. Select "Web Service"
# 4. Connect GitHub repo
# 5. Fill in:
#    - Runtime: Python 3.11
#    - Build command: pip install -r requirements.txt
#    - Start command: uvicorn app.main:app --host 0.0.0.0 --port 8000
# 6. Add env vars from GitHub
# 7. Deploy!
```

### Option C: Heroku (Traditional)

```bash
# 1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
# 2. Login
heroku login

# 3. Create app
heroku create pathsetter-alfred

# 4. Set env variable
heroku config:set GROQ_API_KEY=your_key

# 5. Push to Heroku (auto-deploys)
git push heroku main

# 6. Open
heroku open
```

---

## Step 8: Future Updates

After making changes locally:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main

# Your deployment platform auto-deploys! (on Railway/Render/Heroku)
```

---

## 🎯 Quick Checklist

- [ ] Git initialized locally
- [ ] GitHub repository created
- [ ] Local repo connected to GitHub (git remote add origin)
- [ ] Code pushed to GitHub (git push)
- [ ] GitHub secrets configured with GROQ_API_KEY
- [ ] Deployment platform connected (Railway/Render/Heroku)
- [ ] App deployed and accessible via public URL
- [ ] Frontend loads in browser
- [ ] Chat works end-to-end

---

## 🆘 Troubleshooting

### Git push says "rejected"
```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Authentication failed
- Generate Personal Access Token (see Step 4)
- Use token as password, not your GitHub password

### Deployment fails
- Check build logs in deployment platform
- Verify GROQ_API_KEY is set in secrets
- Ensure requirements.txt is present
- Check Dockerfile is correct

---

## 📊 Repository Structure (What's on GitHub)

```
pathsetter-webai/
├── app/
│   ├── main.py
│   ├── rag.py
│   ├── ingest.py
│   └── check_db.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── assets/
├── data/
│   └── pathsetter_alfred_knowledge.md
├── Dockerfile
├── requirements.txt
├── .gitignore          # ← Prevents uploading sensitive files
├── .env.example        # ← Template for users
├── README.md           # ← Project documentation
├── DEPLOYMENT_OPTIONS.md
├── INTEGRATION_GUIDE.md
└── GITHUB_DEPLOYMENT_GUIDE.md  # ← This file
```

---

## 🔒 Security Best Practices

✅ **DO:**
- Store API keys in GitHub Secrets
- Use `.env.example` as template
- Include `.env` in `.gitignore` (never commit real keys)
- Enable branch protection rules
- Review pull requests before merging

❌ **DON'T:**
- Commit `.env` files
- Push API keys to GitHub
- Make private repos public without review
- Use same keys across multiple environments

---

## 📈 Next Steps

1. **Monitor Your Deployment**
   - Set up error monitoring (Sentry)
   - Check logs regularly

2. **Track Changes**
   ```bash
   git log --oneline  # View all commits
   git status         # Current state
   git diff           # See exactly what changed
   ```

3. **Collaborate**
   - Invite team members to repository
   - Use pull requests for code review
   - Set branch protection rules

4. **Scale**
   - Add more knowledge bases
   - Implement authentication
   - Set up CI/CD pipelines
   - Add monitoring & alerting

---

**You're all set! Your Pathsetter Alfred is now on GitHub and ready for production deployment.** 🚀
