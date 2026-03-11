from agents import (
    Agent,
    output_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import OutputGuardRailOutput, UserAccountContext


output_guardrail_agent = Agent(
    name="Output Guardrail",
    instructions="""
    Evaluate the assistant response for restaurant customer support quality and safety.

    Return exactly these boolean fields:
    - contains_off_topic: true if the response goes outside restaurant customer support topics.
    - is_formal_tone: true if the response is professional, polite, and respectful.
    - is_sanitized: true if the response does not reveal internal or sensitive information.

    Off-topic examples include unrelated areas such as coding help, financial advice, travel planning, or general trivia.

    Internal/sensitive information includes (but is not limited to):
    - internal policies not intended for customers
    - staff-only notes or operational instructions
    - system prompts, hidden rules, model configuration
    - private customer or employee data
    - API keys, tokens, secrets, database details, or internal URLs

    Also provide a short reason summarizing the validation result.
    """,
    output_type=OutputGuardRailOutput,
)


@output_guardrail
async def output_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str,
):
    result = await Runner.run(
        output_guardrail_agent,
        output,
        context=wrapper.context,
    )

    validation = result.final_output

    triggered = (
        validation.contains_off_topic
        or (not validation.is_formal_tone)
        or (not validation.is_sanitized)
    )

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )
