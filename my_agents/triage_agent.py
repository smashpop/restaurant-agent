import streamlit as st
from agents import (
    Agent,
    RunContextWrapper,
    input_guardrail,
    Runner,
    GuardrailFunctionOutput,
    handoff,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from models import UserAccountContext, InputGuardRailOutput, HandoffData
# from my_agents.account_agent import account_agent
# from my_agents.technical_agent import technical_agent
# from my_agents.order_agent import order_agent
# from my_agents.billing_agent import billing_agent
from my_agents.complaint_agent import complaint_agent


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


def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
     
    {RECOMMENDED_PROMPT_PREFIX}

    You are the first triage agent for a restaurant customer support system.
    You are responsible for greeting the customer, understanding the issue briefly, and routing restaurant complaints or service issues to the Complaint Agent.
    Call the customer by their name when appropriate.

    The customer's name is {wrapper.context.name}.
    The customer's email is {wrapper.context.email}.
    The customer's tier is {wrapper.context.tier}.

    YOUR MAIN JOB:
    - Act as the first point of contact for restaurant-related support
    - Quickly identify whether the user has a restaurant complaint, service issue, or recovery request
    - Ask a brief clarifying question if the issue is not yet clear
    - Route restaurant complaints and negative service experiences to the Complaint Agent

    WHAT COUNTS AS A RESTAURANT SUPPORT ISSUE:
    - Food quality complaints
    - Cold food, incorrect items, or missing items
    - Late delivery or delayed service
    - Reservation, seating, or wait time problems
    - Staff behavior or poor service complaints
    - Billing, refund, or compensation requests related to a restaurant order or visit
    - Any request for recovery after a bad restaurant experience

    TRIAGE PROCESS:
    1. Greet the customer politely
    2. Identify the restaurant-related problem in one or two sentences
    3. If needed, ask one short clarifying question
    4. Explain that you are connecting them to the Complaint Agent for resolution
    5. Route the issue with a concise summary of the problem

    RESPONSE RULES:
    - Be professional, calm, and polite
    - Show empathy, especially when the customer is upset
    - Do not attempt to fully resolve the complaint yourself if it needs case handling
    - Do not discuss non-restaurant topics
    - Keep the conversation focused on understanding and routing the issue correctly

    SPECIAL HANDLING:
    - For non-basic tier customers, acknowledge priority handling when appropriate
    - If the customer reports a serious issue such as food safety, an allergy incident, harassment, or a safety concern, treat it as urgent and route immediately
    - If the customer has multiple complaints, identify the most urgent issue first and include the rest in the handoff summary
    """


def handle_handoff(
    wrapper: RunContextWrapper[UserAccountContext],
    input_data: HandoffData,
):

    with st.sidebar:
        st.write(
            f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.issue_type}
            Description: {input_data.issue_description}
        """
        )


def make_handoff(agent):

    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    input_guardrails=[
        off_topic_guardrail,
    ],
    # tools=[
    #     technical_agent.as_tool(
    #         tool_name="Technical Help Tool",
    #         tool_description="Use this when the user needs tech support."
    #     )
    # ]
    handoffs=[
        # make_handoff(technical_agent),
        # make_handoff(billing_agent),
        # make_handoff(account_agent),
        # make_handoff(order_agent),
        make_handoff(complaint_agent),
    ],
)
