import os
import chromadb

# 1. Setup absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level from 'app/' to project root
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
CHROMA_PATH = os.path.join(PROJECT_ROOT, "chroma_store")
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "pathsetter_alfred_knowledge.md")

print(f"📂 Project Root: {PROJECT_ROOT}")
print(f"💾 Chroma Path:  {CHROMA_PATH}")
print(f"📄 Data File:    {DATA_FILE}")

# 2. Check Data File
if not os.path.exists(DATA_FILE):
    print("❌ ERROR: Data file not found!")
    exit(1)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"📊 Data File Size: {len(content)} characters")
    if len(content) < 100:
        print("⚠️ WARNING: Your data file seems empty or very short!")

# 3. Check Chroma DB
print("\n--- Connecting to Chroma ---")
client = chromadb.PersistentClient(path=CHROMA_PATH)

try:
    cols = client.list_collections()
    print(f"📋 Collections found: {[c.name for c in cols]}")

    col = client.get_collection("pathsetter_docs")
    print(f"✅ Collection 'pathsetter_docs' exists!")
    print(f"Count: {col.count()} documents")
except Exception as e:
    print(f"❌ ERROR accessing collection: {e}")
    print("👉 You need to run 'python -m app.ingest' successfully first.")