from my_agents.common_helpers import make_handoff
from my_agents.complaint_agent import complaint_agent
from my_agents.menu_agent import menu_agent
from my_agents.order_agent import order_agent
from my_agents.reservation_agent import reservation_agent
from my_agents.triage_agent import triage_agent


_WIRED = False


def wire_all_agent_handoffs() -> None:
    """Wire hub-and-spoke handoffs with triage as the central router."""
    global _WIRED
    if _WIRED:
        return

    triage_agent.handoffs = [
        make_handoff(menu_agent),
        make_handoff(reservation_agent),
        make_handoff(order_agent),
        make_handoff(complaint_agent),
    ]

    order_agent.handoffs = [make_handoff(triage_agent)]
    menu_agent.handoffs = [make_handoff(triage_agent)]
    reservation_agent.handoffs = [make_handoff(triage_agent)]
    complaint_agent.handoffs = [make_handoff(triage_agent)]

    _WIRED = True