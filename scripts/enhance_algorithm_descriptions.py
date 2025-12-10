#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhance algorithm descriptions with learning aids:
- Quick Summary
- In One Sentence
- Key Insight
- Memory Tip
- Try It Yourself
- Practice Exercise
- Check Your Understanding
- Enhanced Common Mistakes
- Related Algorithms
"""

import sys
import json
import re
import ast
from pathlib import Path
from typing import Dict, Optional, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def generate_one_sentence(algorithm_name: str, category: str, description: str) -> str:
    """Generate 'In One Sentence' description."""
    readable_name = algorithm_name.replace("_", " ").title()
    
    # Category-specific templates
    templates = {
        'Sorting': f"{readable_name}: Repeatedly compares and rearranges elements until the list is sorted, like organizing items in order.",
        'Graph Algorithms': f"{readable_name}: Explores or processes graph structures systematically to find paths, connections, or optimal solutions.",
        'Dynamic Programming': f"{readable_name}: Solves complex problems by breaking them into smaller subproblems and storing results to avoid redundant calculations.",
        'Tree Algorithms': f"{readable_name}: Processes tree structures by visiting nodes in a specific order to perform operations efficiently.",
        'Search Algorithms': f"{readable_name}: Finds elements in data structures by systematically checking locations, similar to looking up information in an organized system."
    }
    
    if category in templates:
        return templates[category]
    
    # Generic template
    return f"{readable_name}: {description.split('.')[0] if description else 'Processes data systematically to achieve a specific goal'}."


def generate_key_insight(algorithm_name: str, category: str, analysis: Dict) -> str:
    """Generate 'Key Insight' explaining the core concept."""
    name_lower = algorithm_name.lower()
    key_ops = analysis.get('key_operations', [])
    
    insights = {
        'bubble_sort': "The largest element 'bubbles up' to the end in each pass, so we can reduce the comparison range each time.",
        'quick_sort': "Divide and conquer: pick a pivot, partition around it, then recursively sort the partitions.",
        'merge_sort': "Divide the array in half, sort each half, then merge the sorted halves together.",
        'binary_search': "Always check the middle element - if it's not what we want, eliminate half the search space.",
        'dijkstra': "Greedy approach: always process the closest unvisited node first, ensuring shortest paths are found.",
        'bfs': "Explore level by level - visit all neighbors before moving to the next level, like ripples in water.",
        'dfs': "Go deep first - explore as far as possible along each branch before backtracking.",
        'fibonacci': "Each number is the sum of the two previous numbers - we can compute this efficiently by storing previous results.",
        'knapsack': "For each item, decide whether to include it or not - store the best value for each weight capacity."
    }
    
    # Check for specific algorithm
    for key, insight in insights.items():
        if key in name_lower:
            return insight
    
    # Category-based insights
    if category == 'Sorting':
        return "Compare elements and rearrange them until everything is in the correct order."
    elif category == 'Graph Algorithms':
        return "Systematically explore graph structures to find optimal paths or connections."
    elif category == 'Dynamic Programming':
        return "Break complex problems into smaller subproblems and reuse solutions to avoid redundant work."
    elif category == 'Search Algorithms':
        return "Efficiently locate elements by eliminating portions of the search space."
    
    return "The algorithm works by systematically processing data according to a specific strategy."


def generate_memory_tip(algorithm_name: str, category: str) -> str:
    """Generate memory aid (mnemonic or visual association)."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace("_", " ").title()
    
    tips = {
        'bubble_sort': "**BUBBLE** = Bring Up Bigger, Leave Elements. Think of bubbles rising in water - larger elements float to the top!",
        'quick_sort': "**QUICK** = Quickly Use Index, Compare & Keep. Like organizing a deck of cards by picking a card and sorting others around it.",
        'merge_sort': "**MERGE** = Make Equal, Recursively Group Elements. Like merging two sorted piles of papers into one.",
        'binary_search': "**BINARY** = Begin In Middle, Always Narrow Your search. Like finding a word in a dictionary - always check the middle!",
        'dijkstra': "**DIJKSTRA** = Distance Increases, Just Keep Shortest Track Record Always. Always pick the closest unvisited node first.",
        'bfs': "**BFS** = Breadth First Search. Like exploring a maze room by room, level by level - visit all neighbors first!",
        'dfs': "**DFS** = Depth First Search. Like exploring a maze - go as deep as possible down one path before trying another.",
        'fibonacci': "**FIBONACCI** = Find In Both, Add Next, Continue Iteratively. Each number is the sum of the two before it!",
        'knapsack': "**KNAPSACK** = Keep Noting All Possible Solutions, Always Check Knapsack. For each item, decide: take it or leave it?"
    }
    
    # Check for specific algorithm
    for key, tip in tips.items():
        if key in name_lower:
            return tip
    
    # Category-based tips
    if category == 'Sorting':
        return f"**{readable_name.upper()}** = Think of organizing items - compare and rearrange until everything is in order!"
    elif category == 'Graph Algorithms':
        return f"**{readable_name.upper()}** = Like exploring a map - visit nodes systematically to find what you need!"
    elif category == 'Dynamic Programming':
        return f"**{readable_name.upper()}** = Remember: solve small problems first, then combine solutions - no redundant work!"
    
    return f"**{readable_name.upper()}** = Remember the key steps: {', '.join(['step 1', 'step 2', 'step 3'])}"


