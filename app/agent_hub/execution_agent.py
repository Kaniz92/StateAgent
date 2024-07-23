class Agent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute_task(self, task):
        print(f"{self.name} is executing task: {task}")
