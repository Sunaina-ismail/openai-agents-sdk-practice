# type: ignore
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
from rich import print
import os
import asyncio
from run import CustomRunner

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

@function_tool
def add(a: int, b: int) ->int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return a + b

agent = Agent(
    name="Mathematician", 
    instructions="You are a helpful assistant", 
    model=model, 
    tools=[add],
)

async def main():
    result = await CustomRunner.run(
        starting_agent=agent,
        input="What is 2 + 2"
    )
    print(result.final_output)

asyncio.run(main())
