from agents import Agent, FunctionTool, RunContextWrapper, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ModelSettings
from dotenv import load_dotenv
from rich import print
# from pydantic import BaseModel
import os
import inspect
import json
from typing import Any


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
    model="gemini-2.0-flash",
)


# @function_tool(name_override="add")
# def add(a: int, b: int) -> int:
#     """Add two numbers
#     Args:
#         a: first number
#         b: second number
        
#     Returns:
#         int: The sum of the two numbers.
#     """

#     return a + b


# raise error in tool to get the sdk own error default_tool_error_function
@function_tool(name_override="add")
def add(a: int, b: int) -> int:
    """Add two numbers with intentional error for testing error handler."""
    raise ValueError("Intentional error to test error handling")
    return a + b


# 1st way of creating tool 
@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The difference of the two numbers.
    """

    return a - b



# ***** Log all the detail of a tool to see how function_tool is wrapped in a FunctionTool ******

# def log_tool_details(tool):
#     print(f"[bold yellow]Tool:[/bold yellow] {tool.name}")
#     print(f"[bold green]Description:[/bold green] {tool.description}")
#     print(f"[bold cyan]Params Schema:[/bold cyan] {tool.params_json_schema}")
#     print(f"[bold magenta]Strict Schema:[/bold magenta] {tool.strict_json_schema}")

#     if tool.on_invoke_tool:
#         print("[bold blue]On Invoke Tool Hook (name):[/bold blue]", tool.on_invoke_tool.__name__)
#         print("[bold white]On Invoke Tool Source:[/bold white]")
#         try:
#             source = inspect.getsource(tool.on_invoke_tool)
#             print(source)
#         except OSError:
#             print("Source not available (might be a lambda or built-in).")
#     else:
#         print("No invoke tool hook defined.")

# print("\n[bold underline]Logging Tool Info[/bold underline]\n")
# for tool in [add, subtract]:
#     log_tool_details(tool)
#     print("-" * 80)




# a function to pass in the FunctionTool which sdk itself create if we use function_tool for creating tool 

async def on_invoke_tool(context: RunContextWrapper[Any], args: str) -> str:
    try:
        parsed_args = json.loads(args)
        return f"Tool ran successfully with arguments: {parsed_args}"

    except Exception as e:
        return f"Error while running tool: {str(e)}"



# 2nd way to creating tool 
my_tool = FunctionTool(
    name="multiplication",
    description="A tool that multiply the params",
    params_json_schema={
                'properties': {
                    'a': {'description': 'first number', 'title': 'A', 'type': 'integer'},
                    'b': {'description': 'second number', 'title': 'B', 'type': 'integer'}
                },
                'required': ['a', 'b'],
                'title': 'muliplication_args',
                'type': 'object',
                'additionalProperties': False
            },
    on_invoke_tool=on_invoke_tool,
    strict_json_schema=True 
)


agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert just answer by using the provided tools. if not provided then simply say sorry"
        "You also greet back peoples if they greet you. not do any other activity"
    ), 
    model=model, 
    tools=[my_tool,add],
    tool_use_behavior="stop_on_first_tool"
    # model_settings=ModelSettings(
    #     tool_choice="subtract"
    # ),
)


# log all the detail of a tool 
for tool in agent.tools:
    print(f"[bold underline]Tool: {tool.name}[/bold underline]\n")
    print(f"[green]Description:[/green] {tool.description}")
    print(f"[green]Params Schema:[/green] {tool.params_json_schema}")
    print(f"[green]Strict Schema:[/green] {tool.strict_json_schema}")
    print(f"[green]On Invoke Tool Hook:[/green] {tool.on_invoke_tool}")
    print("\n" + "-" * 40 + "\n")

result = Runner.run_sync(starting_agent=agent, input="Hello, what is sum of 2 and 6")
print(result.final_output)
