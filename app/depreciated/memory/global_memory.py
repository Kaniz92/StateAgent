from app.depreciated.memory.message_state import Message
from typing import List


class Memory:
    def __init__(self):
        self.history: List[Message] = []

    def add_entry(self, entry:Message):
        self.history.append(entry)

    def get_history(self) -> List[Message]:
        return self.history
