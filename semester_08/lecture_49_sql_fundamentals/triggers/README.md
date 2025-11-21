# Database Triggers

Name of Algorithm  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Database Triggers Flowchart:

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
Database Triggers Step-by-Step Execution:

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
- [Python Implementation](/code/semester_08/lecture_49_sql_fundamentals/triggers/algorithm.py)
- [Java Implementation](/code/semester_08/lecture_49_sql_fundamentals/triggers/Algorithm.java)
- [Python Tests](/code/semester_08/lecture_49_sql_fundamentals/triggers/test_algorithm.py)


   Database Triggers

What problem does it solve? (1 sentence)  
   Automatically executes SQL code in response to specific database events (INSERT, UPDATE, DELETE), enabling automatic data validation, auditing, and maintaining referential integrity.

Intuition (plain-language explanation)  
   Like automatic event handlers: triggers are like 'if this happens, then do that' rules - when you insert/update/delete data (event), the trigger automatically fires and executes predefined SQL code (action), like automatically updating a timestamp, logging changes, or validating data.

Inputs & Outputs  
   - Input: Trigger definition, event type (INSERT/UPDATE/DELETE), table, trigger code.  
   - Output: Automatic actions, data validation, audit logs, maintained data integrity.

Step-by-step description (5–10 lines max)  
Define trigger: specify trigger name, event (BEFORE/AFTER INSERT/UPDATE/DELETE), and table.
Write trigger code: create SQL code to execute when trigger fires.
Create trigger: register trigger with database.
Monitor events: database monitors specified table for trigger events.
Fire trigger: when event occurs, database automatically executes trigger code.
Execute actions: trigger performs defined actions (validate, log, update, etc.).
Commit/rollback: trigger can allow or prevent the triggering operation.
Maintain: update trigger logic as requirements change.

Tiny example (hand-simulated)  
   Table: orders → trigger: AFTER INSERT → code: UPDATE users SET total_orders = total_orders + 1 WHERE id = NEW.user_id → when order inserted → trigger fires automatically → updates user's order count → no application code needed → automatic data consistency.

Time & Space Complexity  
   - Time: O(1) for trigger invocation, execution time depends on trigger code complexity.  
   - Space: O(t) where t is trigger code size (stored on database server).

Strengths  
- Automatic: executes automatically without application intervention.
- Data integrity: enforces business rules at database level.
- Auditing: automatically logs changes for compliance and tracking.

Weaknesses / limitations  
- Hidden logic: triggers can make database behavior non-obvious.
- Performance: can slow down INSERT/UPDATE/DELETE operations.
- Debugging: difficult to trace and debug trigger execution.

Compare with alternatives  
    Alternatives: Application Logic, Constraints, Stored Procedures, Event Handlers

30-second explanation (your own words)  
    Automatically executes SQL code in response to specific database events (INSERT, UPDATE, DELETE), enabling automatic data validation, auditing, and maintaining referential integrity.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
