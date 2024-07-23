import os

from langchain_community.llms import OpenAI
from openai import OpenAI
from transitions import Machine

from app.agent_hub.util import get_hardcoded_agent_list


class PM_Agent:
    # TODO: add more states to check the agent feasibility
    # TODO: implement global and local state managemet: i.e. project state, local agent state
    states = ['START', 'RECEIVE_TASK', 'ASSIGN_AGENT', 'REASSIGN_AGENT','COMPLETE_TASK']

    def __init__(self):
        # define state for PM agent
        self.machine = Machine(model=self, states=PM_Agent.states, initial='START')
        self.machine.add_transition(trigger='receive_task', source='START', dest='RECEIVE_TASK')
        self.machine.add_transition(trigger='assign_agent', source='RECEIVE_TASK', dest='ASSIGN_AGENT')
        self.machine.add_transition(trigger='complete_task', source='ASSIGN_AGENT', dest='COMPLETE_TASK')
        self.machine.add_transition(trigger='reassign_task', source='ASSIGN_AGENT', dest='REASSIGN_AGENT')
        self.machine.add_transition(trigger='project_done', source='COMPLETE_TASK', dest='START')

        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        self.current_task = None

    def on_enter_RECEIVE_TASK(self):
        print('receiving task ...')

        # 1. once the task is received, PM agent decide on the agents needed

        # prompt = f"""
        # You're a project manager with the knowledge of creating dynamic agent teams for a given task.
        # Given the task below, generate a maximum 4 agents, each with a name, description, and order of execution, to solve the task.
        # Output the agents as a JSON array, where each agent is an object with the keys "name", "description", "task" and "orderOfExecution".
        #
        # Task:
        # {self.current_task}
        #
        # Agents:
        # """
        #
        # # pass the prompt
        # messages = [
        #     {"role": "system", "content": prompt}
        # ]
        # response = self.llm.chat.completions.create(
        #     model="gpt-4",
        #     messages=messages,
        #     temperature=0.2,
        #     max_tokens=256,
        #     frequency_penalty=0.0
        # )
        # self.agents = generate_agent_list(json.loads(response.choices[0].message.content.strip()))

        # the above code snippet allows to dynamically determine the agent team with tasks assigned. Due to json decorder error added the following hardcoded list of agents for now.
        self.agents = get_hardcoded_agent_list()

    def on_enter_ASSIGN_AGENT(self):
        print('assigning agents ...')
        print(f'number of agents: {len(self.agents)}')

        for agent in self.agents:
            # 2. each agent maintain a local state machine, which trigger based if feasibility is lower than the threshold
            # this will inform the PM agents, where tasks will be re-assigned again
            is_feasible = agent.execute_task()

            if not is_feasible:
                self.reassign_task()

        self.complete_task()

    def on_enter_COMPLETE_TASK(self):
        print('task completed')

    def on_enter_REASSIGN_AGENT(self):
        print('re-assigning non-feasible agents')
