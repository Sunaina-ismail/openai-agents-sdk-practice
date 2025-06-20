from agents import Agent, Runner, OpenAIChatCompletionsModel, RunContextWrapper, set_tracing_disabled, AsyncOpenAI, function_tool
from dotenv import load_dotenv
from dataclasses import dataclass
import os

API_KEY=os.environ.get("GEMINI_API_KEY")

load_dotenv()
set_tracing_disabled(disabled=True)

@dataclass
class UserInfo:
    name: str
    age: int

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

@function_tool
def fetch_user_data(ctx: RunContextWrapper[UserInfo]):
    # '''Tells you about user'''
    '''Returns the age and name of the user.'''
    return f"The name of the user is {ctx.context.name} and age is {ctx.context.age}"

user = UserInfo(name="Muhammad Fasih", age=10)

agent=Agent[UserInfo](
    name="Assistant",
    instructions="You are a helpful asisstant",
    model=model,
    tools=[fetch_user_data]
)
result=Runner.run_sync(
    agent,
    "What is my name and age?",
    context=user
)

print(result.final_output)