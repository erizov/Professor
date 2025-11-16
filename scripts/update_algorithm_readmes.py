#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate or enhance README.md files for all algorithms under semester_* with
an Introduction and Short Description. Designed to be idempotent and minimal.

Usage:
    python scripts/update_algorithm_readmes.py
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

CATEGORY_HINTS = {
    "sorting": ["lecture_01_sorting_fundamentals", "lecture_02_efficient_sorting", "lecture_03_specialized_sorting"],
    "searching": ["lecture_04_searching"],
    "trees": ["lecture_05_trees", "lecture_06_advanced_trees"],
    "heaps": ["lecture_07_heaps_priority"],
    "hashing": ["lecture_08_hash_tables"],
    "graphs": ["lecture_09_graph_algorithms"],
    "dp": ["lecture_11_dynamic_programming"],
    "strings": ["lecture_12_string_algorithms"],
    "crypto": ["lecture_18_crypto_algorithms"],
    "distributed": ["lecture_19_distributed_patterns"],
    "observability": ["lecture_20_monitoring_observability"],
    "ml": ["lecture_12_ml_algorithms", "lecture_16_advanced_ml", "lecture_22_cnn_architectures", "lecture_29_nlp_advanced", "lecture_30_time_series"],
    "database": ["lecture_53_database_operations", "lecture_54_data_modeling"],
}

CATEGORY_INTRO: Dict[str, str] = {
    "sorting": "Sorting algorithms reorder elements in a list or array according to a comparison key. They are fundamental to computer science and serve as building blocks for efficient data processing.",
    "searching": "Searching algorithms locate a target element or determine its absence within a collection. They trade off between speed, memory, and preconditions like sortedness.",
    "trees": "Tree algorithms operate on hierarchical data structures, enabling efficient insertion, deletion, and various queries over ordered or structured data.",
    "heaps": "Heap and priority-queue algorithms maintain partial order to support efficient retrieval of the minimum or maximum element.",
    "hashing": "Hash table algorithms map keys to indices for average constant-time insert, lookup, and delete, trading space for speed.",
    "graphs": "Graph algorithms analyze relationships between entities modeled as nodes and edges, solving problems like traversal, connectivity, and shortest paths.",
    "dp": "Dynamic programming solves complex problems by breaking them into overlapping subproblems and reusing intermediate results to avoid recomputation.",
    "strings": "String algorithms process sequences of characters for tasks like pattern matching, parsing, and text indexing.",
    "crypto": "Cryptographic algorithms provide confidentiality, integrity, and authenticity guarantees through mathematical primitives and protocols.",
    "distributed": "Distributed algorithms coordinate multiple nodes to achieve reliability, consistency, and scalability in distributed systems.",
    "observability": "Monitoring and observability patterns collect and analyze telemetry data to understand system behavior and performance.",
    "ml": "Machine learning algorithms learn patterns from data to make predictions or decisions, spanning classical methods and deep learning.",
    "database": "Data modeling and database algorithms organize and optimize data storage, retrieval, and governance for robust applications.",
}

SHORT_DESC_HINTS: Dict[str, str] = {
    "bubble_sort": "A simple, stable, in-place sorting algorithm that repeatedly swaps adjacent out-of-order elements. Time: O(n^2) average/worst, Space: O(1).",
    "insertion_sort": "Stable, in-place sort that builds the final array one item at a time by inserting into the sorted prefix. Time: O(n^2) avg/worst, O(n) best.",
    "selection_sort": "In-place sort that repeatedly selects the minimum element and moves it to the front. Time: O(n^2), Space: O(1).",
    "merge_sort": "Divide-and-conquer stable sort that merges sorted halves. Time: O(n log n), Space: O(n).",
    "quick_sort": "Divide-and-conquer sort using partition around a pivot. Average O(n log n), worst O(n^2), often fastest in practice.",
    "heap_sort": "In-place sort using a binary heap to repeatedly extract the max/min. Time: O(n log n), Space: O(1) auxiliary.",
    "linear_search": "Sequentially checks each element for a match. Works on any collection. Time: O(n).",
    "binary_search": "Searches a sorted array by repeatedly halving the search interval. Time: O(log n).",
    "bfs": "Breadth-first search traverses a graph level by level, useful for shortest paths in unweighted graphs.",
    "dfs": "Depth-first search explores as far as possible along a branch before backtracking; useful for cycle detection and topological sorting.",
    "dijkstra": "Computes single-source shortest paths for graphs with non-negative weights using a priority queue.",
    "fibonacci": "Computes the nth Fibonacci number; optimized versions use DP or matrix exponentiation.",
    "edit_distance": "Levenshtein distance between two strings via dynamic programming; counts minimum edit operations.",
    "knapsack": "0/1 knapsack maximizes value within a weight capacity; classic DP with O(nW) time.",
    "kmp": "Knuth–Morris–Pratt string matching uses prefix function to achieve O(n+m) pattern search.",
    "sha256": "Cryptographic hash function producing a 256-bit digest; part of SHA-2 family.",
    "leader_election": "Distributed algorithm to elect a coordinator among nodes ensuring a single leader.",
}

