from enum import Enum


class MemoryState(Enum):
    THOUGHT = 1,
    ACTION = 2,
    OBSERVE = 3,
    ANSWER = 4
    # TODO: ADD DELEGATE OR HELP STATE TOO


class Message:
    def __init__(self, content:str, state: MemoryState):
        self.content = content
        self.state = state

