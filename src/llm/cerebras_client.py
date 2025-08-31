# src/llm/cerebras.py
import os
import time
import random
import logging
import requests
from typing import List
from .base import LLMClient, Message
from src.config import (
    CEREBRAS_API_KEY,
    LLM_MODEL,
    MAX_TOKENS,
    CEREBRAS_API_URL
)

# Module-level logger (configured in your app entrypoint)
logger = logging.getLogger(__name__)

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))

class CerebrasClient(LLMClient):
    def chat(self, messages: List[Message], max_tokens: int = MAX_TOKENS) -> str:
        """
        Send a chat completion request to the Cerebras API.

        Args:
            messages: List of Message objects or dicts with 'role' and 'content'.
            max_tokens: Maximum tokens to generate in the response.

        Returns:
            The model's reply as a string, or an error message.
        """
        headers = {
            "Authorization": f"Bearer {CEREBRAS_API_KEY}",
            "Content-Type": "application/json"
        }

        # Ensure messages are in the correct format
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": m["role"], "content": m["content"]}
                if isinstance(m, dict)
                else {"role": m.role, "content": m.content}
                for m in messages
            ],
            "max_tokens": max_tokens,
            "temperature": TEMPERATURE
        }

        for attempt in range(MAX_RETRIES):
            logger.debug(f"[CerebrasClient] Attempt {attempt+1}/{MAX_RETRIES} → POST {CEREBRAS_API_URL}")

            try:
                r = requests.post(CEREBRAS_API_URL, headers=headers, json=payload, timeout=120)
            except requests.RequestException as e:
                logger.error(f"[CerebrasClient] Request failed: {e}")
                time.sleep((2 ** attempt) + random.uniform(0, 1))
                continue

            logger.debug(f"[CerebrasClient] Status: {r.status_code}")

            # Retry on rate limit or service unavailable
            if r.status_code in (429, 503):
                logger.warning("[CerebrasClient] Rate/service limit hit. Retrying...")
                time.sleep((2 ** attempt) + random.uniform(0, 1))
                continue

            # Handle non-OK responses
            if not r.ok:
                try:
                    err = r.json()
                except Exception:
                    err = r.text
                logger.error(f"[CerebrasClient] Error {r.status_code}: {err}")
                return f"Error {r.status_code}: {err}"

            # Parse JSON
            try:
                out = r.json()
                logger.debug(f"[CerebrasClient] Response JSON: {out}")
            except Exception:
                logger.error("[CerebrasClient] Failed to parse JSON")
                return r.text.strip()

            # Return first choice if available
            if "choices" in out and out["choices"]:
                return out["choices"][0]["message"]["content"].strip()

            # Unexpected payload — log and retry
            logger.warning(f"[CerebrasClient] No 'choices' in response: {out}")
            time.sleep((2 ** attempt) + random.uniform(0, 1))

        return "The model is busy. Please try again shortly."
