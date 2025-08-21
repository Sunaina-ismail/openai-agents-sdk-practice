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
    
    
    
    # Model json return for tool call
    print("=== Tool Schema(s) ===")
    for tool in agent.tools:
        if isinstance(tool, FunctionTool):
            print(f"FunctionTool(")
            print(f"  name='{tool.name}',")
            print(f"  description='{tool.description}',")
            print(f"  parameters={tool.params_json_schema}")
            print(f"  parameters={tool.on_invoke_tool}")
            print(f"  parameters={tool.strict_json_schema}")
            print(f"  parameters={tool.is_enabled}")
            print(json.dumps(tool.params_json_schema, indent=2))
            print(")\n")
        else:
            print(f"🔧 Non-function tool: {tool}")
    print("======================\n\n")



if __name__ == "__main__":
    asyncio.run(main())
        

def main_sync():
    asyncio.run(main())