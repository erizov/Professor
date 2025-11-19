#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 5.2: Expand Framework Examples to More Algorithms
Add framework examples to algorithms that don't have them yet
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]


# Framework examples for various algorithm categories
FRAMEWORK_EXAMPLES_BY_CATEGORY: Dict[str, Dict[str, str]] = {
    "sorting": {
        "java": """// Java Arrays.sort() uses optimized sorting
import java.util.Arrays;

public class SortingExample {
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        Arrays.sort(arr);  // Uses dual-pivot quicksort
        System.out.println(Arrays.toString(arr));
    }
}""",
        "python": """# Python list.sort() uses Timsort
arr = [64, 34, 25, 12, 22, 11, 90]
arr.sort()  # Timsort: hybrid of merge sort and insertion sort
print(arr)""",
        "spring": """// Spring Framework - Sorting in Data Access
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getUsersSorted(String sortBy) {
        List<User> users = userRepository.findAll();
        users.sort(Comparator.comparing(User::getName));
        return users;
    }
}""",
    },
    "searching": {
        "java": """// Java Collections.binarySearch()
import java.util.*;

List<Integer> list = Arrays.asList(1, 3, 5, 7, 9, 11, 13);
int index = Collections.binarySearch(list, 7);
System.out.println("Found at index: " + index);""",
        "python": """# Python bisect module for binary search
import bisect

arr = [1, 3, 5, 7, 9, 11, 13]
index = bisect.bisect_left(arr, 7)
print(f"Insert position: {index}")""",
    },
    "tree": {
        "java": """// Java TreeMap uses Red-Black Tree
import java.util.*;

TreeMap<String, Integer> tree = new TreeMap<>();
tree.put("apple", 1);
tree.put("banana", 2);
tree.put("cherry", 3);
// Maintains sorted order using Red-Black Tree""",
        "python": """# Python - Tree structures in libraries
from collections import defaultdict

# Tree-like structure using nested dictionaries
tree = defaultdict(dict)
tree['root']['left'] = {'value': 1}
tree['root']['right'] = {'value': 2}""",
        "spring": """// Spring Framework - Tree structure in BeanFactory
@Component
public class ServiceTree {
    @Autowired
    private ServiceA serviceA;  // Tree-based dependency graph
    @Autowired
    private ServiceB serviceB;
}""",
    },
    "graph": {
        "java": """// Java - Graph representation and traversal
import java.util.*;

public class GraphExample {
    private Map<Integer, List<Integer>> graph = new HashMap<>();
    
    public void addEdge(int from, int to) {
        graph.computeIfAbsent(from, k -> new ArrayList<>()).add(to);
    }
}""",
        "python": """# NetworkX - Graph library
import networkx as nx

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
# NetworkX uses efficient graph algorithms internally""",
    },
    "hash": {
        "java": """// Java HashMap uses hash table
import java.util.*;

HashMap<String, Integer> map = new HashMap<>();
map.put("key1", 1);
map.put("key2", 2);
// O(1) average case operations""",
        "python": """# Python dict uses hash table
data = {"key1": 1, "key2": 2, "key3": 3}
value = data.get("key1")  # O(1) average case lookup""",
        "spring": """// Spring Framework - Caching with hash tables
@Service
public class CacheService {
    @Cacheable("users")
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}""",
    },
    "dynamic_programming": {
        "java": """// Java - Dynamic programming pattern
public class DPExample {
    public int fibonacci(int n) {
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
}""",
        "python": """# Python - Dynamic programming
def fibonacci(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]""",
    },
}


def determine_algorithm_category(
    algorithm_name: str, lecture_name: str
) -> Optional[str]:
    """Determine algorithm category from name and lecture."""
    algo_lower = algorithm_name.lower()
    lecture_lower = lecture_name.lower()

    if any(
        word in algo_lower or word in lecture_lower
        for word in [
            "sort",
            "bubble",
            "selection",
            "insertion",
            "heap",
            "counting",
            "radix",
            "bucket",
            "merge",
            "quick",
        ]
    ):
        return "sorting"
    elif any(
        word in algo_lower or word in lecture_lower
        for word in ["search", "linear", "binary", "jump", "interpolation"]
    ):
        return "searching"
    elif any(
        word in algo_lower or word in lecture_lower
        for word in ["tree", "bst", "avl", "trie", "binary_tree"]
    ):
        return "tree"
    elif any(
        word in algo_lower or word in lecture_lower
        for word in ["graph", "bfs", "dfs", "dijkstra", "bellman", "floyd"]
    ):
        return "graph"
    elif any(
        word in algo_lower or word in lecture_lower
        for word in ["hash", "hash_table", "hash_map"]
    ):
        return "hash"
    elif any(
        word in algo_lower or word in lecture_lower
        for word in ["dynamic", "fibonacci", "knapsack", "edit_distance", "longest"]
    ):
        return "dynamic_programming"

    return None


def has_framework_examples(content: str) -> bool:
    """Check if README already has framework examples."""
    # Check for code blocks with framework names
    has_java = "```java" in content and any(
        fw in content for fw in ["Spring", "Java", "Arrays", "Collections"]
    )
    has_python = "```python" in content and "Python" in content
    has_spring = "Spring Framework" in content and "```java" in content
    has_dotnet = ".NET Framework" in content and "```csharp" in content

    return has_java or has_python or has_spring or has_dotnet


