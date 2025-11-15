#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Algorithm Generator.

Quickly generates algorithm folder structures for the course.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


# Algorithm definitions for all semesters
ALGORITHMS = {
    "semester_1": {
        "lecture_01_sorting_fundamentals": [
            {
                "folder": "bubble_sort",
                "name": "Bubble Sort",
                "category": "Sorting",
                "time": "O(n²)",
                "space": "O(1)"
            },
            {
                "folder": "selection_sort",
                "name": "Selection Sort",
                "category": "Sorting",
                "time": "O(n²)",
                "space": "O(1)"
            },
            {
                "folder": "insertion_sort",
                "name": "Insertion Sort",
                "category": "Sorting",
                "time": "O(n²)",
                "space": "O(1)"
            },
        ],
        "lecture_02_efficient_sorting": [
            {
                "folder": "merge_sort",
                "name": "Merge Sort",
                "category": "Sorting",
                "time": "O(n log n)",
                "space": "O(n)"
            },
            {
                "folder": "quick_sort",
                "name": "Quick Sort",
                "category": "Sorting",
                "time": "O(n log n)",
                "space": "O(log n)"
            },
            {
                "folder": "heap_sort",
                "name": "Heap Sort",
                "category": "Sorting",
                "time": "O(n log n)",
                "space": "O(1)"
            },
        ],
        "lecture_03_specialized_sorting": [
            {
                "folder": "counting_sort",
                "name": "Counting Sort",
                "category": "Sorting",
                "time": "O(n + k)",
                "space": "O(k)"
            },
            {
                "folder": "radix_sort",
                "name": "Radix Sort",
                "category": "Sorting",
                "time": "O(nk)",
                "space": "O(n + k)"
            },
            {
                "folder": "bucket_sort",
                "name": "Bucket Sort",
                "category": "Sorting",
                "time": "O(n + k)",
                "space": "O(n)"
            },
        ],
        "lecture_04_searching": [
            {
                "folder": "linear_search",
                "name": "Linear Search",
                "category": "Searching",
                "time": "O(n)",
                "space": "O(1)"
            },
            {
                "folder": "binary_search",
                "name": "Binary Search",
                "category": "Searching",
                "time": "O(log n)",
                "space": "O(1)"
            },
            {
                "folder": "jump_search",
                "name": "Jump Search",
                "category": "Searching",
                "time": "O(√n)",
                "space": "O(1)"
            },
            {
                "folder": "interpolation_search",
                "name": "Interpolation Search",
                "category": "Searching",
                "time": "O(log log n)",
                "space": "O(1)"
            },
        ],
        "lecture_05_trees": [
            {
                "folder": "binary_tree",
                "name": "Binary Tree",
                "category": "Data Structure",
                "time": "O(n)",
                "space": "O(n)"
            },
            {
                "folder": "binary_search_tree",
                "name": "Binary Search Tree",
                "category": "Data Structure",
                "time": "O(log n)",
                "space": "O(n)"
            },
            {
                "folder": "avl_tree",
                "name": "AVL Tree",
                "category": "Data Structure",
                "time": "O(log n)",
                "space": "O(n)"
            },
        ],
    },
    "semester_2": {
        "lecture_06_solid_principles": [
            {
                "folder": "single_responsibility",
                "name": "Single Responsibility Principle",
                "category": "SOLID",
                "time": "N/A",
                "space": "N/A"
            },
            {
                "folder": "open_closed",
                "name": "Open/Closed Principle",
                "category": "SOLID",
                "time": "N/A",
                "space": "N/A"
            },
            {
                "folder": "liskov_substitution",
                "name": "Liskov Substitution Principle",
                "category": "SOLID",
                "time": "N/A",
                "space": "N/A"
            },
            {
                "folder": "interface_segregation",
                "name": "Interface Segregation Principle",
                "category": "SOLID",
                "time": "N/A",
                "space": "N/A"
            },
            {
                "folder": "dependency_inversion",
                "name": "Dependency Inversion Principle",
                "category": "SOLID",
                "time": "N/A",
                "space": "N/A"
            },
        ],
        "lecture_07_creational_patterns": [
            {
                "folder": "singleton",
                "name": "Singleton Pattern",
                "category": "Creational Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "factory",
                "name": "Factory Method Pattern",
                "category": "Creational Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "abstract_factory",
                "name": "Abstract Factory Pattern",
                "category": "Creational Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "builder",
                "name": "Builder Pattern",
                "category": "Creational Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "prototype",
                "name": "Prototype Pattern",
                "category": "Creational Pattern",
                "time": "O(n)",
                "space": "O(n)"
            },
        ],
        "lecture_08_structural_patterns": [
            {
                "folder": "adapter",
                "name": "Adapter Pattern",
                "category": "Structural Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "bridge",
                "name": "Bridge Pattern",
                "category": "Structural Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "composite",
                "name": "Composite Pattern",
                "category": "Structural Pattern",
                "time": "O(n)",
                "space": "O(n)"
            },
            {
                "folder": "decorator",
                "name": "Decorator Pattern",
                "category": "Structural Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "facade",
                "name": "Facade Pattern",
                "category": "Structural Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "proxy",
                "name": "Proxy Pattern",
                "category": "Structural Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
        ],
        "lecture_09_behavioral_patterns": [
            {
                "folder": "observer",
                "name": "Observer Pattern",
                "category": "Behavioral Pattern",
                "time": "O(n)",
                "space": "O(n)"
            },
            {
                "folder": "strategy",
                "name": "Strategy Pattern",
                "category": "Behavioral Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "command",
                "name": "Command Pattern",
                "category": "Behavioral Pattern",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "iterator",
                "name": "Iterator Pattern",
                "category": "Behavioral Pattern",
                "time": "O(n)",
                "space": "O(1)"
            },
            {
                "folder": "template_method",
                "name": "Template Method Pattern",
                "category": "Behavioral Pattern",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "chain_of_responsibility",
                "name": "Chain of Responsibility",
                "category": "Behavioral Pattern",
                "time": "O(n)",
                "space": "O(1)"
            },
        ],
    },
    "semester_3": {
        "lecture_10_graph_algorithms": [
            {
                "folder": "dfs",
                "name": "Depth-First Search",
                "category": "Graph Algorithm",
                "time": "O(V + E)",
                "space": "O(V)"
            },
            {
                "folder": "bfs",
                "name": "Breadth-First Search",
                "category": "Graph Algorithm",
                "time": "O(V + E)",
                "space": "O(V)"
            },
            {
                "folder": "dijkstra",
                "name": "Dijkstra's Algorithm",
                "category": "Graph Algorithm",
                "time": "O(E log V)",
                "space": "O(V)"
            },
            {
                "folder": "bellman_ford",
                "name": "Bellman-Ford Algorithm",
                "category": "Graph Algorithm",
                "time": "O(VE)",
                "space": "O(V)"
            },
            {
                "folder": "floyd_warshall",
                "name": "Floyd-Warshall Algorithm",
                "category": "Graph Algorithm",
                "time": "O(V³)",
                "space": "O(V²)"
            },
        ],
        "lecture_11_dynamic_programming": [
            {
                "folder": "fibonacci",
                "name": "Fibonacci Sequence",
                "category": "Dynamic Programming",
                "time": "O(n)",
                "space": "O(n)"
            },
            {
                "folder": "longest_common_subsequence",
                "name": "Longest Common Subsequence",
                "category": "Dynamic Programming",
                "time": "O(mn)",
                "space": "O(mn)"
            },
            {
                "folder": "knapsack",
                "name": "Knapsack Problem",
                "category": "Dynamic Programming",
                "time": "O(nW)",
                "space": "O(nW)"
            },
            {
                "folder": "edit_distance",
                "name": "Edit Distance",
                "category": "Dynamic Programming",
                "time": "O(mn)",
                "space": "O(mn)"
            },
        ],
        "lecture_12_ml_algorithms": [
            {
                "folder": "linear_regression",
                "name": "Linear Regression",
                "category": "Machine Learning",
                "time": "O(n²d)",
                "space": "O(nd)"
            },
            {
                "folder": "logistic_regression",
                "name": "Logistic Regression",
                "category": "Machine Learning",
                "time": "O(nd)",
                "space": "O(d)"
            },
            {
                "folder": "knn",
                "name": "K-Nearest Neighbors",
                "category": "Machine Learning",
                "time": "O(nd)",
                "space": "O(nd)"
            },
            {
                "folder": "decision_tree",
                "name": "Decision Tree",
                "category": "Machine Learning",
                "time": "O(n log n)",
                "space": "O(n)"
            },
            {
                "folder": "kmeans",
                "name": "K-Means Clustering",
                "category": "Machine Learning",
                "time": "O(nki)",
                "space": "O(n + k)"
            },
        ],
        "lecture_13_integration_patterns": [
            {
                "folder": "message_queue",
                "name": "Message Queue Pattern",
                "category": "Integration",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "publish_subscribe",
                "name": "Publish-Subscribe Pattern",
                "category": "Integration",
                "time": "O(n)",
                "space": "O(n)"
            },
            {
                "folder": "event_sourcing",
                "name": "Event Sourcing",
                "category": "Integration",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "cqrs",
                "name": "CQRS Pattern",
                "category": "Integration",
                "time": "O(1)",
                "space": "O(1)"
            },
        ],
    },
    "semester_4": {
        "lecture_14_security_patterns": [
            {
                "folder": "authentication",
                "name": "Authentication Pattern",
                "category": "Security",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "authorization",
                "name": "Authorization Pattern",
                "category": "Security",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "oauth",
                "name": "OAuth 2.0",
                "category": "Security",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "jwt",
                "name": "JSON Web Tokens",
                "category": "Security",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "encryption",
                "name": "Encryption Algorithms",
                "category": "Security",
                "time": "O(n)",
                "space": "O(n)"
            },
        ],
        "lecture_15_testing_patterns": [
            {
                "folder": "unit_testing",
                "name": "Unit Testing Pattern",
                "category": "Testing",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "integration_testing",
                "name": "Integration Testing",
                "category": "Testing",
                "time": "O(n)",
                "space": "O(1)"
            },
            {
                "folder": "tdd",
                "name": "Test-Driven Development",
                "category": "Testing",
                "time": "N/A",
                "space": "N/A"
            },
            {
                "folder": "mocking",
                "name": "Mocking Pattern",
                "category": "Testing",
                "time": "O(1)",
                "space": "O(1)"
            },
        ],
        "lecture_16_deployment_patterns": [
            {
                "folder": "blue_green",
                "name": "Blue-Green Deployment",
                "category": "Deployment",
                "time": "O(1)",
                "space": "O(2n)"
            },
            {
                "folder": "canary",
                "name": "Canary Deployment",
                "category": "Deployment",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "circuit_breaker",
                "name": "Circuit Breaker Pattern",
                "category": "Deployment",
                "time": "O(1)",
                "space": "O(1)"
            },
            {
                "folder": "retry_pattern",
                "name": "Retry Pattern",
                "category": "Deployment",
                "time": "O(k)",
                "space": "O(1)"
            },
        ],
        "lecture_17_performance": [
            {
                "folder": "caching",
                "name": "Caching Strategies",
                "category": "Performance",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "load_balancing",
                "name": "Load Balancing",
                "category": "Performance",
                "time": "O(1)",
                "space": "O(n)"
            },
            {
                "folder": "rate_limiting",
                "name": "Rate Limiting",
                "category": "Performance",
                "time": "O(1)",
                "space": "O(n)"
            },
        ],
    }
}


def create_minimal_algorithm(
    semester: str,
    lecture: str,
    algo_info: Dict[str, Any]
) -> None:
    """Create minimal algorithm structure."""
    base_path = Path(semester) / lecture / algo_info['folder']
    base_path.mkdir(parents=True, exist_ok=True)
    
    # Metadata
    metadata = {
        "name": algo_info['name'],
        "category": algo_info['category'],
        "complexity": {
            "time": algo_info['time'],
            "space": algo_info['space']
        }
    }
    
    with open(base_path / "metadata.json", 'w', 
             encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Simple README
    readme = f"# {algo_info['name']}\n\n"
    readme += f"**Category**: {algo_info['category']}\n\n"
    readme += f"**Time Complexity**: {algo_info['time']}\n\n"
    readme += f"**Space Complexity**: {algo_info['space']}\n\n"
    readme += "## Implementation\n\nSee algorithm.py and Algorithm.java\n"
    
    with open(base_path / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    
    # Simple Python
    func_name = algo_info['folder']
    py_code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""{algo_info['name']} implementation."""


def {func_name}():
    """Implement {algo_info['name']}."""
    print("==" * 35)
    print("{algo_info['name']}")
    print("==" * 35)
    print(f"Time Complexity: {algo_info['time']}")
    print(f"Space Complexity: {algo_info['space']}")
    print("==" * 35)


if __name__ == "__main__":
    {func_name}()
'''
    
    with open(base_path / "algorithm.py", 'w', 
             encoding='utf-8') as f:
        f.write(py_code)
    
    # Simple Java
    java_code = f'''/**
 * {algo_info['name']} implementation.
 */
public class Algorithm {{
    public static void main(String[] args) {{
        System.out.println("==".repeat(35));
        System.out.println("{algo_info['name']}");
        System.out.println("==".repeat(35));
        System.out.println("Time Complexity: {algo_info['time']}");
        System.out.println("Space Complexity: {algo_info['space']}");
        System.out.println("==".repeat(35));
    }}
}}
'''
    
    with open(base_path / "Algorithm.java", 'w', 
             encoding='utf-8') as f:
        f.write(java_code)


def main() -> None:
    """Generate all algorithm structures."""
    total = 0
    
    for semester, lectures in ALGORITHMS.items():
        for lecture, algorithms in lectures.items():
            for algo in algorithms:
                create_minimal_algorithm(semester, lecture, algo)
                total += 1
                print(f"Created: {semester}/{lecture}/{algo['folder']}")
    
    print(f"\nTotal algorithms created: {total}")


if __name__ == "__main__":
    main()

