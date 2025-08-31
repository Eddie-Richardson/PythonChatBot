# src/llm/base.py
from abc import ABC, abstractmethod
from typing import List, Dict

Message = Dict[str, str]  # {"role": "system|user|assistant", "content": "..."}

class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Message], max_tokens: int) -> str:
        ...