# src/memory/convo_store.py
import sqlite3, json, time
from typing import List, Dict
from src.config import MEMORY_CONFIG
from dotenv import load_dotenv

load_dotenv()
db_path = MEMORY_CONFIG["db_path"]

def _conn():
    c = sqlite3.connect(db_path)
    c.execute("""CREATE TABLE IF NOT EXISTS messages(
        workspace TEXT, user_id TEXT, ts REAL, role TEXT, content TEXT
    )""")
    return c

def save_message(workspace: str, user_id: str, role: str, content: str):
    c = _conn()
    c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",
              (workspace, user_id, time.time(), role, content))
    c.commit(); c.close()

def get_history(workspace: str, user_id: str, limit: int = 30) -> List[Dict]:
    c = _conn()
    rows = c.execute("""SELECT role, content FROM messages
                        WHERE workspace=? AND user_id=?
                        ORDER BY ts DESC LIMIT ?""", (workspace, user_id, limit)).fetchall()
    c.close()
    return [{"role": r[0], "content": r[1]} for r in rows[::-1]]
