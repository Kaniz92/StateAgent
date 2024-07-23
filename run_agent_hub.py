from dotenv import load_dotenv

from app.agent_hub.pm_agent import PM_Agent

load_dotenv()

pm_agent = PM_Agent()
pm_agent.current_task = "We need to design a new website layout."
pm_agent.receive_task()
pm_agent.assign_agent()
