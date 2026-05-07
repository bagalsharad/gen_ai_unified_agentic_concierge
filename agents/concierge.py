import os
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from schemas.state import ConciergeState

# Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.1)

class IntentExtraction(BaseModel):
    cuisine: Optional[str] = Field(None, description="Requested cuisine type, e.g., 'Japanese'")
    location: Optional[str] = Field(None, description="Requested location or neighborhood")
    party_size: Optional[int] = Field(None, description="Number of guests requested")
    date_time_hint: Optional[str] = Field(None, description="Time or date requested, e.g., 'Friday night'")
    budget: Optional[str] = Field(None, description="Requested budget tier, e.g., '$$$'")

def concierge_node(state: ConciergeState) -> dict:
    """
    Concierge Master Agent: Interprets intent, delegates tasks, and builds itinerary.
    """
    print("--- Concierge Agent: Processing ---")
    
    updates = {}
    
    # Phase 1: Parse intent if not already parsed
    parsed_constraints = state.get("parsed_constraints", {})
    if not parsed_constraints and state.get("user_intent"):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert dining concierge. Extract the dining constraints from the user's request. If a constraint is not mentioned, leave it null."),
            ("human", "{intent}")
        ])
        
        structured_llm = llm.with_structured_output(IntentExtraction)
        chain = prompt | structured_llm
        
        extraction = chain.invoke({"intent": state["user_intent"]})
        updates["parsed_constraints"] = extraction.model_dump()
        print(f"Extracted constraints: {updates['parsed_constraints']}")

    # Phase 2: Build itinerary if inventory and preferences are present
    elif state.get("inferred_preferences") and state.get("discovered_inventory") and not state.get("proposed_itinerary"):
        print("Building itinerary based on preferences and inventory...")
        
        inventory_str = str(state["discovered_inventory"])
        prefs_str = str(state["inferred_preferences"].model_dump())
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert dining concierge. Based on the user's preferences ({prefs}) and available inventory ({inventory}), propose the single best dining itinerary. Respond with a JSON object containing 'restaurant_id', 'name', 'match_reason', and 'time'."),
            ("human", "Build my itinerary.")
        ])
        
        # Simple JSON extraction for the itinerary
        # In a real production system, we'd use a Pydantic model for the itinerary as well.
        class ItineraryItem(BaseModel):
            restaurant_id: str
            name: str
            match_reason: str
            time: str
            
        structured_builder = llm.with_structured_output(ItineraryItem)
        builder_chain = prompt | structured_builder
        
        best_match = builder_chain.invoke({
            "prefs": prefs_str,
            "inventory": inventory_str
        })
        
        updates["proposed_itinerary"] = [best_match.model_dump()]
        print(f"Proposed Itinerary: {updates['proposed_itinerary']}")

    return updates
