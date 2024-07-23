from transitions import Machine


class Agent:
    states = ['THOUGHT', 'ACTION', 'OBSERVE', 'ANSWER']

    def __init__(self, name, description, task):
        self.name = name
        self.description = description
        self.task = task
        # TODO: for now feasibility default value is 10, but this needs to be updated during the project execution
        self.feasibility = 10

        self.machine = Machine(model=self, states=Agent.states, initial='THOUGHT')
        self.machine.add_transition(trigger='execute_task', source='THOUGHT', dest='ACTION')
        self.machine.add_transition(trigger='observe_feasibility', source='ACTION', dest='OBSERVE')
        self.machine.add_transition(trigger='feasibility_fail', source='OBSERVE', dest='THOUGHT')
        self.machine.add_transition(trigger='complete_task', source='ACTION', dest='ANSWER')

    def on_enter_THOUGHT(self):
        print(f"{self.name} is starting task: {self.task}")

    def on_enter_ACTION(self):
        # TODO: need to implement a proper algorithm for feasibility analysis
        print(f"{self.name} is executing task: {self.task}")
        return self.observe_feasibility()

    def on_enter_OBSERVE(self):
        print('feasibility fail, informing PM agent...')

    def on_enter_ANSWER(self):
        print('project done ...')
