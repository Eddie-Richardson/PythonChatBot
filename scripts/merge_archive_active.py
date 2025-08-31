# scripts/merge_archive_active.py
"""
Merge active and archived conversation history into a single transcript file.

This script:
- Retrieves both active and archived messages
- Expands summaries into full turns
- Outputs a timestamped .txt file containing the merged transcript

Usage:
    python scripts/merge_archive_active.py <workspace> <user_id>
"""

import sys
from datetime import datetime
from src.memory.convo_utils import get_full_conversation, format_conversation_as_text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/merge_archive_active.py <workspace> <user_id>")
        sys.exit(1)

    workspace, user_id = sys.argv[1], sys.argv[2]

    # Retrieve merged conversation (active + archive, expanded)
    merged = get_full_conversation(workspace, user_id, expand_summaries=True)

    # Format as plain text
    transcript = format_conversation_as_text(merged)

    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"merged_conversation_{workspace}_{user_id}_{timestamp}.txt"

    # Save transcript to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Merged conversation saved to {filename}")
