# src/webapp/app.py
"""
FastAPI web interface for the AI Academic & Coding Assistant.

This module:
- Serves a minimal HTML UI for local testing (GET /)
- Exposes API endpoints for:
    - /chat   → Send a message to the assistant and get a reply
    - /ingest → Upload and process a file into the workspace's vector store

Local-only notes:
- No authentication or rate limiting — fine for dev, not for public deployment.
- Static HTML is embedded directly in the route for simplicity.
- File uploads are stored under ./data/uploads/ (relative to project root).
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
import os

# Core assistant logic (single-turn chat)
from src.core.chatbot import chat_once

# File ingestion pipeline (splitting, embedding, storing in Chroma)
from src.tools.ingest import ingest_file

# Create FastAPI app instance
app = FastAPI()

@app.get("/")
def home():
    """
    Serve a barebones HTML page for manual testing of chat and file ingestion.
    This is purely for local dev — in production, a separate frontend would be used.
    """
    return HTMLResponse("""
    <!-- Inline HTML for quick local testing -->
    <html><body style="font-family: sans-serif; max-width: 800px; margin: 2rem auto;">
    <h2>AI Academic & Coding Assistant</h2>

    <!-- Chat form -->
    <form id="chat">
      <input name="workspace" placeholder="workspace (course/repo)" required />
      <input name="user_id" placeholder="user id" required />
      <textarea name="msg" rows="4" style="width:100%;" placeholder="Ask me anything..."></textarea>
      <button type="submit">Send</button>
    </form>
    <pre id="out"></pre>

    <hr/>

    <!-- File upload form -->
    <form id="upload" enctype="multipart/form-data">
      <input name="workspace" placeholder="workspace" required />
      <input type="file" name="file" required />
      <button type="submit">Ingest</button>
    </form>

    <script>
    // Handle chat form submission
    chat.onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(chat);
      const r = await fetch("/chat", {method:"POST", body: fd});
      out.textContent = (await r.json()).reply;
    };

    // Handle file upload form submission
    upload.onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(upload);
      const r = await fetch("/ingest", {method:"POST", body: fd});
      alert(JSON.stringify(await r.json()));
    };
    </script>
    </body></html>
    """)

@app.post("/chat")
async def chat(workspace: str = Form(...), user_id: str = Form(...), msg: str = Form(...)):
    """
    Handle a single chat request.
    - workspace: logical grouping (e.g., course name, repo name)
    - user_id:   identifier for the user (could be Discord ID, etc.)
    - msg:       user message to send to the assistant

    Returns:
        JSON: {"reply": <assistant's reply>}
    """
    reply = chat_once(workspace, user_id, msg)
    return JSONResponse({"reply": reply})

@app.post("/ingest")
async def ingest(workspace: str = Form(...), file: UploadFile = File(...)):
    """
    Handle file ingestion into the workspace's vector store.
    - Saves uploaded file under ./data/uploads/
    - Passes file path to ingest_file() for chunking + embedding.

    Returns:
        JSON: {"ingested_chunks": <count>, "file": <filename>}
    """
    # Save uploaded file locally
    path = os.path.join("data", "uploads", file.filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())

    # Process file into vector DB
    chunks = ingest_file(workspace, path)
    return JSONResponse({"ingested_chunks": chunks, "file": file.filename})
