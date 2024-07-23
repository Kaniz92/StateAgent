from app.llm.llama_cpp import LLM
from app.memory.global_memory import Memory
from app.tool.ToolAdapter import ToolAdapter
from app.memory.message_state import MemoryState
from typing import List, Generic, TypeVar, Dict


class Context:
    def __init__(self, llm: LLM, memory: Memory, tools: List[ToolAdapter]):
        self.problem = None
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def set_problem(self, problem: str):
        self.problem = problem
