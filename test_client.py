import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("ERROR: GOOGLE_API_KEY is not set. Please create a .env file or export it.")
    sys.exit(1)

# Import the LangGraph app directly for local CLI testing without needing the FastAPI server running
from orchestration.graph import app as graph_app
import uuid

def main():
    print("========================================================")
    print("   Unified Agentic Concierge - Interactive Test CLI")
    print("========================================================")
    print("Type 'exit' to quit.")
    
    user_id = "test_user_001"
    
    while True:
        intent = input("\n[User]: ")
        if intent.lower() in ['exit', 'quit']:
            break
            
        if not intent.strip():
            continue
            
        session_id = str(uuid.uuid4())
        
        initial_state = {
            "session_id": session_id,
            "user_id": user_id,
            "user_intent": intent,
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
        
        print("\n[Concierge Orchestrator]: Processing request through multi-agent LangGraph...")
        
        try:
            # Stream the execution to see the node transitions
            for output in graph_app.stream(initial_state):
                for key, value in output.items():
                    print(f" -> Node completed: '{key}'")
            
            # Execute one final invoke to get the end state
            final_state = graph_app.invoke(initial_state)
            
            print("\n================ FINAL RESULT ================")
            print(f"Status: {final_state.get('booking_status')}")
            
            recs = final_state.get("final_recommendations")
            if recs:
                print(f"Booked Recommendation: {json.dumps(recs[0], indent=2)}")
            else:
                print("No booking was completed. Review reflection feedback or constraints.")
                print(f"Reflection Feedback: {final_state.get('reflection_feedback')}")
                
            print("==============================================")
            
        except Exception as e:
            print(f"\n[Error]: Orchestration failed: {e}")

if __name__ == "__main__":
    main()