def generate_try_it_example(algorithm_name: str, category: str) -> str:
    """Generate 'Try It Yourself' section with walkthrough."""
    name_lower = algorithm_name.lower()
    
    examples = {
        'bubble_sort': """**Try sorting this by hand:**
```
Input: [5, 2, 8, 1, 9]

Pass 1:
  Compare 5 and 2 → 5 > 2, swap → [2, 5, 8, 1, 9]
  Compare 5 and 8 → 5 < 8, no swap → [2, 5, 8, 1, 9]
  Compare 8 and 1 → 8 > 1, swap → [2, 5, 1, 8, 9]
  Compare 8 and 9 → 8 < 9, no swap → [2, 5, 1, 8, 9]
  Largest element (9) is now at the end!

Pass 2:
  Compare 2 and 5 → 2 < 5, no swap → [2, 5, 1, 8, 9]
  Compare 5 and 1 → 5 > 1, swap → [2, 1, 5, 8, 9]
  (No need to check 8 and 9 - already sorted)

Continue until sorted: [1, 2, 5, 8, 9]
```""",
        'binary_search': """**Try finding 7 in this sorted array:**
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle element (index 3, value 5)
  5 < 7, so search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, so search left half: [7]

Step 3: Found! Element 7 is at index 3
```""",
        'fibonacci': """**Try computing Fibonacci(5) by hand:**
```
F(0) = 0
F(1) = 1
F(2) = F(1) + F(0) = 1 + 0 = 1
F(3) = F(2) + F(1) = 1 + 1 = 2
F(4) = F(3) + F(2) = 2 + 1 = 3
F(5) = F(4) + F(3) = 3 + 2 = 5

Answer: 5
```"""
    }
    
    if name_lower in examples:
        return examples[name_lower]
    
    # Generic example
    return f"""**Try this example:**
```
Input: [example data]
Step 1: [first operation]
Step 2: [second operation]
...
Output: [result]
```"""


