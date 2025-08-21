# from datetime import datetime
from typing_extensions import TypedDict
from agents import Agent, RunConfig, RunContextWrapper, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, Runner,enable_verbose_stdout_logging
from agents.agent import StopAtTools 
from rich import print
import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


class Location(TypedDict):
    city: str
    country: str

@function_tool
async def get_current_location(ctx:RunContextWrapper) -> str:
    """
    Returns the current location of the user.
    """
    return "Karachi"

class Location(TypedDict):
    city:str

@function_tool(docstring_style="")  
async def fetch_weather(city: Location) -> str:
    
    """Fetch the weather for a given city.

    Args:
        city: The city to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    return "sunny"


plant_agent = Agent(
    name="plant_agent",
    instructions="You are a plant specialist.",
    model=model
)


# my_tool= StopAtTools(
#             stop_at_tool_names=[plant_agent]
#         )

agent = Agent(
    name="Assistant",
   instructions = """
You are a helpful assistant.  
You have tools available use them when the user asks a specific query.  
If the user asks for a task that should be handled by another agent, you can hand it off to that agent.  
Do not stop until all of the user's queries have been answered.
    """,
    tools=[get_current_location, fetch_weather], 
    handoffs=[plant_agent],
    model=model,
    # tool_use_behavior=my_tool
)


result = Runner.run_sync(
    agent,
    """ 1. What is my current location?
        2. what is the weather of Karachi?
        3. What is photosynthesis?
    """,
    # run_config=config
)

print('='*50)
print("Result: ",result.last_agent.name)
print(result.new_items)
print("Result: ",result.final_output)










# You are a helpful assistant.

# You have access to special tools — use them whenever the user asks something related.

# - You have access to special tools. Use them **whenever needed**.
# - use tools you do not answr own your own.


# Do not stop until all of the user's queries have been answered.
# class Location(TypedDict):
#     city:str

# @function_tool(docstring_style="")  
# async def fetch_weather(city: Location) -> str:
    
#     """Fetch the weather for a given city.

#     Args:
#         city: The city to fetch the weather for.
#     """
#     # In real life, we'd fetch the weather from a weather API
#     return "sunny"


# @function_tool()  
# async def get_time() -> str:
    
#     """Get current time.
#     """
    
#     time = datetime.now()
#     # In real life, we'd fetch the weather from a weather API
#     return time




# @function_tool(name_override="fetch_data")  
# def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
#     """Read the contents of a file.

#     Args:
#         path: The path to the file to read.
#         directory: The directory to read the file from.
#     """
#     # In real life, we'd read the file from the file system
    # return "<file contents>"
    
    
    

# for tool in agent.tools:
#     if isinstance(tool, FunctionTool):
#         print(tool.name)
#         print(tool.description)
#         print(tool.params_json_schema)
