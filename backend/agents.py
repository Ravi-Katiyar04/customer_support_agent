# backend/agents.py
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.tool_context import ToolContext
from google.genai import types


retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1
)

# ---------------- TOOL FUNCTIONS ----------------

def product_catalog_lookup(product_name: str) -> dict:
    catalog = {
        "iphone 15 pro": "iPhone 15 Pro, $999, Low Stock (8 units), Titanium",
        "dell xps 15": "Dell XPS 15, $1299, In Stock (45 units), 16GB RAM",
        "sony wh-1000xm5": "Sony WH-1000XM5, $399, In Stock (67 units)"
    }
    result = catalog.get(product_name.lower())
    if result:
        return {"status": "success", "product_info": result}
    return {"status": "error", "error_message": f"Product '{product_name}' not found"}


def order_lookup(order_id: str) -> dict:
    orders = {
        "ORD-001": {"order_id": "ORD-001", "customer": "Ravi", "amount": 250.0, "status": "DELIVERED"},
        "ORD-002": {"order_id": "ORD-002", "customer": "Sam", "amount": 75.0, "status": "RETURNED"},
    }
    result = orders.get(order_id)
    if result:
        return {"status": "success", "order": result}
    return {"status": "error", "error_message": "Order not found"}


LARGE_REFUND_THRESHOLD = 100.0

def request_refund(order_id: str, amount: float, tool_context: ToolContext) -> dict:
    # Automatic small refunds
    if amount <= LARGE_REFUND_THRESHOLD:
        return {
            "status": "approved",
            "refund_id": f"REF-{order_id}-AUTO",
            "amount": amount
        }

    # First call — request approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"Approve refund of ${amount} for order {order_id}?",
            payload={"order_id": order_id, "amount": amount}
        )
        return {"status": "pending", "message": "Awaiting human approval"}

    # After approval response
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "refund_id": f"REF-{order_id}-HUMAN",
            "amount": amount
        }
    else:
        return {"status": "rejected", "message": "Refund rejected"}


# ---------------- LLM AGENTS ----------------

product_catalog_agent = LlmAgent(
    name="product_catalog_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="You are a product catalog agent.",
    tools=[product_catalog_lookup],
)

support_agent = LlmAgent(
    name="customer_support_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
You are a customer support agent.
Use product_catalog_agent for product info.
Use order_lookup for order details.
Use request_refund for refunds and follow approval workflow.
""",
    tools=[
        AgentTool(agent=product_catalog_agent),
        order_lookup,
        request_refund
    ],
)

# ---------------- APP WRAPPER ----------------

support_app = App(
    name="agents",
    root_agent=support_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)
