import asyncio
import json
from agents import Agent, AsyncOpenAI, FunctionTool, ItemHelpers,OpenAIChatCompletionsModel,Runner, function_tool,set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
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

    @function_tool(name_override="guru",description_override="jo khareda wo wapis kro",docstring_style="google",)
    def get_product(user_id:str)->str:
        "Get the product user bought with name price and id"
        return f"""
    Product:makeup,
    price:2000
    id:{user_id}
    """
        
    agent: Agent = Agent(
        name="assistant",
        instructions="you are a customer support agent.use tool do not predict the output if you do not know",
        model=model,
        tools=[get_product]
    )
    
    result = Runner.run_streamed(
        agent,
        input="my id is make10 i bought the some product. return my purchases and detail",
    )
    print("=== Run starting ===")
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    

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





    print("=== Run complete ===")


if __name__ == "__main__":
    asyncio.run(main())
        

def main_sync():
    asyncio.run(main())