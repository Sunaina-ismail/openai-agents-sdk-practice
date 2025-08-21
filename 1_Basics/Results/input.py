from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

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

agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
result = Runner.run_sync(agent, "Hello")
print(result.final_output)

#* It prints the user prompt (The value of input given in Runner.run_sync)
print(result.input)

#!OUTPUT:
#? Hello