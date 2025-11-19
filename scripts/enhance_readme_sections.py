#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive README enhancement script based on critiques.
Adds: Learning Objectives, Prerequisites, Self-Assessment, Visual Diagrams,
Practice Exercises, Real-World Applications, Common Misconceptions,
Worked Examples, TL;DR sections, and fixes Short Description.
"""

import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple
import json

ROOT = Path(__file__).resolve().parents[1]

# Algorithm-specific concise descriptions (not repeating title)
ALGORITHM_DESCRIPTIONS: Dict[str, str] = {
    "quick_sort": "A divide-and-conquer sorting algorithm that partitions an array around a pivot element, recursively sorting subarrays.",
    "bubble_sort": "A simple comparison-based sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
    "merge_sort": "A stable, divide-and-conquer sorting algorithm that divides the array into halves, recursively sorts them, and merges the sorted halves.",
    "heap_sort": "An in-place sorting algorithm that uses a binary heap data structure to sort elements by repeatedly extracting the maximum element.",
    "insertion_sort": "A simple sorting algorithm that builds the final sorted array one item at a time, similar to how you sort playing cards in your hands.",
    "selection_sort": "A sorting algorithm that finds the minimum element from the unsorted portion and places it at the beginning, repeating until sorted.",
    "binary_search": "An efficient search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.",
    "bfs": "A graph traversal algorithm that explores all vertices at the current depth level before moving to vertices at the next depth level.",
    "dfs": "A graph traversal algorithm that explores as far as possible along each branch before backtracking.",
    "dijkstra": "A shortest path algorithm that finds the minimum distance from a source vertex to all other vertices in a weighted graph.",
    "knapsack": "An optimization problem-solving algorithm that determines the most valuable combination of items that fit within a weight constraint.",
    "edit_distance": "A dynamic programming algorithm that calculates the minimum number of operations needed to transform one string into another.",
    "kmp": "A string matching algorithm that uses a precomputed failure function to avoid unnecessary character comparisons.",
    "singleton": "A creational design pattern that ensures a class has only one instance and provides global access to that instance.",
    "factory": "A creational design pattern that provides an interface for creating objects without specifying their exact classes.",
    "observer": "A behavioral design pattern that defines a one-to-many dependency between objects, so when one object changes state, all dependents are notified.",
    "strategy": "A behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable.",
    "mvc": "An architectural pattern that separates an application into three interconnected components: Model, View, and Controller.",
    "repository": "A design pattern that abstracts data access logic, providing a collection-like interface for accessing domain objects.",
    "jwt": "A compact, URL-safe token format for securely transmitting information between parties as a JSON object.",
    "oauth": "An authorization framework that enables applications to obtain limited access to user accounts on HTTP services.",
    "authentication": "The process of verifying the identity of a user, device, or system attempting to access resources.",
    "authorization": "The process of determining what actions an authenticated user is permitted to perform on resources.",
    "caching": "A performance optimization technique that stores frequently accessed data in fast storage to reduce access time.",
    "load_balancing": "A technique for distributing incoming network traffic across multiple servers to ensure reliability and performance.",
    "rate_limiting": "A technique for controlling the rate of requests sent or received by a network interface controller.",
    "circuit_breaker": "A design pattern that prevents cascading failures by stopping requests to a failing service until it recovers.",
    "retry_pattern": "A design pattern that automatically retries failed operations with exponential backoff to handle transient failures.",
    "message_queue": "An asynchronous communication pattern where messages are stored in a queue until they can be processed.",
    "publish_subscribe": "A messaging pattern where publishers send messages to topics without knowing who the subscribers are.",
    "blue_green": "A deployment strategy that maintains two identical production environments, switching traffic between them for zero-downtime deployments.",
    "canary": "A deployment strategy that gradually rolls out changes to a small subset of users before full deployment.",
    "aes": "A symmetric encryption algorithm that encrypts data in fixed-size blocks using a secret key.",
    "rsa": "An asymmetric encryption algorithm that uses a public-private key pair for secure data transmission.",
    "sha256": "A cryptographic hash function that produces a 256-bit hash value, commonly used for data integrity verification.",
    "leader_election": "A distributed computing algorithm that selects a single node to coordinate activities in a cluster.",
    "log_aggregation": "The process of collecting, centralizing, and storing log data from multiple sources for analysis and monitoring.",
}

# Category-based descriptions for algorithms not in specific mapping
CATEGORY_DESCRIPTIONS: Dict[str, str] = {
    "sorting": "A comparison-based algorithm that arranges elements in a specific order (ascending or descending).",
    "searching": "An algorithm that finds the location of a target value within a data structure.",
    "tree": "A hierarchical data structure algorithm that organizes data in a tree-like structure with nodes and edges.",
    "graph": "An algorithm that processes graph data structures, exploring relationships between vertices and edges.",
    "dynamic_programming": "An optimization technique that solves complex problems by breaking them into simpler subproblems and storing results.",
    "string": "An algorithm that processes and manipulates sequences of characters to solve string-related problems.",
    "pattern": "A reusable solution to a commonly occurring problem in software design.",
    "security": "A security mechanism that protects data, systems, or communications from unauthorized access or attacks.",
    "testing": "A software testing technique that validates the correctness and quality of code implementations.",
    "deployment": "A strategy for releasing software updates to production environments with minimal disruption.",
    "performance": "An optimization technique that improves system efficiency, speed, or resource utilization.",
    "integration": "A pattern for connecting and coordinating different software components or systems.",
    "distributed": "An algorithm designed to work across multiple networked computers or nodes.",
    "monitoring": "A technique for observing and tracking system behavior, performance, and health.",
    "ml": "A machine learning algorithm that learns patterns from data to make predictions or decisions.",
}


def infer_category(lecture_path: str) -> Optional[str]:
    """Infer category from lecture path."""
    path_lower = lecture_path.lower()

    if any(x in path_lower for x in ["sorting", "sort"]):
        return "sorting"
    elif any(x in path_lower for x in ["searching", "search"]):
        return "searching"
    elif any(x in path_lower for x in ["tree", "trees"]):
        return "tree"
    elif any(x in path_lower for x in ["graph", "graphs"]):
        return "graph"
    elif any(x in path_lower for x in ["dynamic_programming", "dp"]):
        return "dynamic_programming"
    elif any(x in path_lower for x in ["string", "strings"]):
        return "string"
    elif any(
        x in path_lower
        for x in ["security", "crypto", "encryption", "jwt", "oauth", "authentication"]
    ):
        return "security"
    elif any(x in path_lower for x in ["testing", "test", "tdd", "mocking"]):
        return "testing"
    elif any(x in path_lower for x in ["deployment", "blue_green", "canary"]):
        return "deployment"
    elif any(
        x in path_lower
        for x in ["performance", "caching", "load_balancing", "rate_limiting"]
    ):
        return "performance"
    elif any(
        x in path_lower
        for x in [
            "pattern",
            "solid",
            "creational",
            "structural",
            "behavioral",
            "architectural",
        ]
    ):
        return "pattern"
    elif any(
        x in path_lower
        for x in ["integration", "message_queue", "publish_subscribe", "cqrs"]
    ):
        return "integration"
    elif any(
        x in path_lower for x in ["distributed", "leader_election", "circuit_breaker"]
    ):
        return "distributed"
    elif any(
        x in path_lower for x in ["monitoring", "observability", "log_aggregation"]
    ):
        return "monitoring"
    elif any(
        x in path_lower for x in ["ml", "machine_learning", "neural", "cnn", "rnn"]
    ):
        return "ml"

    return None


def get_short_description(algorithm_name: str, category: Optional[str]) -> str:
    """Get concise short description that doesn't repeat the title."""
    normalized_name = algorithm_name.lower().replace("-", "_")

    if normalized_name in ALGORITHM_DESCRIPTIONS:
        return ALGORITHM_DESCRIPTIONS[normalized_name]

    if category and category in CATEGORY_DESCRIPTIONS:
        return CATEGORY_DESCRIPTIONS[category]

    return "An algorithm that solves a specific computational problem efficiently."


