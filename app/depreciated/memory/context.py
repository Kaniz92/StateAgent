from app.depreciated.llm.llama_cpp import LLM
from app.depreciated.memory.global_memory import Memory
from app.depreciated.tool.ToolAdapter import ToolAdapter
from typing import List


class Context:
    def __init__(self, llm: LLM, memory: Memory, tools: List[ToolAdapter]):
        self.problem = None
        self.llm = llm
        self.memory = memory
        self.tools = tools

    def set_problem(self, problem: str):
        self.problem = problem
