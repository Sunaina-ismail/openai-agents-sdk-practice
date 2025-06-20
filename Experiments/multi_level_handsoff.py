from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, enable_verbose_stdout_logging, RunConfig
from dotenv import load_dotenv
from rich import print
import os

# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

config = RunConfig(
    model=model
)

calculus_agent = Agent(
    name="Calculus Expert",
    instructions="You are a world-class calculus expert. Your task is to solve complex problems related to differentiation, integration, limits, series, and differential equations. Provide clear, step-by-step solutions and explanations. Ensure accuracy in all calculations and theoretical applications.",
    handoff_description="Handles all advanced calculus problems and provides detailed solutions."
)

math_expert_agent = Agent(
    name="Mathematician", 
    instructions=(
        "Help the user with their questions."
        "If they ask about calculus, handoff to the Calculus Agent."
        "MAKE SURE you are **NOT ALLOWED** to answer calculus related questions."
    ),
    handoff_description="Handles all mathematical questions and calculations.",
    handoffs=[calculus_agent]
)


triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
    ),
    handoffs=[math_expert_agent],
)


result = Runner.run_sync(starting_agent=triage_agent, input="What is the derivative of x^2", run_config=config)
print(result.final_output)