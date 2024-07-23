# StateAgent

This project demonstrates a multi-agent system where a Project Manager (PM) agent creates a dynamic team of agents to accomplish a given task. Each agent is assigned a specific role and task, and the PM agent evaluates the feasibility of each agent completing their assigned task using a language model (LLM) like OpenAI's GPT-4.

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

    run run_agent_hub.py

## References

base code - https://github.com/alexsniffin/assemble/tree/main

agent_core - https://developer.nvidia.com/blog/introduction-to-llm-agents/

fsm impl - https://github.com/pytransitions/transitions
