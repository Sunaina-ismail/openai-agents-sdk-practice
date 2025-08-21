from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.run import RunConfig
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",   
)

@function_tool()

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)
config=RunConfig(
    model=model
)

agent = Agent(
    name="MatchFounder",
    instructions="",
    model=model
)

result = Runner.run_sync(agent,"Find a match whose age is more than 22")

print(result.final_output)