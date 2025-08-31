# src/tools/web.py
import requests
from bs4 import BeautifulSoup
import trafilatura

def fetch_url(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        content = trafilatura.extract(downloaded) or ""
        if content.strip():
            return content
    # fallback
    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text(separator="\n")
