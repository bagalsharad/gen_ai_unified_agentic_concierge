import os
import traceback
from dotenv import load_dotenv
load_dotenv()
from orchestration.graph import app as graph_app
import uuid

initial_state = {
    "session_id": str(uuid.uuid4()),
    "user_id": "test_user",
    "user_intent": "I want sushi",
    "parsed_constraints": {},
    "discovered_inventory": [],
    "inferred_preferences": None,
    "proposed_itinerary": [],
    "booking_status": "pending",
    "reflection_feedback": [],
    "final_recommendations": [],
    "audit_log": [],
    "event_trace": [],
    "conversation_history": [],
    "confidence_score": 1.0,
    "iteration": 0
}

try:
    final_state = graph_app.invoke(initial_state)
    print("Success")
except Exception as e:
    traceback.print_exc()
