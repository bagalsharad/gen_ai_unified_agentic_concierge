from schemas.state import ConciergeState
import random

def discovery_node(state: ConciergeState) -> dict:
    """
    Discovery Agent: Searches Resy and Tock for dining inventory based on constraints.
    In a real implementation, this would invoke the gRPC connectors.
    Here we simulate inventory retrieval based on the constraints.
    """
    print("--- Discovery Agent: Fetching Inventory ---")
    
    constraints = state.get("parsed_constraints", {})
    cuisine = constraints.get("cuisine", "any cuisine")
    location = constraints.get("location", "the area")
    
    print(f"Searching for {cuisine} options in {location}...")
    
    # Mock inventory response
    inventory = []
    
    if cuisine and "japanese" in cuisine.lower():
        inventory.extend([
            {"platform": "resy", "restaurant_id": "j1", "name": "Sushi Nakazawa", "tags": ["japanese", "omakase", "seafood"], "available_slots": ["19:00", "20:00", "21:30"], "price_tier": "$$$$"},
            {"platform": "tock", "restaurant_id": "j2", "name": "Masa", "tags": ["japanese", "sushi", "exclusive", "seafood"], "available_slots": ["18:30"], "price_tier": "$$$$"}
        ])
    elif cuisine and "italian" in cuisine.lower():
        inventory.extend([
            {"platform": "resy", "restaurant_id": "i1", "name": "Carbone", "tags": ["italian", "pasta"], "available_slots": ["21:00", "22:00"], "price_tier": "$$$"},
            {"platform": "resy", "restaurant_id": "i2", "name": "Lilia", "tags": ["italian", "pasta", "brooklyn"], "available_slots": ["17:30", "18:00"], "price_tier": "$$$"}
        ])
    else:
        # Fallback generic inventory
        inventory.extend([
            {"platform": "resy", "restaurant_id": "g1", "name": "Le Bernardin", "tags": ["french", "seafood"], "available_slots": ["19:00", "20:30"], "price_tier": "$$$$"},
            {"platform": "tock", "restaurant_id": "g2", "name": "Eleven Madison Park", "tags": ["vegan", "tasting menu"], "available_slots": ["18:00", "19:30"], "price_tier": "$$$$"}
        ])
        
    return {"discovered_inventory": inventory}
