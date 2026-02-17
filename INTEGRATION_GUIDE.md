# Alfred Integration Guide

## Overview
Alfred is a conversational AI chatbot for Pathsetter's infrastructure platform. You can integrate it into your website in multiple ways.

---

## Option 1: Iframe Embed (Easiest)

If Alfred is running at `https://alfred.pathsetter.ai`, embed it on any page with:

```html
<iframe 
  src="https://alfred.pathsetter.ai" 
  width="600" 
  height="800" 
  style="border: none; border-radius: 12px;"
  allow="*">
</iframe>
```

**Pros:**
- Simple to implement
- Isolated environment
- Works everywhere

**Cons:**
- Cannot deeply customize UI
- Some styling limitations

---

## Option 2: Direct Integration (Full Control)

Copy the frontend files into your website and call the API directly.

### Step 1: Copy Frontend Files
```bash
cp -r frontend/* /path/to/your/website/alfred/
```

### Step 2: Update API Endpoint in JavaScript
In `frontend/script.js`, change:
```javascript
const res = await fetch('/chat', {...})
```

To:
```javascript
const res = await fetch('https://api.pathsetter.ai/chat', {...})
```

### Step 3: Add to Your Website
```html
<link rel="stylesheet" href="/alfred/style.css">
<div id="alfred-container"></div>
<script>
  // Load the Alfred container
  fetch('/alfred/index.html')
    .then(r => r.text())
    .then(html => {
      document.getElementById('alfred-container').innerHTML = html;
    });
</script>
<script src="/alfred/script.js"></script>
```

---

## Option 3: As a Widget/Button (Chat Bubble)

Add a floating chat bubble that opens Alfred in a modal:

```html
<!-- Add button -->
<button id="alfred-btn" style="
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(90deg, #2EE6B6, #1CCFA8);
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(46,230,182,0.3);
" onclick="toggleAlfred()">
  A
</button>

<!-- Modal -->
<div id="alfred-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9999;">
  <div style="position:absolute; bottom:20px; right:20px; width:420px; height:600px; background:white; border-radius:12px;">
    <iframe src="https://alfred.pathsetter.ai" width="100%" height="100%" style="border:none; border-radius:12px;"></iframe>
  </div>
</div>

<script>
function toggleAlfred() {
  const modal = document.getElementById('alfred-modal');
  modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
}
</script>
```

---

## Option 4: Deployment Options

### 4A. Docker (Recommended for Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Deploy to cloud:
```bash
# AWS ECS / Heroku / Railway / Render
docker build -t alfred .
docker push your-registry/alfred:latest
```

### 4B. Direct Server Deployment

**On your server:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production ASGI server
pip install gunicorn uvicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**With Nginx reverse proxy:**
```nginx
server {
  listen 443 ssl;
  server_name alfred.pathsetter.ai;
  
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  
  location / {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
  }
}
```

---

## API Endpoints

### Chat Endpoint
**POST** `/chat`

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "What is Alfred?"},
    {"role": "assistant", "content": "Alfred is..."},
    {"role": "user", "content": "Tell me more"}
  ]
}
```

**Response:**
```json
{
  "answer": "Alfred is an AI-native operating system for infrastructure..."
}
```

**CORS:** Enabled for all origins by default. Update `app/main.py` to restrict if needed:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://pathsetter.ai", "https://www.pathsetter.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Environment Setup

Create `.env` file on your server:
```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Testing Integration

1. **Test API directly:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hi"}]}'
```

2. **Test UI:**
- Open http://localhost:8000/
- Send messages and verify responses

3. **Test CORS:**
```javascript
fetch('https://alfred.pathsetter.ai/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({messages: [{role: 'user', content: 'test'}]})
})
.then(r => r.json())
.then(console.log)
```

---

## Customization

### Change Colors
Edit `frontend/style.css`:
```css
:root {
  --mint: #YOUR_COLOR;
  --mint-strong: #YOUR_ACCENT;
}
```

### Change Logo
Replace `frontend/assets/logo.svg` with your own.

### Change System Prompt
Edit `app/rag.py` in the `generate_answer()` function:
```python
system_instruction = "Your custom instructions here..."
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Update `allow_origins` in `app/main.py` |
| 404 Frontend not found | Ensure `frontend/` folder exists at the same level as `app/` |
| API not responding | Check `GROQ_API_KEY` is set in `.env` |
| Slow responses | Increase `max_tokens` or adjust model in `app/rag.py` |

---

## Next Steps

1. **Choose deployment option** (Docker, Heroku, AWS, etc.)
2. **Set up domain** (e.g., alfred.pathsetter.ai)
3. **Configure SSL/TLS** for HTTPS
4. **Update CORS** for your domain
5. **Embed on website** using one of the options above
6. **Monitor usage** with logs and analytics

For questions, email: hello@pathsetter.ai