def generate_practice_exercise(algorithm_name: str, category: str) -> str:
    """Generate practice exercise."""
    name_lower = algorithm_name.lower()
    
    exercises = {
        'bubble_sort': """**Exercise 1 (Easy):**
Sort this list by hand: [64, 34, 25, 12, 22, 11, 90]
Show each pass and count how many swaps you make.

**Exercise 2 (Medium):**
Write a function to sort a list of student names alphabetically using bubble sort.

**Exercise 3 (Hard):**
Optimize bubble sort to stop early if the list is already sorted. How does this improve performance?""",
        'binary_search': """**Exercise 1 (Easy):**
Find the number 42 in this sorted array: [10, 20, 30, 40, 50, 60, 70]
Show each step of your search.

**Exercise 2 (Medium):**
Implement binary search to find the first occurrence of a target value in a sorted array with duplicates.

**Exercise 3 (Hard):**
What happens if you try binary search on an unsorted array? Why doesn't it work?""",
        'fibonacci': """**Exercise 1 (Easy):**
Calculate the first 10 Fibonacci numbers by hand.

**Exercise 2 (Medium):**
Write a function to compute Fibonacci(n) using dynamic programming (store previous results).

**Exercise 3 (Hard):**
Compare the time complexity of recursive Fibonacci vs dynamic programming Fibonacci. Why is DP faster?"""
    }
    
    if name_lower in exercises:
        return exercises[name_lower]
    
    # Generic exercises
    return f"""**Exercise 1 (Easy):**
Trace through the algorithm with a small example (3-5 elements).

**Exercise 2 (Medium):**
Implement the algorithm in your preferred programming language.

**Exercise 3 (Hard):**
Optimize the algorithm or apply it to solve a real-world problem."""


def generate_check_understanding(algorithm_name: str, category: str, complexity: str) -> str:
    """Generate 'Check Your Understanding' Q&A."""
    name_lower = algorithm_name.lower()
    
    questions = {
        'bubble_sort': """**Q1:** How many passes are needed for n elements in the worst case?
**A:** At most n-1 passes (the last element is already in place after n-1 passes).

**Q2:** What is the best-case time complexity and when does it occur?
**A:** O(n) when the array is already sorted and we use early termination.

**Q3:** Why is bubble sort called "bubble" sort?
**A:** Because larger elements "bubble up" to the end of the array, like bubbles rising in water.

**Q4:** Is bubble sort stable?
**A:** Yes, it preserves the relative order of equal elements.""",
        'binary_search': """**Q1:** Why must the array be sorted for binary search?
**A:** Because we eliminate half the search space based on comparison - this only works if elements are ordered.

**Q2:** What is the time complexity of binary search?
**A:** O(log n) - we halve the search space each time.

**Q3:** What is the space complexity of iterative binary search?
**A:** O(1) - we only use a few variables, no extra space needed.

**Q4:** When would you use binary search instead of linear search?
**A:** When the array is sorted and you need to search multiple times - the O(log n) vs O(n) advantage is significant.""",
        'fibonacci': """**Q1:** What are the base cases for Fibonacci?
**A:** F(0) = 0 and F(1) = 1.

**Q2:** Why is recursive Fibonacci slow?
**A:** It recalculates the same values many times (exponential time complexity).

**Q3:** How does dynamic programming make Fibonacci faster?
**A:** By storing previously computed values, we avoid redundant calculations (linear time complexity).

**Q4:** What is the space complexity of DP Fibonacci?
**A:** O(n) if we store all values, or O(1) if we only keep the last two values."""
    }
    
    if name_lower in questions:
        return questions[name_lower]
    
    # Generic questions
    return f"""**Q1:** What problem does this algorithm solve?
**A:** [Answer based on algorithm purpose]

**Q2:** What is the time complexity?
**A:** {complexity}

**Q3:** When would you use this algorithm?
**A:** [Answer based on use cases]

**Q4:** What are the main steps of this algorithm?
**A:** [List 3-5 key steps]"""


def enhance_common_mistakes(mistakes: str) -> str:
    """Enhance common mistakes section with solutions."""
    if not mistakes or len(mistakes.strip()) < 50:
        return """## Common Mistakes

### ❌ Mistake 1: Not handling edge cases
**Problem:** Forgetting to check for empty input or single element.
**Solution:** Always add checks at the beginning:
```python
if not data or len(data) <= 1:
    return data
```

### ❌ Mistake 2: Off-by-one errors
**Problem:** Incorrect loop boundaries causing index out of range.
**Solution:** Carefully check your loop conditions and array bounds.

### ❌ Mistake 3: Not understanding complexity
**Problem:** Using the algorithm for large datasets when it's too slow.
**Solution:** Understand when O(n²) is acceptable (small data) vs when you need O(n log n).

### ❌ Mistake 4: Incorrect implementation
**Problem:** Logic errors in the core algorithm.
**Solution:** Trace through examples step-by-step, test with known inputs/outputs.

### 💡 How to Avoid
- Always test with edge cases (empty, single element, already sorted)
- Draw diagrams or trace through examples manually
- Start with a simple version, then optimize
- Use debugging tools to step through your code"""
    
    # Enhance existing mistakes
    enhanced = "## Common Mistakes\n\n"
    
    mistake_lines = [line.strip() for line in mistakes.split('\n') if line.strip() and line.strip().startswith('-')]
    
    for i, mistake in enumerate(mistake_lines[:4], 1):
        mistake_text = mistake.lstrip('- ').strip()
        enhanced += f"### ❌ Mistake {i}: {mistake_text}\n"
        enhanced += f"**Solution:** [How to fix this mistake]\n\n"
    
    enhanced += """### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing"""
    
    return enhanced