README_TEMPLATE = """# {title}

## Introduction
{introduction}

## Short Description
{short_description}

## Often Used Together With
{often_used_together}

## Do Not Confuse With
{do_not_confuse_with}

"""

INTRO_RE = re.compile(r"^##\s*Introduction\s*$", re.IGNORECASE | re.MULTILINE)
SHORT_RE = re.compile(r"^##\s*Short\s*Description\s*$", re.IGNORECASE | re.MULTILINE)
TOGETHER_RE = re.compile(r"^##\s*Often\s*Used\s*Together\s*With\s*$", re.IGNORECASE | re.MULTILINE)
CONFUSE_RE = re.compile(r"^##\s*Do\s*Not\s*Confuse\s*With\s*$", re.IGNORECASE | re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def infer_category(lecture_path: str) -> Optional[str]:
    for cat, hints in CATEGORY_HINTS.items():
        if any(h in lecture_path for h in hints):
            return cat
    return None


def prettify_name(name: str) -> str:
    return name.replace("_", " ").title()


def get_short_desc(algo_name: str, category: Optional[str]) -> str:
    if algo_name in SHORT_DESC_HINTS:
        return SHORT_DESC_HINTS[algo_name]
    # generic fallbacks by category
    if category and category in CATEGORY_INTRO:
        base = CATEGORY_INTRO[category]
        return f"{prettify_name(algo_name)} is a {category} algorithm. {base}"
    return f"{prettify_name(algo_name)} is an algorithm commonly used in computer science for solving a well-defined class of problems efficiently."


def get_intro(category: Optional[str]) -> str:
    if category and category in CATEGORY_INTRO:
        return CATEGORY_INTRO[category]
    return "This algorithm is widely used in computer science for solving a specific class of problems efficiently and reliably."


def readme_needs_section(content: str, section_re) -> bool:
    return not bool(section_re.search(content))

OFTEN_USED_DEFAULTS: Dict[str, str] = {
    "sorting": "- Binary Search\n- Hash Tables\n- Heaps/Priority Queues",
    "searching": "- Sorting Algorithms\n- Hash Tables\n- Trees (BST/AVL)",
    "trees": "- Hash Tables\n- Heaps/Priority Queues\n- Graph Traversals",
    "heaps": "- Heap Sort\n- Dijkstra's Algorithm\n- Event Scheduling",
    "hashing": "- Caching\n- Bloom Filters\n- Consistent Hashing",
    "graphs": "- BFS/DFS\n- Dijkstra/Floyd–Warshall\n- Topological Sort",
    "dp": "- Greedy Algorithms\n- Divide and Conquer\n- Memoization",
    "strings": "- Trie\n- Suffix Array/Tree\n- Hashing (Rabin–Karp)",
    "crypto": "- Key Exchange (Diffie–Hellman)\n- Digital Signatures\n- HMAC",
    "distributed": "- Consensus (Raft/Paxos)\n- Heartbeats\n- Gossip Protocols",
    "observability": "- Metrics (Prometheus)\n- Logging\n- Tracing",
    "ml": "- Feature Engineering\n- Cross-Validation\n- Regularization",
    "database": "- Indexing (B-Tree)\n- ETL Pipelines\n- Data Warehousing",
}

def get_often_used_together(algo_name: str, category: Optional[str]) -> str:
    if category and category in OFTEN_USED_DEFAULTS:
        return OFTEN_USED_DEFAULTS[category]
    return "- Related Algorithms\n- Complementary Data Structures\n- Common Utilities"


def ensure_sections(content: str, title: str, introduction: str, short_description: str, often_used_together: str, do_not_confuse_with: str) -> str:
    # If content lacks a title, prepend one
    if not TITLE_RE.search(content):
        content = f"# {title}\n\n" + content

    # Append missing sections to the end to avoid disrupting existing content
    additions = []
    if readme_needs_section(content, INTRO_RE):
        additions.append(f"## Introduction\n{introduction}\n")
    if readme_needs_section(content, SHORT_RE):
        additions.append(f"## Short Description\n{short_description}\n")
    if readme_needs_section(content, TOGETHER_RE):
        additions.append(f"## Often Used Together With\n{often_used_together}\n")
    if readme_needs_section(content, CONFUSE_RE):
        additions.append(f"## Do Not Confuse With\n{do_not_confuse_with}\n")

    if additions:
        if not content.endswith("\n"):
            content += "\n"
        content += "\n".join(additions) + "\n"
    return content


def process_algorithm_dir(algo_dir: Path) -> Tuple[bool, Optional[str]]:
    # Find algorithm name and category
    algo_name = algo_dir.name
    # Lecture path two levels up: semester_x/lecture_y
    lecture_path = str(algo_dir.parent)
    category = infer_category(lecture_path)

    title = prettify_name(algo_name)
    introduction = get_intro(category)
    short_desc = get_short_desc(algo_name, category)
    together = get_often_used_together(algo_name, category)
    # Build a reasonable "Do Not Confuse With" list
    cat_defaults = {
        "sorting": "- Algorithms with different stability or in-place behavior\n- Asymptotically similar but practically different methods",
        "searching": "- Methods requiring sorted input vs. not\n- Probabilistic vs. deterministic search",
        "graphs": "- Algorithms assuming weighted vs. unweighted graphs\n- Directed vs. undirected assumptions",
        "dp": "- Greedy heuristics that may not yield optimal solutions\n- Divide-and-conquer without memoization",
        "strings": "- Hash-based vs prefix-function-based matchers\n- Exact vs approximate matching",
        "crypto": "- Hash vs encryption primitives\n- Message digest vs MAC",
        "distributed": "- Consensus vs leader election\n- Fault tolerance vs availability strategies",
        "ml": "- Supervised vs unsupervised methods\n- Parametric vs non-parametric models",
        "database": "- OLTP vs OLAP designs\n- Normalization vs denormalization strategies",
    }
    algo_confuse_specific = {
        "bubble_sort": "- Insertion Sort (similar O(n^2) but different behavior on partially sorted data)\n- Selection Sort (selects min each pass, fewer swaps)",
        "insertion_sort": "- Bubble Sort (swapping adjacent pairs vs inserting into sorted prefix)",
        "merge_sort": "- Quick Sort (both divide-and-conquer but different partitioning and stability)",
        "binary_search": "- Interpolation Search (assumes uniform distribution)\n- Exponential Search (for unbounded arrays)",
        "bfs": "- DFS (different traversal order and use-cases)",
        "dijkstra": "- Bellman–Ford (handles negative edges)\n- A* (uses heuristic)",
        "kmp": "- Rabin–Karp (hash-based matching)\n- Boyer–Moore (different skipping heuristics)",
        "sha256": "- MD5/SHA-1 (weaker security)\n- SHA-3 (different construction)",
    }
    do_not_confuse_with = algo_confuse_specific.get(algo_name, cat_defaults.get(category, "- Algorithms with similar names but different guarantees\n- Techniques with distinct prerequisites or goals"))

    readme_path = algo_dir / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        new_content = ensure_sections(content, title, introduction, short_desc, together, do_not_confuse_with)
        if new_content != content:
            readme_path.write_text(new_content, encoding="utf-8")
            return True, f"updated {readme_path}"
        return False, None
    else:
        # Create minimal README
        tmpl = README_TEMPLATE.format(title=title, introduction=introduction, short_description=short_desc, often_used_together=together, do_not_confuse_with=do_not_confuse_with)
        readme_path.write_text(tmpl, encoding="utf-8")
        return True, f"created {readme_path}"


def is_algorithm_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    # Heuristics: has algorithm.py or metadata.json or Algorithm.java
    if (path / "algorithm.py").exists() or (path / "metadata.json").exists() or (path / "Algorithm.java").exists():
        return True
    # Or contains a single .py whose name equals folder
    if (path / f"{path.name}.py").exists():
        return True
    return False


def main() -> None:
    updated = 0
    processed = 0
    for entry in ROOT.iterdir():
        if entry.is_dir() and entry.name.startswith("semester_"):
            for lecture in entry.iterdir():
                if not lecture.is_dir():
                    continue
                for algo_dir in lecture.iterdir():
                    if is_algorithm_dir(algo_dir):
                        processed += 1
                        changed, msg = process_algorithm_dir(algo_dir)
                        if changed:
                            updated += 1
                            print(msg)
    print(f"Processed {processed} algorithm folders; updated {updated} READMEs.")


if __name__ == "__main__":
    main()
