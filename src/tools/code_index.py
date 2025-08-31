# src/tools/code_index.py
"""
code_index.py
-------------
Indexes your codebase into a Chroma vector store for semantic search.

Usage:
    python -m src.tools.code_index
"""

import os
from pathlib import Path
from typing import List

from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# === CONFIG ===
SRC_DIR = Path(__file__).resolve().parents[1]  # points to src/
DATA_DIR = SRC_DIR.parent / "data" / "chroma"
COLLECTION_NAME = "code_index"

# Cerebras embedding function placeholder
# Replace with your actual embedding call
def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Given a list of strings, return a list of embedding vectors.
    Swap this out with your Cerebras embedding API call.
    """
    # Example: return cerebras_client.embed(texts)
    raise NotImplementedError("Hook up to Cerebras embedding API here.")

# === FILE LOADING ===
def get_python_files(base_dir: Path) -> List[Path]:
    """Recursively find all .py files under base_dir."""
    return [p for p in base_dir.rglob("*.py") if p.is_file()]

def read_file(path: Path) -> str:
    """Read file contents as UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

# === CHUNKING ===
def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """
    Naive chunker: splits text into ~max_chars segments.
    You can replace with a smarter splitter (e.g., by function/class).
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks

# === INDEXING ===
def index_code():
    # Init Chroma client
    client = Client(Settings(
        persist_directory=str(DATA_DIR)
    ))

    # Create or get collection
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except:
        collection = client.create_collection(COLLECTION_NAME)

    # Gather files
    py_files = get_python_files(SRC_DIR)
    print(f"Found {len(py_files)} Python files to index.")

    ids, docs, metas = [], [], []

    for file_path in py_files:
        content = read_file(file_path)
        if not content.strip():
            continue

        for i, chunk in enumerate(chunk_text(content)):
            ids.append(f"{file_path.name}-{i}")
            docs.append(chunk)
            metas.append({"file": str(file_path), "chunk": i})

    # Embed
    print("Generating embeddings...")
    embeddings = embed_texts(docs)

    # Add to Chroma
    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metas,
        embeddings=embeddings
    )

    client.persist()
    print(f"Indexed {len(docs)} chunks into '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    index_code()
