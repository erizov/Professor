#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate "Do Not Confuse With" sections in all algorithm README.md files
with relevant, algorithm-specific content.

Usage:
    python scripts/populate_do_not_confuse.py
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Comprehensive mapping of algorithms to what they should not be confused with
DO_NOT_CONFUSE_MAPPING: Dict[str, str] = {
    # Sorting Algorithms
    "bubble_sort": """- **Insertion Sort**: Both O(n²) but insertion sort builds sorted prefix by inserting elements, while bubble sort swaps adjacent pairs
- **Selection Sort**: Both O(n²) but selection sort finds minimum each pass, bubble sort uses adjacent swaps
- **Cocktail Sort**: Bidirectional bubble sort variant, not the same algorithm""",
    
    "insertion_sort": """- **Bubble Sort**: Similar O(n²) complexity but insertion sort inserts into sorted prefix, bubble sort swaps adjacent pairs
- **Selection Sort**: Both in-place O(n²) but selection sort selects minimum, insertion sort builds sorted prefix incrementally
- **Shell Sort**: Uses insertion sort as subroutine but with gap sequences for better performance""",
    
    "selection_sort": """- **Bubble Sort**: Both O(n²) but selection sort finds minimum each pass, bubble sort uses adjacent swaps
- **Insertion Sort**: Both O(n²) but insertion sort builds sorted prefix, selection sort finds minimum each iteration
- **Heap Sort**: Uses selection principle but with O(n log n) complexity via heap data structure""",
    
    "merge_sort": """- **Quick Sort**: Both divide-and-conquer O(n log n) but merge sort is stable and requires O(n) space, quick sort is in-place but unstable
- **Heap Sort**: Both O(n log n) but heap sort is in-place, merge sort requires extra space
- **Tim Sort**: Hybrid algorithm that uses merge sort as a component but optimizes for real-world data""",
    
    "quick_sort": """- **Merge Sort**: Both divide-and-conquer O(n log n) but quick sort is in-place and unstable, merge sort requires O(n) space and is stable
- **Heap Sort**: Both O(n log n) but heap sort guarantees O(n log n) worst-case, quick sort can degrade to O(n²)
- **Intro Sort**: Hybrid that uses quick sort but falls back to heap sort to avoid worst-case performance""",
    
    "heap_sort": """- **Selection Sort**: Both use selection principle but heap sort achieves O(n log n) via heap, selection sort is O(n²)
- **Quick Sort**: Both O(n log n) but heap sort guarantees worst-case performance, quick sort can degrade
- **Priority Queue**: Heap sort uses heap structure but is a sorting algorithm, not a data structure""",
    
    "counting_sort": """- **Radix Sort**: Counting sort is used as subroutine in radix sort, but they're different algorithms
- **Bucket Sort**: Both non-comparison sorts but counting sort counts occurrences, bucket sort distributes into buckets
- **Pigeonhole Sort**: Similar to counting sort but for integer keys with small range""",
    
    "radix_sort": """- **Counting Sort**: Radix sort uses counting sort as subroutine, but radix processes digits, counting sort counts occurrences
- **Bucket Sort**: Both distribute elements but radix sort processes digits, bucket sort uses hash function
- **LSD vs MSD**: Least Significant Digit vs Most Significant Digit are variants, not different algorithms""",
    
    "bucket_sort": """- **Counting Sort**: Both non-comparison sorts but bucket sort distributes into buckets, counting sort counts occurrences
- **Radix Sort**: Both distribute elements but bucket sort uses hash function, radix sort processes digits
- **Hash Table**: Bucket sort uses buckets but is a sorting algorithm, not a lookup data structure""",
    
    # Searching Algorithms
    "linear_search": """- **Binary Search**: Linear search works on unsorted data O(n), binary search requires sorted data O(log n)
- **Interpolation Search**: Both search but interpolation assumes uniform distribution, linear search makes no assumptions
- **Hash Table Lookup**: Hash tables provide O(1) average lookup, linear search is O(n) sequential""",
    
    "binary_search": """- **Linear Search**: Binary search requires sorted data O(log n), linear search works on any data O(n)
- **Interpolation Search**: Both require sorted data but interpolation assumes uniform distribution for better average case
- **Ternary Search**: Divides into three parts instead of two, similar concept but different implementation""",
    
    "jump_search": """- **Binary Search**: Both require sorted data but jump search uses fixed jump size, binary search halves the search space
- **Linear Search**: Both sequential but jump search skips elements, linear search checks every element
- **Exponential Search**: Similar jumping concept but exponential search doubles jump size, jump search uses fixed size""",
    
    "interpolation_search": """- **Binary Search**: Both require sorted data but interpolation assumes uniform distribution, binary search always halves
- **Linear Search**: Both sequential but interpolation uses position estimation, linear search checks sequentially
- **Exponential Search**: Both use position estimation but exponential search for unbounded arrays""",
    
    # Tree Algorithms
    "binary_search_tree": """- **Binary Tree**: BST enforces ordering property (left < root < right), binary tree has no ordering requirement
- **AVL Tree**: AVL is a self-balancing BST with height balance, BST can become unbalanced
- **Red-Black Tree**: Red-black is a self-balancing BST with color properties, BST has no balancing mechanism""",
    
    "avl_tree": """- **Red-Black Tree**: Both self-balancing BSTs but AVL maintains strict height balance, red-black uses color properties
- **Binary Search Tree**: AVL is a balanced BST variant, regular BST can become unbalanced
- **Splay Tree**: Both self-adjusting but AVL maintains balance, splay tree moves accessed nodes to root""",
    
    "red_black_tree": """- **AVL Tree**: Both self-balancing BSTs but red-black uses color properties, AVL maintains strict height balance
- **Binary Search Tree**: Red-black is a balanced BST variant, regular BST has no balancing
- **B-Tree**: Both balanced but B-tree is multi-way, red-black is binary""",
    
    "b_tree": """- **Binary Search Tree**: B-tree is multi-way (multiple children), BST is binary (two children)
- **B+ Tree**: B+ tree stores data only in leaves, B-tree stores data in all nodes
- **Red-Black Tree**: Both balanced but B-tree is multi-way, red-black is binary""",
    
    # Graph Algorithms
    "bfs": """- **DFS**: BFS explores level by level (queue-based), DFS goes deep first (stack-based)
- **Dijkstra's Algorithm**: BFS finds shortest path in unweighted graphs, Dijkstra handles weighted graphs
- **Level-Order Traversal**: BFS is level-order traversal for trees, but BFS works on any graph""",
    
    "dfs": """- **BFS**: DFS explores deep first (stack-based), BFS explores level by level (queue-based)
- **Backtracking**: DFS is traversal algorithm, backtracking is problem-solving technique using DFS
- **Topological Sort**: Topological sort uses DFS but is a specific application, not the same as DFS""",
    
    "dijkstra": """- **BFS**: Dijkstra handles weighted graphs with priority queue, BFS is for unweighted graphs with queue
- **Bellman-Ford**: Both find shortest paths but Dijkstra requires non-negative weights, Bellman-Ford handles negative weights
- **A* Algorithm**: A* uses heuristic function, Dijkstra explores uniformly in all directions""",
    
    "bellman_ford": """- **Dijkstra's Algorithm**: Both find shortest paths but Bellman-Ford handles negative weights, Dijkstra requires non-negative
- **Floyd-Warshall**: Bellman-Ford is single-source, Floyd-Warshall finds all-pairs shortest paths
- **SPFA**: Shortest Path Faster Algorithm is optimization of Bellman-Ford, not a different algorithm""",
    
    "floyd_warshall": """- **Dijkstra's Algorithm**: Floyd-Warshall finds all-pairs shortest paths, Dijkstra is single-source
- **Bellman-Ford**: Floyd-Warshall finds all-pairs, Bellman-Ford is single-source
- **Johnson's Algorithm**: Both find all-pairs but Johnson's uses Dijkstra as subroutine, Floyd-Warshall uses dynamic programming""",
    
    # Dynamic Programming
    "edit_distance": """- **Hamming Distance**: Edit distance allows insertions/deletions, Hamming distance only allows substitutions
- **Longest Common Subsequence**: LCS finds common subsequence, edit distance finds transformation cost
- **String Matching**: Edit distance measures similarity, string matching finds exact occurrences""",
    
    "longest_common_subsequence": """- **Edit Distance**: LCS finds common subsequence, edit distance finds transformation cost
- **Longest Common Substring**: LCS is subsequence (non-contiguous), substring must be contiguous
- **Longest Increasing Subsequence**: LIS finds increasing sequence, LCS finds common sequence""",
    
    "knapsack": """- **Fractional Knapsack**: 0/1 knapsack takes items whole, fractional knapsack can take fractions (greedy solution)
- **Subset Sum**: Subset sum is special case of knapsack with value=weight, but different problem formulation
- **Bin Packing**: Knapsack maximizes value, bin packing minimizes bins used""",
    
    "fibonacci": """- **Memoization**: Fibonacci can use memoization, but memoization is a technique, not the algorithm
- **Dynamic Programming**: Fibonacci is a DP problem, but DP is a paradigm, not this specific algorithm
- **Matrix Exponentiation**: Fibonacci can be computed via matrix exponentiation, but that's an optimization technique""",
    
    # String Algorithms
    "kmp": """- **Rabin-Karp**: KMP uses prefix function for O(n+m), Rabin-Karp uses hashing for average O(n+m)
- **Boyer-Moore**: Both pattern matching but Boyer-Moore skips characters right-to-left, KMP processes left-to-right
- **Naive String Matching**: KMP avoids redundant comparisons, naive matching checks every position""",
    
    "rabin_karp": """- **KMP Algorithm**: Both pattern matching but Rabin-Karp uses hashing, KMP uses prefix function
- **Boyer-Moore**: Both pattern matching but Boyer-Moore skips characters, Rabin-Karp uses rolling hash
- **Hash Table**: Rabin-Karp uses hashing but is a string matching algorithm, not a data structure""",
    
    "boyer_moore": """- **KMP Algorithm**: Both pattern matching but Boyer-Moore processes right-to-left, KMP processes left-to-right
- **Rabin-Karp**: Both pattern matching but Boyer-Moore uses character skipping, Rabin-Karp uses hashing
- **Sunday Algorithm**: Sunday is variant of Boyer-Moore with different bad character rule""",
    
    # Machine Learning
    "linear_regression": """- **Logistic Regression**: Linear regression predicts continuous values, logistic regression predicts probabilities/classification
- **Polynomial Regression**: Linear regression uses linear relationship, polynomial regression uses polynomial features
- **Ridge/Lasso Regression**: These are regularized variants, not the base algorithm""",
    
    "logistic_regression": """- **Linear Regression**: Logistic regression is for classification, linear regression is for regression
- **Perceptron**: Both linear classifiers but logistic regression uses sigmoid, perceptron uses step function
- **SVM**: Both classifiers but SVM finds maximum margin, logistic regression finds probability distribution""",
    
    "svm": """- **Logistic Regression**: Both classifiers but SVM finds maximum margin hyperplane, logistic regression finds probability distribution
- **Perceptron**: Both linear classifiers but SVM maximizes margin, perceptron just finds separating hyperplane
- **Neural Networks**: SVM is single-layer with kernel trick, neural networks are multi-layer""",
    
    "knn": """- **K-Means Clustering**: KNN is supervised classification/regression, K-means is unsupervised clustering
- **Decision Trees**: Both classifiers but KNN is instance-based, decision trees are model-based
- **Naive Bayes**: Both classifiers but KNN uses distance, naive Bayes uses probability""",
    
    "naive_bayes": """- **Bayesian Networks**: Naive Bayes assumes feature independence, Bayesian networks model dependencies
- **Logistic Regression**: Both probabilistic but naive Bayes uses Bayes' theorem, logistic regression uses sigmoid
- **Gaussian Mixture Models**: Naive Bayes is classifier, GMM is clustering/unsupervised learning""",
    
    "random_forest": """- **Decision Tree**: Random forest is ensemble of decision trees, not a single tree
- **Gradient Boosting**: Both ensemble methods but random forest uses bagging, gradient boosting uses boosting
- **Extra Trees**: Both ensemble methods but extra trees uses random splits, random forest uses best splits""",
    
    # Design Patterns
    "singleton": """- **Factory Pattern**: Singleton ensures single instance, factory creates objects
- **Static Class**: Singleton allows inheritance and interfaces, static class cannot
- **Global Variable**: Singleton is object-oriented pattern, global variable is procedural approach""",
    
    "factory": """- **Abstract Factory**: Factory creates single product type, abstract factory creates families of products
- **Builder Pattern**: Factory creates objects directly, builder constructs complex objects step by step
- **Singleton**: Factory creates multiple instances, singleton ensures single instance""",
    
    "abstract_factory": """- **Factory Pattern**: Abstract factory creates families of products, factory creates single product type
- **Builder Pattern**: Abstract factory creates families, builder constructs complex objects
- **Prototype Pattern**: Abstract factory uses inheritance, prototype uses cloning""",
    
    "observer": """- **Pub-Sub Pattern**: Observer is synchronous push model, pub-sub is asynchronous message-based
- **Mediator Pattern**: Observer has direct subject-observer relationship, mediator centralizes communication
- **Chain of Responsibility**: Observer notifies all, chain of responsibility passes request along chain""",
    
    "strategy": """- **Template Method**: Strategy uses composition, template method uses inheritance
- **State Pattern**: Strategy chooses algorithm, state pattern changes behavior based on state
- **Command Pattern**: Strategy encapsulates algorithm, command encapsulates request""",
    
    "mvc": """- **MVVM**: MVC has controller, MVVM has view model with data binding
- **MVP**: MVC has passive view, MVP has presenter that updates view
- **MVI**: MVC is imperative, MVI (Model-View-Intent) is reactive""",
    
    # Security Patterns
    "jwt": """- **Session Tokens**: JWT is stateless and self-contained, session tokens require server-side storage
- **OAuth**: JWT is token format, OAuth is authorization framework (JWT can be used in OAuth)
- **API Keys**: JWT contains claims and is signed, API keys are simple identifiers""",
    
    "oauth": """- **JWT**: OAuth is authorization framework, JWT is token format (OAuth can use JWT)
- **SAML**: OAuth is for authorization, SAML is for authentication/SSO
- **OpenID Connect**: OAuth is authorization, OpenID Connect adds authentication layer on top""",
    
    "encryption": """- **Hashing**: Encryption is reversible (decrypt), hashing is one-way (cannot reverse)
- **Encoding**: Encryption requires key and provides security, encoding is reversible without security
- **Compression**: Encryption protects data, compression reduces size""",
    
    "aes": """- **RSA**: AES is symmetric encryption (same key), RSA is asymmetric (public/private keys)
- **DES/3DES**: AES is modern standard (128/192/256 bits), DES is deprecated (56 bits)
- **ChaCha20**: Both symmetric but AES is block cipher, ChaCha20 is stream cipher""",
    
    "rsa": """- **AES**: RSA is asymmetric encryption, AES is symmetric encryption
- **ECC**: Both asymmetric but RSA uses large integers, ECC uses elliptic curves (smaller keys)
- **Diffie-Hellman**: RSA is encryption/signing, Diffie-Hellman is key exchange""",
    
    "sha256": """- **MD5/SHA-1**: SHA-256 is secure, MD5 and SHA-1 are cryptographically broken
- **SHA-3**: SHA-256 is SHA-2 family, SHA-3 uses different construction (Keccak)
- **HMAC**: SHA-256 is hash function, HMAC is message authentication code using hash function""",
    
    # Deployment Patterns
    "blue_green": """- **Canary Deployment**: Blue-green switches all traffic instantly, canary gradually increases traffic
- **Rolling Deployment**: Blue-green uses two environments, rolling updates instances gradually
- **A/B Testing**: Blue-green is deployment strategy, A/B testing is feature experimentation""",
    
    "canary": """- **Blue-Green Deployment**: Canary gradually increases traffic, blue-green switches all traffic instantly
- **Rolling Deployment**: Canary routes percentage of traffic, rolling updates instances one by one
- **Feature Flags**: Canary is deployment strategy, feature flags control feature visibility""",
    
    # Testing Patterns
    "unit_testing": """- **Integration Testing**: Unit tests test isolated units, integration tests test component interactions
- **End-to-End Testing**: Unit tests are fast and isolated, E2E tests exercise full system
- **Mocking**: Unit testing is testing approach, mocking is technique used in unit tests""",
    
    "integration_testing": """- **Unit Testing**: Integration tests test interactions, unit tests test isolated units
- **End-to-End Testing**: Integration tests test components, E2E tests test full user workflows
- **System Testing**: Integration tests focus on interfaces, system tests focus on complete system""",
    
    "mocking": """- **Stubbing**: Mocking verifies interactions, stubbing provides predefined responses
- **Faking**: Mocking is for testing, faking is lightweight implementation for testing
- **Spying**: Mocking replaces object, spying wraps real object to record calls""",
    
    "tdd": """- **BDD**: TDD is test-driven development, BDD is behavior-driven development (different focus)
- **Test-First Development**: TDD includes refactoring cycle, test-first is just writing tests first
- **Unit Testing**: TDD is development methodology, unit testing is testing approach""",
    
    # Performance Patterns
    "caching": """- **Memoization**: Caching stores computed results, memoization is caching technique for functions
- **CDN**: Caching is general pattern, CDN is distributed caching infrastructure
- **Database Query Cache**: Caching is pattern, query cache is specific implementation""",
    
    "load_balancing": """- **Reverse Proxy**: Load balancing distributes requests, reverse proxy forwards requests (can include load balancing)
- **API Gateway**: Load balancing is traffic distribution, API gateway provides routing and more features
- **Failover**: Load balancing distributes load, failover switches to backup on failure""",
    
    "rate_limiting": """- **Throttling**: Rate limiting limits request rate, throttling limits resource usage
- **Quotas**: Rate limiting is per-time-window, quotas are total limits over period
- **Circuit Breaker**: Rate limiting prevents overload, circuit breaker prevents cascading failures""",
    
    # Integration Patterns
    "message_queue": """- **Pub-Sub**: Message queue is point-to-point, pub-sub is one-to-many messaging
- **Event Bus**: Message queue stores messages, event bus broadcasts events immediately
- **Stream Processing**: Message queue is messaging, stream processing is continuous data processing""",
    
    "publish_subscribe": """- **Message Queue**: Pub-sub is one-to-many, message queue is point-to-point
- **Observer Pattern**: Pub-sub is messaging infrastructure, observer is design pattern
- **Event Sourcing**: Pub-sub is messaging, event sourcing is data storage pattern""",
    
    "cqrs": """- **Event Sourcing**: CQRS separates read/write, event sourcing stores events (often used together)
- **Repository Pattern**: CQRS separates models, repository abstracts data access
- **Microservices**: CQRS is pattern, microservices is architecture style (CQRS fits well)""",
    
    # Distributed Patterns
    "leader_election": """- **Consensus Algorithms**: Leader election chooses leader, consensus ensures agreement (Raft/Paxos do both)
- **Master-Slave**: Leader election is algorithm, master-slave is architecture pattern
- **Primary-Backup**: Leader election chooses primary, primary-backup is replication strategy""",
    
    "circuit_breaker": """- **Retry Pattern**: Circuit breaker stops requests on failure, retry pattern retries failed requests
- **Bulkhead**: Circuit breaker prevents cascading failures, bulkhead isolates resources
- **Timeout**: Circuit breaker opens on failures, timeout limits request duration""",
    
    "retry_pattern": """- **Circuit Breaker**: Retry attempts again, circuit breaker stops on repeated failures
- **Exponential Backoff**: Retry pattern includes backoff, exponential backoff is specific backoff strategy
- **Idempotency**: Retry pattern retries operations, idempotency ensures safe retries""",
}

