import dotenv

dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from models import UserAccountContext
from my_agents.triage_agent import triage_agent
from my_agents.handoff_registry import wire_all_agent_handoffs

client = OpenAI()
wire_all_agent_handoffs()

MAX_HANDOFFS_PER_MESSAGE = 2

user_account_ctx = UserAccountContext(
    customer_id=1,
    name="홍길동",
    tier="basic",
)


if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "restaurant-agent-memory.db",
    )
session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent


async def paint_history():
    messages = await session.get_items()
    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"].replace("$", "\$"))


asyncio.run(paint_history())


async def run_agent(message):

    with st.chat_message("ai"):
        text_placeholder = st.empty()
        response = ""

        st.session_state["text_placeholder"] = text_placeholder
        handoff_count = 0

        try:

            stream = Runner.run_streamed(
                st.session_state["agent"],
                message,
                session=session,
                context=user_account_ctx,
            )

            async for event in stream.stream_events():
                if event.type == "raw_response_event":

                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response.replace("$", "\$"))

                elif event.type == "agent_updated_stream_event":

                    if st.session_state["agent"].name != event.new_agent.name:
                        handoff_count += 1
                        if handoff_count > MAX_HANDOFFS_PER_MESSAGE:
                            st.session_state.get("text_placeholder", text_placeholder).empty()
                            st.write(
                                "죄송합니다. 문의를 다시 해주세요. 담당자에게 연결해드리겠습니다."
                            )
                            st.session_state["agent"] = triage_agent
                            break
                        
                        st.write(f"🤖 Transfered from {st.session_state['agent'].name} to {event.new_agent.name}")

                        st.session_state["agent"] = event.new_agent

                        text_placeholder = st.empty()

                        st.session_state["text_placeholder"] = text_placeholder
                        response = ""

        except InputGuardrailTripwireTriggered:
            st.session_state.get("text_placeholder", text_placeholder).empty()
            st.write("I'm sorry, but I can't assist with that request.")


        except OutputGuardrailTripwireTriggered:
            st.session_state.get("text_placeholder", text_placeholder).empty()
            st.write("I'm sorry, but I can't show you that answer.")

message = st.chat_input(
    "Write a message for your assistant",
)

if message:

    if message:
        with st.chat_message("human"):
            st.write(message)
        asyncio.run(run_agent(message))


# with st.sidebar:
#     reset = st.button("Reset memory")
#     if reset:
#         asyncio.run(session.clear_session())
#     st.write(asyncio.run(session.get_items()))