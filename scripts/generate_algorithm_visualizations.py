#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate visualizations for all algorithms."""

from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]


def find_all_algorithm_folders():
    """Find all algorithm folders."""
    algorithm_folders = []
    
    for semester_dir in sorted(ROOT.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if algo_dir.is_dir() and (algo_dir / "README.md").exists():
                    algorithm_folders.append(algo_dir)
    
    return algorithm_folders


def get_algorithm_name(algo_dir: Path):
    """Get algorithm name from directory or README."""
    # Try to get from README title
    readme_path = algo_dir / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    
    # Fallback to directory name
    return algo_dir.name.replace("_", " ").title()


def get_algorithm_category(algo_dir: Path):
    """Determine algorithm category from path."""
    path_str = str(algo_dir)
    
    if "sorting" in path_str.lower():
        return "sorting"
    elif "search" in path_str.lower():
        return "searching"
    elif "tree" in path_str.lower():
        return "tree"
    elif "graph" in path_str.lower():
        return "graph"
    elif "dynamic" in path_str.lower() or "dp" in path_str.lower():
        return "dynamic_programming"
    elif "pattern" in path_str.lower():
        return "design_pattern"
    elif "ml" in path_str.lower() or "machine" in path_str.lower():
        return "machine_learning"
    else:
        return "general"


def generate_ascii_flowchart(algorithm_name: str, category: str):
    """Generate ASCII flowchart for algorithm."""
    if category == "sorting":
        return f"""
```
{algorithm_name} Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Initialize  │
│   array     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Compare    ├──────┐
│  elements?  │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│   Swap if   │      │
│  needed     │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│   Sorted?   │
└──────┬──────┘
       │ No
       └──────┐
              │
       Yes    │
       │      │
       ▼      ▼
┌─────────────┐
│    End      │
└─────────────┘
```
"""
    elif category == "searching":
        return f"""
```
{algorithm_name} Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Get search │
│    target   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Check     ├──────┐
│  current   │      │
│  element?  │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│   Move to   │      │
│   next      │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│   Found?    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```
"""
    elif category == "tree":
        return f"""
```
{algorithm_name} Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│    root     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Node       ├──────┐
│  exists?    │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Process    │      │
│   node      │      │
└──────┬──────┘      │
       │             │
       ▼             │
┌─────────────┐      │
│  Traverse   │      │
│  children   │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```
"""
    else:
        return f"""
```
{algorithm_name} Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```
"""


def generate_ascii_step_by_step(algorithm_name: str, category: str):
    """Generate ASCII step-by-step execution diagram."""
    if category == "sorting":
        return f"""
```
{algorithm_name} Step-by-Step Execution:

Input: [5, 3, 2, 8, 1]

Pass 1:
[5, 3, 2, 8, 1]
 ↑  ↑
Swap: 5 > 3
[3, 5, 2, 8, 1]
    ↑  ↑
Swap: 5 > 2
[3, 2, 5, 8, 1]
       ↑  ↑
No swap: 5 < 8
[3, 2, 5, 8, 1]
          ↑  ↑
Swap: 8 > 1
Result: [3, 2, 5, 1, 8]

Pass 2:
[3, 2, 5, 1, 8]
 ↑  ↑
Swap: 3 > 2
[2, 3, 5, 1, 8]
    ↑  ↑
No swap: 3 < 5
[2, 3, 5, 1, 8]
       ↑  ↑
Swap: 5 > 1
Result: [2, 3, 1, 5, 8]

Final: [1, 2, 3, 5, 8]
```
"""
    elif category == "searching":
        return f"""
```
{algorithm_name} Step-by-Step Execution:

Array: [1, 3, 5, 7, 9, 11]
Target: 7

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
"""
    else:
        return f"""
```
{algorithm_name} Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```
"""


def generate_mermaid_flowchart(algorithm_name: str, category: str):
    """Generate Mermaid flowchart."""
    if category == "sorting":
        return """
```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize array]
    Init --> Compare{Compare elements}
    Compare -->|Yes| Swap[Swap if needed]
    Swap --> Check{More elements?}
    Check -->|Yes| Compare
    Check -->|No| Sorted{Array sorted?}
    Sorted -->|No| Compare
    Sorted -->|Yes| End([End])
```
"""
    elif category == "searching":
        return """
```mermaid
flowchart TD
    Start([Start]) --> Init[Get search target]
    Init --> Check{Check current element}
    Check -->|Match| Found([Found])
    Check -->|No match| Next[Move to next]
    Next --> More{More elements?}
    More -->|Yes| Check
    More -->|No| NotFound([Not Found])
```
"""
    else:
        return """
```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```
"""


def create_visualizations_folder(algo_dir: Path):
    """Create visualizations folder if it doesn't exist."""
    vis_dir = algo_dir / "visualizations"
    vis_dir.mkdir(exist_ok=True)
    return vis_dir


def update_readme_with_visualizations(readme_path: Path, algorithm_name: str, category: str, algo_dir: Path):
    """Update README with visualization sections."""
    content = readme_path.read_text(encoding="utf-8")
    
    # Check if visualization section already exists
    if "## Algorithm Visualization" in content or "## Visualizations" in content:
        # Update existing section with SVG link if missing
        vis_dir = algo_dir / "visualizations"
        if (vis_dir / "flowchart.svg").exists() and "flowchart.svg" not in content:
            relative_svg = (vis_dir / "flowchart.svg").relative_to(ROOT)
            svg_link = f"\n### Flowchart (SVG)\n\n![{algorithm_name} Flowchart]({relative_svg.as_posix()})\n\n"
            # Insert SVG link after ASCII flowchart
            pattern = r"(### Flowchart \(ASCII\).*?\n```\n)"
            new_content = re.sub(pattern, r"\1" + svg_link, content, flags=re.DOTALL)
            if new_content != content:
                readme_path.write_text(new_content, encoding="utf-8")
                return True
        return False
    
    # Generate visualizations
    ascii_flowchart = generate_ascii_flowchart(algorithm_name, category)
    ascii_steps = generate_ascii_step_by_step(algorithm_name, category)
    mermaid_flowchart = generate_mermaid_flowchart(algorithm_name, category)
    
    # Check if SVG exists
    vis_dir = algo_dir / "visualizations"
    svg_section = ""
    if (vis_dir / "flowchart.svg").exists():
        relative_svg = (vis_dir / "flowchart.svg").relative_to(ROOT)
        svg_section = f"""
### Flowchart (SVG)

![{algorithm_name} Flowchart]({relative_svg.as_posix()})

"""
    
    # Create visualization section
    visualization_section = f"""
## Algorithm Visualization

### Flowchart (ASCII)

{ascii_flowchart}
{svg_section}### Step-by-Step Execution

{ascii_steps}

### Interactive Flowchart (Mermaid)

{mermaid_flowchart}

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
"""
    
    # Find insertion point (after Code Files section or after title)
    if "## Code Files" in content:
        # Insert after Code Files section
        # Find the end of Code Files section (after the last link)
        code_files_match = re.search(r"(## Code Files\n\n.*?\n\n)", content, re.DOTALL)
        if code_files_match:
            insert_pos = code_files_match.end()
            new_content = content[:insert_pos] + visualization_section + content[insert_pos:]
        else:
            # Try to find after Code Files header
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.strip() == "## Code Files":
                    # Find the end of the section (empty line after links)
                    for j in range(i + 1, min(i + 20, len(lines))):
                        if lines[j].strip() == "" and j > i + 3:
                            insert_pos = j + 1
                            lines.insert(insert_pos, visualization_section)
                            new_content = "\n".join(lines)
                            break
                    else:
                        # Fallback: insert after Code Files header
                        lines.insert(i + 1, visualization_section)
                        new_content = "\n".join(lines)
                    break
            else:
                new_content = content
    else:
        # Insert after title
        lines = content.split("\n")
        insert_pos = 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith("#"):
                insert_pos = i
                break
            if i > 5:
                insert_pos = i
                break
        
        lines.insert(insert_pos, visualization_section)
        new_content = "\n".join(lines)
    
    if new_content != content:
        readme_path.write_text(new_content, encoding="utf-8")
        return True
    
    return False


def main():
    """Main function."""
    algorithm_folders = find_all_algorithm_folders()
    
    created_folders = 0
    updated_readmes = 0
    skipped = 0
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Creating visualizations...\n")
    
    for algo_dir in algorithm_folders:
        # Create visualizations folder
        vis_dir = create_visualizations_folder(algo_dir)
        if vis_dir.exists():
            created_folders += 1
        
        # Update README with visualizations
        readme_path = algo_dir / "README.md"
        algorithm_name = get_algorithm_name(algo_dir)
        category = get_algorithm_category(algo_dir)
        
        if update_readme_with_visualizations(readme_path, algorithm_name, category, algo_dir):
            updated_readmes += 1
            if updated_readmes % 50 == 0:
                print(f"Updated {updated_readmes} README files...")
        else:
            skipped += 1
    
    print(f"\n=== Summary ===")
    print(f"Created visualization folders: {created_folders}")
    print(f"Updated README files: {updated_readmes}")
    print(f"Skipped (already has visualizations): {skipped}")
    print(f"Total: {len(algorithm_folders)}")


if __name__ == "__main__":
    main()

