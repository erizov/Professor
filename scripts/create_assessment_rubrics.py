#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create assessment rubrics for algorithms.
Adds grading criteria and assessment information to README files.
"""

import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]

ASSESSMENT_SECTION = """## Assessment

### Self-Assessment Questions

**Comprehension:**
1. What is the time complexity of this algorithm?
2. What is the space complexity of this algorithm?

**Analysis:**
3. Why does this algorithm work correctly?
4. What are the key steps in this algorithm?

**Application:**
5. When would you choose this algorithm over alternatives?
6. What are the constraints for using this algorithm?

**Debugging:**
7. What would happen if [common mistake]?
8. How would you fix [common error]?

### Grading Rubric

| Criterion | Excellent (5) | Good (4) | Adequate (3) | Poor (2) |
|-----------|---------------|----------|--------------|----------|
| **Correctness** | All tests pass, handles edge cases | 90%+ tests pass | 70%+ tests pass | <70% tests pass |
| **Efficiency** | Optimal complexity | Near optimal | Works but inefficient | Very inefficient |
| **Code Quality** | Excellent style, very readable | Good style, readable | Adequate style | Poor style |
| **Testing** | 90%+ coverage, comprehensive | 70%+ coverage, good | 50%+ coverage, basic | <50% coverage |
| **Documentation** | Complete, clear, examples | Mostly complete | Some gaps | Missing key parts |

**Scoring Guide:**
- Excellent (90-100%): Mastery demonstrated
- Good (80-89%): Solid understanding
- Adequate (70-79%): Basic understanding
- Poor (60-69%): Needs improvement
- Fail (<60%): Insufficient understanding

### Practice Exercises

**Level 1 - Beginner (3 exercises):**
1. Trace the algorithm execution on [simple example]
2. Fill in the missing code in [partial implementation]
3. Identify the output for [given input]

**Level 2 - Intermediate (4 exercises):**
4. Fix the bug in [buggy implementation]
5. Implement a variation that [specific requirement]
6. Optimize the algorithm for [specific constraint]
7. Compare this algorithm with [alternative algorithm]

**Level 3 - Advanced (3 exercises):**
8. Design an improved version that [enhancement]
9. Implement the algorithm for [different data type]
10. Analyze the algorithm's behavior with [edge case]

**Level 4 - Expert (2 exercises):**
11. Research and implement [advanced variant]
12. Design a new algorithm inspired by this one

**Solutions**: See `solutions/` directory for detailed solutions.
"""


def add_assessment_section(readme_path: Path) -> bool:
    """Add assessment section to README."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Check if section already exists
        if "## Assessment" in content:
            return False

        # Find insertion point - before "## Examples of Implementation" or at end
        insertion_points = [
            (r"(## Examples of Implementation)", ASSESSMENT_SECTION + "\n\n\1"),
            (r"(## References)", ASSESSMENT_SECTION + "\n\n\1"),
        ]

        for pattern, replacement in insertion_points:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                readme_path.write_text(content, encoding="utf-8")
                return True

        # If no insertion point found, add at end
        content = content.rstrip() + "\n\n" + ASSESSMENT_SECTION + "\n"
        readme_path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Add assessment sections to top algorithms."""
    # Top 20 algorithms
    top_algorithms = [
        "semester_01/lecture_02_efficient_sorting/quick_sort",
        "semester_01/lecture_02_efficient_sorting/merge_sort",
        "semester_01/lecture_04_searching/binary_search",
        "semester_01/lecture_09_graph_algorithms/bfs",
        "semester_01/lecture_09_graph_algorithms/dijkstra",
    ]

    updated_count = 0
    for algo_path in top_algorithms:
        readme_path = ROOT / algo_path / "README.md"
        if readme_path.exists():
            if add_assessment_section(readme_path):
                updated_count += 1
                print(f"Added assessment section to {algo_path}")

    print(f"\nAdded assessment sections to {updated_count} algorithms")


if __name__ == "__main__":
    main()
