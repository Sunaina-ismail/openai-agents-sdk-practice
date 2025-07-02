from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from rich import print
import os
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

agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert"
    ), 
    model=model, 
    output_type=int
)
result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
print(result.final_output)
