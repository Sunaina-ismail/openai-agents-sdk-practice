from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelResponse
from dotenv import load_dotenv
# from rich import print
import os

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

agent = Agent(
    name="Mathematician", 
    instructions="You are a helpful assistant", 
    model=model, 
)

result = Runner.run_sync(starting_agent=agent, input="What is the capital of Pakistan")
print(result)
