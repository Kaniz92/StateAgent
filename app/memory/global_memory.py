from app.memory.message_state import Message
from typing import List, Generic, TypeVar, Dict

class Memory:
    def __init__(self):
        self.history: List[Message] = []

    def add_entry(self, entry:Message):
        self.history.append(entry)

    def get_history(self) -> List[Message]:
        return self.history
