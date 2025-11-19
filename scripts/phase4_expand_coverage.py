#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4 Enhancements: Expand Framework Examples and Real-World Applications Coverage
Based on Comprehensive_Critiques_and_Improvement3.md
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

ROOT = Path(__file__).resolve().parents[1]


# Expanded framework examples for more algorithm types
EXPANDED_FRAMEWORK_EXAMPLES: Dict[str, Dict[str, str]] = {
    "heap_sort": {
        "java": """// Java PriorityQueue uses heap internally
import java.util.*;

public class HeapSortExample {
    public static void main(String[] args) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        heap.add(64);
        heap.add(34);
        heap.add(25);
        heap.add(12);
        
        // PriorityQueue maintains min-heap property
        while (!heap.isEmpty()) {
            System.out.println(heap.poll()); // Always removes smallest
        }
    }
}""",
        "python": """# Python heapq module uses heap sort
import heapq

def heap_sort_example():
    arr = [64, 34, 25, 12, 22, 11, 90]
    heapq.heapify(arr)  # Convert to min-heap
    
    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))
    return sorted_arr""",
    },
    "bfs": {
        "spring": """// Spring Framework - BFS in Dependency Resolution
@Component
public class DependencyResolver {
    public List<Component> resolveDependencies(Component root) {
        Queue<Component> queue = new LinkedList<>();
        Set<Component> visited = new HashSet<>();
        List<Component> result = new ArrayList<>();
        
        queue.offer(root);
        visited.add(root);
        
        while (!queue.isEmpty()) {
            Component current = queue.poll();
            result.add(current);
            
            // BFS: Add all dependencies
            for (Component dep : current.getDependencies()) {
                if (!visited.contains(dep)) {
                    visited.add(dep);
                    queue.offer(dep);
                }
            }
        }
        return result;
    }
}""",
        "python": """# NetworkX uses BFS for graph traversal
import networkx as nx
from collections import deque

def bfs_example(graph, start):
    queue = deque([start])
    visited = {start}
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result""",
    },
    "dfs": {
        "spring": """// Spring Framework - DFS in Bean Initialization
@Component
public class BeanInitializer {
    private Set<Bean> visited = new HashSet<>();
    
    public void initializeBeans(Bean root) {
        if (visited.contains(root)) {
            return; // Cycle detection
        }
        
        visited.add(root);
        
        // DFS: Initialize dependencies first
        for (Bean dependency : root.getDependencies()) {
            initializeBeans(dependency);
        }
        
        root.initialize();
    }
}""",
        "python": """# Python - DFS implementation
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    
    return result""",
    },
    "dijkstra": {
        "java": """// Java - Dijkstra's Algorithm for Shortest Path
import java.util.*;

public class DijkstraExample {
    public Map<Node, Integer> shortestPaths(Graph graph, Node start) {
        PriorityQueue<Node> pq = new PriorityQueue<>(
            Comparator.comparingInt(n -> distances.get(n))
        );
        Map<Node, Integer> distances = new HashMap<>();
        Set<Node> visited = new HashSet<>();
        
        distances.put(start, 0);
        pq.offer(start);
        
        while (!pq.isEmpty()) {
            Node current = pq.poll();
            if (visited.contains(current)) continue;
            
            visited.add(current);
            
            for (Edge edge : graph.getEdges(current)) {
                int newDist = distances.get(current) + edge.weight;
                if (newDist < distances.getOrDefault(edge.to, Integer.MAX_VALUE)) {
                    distances.put(edge.to, newDist);
                    pq.offer(edge.to);
                }
            }
        }
        return distances;
    }
}""",
    },
    "hash_table": {
        "java": """// Java HashMap uses hash table
import java.util.*;

public class HashTableExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        map.put("apple", 1);
        map.put("banana", 2);
        map.put("cherry", 3);
        
        // O(1) average case lookup
        Integer value = map.get("banana");
        System.out.println(value); // 2
    }
}""",
        "python": """# Python dict uses hash table
def hash_table_example():
    # Dictionary is implemented as hash table
    data = {
        "apple": 1,
        "banana": 2,
        "cherry": 3
    }
    
    # O(1) average case lookup
    value = data.get("banana")
    return value""",
    },
    "strategy": {
        "spring": """// Spring Framework - Strategy Pattern with @Qualifier
public interface PaymentStrategy {
    void pay(double amount);
}

@Component("creditCard")
public class CreditCardStrategy implements PaymentStrategy {
    public void pay(double amount) {
        // Credit card payment logic
    }
}

@Component("paypal")
public class PayPalStrategy implements PaymentStrategy {
    public void pay(double amount) {
        // PayPal payment logic
    }
}

@Service
public class PaymentService {
    @Autowired
    @Qualifier("creditCard")
    private PaymentStrategy strategy;
    
    public void processPayment(double amount) {
        strategy.pay(amount);
    }
}""",
        "dotnet": """// .NET - Strategy Pattern
public interface IPaymentStrategy
{
    void Pay(decimal amount);
}

public class CreditCardStrategy : IPaymentStrategy
{
    public void Pay(decimal amount)
    {
        // Credit card payment logic
    }
}

public class PaymentService
{
    private readonly IPaymentStrategy _strategy;
    
    public PaymentService(IPaymentStrategy strategy)
    {
        _strategy = strategy;
    }
    
    public void ProcessPayment(decimal amount)
    {
        _strategy.Pay(amount);
    }
}""",
    },
    "adapter": {
        "spring": """// Spring Framework - Adapter Pattern
public interface NewPaymentService {
    void processPayment(double amount);
}

@Component
public class LegacyPaymentAdapter implements NewPaymentService {
    @Autowired
    private LegacyPaymentService legacyService;
    
    public void processPayment(double amount) {
        // Adapt legacy interface to new interface
        legacyService.pay(amount, "USD");
    }
}""",
    },
    "decorator": {
        "spring": """// Spring Framework - Decorator Pattern with @Transactional
@Service
public class UserService {
    @Transactional  // Decorator adds transaction management
    public User createUser(User user) {
        return userRepository.save(user);
    }
    
    @Cacheable("users")  // Decorator adds caching
    public User getUser(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}""",
    },
}


