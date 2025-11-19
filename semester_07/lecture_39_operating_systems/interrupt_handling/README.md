# Interrupt Handling

1. **Name of Algorithm**  
   Interrupt Handling

2. **What problem does it solve? (1 sentence)**  
Manages asynchronous events (hardware interrupts, software interrupts, exceptions) that require immediate CPU attention, enabling responsive system behavior and efficient I/O operations.

3. **Intuition (plain-language explanation)**  
   Like a doorbell interrupting your work: when hardware needs attention (keyboard pressed, disk finished reading), it sends an interrupt signal to CPU - CPU stops current work, handles the interrupt (processes keyboard input), then returns to what it was doing.

4. **Inputs & Outputs**  
   - Input: Interrupt signals from hardware devices, software interrupts (system calls), exceptions (errors, page faults), interrupt service routines (ISRs).  
   - Output: Handled interrupts, updated system state, resumed process execution, I/O operations completed.

5. **Step-by-step description (5–10 lines max)**  
1. Interrupt occurs: hardware device or software generates interrupt signal to CPU.
2. Save context: CPU saves current process state (registers, program counter) to stack.
3. Identify interrupt: CPU determines interrupt type and source (keyboard, timer, disk, etc.).
4. Lookup ISR: use interrupt vector table to find appropriate interrupt service routine (ISR).
5. Disable interrupts: temporarily disable interrupts to prevent nested interrupts during handling.
6. Execute ISR: run interrupt service routine to handle the interrupt (read keyboard buffer, update timer, etc.).
7. Re-enable interrupts: restore interrupt enable flag to allow future interrupts.
8. Restore context: restore saved process state from stack.
9. Resume execution: return to interrupted process or switch to higher-priority process.

6. **Tiny example (hand-simulated)**  
   Keyboard interrupt: user presses key → keyboard controller sends interrupt → CPU saves current process state → looks up keyboard ISR → executes ISR: reads key code from keyboard buffer → updates input queue → restores process state → resumes interrupted process → key appears in application.

7. **Time & Space Complexity**  
   - Time: O(1) for interrupt identification and ISR lookup, O(I) for ISR execution where I is ISR complexity (typically microseconds).  
   - Space: O(P) for interrupt stack per process, O(V) for interrupt vector table where V is number of interrupt types.

8. **Strengths**  
- Responsive: enables immediate handling of time-sensitive events.
- Efficient: allows CPU to continue other work while waiting for I/O.
- Flexible: supports various interrupt types and priorities.

9. **Weaknesses / limitations**  
- Overhead: context switching and ISR execution add overhead.
- Complexity: requires careful design to handle nested interrupts and race conditions.
- Latency: interrupt handling may delay time-critical operations.

10. **Compare with alternatives**  
    Alternatives: Polling, Event-driven Programming, Cooperative Multitasking, Synchronous I/O

11. **30-second explanation (your own words)**  
Manages asynchronous events that require immediate CPU attention, enabling responsive system behavior and efficient I/O operations through interrupt service routines and context switching.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
