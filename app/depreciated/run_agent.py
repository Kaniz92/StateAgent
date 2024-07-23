from langchain import OpenAI

llm = OpenAI(model = "text-davinci-003")

# llm = LLM()
# memory = Memory()
# tools = [
#     StockTickerPrice()
# ]
#
# state_machine = StateMachine(llm, memory, tools)
# state_machine.run("What's the price of NVDA?")
#
# print("output: ", memory.get_history()[-1].content)