# Expanded real-world applications
EXPANDED_REAL_WORLD_APPS: Dict[str, List[str]] = {
    "heap_sort": [
        "**Operating Systems**: Process scheduling uses priority queues (heap-based)",
        "**Game Development**: A* pathfinding uses heaps for open set management",
        "**Network Routing**: OSPF and other routing protocols use heaps",
        "**Event Simulation**: Discrete event simulation uses priority queues",
        "**Task Scheduling**: Job schedulers use heaps for priority-based scheduling",
    ],
    "bfs": [
        "**Social Networks**: Facebook uses BFS for friend suggestions and graph traversal",
        "**Web Crawling**: Search engines use BFS to crawl web pages level by level",
        "**Network Analysis**: Network topology discovery uses BFS",
        "**Shortest Path (Unweighted)**: GPS systems use BFS for unweighted graphs",
        "**Level-Order Traversal**: Tree algorithms use BFS for level-order processing",
    ],
    "dfs": [
        "**Compiler Design**: Abstract syntax tree traversal uses DFS",
        "**Maze Solving**: Pathfinding algorithms use DFS for exploration",
        "**Topological Sort**: Build systems use DFS for dependency resolution",
        "**Cycle Detection**: Graph algorithms use DFS to detect cycles",
        "**File System Traversal**: Directory traversal uses DFS",
    ],
    "dijkstra": [
        "**GPS Navigation**: Google Maps, Waze use Dijkstra for route planning",
        "**Network Routing**: OSPF protocol uses Dijkstra for shortest path",
        "**Social Networks**: LinkedIn uses Dijkstra for connection paths",
        "**Game AI**: Pathfinding in games uses Dijkstra variants",
        "**Telecommunications**: Network routing and call routing use Dijkstra",
    ],
    "hash_table": [
        "**Database Indexing**: Hash indexes for fast lookups",
        "**Caching Systems**: Memcached, Redis use hash tables internally",
        "**Programming Languages**: Python dict, Java HashMap, JavaScript objects",
        "**Web Browsers**: Browser caches use hash tables for URL lookups",
        "**Compilers**: Symbol tables use hash tables for identifier lookup",
    ],
    "strategy": [
        "**Payment Processing**: Stripe, PayPal use strategy pattern for payment methods",
        "**E-commerce**: Shopping cart systems use strategy for shipping calculations",
        "**Game Development**: AI behavior uses strategy pattern for different tactics",
        "**Sorting Libraries**: Collections.sort() uses strategy for comparison",
        "**Validation Frameworks**: Input validation uses strategy for different rules",
    ],
    "adapter": [
        "**Legacy System Integration**: Adapting old APIs to new interfaces",
        "**Third-Party Libraries**: Wrapping external libraries with adapters",
        "**Database Drivers**: JDBC adapters for different database systems",
        "**Payment Gateways**: Adapting different payment provider APIs",
        "**Message Formats**: Converting between JSON, XML, Protocol Buffers",
    ],
    "decorator": [
        "**Java I/O Streams**: BufferedReader, BufferedInputStream are decorators",
        "**Python Decorators**: @property, @staticmethod are decorator pattern",
        "**Spring Framework**: @Transactional, @Cacheable are decorators",
        "**Web Frameworks**: Middleware in Express.js, Flask use decorator pattern",
        "**Logging Frameworks**: Adding logging, timing to methods",
    ],
}


