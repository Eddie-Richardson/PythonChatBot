# src/core/chatbot.py
from typing import List, Dict
from src.config import LLM_PROVIDER, MAX_TOKENS
from src.core.prompts import SYSTEM_ACADEMIC_CODING
from src.llm.cerebras_client import CerebrasClient
from src.memory.convo_store import save_message, get_history
from src.memory.kb_store import search

def _client():
    return CerebrasClient()

def build_messages(workspace: str, user_id: str, user_input: str, kb_snippets: List[str]):
    messages: List[Dict[str,str]] = [{"role": "system", "content": SYSTEM_ACADEMIC_CODING}]
    # Add knowledge snippets as context
    if kb_snippets:
        context = "\n\n".join(f"- {s}" for s in kb_snippets)
        messages.append({"role": "system", "content": f"Context from knowledge base:\n{context}"})
    messages += get_history(workspace, user_id, limit=20)
    messages.append({"role": "user", "content": user_input})
    return messages

def retrieve_kb(workspace: str, query: str, k: int = 5):
    hits = search(workspace, query, k=k)
    texts = [h["text"] for h in hits]
    return texts

def chat_once(workspace: str, user_id: str, user_input: str) -> str:
    kb = retrieve_kb(workspace, user_input, k=5)
    messages = build_messages(workspace, user_id, user_input, kb)
    reply = _client().chat(messages, max_tokens=MAX_TOKENS)
    save_message(workspace, user_id, "user", user_input)
    save_message(workspace, user_id, "assistant", reply)
    return reply

def summarize_history_if_long(workspace: str, user_id: str):
    hist = get_history(workspace, user_id, limit=60)
    if len(hist) < 40:
        return
    prompt = [
        {"role": "system", "content": "Summarize the prior conversation into concise bullet points capturing facts, decisions, and TODOs."},
        {"role": "user", "content": "\n\n".join(f"{m['role']}: {m['content']}" for m in hist[:-10])}
    ]
    summary = HFClient().chat(prompt, max_tokens=220)
    save_message(workspace, user_id, "system", f"Conversation summary:\n{summary}")
