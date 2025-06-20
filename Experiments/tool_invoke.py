from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ModelSettings, RunContextWrapper
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
import os, asyncio

# enable_verbose_stdout_logging()
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

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model, 
    tools=[add],
)
async def main():
    contex=RunContextWrapper(context=None)
    arguments='{"a":2,"b":2}'
    data = await agent.tools[0].on_invoke_tool(contex, arguments)
    print(data)

asyncio.run(main())
