import streamlit as st
from agents import function_tool, AgentHooks, Agent, Tool, RunContextWrapper
from models import UserAccountContext
import random
from datetime import datetime, timedelta


# =============================================================================
# TECHNICAL SUPPORT TOOLS
# =============================================================================


@function_tool
def run_diagnostic_check(
    context: UserAccountContext, product_name: str, issue_description: str
) -> str:
    """
    Run a diagnostic check on the customer's product to identify potential issues.

    Args:
        product_name: Name of the product experiencing issues
        issue_description: Description of the problem
    """
    diagnostics = [
        "✅ Server connectivity: Normal",
        "✅ API endpoints: Responsive",
        "⚠️  Cache memory: 85% full (recommend clearing)",
        "✅ Database connections: Stable",
        "⚠️  Last update: 7 days ago (update available)",
    ]

    return f"🔍 Diagnostic results for {product_name}:\n" + "\n".join(diagnostics)


@function_tool
def provide_troubleshooting_steps(context: UserAccountContext, issue_type: str) -> str:
    """
    Provide step-by-step troubleshooting instructions for common issues.

    Args:
        issue_type: Type of issue (connection, login, performance, crash, etc.)
    """
    steps_map = {
        "connection": [
            "1. Check internet connectivity",
            "2. Clear browser cache and cookies",
            "3. Disable browser extensions temporarily",
            "4. Try incognito/private browsing mode",
            "5. Restart your router/modem",
        ],
        "login": [
            "1. Verify username and password",
            "2. Check caps lock is off",
            "3. Clear browser cache",
            "4. Try password reset if needed",
            "5. Disable VPN temporarily",
        ],
        "performance": [
            "1. Close unnecessary browser tabs",
            "2. Clear browser cache",
            "3. Check available RAM and storage",
            "4. Update your browser",
            "5. Restart the application",
        ],
        "crash": [
            "1. Update to latest version",
            "2. Restart the application",
            "3. Check system requirements",
            "4. Disable conflicting software",
            "5. Run in safe mode",
        ],
    }

    steps = steps_map.get(
        issue_type.lower(),
        [
            "1. Restart the application",
            "2. Check for updates",
            "3. Contact support with error details",
        ],
    )

    context.add_troubleshooting_step(f"Provided {issue_type} troubleshooting steps")
    return f"🛠️ Troubleshooting steps for {issue_type}:\n" + "\n".join(steps)


@function_tool
def escalate_to_engineering(
    context: UserAccountContext, issue_summary: str, priority: str = "medium"
) -> str:
    """
    Escalate a technical issue to the engineering team.

    Args:
        issue_summary: Brief summary of the technical issue
        priority: Priority level (low, medium, high, critical)
    """
    ticket_id = f"ENG-{random.randint(10000, 99999)}"

    return f"""
🚀 Issue escalated to Engineering Team
📋 Ticket ID: {ticket_id}
⚡ Priority: {priority.upper()}
📝 Summary: {issue_summary}
🕐 Expected response: {2 if context.is_premium_customer() else 4} hours
    """.strip()


# =============================================================================
# BILLING SUPPORT TOOLS
# =============================================================================


@function_tool
def lookup_billing_history(context: UserAccountContext, months_back: int = 6) -> str:
    """
    Look up customer's billing history and payment records.

    Args:
        months_back: Number of months to look back (default 6)
    """
    payments = []
    for i in range(months_back):
        date = datetime.now() - timedelta(days=30 * i)
        amount = random.choice([29.99, 49.99, 99.99])
        status = random.choice(["Paid", "Paid", "Paid", "Failed"])
        payments.append(f"• {date.strftime('%b %Y')}: ${amount} - {status}")

    return f"💳 Billing History (Last {months_back} months):\n" + "\n".join(payments)


@function_tool
def process_refund_request(
    context: UserAccountContext, refund_amount: float, reason: str
) -> str:
    """
    Process a refund request for the customer.

    Args:
        refund_amount: Amount to refund
        reason: Reason for the refund
    """
    processing_days = 3 if context.is_premium_customer() else 5
    refund_id = f"REF-{random.randint(100000, 999999)}"

    return f"""
✅ Refund request processed
🔗 Refund ID: {refund_id}
💰 Amount: ${refund_amount}
📝 Reason: {reason}
⏱️ Processing time: {processing_days} business days
💳 Refund will appear on original payment method
    """.strip()