def generate_learning_objectives(algorithm_name: str, category: Optional[str]) -> str:
    """Generate learning objectives section."""
    section = "## Learning Objectives\n\n"
    section += "By the end of this lecture, students will be able to:\n\n"
    section += (
        "1. Implement " + algorithm_name.replace("_", " ").title() + " from scratch\n"
    )
    section += "2. Analyze time and space complexity using Big O notation\n"
    section += "3. Identify when to use this algorithm vs. alternative approaches\n"
    section += "4. Recognize common implementation pitfalls and how to avoid them\n"
    section += "5. Apply this algorithm to solve real-world problems\n"

    if category == "sorting":
        section += "6. Compare stability, in-place properties, and performance characteristics\n"
    elif category == "graph":
        section += "6. Visualize graph traversal and understand edge cases\n"
    elif category == "pattern":
        section += "6. Recognize when this pattern is appropriate in system design\n"
    elif category == "security":
        section += "6. Understand security implications and best practices\n"

    return section + "\n"


def generate_prerequisites(
    algorithm_name: str, category: Optional[str], semester: int
) -> str:
    """Generate prerequisites section."""
    section = "## Prerequisites\n\n"

    if semester == 1:
        section += "- Basic programming knowledge in Python or Java\n"
        section += "- Understanding of arrays, lists, and basic data structures\n"
        section += "- Familiarity with loops, conditionals, and functions\n"
        if category == "sorting":
            section += "- Basic understanding of comparison operations\n"
        elif category == "searching":
            section += "- Knowledge of array indexing and iteration\n"
    elif semester == 2:
        section += "- Completed Semester 1 algorithms course\n"
        section += "- Understanding of object-oriented programming concepts\n"
        section += "- Familiarity with design principles (SOLID)\n"
        if category == "pattern":
            section += "- Knowledge of interfaces, inheritance, and polymorphism\n"
    elif semester == 3:
        section += "- Completed Semesters 1-2\n"
        section += "- Understanding of graph data structures\n"
        section += "- Basic knowledge of recursion\n"
        if category == "ml":
            section += "- Elementary linear algebra and statistics\n"
            section += "- Basic calculus concepts (for ML algorithms)\n"
    elif semester >= 4:
        section += "- Completed previous semesters\n"
        section += "- Understanding of distributed systems concepts\n"
        section += "- Knowledge of system design principles\n"
        if category == "security":
            section += "- Basic understanding of cryptography\n"
        elif category == "deployment":
            section += "- Familiarity with containerization (Docker)\n"

    return section + "\n"


