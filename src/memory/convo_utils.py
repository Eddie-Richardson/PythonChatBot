from typing import List, Dict
from src.memory.convo_store import get_history
from src.memory.archive_store import get_archive

def get_full_conversation(workspace: str, user_id: str, expand_summaries: bool = False) -> List[Dict]:
    """
    Retrieve the complete conversation for a given workspace/user.

    Args:
        workspace: KB namespace / conversation grouping
        user_id:   Unique user identifier
        expand_summaries: If True, replace any summary messages in the active store
                          with the archived messages they represent.

    Returns:
        A single chronological list of message dicts:
        [{"role": "user"|"assistant"|"system", "content": "..."}]
    """
    archived = get_archive(workspace, user_id)  # oldest first
    active = get_history(workspace, user_id, limit=9999)  # chronological

    if not expand_summaries:
        return archived + active

    expanded: List[Dict] = []
    for msg in active:
        if msg["role"] == "system" and msg["content"].startswith("Conversation summary:"):
            # Insert archived messages before the summary
            expanded.extend(archived)
            # Optionally keep the summary itself for reference
            expanded.append(msg)
        else:
            expanded.append(msg)

    return expanded

def format_conversation_as_text(messages: List[Dict]) -> str:
    """
    Convert a list of messages into a readable text transcript.
    """
    return "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
