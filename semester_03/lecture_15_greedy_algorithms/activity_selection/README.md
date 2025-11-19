# Activity Selection

1. **Name of Algorithm**  
   Activity Selection

2. **What problem does it solve? (1 sentence)**  
   Selects the maximum number of non-overlapping activities from a set, where each activity has a start and finish time.

3. **Intuition (plain-language explanation)**  
   Greedily choose the activity that finishes earliest: it leaves the most time for remaining activities, maximizing total count.

4. **Inputs & Outputs**  
   - Input: List of activities, each with start_time and finish_time.  
   - Output: Maximum-size set of non-overlapping activities.

5. **Step-by-step description (5–10 lines max)**  
1. Sort activities by finish_time (ascending).
2. Initialize selected = [first activity].
3. For each remaining activity: if its start_time >= finish_time of last selected, add it to selected.
4. Return selected set.

6. **Tiny example (hand-simulated)**  
   Activities: (1,4), (3,5), (0,6), (5,7), (8,9). Sorted: (1,4), (3,5), (0,6), (5,7), (8,9). Selected: (1,4), (5,7), (8,9) = 3 activities.

7. **Time & Space Complexity**  
   - Time: O(n log n) for sorting, O(n) for selection = O(n log n) total.  
   - Space: O(n) for storing activities and result.

8. **Strengths**  
- Simple greedy approach with optimal solution.
- Efficient O(n log n) time complexity.

9. **Weaknesses / limitations**  
- Assumes activities are sorted (or requires sorting).
- Only maximizes count, not total duration or value.

10. **Compare with alternatives**  
    Alternatives: Weighted Activity Selection (DP), Interval Scheduling (variants), Greedy with different criteria

11. **30-second explanation (your own words)**  
    Greedily selects activities that finish earliest, leaving maximum time for future selections and guaranteeing optimal count.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
