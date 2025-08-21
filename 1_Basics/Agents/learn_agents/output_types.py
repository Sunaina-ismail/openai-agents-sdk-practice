import asyncio
from agents import Agent, AsyncOpenAI, ModelSettings, RunConfig, OpenAIChatCompletionsModel,Runner
from openai.types.responses import ResponseTextDeltaEvent


import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set..")



class Capital(BaseModel):
    country:str
    capital:str
    
    
    
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


    agent: Agent = Agent(
        name="assistant", # required
        instructions="you are a helper agent",
        model=model,
        output_type=list[Capital]
    )
    
    
    # agent and input are required 
    result = Runner.run_streamed(starting_agent=agent, input="give me Capital of 5 south asian countries.", run_config=config)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
        

def main_sync():
    asyncio.run(main())