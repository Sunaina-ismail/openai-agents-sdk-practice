import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper
from dotenv import load_dotenv
from dataclasses import dataclass
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

@dataclass
class UserContext:  
    name: str
    age: int

def dynamic_instructions(
    wrapper: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {wrapper.context.name}. Help them with their questions."

# instructions according to condition like user is naina or other 
def dynamic_instructions2(
        context: RunContextWrapper[UserContext], agent: Agent[UserContext]
    ) -> str:
        if context.context.name.lower() == "naina":
            return "The user is Naina, a medical student. Give detailed yet easy explanations."
        else:
            return f"The user's name is {context.context.name}. Keep responses concise."

# the instructions may be awaited means async 
async def dynamic_instructions_async(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
    ) -> str:
        await asyncio.sleep(0.1)  # simulate delay
        return f"Welcome {context.context.name}. You are talking to a scientific assistant."
    
    
agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
    model=model
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

context = UserContext(name="Ahmed", age=20)
result = Runner.run_sync(agent, "Hello", context=context)
print(result.final_output)