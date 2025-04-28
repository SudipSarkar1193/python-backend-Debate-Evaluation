from langchain.memory import ConversationBufferWindowMemory
from typing import Dict
import uuid


class MemoryManager:
    def __init__(self, k: int = 5):
        self.session_store: Dict[str, Dict] = {}
        self.k = k

    def create_session(self, topic: str) -> str:
        session_id = str(uuid.uuid4())
        memory = ConversationBufferWindowMemory(
            memory_key="history",
            k=self.k,
            return_messages=True
        )
        self.session_store[session_id] = {
            "topic": topic,
            "memory": memory
        }
        return session_id

    def get_memory(self, session_id: str):
        return "Memory is not implemented yet"

    def get_topic(self, session_id: str) -> str:
        return "dummy-topic"