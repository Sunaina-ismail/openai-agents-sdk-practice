from dataclasses import dataclass
from typing import Any
from agents import Agent, Handoff, RunContextWrapper, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from rich import print
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
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    model=model,
    handoff_description="Handles all mathematical questions and calculations."
)

@dataclass
class UserContext:
    name:str
        
physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    model=model,
    handoff_description="Handles all physics-related queries and theoretical explanations."
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
async def tech_on_invoke(ctx: RunContextWrapper[Any], args_json: str):
    return Agent[UserContext](
        name="tech_agent",
        instructions="You are a tech support expert. Help the user with technical issues.",
        model=model
    )


tech_handoff = Handoff[UserContext](
    tool_name="transfer_to_tech",
    tool_description="Send to technical support for login or bug-related issues.",
    input_json_schema={
        "type": "object",
        "properties": {"issue": {"type": "string"}},
        "required": ["issue"]
    },
    on_invoke_handoff=tech_on_invoke,
    agent_name="tech_agent"
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
        "If they ask about tech,handoffs to the tech agent"
    ),
    handoffs=[math_expert_agent, physics_expert_agent, confidentional_agent,tech_handoff],
    model=model
)

result = Runner.run_sync(starting_agent=triage_agent, input="What is 2 + 2")
# print(result.last_agent)
print(result.final_output)
print(result.new_items)