def find_related_algorithms(algorithm_name: str, category: str, all_algorithms: List[str]) -> List[str]:
    """Find related algorithms in the same category."""
    related = []
    name_lower = algorithm_name.lower()
    
    # Category-based relationships
    if category == 'Sorting':
        sorting_algs = [a for a in all_algorithms if any(x in a.lower() for x in ['sort', 'heap', 'merge', 'quick', 'insertion', 'selection'])]
        related = [a for a in sorting_algs if a != algorithm_name][:3]
    elif category == 'Graph Algorithms':
        graph_algs = [a for a in all_algorithms if any(x in a.lower() for x in ['bfs', 'dfs', 'dijkstra', 'bellman', 'floyd', 'graph'])]
        related = [a for a in graph_algs if a != algorithm_name][:3]
    elif category == 'Dynamic Programming':
        dp_algs = [a for a in all_algorithms if any(x in a.lower() for x in ['fibonacci', 'knapsack', 'edit', 'lcs', 'dynamic'])]
        related = [a for a in dp_algs if a != algorithm_name][:3]
    
    return related


def read_algorithm_files(algorithm_folder: Path) -> Dict[str, any]:
    """Read algorithm files."""
    files = {
        'readme': None,
        'algorithm_py': None,
        'metadata': None,
        'analysis': {}
    }
    
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        try:
            files['readme'] = readme_path.read_text(encoding='utf-8')
        except:
            pass
    
    algo_path = algorithm_folder / "algorithm.py"
    if algo_path.exists():
        try:
            files['algorithm_py'] = algo_path.read_text(encoding='utf-8')
        except:
            pass
    
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            files['metadata'] = json.loads(metadata_path.read_text(encoding='utf-8'))
        except:
            pass
    
    return files


def get_category(files: Dict) -> str:
    """Get algorithm category."""
    if files['metadata'] and files['metadata'].get('category'):
        return files['metadata']['category']
    return 'Algorithms'


def get_complexity(files: Dict) -> str:
    """Get complexity information."""
    if files['metadata']:
        if isinstance(files['metadata'].get('complexity'), dict):
            return files['metadata']['complexity'].get('time', 'O(n²)')
        elif isinstance(files['metadata'].get('time_complexity'), str):
            return files['metadata'].get('time_complexity', 'O(n²)')
    return 'O(n²)'


