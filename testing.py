from agents import OpenAIChatCompletionsModel, function_tool, ModelSettings, ModelTracing, AgentOutputSchema, Agent, ToolsToFinalOutputResult, RunContextWrapper, FunctionToolResult, Runner
from openai import AsyncOpenAI
from pydantic import BaseModel
from rich import print
from typing import List
import os

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
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
def add(a: int, b: int) -> str:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return f"The sum of {a} and {b} is {a + b}"


def sum(a: int, b: int) -> str:
    """Add two numbers

    Args:
        a: first number
        b: second number
    """
    return f"The sum of {a} and {b} is {a + b}"

formatter_agent=Agent(
    name="Formater",
    instructions="You convert given data into desired output",
    model=model,
    output_type=AgentOutputSchema(
        output_type=OutputType,
        strict_json_schema=True
    ),
)


async def get_expected_output_type(
    ctx: RunContextWrapper[None],
    result_list: List[FunctionToolResult]
) -> ToolsToFinalOutputResult:
    result = await Runner.run(
        starting_agent=formatter_agent,
        input=result_list[0].output
    )
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output=result.final_output
    )

agent = Agent(
    name="Math Assistant",
    instructions="You are good at maths",
    model=model,
    tools=[add],
    tool_use_behavior=get_expected_output_type,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="What is 2 + 2"
)

print(result.final_output)

# async def main():
#     response = await model.get_response(
#         input="What is 2+2",
#         system_instructions="You are good at maths. You have tools to implement",
#         handoffs=[],
#         model_settings=ModelSettings(
#             tool_choice="required"
#         ),
#         output_schema=AgentOutputSchema(
#             output_type=OutputType,
#             strict_json_schema=True
#         ),
#         tools=[add],
#         tracing=ModelTracing.DISABLED,
#         previous_response_id=None,
#     )
#     print(response)
