from langgraph.graph import StateGraph, END
from schemas.state import ConciergeState
from agents.concierge import concierge_node
from agents.discovery import discovery_node
from agents.preference import preference_node
from agents.reflection import reflection_node
from agents.booking import booking_node

def should_reflect(state: ConciergeState) -> str:
    """Determine if the proposed itinerary needs reflection/audit."""
    iteration = state.get("iteration", 0)
    
    # If we've looped too many times, break out to booking to prevent infinite loops
    if iteration > 2:
        print("--- Orchestrator: Max iterations reached, forcing booking ---")
        return "booking"
        
    if state.get("proposed_itinerary") and not state.get("reflection_feedback"):
        return "reflection"
    if state.get("reflection_feedback") and state.get("confidence_score", 1.0) < 0.8:
        return "concierge" # Retry building itinerary
    return "booking"

def route_from_concierge(state: ConciergeState) -> str:
    """Route from concierge based on what information is missing."""
    if not state.get("inferred_preferences"):
        return "preference"
    if not state.get("discovered_inventory"):
        return "discovery"
    if state.get("proposed_itinerary"):
        return "reflection"
    return END

def concierge_wrapper(state: ConciergeState) -> dict:
    """Wraps the concierge node to increment iteration."""
    iteration = state.get("iteration", 0) + 1
    updates = concierge_node(state)
    updates["iteration"] = iteration
    return updates

def build_graph() -> StateGraph:
    workflow = StateGraph(ConciergeState)

    # Add Nodes
    workflow.add_node("concierge", concierge_wrapper)
    workflow.add_node("discovery", discovery_node)
    workflow.add_node("preference", preference_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("booking", booking_node)

    # Set Entry Point
    workflow.set_entry_point("concierge")

    # Add Edges
    workflow.add_conditional_edges(
        "concierge",
        route_from_concierge,
        {
            "preference": "preference",
            "discovery": "discovery",
            "reflection": "reflection",
            END: END
        }
    )

    workflow.add_edge("preference", "concierge")
    workflow.add_edge("discovery", "concierge")

    workflow.add_conditional_edges(
        "reflection",
        should_reflect,
        {
            "concierge": "concierge", # Retry loop
            "booking": "booking"
        }
    )

    workflow.add_edge("booking", END)

    return workflow.compile()

app = build_graph()
