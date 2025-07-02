"""
I wrote this code myself, and it was challenging because I restricted myself from looking at the source code of the Runner class. Every line was written solely by me. This CustomRunner class allows users to perform tool calling, use input and output guardrails, handle handoffs, and more.
"""
from agents import (
    Agent,
    Handoff,
    handoff,
    Tool,
    AgentOutputSchemaBase,
    AgentOutputSchema,
    TResponseInputItem,
    InputGuardrail,
    RunContextWrapper,
    InputGuardrailResult,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    OutputGuardrail,
    OutputGuardrailResult,
    RunConfig,
    Model,
    RunItem,
    ModelResponse,
    RunHooks,
    ItemHelpers,
    RunResult,
    MaxTurnsExceeded,
    AgentsException
)

from agents._run_impl import (
    AgentToolUseTracker,
    RunImpl,
    get_model_tracing_impl,
    SingleStepResult,
    TraceCtxManager,
    NextStepFinalOutput,
    NextStepHandoff,
    NextStepRunAgain
)
from agents.tracing import SpanError, agent_span

from agents.util import _coro, _error_tracing

from agents.run_context import TContext
from typing import List, Any, cast
import copy
import asyncio

DEFAULT_MAX_TURN = 10

class AdvanceRunner:
    @classmethod
    def _get_handoffs(cls, agent: Agent[TContext]) -> List[Handoff]:
        handoffs: List[Handoff] = []

        for handoff_item in agent.handoffs:
            if isinstance(handoff_item, Handoff):
                handoffs.append(handoff_item)
            elif isinstance(handoff_item, Agent):
                handoffs.append(handoff(handoff_item))

        return handoffs

    @classmethod
    async def _get_all_tools(cls, agent: Agent[TContext]) -> List[Tool]:
        return await agent.get_all_tools()
    
    @classmethod
    def _get_output_schema(cls, agent: Agent[TContext]) -> AgentOutputSchemaBase | None:
        if agent.output_type is None or agent.output_type is str:
            return None
        elif isinstance(agent.output_type, AgentOutputSchemaBase):
            return agent.output_type
        else:
            return AgentOutputSchema(agent.output_type)
        
    @classmethod
    async def _run_input_guardrails(
        cls, 
        agent: Agent[Any], 
        input: List[TResponseInputItem] | str,
        guardrails: List[InputGuardrail] | None,
        context: RunContextWrapper[TContext]
        ) -> List[InputGuardrailResult]:
        if not guardrails:
            return []
        
        guardrail_tasks = [
            asyncio.create_task(
                RunImpl.run_single_input_guardrail(agent, guardrail, input, context)
            ) for guardrail in guardrails 
        ]

        guardrail_results: List[InputGuardrailResult] = []

        for done in asyncio.as_completed(guardrail_tasks):
            result = await done
            if result.output.tripwire_triggered:

                for t in guardrail_tasks:
                    t.cancel()

                _error_tracing.attach_error_to_current_span(
                    SpanError(
                        message="Input Guardrail Trip Wire Triggered",
                        data={"guardrail": result.guardrail.get_name()}
                    )   
                )
                raise InputGuardrailTripwireTriggered(result)
            else:
                guardrail_results.append(result)

        return guardrail_results

    @classmethod
    async def _run_output_guardrails(
        cls,
        agent: Agent[Any],
        agent_output: Any,
        context: RunContextWrapper[TContext],
        guardrails: List[OutputGuardrail]
    ) -> List[OutputGuardrailResult]:

        if not guardrails:
            return []

        guardrail_tasks = [
            asyncio.create_task(RunImpl.run_single_output_guardrail(guardrail, agent, agent_output, context)) 
            for guardrail in guardrails
        ]    

        guardrail_results: List[OutputGuardrailResult] = []

        for done in asyncio.as_completed(guardrail_tasks):
            result = await done
            if result.output.tripwire_triggered:

                for t in guardrail_tasks:
                    t.cancel()
                _error_tracing.attach_error_to_current_span(
                    SpanError(
                        message="Output Guardrail Trip Wire Triggered.",
                        data={"guardrail": result.guardrail.get_name()}
                    )
                )
                raise OutputGuardrailTripwireTriggered(result)
            else:
                guardrail_results.append(result)

        return guardrail_results

    @classmethod
    def _get_model(self, agent: Agent[TContext], run_config: RunConfig) -> Model:
        if isinstance(run_config.model, Model):
            return run_config.model
        elif isinstance(run_config.model, str):
            return run_config.model_provider.get_model(run_config.model)
        elif isinstance(agent.model, Model):
            return agent.model
        else:
            return run_config.model_provider.get_model(agent.model)

    @classmethod
    async def _get_new_response(
        cls,
        orignal_input: str | List[TResponseInputItem],
        system_instructions: str | None,
        run_config: RunConfig,
        context_wrapper: RunContextWrapper[TContext],
        agent: Agent[TContext],
        output_schema: AgentOutputSchemaBase | None,
        all_tools: List[Tool],
        handoffs: List[Handoff],
        tool_use_tracker: AgentToolUseTracker,
        previous_response_id: str | None,
    ) -> ModelResponse:
        model = cls._get_model(agent, run_config)

        model_settings=agent.model_settings.resolve(run_config.model_settings)
        model_settings=RunImpl.maybe_reset_tool_choice(agent, tool_use_tracker, model_settings)

        response= await model.get_response(
            system_instructions,
            orignal_input,
            model_settings,
            all_tools,
            output_schema,
            handoffs,
            get_model_tracing_impl(
                run_config.tracing_disabled, run_config.trace_include_sensitive_data
            ),
            previous_response_id=previous_response_id
        )
        context_wrapper.usage.add(response.usage)
        return response

    @classmethod
    async def _get_single_step_result_from_response(
        cls,
        agent: Agent[TContext],
        context_wrapper: RunContextWrapper[TContext],
        orignal_input: str | List[TResponseInputItem],
        tool_use_tracker: AgentToolUseTracker,
        pre_step_items: List[RunItem],
        new_response: ModelResponse,
        hooks: RunHooks,
        handoffs: List[Handoff],
        run_config: RunConfig,
        output_schema: AgentOutputSchemaBase | None,
        all_tools: List[Tool]
    ) -> SingleStepResult:
        processed_response = RunImpl.process_model_response(
            agent=agent,
            all_tools=all_tools,
            response=new_response,
            output_schema=output_schema,
            handoffs=handoffs
        )
        tool_use_tracker.add_tool_use(agent, processed_response.tools_used)
        return await RunImpl.execute_tools_and_side_effects(
            agent=agent,
            original_input=orignal_input,
            pre_step_items=pre_step_items,
            new_response=new_response,
            output_schema=output_schema,
            hooks=hooks,
            context_wrapper=context_wrapper,
            run_config=run_config,
            processed_response=processed_response
        )
    
    @classmethod
    async def _run_single_turn(
        cls,
        *,
        agent: Agent[Any],
        context_wrapper: RunContextWrapper[TContext],
        tool_use_tracker: AgentToolUseTracker,
        run_config: RunConfig,
        all_tools: List[Tool],
        previous_response_id: str | None,
        should_run_agent_start_hook: bool,
        hooks: RunHooks,
        generated_items: List[RunItem],
        orignal_input: str | List[TResponseInputItem]
    ) -> SingleStepResult:
        if should_run_agent_start_hook:
            await asyncio.gather(
                hooks.on_agent_start(context_wrapper, agent),
                (
                    agent.hooks.on_start(context_wrapper, agent)
                    if agent.hooks else 
                    _coro.noop_coroutine()
                )
            )

        handoffs = cls._get_handoffs(agent)
        output_schema = cls._get_output_schema(agent)
        system_instructions = await agent.get_system_prompt(context_wrapper)

        input = ItemHelpers.input_to_new_input_list(orignal_input)
        input.extend([generated_item.to_input_item() for generated_item in generated_items])

        new_response = await cls._get_new_response(
            orignal_input,
            system_instructions,
            run_config,
            context_wrapper,
            agent,
            output_schema,
            all_tools,
            handoffs,
            tool_use_tracker,
            previous_response_id
        )

        return await cls._get_single_step_result_from_response(
            agent=agent,
            context_wrapper=context_wrapper,
            orignal_input=orignal_input,
            tool_use_tracker=tool_use_tracker,
            pre_step_items=generated_items,
            new_response=new_response,
            hooks=hooks,
            handoffs=handoffs,
            run_config=run_config,
            output_schema=output_schema,
            all_tools=all_tools
        )

    @classmethod
    async def run(
        cls,
        starting_agent: Agent[TContext],
        input: str | List[TResponseInputItem],
        *,
        run_config: RunConfig | None = None,
        context: TContext | None = None,
        max_turn: int = DEFAULT_MAX_TURN,
        hooks: RunHooks | None = None,
        previous_response_id: str | None = None,
    ):
        
        if hooks is None:
            hooks = RunHooks[Any]()
        if run_config is None:
            run_config = RunConfig()
        
        tool_use_tracker = AgentToolUseTracker()

        with TraceCtxManager(
            workflow_name=run_config.workflow_name,
            trace_id=run_config.trace_id,
            group_id=run_config.group_id,
            metadata=run_config.trace_metadata,
            disabled=run_config.tracing_disabled  
        ):
            current_turn: int = 0
            orignal_input: str | List[TResponseInputItem] = copy.deepcopy(input)
            generated_items: List[RunItem] = []
            model_responses: List[ModelResponse] = []

            context_wrapper = RunContextWrapper( #type: ignore
                context=context 
            )
            input_guardrail_results: List[InputGuardrailResult] = []
            current_agent = starting_agent
            current_span = None
            should_run_agent_start_hook = True


            try:
                while True:
                    if current_span is None:
                        handoff_names = [h.agent_name for h in cls._get_handoffs(current_agent)]
                        if output_schema := cls._get_output_schema(current_agent):
                            output_type_name = output_schema.name()
                        else:
                            output_type_name = "str"

                        current_span = agent_span(
                            name=current_agent.name,
                            handoffs=handoff_names,
                            output_type=output_type_name
                        )

                        current_span.start(mark_as_current=True)
                        all_tools = await cls._get_all_tools(current_agent)
                        current_span.span_data.tools = [t.name for t in all_tools]

                    current_turn += 1
                    if current_turn > max_turn:
                        _error_tracing.attach_error_to_span(
                            current_span,
                            SpanError(
                                message=f"Max Turn Exceeded {max_turn}",
                                data={"max_turn": max_turn}
                            )
                        )
                        
                        raise MaxTurnsExceeded(f"Max turn exceeded {max_turn}") 

                    if current_turn == 1:
                        input_guardrail_results, turn_results = await asyncio.gather(
                            cls._run_input_guardrails(
                                current_agent, 
                                orignal_input,
                                starting_agent.input_guardrails + (run_config.input_guardrails if run_config.input_guardrails else []),
                                context_wrapper,
                            ),
                            cls._run_single_turn( 
                                agent=current_agent, 
                                context_wrapper=context_wrapper,
                                generated_items=generated_items,
                                all_tools=all_tools,
                                hooks=hooks,
                                orignal_input=orignal_input,
                                run_config=run_config,
                                previous_response_id=previous_response_id,
                                should_run_agent_start_hook=should_run_agent_start_hook,
                                tool_use_tracker=tool_use_tracker,
                            )
                        )
                    else:
                        turn_results = await cls._run_single_turn( 
                            agent=current_agent, 
                            context_wrapper=context_wrapper,
                            generated_items=generated_items,
                            all_tools=all_tools,
                            hooks=hooks,
                            orignal_input=orignal_input,
                            run_config=run_config,
                            previous_response_id=previous_response_id,
                            should_run_agent_start_hook=should_run_agent_start_hook,
                            tool_use_tracker=tool_use_tracker,
                        )

                    should_run_agent_start_hook=False
                    model_responses.append(turn_results.model_response)
                    generated_items=turn_results.generated_items
                    orignal_input=turn_results.original_input

                    if isinstance(turn_results.next_step, NextStepFinalOutput):
                        output_gaurdrail_results = await cls._run_output_guardrails( 
                            current_agent,
                            turn_results.next_step.output,
                            context_wrapper,
                            current_agent.output_guardrails + (run_config.output_guardrails if run_config.output_guardrails else [])
                        )

                        return RunResult(
                            input=orignal_input,
                            context_wrapper=context_wrapper,
                            final_output=turn_results.next_step.output,
                            input_guardrail_results=input_guardrail_results,
                            output_guardrail_results=output_gaurdrail_results,
                            new_items=generated_items,
                            raw_responses=model_responses,
                            _last_agent=current_agent
                        )
                    elif isinstance(turn_results.next_step, NextStepHandoff):
                        current_agent = cast(Agent[TContext], turn_results.next_step.new_agent)
                        current_span.finish(reset_current=True)
                        current_span = None
                        should_run_agent_start_hook=True
                    elif isinstance(turn_results.next_step, NextStepRunAgain):
                        pass

                    else:
                        raise AgentsException(f"Invalid nest step output type: {type(turn_results.next_step)}")
            finally:
                if current_span:
                    current_span.finish(reset_current=True)
