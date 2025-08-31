# src/tools/ingest.py
import os
from typing import List
from pypdf import PdfReader
from docx import Document
from src.memory.kb_store import add_docs
from src.memory.chunking import chunk_text

def ingest_file(workspace: str, path: str):
    ext = os.path.splitext(path)[1].lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(path)
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    elif ext == ".docx":
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
    elif ext in (".md", ".txt"):
        text = open(path, "r", encoding="utf-8", errors="ignore").read()
    else:
        raise ValueError("Unsupported file type")
    chunks = chunk_text(text)
    add_docs(workspace, chunks, [{"workspace": workspace, "source": os.path.basename(path)} for _ in chunks])
    return len(chunks)