def find_all_readme_files() -> List[Path]:
    """Find all README.md files in algorithm directories."""
    readme_files = []
    for readme_path in ROOT.rglob("**/README.md"):
        if "supporting_documents" in str(readme_path):
            continue
        if readme_path.name == "README.md" and readme_path.parent.name != "Professor":
            readme_files.append(readme_path)
    return readme_files


def has_enhanced_framework_examples(content: str) -> bool:
    """Check if README already has enhanced framework examples."""
    # Check for multiple frameworks or detailed code
    # Be more lenient - only skip if it has 3+ framework examples
    framework_count = sum(
        1
        for fw in [
            "Spring Framework",
            ".NET Framework",
            "Java Standard Library",
            "Python Standard Library",
            "Nginx",
            "Kubernetes",
            "Redis",
        ]
        if fw in content
    )

    # Skip only if it has 3+ frameworks already
    return framework_count >= 3


def has_enhanced_real_world_apps(content: str) -> bool:
    """Check if README already has enhanced real-world applications."""
    # Check for specific company names or detailed examples
    # Be more lenient - only skip if it has 5+ specific examples
    companies = [
        "Google",
        "Amazon",
        "Facebook",
        "PostgreSQL",
        "Spring",
        "Standard Libraries",
        "Database Systems",
        "Operating Systems",
        "Game Development",
        "Social Networks",
        "GPS Navigation",
        "Web Crawling",
        "Network Routing",
    ]
    company_count = sum(1 for company in companies if company in content)

    # Skip only if it has 5+ specific examples already
    return company_count >= 5


