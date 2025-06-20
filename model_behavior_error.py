from typing import Any
from pydantic import BaseModel
from rich import print
from agents import RunContextWrapper, FunctionTool, Agent, Runner


# Dummy work function
def do_some_work(data: str) -> str:
    return f"Processed: {data}"


# Arguments schema
class FunctionArgs(BaseModel):
    username: str
    age: int


# Tool function
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


async def run_function_1(ctx: RunContextWrapper[Any]) -> str:
    return "hello"

# Get the schema and patch it
schema = FunctionArgs.model_json_schema()
schema["additionalProperties"] = False  # Required fix

# Define the tool
tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data (username and age).",
    params_json_schema=schema,
    on_invoke_tool=run_function_1,
)

# Define agent
agent = Agent(
    name="UserProcessor",
    instructions="You are an assistant that processes user data using tools when appropriate.",
    tools=[tool]
)

# Run synchronously
result = Runner.run_sync(
    starting_agent=agent,
    input="The user's name is Alice and she is 30 years old."
)
print(agent.tools)
print(result.final_output)
