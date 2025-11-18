#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch algorithm descriptions from Wikipedia and update README files.

This script uses web search to get algorithm descriptions for algorithms
not yet in our database.
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


def get_wikipedia_url(algorithm_name: str) -> str:
    """Convert algorithm name to Wikipedia URL format."""
    # Convert snake_case to Title Case
    words = algorithm_name.split('_')
    title = '_'.join(word.capitalize() for word in words)
    return f"https://en.wikipedia.org/wiki/{title}"


def create_readme_from_template(algorithm_name: str, 
                                description: str = None) -> str:
    """Create README content from template."""
    title = algorithm_name.replace('_', ' ').title()
    wiki_url = get_wikipedia_url(algorithm_name)
    
    if description:
        desc_text = description
    else:
        desc_text = f"""{title} is a fundamental algorithm in computer science. 
This algorithm is used to solve specific computational problems efficiently. 
Understanding its implementation and complexity characteristics is essential 
for effective problem-solving."""
    
    readme = f"""# {title}

**Category**: Algorithm

## Overview

{desc_text}

## Description

{title} addresses specific computational challenges in [domain]. This technique 
is applied in various domains to solve problems efficiently.

## How It Works

[Algorithm description to be added from Wikipedia or other sources]

## Complexity Analysis

- **Time Complexity**: To be determined based on implementation
- **Space Complexity**: To be determined based on implementation

## Use Cases

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and 
performance analysis.

## References

- Wikipedia: [{title}]({wiki_url})
- Additional resources available in academic literature and algorithm textbooks

## Examples

Run the algorithm with:
```bash
python algorithm.py
```

## Learning Objectives

By studying this algorithm, you will learn:
1. The fundamental approach and logic
2. Time and space complexity analysis
3. When to use this algorithm vs alternatives
4. Implementation details and optimizations
"""
    return readme


def find_algorithms_needing_descriptions() -> List[Path]:
    """Find algorithm folders that need better descriptions."""
    base_path = Path('.')
    algorithm_folders = []
    
    for semester_dir in base_path.glob('semester_*'):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ['__pycache__', '.git']):
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if 'lecture_' not in lecture_dir.name:
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith('lecture_'):
                    continue
                if any(x in algo_dir.name for x in ['__pycache__', '.git']):
                    continue
                
                readme_path = algo_dir / 'README.md'
                if readme_path.exists():
                    content = readme_path.read_text(encoding='utf-8')
                    # Check if it has placeholder content
                    if '[describe use case]' in content or '[Use case 1]' in content or '[Algorithm description to be added' in content:
                        algorithm_folders.append(algo_dir)
    
    return sorted(algorithm_folders)


def update_readme_with_web_info(readme_path: Path, 
                                algorithm_name: str,
                                web_description: str = None) -> bool:
    """Update README with information from web search."""
    if web_description:
        # We have web description, update the README
        content = readme_path.read_text(encoding='utf-8')
        
        # Replace placeholder descriptions
        if '[Algorithm description to be added' in content:
            # Update the "How It Works" section
            content = re.sub(
                r'## How It Works\s+\[Algorithm description to be added.*?\]',
                f'## How It Works\n\n{web_description}',
                content,
                flags=re.DOTALL
            )
            readme_path.write_text(content, encoding='utf-8')
            return True
    
    return False


def main() -> None:
    """Main function."""
    print("Finding algorithms needing descriptions...")
    algorithm_folders = find_algorithms_needing_descriptions()
    print(f"Found {len(algorithm_folders)} algorithms needing descriptions\n")
    
    # For now, just report what needs to be done
    # In a full implementation, we would use web_search here
    print("Algorithms that need Wikipedia descriptions:")
    for i, algo_folder in enumerate(algorithm_folders[:50], 1):
        print(f"  {i}. {algo_folder.name}")
    
    if len(algorithm_folders) > 50:
        print(f"  ... and {len(algorithm_folders) - 50} more")
    
    print(f"\nTotal: {len(algorithm_folders)} algorithms need descriptions")
    print("\nNote: Use web_search tool to fetch descriptions from Wikipedia")
    print("      for each algorithm and update README files accordingly.")


if __name__ == "__main__":
    main()