# Category-based defaults for algorithms not in specific mapping
CATEGORY_DEFAULTS: Dict[str, str] = {
    "sorting": """- Algorithms with different time complexities (O(n²) vs O(n log n))
- Stable vs unstable sorting algorithms
- In-place vs out-of-place algorithms""",
    
    "searching": """- Algorithms requiring sorted data vs those that don't
- Deterministic vs probabilistic search methods
- Exact match vs approximate/fuzzy search""",
    
    "trees": """- Balanced vs unbalanced tree structures
- Binary vs multi-way trees
- Self-balancing mechanisms (AVL, red-black, etc.)""",
    
    "graphs": """- Algorithms for weighted vs unweighted graphs
- Single-source vs all-pairs shortest path algorithms
- Directed vs undirected graph assumptions""",
    
    "dp": """- Dynamic programming vs greedy algorithms
- Memoization vs tabulation approaches
- Overlapping subproblems vs optimal substructure""",
    
    "strings": """- Exact vs approximate string matching
- Hash-based vs automaton-based algorithms
- Pattern matching vs string similarity""",
    
    "ml": """- Supervised vs unsupervised learning algorithms
- Parametric vs non-parametric models
- Classification vs regression problems""",
    
    "security": """- Encryption vs hashing (reversible vs one-way)
- Symmetric vs asymmetric encryption
- Authentication vs authorization""",
    
    "testing": """- Unit vs integration vs end-to-end testing
- Testing approaches vs testing techniques
- Test-driven vs test-last development""",
    
    "deployment": """- Zero-downtime deployment strategies
- Traffic routing vs instance management
- Deployment patterns vs feature flags""",
    
    "performance": """- Caching strategies vs storage patterns
- Load distribution vs resource allocation
- Rate limiting vs throttling""",
    
    "patterns": """- Creational vs structural vs behavioral patterns
- Design patterns vs architectural patterns
- Patterns vs principles (SOLID)""",
}


