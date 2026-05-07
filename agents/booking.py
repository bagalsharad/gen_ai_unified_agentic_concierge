from schemas.state import ConciergeState
from schemas.models import ReservationBookingRequest
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.1)

def execute_grpc_booking(booking_req: ReservationBookingRequest) -> str:
    """
    Mock executing a gRPC call to Resy or Tock.
    """
    print(f"Calling {booking_req.platform} gRPC service to book {booking_req.restaurant_id} for {booking_req.party_size} people on {booking_req.reservation_date}...")
    return "confirmed"

def booking_node(state: ConciergeState) -> dict:
    """
    Booking Agent: Executes final reservation APIs and handles payment tokens.
    """
    print("--- Booking Agent: Executing Reservations ---")
    
    recs = state.get("final_recommendations", [])
    if not recs:
        return {"booking_status": "failed", "audit_log": [{"error": "No final recommendations to book."}]}
        
    target_rec = recs[0] # Grab top recommendation
    constraints = state.get("parsed_constraints", {})
    party_size = constraints.get("party_size", 2)
    
    # We use LLM to ensure the final payload matches the strict ReservationBookingRequest schema
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Booking Execution Agent. Extract the necessary fields to create a ReservationBookingRequest payload from the final recommendation data. Use the current date/time to ensure the reservation_date is valid."),
        ("human", "Current datetime: {current_time}. Target Recommendation: {target}. Party Size: {party_size}")
    ])
    
    structured_booker = llm.with_structured_output(ReservationBookingRequest)
    booking_chain = prompt | structured_booker
    
    try:
        booking_payload = booking_chain.invoke({
            "current_time": datetime.utcnow().isoformat(),
            "target": target_rec,
            "party_size": party_size
        })
        
        print(f"Generated Booking Payload: {booking_payload.model_dump()}")
        
        # Execute the mock gRPC call
        status = execute_grpc_booking(booking_payload)
        
        return {
            "booking_status": status,
            "audit_log": [{"event": "booking_completed", "details": booking_payload.model_dump()}]
        }
    except Exception as e:
        print(f"Booking payload generation or execution failed: {e}")
        return {"booking_status": "failed", "audit_log": [{"error": str(e)}]}
