from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    enable_verbose_stdout_logging
)
from agents.run import RunConfig
from rich import print

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")
enable_verbose_stdout_logging()
model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config=RunConfig(
    model=model
) 

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent[MathHomeworkOutput]( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=model
)

@input_guardrail()
async def math_guardrail( 
    ctx: RunContextWrapper[MathHomeworkOutput], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input
    )
    print(result.last_agent.name)
    print(f"the guardrail agent  {result.final_output}")
    print(result.new_items)
    
    return GuardrailFunctionOutput(
        output_info="checking", 
        tripwire_triggered=result.final_output.is_math_homework,
    )

agent = Agent(  
    name="math_agent",
    instructions="You are a math agent. You help user with their questions.you have guardrails check the input then answer",
    input_guardrails=[math_guardrail],
)

triage_agent = Agent(  
    name="triage_agent",
    instructions="you have a handoffs agent do handoffs if required. you will not answer any query just do handoffs. you must handoffs if question is of maths",
    input_guardrails=[math_guardrail],
    handoffs=[agent]
)

async def main():
    try:
        result = await Runner.run(triage_agent, "What is the 2 + 2?", run_config=config)
        print(result.input_guardrail_results)
        print("Guardrail didn't trip")
        print(result.last_agent.name)
        print(f"the customer agent  {result.final_output}")
        print(result.new_items)
        print(result.final_output)
        

    except InputGuardrailTripwireTriggered as e:
        print(e.guardrail_result)
        print("Math homework guardrail tripped")
        
        

asyncio.run(main())
