# Microkernel Architecture

1. **Name of Algorithm**  
   Microkernel Architecture

2. **What problem does it solve? (1 sentence)**  
   Minimizes kernel to essential functions (IPC, scheduling, memory management), moving most OS services to user-space servers, improving modularity, security, and maintainability.

3. **Intuition (plain-language explanation)**  
   Like a minimal government with specialized agencies: microkernel architecture is like a minimal central government (kernel) that only handles essential functions (like basic laws and coordination), while specialized agencies (user-space servers) handle specific services (like file systems, network stacks) - if an agency (server) crashes, it doesn't bring down the whole government (system), and you can update or replace agencies (servers) without changing the core government (kernel).

4. **Inputs & Outputs**  
   - Input: System calls, IPC messages, hardware interrupts, resource requests.  
   - Output: Minimal kernel, user-space servers, modular OS services, improved reliability.

5. **Step-by-step description (5–10 lines max)**  
1. Minimize kernel: implement only essential functions in kernel (IPC, scheduling, memory).
2. Create servers: implement OS services as user-space servers (file system, network, device drivers).
3. IPC mechanism: provide inter-process communication for kernel-server and server-server communication.
4. Message passing: use message passing for all communication (no shared memory in kernel).
5. Isolate servers: run servers in separate address spaces for isolation.
6. Handle failures: if server crashes, only that service fails (system continues).
7. Update servers: update or replace servers without kernel changes.
8. Secure: kernel enforces security and isolation between servers.
9. Optimize: optimize IPC performance for efficient communication.

6. **Tiny example (hand-simulated)**  
   Microkernel: minimal kernel (IPC, scheduling, memory) → user-space servers: file system server, network server, device driver servers → IPC: kernel and servers communicate via messages → isolation: file server crash doesn't crash system → update: replace file server without kernel changes → modularity: add new services as new servers → microkernel architecture.

7. **Time & Space Complexity**  
   - Time: O(1) for kernel operations, O(m) for IPC where m is message size (may be slower than monolithic).  
   - Space: O(k + s) where k is kernel size, s is total server size (smaller kernel, distributed services).

8. **Strengths**  
- Modularity: services can be updated or replaced independently.
- Reliability: server failures don't crash entire system.
- Security: better isolation between OS components.

9. **Weaknesses / limitations**  
- Performance: IPC overhead may be higher than monolithic kernel.
- Complexity: managing multiple servers adds complexity.
- Coordination: requires careful coordination between servers.

10. **Compare with alternatives**  
    Alternatives: Monolithic Kernel, Hybrid Kernel, Exokernel, Modular Kernel

11. **30-second explanation (your own words)**  
    Minimizes kernel to essential functions (IPC, scheduling, memory management), moving most OS services to user-space servers, improving modularity, security, and maintainability.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
