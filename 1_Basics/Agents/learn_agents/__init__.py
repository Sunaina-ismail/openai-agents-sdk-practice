# import inspect
# from agents import Agent, AsyncOpenAI, ModelSettings, RunConfig, OpenAIChatCompletionsModel,Runner


# # load the API key 
# import os
# from dotenv import load_dotenv
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY is not set..")

# def main():
    
    
    
#     # set external client whose API we will use and the base url (for Openai agent sdk you do not need this)
#     external_client = AsyncOpenAI(
#         api_key=GEMINI_API_KEY,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

#     print(f"external_client\n{dir(external_client)}\n\n\n\n\n\n")
# # 'api_key', 'audio', 'auth_headers', 'base_url', 'batches', 'beta', 'chat', 'close', 'completions', 'containers', 'copy', 'custom_auth', 'default_headers', 'default_query', 'delete', 'embeddings', 'evals', 'files', 'fine_tuning', 'get', 'get_api_list', 'images', 'is_closed', 'max_retries', 'models', 'moderations', 'organization', 'patch', 'platform_headers', 'post', 'project', 'put', 'qs', 'request', 'responses', 'timeout', 'uploads', 'user_agent', 'vector_stores', 'websocket_base_url', 'with_options', 'with_raw_response', 'with_streaming_response'



#     # set model you are using and it's client whose model you will use (for Openai agent sdk you do not need this)
#     model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
        
#     )

#     print(f"model\n{dir(model)}\n\n\n\n\n\n")
# # 'get_response', 'model', 'stream_response' 



#     # set configuration optional but recommended for all agents
#     config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True,
#         model_settings=ModelSettings(tool_choice="none") 
#     )


#     print(f"config\n{dir(config)}\n\n\n\n\n\n")
# #  'group_id', 'handoff_input_filter', 'input_guardrails', 'model', 'model_provider', 'model_settings', 'output_guardrails', 'trace_id', 'trace_include_sensitive_data', 'trace_metadata', 'tracing_disabled', 'workflow_name'




#     # create agent that will call the LLM 
#     agent: Agent = Agent(
#         name="assistant", # required
#         instructions="you are a helper agent",
        
#     )


#     print(f"agent\n{dir(agent)}\n\n\n\n\n\n")
    
# # 'as_tool', 'clone', 'get_all_tools', 'get_mcp_tools', 'get_prompt', 'get_system_prompt', 'handoff_description', 'handoffs', 'hooks', 'input_guardrails', 'instructions', 'mcp_config', 'mcp_servers', 'model', 'model_settings', 'name', 'output_guardrails', 'output_type', 'prompt', 'reset_tool_choice', 'tool_use_behavior', 'tools'


#     print("\n📜 All public attributes and methods of Agent:\n")
#     for name in dir(Agent):
#         if not name.startswith("_"):
#             attr = getattr(Agent, name)
#             if callable(attr):
#                 print(f"🔹 Method: {name}{inspect.signature(attr)}")
#             else:
#                 print(f"🔸 Attribute: {name} = {attr}")
     
     
# main()     


def main():
    print("hello")
    
    