# scripts/list_users.py
"""
List all distinct user IDs for a given workspace.

Usage:
    python scripts/list_users.py <workspace>
"""

import sys, sqlite3
from src.config import MEMORY_CONFIG

db_path = MEMORY_CONFIG["db_path"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/list_users.py <workspace>")
        sys.exit(1)

    workspace = sys.argv[1]

    # Query DB for all unique user IDs in the given workspace
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT DISTINCT user_id FROM messages WHERE workspace=?",
        (workspace,)
    ).fetchall()
    conn.close()

    print(f"Users in workspace '{workspace}':")
    for (uid,) in rows:
        print(f"- {uid}")
