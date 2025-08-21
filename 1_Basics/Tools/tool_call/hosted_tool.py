import asyncio
from agents import Agent, AsyncOpenAI, FunctionTool, RunConfig, OpenAIChatCompletionsModel,Runner, WebSearchTool,CodeInterpreterTool,set_default_openai_key,set_tracing_disabled




set_default_openai_key("sk-key", use_for_tracing=False)

import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set..")



set_tracing_disabled(True)  # global level tracing disabled

async def main():
    
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        
    )


    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
        
    )





    agent: Agent = Agent(
        name="assistant", # required
        instructions="you are a helper agent",
        model=model,
        #  tools=[WebSearchTool(),CodeInterpreterTool()],  # hosted tools only for openai API right now not for third party Models
    )
    
    for tool in agent.tools:
        if isinstance(tool, FunctionTool):
            print(tool.name)
            print(tool.description)
            print()
    
    # agent and input are required 
    result = await Runner.run(starting_agent=agent, input="what is the weather of  longitude 57 latitude 33", )
    
    print(result.final_output)
        

def main_sync():
    asyncio.run(main())