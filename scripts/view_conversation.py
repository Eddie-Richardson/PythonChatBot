# scripts/view_conversation.py
"""
View the full conversation history for a given workspace and user.

This script pulls both active and archived messages from the memory store
and prints them in two formats:
1. With summaries (compact view)
2. Fully expanded (every turn in detail)

Usage:
    python scripts/view_conversation.py <workspace> <user_id>
"""

import sys
from src.memory.convo_utils import get_full_conversation, format_conversation_as_text

if __name__ == "__main__":
    # Require exactly two arguments: workspace and user_id
    if len(sys.argv) != 3:
        print("Usage: python scripts/view_conversation.py <workspace> <user_id>")
        sys.exit(1)

    workspace, user_id = sys.argv[1], sys.argv[2]

    # Compact view with summaries
    print("=== FULL CONVERSATION (with summaries) ===")
    print(format_conversation_as_text(get_full_conversation(workspace, user_id)))

    # Expanded view with all turns
    print("\n=== FULL CONVERSATION (expanded raw turns) ===")
    print(format_conversation_as_text(get_full_conversation(workspace, user_id, expand_summaries=True)))
