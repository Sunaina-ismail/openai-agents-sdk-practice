import asyncio
from agents import (
    Agent, AsyncOpenAI, RunContextWrapper, Runner,
    RunConfig, OpenAIChatCompletionsModel
)
from pydantic import BaseModel
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set.")

# ✅ More detailed context
class PatientInfo(BaseModel):
    name: str
    age: int
    symptoms: str
    urgency_level: str  # e.g., "low", "moderate", "high"

# ✅ Dynamic instructions using rich context
def triage_instructions(
    context: RunContextWrapper[PatientInfo], agent: Agent[PatientInfo]
) -> str:
    patient = context.context
    return (
        f"You are a virtual medical assistant named {agent.name}. "
        f"The patient's name is {patient.name}, age {patient.age}. "
        f"They reported: {patient.symptoms}. Urgency level: {patient.urgency_level}. "
        "Greet them politely by name, use simple language, express care. "
        "Offer initial guidance and suggest whether they should seek a doctor, hospital visit, or stay home."
    )

# ✅ Async function to use in your real app/API
async def handle_patient_query(patient_data: PatientInfo, user_question: str):
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

    agent = Agent[PatientInfo](
        name="Nurse Alia",
        instructions=triage_instructions,
        model=model
    )

    result = Runner.run_streamed(
        agent,
        input=user_question,
        run_config=config,
        context=patient_data
    )

    print("\n--- Response ---")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

# 🧪 Test run
def main_sync():
    patient = PatientInfo(
        name="Sumayya",
        age=27,
        symptoms="i have pain in legs.",
        urgency_level="moderate"
    )
    asyncio.run(handle_patient_query(patient, "What should I do next?"))

if __name__ == "__main__":
    main_sync()
