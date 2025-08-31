# scripts/clear_active_history.py
"""
Clear the active (non-archived) conversation history for a given workspace and user.

Usage:
    python scripts/clear_active_history.py <workspace> <user_id>
"""

import sys
from src.memory.convo_store import clear_history

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/clear_active_history.py <workspace> <user_id>")
        sys.exit(1)

    workspace, user_id = sys.argv[1], sys.argv[2]

    # Clear active history from the store
    clear_history(workspace, user_id)

    print(f"Active history cleared for workspace '{workspace}', user '{user_id}'.")
