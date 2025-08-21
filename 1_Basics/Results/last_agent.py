from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

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

math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are good at maths",
    model=model
)

physics_expert_agent = Agent(
    name="Physician", 
    instructions="You are good at physics",
    model=model    
)

confidentional_agent = Agent(
    name="General Knowledge Assistant",
    instructions=(
        "You are a highly intelligent, confident assistant capable of answering questions "
        "across all domains including science, technology, history, philosophy, math, health, and more. "
        "Respond clearly and accurately, and if you're unsure about something, state that honestly."
    ),
    model=model
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[math_expert_agent, physics_expert_agent, confidentional_agent],
    model=model
)

result = Runner.run_sync(starting_agent=triage_agent, input="What is the capital of Pakistan")
print(result.last_agent)
print(result.final_output)