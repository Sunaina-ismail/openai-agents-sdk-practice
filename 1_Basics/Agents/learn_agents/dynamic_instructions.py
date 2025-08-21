import asyncio
from agents import Agent, AsyncOpenAI, ModelSettings, RunConfig, OpenAIChatCompletionsModel, RunContextWrapper,Runner
from openai.types.responses import ResponseTextDeltaEvent


import os
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set..")


# the context classs passed to the dynamic instructions
class User(BaseModel):
    name:str
    
    
    
# dynamic instructions with a context that agent will get and use for instructions also the "agent" will give the agents name wether assistant or whatever
def dynamic_instructions(
    context: RunContextWrapper[User], agent: Agent[User]
) -> str:
    return f"The Users's name is {context.context.name} . Greet user first and also give him this I'm {agent.name} then answer his or her query"
    
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


    #create context data
    context_input = User(name="bandar")

    agent= Agent[User](
        name="doctor",
        instructions=dynamic_instructions,
        model=model,       
    )
    
    # a new parameter "context" to get the context data that will be passed to the dymanic instructions parameter
    result = Runner.run_streamed(agent, "where is the jahan sikandar from? he is a fictional novel character Jannat k Pattay", run_config=config, context=context_input)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
        


def main_sync():
    asyncio.run(main())
    