@function_tool
def update_payment_method(context: UserAccountContext, payment_type: str) -> str:
    """
    Help customer update their payment method.

    Args:
        payment_type: Type of payment method (credit_card, paypal, bank_transfer)
    """
    return f"""
💳 Payment method update initiated
📋 Type: {payment_type.replace('_', ' ').title()}
🔒 Secure link sent to: {context.email}
⏰ Link expires in: 24 hours
✅ No interruption to current service
    """.strip()


@function_tool
def apply_billing_credit(
    context: UserAccountContext, credit_amount: float, reason: str
) -> str:
    """
    Apply account credit for billing issues or compensation.

    Args:
        credit_amount: Amount of credit to apply
        reason: Reason for the credit
    """
    return f"""
🎁 Account credit applied
💰 Credit amount: ${credit_amount}
📝 Reason: {reason}
⚡ Applied to account: {context.customer_id}
📧 Confirmation sent to: {context.email}
    """.strip()


# =============================================================================
# ORDER MANAGEMENT TOOLS
# =============================================================================


@function_tool
def lookup_order_status(context: UserAccountContext, order_number: str) -> str:
    """
    Look up the current status and details of an order.

    Args:
        order_number: Customer's order number
    """
    statuses = ["processing", "shipped", "in_transit", "delivered"]
    current_status = random.choice(statuses)

    tracking_number = f"1Z{random.randint(100000, 999999)}"
    estimated_delivery = datetime.now() + timedelta(days=random.randint(1, 5))

    return f"""
📦 Order Status: {order_number}
🏷️ Status: {current_status.title()}
🚚 Tracking: {tracking_number}
📅 Estimated delivery: {estimated_delivery.strftime('%B %d, %Y')}
📍 Shipping to: {context.email}
    """.strip()


@function_tool
def initiate_return_process(
    context: UserAccountContext, order_number: str, return_reason: str, items: str
) -> str:
    """
    Start the return process for an order.

    Args:
        order_number: Order number to return
        return_reason: Reason for return
        items: Items being returned
    """
    return_id = f"RET-{random.randint(100000, 999999)}"
    return_label_fee = 0 if context.is_premium_customer() else 5.99

    return f"""
📦 Return initiated
🔗 Return ID: {return_id}
📋 Order: {order_number}
📝 Items: {items}
💰 Return label fee: ${return_label_fee}
📧 Return label sent to: {context.email}
⏰ Return window: 30 days
    """.strip()


@function_tool
def schedule_redelivery(
    context: UserAccountContext, tracking_number: str, preferred_date: str
) -> str:
    """
    Schedule a redelivery for a failed delivery attempt.

    Args:
        tracking_number: Package tracking number
        preferred_date: Customer's preferred delivery date
    """
    return f"""
🚚 Redelivery scheduled
📦 Tracking: {tracking_number}
📅 New delivery date: {preferred_date}
🏠 Address confirmed: {context.email}
📞 Driver will call 30 minutes before delivery
    """.strip()


@function_tool
def expedite_shipping(context: UserAccountContext, order_number: str) -> str:
    """
    Upgrade shipping speed for an order (premium customers only).

    Args:
        order_number: Order to expedite
    """
    if not context.is_premium_customer():
        return "❌ Expedited shipping upgrade requires Premium membership"

    return f"""
⚡ Shipping expedited
📦 Order: {order_number}
🚀 Upgraded to: Next-day delivery
💰 No additional charge (Premium benefit)
📧 Updated tracking sent to: {context.email}
    """.strip()


# =============================================================================
# ACCOUNT MANAGEMENT TOOLS
# =============================================================================


@function_tool
def reset_user_password(context: UserAccountContext, email: str) -> str:
    """
    Send password reset instructions to the customer's email.

    Args:
        email: Email address to send reset instructions
    """
    reset_token = f"RST-{random.randint(100000, 999999)}"

    return f"""
🔐 Password reset initiated
📧 Reset link sent to: {email}
🔗 Reset token: {reset_token}
⏰ Link expires in: 1 hour
🛡️ For security, link is single-use only
    """.strip()


@function_tool
def enable_two_factor_auth(context: UserAccountContext, method: str = "app") -> str:
    """
    Help customer set up two-factor authentication.

    Args:
        method: 2FA method (app, sms, email)
    """
    setup_code = f"2FA-{random.randint(100000, 999999)}"

    return f"""
🔒 Two-Factor Authentication Setup
📱 Method: {method.upper()}
🔑 Setup code: {setup_code}
📧 Instructions sent to: {context.email}
⚡ Enhanced security activated
    """.strip()


