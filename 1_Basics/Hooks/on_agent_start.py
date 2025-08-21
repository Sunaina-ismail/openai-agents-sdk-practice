from agents import Agent, ModelSettings, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunHooks, RunContextWrapper, function_tool, AgentHooks,enable_verbose_stdout_logging
from agents.tool import ToolErrorFunction
from dotenv import load_dotenv
from dataclasses import dataclass
from pydantic import BaseModel
from rich import print
from typing import TypeVar, Any
import os

T = TypeVar("T")

load_dotenv()
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()


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

class MyContext(BaseModel):
    name: str
    age: str

@function_tool
def get_user_info(ctx: RunContextWrapper[MyContext]) -> str:
    """Tells the name and and the age of the user"""
    return f"The User name is {ctx.context.name} and age is {ctx.context.age}"

@dataclass
class CustomRunHook(RunHooks[T]):
    async def on_agent_start(self, context: RunContextWrapper[T], agent: Agent[T]) -> None:
        print("Runner hook is started")
    async def on_agent_end(self, context: RunContextWrapper[T], agent: Agent[T], output: Any) -> None:
        print("Runner hook is ended")
        
    async def on_handoff(
        self,context,from_agent,to_agent):
        print("now handoffs i am runner hook handoff")

@dataclass
class CustomAgentHook(AgentHooks[T]):
    async def on_start(self, context: RunContextWrapper[T], agent: Agent[T]) -> None:
        print("Agent hook is started")

    async def on_end(self, context: RunContextWrapper[T], agent: Agent[T], output: Any) -> None:
        print("Agent hook is stopped")
        
    


class NainaClass(AgentHooks):
    async def on_start(self,context,agent):
        print("i am naina")
        
    # async def on_agent_end(self,context,agent,output):
    #     print("i am dunaina")
    
    async def on_handoff(self, context, agent, source):
        print("handoff from agent hook")
    
        
bio_agent = Agent[MyContext](
    name="biology Assistant", 
    instructions="You are a biology assistant.", 
    model=model,
    hooks=NainaClass(),
    model_settings=ModelSettings(max_tokens=10)
)

agent = Agent[MyContext](
    name="Assistant", 
    instructions="""You are a helpful assistant. must handoffs to biology agent if prompt is related to handoff agent.
    """, 
    model=model,
    tools=[get_user_info],
    hooks=NainaClass(),
    handoffs=[bio_agent] ,
    # model_settings=ModelSettings(max_tokens=5) 
)

context: MyContext = MyContext(name="Muhammad Fasih", age="10")
result = Runner.run_sync(agent, "Tell me about cell", hooks=CustomRunHook(), context=context,)
print(result.final_output)

