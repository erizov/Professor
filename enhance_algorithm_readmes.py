#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to enhance all algorithm README files with:
1. Introduction and short description
2. "Often Used Together With" section
3. "Do Not Confuse With" section
4. "Examples of Implementation" section (Spring, J2EE, .NET, Docker, Kubernetes, Kafka, etc.)
"""

import os
from pathlib import Path
from typing import Dict, List
import json


# Mapping of algorithm categories to related algorithms and frameworks
RELATED_ALGORITHMS = {
    "sorting": ["quick_sort", "merge_sort", "heap_sort", "insertion_sort"],
    "searching": ["binary_search", "linear_search", "hash_table"],
    "trees": ["bst", "avl_tree", "red_black_tree", "b_tree"],
    "graphs": ["dfs", "bfs", "dijkstra", "bellman_ford"],
    "dp": ["fibonacci", "knapsack", "lcs", "edit_distance"],
    "patterns": ["factory", "singleton", "observer", "strategy"],
    "ml": ["linear_regression", "logistic_regression", "knn", "svm"],
}

# Framework/technology examples by category
FRAMEWORK_EXAMPLES = {
    "sorting": {
        "spring": "Spring Data JPA uses sorting for query results (Sort.by())",
        "j2ee": "J2EE Collections.sort() for enterprise data processing",
        "docker": "Docker image layers use topological sorting",
        "kubernetes": "Kubernetes pod scheduling uses priority-based sorting",
        "kafka": "Kafka partition ordering ensures message sequence",
    },
    "searching": {
        "spring": "Spring Data repositories use binary search for indexed queries",
        "j2ee": "J2EE EntityManager.find() uses hash-based search",
        "docker": "Docker registry uses search algorithms for image lookup",
        "kubernetes": "Kubernetes API server uses search for resource discovery",
        "kafka": "Kafka consumer groups use search for partition assignment",
    },
    "trees": {
        "spring": "Spring BeanFactory uses tree structure for dependency injection",
        "j2ee": "J2EE JNDI uses tree structure for naming services",
        "docker": "Docker filesystem layers form a tree structure",
        "kubernetes": "Kubernetes resource hierarchy is tree-based",
        "kafka": "Kafka topic partitions use tree structures for routing",
    },
    "graphs": {
        "spring": "Spring dependency graph for bean initialization",
        "j2ee": "J2EE application dependency graph",
        "docker": "Docker container network graph",
        "kubernetes": "Kubernetes service mesh uses graph algorithms",
        "kafka": "Kafka consumer group rebalancing uses graph algorithms",
    },
    "patterns": {
        "spring": "Spring Framework extensively uses design patterns (Factory, Singleton, Proxy)",
        "j2ee": "J2EE patterns (DAO, Service Locator, MVC)",
        ".net": ".NET Core uses patterns (Dependency Injection, Repository)",
        "docker": "Docker uses patterns for container orchestration",
        "kubernetes": "Kubernetes controllers use Observer and Strategy patterns",
    },
    "ml": {
        "spring": "Spring AI integration for ML model serving",
        ".net": ".NET ML.NET for machine learning",
        "docker": "Docker containers for ML model deployment",
        "kubernetes": "Kubernetes for ML model scaling and serving",
        "kafka": "Kafka Streams for real-time ML feature processing",
    },
}


def get_algorithm_category(algorithm_name: str, lecture_path: str) -> str:
    """Determine algorithm category from name and path."""
    algorithm_name_lower = algorithm_name.lower()
    lecture_lower = lecture_path.lower()
    
    if "sort" in algorithm_name_lower or "sorting" in lecture_lower:
        return "sorting"
    elif "search" in algorithm_name_lower or "searching" in lecture_lower:
        return "searching"
    elif "tree" in algorithm_name_lower or "trees" in lecture_lower:
        return "trees"
    elif "graph" in algorithm_name_lower or "graph" in lecture_lower:
        return "graphs"
    elif "dp" in lecture_lower or "dynamic" in lecture_lower:
        return "dp"
    elif "pattern" in lecture_lower:
        return "patterns"
    elif "ml" in lecture_lower or "machine" in lecture_lower or "clustering" in lecture_lower:
        return "ml"
    return "general"


def get_confusion_pairs(algorithm_name: str, category: str) -> List[str]:
    """Get algorithms that are commonly confused with this one."""
    confusion_map = {
        "bubble_sort": ["selection_sort", "insertion_sort"],
        "quick_sort": ["merge_sort", "heap_sort"],
        "merge_sort": ["quick_sort", "heap_sort"],
        "binary_search": ["linear_search", "jump_search"],
        "dfs": ["bfs"],
        "bfs": ["dfs"],
        "dijkstra": ["bellman_ford", "floyd_warshall"],
        "avl_tree": ["red_black_tree", "bst"],
        "singleton": ["factory", "builder"],
        "factory": ["abstract_factory", "builder"],
        "observer": ["pub_sub", "mediator"],
        "strategy": ["state", "template_method"],
    }
    return confusion_map.get(algorithm_name, [])


def generate_introduction(algorithm_name: str, metadata: Dict) -> str:
    """Generate introduction section."""
    name_formatted = algorithm_name.replace("_", " ").title()
    description = metadata.get("description", f"{name_formatted} is a fundamental algorithm.")
    
    intro = f"""## Introduction

{name_formatted} is {description.lower()}

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding {name_formatted} is essential for building performant and scalable applications.

### Short Description

{description}

