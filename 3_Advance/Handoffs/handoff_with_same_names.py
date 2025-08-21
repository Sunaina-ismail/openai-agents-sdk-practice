# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, RunConfig, AgentHooks,enable_verbose_stdout_logging
# from openai import AsyncOpenAI
# from dotenv import load_dotenv
# from rich import print
# import os
# import asyncio

# load_dotenv()
# set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

# API_KEY=os.environ.get("GEMINI_API_KEY")

# config = RunConfig(
#     model=OpenAIChatCompletionsModel(
#         model="gemini-1.5-flash",
#         openai_client=AsyncOpenAI(
#             api_key=API_KEY,
#             base_url="https://generativelanguage.googleapis.com/v1beta/openai"
#         )
#     )
# )

# class CustomMathAgentHooks(AgentHooks):
#     async def on_start(self, context, agent):
#         print("Math Agent is started.")

#     async def on_end(self, context, agent, output):
#         print("Math Agent is ended.")

# #! COMMON NAME OF AGENT


# class CustomPhysicsAgentHooks(AgentHooks):
#     async def on_start(self, context, agent):
#         print("Physics Agent is started.")

#     async def on_end(self, context, agent, output):
#         print("Physics Agent is ended.")

# #! COMMON NAME OF AGENT
# physics_expert_agent = Agent(
#     name="Physicist", 
#     instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
#     handoff_description="Handles all physics-related queries and theoretical explanations.",
#     hooks=CustomPhysicsAgentHooks()
# )
# math_expert_agent = Agent(
#     name="mathematician", 
#     instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed. only math no other queries",
#     handoff_description="Handles all mathematical questions and calculations.",
#     hooks=CustomMathAgentHooks()
# )
# triage_agent = Agent(
#     name="Traige Agent",
#     instructions=(
#         "You are a triage agent"
#     ),
#     handoffs=[math_expert_agent,physics_expert_agent]
# )

# async def main():
#     await Runner.run(
#         starting_agent=triage_agent,
#         input="Tell me the basics concepts of algebra",
#         run_config=config
#     )
    
    

# asyncio.run(main())

# #! HANDOFF K CASE MA LLM AGENT KO JUST ITNA BATATA HA K KONSA AGENT  KO HANDOFF KRNA HA MEANS AGENT'S (NAME) AND USMY KIA (ARGUMENTS) JANY CHAHYE

# #? ISLIYE AGAR EK NAME K MULTIPLE HANDOFF AGENTS HONGY TO REAL MA SIRF US AGENT KO HANDOFF KIA JAYEGA JO AGENT.HANDOFFS LIST MA LAST AGENT HO



from dataclasses import dataclass
import os, asyncio
from dotenv import load_dotenv
from agents import(
 Agent,
 RunConfig,
 RunContextWrapper,
 Runner,
 AsyncOpenAI, 
 OpenAIChatCompletionsModel, 
 enable_verbose_stdout_logging,
 function_tool,
 set_tracing_disabled,
 )


load_dotenv()
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
 raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
 api_key=gemini_api_key,
 base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
 model="gemini-2.5-flash",
 openai_client=external_client,
)

config = RunConfig(
 model=model,
 model_provider=external_client,
 tracing_disabled=set_tracing_disabled(True) 
)


# -----------------------------------------------------------------------//

@dataclass
class UserInfo:
 name : str
 id : int
 

# ----------------------------------------------------------------------//

@function_tool
def get_user_info(wrapper:RunContextWrapper[UserInfo]):
    """_summary_

    Args:
        wrapper (RunContextWrapper[UserInfo]): "

    Returns:
        _type_: _description_
    """ ""
    return f"{wrapper.context.name} is a QA Engineer"


getting_info_agent = Agent(
 name = "GettingInfo Agent",

 instructions = """
 "You are a helpful assistant. "
 "When asked about the QA Engineer or details about the user, "
 "always call the `get_user_info` tool to answer. "
 "Do not try to answer without calling the tool." 
 """,

 tools = [get_user_info]
)

async def main():

 user_details = UserInfo(
 name = "Mueza Ejaz",
 id = 12458
) 

 input = "who is the QA Engineer?"
 result = await Runner.run(getting_info_agent, input, context = user_details, run_config = config) 

 print("User Information:")
 print(result.final_output)


if __name__ == "__main__":
 asyncio.run(main())