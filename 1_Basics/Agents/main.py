from dataclasses import dataclass
from typing import Any
from agents import Agent, Handoff, ModelSettings, ModelTracing, RunContextWrapper, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, function_tool, set_tracing_disabled, RunConfig, set_default_openai_api, set_default_openai_client
from dotenv import load_dotenv
from rich import print
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

enable_verbose_stdout_logging()

model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client,
        
    )

config = RunConfig(
    model=model,
    # model_settings=ModelSettings(
    #     tool_choice="minus"
    # )
)


# story_writer = Agent(
#     name="Story Writer", 
#     instructions="You are a story writer", 
# )

# rating_agent = Agent(
#     name="Rating Agent", 
#     instructions="You are given the story you have to rate it out of 10", 
# )

# @function_tool
# def sum(a,b):
#     return f"Sum is {a + b}"

# @function_tool
# def minus(a,b):
#     return f"minus is {a - b}"


async def main():
    # story = await Runner.run(
    #     starting_agent=story_writer, 
    #     input="Write a 5 line story on Agentic AI", 
    #     run_config=config
    # )
    # rating = await Runner.run(
        # starting_agent=rating_agent, 
        # input=story.to_input_list(), 
        # run_config=config
    # )
    
        
    # print(await model.get_response(
    #      system_instructions="You are a story writer",
    #     input="Write a 5-line story about Agentic AI",
    #     model_settings=ModelSettings(),  # default settings
    #     tools=[],  # agar koi tool nahi use kar rahe
    #     output_schema=None,  # agar tumhe schema ki zarurat nahi
    #     handoffs=[],  # handoffs bhi nahi use ho rahe
    #     tracing=ModelTracing.DISABLED,
    #     previous_response_id=None,
    # ))
    
    
    # print(rating.final_output)
    
   
        

 

    mainAgent =Agent(
        name="helper",
        instructions="You're a smart assistant. Route the question to tech if needed.",
        model=model
        
    )
    
    
    result = await Runner.run(
        mainAgent,"Hello tell me about Agentic AI",run_config=config
    )
    
    
    print(result.final_output)


asyncio.run(main())