def generate_tldr(algorithm_name: str, category: Optional[str]) -> str:
    """Generate TL;DR section."""
    name_display = algorithm_name.replace("_", " ").title()

    section = "## TL;DR (Too Long; Didn't Read)\n\n"

    # One sentence description
    desc = get_short_description(algorithm_name, category)
    section += f"**One Sentence**: {desc}\n\n"

    # Complexity (will be filled from existing README if available)
    section += "**Time Complexity**: See complexity analysis below\n"
    section += "**Space Complexity**: See complexity analysis below\n"
    section += "**When to Use**: See 'Best Use Case' section\n"
    section += "**When NOT to Use**: See 'Do Not Confuse With' section\n\n"

    return section


def generate_self_assessment(algorithm_name: str, category: Optional[str]) -> str:
    """Generate self-assessment questions."""
    name_display = algorithm_name.replace("_", " ").title()

    section = "## Self-Assessment Questions\n\n"
    section += "Test your understanding with these questions:\n\n"

    section += "### Comprehension\n"
    section += f"1. Can you explain how {name_display} works in your own words?\n"
    section += f"2. What is the key insight or technique that makes {name_display} efficient?\n\n"

    section += "### Analysis\n"
    section += (
        f"3. What are the best-case, average-case, and worst-case time complexities?\n"
    )
    section += (
        f"4. When would you choose {name_display} over alternative algorithms?\n\n"
    )

    section += "### Application\n"
    section += f"5. Can you implement {name_display} from memory without looking at the code?\n"
    section += f"6. What real-world problem could you solve using {name_display}?\n\n"

    section += "### Debugging\n"
    section += (
        f"7. What are the most common mistakes when implementing {name_display}?\n"
    )
    section += f"8. How would you test your {name_display} implementation?\n\n"

    section += "**Scoring**: If you can answer 6+ questions confidently, you've mastered this algorithm!\n\n"

    return section


