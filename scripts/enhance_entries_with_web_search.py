#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhance template entries with information from reputable web sources.

This script uses web search to find algorithm information from Wikipedia,
GeeksforGeeks, and other reputable sources, then updates the JSON entries.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import time

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "scripts" / "data" / "learning_template_entries.json"


def load_entries() -> List[Dict]:
    """Load existing entries."""
    if not DATA_PATH.exists():
        return []
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return data.get("entries", [])


def save_entries(entries: List[Dict]) -> None:
    """Save entries to JSON file."""
    output_data = {"entries": entries}
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def needs_enhancement(entry: Dict) -> bool:
    """Check if entry needs enhancement."""
    # Check if it's a placeholder entry
    problem = entry.get("problem", "").lower()
    intuition = entry.get("intuition", "").lower()
    
    placeholder_phrases = [
        "implements",
        "algorithm-specific",
        "fundamental algorithm",
        "solves computational problems",
    ]
    
    return any(phrase in problem or phrase in intuition for phrase in placeholder_phrases)


def get_algorithm_category_from_path(path: str) -> str:
    """Infer algorithm category from path."""
    path_lower = path.lower()
    
    if "sort" in path_lower:
        return "sorting"
    elif "search" in path_lower:
        return "searching"
    elif "tree" in path_lower or "bst" in path_lower:
        return "tree"
    elif "graph" in path_lower:
        return "graph"
    elif "hash" in path_lower:
        return "hashing"
    elif "heap" in path_lower:
        return "heap"
    elif "dp" in path_lower or "dynamic" in path_lower:
        return "dynamic_programming"
    elif "string" in path_lower:
        return "string"
    elif "sql" in path_lower or "database" in path_lower:
        return "database"
    elif "ml" in path_lower or "machine_learning" in path_lower:
        return "machine_learning"
    elif "ai" in path_lower or "artificial" in path_lower:
        return "ai"
    elif "security" in path_lower or "crypto" in path_lower:
        return "security"
    elif "concurrency" in path_lower or "thread" in path_lower:
        return "concurrency"
    elif "distributed" in path_lower:
        return "distributed"
    elif "design_pattern" in path_lower or "pattern" in path_lower:
        return "design_pattern"
    else:
        return "general"


def create_search_query(entry: Dict) -> str:
    """Create a web search query for the algorithm."""
    name = entry.get("name", "")
    category = get_algorithm_category_from_path(entry.get("path", ""))
    
    # Create focused search query
    query = f"{name} algorithm"
    if category != "general":
        query += f" {category}"
    query += " wikipedia geeksforgeeks"
    
    return query


def main():
    """Main entry point - this will be enhanced with actual web search."""
    print("Loading entries...")
    entries = load_entries()
    
    print(f"Found {len(entries)} entries")
    
    # Identify entries that need enhancement
    needs_update = [e for e in entries if needs_enhancement(e)]
    print(f"Found {len(needs_update)} entries that need enhancement")
    
    print("\nNote: This script identifies entries that need web search enhancement.")
    print("The actual web search will be performed by the AI assistant.")
    print(f"\nEntries to enhance: {len(needs_update)}")
    
    # Show sample of entries that need enhancement
    print("\nSample entries needing enhancement:")
    for i, entry in enumerate(needs_update[:10]):
        print(f"  {i+1}. {entry.get('name')} - {entry.get('path')}")
    
    if len(needs_update) > 10:
        print(f"  ... and {len(needs_update) - 10} more")


if __name__ == "__main__":
    main()