def add_framework_examples_to_readme(
    readme_path: Path, algorithm_name: str, lecture_name: str
) -> bool:
    """Add framework examples to README if missing."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Check if already has examples
        if has_framework_examples(content):
            return False

        # Determine category
        category = determine_algorithm_category(algorithm_name, lecture_name)
        if not category:
            return False

        # Get examples for category
        examples = FRAMEWORK_EXAMPLES_BY_CATEGORY.get(category, {})
        if not examples:
            return False

        # Find Examples section
        examples_patterns = [
            r"(## Examples of Implementation\s*\n\s*\n)(.*?)(?=\n##|\Z)",
            r"(## Examples of Deployment\s*\n\s*\n)(.*?)(?=\n##|\Z)",
            r"(## Examples\s*\n\s*\n)(.*?)(?=\n##|\Z)",
        ]

        match = None
        for pattern in examples_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                break

        if not match:
            # Try to add section before "Algorithm Steps" or "Real-World Applications"
            insert_patterns = [
                r"(## Real-World Applications\s*\n)",
                r"(## Algorithm Steps\s*\n)",
                r"(## Detailed Explanation\s*\n)",
            ]

            for pattern in insert_patterns:
                match = re.search(pattern, content)
                if match:
                    # Insert Examples section before this
                    new_section = "## Examples of Implementation\n\n"

                    if "java" in examples:
                        new_section += "### Java Standard Library\n\n"
                        new_section += "```java\n" + examples["java"] + "\n```\n\n"
                        new_section += "**Purpose**: Java standard library uses this algorithm for core data structure operations.\n\n"

                    if "python" in examples:
                        new_section += "### Python Standard Library\n\n"
                        new_section += "```python\n" + examples["python"] + "\n```\n\n"
                        new_section += "**Purpose**: Python standard library uses this algorithm for efficient data operations.\n\n"

                    if "spring" in examples:
                        new_section += "### Spring Framework\n\n"
                        new_section += "```java\n" + examples["spring"] + "\n```\n\n"
                        new_section += "**Purpose**: Spring Framework uses this pattern/algorithm for enterprise application development.\n\n"

                    content = (
                        content[: match.start()]
                        + new_section
                        + content[match.start() :]
                    )
                    readme_path.write_text(content, encoding="utf-8")
                    return True
            return False

        # Add to existing section
        existing_section = match.group(2) if match.lastindex >= 2 else ""

        new_examples = ""
        if "java" in examples and "```java" not in existing_section:
            new_examples += "### Java Standard Library\n\n"
            new_examples += "```java\n" + examples["java"] + "\n```\n\n"
            new_examples += "**Purpose**: Java standard library uses this algorithm for core data structure operations.\n\n"

        if "python" in examples and "```python" not in existing_section:
            new_examples += "### Python Standard Library\n\n"
            new_examples += "```python\n" + examples["python"] + "\n```\n\n"
            new_examples += "**Purpose**: Python standard library uses this algorithm for efficient data operations.\n\n"

        if "spring" in examples and "Spring Framework" not in existing_section:
            new_examples += "### Spring Framework\n\n"
            new_examples += "```java\n" + examples["spring"] + "\n```\n\n"
            new_examples += "**Purpose**: Spring Framework uses this pattern/algorithm for enterprise application development.\n\n"

        if new_examples:
            content = content[: match.end(2)] + new_examples + content[match.end(2) :]
            readme_path.write_text(content, encoding="utf-8")
            return True

        return False

    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Execute Phase 5.2: Expand framework examples."""
    print("=" * 70)
    print("Phase 5.2: Expand Framework Examples to More Algorithms")
    print("=" * 70)

    readme_files = []
    for readme_path in ROOT.rglob("**/README.md"):
        if "supporting_documents" in str(readme_path) or "scripts" in str(readme_path):
            continue
        if readme_path.name == "README.md" and readme_path.parent.name != "Professor":
            readme_files.append(readme_path)

    print(f"\nFound {len(readme_files)} README files to process")

    updated = 0
    for i, readme_path in enumerate(readme_files, 1):
        algorithm_name = readme_path.parent.name
        lecture_name = (
            readme_path.parent.parent.name if readme_path.parent.parent else ""
        )

        if add_framework_examples_to_readme(readme_path, algorithm_name, lecture_name):
            updated += 1
            if updated % 50 == 0:
                print(
                    f"[PROGRESS] Processed {i}/{len(readme_files)} files, updated {updated}..."
                )

    print(f"\n[COMPLETE] Processed {len(readme_files)} files")
    print(f"Updated {updated} README files with framework examples")
    print("\nFramework examples added for:")
    print("  - Sorting algorithms (Java, Python, Spring)")
    print("  - Searching algorithms (Java, Python)")
    print("  - Tree algorithms (Java, Python, Spring)")
    print("  - Graph algorithms (Java, Python)")
    print("  - Hash table algorithms (Java, Python, Spring)")
    print("  - Dynamic programming (Java, Python)")


if __name__ == "__main__":
    main()
