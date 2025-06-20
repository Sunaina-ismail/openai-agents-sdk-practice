from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, handoff, HandoffInputData, InputGuardrail
from dotenv import load_dotenv
from rich import print
import os

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

@function_tool(name_override="add")
def add(a: int, b: int) ->int:
    """Add two numbers

    Args:
        a: first number 
        b: second number
    """ 
    print("add")
    return a + b


@function_tool(name_override="subtract")
def subtract(a: int, b: int) ->int:
    """Subtract two numbers

    Args:
        a: first number
        b: second number
    """ 
    print("subtract")
    return a - b


@function_tool(name_override="multiply")
def multiply(a: int, b: int) ->int:
    """Multiply two numbers

    Args:
        a: first number
        b: second number
    """ 
    print("multiply")
    return a * b

def custom_input_filter_function(input: HandoffInputData) -> HandoffInputData:
    print("custom_input_filter_function")
    return input

physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    model=model,
    handoff_description="Handles all physics-related queries and theoretical explanations."
)

math_expert_agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed."
        "You have tools to perform tasks"
        "MAKE SURE that you **MUST** use tools to perform task"
        "Also tou are NOT ALLOWED to perform task rather than MATHS related"
        "If the task is physics related so you should HANDSOFF to PHYSICIST AGENT"
    ),
    model=model,
    handoff_description="Handles all mathematical questions and calculations.",
    tools=[add, subtract, multiply],
    handoffs=[
        handoff(
            agent=physics_expert_agent,
            input_filter=custom_input_filter_function
        )
    ]
)

result = Runner.run_sync(
    starting_agent=math_expert_agent, 
    input=(
        "What is the sum of 10 and 39"
        "What is the difference of 40 and 23"
        "What is the product of 8 and 5"
        "What is the Newton's first law of motion"
    )
)
print(result.final_output)
