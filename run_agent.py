from app.llm.llama_cpp import LLM
from app.memory.global_memory import Memory
from app.agent.stock_agent import StockTickerPrice
from app.memory.finite_state_machine import StateMachine

llm = LLM()
memory = Memory()
tools = [
    StockTickerPrice()
]

state_machine = StateMachine(llm, memory, tools)
state_machine.run("What's the price of NVDA?")

print("output: ", memory.get_history()[-1].content)
