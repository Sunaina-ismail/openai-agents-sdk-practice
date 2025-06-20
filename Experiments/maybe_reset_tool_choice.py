from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings
from agents._run_impl import AgentToolUseTracker, RunImpl
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
import os

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

tool_use_tracker=AgentToolUseTracker()

#? CASE 01
# first_agent = Agent(
#     name="Mathematician", 
#     instructions="You are math expert", 
#     model=model,
#     model_settings=ModelSettings(
#         tool_choice="required"
#     ),
#     reset_tool_choice=True
# )
# print(first_agent.model_settings) #! Orignal model_settings of first_agent

# tool_use_tracker.add_tool_use(agent=first_agent, tool_names=[]) 

# model_settings=RunImpl().maybe_reset_tool_choice(
#     agent=first_agent,
#     model_settings=first_agent.model_settings,
#     tool_use_tracker=tool_use_tracker
# )
# print(model_settings) #! Remains same because tool_names is empty + reset_tool_choice is True


# #? CASE 02
second_agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model,
    model_settings=ModelSettings(
        tool_choice="required"
    ),
    reset_tool_choice=True
)

print(second_agent.model_settings) #! Orignal model_settings of second_agent

tool_use_tracker.add_tool_use(agent=second_agent, tool_names=["dummy"]) 
model_settings=RunImpl().maybe_reset_tool_choice(
    agent=second_agent,
    model_settings=second_agent.model_settings,
    tool_use_tracker=tool_use_tracker
)
print(model_settings) #! model setting is overrided (tool_choice=None) because tool_names has the tool_name + reset_tool_choice is True

# #? CASE 03
# third_agent = Agent(
#     name="Mathematician", 
#     instructions="You are math expert", 
#     model=model,
#     model_settings=ModelSettings(
#         tool_choice="required"
#     ),
#     reset_tool_choice=False
# )

# print(third_agent.model_settings) #! Orignal model_settings of second_agent

# tool_use_tracker.add_tool_use(agent=third_agent, tool_names=["dummy"]) 
# model_settings=RunImpl().maybe_reset_tool_choice(
#     agent=third_agent,
#     model_settings=third_agent.model_settings,
#     tool_use_tracker=tool_use_tracker
# )
# print(model_settings) #! model setting remains same because reset_tool_choice is False


