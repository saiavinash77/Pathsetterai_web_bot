# Deployment to Popular Platforms

## Heroku (Easiest for Quick Launch)

### 1. Create Heroku App
```bash
heroku login
heroku create alfredai-pathsetter
```

### 2. Set Environment Variables
```bash
heroku config:set GROQ_API_KEY=your_groq_key_here
```

### 3. Deploy
```bash
git push heroku main
```

### 4. Open
```bash
heroku open
```

---

## Railway.app (Modern & Simple)

### 1. Connect GitHub
- Go to [railway.app](https://railway.app)
- Click "New Project"
- Select "GitHub Repo"
- Authorize and select your repo

### 2. Set Variables
- In Railway dashboard, add `GROQ_API_KEY`

### 3. Deploy
- Railway auto-deploys on `git push`

### 4. Custom Domain
- In Railway settings, add domain and SSL auto-generates

---

## AWS (Professional)

### Option A: ECS (Elastic Container Service)
```bash
# Build image
docker build -t alfred .

# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ECR_URL
docker tag alfred:latest YOUR_ECR_URL/alfred:latest
docker push YOUR_ECR_URL/alfred:latest

# Create ECS task and service via AWS Console, set GROQ_API_KEY in task definition
```

### Option B: Lightsail
```bash
# Upload files to Lightsail instance
scp -r . ubuntu@your.instance.ip:/home/ubuntu/alfred

# SSH and run
ssh ubuntu@your.instance.ip
cd alfred
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Google Cloud (GCP)

### Cloud Run (Serverless)
```bash
# Build and deploy
gcloud run deploy alfred \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GROQ_API_KEY=your_key \
  --allow-unauthenticated

# Go to the provided URL
```

---

## DigitalOcean (VPS)

### 1. Droplet Setup
```bash
# SSH into droplet
ssh root@your.droplet.ip

# Update system
apt update && apt upgrade -y

# Install Python & dependencies
apt install python3-pip python3-venv -y

# Clone repo
git clone https://github.com/your-org/pathsetter-webai.git
cd pathsetter-webai

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > .env

# Run with systemd (background service)
sudo cp systemd/alfred.service /etc/systemd/system/
sudo systemctl enable alfred
sudo systemctl start alfred
```

### 2. Systemd Service File
Create `/etc/systemd/system/alfred.service`:
```ini
[Unit]
Description=Alfred Pathsetter AI
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/pathsetter-webai
Environment="PATH=/home/ubuntu/pathsetter-webai/venv/bin"
EnvironmentFile=/home/ubuntu/pathsetter-webai/.env
ExecStart=/home/ubuntu/pathsetter-webai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Nginx Reverse Proxy
```nginx
upstream alfred {
    server localhost:8000;
}

server {
    listen 80;
    server_name alfred.pathsetter.ai;
    
    location / {
        proxy_pass http://alfred;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_buffering off;
    }
}
```

### 4. SSL with Let's Encrypt
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d alfred.pathsetter.ai
```

---

## Docker Compose (Local + Production)

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  alfred:
    build: .
    ports:
      - "8000:8000"
    environment:
      GROQ_API_KEY: ${GROQ_API_KEY}
    volumes:
      - ./chroma_store:/app/chroma_store
      - ./data:/app/data
    restart: always
```

Run:
```bash
GROQ_API_KEY=your_key docker-compose up -d
```

---

## Monitoring & Logging

### Simple Logging (Tail logs)
```bash
journalctl -u alfred -f  # DigitalOcean
heroku logs --tail       # Heroku
```

### Advanced Monitoring
- Use **Sentry** for error tracking:
```python
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

- Use **DataDog** or **New Relic** for performance monitoring

---

## Performance Tuning

### For High Traffic
```python
# In app/main.py, increase workers
# Run: gunicorn app.main:app -w 8 -k uvicorn.workers.UvicornWorker
```

### Cache Responses
```python
from fastapi_cache2 import FastAPICache2
# Reduce duplicate API calls to Groq
```

### Database Optimization
- Pre-load Chroma embeddings into memory
- Use Redis for session caching

---

## Quick Summary

| Platform | Ease | Cost | Command |
|----------|------|------|---------|
| Heroku | Easy | $7+/mo | `git push heroku main` |
| Railway | Very Easy | $5+/mo | Auto-deploy |
| DigitalOcean | Medium | $5+/mo | SSH + systemd |
| AWS | Hard | ~$20+/mo | ECS / Cloud Run |
| Docker + Nginx | Medium | VPS cost | `docker-compose up` |

**Recommended for Pathsetter AI:** Railway.app (simplest) or DigitalOcean ($5/mo VPS with Nginx).
