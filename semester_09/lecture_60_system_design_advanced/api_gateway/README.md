# API Gateway

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
API Gateway Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```

### Step-by-Step Execution

```
API Gateway Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```

### Interactive Flowchart (Mermaid)

```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.

- [Python Implementation](/code/semester_09/lecture_60_system_design_advanced/api_gateway/algorithm.py)
- [Java Implementation](/code/semester_09/lecture_60_system_design_advanced/api_gateway/Algorithm.java)
- [Python Tests](/code/semester_09/lecture_60_system_design_advanced/api_gateway/test_algorithm.py)

   API Gateway

What problem does it solve? (1 sentence)  
   Provides a single entry point for client requests to multiple backend services, handling routing, authentication, rate limiting, and other cross-cutting concerns, simplifying client interactions and service management.

Intuition (plain-language explanation)  
   Like a receptionist: API Gateway is like a receptionist at a building - instead of clients going directly to each office (service), they go to the receptionist (gateway) who routes them to the right office, checks their ID (authentication), and handles common tasks (rate limiting, logging) - this makes it easier for clients (they only need to know one address) and easier to manage the building (centralized control).

Inputs & Outputs  

  - Input: Client requests, routing rules, authentication tokens, rate limit policies, service endpoints.  
  - Output: Routed requests, authenticated sessions, rate-limited traffic, aggregated responses, service calls.

Step-by-step description (5–10 lines max)  
Receive request: receive client request at gateway.
Authenticate: authenticate client (validate token, check credentials).
Authorize: authorize request (check permissions, policies).
Rate limit: check and enforce rate limits.
Route: route request to appropriate backend service based on URL/path.
Transform: optionally transform request (protocol conversion, data format).
Forward: forward request to backend service.
Aggregate: optionally aggregate responses from multiple services.
Transform response: transform response if needed.
Return: return response to client.

Tiny example (hand-simulated)  
   API Gateway: client request: GET /api/users/123 → gateway: authenticate token → authorize: check permissions → rate limit: check quota → route: forward to user-service → service: returns user data → gateway: transform response → return: JSON response to client → API Gateway operational.

Time & Space Complexity  

  - Time: O(1) for routing and basic operations, O(n) for aggregation where n is number of services.  
  - Space: O(r + c) where r is routing rules, c is cache size (request/response caching).

Strengths  

- Simplification: simplifies client interactions with multiple services.
- Centralization: centralizes cross-cutting concerns (auth, rate limiting).
- Flexibility: enables service composition and aggregation.

Weaknesses / limitations  

- Single point of failure: gateway failure affects all services.
- Latency: adds latency to requests (extra hop).
- Complexity: gateway can become complex with many features.

Compare with alternatives  
    Alternatives: Direct Service Access, Service Mesh, Load Balancer, Reverse Proxy

30-second explanation (your own words)  
    Provides a single entry point for client requests to multiple backend services, handling routing, authentication, rate limiting, and other cross-cutting concerns, simplifying client interactions and service management.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
