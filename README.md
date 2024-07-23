# StateAgent

This project demonstrate a multi-agent system comprising a Project Manager (PM) and and dynamically generated agent team to accomplish a given task. Each agent is designed to have finite state machine based on different roles. PM Agent consist of states: START, RECEIVE_TASK, ASSIGN_AGENTS, REASSIGN_AGENTS, COMPLETE_TASK and any other agent consist of states: THOUGHT, ACTION, OBSERVE, ANSWER states. A task is received by PM Agent, which trigger to generate and assign agents. Then each agent will run in order while self-observing the feasibility. If the feasibility is lower than a threashold value, then the Agent's state will change to THOUGHT and inform PM Agent, which would change the state to REASSIGN_AGENTS. Then the tasks are re-routes and agents are re-assigned.

![Proposed Model](/model.png "Proposed Model")
## Project Structure

- `Agent`: A class representing an individual agent with attributes for name, description, task, and feasibility.
- `ProjectManagerAgent`: A class representing the PM agent, responsible for generating agent teams and evaluating task feasibility.

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Kaniz92/StateAgent.git
    cd StateAgent
    ```

2. **Install Dependencies**

    Ensure you have Python 3.11 installed. Then, install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up OpenAI API Key**

    Make sure you have an OpenAI API key. You can set it up as an environment variable:

    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

## Usage

run the run_agent_hub.py

## References

base code - https://github.com/alexsniffin/assemble/tree/main

agent_core - https://developer.nvidia.com/blog/introduction-to-llm-agents/

fsm impl - https://github.com/pytransitions/transitions
