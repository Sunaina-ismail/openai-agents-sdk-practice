from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, RunContextWrapper
from dotenv import load_dotenv
from rich import print
import os, asyncio

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    model=model,
    handoff_description="Handles all physics-related queries and theoretical explanations."
)

async def main():
    ctx=RunContextWrapper(context=None)
    handoff_=handoff(physics_expert_agent)
    handoff_agent = await handoff_.on_invoke_handoff(ctx, '{}')
    print(handoff_agent)

asyncio.run(main())