from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
from rich import print
from typing import Optional
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

# this shows error 
@function_tool(strict_mode=False)
def add(a: int, b: int, reasoning: Optional[str] = None) -> int:
    """Add two numbers

    Args:
        a (int): first number
        b (int): second number
        reasoning (str, optional): reasoning that what are you doing

    Returns:
        int: The sum of the two numbers.
    """
    print(reasoning)
    return a + b


# without error tool 
@function_tool(strict_mode=False)
def add(a: int, b: int, reasoning: str) -> int:
    """
    Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.
        reasoning (str): The reason for performing this operation.

    Returns:
        int: The sum of the two numbers.
    """
    print(f"Reasoning: {reasoning}")
    return a + b


agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert"
    ), 
    model=model, 
    tools=[add],
)

result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)
