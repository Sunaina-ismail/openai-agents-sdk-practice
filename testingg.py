from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings, RunHooks, AgentHooks, RunContextWrapper
from agents.run import RunConfig
from dotenv import load_dotenv
from rich import print
from agents.agent import StopAtTools
import os
from dataclasses import dataclass

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)
config=RunConfig(
    model=model
)
@dataclass
class FakeUser:
    user_name: str | None

class CustomAgentHook(AgentHooks[FakeUser]):
    async def on_start(self, context, agent):
        print(context.context)
        print(context)
        print("agent started")

    async def on_end(self, context, agent, output):
        print("agent ended")

@dataclass
class User:
    name: str | None
    age: int | None
    password: int

user_1 = User(name="Muhammad Fasih", age=19, password=1234)

agent=Agent[User](
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
    model_settings=ModelSettings(
        temperature=1.0
    ),
)

# result=Runner.run_sync(
#     starting_agent=agent,
#     input="greet the user",
#     context=user_1
# )

# print(result.final_output)
# print(result.raw_responses)

data = StopAtTools(
    stop_at_tool_names=["abc"]
)