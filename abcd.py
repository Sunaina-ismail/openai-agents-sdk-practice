from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a + b


@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    Args:
        a: the first number
        b: the second number
    """
    return a - b

agent=Agent(
   name="Mathematician",
   instructions=(
       "You are a math expert. You have tools to perform calculation"
       "You are a math expert agent. You must call tools **ONE BY ONE**"
   ),
   tools=[add, subtract],
   model=model,
   tool_use_behavior="stop_on_first_tool"
)

result=Runner.run_sync(
    starting_agent=agent,
    input="Tell me the sum of 10 and 20, furthermore the difference of 20 and 2"
)
print(result.final_output)