def add_framework_examples_to_readme(readme_path: Path, algorithm_name: str) -> bool:
    """Add framework examples if missing."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Check if already has enhanced examples
        if has_enhanced_framework_examples(content):
            return False

        # Check if Examples section exists (try different variations)
        has_examples = (
            "## Examples of Implementation" in content
            or "## Examples of Deployment" in content
            or "## Examples" in content
        )
        if not has_examples:
            return False

        # Get examples - try exact match, then partial, then algorithm type
        examples = EXPANDED_FRAMEWORK_EXAMPLES.get(algorithm_name, {})
        if not examples:
            # Try partial match (e.g., "heap_sort" matches "min_heap")
            algo_lower = algorithm_name.lower()
            for key, ex in EXPANDED_FRAMEWORK_EXAMPLES.items():
                if key in algo_lower or algo_lower in key:
                    examples = ex
                    break

        # Try algorithm type matching
        if not examples:
            algo_lower = algorithm_name.lower()
            if "heap" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("heap_sort", {})
            elif algo_lower == "bfs" or "breadth" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("bfs", {})
            elif algo_lower == "dfs" or "depth" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("dfs", {})
            elif "dijkstra" in algo_lower or "shortest_path" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("dijkstra", {})
            elif "hash" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("hash_table", {})
            elif "strategy" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("strategy", {})
            elif "adapter" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("adapter", {})
            elif "decorator" in algo_lower:
                examples = EXPANDED_FRAMEWORK_EXAMPLES.get("decorator", {})

        if not examples:
            return False

        # Find Examples section and enhance it (try different variations)
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
            return False

        existing_section = match.group(2)

        # Build new examples
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

        if "dotnet" in examples and ".NET Framework" not in existing_section:
            new_examples += "### .NET Framework\n\n"
            new_examples += "```csharp\n" + examples["dotnet"] + "\n```\n\n"
            new_examples += "**Purpose**: .NET Framework implements this pattern/algorithm for service architecture.\n\n"

        if new_examples:
            # Append to existing section
            content = content[: match.end(2)] + new_examples + content[match.end(2) :]
            readme_path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def add_real_world_apps_to_readme(readme_path: Path, algorithm_name: str) -> bool:
    """Add real-world applications if missing."""
    try:
        content = readme_path.read_text(encoding="utf-8")

        # Check if already has enhanced applications
        if has_enhanced_real_world_apps(content):
            return False

        # Check if Real-World Applications section exists
        if "## Real-World Applications" not in content:
            return False

        # Get applications - try exact match, then partial, then algorithm type
        applications = EXPANDED_REAL_WORLD_APPS.get(algorithm_name, [])
        if not applications:
            # Try partial match
            algo_lower = algorithm_name.lower()
            for key, apps in EXPANDED_REAL_WORLD_APPS.items():
                if key in algo_lower or algo_lower in key:
                    applications = apps
                    break

        # Try algorithm type matching
        if not applications:
            algo_lower = algorithm_name.lower()
            if "heap" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("heap_sort", [])
            elif algo_lower == "bfs" or "breadth" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("bfs", [])
            elif algo_lower == "dfs" or "depth" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("dfs", [])
            elif "dijkstra" in algo_lower or "shortest_path" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("dijkstra", [])
            elif "hash" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("hash_table", [])
            elif "strategy" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("strategy", [])
            elif "adapter" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("adapter", [])
            elif "decorator" in algo_lower:
                applications = EXPANDED_REAL_WORLD_APPS.get("decorator", [])

        if not applications:
            return False

        # Find Real-World Applications section
        rwa_pattern = r"(## Real-World Applications\s*\n\s*\n)(.*?)(?=\n##|\Z)"
        match = re.search(rwa_pattern, content, re.DOTALL)

        if not match:
            return False

        existing_section = match.group(2)

        # Build new applications
        new_apps = "\n".join(f"- {app}" for app in applications)

        # Append to existing section if it's short/generic
        if len(existing_section.strip()) < 200:  # Generic or short content
            content = (
                content[: match.end(2)]
                + "\n"
                + new_apps
                + "\n\n"
                + content[match.end(2) :]
            )
            readme_path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Execute Phase 4 enhancements."""
    print("=" * 70)
    print("Phase 4 Enhancements: Expand Framework Examples and Real-World Applications")
    print("=" * 70)

    readme_files = find_all_readme_files()
    print(f"\nFound {len(readme_files)} README files to process")

    framework_updated = 0
    rwa_updated = 0

    for i, readme_path in enumerate(readme_files, 1):
        algorithm_name = readme_path.parent.name

        if add_framework_examples_to_readme(readme_path, algorithm_name):
            framework_updated += 1

        if add_real_world_apps_to_readme(readme_path, algorithm_name):
            rwa_updated += 1

        if (framework_updated + rwa_updated) % 50 == 0 and (
            framework_updated + rwa_updated
        ) > 0:
            print(
                f"[PROGRESS] Processed {i}/{len(readme_files)} files, updated {framework_updated + rwa_updated}..."
            )

    print(f"\n[COMPLETE] Processed {len(readme_files)} files")
    print(f"Framework examples enhanced: {framework_updated} files")
    print(f"Real-world applications enhanced: {rwa_updated} files")
    print(f"Total enhancements: {framework_updated + rwa_updated} files")
    print("\nEnhancements applied:")
    print("  - Expanded framework examples to more algorithms")
    print("  - Added real-world applications with specific use cases")
    print(
        "  - Enhanced coverage for heap sort, BFS, DFS, Dijkstra, hash tables, design patterns"
    )


if __name__ == "__main__":
    main()