def enhance_md_file(filepath: Path, algorithm_name: str, files: Dict, all_algorithms: List[str], level: str, language: str) -> str:
    """Enhance existing MD file with new sections."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        content = ""
    
    category = get_category(files)
    complexity = get_complexity(files)
    
    # Extract description from existing content (skip flowchart/visualization text)
    description = ""
    if content:
        lines = content.split('\n')
        skip_patterns = ['flowchart', 'step-by-step', 'execution', 'start', 'init', '-->', '│', '┌', '└']
        for line in lines[:30]:
            line_lower = line.lower()
            # Skip flowchart, diagram, and visualization text
            if any(pattern in line_lower for pattern in skip_patterns):
                continue
            if line.strip() and not line.startswith('#') and len(line) > 30:
                # Make sure it's actual description, not code or special chars
                if not line.strip().startswith('```') and not line.strip().startswith('-') and '[' not in line:
                    description = line.strip()
                    break
    
    # Generate new sections
    one_sentence = generate_one_sentence(algorithm_name, category, description)
    key_insight = generate_key_insight(algorithm_name, category, files['analysis'])
    memory_tip = generate_memory_tip(algorithm_name, category)
    try_it = generate_try_it_example(algorithm_name, category)
    practice = generate_practice_exercise(algorithm_name, category)
    check_understanding = generate_check_understanding(algorithm_name, category, complexity)
    
    # Extract existing common mistakes
    mistakes_section = ""
    if "## Common Mistakes" in content:
        mistakes_start = content.find("## Common Mistakes")
        next_section = content.find("\n## ", mistakes_start + 1)
        if next_section == -1:
            mistakes_section = content[mistakes_start:]
        else:
            mistakes_section = content[mistakes_start:next_section]
    
    enhanced_mistakes = enhance_common_mistakes(mistakes_section)
    
    # Find related algorithms
    related = find_related_algorithms(algorithm_name, category, all_algorithms)
    
    # Check if already enhanced (has Quick Summary)
    already_enhanced = "## 📋 Quick Summary" in content
    
    # Build enhanced content
    enhanced = ""
    
    # Add title and Quick Summary at the top
    if content.startswith('#'):
        # Extract title
        first_newline = content.find('\n')
        if first_newline != -1:
            title = content[:first_newline]
            content = content[first_newline:].lstrip()
        else:
            title = content
            content = ""
        
        enhanced += title + "\n\n"
    else:
        enhanced += f"# {algorithm_name.replace('_', ' ').title()}\n\n"
    
    # Add Quick Summary only if not already present
    if not already_enhanced:
        enhanced += "## 📋 Quick Summary\n\n"
        enhanced += f"- **Purpose:** {one_sentence}\n"
        enhanced += f"- **Complexity:** {complexity}\n"
        enhanced += f"- **Category:** {category}\n"
        enhanced += f"- **Key Idea:** {key_insight}\n\n"
    
    # Insert new sections after Quick Summary (only if not already present)
    if "## 💬 In One Sentence" not in content:
        enhanced += "## 💬 In One Sentence\n\n"
        enhanced += f"{one_sentence}\n\n"
    
    if "## 💡 Key Insight" not in content:
        enhanced += "## 💡 Key Insight\n\n"
        enhanced += f"{key_insight}\n\n"
    
    if "## 🧠 Memory Tip" not in content:
        enhanced += "## 🧠 Memory Tip\n\n"
        enhanced += f"{memory_tip}\n\n"
    
    # Add existing content, filtering out duplicate sections
    if content:
        lines = content.split('\n')
        skip_sections = ['## 📋 Quick Summary', '## 💬 In One Sentence', 
                        '## 💡 Key Insight', '## 🧠 Memory Tip']
        skip_until_newline = False
        
        for line in lines:
            # Skip duplicate sections
            if any(section in line for section in skip_sections):
                skip_until_newline = True
                continue
            
            if skip_until_newline and line.strip() == '':
                skip_until_newline = False
                continue
            
            if skip_until_newline:
                continue
            
            # Skip flowchart/diagram text that got into description
            if any(x in line.lower() for x in ['flowchart', 'step-by-step execution', '-->', 'start([start']):
                continue
            
            enhanced += line + "\n"
    
    # Insert new sections before "Common Mistakes" or at the end (only if not present)
    if "## 🎯 Try It Yourself" not in enhanced:
        if "## Common Mistakes" in enhanced or "## Recommended Literature" in enhanced:
            # Find insertion point (before Common Mistakes or Recommended Literature)
            insert_pos = enhanced.find("## Common Mistakes")
            if insert_pos == -1:
                insert_pos = enhanced.find("## Recommended Literature")
            
            if insert_pos != -1:
                before = enhanced[:insert_pos].rstrip()
                after = enhanced[insert_pos:]
                
                enhanced = before + "\n\n"
                enhanced += "## 🎯 Try It Yourself\n\n"
                enhanced += f"{try_it}\n\n"
                
                enhanced += "## ✏️ Practice Exercise\n\n"
                enhanced += f"{practice}\n\n"
                
                enhanced += "## ✅ Check Your Understanding\n\n"
                enhanced += f"{check_understanding}\n\n"
                enhanced += after
            else:
                # Add at the end
                enhanced += "\n## 🎯 Try It Yourself\n\n"
                enhanced += f"{try_it}\n\n"
                
                enhanced += "## ✏️ Practice Exercise\n\n"
                enhanced += f"{practice}\n\n"
                
                enhanced += "## ✅ Check Your Understanding\n\n"
                enhanced += f"{check_understanding}\n\n"
        else:
            # Add at the end
            enhanced += "\n## 🎯 Try It Yourself\n\n"
            enhanced += f"{try_it}\n\n"
            
            enhanced += "## ✏️ Practice Exercise\n\n"
            enhanced += f"{practice}\n\n"
            
            enhanced += "## ✅ Check Your Understanding\n\n"
            enhanced += f"{check_understanding}\n\n"
    
    # Replace Common Mistakes section if it exists, or add enhanced version
    if "## Common Mistakes" in enhanced:
        mistakes_start = enhanced.find("## Common Mistakes")
        next_section = enhanced.find("\n## ", mistakes_start + len("## Common Mistakes"))
        
        if next_section != -1:
            before_mistakes = enhanced[:mistakes_start]
            after_mistakes = enhanced[next_section:]
            enhanced = before_mistakes + enhanced_mistakes + "\n\n" + after_mistakes
        else:
            enhanced = enhanced[:mistakes_start] + enhanced_mistakes
    else:
        # Add enhanced mistakes section
        enhanced += enhanced_mistakes + "\n\n"
    
    # Add Related Algorithms at the end
    if related:
        enhanced += "## 🔗 Related Algorithms\n\n"
        enhanced += "You might also want to learn:\n"
        for rel in related:
            readable = rel.replace('_', ' ').title()
            enhanced += f"- **{readable}** - Similar algorithm in the same category\n"
        enhanced += "\n"
    
    return enhanced


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm folders."""
    algorithm_folders = []
    
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue
                
                algorithm_folders.append(algo_dir)
    
    return sorted(algorithm_folders)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("ENHANCING ALGORITHM DESCRIPTIONS WITH LEARNING AIDS")
    print("="*70)
    
    algorithm_folders = find_all_algorithm_folders()
    all_algorithm_names = [f.name for f in algorithm_folders]
    
    print(f"\nFound {len(algorithm_folders)} algorithm folders")
    print("\nAdding learning aids:")
    print("  - Quick Summary")
    print("  - In One Sentence")
    print("  - Key Insight")
    print("  - Memory Tip")
    print("  - Try It Yourself")
    print("  - Practice Exercise")
    print("  - Check Your Understanding")
    print("  - Enhanced Common Mistakes")
    print("  - Related Algorithms")
    
    start_time = time.time()
    processed = 0
    errors = 0
    
    for i, algo_folder in enumerate(algorithm_folders, 1):
        algorithm_name = algo_folder.name
        
        try:
            files = read_algorithm_files(algo_folder)
            
            # Process all 4 MD files
            for level in ['school', 'univer']:
                for lang in ['en', 'ru']:
                    md_file = algo_folder / f"{level}.{lang}.md"
                    if md_file.exists():
                        enhanced_content = enhance_md_file(
                            md_file, algorithm_name, files, 
                            all_algorithm_names, level, lang
                        )
                        md_file.write_text(enhanced_content, encoding='utf-8')
            
            processed += 1
            
        except Exception as e:
            print(f"  [ERROR] {algorithm_name}: {e}")
            errors += 1
        
        if i % 100 == 0:
            elapsed = time.time() - start_time
            print(f"Progress: {i}/{len(algorithm_folders)} ({i/len(algorithm_folders)*100:.1f}%) | "
                  f"Time: {elapsed:.1f}s")
    
    total_time = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"Complete: {processed}/{len(algorithm_folders)} algorithms")
    print(f"Errors: {errors}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Files enhanced: {processed * 4}")
    print(f"{'='*70}")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    import time
    sys.exit(main())

