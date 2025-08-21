from agents import Agent, HandoffInputData, handoff, RunContextWrapper
from rich import print
from pydantic import BaseModel

agent=Agent(
    name="Assistant",
)

handoff_data_without_input_type=handoff(
    agent=agent,
)

print("1st ",handoff_data_without_input_type)
#! OUTPUT:
"""
Handoff(
    tool_name='transfer_to_assistant',
    tool_description='Handoff to the Assistant agent to handle the request. ',
    input_json_schema={
        'additionalProperties': False,
        'type': 'object',
        'properties': {},
        'required': []
    },
    on_invoke_handoff=<function handoff.<locals>._invoke_handoff at 0x0000013F17458CC0>,
    agent_name='Assistant',
    input_filter=None,
    strict_json_schema=True
)
"""

class MyInputType(BaseModel):
    name: str

def on_handoff(ctx: RunContextWrapper, input: MyInputType):
    print(input)

def custom_input_filter(input_list: HandoffInputData) -> HandoffInputData:
    print("Hello World")
    return input_list

handoff_data_with_input_type=handoff(
    agent=agent,
    input_type=MyInputType,
    on_handoff=on_handoff,
    input_filter=custom_input_filter
)

print("2nd " ,handoff_data_with_input_type)


#! OUTPUT:hi
"""
Handoff(
    tool_name='transfer_to_assistant',
    tool_description='Handoff to the Assistant agent to handle the request. ',
    input_json_schema={
        'properties': {'name': {'title': 'Name', 'type': 'string'}},
        'required': ['name'],
        'title': 'MyInputType',
        'type': 'object',
        'additionalProperties': False
    },
    on_invoke_handoff=<function handoff.<locals>._invoke_handoff at 0x0000013F1CC39D00>,
    agent_name='Assistant',
    input_filter=None,
    strict_json_schema=True
)
"""

