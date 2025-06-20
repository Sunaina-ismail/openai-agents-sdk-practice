from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, output_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()
set_tracing_disabled(disabled=True)

output = None
API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
)

class OutputType(BaseModel):
    first_number: int
    second_number: int
    result: int

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: first number
        b: second number
    
    """
    return a + b

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check the output of the agent and arrange them in the given expected output type",
    output_type=OutputType,
    model=model
)


@output_guardrail
async def type_sorter( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    print(ctx)
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    global output
    output = result.final_output
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=False,
    )

agent = Agent(
    name="Mathematician", 
    instructions="You are math expert", 
    model=model, 
    tools=[add],
    output_guardrails=[type_sorter]
)

# result = Runner.run_sync(starting_agent=agent, input="What is 2+2")
# result.final_output = output
# print(result.final_output)
class A:
    pass

class B(A):
    pass

b=B()
print(isinstance(b, B))