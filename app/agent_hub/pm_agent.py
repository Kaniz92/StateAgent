import os
import json

from langchain_community.llms import OpenAI
from openai import OpenAI
from transitions import Machine

from app.agent_hub.execution_agent import Agent

class PM_Agent:
    def __init__(self):
        # TODO: add more states to check the agent feasibility
        # TODO: implement global and local state managemet: i.e. project state, local agent state
        self.states = ['START', 'RECEIVE_TASK', 'ASSIGN_AGENT', 'COMPLETE_TASK']

        # define state for PM agent
        self.machine = Machine(model = self, states = self.states, initial = 'START')
        self.machine.add_transition(trigger='receive_task', source = 'START', dest='RECEIVE_TASK')
        self.machine.add_transition(trigger='assign_agent', source='RECEIVE_TASK', dest='ASSIGN_AGENT')
        self.machine.add_transition(trigger='complete_task', source='ASSIGN_AGENT', dest='COMPLETE_TASK')
        self.machine.add_transition(trigger='project_done', source='COMPLETE_TASK', dest='START')

        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        self.current_task = None


    def generate_agent_list(self, agents_list):
        agents = {}

        for agent_info in agents_list:
            agent_key = agent_info['name'].lower().replace(" ", "_")
            agents[agent_key] = Agent(agent_info['name'], agent_info["description"])
        #     TODO: add feasibility too
        return agents

    def on_enter_RECEIVE_TASK(self):
        print('receiving task ...')
        # 1. once the task is received, PM agent decide on the agents needed
        prompt = f"""
        You're a project manager with the knowledge of creating dynamic agent teams for a given task.
        Given the task below, generate a maximum 4 agents, each with a name, description, and order of execution, to solve the task.
        Output the agents as a JSON array, where each agent is an object with the keys "name", "description", and "orderOfExecution".

        Task:
        {self.current_task}

        Agents:
        """

        # pass the prompt
        messages = [
            {"role": "system", "content": prompt}
        ]
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2,
            max_tokens=256,
            frequency_penalty=0.0
        )

        self.agents = self.generate_agent_list(json.loads(response.choices[0].message.content.strip()))


    def on_enter_ASSIGN_AGENT(self):
        print('assigning agents ...')
        task_type = self.parse_task(self.current_task)
        # task_type = 'development_agent'
        self.assign_agent(task_type)

    def on_enter_COMPLETE_TASK(self):
        print('task completed')
        self.complete_task()

    def parse_task(self, task_description):
        # TODO: add prompt templating to get task description
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

    def assign_agent(self, task_type):
        agent = self.agents.get(task_type)
        if agent:
            agent.execute_task(task_type)
        else:
            print("No agent available for this task type.")
        self.complete_task()


    def complete_task(self):
        print('task completed!')


    def project_done(self):
        print('project done!')
