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
        if session_id not in self.session_store:
            raise ValueError("Invalid session_id")
        return self.session_store[session_id]["memory"]

    def get_topic(self, session_id: str) -> str:
        if session_id not in self.session_store:
            raise ValueError("Invalid session_id")
        return self.session_store[session_id]["topic"]
    
    def print_current_memory(self, session_id: str):
        """Prints the current conversation memory for a session."""
        if session_id not in self.session_store:
            raise ValueError("Invalid session_id")
        
        memory = self.session_store[session_id]["memory"]
        history = memory.buffer
        
        if not history:
            print("No conversation history yet.")
            return
        
        print(f"Conversation history for session {session_id}:")
        for message in history:
            role = getattr(message, "type", "unknown")
            content = getattr(message, "content", "")
            print(f"[{role}] {content}")