def generate_practice_exercises(algorithm_name: str, category: Optional[str]) -> str:
    """Generate practice exercises with graduated difficulty."""
    name_display = algorithm_name.replace("_", " ").title()

    section = "## Practice Exercises\n\n"

    section += "### Level 1: Understanding (Beginner)\n"
    section += (
        f"1. Trace through {name_display} step-by-step with input: [5, 2, 8, 1, 9]\n"
    )
    section += f"2. Identify the base case(s) in {name_display}\n"
    section += f"3. Explain why {name_display} has its time complexity\n\n"

    section += "### Level 2: Implementation (Intermediate)\n"
    section += (
        f"4. Implement {name_display} from scratch using only the function signature\n"
    )
    section += f"5. Modify {name_display} to handle edge cases (empty input, single element, etc.)\n"
    section += f"6. Add logging to track the algorithm's execution steps\n\n"

    section += "### Level 3: Optimization (Advanced)\n"
    section += f"7. Optimize {name_display} for a specific use case (e.g., nearly sorted data)\n"
    section += f"8. Implement a parallel or distributed version of {name_display}\n"
    section += f"9. Compare {name_display} performance with alternative algorithms on large datasets\n\n"

    section += "### Level 4: Real-World Application (Expert)\n"
    section += (
        f"10. Design a system that uses {name_display} to solve a production problem\n"
    )
    section += f"11. Create unit tests with 100% code coverage for {name_display}\n"
    section += (
        f"12. Write a technical blog post explaining {name_display} to beginners\n\n"
    )

    return section


def generate_real_world_applications(
    algorithm_name: str, category: Optional[str]
) -> str:
    """Generate real-world applications section."""
    name_display = algorithm_name.replace("_", " ").title()

    section = "## Real-World Applications\n\n"

    apps = {
        "quick_sort": [
            "**Database Systems**: Used in SQL ORDER BY operations for efficient query result sorting",
            "**Operating Systems**: Process scheduling and file system organization",
            "**Gaming**: Leaderboard ranking and score sorting",
        ],
        "merge_sort": [
            "**External Sorting**: Sorting large files that don't fit in memory",
            "**Version Control**: Git uses merge sort for three-way merges",
            "**Inversion Counting**: Counting inversions in arrays (used in recommendation systems)",
        ],
        "binary_search": [
            "**Search Engines**: Finding documents in sorted indexes",
            "**Databases**: Index lookups in B-trees",
            "**Debugging**: Binary search for finding bugs (git bisect)",
        ],
        "bfs": [
            "**Social Networks**: Finding shortest path between users (degrees of separation)",
            "**Web Crawling**: Discovering all pages on a website",
            "**GPS Navigation**: Finding shortest route between locations",
        ],
        "dfs": [
            "**Maze Solving**: Finding paths through mazes",
            "**Dependency Resolution**: Resolving package dependencies",
            "**Topological Sorting**: Task scheduling and build systems",
        ],
        "singleton": [
            "**Database Connections**: Managing single connection pool instance",
            "**Logging Systems**: Centralized logger instance",
            "**Configuration Managers**: Single source of truth for application settings",
        ],
        "observer": [
            "**Model-View Architectures**: UI updates when data changes",
            "**Event Systems**: Pub-sub messaging in distributed systems",
            "**Reactive Programming**: RxJava, React.js state management",
        ],
        "jwt": [
            "**REST APIs**: Stateless authentication for microservices",
            "**Single Sign-On (SSO)**: Cross-domain authentication",
            "**Mobile Apps**: Secure token-based authentication",
        ],
        "caching": [
            "**Web Browsers**: Browser cache for faster page loads",
            "**CDNs**: Content delivery networks cache static assets",
            "**Databases**: Query result caching (Redis, Memcached)",
        ],
        "load_balancing": [
            "**Web Servers**: Distributing HTTP requests across multiple servers",
            "**API Gateways**: Routing traffic to backend services",
            "**Database Clusters**: Distributing queries across database replicas",
        ],
    }

    normalized_name = algorithm_name.lower().replace("-", "_")
    if normalized_name in apps:
        for app in apps[normalized_name]:
            section += f"- {app}\n"
    else:
        section += f"- **Enterprise Applications**: {name_display} is widely used in production systems\n"
        section += (
            f"- **Performance Optimization**: Applied to improve system efficiency\n"
        )
        section += (
            f"- **System Design**: Integral part of scalable architecture patterns\n"
        )

    section += "\n"
    return section


