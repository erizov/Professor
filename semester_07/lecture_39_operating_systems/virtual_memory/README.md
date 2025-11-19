# Virtual Memory

1. **Name of Algorithm**  
   Virtual Memory

2. **What problem does it solve? (1 sentence)**  
   Provides illusion of larger memory than physically available by using disk storage as extension of RAM, enabling programs to use more memory than physically installed and improving memory utilization through paging.

3. **Intuition (plain-language explanation)**  
   Like having a magic filing cabinet: programs think they have huge memory (virtual addresses), but the OS secretly stores some of it on disk (like a filing cabinet) and only keeps frequently used parts in RAM (desk) - when program needs something from disk, OS swaps it in (brings file to desk).

4. **Inputs & Outputs**  
   - Input: Virtual addresses from processes, physical memory (RAM), disk storage (swap space), page size, page table entries.  
   - Output: Virtual-to-physical address translation, page tables, swapped pages on disk, memory protection.

5. **Step-by-step description (5–10 lines max)**  
1. Divide memory into pages: split virtual and physical memory into fixed-size pages (typically 4KB).
2. Create page tables: maintain mapping from virtual pages to physical pages (or disk) for each process.
3. Translate addresses: when process accesses virtual address, use page table to find physical address.
4. Check page presence: if page in RAM (page present), access directly.
5. Handle page fault: if page not in RAM (page fault), load page from disk to RAM.
6. Update page table: mark page as present, update physical address mapping.
7. Resume execution: retry the memory access that caused page fault.
8. Evict pages: when RAM full, select page to evict (LRU, FIFO) and write to disk if modified.
9. Update page table: mark evicted page as not present, record disk location.

6. **Tiny example (hand-simulated)**  
   Process accesses virtual address 0x1000 → page table lookup: virtual page 1 → not in RAM (page fault) → OS selects page to evict (LRU) → writes evicted page to disk → loads page 1 from disk to RAM at physical address 0x5000 → updates page table: virtual page 1 → physical page 0x5000 → retry access → success.

7. **Time & Space Complexity**  
   - Time: O(1) for address translation (with TLB cache), O(D) for page fault handling where D is disk access time (typically 5-10ms, much slower than RAM).  
   - Space: O(P) for page tables where P is number of virtual pages per process, O(S) for swap space on disk where S is total virtual memory size.

8. **Strengths**  
- Larger address space: enables programs to use more memory than physically available.
- Memory protection: isolates processes by giving each its own virtual address space.
- Efficient utilization: allows more processes to run simultaneously.

9. **Weaknesses / limitations**  
- Performance: page faults are slow (disk access much slower than RAM).
- Overhead: page tables consume memory and require management.
- Complexity: requires hardware support (MMU) and careful algorithm design.

10. **Compare with alternatives**  
    Alternatives: Physical Memory Only, Segmentation, Hybrid Paging-Segmentation, Memory Overcommit

11. **30-second explanation (your own words)**  
    Provides illusion of larger memory than physically available by using disk storage as extension of RAM, enabling programs to use more memory and improving utilization through paging and virtual-to-physical address translation.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
