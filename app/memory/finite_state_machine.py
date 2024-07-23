import json
from pydantic import BaseModel
from typing import List, Generic, TypeVar, Dict
from abc import ABC, abstractmethod
from app.llm.llama_cpp import LLM
from app.memory.global_memory import Memory
from app.tool.ToolAdapter import ToolAdapter
from app.memory.message_state import MemoryState, Message
from app.memory.context import Context

class StateAdapter(ABC):
    @abstractmethod
    def handle(self, context:Context):
        pass




class StateMachine:
    def __init__(self, llm:LLM, memory:Memory, tools: List[ToolAdapter]):
        self.state = MemoryState.THOUGHT
        self.context = Context(llm, memory, tools)
        self.state_handlers: Dict[MemoryState, StateAdapter] = {
            MemoryState.THOUGHT: Thought(),
            MemoryState.ACTION: Action(),
            MemoryState.OBSERVE: Observe()
        }

    def run(self, query: str):
        self.context.set_problem(query)

        while True:
            if self.state == MemoryState.ANSWER:
                break

            self.state = self.state_handlers[self.state].handle(self.context)


class Thought(StateAdapter):
    def handle(self, context:Context):
        tools = [{'name': tool.name, 'description': tool.description} for tool in context.tools]

        prompt = f"""You're a helpful assistant. Given the Problem provided below and any previous thoughts, actions, and observations from the History, generate the next thought to solve the problem.

                Constraints:
                - If you know the answer start your response with "Answer:" otherwise give your thought by starting your response with "Thought:".
                - Do NOT guess the answer! You must use your tools for solving the problem UNLESS the problem cannot be solved by the tools.
                
                Example response for a thought:
                \"\"\"
                Thought: I'll use my Wikipedia tool to get the answer.
                \"\"\"
                
                Example response for an answer:
                \"\"\"
                Answer: I can use my tools to assist with solving your problem.
                \"\"\"
                
                Tools:
                {tools}
                
                History:
                {[message.content for message in context.memory.get_history()]}
                
                Problem:
                {context.problem}
                        """

        response = context.llm.generate(prompt)

        if response.find('Answer') != -1:
            parse_answer = response.split('Answer:')[1]
            context.memory.add_entry(Message(parse_answer, MemoryState.ANSWER))
            return MemoryState.ANSWER
        else:
            parse_answer = response.split('Thought:')[1]
            context.memory.add_entry(Message(parse_answer, MemoryState.THOUGHT))
            return MemoryState.ACTION # TODO: is this state return is correct????


class Action(StateAdapter):
    def handle(self, context:Context):
        prompt= f"""You're a helpful assistant who has knowledge of tools to solve problems. Given the problem and the thought, select an appropriate action to perform. Actions are defined as JSON schemas, use that as a template to generate the action input with valid JSON that matches the schema.

            Problem:
            {context.problem}
            
            Thought:
            {context.memory.get_history()[-1].content}
            
            Tools:
            {[tool.schema() for tool in context.tools]}
            
            Action input:
                    """

        tool_schemas = [tool.schema() for tool in context.tools]
        response = context.llm.generate(prompt, tool_schemas)
        # response = context.llm.generate(prompt)
        parsed_response = json.loads(response)

        tool = [tool for tool in context.tools if tool.name() == parsed_response['name']][0]
        output =tool.execute(parsed_response)
        output_json = json.dumps(output)

        content = f"""
        Action input:
        {parsed_response}

        Action output:
        {output_json}
        """

        context.memory.add_entry(Message(content, MemoryState.OBSERVE))
        return MemoryState.OBSERVE


class Observe(StateAdapter):
    def handle(self, context: Context):
        prompt = f"""You're a helpful assistant who has knowledge of tools to solve problems. Observe the results of the previous action and make an observation on the output whether it is correct based on the history.

            History:
            {[message.content for message in context.memory.get_history()]}
            
            Observation:
                    """
        response = context.llm.generate(prompt)
        context.memory.add_entry(Message(response, MemoryState.THOUGHT))
        return MemoryState.THOUGHT
