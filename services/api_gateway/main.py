import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from orchestration.graph import app as graph_app
import uuid

app = FastAPI(title="Unified Agentic Concierge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    intent: str

class ChatResponse(BaseModel):
    session_id: str
    status: str
    response: Dict[str, Any]

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Entry point for user conversational requests.
    Initializes the LangGraph state and invokes the orchestrator.
    """
    session_id = str(uuid.uuid4())
    
    initial_state = {
        "session_id": session_id,
        "user_id": request.user_id,
        "user_intent": request.intent,
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
        "confidence_score": 1.0
    }
    
    try:
        # Execute the LangGraph workflow
        final_state = graph_app.invoke(initial_state)
        
        return ChatResponse(
            session_id=session_id,
            status=final_state.get("booking_status", "unknown"),
            response={"recommendations": final_state.get("final_recommendations")}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
