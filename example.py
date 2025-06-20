from agents import Agent, Runner, FunctionTool, RunContextWrapper, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI
from typing import Any
from agents.model_settings import ModelSettings
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
    api_key=GEMINI_API_KEY
)
set_default_openai_client(external_client)
set_tracing_disabled(True)

# Dummy schema for the function input
class FunctionArgs(BaseModel):
    username: str
    age: int
    model_config = ConfigDict(extra="forbid")

# Dummy Gemini call (real call, but with simple fallback)
def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "Gemini API key not found."
        
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=body)
        if response.ok:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"[Gemini error: {response.status_code}]"
    except Exception as e:
        return f"[Gemini request failed: {str(e)}]"


# Dummy async tool that uses Gemini (or just echoes)
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    print("Args (raw):", args)
    parsed = FunctionArgs.model_validate_json(args)
    prompt = f"Dummy prompt for Gemini: {parsed.username} is {parsed.age} years old."
    response = call_gemini(prompt)
    return f"Gemini responded: {response}"


# Register dummy tool
tool = FunctionTool(
    name="process_user",
    description="Dummy tool to simulate processing of user info with Gemini",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function
)

# Create dummy agent
example_agent = Agent(
    name="dummy_agent",
    instructions="Pretend to process input using Gemini, just for testing.",
    tools=[tool],
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
)

# Run agent with fake input
output = Runner.run_sync(example_agent, input="Just test something with a 14-year-old Mr. X.")
print("Final output:", output.final_output)