def infer_category(lecture_path: str) -> Optional[str]:
    """Infer category from lecture path."""
    path_lower = lecture_path.lower()
    
    if any(x in path_lower for x in ["sorting", "sort"]):
        return "sorting"
    elif any(x in path_lower for x in ["searching", "search"]):
        return "searching"
    elif any(x in path_lower for x in ["tree", "trees"]):
        return "trees"
    elif any(x in path_lower for x in ["graph", "graphs"]):
        return "graphs"
    elif any(x in path_lower for x in ["dynamic_programming", "dp"]):
        return "dp"
    elif any(x in path_lower for x in ["string", "strings"]):
        return "strings"
    elif any(x in path_lower for x in ["ml", "machine_learning", "neural", "cnn", "rnn", "transformer"]):
        return "ml"
    elif any(x in path_lower for x in ["security", "crypto", "encryption", "jwt", "oauth", "authentication"]):
        return "security"
    elif any(x in path_lower for x in ["testing", "test", "tdd", "mocking"]):
        return "testing"
    elif any(x in path_lower for x in ["deployment", "blue_green", "canary"]):
        return "deployment"
    elif any(x in path_lower for x in ["performance", "caching", "load_balancing", "rate_limiting"]):
        return "performance"
    elif any(x in path_lower for x in ["pattern", "solid", "creational", "structural", "behavioral", "architectural"]):
        return "patterns"
    
    return None


