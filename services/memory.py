class MemoryManager:
    def __init__(self, k: int = 5):
        self.k = k
        pass

    def create_session(self, topic: str) -> str:
        return "dummy-session-id - " + topic

    def get_memory(self, session_id: str):
        return "Memory is not implemented yet"

    def get_topic(self, session_id: str) -> str:
        return "dummy-topic"