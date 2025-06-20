from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, InputGuardrail, InputGuardrailResult, input_guardrail, output_guardrail, OutputGuardrail, OutputGuardrailResult, GuardrailFunctionOutput
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

agent=Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    model=model
)

result=Runner.run_sync(
    starting_agent=agent,   
    input="Hello World"
)

print(result.final_output)