def generate_common_misconceptions(algorithm_name: str, category: Optional[str]) -> str:
    """Generate common misconceptions section."""
    name_display = algorithm_name.replace("_", " ").title()

    section = "## Common Misconceptions\n\n"

    misconceptions = {
        "quick_sort": [
            (
                '❌ **WRONG**: "Quick Sort is always O(n log n)"',
                "✓ **CORRECT**: Quick Sort is O(n²) in worst case (already sorted input), but O(n log n) average case",
            ),
            (
                '❌ **WRONG**: "Quick Sort requires O(n) extra space"',
                "✓ **CORRECT**: Quick Sort is in-place with O(log n) space for recursion stack",
            ),
        ],
        "merge_sort": [
            (
                '❌ **WRONG**: "Merge Sort is always faster than Quick Sort"',
                "✓ **CORRECT**: Quick Sort is usually faster in practice due to better cache locality",
            ),
            (
                '❌ **WRONG**: "Merge Sort can\'t be done in-place"',
                "✓ **CORRECT**: In-place variants exist but are more complex",
            ),
        ],
        "binary_search": [
            (
                '❌ **WRONG**: "Binary Search works on any array"',
                "✓ **CORRECT**: Binary Search requires the array to be sorted",
            ),
            (
                '❌ **WRONG**: "Binary Search is always faster than Linear Search"',
                "✓ **CORRECT**: For small arrays, linear search may be faster due to overhead",
            ),
        ],
    }

    normalized_name = algorithm_name.lower().replace("-", "_")
    if normalized_name in misconceptions:
        for wrong, correct in misconceptions[normalized_name]:
            section += f"{wrong}\n"
            section += f"{correct}\n\n"
    else:
        section += (
            f'❌ **WRONG**: "{name_display} is the best solution for all problems"\n'
        )
        section += f"✓ **CORRECT**: {name_display} has specific use cases and trade-offs; choose algorithms based on requirements\n\n"
        section += f'❌ **WRONG**: "{name_display} is too complex to understand"\n'
        section += f"✓ **CORRECT**: {name_display} can be understood by breaking it down into smaller steps\n\n"

    return section


def generate_visual_diagram(algorithm_name: str, category: Optional[str]) -> str:
    """Generate ASCII art diagram for algorithm visualization."""
    section = "## Algorithm Visualization\n\n"

    diagrams = {
        "quick_sort": """
```
Quick Sort Visualization: [5, 2, 8, 1, 9]

Initial:           [5, 2, 8, 1, 9]
                    ↓
Partition (pivot=5): [2, 1] [5] [8, 9]
                    ↓        ↓      ↓
Recurse left:      [1, 2]  [5]  [8, 9]
                    ↓        ↓      ↓
Combine:           [1, 2, 5, 8, 9]
```
""",
        "merge_sort": """
```
Merge Sort Visualization: [5, 2, 8, 1]

Divide:
[5, 2, 8, 1]
    ↓
[5, 2]  [8, 1]
  ↓        ↓
[5] [2]  [8] [1]

Merge:
[2, 5]  [1, 8]
    ↓
[1, 2, 5, 8]
```
""",
        "binary_search": """
```
Binary Search: Find 7 in [1, 3, 5, 7, 9, 11]

Step 1: Check middle (index 2, value 5)
[1, 3, 5, 7, 9, 11]
         ↑
        5 < 7, search right

Step 2: Check middle of right half (index 4, value 9)
[7, 9, 11]
    ↑
    9 > 7, search left

Step 3: Check remaining (index 3, value 7)
[7]
 ↑
 Found! Index 3
```
""",
    }

    normalized_name = algorithm_name.lower().replace("-", "_")
    if normalized_name in diagrams:
        section += diagrams[normalized_name]
    else:
        section += f"*Visual diagram for {algorithm_name.replace('_', ' ').title()} would be added here*\n"
        section += "*Consider using online visualization tools or drawing step-by-step execution*\n"

    section += "\n"
    return section


