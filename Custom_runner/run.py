"""
I wrote this code myself, and it was challenging because I restricted myself from looking at the source code of the Runner class. Every line was written solely by me. This CustomRunner class allows users to perform tool calling, use input and output guardrails, handle handoffs, and more.
"""
from agents import (
    RunConfig, 
    InputGuardrail, 
    OutputGuardrail, 
    RunResult, 
    RunHooks, 
    ModelResponse, 
    RunContextWrapper, 
    TResponseInputItem, 
    RunImpl, 
    Tool, 
    handoff, 
    Handoff, 
    Model, 
    ModelTracing, 
    AgentOutputSchemaBase, 
    RunItem, 
    AgentOutputSchema,
    MaxTurnsExceeded, 
    Agent,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered
)
from agents._run_impl import (
    AgentToolUseTracker, 
    SingleStepResult, 
    NextStepFinalOutput, 
    NextStepHandoff, 
    NextStepRunAgain
)
from rich import print
from typing import TypeVar, List, Any
import asyncio


DEFAULT_MAX_TURN = 10
TContext = TypeVar("TContext")

class CustomRunner:
    @classmethod
    async def run(
        cls,
        starting_agent: Agent[TContext],
        input: str,
        *,
        context: RunContextWrapper[TContext] | None = None,
        run_config: RunConfig | None = None,
        input_guardrails: List[InputGuardrail] | None = None,
        output_guardrails: List[OutputGuardrail] | None = None,
        hooks: RunHooks | None = None,
        previous_response_id: Any =None,
        max_turn: int = DEFAULT_MAX_TURN,
    ) -> RunResult:
        
        if run_config == None:
            run_config = RunConfig()
        if hooks == None:
            hooks = RunHooks()

        tool_use_tracker = AgentToolUseTracker()
        model_responses: List[ModelResponse] = []
        current_agent: Agent = starting_agent
        all_tools: List[Tool] = []
        generated_items: List[Any] = []
        context = RunContextWrapper(
            context=context #type: ignore
        )
        current_turn: int = 0

        while True:

            current_turn += 1
            if current_turn > max_turn:
                raise MaxTurnsExceeded("Max turn exceeded")

            all_tools = await cls._get_all_tools(current_agent)
            system_prompt = await current_agent.get_system_prompt(context)
            if current_turn == 1:
                _, turn_result = await asyncio.gather(
                    cls._run_input_guardrails(
                        agent=starting_agent,
                        context=context,
                        input=input,
                        guardrails=((starting_agent.input_guardrails) + (run_config.input_guardrails if run_config.input_guardrails else [])),
                    ),
                    cls._run_single_turn(
                        agent=starting_agent,
                        all_tools=all_tools,
                        context_wrapper=context,
                        generated_items=generated_items,
                        hooks=hooks,
                        original_input=input,
                        run_config=run_config,
                        system_prompt=system_prompt,
                        tool_use_tracker=tool_use_tracker,
                        previous_response_id=previous_response_id
                    )
                )
            else:
                turn_result = await cls._run_single_turn(
                    agent=current_agent,
                    all_tools=all_tools,
                    context_wrapper=context,
                    generated_items=generated_items,
                    hooks=hooks,
                    original_input=input,
                    run_config=run_config,
                    system_prompt=system_prompt,
                    tool_use_tracker=tool_use_tracker,
                    previous_response_id=previous_response_id
                )

            model_responses.append(turn_result.model_response)
            generated_items.append(turn_result.generated_items)

            if isinstance(turn_result.next_step, NextStepFinalOutput):
                await cls._run_output_guardrails(
                    agent=current_agent,
                    context=context,
                    guardrails=(current_agent.output_guardrails) + (run_config.output_guardrails if run_config.output_guardrails else []),
                    agent_output=turn_result.next_step.output
                )
                return RunResult(
                    context_wrapper=context,
                    final_output=turn_result.next_step.output,
                    input=input,
                    input_guardrail_results=[],
                    output_guardrail_results=[],
                    new_items=generated_items,
                    raw_responses=model_responses,
                    _last_agent=current_agent
                )
            elif isinstance(turn_result.next_step, NextStepHandoff):
                current_agent = turn_result.next_step.new_agent
            elif isinstance(turn_result.next_step, NextStepRunAgain):
                input=str(
                    turn_result.new_step_items[-1].output #type: ignore
                )
            else:
                raise ValueError("Something went wrong")
            
    @classmethod
    async def _run_input_guardrails(
        cls,
        agent: Agent[TContext],
        guardrails: list[InputGuardrail],
        input: str | List[TResponseInputItem],
        context: RunContextWrapper[TContext],
    ):
        tasks=[
        asyncio.create_task(
            RunImpl.run_single_input_guardrail(
                agent,
                guadrail,
                input,
                context
            )
        )   
        for guadrail in guardrails
        ]   
        for done in asyncio.as_completed(tasks):
            result = await done
            if result.output.tripwire_triggered:
                raise InputGuardrailTripwireTriggered(result)

    @classmethod
    async def _run_output_guardrails(
        cls,
        agent: Agent[TContext],
        guardrails: list[OutputGuardrail],
        agent_output: Any,
        context: RunContextWrapper[TContext],
    ):
        tasks=[
        asyncio.create_task(
            RunImpl.run_single_output_guardrail(
                guadrail,
                agent,
                agent_output,
                context
            )
        )   
        for guadrail in guardrails
        ]   

        for done in asyncio.as_completed(tasks):
            result = await done
            if result.output.tripwire_triggered:
                raise OutputGuardrailTripwireTriggered(result)
    
    @classmethod
    async def _get_new_response(
        cls,
        agent: Agent[TContext],
        system_prompt: str | None,
        input: str | list[TResponseInputItem],
        all_tools: List[Tool],
        handoffs: List[Handoff[Any]],
        run_config: RunConfig,
        tool_use_tracker: AgentToolUseTracker,
        output_schema: AgentOutputSchemaBase | None,
        prevoiuse_response_id: str | None
    ) -> ModelResponse:
        model = cls._get_model(agent, run_config)
        model_settings = agent.model_settings
        model_settings = RunImpl.maybe_reset_tool_choice(agent, tool_use_tracker, model_settings)

        new_response = await model.get_response(
            system_instructions=system_prompt,
            input=input,
            model_settings=model_settings,
            tools=all_tools,
            output_schema=output_schema,
            handoffs=handoffs,
            tracing=ModelTracing.DISABLED,
            previous_response_id=prevoiuse_response_id,
        )
        return new_response

    @classmethod
    async def _run_single_turn(
        cls,
        agent: Agent[TContext],
        all_tools: list[Tool],
        original_input: str | list[TResponseInputItem],
        generated_items: list[RunItem],
        hooks: RunHooks[TContext],
        context_wrapper: RunContextWrapper[TContext],
        run_config: RunConfig,
        tool_use_tracker: AgentToolUseTracker,
        previous_response_id: str | None,
        system_prompt: str | None,
    ) -> SingleStepResult:
        handoffs = cls._get_handsoff(agent)
        output_schema = cls._get_output_schema(agent)

        new_response = await cls._get_new_response(
            agent=agent,
            all_tools=all_tools,
            handoffs=handoffs,
            run_config=run_config,
            input=original_input,
            output_schema=output_schema,
            system_prompt=system_prompt,
            tool_use_tracker=tool_use_tracker,
            prevoiuse_response_id=previous_response_id
        )

        return await cls._get_single_step_result_from_response(
            agent=agent,
            all_tools=all_tools,
            original_input=original_input,
            context_wrapper=context_wrapper,
            handoffs=handoffs,
            hooks=hooks,
            new_response=new_response,
            output_schema=output_schema,
            run_config=run_config,
            tool_use_tracker=tool_use_tracker,
            pre_step_items=generated_items
        )

    @classmethod
    async def _get_single_step_result_from_response(
        cls,
        agent: Agent[TContext],
        all_tools: list[Tool],
        original_input: str | list[TResponseInputItem],
        pre_step_items: list[RunItem],
        new_response: ModelResponse,
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff[Any]],
        hooks: RunHooks[TContext],
        context_wrapper: RunContextWrapper[TContext],
        run_config: RunConfig,
        tool_use_tracker: AgentToolUseTracker
    ) -> SingleStepResult:
        processed_response = RunImpl.process_model_response(
            agent=agent,
            all_tools=all_tools,
            response=new_response,
            output_schema=output_schema,
            handoffs=handoffs,
        )
        
        tool_use_tracker.add_tool_use(agent, processed_response.tools_used)

        return await RunImpl.execute_tools_and_side_effects(
            agent=agent,
            context_wrapper=context_wrapper,
            hooks=hooks,
            new_response=new_response,
            original_input=original_input,
            output_schema=output_schema,
            processed_response=processed_response,
            run_config=run_config,
            pre_step_items=pre_step_items
        )

    @classmethod
    def _get_model(
        cls,
        agent: Agent[Any],
        run_config: RunConfig
    ) -> Model:
        if isinstance(run_config.model, Model):
            return run_config.model 
        elif isinstance(run_config.model, str):
            return run_config.model_provider.get_model(run_config.model)
        elif isinstance(agent.model, Model):
            return agent.model
        else:
            raise ValueError("Invalid model type.")

    @classmethod
    async def _get_all_tools(
        cls,
        agent: Agent[TContext],
    ) -> List[Tool]:
        return await agent.get_all_tools()

    @classmethod
    def _get_handsoff(
        cls,
        agent: Agent[TContext]
    ):
        if not agent.handoffs:
            return []
        
        handsoff_list: List[Handoff] = []

        for single_handsoff in agent.handoffs:
            if isinstance(single_handsoff, Handoff):
                handsoff_list.append(single_handsoff)
            elif isinstance(single_handsoff, Agent):
                handsoff_list.append(handoff(single_handsoff))
            else:
                raise ValueError("Invalid handoffs type")
        return handsoff_list
    
    @classmethod
    def _get_output_schema(
        cls,
        agent: Agent[TContext]
    ) -> AgentOutputSchemaBase | None:

        if agent.output_type == None:
            return None
        elif isinstance(agent.output_type, AgentOutputSchemaBase):
            return agent.output_type
        else:
            return AgentOutputSchema(agent.output_type)
        
