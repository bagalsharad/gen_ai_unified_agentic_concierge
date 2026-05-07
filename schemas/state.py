from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator
from schemas.models import UserPreferences

class ConciergeState(TypedDict):
    session_id: str
    user_id: str
    user_intent: str
    parsed_constraints: Dict[str, Any]
    discovered_inventory: List[Dict[str, Any]]
    inferred_preferences: Optional[UserPreferences]
    proposed_itinerary: List[Dict[str, Any]]
    booking_status: str
    reflection_feedback: Annotated[List[str], operator.add]
    final_recommendations: List[Dict[str, Any]]
    audit_log: Annotated[List[Dict[str, Any]], operator.add]
    event_trace: Annotated[List[str], operator.add]
    conversation_history: Annotated[List[Dict[str, str]], operator.add]
    confidence_score: float
    iteration: int
