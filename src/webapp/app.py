# src/webapp/app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
import os
from src.core.chatbot import chat_once
from src.tools.ingest import ingest_file

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <html><body style="font-family: sans-serif; max-width: 800px; margin: 2rem auto;">
    <h2>AI Academic & Coding Assistant</h2>
    <form id="chat">
      <input name="workspace" placeholder="workspace (course/repo)" required />
      <input name="user_id" placeholder="user id" required />
      <textarea name="msg" rows="4" style="width:100%;" placeholder="Ask me anything..."></textarea>
      <button type="submit">Send</button>
    </form>
    <pre id="out"></pre>
    <hr/>
    <form id="upload" enctype="multipart/form-data">
      <input name="workspace" placeholder="workspace" required />
      <input type="file" name="file" required />
      <button type="submit">Ingest</button>
    </form>
    <script>
    chat.onsubmit = async (e) => {
      e.preventDefault();
      const fd = new FormData(chat);
      const r = await fetch("/chat", {method:"POST", body: fd});
      out.textContent = (await r.json()).reply;
    };
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
    reply = chat_once(workspace, user_id, msg)
    return JSONResponse({"reply": reply})

@app.post("/ingest")
async def ingest(workspace: str = Form(...), file: UploadFile = File(...)):
    path = os.path.join("data", "uploads", file.filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())
    chunks = ingest_file(workspace, path)
    return JSONResponse({"ingested_chunks": chunks, "file": file.filename})
