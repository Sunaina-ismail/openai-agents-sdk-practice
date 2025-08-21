import asyncio
import json
from agents import Agent, AsyncOpenAI, FunctionTool, ItemHelpers,OpenAIChatCompletionsModel,Runner, function_tool,set_tracing_disabled
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

    @function_tool
    def get_user_name(Name:str)->str:
        return f"Hello How are you {Name}."
    
    agent: Agent = Agent(
        name="assistant",
        instructions="you are a helper agent. tell user his or her name and then answer there question what every they say ",
        model=model,
        tools=[get_user_name]
    )
    
    result = Runner.run_streamed(
        agent,
        input="Hello i am nawaz shareef ex PM of pakistan, what is cell?",
    )
    print("=== Run starting ===")
    

    # all events step by step tracing 
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            print("OUtput", event.type)
            print("\n🔍 Full event data:", event.data , "\n\n\n\n\n\n")
            if hasattr(event.data, "delta") and event.data.delta:
                print("[Streamed Delta]", event.data.delta, end="", flush=True)

                # Fallback if it's normal text
            elif hasattr(event.data, "content") and event.data.content:
                print("[Streamed Token]", event.data.content, end="", flush=True)

                # Fallback for arguments during function call
            elif hasattr(event.data, "arguments"):
                print("[Function Arguments Streaming]", event.data.arguments, end="", flush=True)

            else:
                print("⚠️ No streamable text found in this delta.")
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called",event.item)
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())
        

def main_sync():
    asyncio.run(main())