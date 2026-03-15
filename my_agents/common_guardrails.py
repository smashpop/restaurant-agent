from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, input_guardrail

from models import InputGuardRailOutput, UserAccountContext


input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    Classify the user's message with two booleans:
    - is_off_topic: true if the request is not related to restaurant customer support
    - is_inappropriate: true if the message contains abusive, insulting, hateful, sexually explicit, threatening, or otherwise inappropriate language

    Ensure the user's request is related to restaurant customer support and not off-topic.

    Consider it ON-TOPIC only when the user asks about restaurant-related matters such as:
    - menu, ingredients, allergens, and nutrition
    - reservations, waitlist, table availability, and operating hours
    - dine-in, takeout, delivery, and order status
    - pricing, promotions, payments, receipts, and refunds for restaurant orders
    - location, parking, accessibility, and contact details
    - complaints, service feedback, and issue resolution related to restaurant service

    Consider it OFF-TOPIC when the user asks about unrelated domains (for example coding help, finance advice, travel planning, general trivia, or any non-restaurant business support).

    If the request is off-topic or inappropriate, return a clear reason for the tripwire.
    You may do brief small talk at the beginning, but do not provide help for requests unrelated to restaurant customer support.

    Output rules:
    - Set both booleans explicitly (true or false)
    - If both conditions apply, set both to true
    - Always provide a short reason
""",
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=wrapper.context,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=(
            result.final_output.is_off_topic
            or result.final_output.is_inappropriate
        ),
    )