@function_tool
def update_account_email(
    context: UserAccountContext, old_email: str, new_email: str
) -> str:
    """
    Process account email address change.

    Args:
        old_email: Current email address
        new_email: New email address
    """
    verification_code = f"VER-{random.randint(100000, 999999)}"

    return f"""
📧 Email update requested
📤 From: {old_email}
📥 To: {new_email}
🔐 Verification code: {verification_code}
⏰ Code expires in: 30 minutes
✅ Change will be activated after verification
    """.strip()


@function_tool
def deactivate_account(
    context: UserAccountContext, reason: str, feedback: str = ""
) -> str:
    """
    Process account deactivation request.

    Args:
        reason: Reason for account deactivation
        feedback: Optional feedback from customer
    """
    return f"""
⚠️ Account deactivation initiated
👤 Account: {context.customer_id}
📝 Reason: {reason}
💬 Feedback: {feedback if feedback else 'None provided'}
⏰ Account will be deactivated in 24 hours
🔄 Can be reactivated within 30 days
📧 Confirmation sent to: {context.email}
    """.strip()


@function_tool
def export_account_data(context: UserAccountContext, data_types: str) -> str:
    """
    Generate export of customer's account data.

    Args:
        data_types: Types of data to export (profile, orders, billing, etc.)
    """
    export_id = f"EXP-{random.randint(100000, 999999)}"

    return f"""
📊 Data export requested
🔗 Export ID: {export_id}
📋 Data types: {data_types}
⏱️ Processing time: 2-4 hours
📧 Download link will be sent to: {context.email}
🔒 Link expires in: 7 days
    """.strip()


# =============================================================================
# MENU TOOLS
# =============================================================================


@function_tool
def lookup_menu_items(context: UserAccountContext, query: str) -> str:
    """
    Look up menu items, descriptions, and prices matching the customer's query.

    Args:
        query: Dish name, category, or keyword to search (e.g. "pasta", "vegan", "dessert")
    """
    sample_items = [
        {"name": "Grilled Salmon", "category": "Main", "price": 24.99, "description": "Atlantic salmon with lemon herb butter"},
        {"name": "Margherita Pizza", "category": "Pizza", "price": 16.99, "description": "Tomato, fresh mozzarella, basil"},
        {"name": "Caesar Salad", "category": "Starter", "price": 12.99, "description": "Romaine, parmesan, croutons, caesar dressing"},
        {"name": "Truffle Pasta", "category": "Main", "price": 22.99, "description": "Fresh tagliatelle with black truffle cream"},
        {"name": "Tiramisu", "category": "Dessert", "price": 9.99, "description": "Classic Italian tiramisu with espresso"},
        {"name": "Veggie Burger", "category": "Main", "price": 14.99, "description": "Plant-based patty with avocado and house sauce"},
    ]

    keyword = query.lower()
    matches = [
        item for item in sample_items
        if keyword in item["name"].lower()
        or keyword in item["category"].lower()
        or keyword in item["description"].lower()
    ]

    if not matches:
        matches = sample_items[:3]

    lines = [f"• {i['name']} ({i['category']}) — ${i['price']:.2f}: {i['description']}" for i in matches]
    return f"🍽️ Menu results for '{query}':\n" + "\n".join(lines)


@function_tool
def check_allergens(context: UserAccountContext, dish_name: str) -> str:
    """
    Return allergen and dietary information for a specific dish.

    Args:
        dish_name: Name of the dish to check
    """
    allergen_data = {
        "grilled salmon": {"allergens": ["fish"], "dietary": ["gluten-free", "dairy-free"]},
        "margherita pizza": {"allergens": ["gluten", "dairy"], "dietary": ["vegetarian"]},
        "caesar salad": {"allergens": ["gluten", "dairy", "eggs", "fish (anchovies)"], "dietary": []},
        "truffle pasta": {"allergens": ["gluten", "dairy", "eggs"], "dietary": ["vegetarian"]},
        "tiramisu": {"allergens": ["gluten", "dairy", "eggs"], "dietary": ["vegetarian"]},
        "veggie burger": {"allergens": ["gluten", "soy"], "dietary": ["vegan", "dairy-free"]},
    }

    key = dish_name.lower().strip()
    info = allergen_data.get(key)

    if not info:
        return (
            f"⚠️ Allergen details for '{dish_name}' are not on record in our system. "
            "Please ask a staff member in-restaurant for the most up-to-date information."
        )

    allergens_str = ", ".join(info["allergens"]) if info["allergens"] else "None listed"
    dietary_str = ", ".join(info["dietary"]) if info["dietary"] else "None"

    return f"""
🥦 Allergen Info: {dish_name.title()}
⚠️  Contains: {allergens_str}
✅ Dietary labels: {dietary_str}
ℹ️  Always inform staff of severe allergies before ordering.
    """.strip()


