# Pathsetter Alfred - AI-Powered Infrastructure Assistant

A conversational AI chatbot built with **FastAPI**, **Chroma DB**, and **Groq LLM** that provides intelligent responses about Pathsetter infrastructure and operations.

---

## 🎯 Project Overview

**Pathsetter Alfred** is a Retrieval-Augmented Generation (RAG) chatbot designed to answer questions about the Pathsetter project. It combines:

- **LLM Intelligence**: Powered by Groq's lightning-fast LLM (`mixtral-8b-7b-32768`)
- **Vector Search**: Uses Chroma DB for semantic similarity matching
- **Web Interface**: Clean, responsive frontend for easy interaction
- **Containerized**: Docker-ready for seamless deployment

### Key Features
✅ Real-time conversational AI responses  
✅ Semantic search through knowledge base  
✅ Auto-deployed with smart grepping for fast answers  
✅ CORS-enabled for cross-origin requests  
✅ Production-ready with Uvicorn  
✅ Docker containerization for easy deployment  

---

## 📊 Architecture

```
pathsetter-webai/
├── app/                           # Backend API
│   ├── main.py                   # FastAPI application & routes
│   ├── rag.py                    # RAG pipeline (search + LLM)
│   ├── ingest.py                 # Data ingestion & embeddings
│   └── check_db.py               # Database validation utility
├── frontend/                      # Web UI
│   ├── index.html                # Chat interface
│   ├── script.js                 # Frontend logic
│   ├── style.css                 # Styling
│   └── assets/                   # Images & logos
├── data/                         # Knowledge base
│   └── pathsetter_alfred_knowledge.md
├── chroma_store/                 # Vector database (persistent)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
├── .gitignore                    # Git ignore rules
├── DEPLOYMENT_OPTIONS.md         # Deployment guides
├── INTEGRATION_GUIDE.md          # API integration docs
└── README.md                     # This file
```

---

## 🚀 How It Works

### 1. **Data Ingestion** (`ingest.py`)
- Reads knowledge base from `pathsetter_alfred_knowledge.md`
- Splits text into overlapping chunks (200 words, 50-word overlap)
- Generates embeddings using Chroma's default model (all-MiniLM-L6-v2)
- Stores chunks in local Chroma database for fast retrieval

### 2. **RAG Pipeline** (`rag.py`)
When a user asks a question:
1. **Semantic Search**: Query is converted to embeddings, similar chunks retrieved from Chroma
2. **Context Building**: Top 3 relevant chunks are fetched
3. **LLM Processing**: Groq LLM generates answer using conversation history + context
4. **Smart Filtering**: 
   - Greeting detection → Direct friendly response
   - Ambiguous queries → Asks for clarification
   - Full context queries → Calls LLM with RAG

### 3. **API Endpoints** (`main.py`)
- **GET `/`** → Serves UI (index.html)
- **POST `/api/chat`** → Accepts messages, returns AI response
- **GET `/static/*`** → Serves frontend assets

---

## 💾 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | FastAPI |
| **Server** | Uvicorn |
| **LLM** | Groq (mixtral-8b-7b) |
| **Vector DB** | Chroma DB (local persistent) |
| **Embeddings** | all-MiniLM-L6-v2 |
| **Frontend** | HTML5 + Vanilla JavaScript |
| **Containerization** | Docker |

---

## 🛠️ Prerequisites

- Python 3.11+
- Groq API Key (get free at [console.groq.com](https://console.groq.com))
- Docker (optional, for containerized deployment)
- Git (for version control)

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/pathsetter-webai.git
cd pathsetter-webai
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Get your Groq API key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up/Login
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste into `.env`

### 5. Ingest Knowledge Base (One-time setup)
```bash
python -m app.ingest
```

Expected output:
```
🚀 Starting ingestion...
📦 Created X chunks.
✅ Successfully added X documents to Chroma.
```

This creates the `chroma_store/` directory with embeddings.

### 6. Validate Database (Optional)
```bash
python -m app.check_db
```

---

## 🎮 Running Locally

### Development Mode
```bash
# Start the server (auto-reload on code changes)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Start without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open your browser and navigate to:
```
http://localhost:8000
```

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t pathsetter-alfred:latest .
```

### Run Container Locally
```bash
docker run -e GROQ_API_KEY=your_key_here \
  -p 8000:8000 \
  pathsetter-alfred:latest
```

Access at `http://localhost:8000`

---

## 📦 API Usage

### Chat Endpoint

**Request:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is Pathsetter?"}
    ]
  }'