def update_readme_sections(
    readme_path: Path, algorithm_name: str, lecture_path: str, semester: int
) -> bool:
    """Update README with all new sections."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        category = infer_category(lecture_path)

        # Fix Short Description
        short_desc_pattern = (
            r"(### Short Description\s*\n\s*\n)(.*?)(\n\s*\n\*\*Key Characteristics)"
        )
        new_short_desc = get_short_description(algorithm_name, category)
        if re.search(short_desc_pattern, content, re.DOTALL):
            content = re.sub(
                short_desc_pattern,
                r"\1" + new_short_desc + r"\3",
                content,
                flags=re.DOTALL,
            )

        # Add TL;DR after Introduction
        if "## TL;DR" not in content:
            intro_pattern = (
                r"(## Introduction\s*\n\s*\n.*?\n\s*\n)(### Short Description)"
            )
            tldr_section = generate_tldr(algorithm_name, category)
            if re.search(intro_pattern, content, re.DOTALL):
                content = re.sub(
                    intro_pattern,
                    r"\1" + tldr_section + r"\2",
                    content,
                    flags=re.DOTALL,
                )

        # Add Learning Objectives after TL;DR or after Introduction
        if "## Learning Objectives" not in content:
            if "## TL;DR" in content:
                # Add after TL;DR
                tldr_end = content.find("## TL;DR") + len("## TL;DR")
                tldr_section_end = content.find("\n## ", tldr_end)
                if tldr_section_end > 0:
                    content = (
                        content[:tldr_section_end]
                        + "\n"
                        + generate_learning_objectives(algorithm_name, category)
                        + content[tldr_section_end:]
                    )
                else:
                    # TL;DR is last section, add at end
                    content = (
                        content
                        + "\n"
                        + generate_learning_objectives(algorithm_name, category)
                    )
            else:
                # Add after Introduction
                intro_end = content.find("### Short Description")
                if intro_end > 0:
                    content = (
                        content[:intro_end]
                        + generate_learning_objectives(algorithm_name, category)
                        + content[intro_end:]
                    )

        # Add Prerequisites if not exists (after Learning Objectives)
        if "## Prerequisites" not in content:
            if "## Learning Objectives" in content:
                # Add after Learning Objectives
                lo_end = content.find("## Learning Objectives") + len(
                    "## Learning Objectives"
                )
                lo_section_end = content.find("\n## ", lo_end)
                if lo_section_end > 0:
                    content = (
                        content[:lo_section_end]
                        + "\n"
                        + generate_prerequisites(algorithm_name, category, semester)
                        + content[lo_section_end:]
                    )
                else:
                    content = (
                        content
                        + "\n"
                        + generate_prerequisites(algorithm_name, category, semester)
                    )
            else:
                # Add after Introduction if Learning Objectives doesn't exist
                intro_end = content.find("### Short Description")
                if intro_end > 0:
                    content = (
                        content[:intro_end]
                        + generate_prerequisites(algorithm_name, category, semester)
                        + content[intro_end:]
                    )

        # Add sections before "Examples of Implementation"
        new_sections = []

        if "## Self-Assessment Questions" not in content:
            new_sections.append(generate_self_assessment(algorithm_name, category))

        if "## Algorithm Visualization" not in content:
            new_sections.append(generate_visual_diagram(algorithm_name, category))

        if "## Practice Exercises" not in content:
            new_sections.append(generate_practice_exercises(algorithm_name, category))

        if "## Real-World Applications" not in content:
            new_sections.append(
                generate_real_world_applications(algorithm_name, category)
            )

        if "## Common Misconceptions" not in content:
            new_sections.append(
                generate_common_misconceptions(algorithm_name, category)
            )

        # Insert new sections before "Examples of Implementation"
        if new_sections and "## Examples of Implementation" in content:
            examples_pos = content.find("## Examples of Implementation")
            content = (
                content[:examples_pos]
                + "\n".join(new_sections)
                + "\n"
                + content[examples_pos:]
            )
        elif new_sections:
            # Add at the end if Examples section doesn't exist
            content += "\n" + "\n".join(new_sections)

        readme_path.write_text(content, encoding="utf-8")
        return True

    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Main function to enhance all READMEs."""
    updated_count = 0
    processed_count = 0

    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue

        # Extract semester number
        semester_match = re.search(r"semester_(\d+)", semester_dir.name)
        semester = int(semester_match.group(1)) if semester_match else 1

        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue

            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue

                readme_path = algo_dir / "README.md"
                if not readme_path.exists():
                    continue

                algorithm_name = algo_dir.name
                processed_count += 1

                if update_readme_sections(
                    readme_path, algorithm_name, str(lecture_dir), semester
                ):
                    updated_count += 1
                    if updated_count % 10 == 0:
                        print(f"Updated {updated_count} READMEs...")

    print(f"\nProcessed {processed_count} algorithm READMEs")
    print(f"Updated {updated_count} READMEs with new sections")


if __name__ == "__main__":
    main()
