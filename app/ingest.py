import os
from typing import List
from dotenv import load_dotenv
import chromadb

load_dotenv()

# We only need Groq for the chat part later, not for ingestion anymore.
# Chroma will handle embeddings locally.

chroma_client = chromadb.PersistentClient(path="chroma_store")
COLLECTION_NAME = "pathsetter_docs"

def load_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def split_text(text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def main():
    print("🚀 Starting ingestion...")

    # 1. Load text
    # Make sure this matches your actual file name!
    raw_text = load_text("data/pathsetter_alfred_knowledge.md")

    # 2. Split into chunks
    chunks = split_text(raw_text)
    print(f"📦 Created {len(chunks)} chunks.")

    # 3. Create / get Chroma collection
    # We do NOT pass an embedding function, so Chroma uses the default (all-MiniLM-L6-v2)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    # 4. Generate IDs
    ids = [f"chunk-{i}" for i in range(len(chunks))]

    # 5. Add to collection (Chroma computes embeddings automatically now!)
    collection.add(
        ids=ids,
        documents=chunks
    )

    print("✅ Ingestion complete. Data stored in 'chroma_store'.")

if __name__ == "__main__":
    main()
    