**Key Characteristics:**
- **Time Complexity**: {metadata.get('time_complexity', 'Varies')}
- **Space Complexity**: {metadata.get('space_complexity', 'Varies')}
- **Stability**: {metadata.get('stability', 'N/A')}
- **Best Use Case**: {metadata.get('best_use_case', 'General purpose')}
"""
    return intro


def generate_often_used_together(algorithm_name: str, category: str) -> str:
    """Generate 'Often Used Together With' section."""
    related = RELATED_ALGORITHMS.get(category, [])
    
    if not related:
        return ""
    
    section = "## Often Used Together With\n\n"
    section += f"{algorithm_name.replace('_', ' ').title()} is commonly used in combination with:\n\n"
    
    for related_alg in related:
        if related_alg != algorithm_name:
            section += f"- **{related_alg.replace('_', ' ').title()}**: Often combined for comprehensive solutions\n"
    
    section += "\n**Common Combinations:**\n"
    section += f"- Used together in production systems for optimal performance\n"
    section += f"- Complementary algorithms that solve related problems\n"
    section += f"- Often part of larger algorithmic frameworks\n"
    
    return section


def generate_do_not_confuse(algorithm_name: str, category: str) -> str:
    """Generate 'Do Not Confuse With' section."""
    confusion_pairs = get_confusion_pairs(algorithm_name, category)
    
    if not confusion_pairs:
        return ""
    
    section = "## Do Not Confuse With\n\n"
    section += f"**{algorithm_name.replace('_', ' ').title()}** should not be confused with:\n\n"
    
    for confused_with in confusion_pairs:
        section += f"- **{confused_with.replace('_', ' ').title()}**: "
        section += f"Different approach/use case, though related\n"
    
    section += "\n**Key Differences:**\n"
    section += "- Each algorithm has distinct characteristics and use cases\n"
    section += "- Understanding the differences is crucial for correct application\n"
    section += "- Similar names don't imply similar implementations\n"
    
    return section


def generate_implementation_examples(algorithm_name: str, category: str) -> str:
    """Generate 'Examples of Implementation' section."""
    examples = FRAMEWORK_EXAMPLES.get(category, {})
    
    section = "## Examples of Implementation\n\n"
    section += "This algorithm is implemented in various frameworks and technologies:\n\n"
    
    if "spring" in examples:
        section += f"### Spring Framework\n{examples['spring']}\n\n"
    
    if "j2ee" in examples:
        section += f"### J2EE (Java Enterprise Edition)\n{examples['j2ee']}\n\n"
    
    if ".net" in examples:
        section += f"### .NET Framework\n{examples['.net']}\n\n"
    
    if "docker" in examples:
        section += f"### Docker\n{examples['docker']}\n\n"
    
    if "kubernetes" in examples:
        section += f"### Kubernetes\n{examples['kubernetes']}\n\n"
    
    if "kafka" in examples:
        section += f"### Apache Kafka\n{examples['kafka']}\n\n"
    
    section += "**Real-World Applications:**\n"
    section += "- Production systems use these implementations for scalability\n"
    section += "- Enterprise frameworks provide optimized versions\n"
    section += "- Cloud platforms integrate these algorithms for performance\n"
    
    return section


def enhance_readme(readme_path: Path, algorithm_name: str, lecture_path: str) -> None:
    """Enhance a single README file."""
    try:
        # Read metadata if available
        metadata_path = readme_path.parent / "metadata.json"
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # Read existing README
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = f"# {algorithm_name.replace('_', ' ').title()}\n\n"
        
        # Determine category
        category = get_algorithm_category(algorithm_name, lecture_path)
        
        # Generate new sections
        intro = generate_introduction(algorithm_name, metadata)
        often_used = generate_often_used_together(algorithm_name, category)
        do_not_confuse = generate_do_not_confuse(algorithm_name, category)
        examples = generate_implementation_examples(algorithm_name, category)
        
        # Check if sections already exist
        if "## Introduction" not in content:
            # Insert after title
            lines = content.split('\n')
            insert_idx = 1
            for i, line in enumerate(lines):
                if line.startswith('#') and i > 0:
                    insert_idx = i + 1
                    break
            
            new_content = '\n'.join(lines[:insert_idx]) + '\n\n' + intro
            if lines[insert_idx:]:
                new_content += '\n' + '\n'.join(lines[insert_idx:])
            content = new_content
        
        # Append new sections if not present
        if "## Often Used Together With" not in content:
            content += "\n\n" + often_used
        
        if "## Do Not Confuse With" not in content:
            content += "\n\n" + do_not_confuse
        
        if "## Examples of Implementation" not in content:
            content += "\n\n" + examples
        
        # Write back
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Enhanced: {readme_path}")
    
    except Exception as e:
        print(f"Error enhancing {readme_path}: {e}")


def main():
    """Main function to enhance all README files."""
    base_path = Path(".")
    
    # Find all algorithm directories
    algorithm_dirs = []
    for semester_dir in base_path.glob("semester_*/lecture_*/*"):
        if semester_dir.is_dir() and (semester_dir / "algorithm.py").exists():
            algorithm_dirs.append(semester_dir)
    
    print(f"Found {len(algorithm_dirs)} algorithm directories")
    
    for alg_dir in algorithm_dirs:
        algorithm_name = alg_dir.name
        lecture_path = str(alg_dir.parent)
        readme_path = alg_dir / "README.md"
        
        enhance_readme(readme_path, algorithm_name, lecture_path)
    
    print(f"\nEnhanced {len(algorithm_dirs)} README files")


if __name__ == "__main__":
    main()

