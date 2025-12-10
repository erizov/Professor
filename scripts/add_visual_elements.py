#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.2: Add Visual Elements to algorithm descriptions:
- Add Mermaid flowcharts (render on GitHub)
- Improve visual formatting with better structure
- Add visual separators
- Enhance code block formatting
"""

import sys
import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def generate_mermaid_flowchart(algorithm_name: str, category: str) -> str:
    """Generate Mermaid flowchart for algorithm."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Algorithm-specific flowcharts
    flowcharts = {
        'bubble_sort': r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize array]
    Init --> Loop1[For i = 0 to n-1]
    Loop1 --> Loop2[For j = 0 to n-i-2]
    Loop2 --> Compare{Compare arr[j] and arr[j+1]}
    Compare -->|arr[j] > arr[j+1]| Swap[Swap elements]
    Compare -->|arr[j] <= arr[j+1]| Next[Next iteration]
    Swap --> Next
    Next --> Check{More elements?}
    Check -->|Yes| Loop2
    Check -->|No| Sorted{Array sorted?}
    Sorted -->|No| Loop1
    Sorted -->|Yes| End([End])
```""",
        'quick_sort': r"""```mermaid
flowchart TD
    Start([Start]) --> Check{Base case?}
    Check -->|Yes| End([End])
    Check -->|No| Pivot[Choose pivot]
    Pivot --> Partition[Partition array]
    Partition --> Left[Recursively sort left]
    Partition --> Right[Recursively sort right]
    Left --> Merge[Merge results]
    Right --> Merge
    Merge --> End
```""",
        'binary_search': r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Set left=0, right=n-1]
    Init --> Loop{left <= right?}
    Loop -->|No| NotFound[Return -1]
    Loop -->|Yes| Mid[Calculate mid]
    Mid --> Compare{Compare arr[mid] with target}
    Compare -->|Equal| Found[Return mid]
    Compare -->|arr[mid] > target| Left[Set right = mid-1]
    Compare -->|arr[mid] < target| Right[Set left = mid+1]
    Left --> Loop
    Right --> Loop
    Found --> End([End])
    NotFound --> End
```""",
        'merge_sort': r"""```mermaid
flowchart TD
    Start([Start]) --> Check{Base case?}
    Check -->|Yes| End([End])
    Check -->|No| Split[Split array in half]
    Split --> Left[Recursively sort left half]
    Split --> Right[Recursively sort right half]
    Left --> Merge[Merge sorted halves]
    Right --> Merge
    Merge --> End
```""",
        'dijkstra': r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize distances]
    Init --> Select[Select unvisited node with min distance]
    Select --> Mark[Mark as visited]
    Mark --> Update[Update distances to neighbors]
    Update --> Check{All nodes visited?}
    Check -->|No| Select
    Check -->|Yes| End([End])
```""",
        'fibonacci': r"""```mermaid
flowchart TD
    Start([Start]) --> Check{Base case?}
    Check -->|n <= 1| Return[Return n]
    Check -->|No| Memo{In memo?}
    Memo -->|Yes| ReturnMemo[Return memo[n]]
    Memo -->|No| Calc[Calculate F(n-1) + F(n-2)]
    Calc --> Store[Store in memo]
    Store --> ReturnMemo
    Return --> End([End])
    ReturnMemo --> End
```"""
    }
    
    # Check for specific algorithm
    for key, flowchart in flowcharts.items():
        if key in name_lower:
            return flowchart
    
    # Generic flowchart based on category
    if category == 'Sorting':
        return r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process[Process elements]
    Process --> Compare{Compare elements}
    Compare -->|Swap needed| Swap[Swap elements]
    Compare -->|No swap| Next[Next iteration]
    Swap --> Next
    Next --> Check{All processed?}
    Check -->|No| Process
    Check -->|Yes| End([End])
