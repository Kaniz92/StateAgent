from app.agent_hub.execution_agent import Agent


def generate_agent_list(agents_list):
    agents = []

    for agent_info in agents_list:
        # agent_key = agent_info['name'].lower().replace(" ", "_")
        agent = Agent(agent_info['name'], agent_info["description"], agent_info['task'])
        agents.append(agent)
    #     TODO: add feasibility too
    return agents


def get_hardcoded_agent_list():
    agent_list = [
        {
            'name': 'Developing Agent',
            'description': 'code development',
            'task': 'develop'
        },
        {
            'name': 'Testing Agent',
            'description': 'code test',
            'task': 'test'

        }
    ]

    return generate_agent_list(agent_list)
