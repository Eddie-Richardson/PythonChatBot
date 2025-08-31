# src/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value or not value.strip():
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return value.strip()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "cerebras").strip().lower()
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1-8b")
try:
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
except ValueError:
    raise EnvironmentError("MAX_TOKENS must be an integer")

# Memory
MEMORY_CONFIG = {
    "db_path": Path(os.getenv("CONVO_DB_PATH", "data/convos.db")).resolve(),
    "chroma_dir": str(Path(os.getenv("CHROMA_DIR", "data/chroma")).resolve())
}

# Providers
CEREBRAS_API_KEY = require_env("CEREBRAS_API_KEY")
CEREBRAS_API_URL = os.getenv("CEREBRAS_API_URL", "https://api.cerebras.ai/v1/chat/completions")

# Interfaces
DISCORD_TOKEN = require_env("DISCORD_TOKEN")