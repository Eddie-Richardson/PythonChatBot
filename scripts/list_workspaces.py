# scripts/list_workspaces.py
"""
List all distinct workspaces stored in the message database.

Usage:
    python scripts/list_workspaces.py
"""

import sqlite3
from src.config import MEMORY_CONFIG

# Path to SQLite database from config
db_path = MEMORY_CONFIG["db_path"]

if __name__ == "__main__":
    # Connect to DB and fetch all unique workspaces
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT DISTINCT workspace FROM messages").fetchall()
    conn.close()

    print("Workspaces:")
    for (ws,) in rows:
        print(f"- {ws}")

