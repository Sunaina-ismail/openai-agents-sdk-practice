# type: ignore
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os, random
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    output_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    AgentOutputSchema,
    ModelSettings
)
from run import CustomRunner
from agents.run import RunConfig
from typing import Literal
from rich import print

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

def game(
        user_choice: Literal["rock", "paper", "scissor"], 
        computer_choice: Literal["rock", "paper", "scissor"],
    ):
    if(
        (user_choice == "paper" and computer_choice == "rock") or 
        (user_choice == "rock" and computer_choice == "scissor") or 
        (user_choice == "scissor" and computer_choice == "paper")
    ):
        return "User wins"
    elif(
        (user_choice == "rock" and computer_choice == "paper") or 
        (user_choice == "scissor" and computer_choice == "rock") or 
        (user_choice == "paper" and computer_choice == "scissor")
    ):
        return "Agent wins"
    else:
        return "There is draw"


class AgentAnswer(BaseModel):
    choice: Literal["rock", "paper", "scissor"]


@output_guardrail
async def play_game( 
    ctx: RunContextWrapper[None], agent: Agent[None], output: AgentAnswer
) -> GuardrailFunctionOutput:
    
    user_input: Literal["rock", "paper", "scissor"] = random.choice(("rock", "paper", "scissor"))
    print(f"User Choosed: {user_input}")
    print(f"Agent Choosed: {output.choice}")
    decesion=game(user_choice=user_input, computer_choice=output.choice)
    print(decesion)
    if output.choice == "paper":
        return GuardrailFunctionOutput(
            output_info="Agent cannot choose paper", 
            tripwire_triggered=True,
        )
    return GuardrailFunctionOutput(
        output_info=decesion,
        tripwire_triggered=False
    )

agent = Agent(  
    name="Rock, Paper and Scissor Master Agent",
    instructions="Your responsiblity is just to choose one from rock, paper and scissor",
    output_guardrails=[play_game],
    output_type=AgentOutputSchema(output_type=AgentAnswer, strict_json_schema=True),
    model_settings=ModelSettings(
        temperature=1
    )
)

config=RunConfig(
    model=model,
) 

async def main():
    try:
        await CustomRunner.run(agent, "Start the game", run_config=config)
        print("Guadrail didn't tripped")

    except OutputGuardrailTripwireTriggered:
        print("Agent cannot choose paper")

asyncio.run(main())