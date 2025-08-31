# scripts/dump_archive.py
"""
Export all archived messages for a given workspace and user to a JSON file.

Usage:
    python scripts/dump_archive.py <workspace> <user_id>
"""

import sys, json
from src.memory.archive_store import get_archive

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/dump_archive.py <workspace> <user_id>")
        sys.exit(1)

    workspace, user_id = sys.argv[1], sys.argv[2]

    # Retrieve archived messages
    archive = get_archive(workspace, user_id)

    # Save to JSON file
    filename = f"archive_{workspace}_{user_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(archive, f, indent=2, ensure_ascii=False)

    print(f"Archived messages saved to {filename}")

