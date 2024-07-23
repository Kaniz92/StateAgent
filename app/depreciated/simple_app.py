from transitions import Machine
# from langchain import LLM, OpenAI
from transitions import Machine
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class ProjectManagerAgent:
    states = ['IDLE', 'RECEIVING_TASK', 'ASSIGNING_AGENT', 'COMPLETED']

    def __init__(self):
        self.machine = Machine(model=self, states=ProjectManagerAgent.states, initial='IDLE')
        self.machine.add_transition(trigger='receive_task', source='IDLE', dest='RECEIVING_TASK')
        self.machine.add_transition(trigger='assign_agent', source='RECEIVING_TASK', dest='ASSIGNING_AGENT')
        self.machine.add_transition(trigger='complete_task', source='ASSIGNING_AGENT', dest='COMPLETED')
        self.machine.add_transition(trigger='reset', source='COMPLETED', dest='IDLE')

        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.agents = {
            'design': Agent('Design Agent'),
            'development': Agent('Development Agent'),
            'testing': Agent('Testing Agent')
        }
        self.current_task = None

    def on_enter_RECEIVING_TASK(self):
        print("Receiving task...")

    def on_enter_ASSIGNING_AGENT(self):
        print("Assigning agent...")
        task_type = self.parse_task(self.current_task)
        self.assign_agent_for_task(task_type)

    def on_enter_COMPLETED(self):
        print("Task completed!")

    def parse_task(self, task_description):
        # response = self.llm(task_description)
        # Simplified response handling
        messages = [
            {"role": "system", "content": task_description}
        ]
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=256,
            frequency_penalty=0.0
        )

        print(response)
        return response['task_type']

    def assign_agent_for_task(self, task_type):
        agent = self.agents.get(task_type)
        if agent:
            agent.execute_task(task_type)
        else:
            print("No agent available for this task type.")
        self.complete_task()


class Agent:
    def __init__(self, name):
        self.name = name

    def execute_task(self, task):
        print(f"{self.name} is executing task: {task}")


# Example usage
pm_agent = ProjectManagerAgent()
pm_agent.current_task = "We need to design a new website layout."
pm_agent.receive_task()
# pm_agent.assign_agent()

