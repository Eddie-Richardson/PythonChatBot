# scripts/test_cerebras.py
import logging
from src.llm.cerebras_client import CerebrasClient
from src.config import CEREBRAS_API_URL, LLM_MODEL

# Configure logging here so it applies globally
logging.basicConfig(
    level=logging.DEBUG,  # Change to INFO for less verbosity
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    print(f"Using Cerebras endpoint: {CEREBRAS_API_URL}")
    print(f"Model: {LLM_MODEL}")

    client = CerebrasClient()

    messages = [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Say hello from Cerebras."}
    ]

    try:
        response = client.chat(messages)
        print("\n--- Model Response ---")
        print(response)
    except Exception as e:
        print("\n--- Error ---")
        print(e)

if __name__ == "__main__":
    main()
