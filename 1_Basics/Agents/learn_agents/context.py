import asyncio
from dataclasses import dataclass
from agents import Agent, AsyncOpenAI, ModelSettings, RunConfig, OpenAIChatCompletionsModel,Runner
from openai.types.responses import ResponseTextDeltaEvent


import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set..")



class Purchases(BaseModel):
    item1:str
    item2:str
    
    
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> list[Purchases]:
        return [Purchases(item1="laptop", item2="dress")]
    
async def main():
    
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )


    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
        
    )


    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )
    
    
    

    user=UserContext(uid="123",is_pro_user=True)
    
    purchases = await user.fetch_purchases()

    agent = Agent[UserContext](
        name="assistant", # required
            instructions="""
You're a helpful assistant. Based on the provided list of purchases, return the same data in the following JSON format(required this format only):

[
  {
    "item1": "...",
    "item2": "..."
  }
]
""",
        model=model,
    )
    
    
    # agent and input are required 
    result = await Runner.run(starting_agent=agent, input=f"return the purchases of user uid is 123", run_config=config, context=user)
    print(result.final_output)
        

def main_sync():
    asyncio.run(main())