# Unified Agentic Concierge Architecture

## 1. High-Level Diagram

```mermaid
graph TD
    User([User Mobile / Web]) -->|HTTP/REST| API_Gateway[FastAPI Gateway]
    
    API_Gateway -->|Invoke Graph| LangGraph_Orchestrator[LangGraph Master Orchestrator]
    
    subgraph Multi-Agent Orchestration Layer
        LangGraph_Orchestrator --> ConciergeAgent[Concierge Master Agent]
        ConciergeAgent --> DiscoveryAgent[Discovery Agent]
        ConciergeAgent --> PreferenceAgent[Preference Agent]
        ConciergeAgent --> ReflectionNode[Reflection & Self-Correction]
        ReflectionNode -->|Retry| ConciergeAgent
        ReflectionNode --> BookingAgent[Booking Agent]
    end
    
    subgraph Semantic Knowledge Layer
        PreferenceAgent -->|Cypher Queries| Neo4j[(Neo4j Knowledge Graph)]
    end
    
    subgraph Connector Services (gRPC)
        DiscoveryAgent --> ResyConn[Resy Connector]
        DiscoveryAgent --> TockConn[Tock Connector]
        BookingAgent --> ResyConn
        BookingAgent --> TockConn
        PreferenceAgent --> RooamConn[Rooam Connector]
    end
    
    subgraph Event-Driven Infrastructure
        Kafka[(Apache Kafka)] -->|inventory_updates| DiscoveryAgent
        Kafka -->|booking_confirmations| Neo4j
    end
    
    ResyConn --> ExtResy[Resy API]
    TockConn --> ExtTock[Tock API]
    RooamConn --> ExtRooam[Rooam API]
```

## 2. Core Components

### User Interaction Layer
- **FastAPI API Gateway:** Exposes conversational endpoints for clients. Manages auth (JWT) and passes state down to the orchestrator.

### Orchestration Layer (LangGraph)
- **Concierge Master Agent:** The core router that interprets user intent and delegates to sub-agents.
- **Discovery Agent:** Interfaces with Resy and Tock connectors to retrieve live inventory.
- **Preference Agent:** Reads user transaction history and preferences from Neo4j to personalize recommendations.
- **Reflection Node:** Validates proposed itineraries against user restrictions (allergies, budget, time). If it fails, it pushes back to the Concierge Agent.
- **Booking Agent:** Performs the final API calls to secure reservations and updates the DB via Kafka events.

### Semantic Knowledge Layer (Neo4j)
- Instead of LlamaIndex + Vector DB, **Neo4j** acts as the primary knowledge graph, modeling the relationships between `User`, `Restaurant`, `Cuisine`, `DietaryRestriction`, and `Transaction` (from Rooam). This allows graph-based recommendations (e.g., "Users who like Omakase and spend $$$ often go to Restaurant Y").

### Connector Microservices
- Isolated gRPC Python services (`Resy`, `Tock`, `Rooam`). They implement circuit breakers, rate limiting, and standardizing data back to the core.

### Event-Driven Backbone (Kafka)
- Decouples long-running operations. Connectors can push real-time availability updates to Kafka, which updates cache or prompts the Discovery Agent.
