from schemas.state import ConciergeState
from pydantic import BaseModel, Field
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.1)

class ReflectionAudit(BaseModel):
    feedback: List[str] = Field(..., description="List of critique points or warnings about the itinerary.")
    confidence_score: float = Field(..., description="Score from 0.0 to 1.0 indicating confidence in the recommendation.")
    is_safe: bool = Field(..., description="True if it violates no strict rules (e.g. allergies).")

def reflection_node(state: ConciergeState) -> dict:
    """
    Reflection Node: Audits proposed itinerary against preferences/restrictions.
    """
    print("--- Reflection Agent: Auditing Itinerary ---")
    
    proposed = state.get("proposed_itinerary", [])
    prefs = state.get("inferred_preferences")
    constraints = state.get("parsed_constraints")
    
    if not proposed:
        return {"reflection_feedback": ["No itinerary proposed to evaluate."], "confidence_score": 0.0}
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert dining auditor. Review the proposed itinerary against the user's inferred preferences and explicit constraints. Check for allergies, dietary restrictions, and budget mismatches. Output your critique, a confidence score (0.0 to 1.0), and a boolean indicating if it's strictly safe to book."),
        ("human", "Preferences: {prefs}\nConstraints: {constraints}\nProposed Itinerary: {proposed}")
    ])
    
    structured_auditor = llm.with_structured_output(ReflectionAudit)
    audit_chain = prompt | structured_auditor
    
    audit_result = audit_chain.invoke({
        "prefs": prefs.model_dump() if prefs else "None",
        "constraints": constraints,
        "proposed": proposed
    })
    
    print(f"Reflection Audit: {audit_result.model_dump()}")
    
    # If safe and high confidence, promote to final recommendations
    final_recs = []
    if audit_result.is_safe and audit_result.confidence_score >= 0.8:
        final_recs = proposed
        
    return {
        "reflection_feedback": audit_result.feedback,
        "confidence_score": audit_result.confidence_score,
        "final_recommendations": final_recs
    }
