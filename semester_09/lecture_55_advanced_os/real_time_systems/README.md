# Real-Time Systems

1. **Name of Algorithm**  
   Real-Time Systems

2. **What problem does it solve? (1 sentence)**  
   Processes tasks and responds to events within strict timing constraints, ensuring predictable and deterministic behavior for time-critical applications.

3. **Intuition (plain-language explanation)**  
   Like a traffic light controller: real-time systems are like traffic light controllers that must respond within strict time limits - if a car approaches (event), the system must change the light (response) within a guaranteed time (deadline) - missing the deadline (like a light not changing) can have serious consequences (accidents) - the system must be predictable and always meet timing requirements, unlike regular systems that prioritize average performance.

4. **Inputs & Outputs**  
   - Input: Real-time events, tasks with deadlines, timing constraints, sensor data, control signals.  
   - Output: Timely responses, deterministic behavior, guaranteed deadlines, real-time control.

5. **Step-by-step description (5–10 lines max)**  
1. Define requirements: specify timing constraints and deadlines for tasks.
2. Choose scheduler: select real-time scheduler (rate monotonic, earliest deadline first).
3. Analyze schedulability: verify all tasks can meet deadlines (schedulability analysis).
4. Prioritize: assign priorities based on deadlines (shorter deadline = higher priority).
5. Schedule: schedule tasks to meet all deadlines.
6. Monitor: continuously monitor task execution and timing.
7. Handle interrupts: process real-time interrupts with minimal latency.
8. Guarantee: ensure all tasks complete before deadlines.
9. Optimize: optimize for predictability over average performance.
10. Test: thoroughly test timing behavior under various conditions.

6. **Tiny example (hand-simulated)**  
   Real-time system: flight control → task: update control surfaces every 10ms (deadline) → scheduler: rate monotonic → priority: highest → guarantee: always completes within 8ms → interrupt: sensor reading → process within 1ms → deterministic: predictable timing → safety: critical system → real-time guarantees met.

7. **Time & Space Complexity**  
   - Time: O(n log n) for scheduling where n is number of tasks, O(1) for interrupt handling.  
   - Space: O(n) where n is number of tasks (task control blocks and scheduling data).

8. **Strengths**  
- Predictability: guarantees timing behavior and deadline compliance.
- Safety: critical for safety-critical applications (avionics, medical devices).
- Determinism: provides deterministic and repeatable behavior.

9. **Weaknesses / limitations**  
- Complexity: real-time scheduling and analysis is complex.
- Resource constraints: requires careful resource management.
- Flexibility: less flexible than general-purpose systems.

10. **Compare with alternatives**  
    Alternatives: General-Purpose OS, Soft Real-Time Systems, Event-Driven Systems, Time-Triggered Systems

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
