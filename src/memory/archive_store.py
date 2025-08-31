# src/memory/archive_store.py
import sqlite3, time
from typing import List, Dict
from src.config import MEMORY_CONFIG
from dotenv import load_dotenv

load_dotenv()
db_path = MEMORY_CONFIG["db_path"]

def _conn():
    c = sqlite3.connect(db_path)
    c.execute("""CREATE TABLE IF NOT EXISTS archive_messages(
        workspace TEXT, user_id TEXT, ts REAL, role TEXT, content TEXT
    )""")
    return c

def archive_messages(workspace: str, user_id: str, messages: List[Dict]):
    """
    Append a batch of messages to the archive store for long-term storage.
    Each message dict must have 'role' and 'content' keys.
    """
    if not messages:
        return
    c = _conn()
    for m in messages:
        c.execute("INSERT INTO archive_messages VALUES (?,?,?,?,?)",
                  (workspace, user_id, time.time(), m["role"], m["content"]))
    c.commit(); c.close()

def get_archive(workspace: str, user_id: str) -> List[Dict]:
    """
    Retrieve all archived messages for a given workspace/user.
    """
    c = _conn()
    rows = c.execute("""SELECT role, content FROM archive_messages
                        WHERE workspace=? AND user_id=?
                        ORDER BY ts ASC""",
                     (workspace, user_id)).fetchall()
    c.close()
    return [{"role": r[0], "content": r[1]} for r in rows]
