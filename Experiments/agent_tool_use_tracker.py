from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging
from agents._run_impl import AgentToolUseTracker
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
import os
from agents.extensions.visualization import draw_graph

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

class OutputType(BaseModel):
    result: str

agent1 = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model, 
)
agent2 = Agent(
    name="Physics Master", 
    instructions="You are physics expert", 
    model=model, 
)

tool_use_tracker=AgentToolUseTracker()
print(tool_use_tracker)


tool_use_tracker.add_tool_use(agent=agent1, tool_names=[]) 
print(tool_use_tracker.agent_to_tools)
print(tool_use_tracker.has_used_tools(agent=agent1)) #! False because tool_names array is empty


tool_use_tracker.add_tool_use(agent=agent2, tool_names=["search"]) 
print(tool_use_tracker.agent_to_tools)
print(tool_use_tracker.has_used_tools(agent=agent2)) #! True because tool_names has tool