def get_do_not_confuse_content(algorithm_name: str, category: Optional[str]) -> str:
    """Get 'Do Not Confuse With' content for an algorithm."""
    # Try exact match first
    if algorithm_name in DO_NOT_CONFUSE_MAPPING:
        return DO_NOT_CONFUSE_MAPPING[algorithm_name]
    
    # Try normalized name (handle variations)
    normalized = algorithm_name.lower().replace("-", "_").replace(" ", "_")
    if normalized in DO_NOT_CONFUSE_MAPPING:
        return DO_NOT_CONFUSE_MAPPING[normalized]
    
    # Use category default
    if category and category in CATEGORY_DEFAULTS:
        return CATEGORY_DEFAULTS[category]
    
    # Generic fallback
    return """- Algorithms with similar names but different characteristics
- Techniques with distinct use cases or complexity guarantees
- Related concepts that serve different purposes"""


def update_readme_do_not_confuse(readme_path: Path, algorithm_name: str, category: Optional[str]) -> bool:
    """Update the 'Do Not Confuse With' section in a README file."""
    if not readme_path.exists():
        return False
    
    content = readme_path.read_text(encoding="utf-8")
    new_content = get_do_not_confuse_content(algorithm_name, category)
    
    # Pattern to match the "Do Not Confuse With" section
    # Matches from "## Do Not Confuse With" to the next "##" or end of file
    pattern = r"(##\s+Do\s+Not\s+Confuse\s+With\s*\n)(.*?)(?=\n##\s+|$)"
    
    def replace_section(match):
        header = match.group(1)
        # Format the new content with proper indentation
        formatted_content = new_content.strip()
        return f"{header}{formatted_content}\n\n"
    
    if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
        # Section exists, replace it
        new_file_content = re.sub(pattern, replace_section, content, flags=re.IGNORECASE | re.DOTALL)
    else:
        # Section doesn't exist, add it before "Examples of Implementation" or at the end
        examples_pattern = r"(##\s+Examples\s+of\s+Implementation)"
        if re.search(examples_pattern, content, re.IGNORECASE):
            # Insert before Examples section
            new_file_content = re.sub(
                examples_pattern,
                f"## Do Not Confuse With\n\n{new_content.strip()}\n\n\\1",
                content,
                flags=re.IGNORECASE
            )
        else:
            # Add at the end
            if not content.endswith("\n"):
                content += "\n"
            new_file_content = content + f"\n## Do Not Confuse With\n\n{new_content.strip()}\n"
    
    if new_file_content != content:
        readme_path.write_text(new_file_content, encoding="utf-8")
        return True
    
    return False


def main():
    """Main function to process all algorithm READMEs."""
    updated_count = 0
    processed_count = 0
    
    # Find all algorithm directories
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                
                # Check if this is an algorithm directory
                if not ((algo_dir / "algorithm.py").exists() or 
                       (algo_dir / "Algorithm.java").exists() or
                       (algo_dir / "README.md").exists()):
                    continue
                
                readme_path = algo_dir / "README.md"
                if not readme_path.exists():
                    continue
                
                algorithm_name = algo_dir.name
                category = infer_category(str(lecture_dir))
                
                processed_count += 1
                if update_readme_do_not_confuse(readme_path, algorithm_name, category):
                    updated_count += 1
                    print(f"Updated: {readme_path.relative_to(ROOT)}")
    
    print(f"\nProcessed {processed_count} algorithm READMEs")
    print(f"Updated {updated_count} 'Do Not Confuse With' sections")


if __name__ == "__main__":
    main()