```"""
    elif category == 'Graph Algorithms':
        return r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize graph]
    Init --> Select[Select starting node]
    Select --> Process[Process node]
    Process --> Visit[Visit neighbors]
    Visit --> Update[Update state]
    Update --> Check{More nodes?}
    Check -->|Yes| Select
    Check -->|No| End([End])
```"""
    elif category == 'Dynamic Programming':
        return r"""```mermaid
flowchart TD
    Start([Start]) --> Check{Base case?}
    Check -->|Yes| Return[Return base value]
    Check -->|No| Memo{In memo?}
    Memo -->|Yes| ReturnMemo[Return memo value]
    Memo -->|No| Solve[Solve subproblem]
    Solve --> Store[Store in memo]
    Store --> ReturnMemo
    Return --> End([End])
    ReturnMemo --> End
```"""
    else:
        return r"""```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize]
    Init --> Process[Process data]
    Process --> Check{Condition?}
    Check -->|Yes| Action[Execute action]
    Check -->|No| End([End])
    Action --> Process
```"""


def add_visual_separators(content: str) -> str:
    """Add visual separators between sections."""
    # Add horizontal rule before major sections (but not first one)
    sections_to_separate = [
        '## 🎯 Try It Yourself',
        '## ✏️ Practice Exercise',
        '## ✅ Check Your Understanding',
        '## Common Mistakes',
        '## Recommended Literature'
    ]
    
    for section in sections_to_separate:
        if section in content:
            # Add separator before section (if not already there)
            pattern = f'\\n{section}'
            replacement = f'\n\n---\n\n{section}'
            if f'\n---\n\n{section}' not in content:
                content = re.sub(pattern, replacement, content)
    
    return content


def improve_code_formatting(content: str) -> str:
    """Improve code block formatting."""
    # Ensure code blocks have proper language tags
    # Find code blocks without language tags
    pattern = r'```\n(def |class |import |from |# )'
    replacement = r'```python\n\1'
    content = re.sub(pattern, replacement, content)
    
    return content


def add_visual_flowchart(content: str, algorithm_name: str, category: str) -> str:
    """Add Mermaid flowchart if not present."""
    # Check if Mermaid flowchart already exists
    if '```mermaid' in content:
        return content
    
    # Find where to insert (after Quick Summary or Key Insight)
    insert_positions = [
        ('## 💡 Key Insight', 'after'),
        ('## 📋 Quick Summary', 'after'),
        ('## Algorithm Complexity', 'before')
    ]
    
    flowchart = generate_mermaid_flowchart(algorithm_name, category)
    
    for section, position in insert_positions:
        if section in content:
            pos = content.find(section)
            if position == 'after':
                # Find end of section
                next_section = content.find('\n## ', pos + len(section))
                if next_section != -1:
                    # Insert before next section
                    content = content[:next_section] + '\n\n## 📊 Visual Flowchart\n\n' + flowchart + '\n\n' + content[next_section:]
                else:
                    # Insert at end
                    content = content + '\n\n## 📊 Visual Flowchart\n\n' + flowchart + '\n'
                return content
            else:
                # Insert before section
                content = content[:pos] + '\n## 📊 Visual Flowchart\n\n' + flowchart + '\n\n' + content[pos:]
                return content
    
    # If no good position found, add after title
    if content.startswith('#'):
        first_section = content.find('\n## ')
        if first_section != -1:
            content = content[:first_section] + '\n\n## 📊 Visual Flowchart\n\n' + flowchart + '\n\n' + content[first_section:]
        else:
            content = content + '\n\n## 📊 Visual Flowchart\n\n' + flowchart + '\n'
    
    return content


def enhance_visual_formatting(content: str) -> str:
    """Enhance overall visual formatting."""
    # Add note about Mermaid rendering
    if '```mermaid' in content and 'Mermaid diagrams are rendered' not in content:
        mermaid_pos = content.find('```mermaid')
        if mermaid_pos != -1:
            # Find end of mermaid block
            end_pos = content.find('```', mermaid_pos + 10)
            if end_pos != -1:
                note = '\n\n> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.\n'
                content = content[:end_pos + 3] + note + content[end_pos + 3:]
    
    return content


def improve_md_file(md_file: Path) -> bool:
    """Add visual elements to a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Get category
        metadata_path = algorithm_folder / "metadata.json"
        category = "Algorithms"
        if metadata_path.exists():
            try:
                import json
                metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
                if metadata.get('category'):
                    category = metadata['category']
            except:
                pass
        
        # Apply visual improvements
        content = add_visual_flowchart(content, algorithm_name, category)
        content = add_visual_separators(content)
        content = improve_code_formatting(content)
        content = enhance_visual_formatting(content)
        
        md_file.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"  [ERROR] {md_file.name}: {e}")
        return False


def find_all_md_files() -> list:
    """Find all algorithm MD files."""
    md_files = []
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/school.*.md"):
        md_files.append(md_file)
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/univer.*.md"):
        md_files.append(md_file)
    
    return sorted(md_files)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("PHASE 2.2: ADDING VISUAL ELEMENTS")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nAdding:")
    print("  - Mermaid flowcharts (render on GitHub)")
    print("  - Visual separators between sections")
    print("  - Improved code block formatting")
    print("  - Enhanced visual structure")
    
    improved = 0
    errors = 0
    
    for i, md_file in enumerate(md_files, 1):
        if improve_md_file(md_file):
            improved += 1
        else:
            errors += 1
        
        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} ({i/len(md_files)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"Improved: {improved}/{len(md_files)} files")
    print(f"Errors: {errors}")
    print(f"{'='*70}")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