@function_tool
def get_daily_specials(context: UserAccountContext) -> str:
    """
    Return today's chef specials and promotional items.
    """
    specials = [
        {"name": "Lobster Bisque", "price": 14.99, "note": "Chef's special — limited availability"},
        {"name": "Wagyu Beef Burger", "price": 28.99, "note": "Weekend special"},
        {"name": "Seasonal Berry Tart", "price": 10.99, "note": "Dessert of the day"},
    ]

    lines = [f"⭐ {s['name']} — ${s['price']:.2f}  ({s['note']})" for s in specials]
    return "🍴 Today's Specials:\n" + "\n".join(lines)


# =============================================================================
# RESERVATION TOOLS
# =============================================================================


@function_tool
def check_table_availability(
    context: UserAccountContext, date: str, time: str, party_size: int
) -> str:
    """
    Check available tables for a given date, time, and party size.

    Args:
        date: Desired date in YYYY-MM-DD format
        time: Desired time in HH:MM format (24-hour)
        party_size: Number of guests
    """
    available_slots = ["18:00", "18:30", "19:00", "20:30", "21:00"]
    requested = time.strip()

    if requested in available_slots:
        availability = f"✅ {time} is available for {party_size} guests on {date}."
    else:
        alternatives = ", ".join(available_slots[:3])
        availability = (
            f"❌ {time} is fully booked for {party_size} guests on {date}. "
            f"Available slots: {alternatives}"
        )

    return f"📅 Table Availability — {date}\n{availability}"


@function_tool
def make_reservation(
    context: UserAccountContext, date: str, time: str, party_size: int, special_requests: str = ""
) -> str:
    """
    Create a new table reservation for the customer.

    Args:
        date: Reservation date in YYYY-MM-DD format
        time: Reservation time in HH:MM format (24-hour)
        party_size: Number of guests
        special_requests: Optional special requests (e.g. high chair, window seat, anniversary)
    """
    reservation_id = f"RES-{random.randint(100000, 999999)}"

    return f"""
✅ Reservation Confirmed
🔖 Reservation ID: {reservation_id}
👤 Name: {context.name}
📅 Date: {date}  ⏰ Time: {time}
👥 Party size: {party_size}
💬 Special requests: {special_requests if special_requests else 'None'}
📧 Confirmation sent to: {context.email}
ℹ️  Please arrive 5 minutes early. Cancellations accepted up to 2 hours before.
    """.strip()


@function_tool
def cancel_or_modify_reservation(
    context: UserAccountContext, reservation_id: str, action: str, new_details: str = ""
) -> str:
    """
    Cancel or modify an existing reservation.

    Args:
        reservation_id: The reservation ID to cancel or modify
        action: Either 'cancel' or 'modify'
        new_details: For modifications, describe the changes (date/time/party size)
    """
    if action.lower() == "cancel":
        return f"""
🚫 Reservation Cancelled
🔖 Reservation ID: {reservation_id}
👤 Name: {context.name}
📧 Cancellation confirmation sent to: {context.email}
ℹ️  We hope to welcome you another time.
        """.strip()
    else:
        return f"""
✏️ Reservation Modified
🔖 Reservation ID: {reservation_id}
📝 Changes requested: {new_details if new_details else 'Not specified'}
📧 Updated confirmation will be sent to: {context.email}
ℹ️  Please confirm any changes with the restaurant directly if time-sensitive.
        """.strip()


class AgentToolUsageLoggingHooks(AgentHooks):

    async def on_tool_start(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        tool: Tool,
    ):
        with st.sidebar:
            st.write(f"🔧 **{agent.name}** starting tool: `{tool.name}`")

    async def on_tool_end(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        tool: Tool,
        result: str,
    ):
        with st.sidebar:
            st.write(f"🔧 **{agent.name}** used tool: `{tool.name}`")
            st.code(result)

    async def on_handoff(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        source: Agent[UserAccountContext],
    ):
        with st.sidebar:
            st.write(f"🔄 Handoff: **{source.name}** → **{agent.name}**")

    async def on_start(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
    ):
        with st.sidebar:
            st.write(f"🚀 **{agent.name}** activated")

    async def on_end(
        self,
        context: RunContextWrapper[UserAccountContext],
        agent: Agent[UserAccountContext],
        output,
    ):
        with st.sidebar:
            st.write(f"🏁 **{agent.name}** completed")
