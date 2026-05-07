import os
from neo4j import GraphDatabase
from schemas.state import ConciergeState
from schemas.models import UserPreferences

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def get_user_preferences_from_neo4j(user_id: str) -> UserPreferences:
    """
    Executes Cypher queries against Neo4j to build the UserPreferences object.
    Falls back to mock data if connection fails.
    """
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity()
        
        # Example queries assuming a schema where User has relations PREFERS, HAS_ALLERGY
        query = """
        MATCH (u:User {id: $user_id})
        OPTIONAL MATCH (u)-[:PREFERS]->(c:Cuisine)
        OPTIONAL MATCH (u)-[:HAS_ALLERGY]->(a:Ingredient)
        RETURN collect(DISTINCT c.name) as cuisines, collect(DISTINCT a.name) as allergies
        """
        
        with driver.session() as session:
            result = session.run(query, user_id=user_id)
            record = result.single()
            
            if record:
                return UserPreferences(
                    favorite_cuisines=record["cuisines"],
                    allergies=record["allergies"],
                    dietary_restrictions=[],
                    disliked_ingredients=[],
                    average_spend=250.0 # Mocked for now, normally computed from Rooam transactions
                )
                
    except Exception as e:
        print(f"Neo4j connection or query failed: {e}. Falling back to mock preferences.")
        
    # Fallback mock preferences
    return UserPreferences(
        favorite_cuisines=["Japanese", "Italian"],
        allergies=["shellfish"],
        average_spend=250.0
    )

def preference_node(state: ConciergeState) -> dict:
    """
    Preference Agent: Queries Neo4j for user history and infers preferences.
    """
    print("--- Preference Agent: Querying Neo4j Semantic Graph ---")
    
    user_id = state.get("user_id", "default_user")
    prefs = get_user_preferences_from_neo4j(user_id)
    
    print(f"Retrieved Preferences: {prefs.model_dump()}")
    
    return {"inferred_preferences": prefs}