```

**Response:**
```json
{
  "answer": "Pathsetter is an infrastructure automation platform that..."
}
```

**Message Format:**
```python
{
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "Message text"
    }
  ]
}
```

---

## 🌐 Deployment Options

### Quick Deployment (Recommended for Testing)
- **Railway.app** - Auto-deploys from GitHub, free tier available
- **Render.com** - Simple, free tier with auto-deploy

### Production Options
- **Heroku** - Traditional PaaS, easy setup
- **AWS ECS** - Scalable, professional-grade
- **DigitalOcean** - Affordable, good performance
- **Google Cloud Run** - Serverless, pay-per-use

**See [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md) for detailed setup guides for each platform.**

---

## 📚 Project Files Explained

### Backend Files

**`app/main.py`**
- FastAPI application setup
- CORS middleware configuration
- API endpoints (GET `/`, POST `/api/chat`)
- Static file serving for frontend

**`app/rag.py`** (Core AI Logic)
- `generate_answer()` - Main RAG pipeline
- Handles semantic search via Chroma
- Calls Groq LLM for response generation
- Smart filtering for greetings & ambiguous queries

**`app/ingest.py`** (Setup Script)
- Loads markdown knowledge base
- Chunks text into overlapping segments
- Generates and stores embeddings
- One-time execution needed before app runs

**`app/check_db.py`**
- Validates Chroma database integrity
- Lists stored documents
- Useful for debugging

### Frontend Files

**`frontend/index.html`**
- Chat UI structure
- Message display container
- Input field and send button
- Logo and branding

**`frontend/script.js`**
- Event listeners for send button
- Message sending to `/api/chat`
- UI updates with responses
- Message history management

**`frontend/style.css`**
- Responsive design
- Chat bubble styling
- Mobile-friendly layout
- Dark/light theme support

### Configuration Files

**`requirements.txt`**
```
fastapi              # Web framework
uvicorn[standard]    # ASGI server
groq                 # LLM provider
chromadb             # Vector database
pydantic             # Data validation
python-dotenv        # Environment variables
tiktoken             # Token counting
```

**`Dockerfile`**
- Python 3.11-slim base
- Dependency installation
- App, frontend, and data copying
- Port 8000 exposure
- Production server startup

**`.env` (Created by you)**
```env
GROQ_API_KEY=your_api_key
```

**`.env.example` (Template)**
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🔧 Development Workflow

### Making Changes

1. **Update Knowledge Base**
   ```bash
   # Edit data/pathsetter_alfred_knowledge.md
   # Then re-ingest
   python -m app.ingest
   ```

2. **Modify Backend Logic**
   - Edit `app/rag.py` or `app/main.py`
   - Server auto-reloads in development mode

3. **Update Frontend**
   - Edit `frontend/script.js`, `style.css`, etc.
   - Refresh browser to see changes

4. **Test Changes**
   ```bash
   # Run locally
   uvicorn app.main:app --reload
   ```

---

## 🚨 Troubleshooting

### Issue: `GROQ_API_KEY not set`
**Solution:** 
- Ensure `.env` file exists in root directory
- Verify API key is correctly copied
- Restart the application

### Issue: Chroma database errors
**Solution:**
```bash
# Rebuild the database
rm -rf chroma_store/
python -m app.ingest
```

### Issue: Port 8000 already in use
**Solution:**
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### Issue: Frontend not loading
**Solution:**
- Check that `frontend/` directory exists
- Verify `index.html` is present
- Clear browser cache and refresh

---

## 📋 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | API key from [console.groq.com](https://console.groq.com) |

---

## 🤝 Contributing

Contributions are welcome! For major changes:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

For issues or questions:
- Check [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for API details
- Review [DEPLOYMENT_OPTIONS.md](DEPLOYMENT_OPTIONS.md) for deployment help
- Open an issue on GitHub

---

## ✨ What We Built

This project demonstrates a modern AI-powered solution combining:
- **Recent AI Tech**: Groq's ultra-fast LLM inference
- **Vector Databases**: Semantic search with Chroma
- **Web APIs**: RESTful FastAPI backend
- **Modern UI**: Responsive web interface
- **DevOps**: Docker containerization & cloud deployment

Perfect for building domain-specific AI assistants for any knowledge base!

---

**Last Updated:** February 2026  
**Version:** 0.3.0  
**Status:** Production Ready ✅