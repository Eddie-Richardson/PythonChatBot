# src/memory/chunking.py
import re, os, textwrap

def chunk_text(text: str, size: int = 800, overlap: int = 150):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+size])
        chunks.append(textwrap.dedent(chunk).strip())
        i += size - overlap
    return chunks
