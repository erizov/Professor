#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SVG flowcharts for algorithms."""

from pathlib import Path
import re

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
    else:
        return "general"


def generate_svg_flowchart(algorithm_name: str, category: str):
    """Generate optimized SVG flowchart."""
    # Escape XML special characters
    name = algorithm_name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    if category == "sorting":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500" width="400" height="500">
  <defs>
    <style>
      .box {{ fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; }}
      .diamond {{ fill: #fff3cd; stroke: #ff9800; stroke-width: 2; }}
      .start {{ fill: #d4edda; stroke: #28a745; stroke-width: 2; }}
      .end {{ fill: #f8d7da; stroke: #dc3545; stroke-width: 2; }}
      .text {{ font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }}
    </style>
  </defs>
  
  <!-- Start -->
  <rect x="150" y="20" width="100" height="40" rx="5" class="start"/>
  <text x="200" y="45" class="text">Start</text>
  
  <!-- Initialize -->
  <rect x="150" y="80" width="100" height="40" rx="5" class="box"/>
  <text x="200" y="105" class="text">Initialize</text>
  
  <!-- Arrow -->
  <line x1="200" y1="60" x2="200" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Compare -->
  <polygon points="200,140 250,180 200,220 150,180" class="diamond"/>
  <text x="200" y="185" class="text">Compare</text>
  
  <!-- Arrow -->
  <line x1="200" y1="120" x2="200" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Swap -->
  <rect x="150" y="240" width="100" height="40" rx="5" class="box"/>
  <text x="200" y="265" class="text">Swap</text>
  
  <!-- Arrow Yes -->
  <line x1="250" y1="180" x2="300" y2="180" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="180" x2="300" y2="260" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="260" x2="250" y2="260" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="280" y="175" class="text" font-size="10">Yes</text>
  
  <!-- Check sorted -->
  <polygon points="200,300 250,340 200,380 150,340" class="diamond"/>
  <text x="200" y="345" class="text">Sorted?</text>
  
  <!-- Arrow -->
  <line x1="200" y1="280" x2="200" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- End -->
  <rect x="150" y="400" width="100" height="40" rx="5" class="end"/>
  <text x="200" y="425" class="text">End</text>
  
  <!-- Arrow Yes -->
  <line x1="200" y1="380" x2="200" y2="400" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="220" y="395" class="text" font-size="10">Yes</text>
  
  <!-- Arrow No (loop back) -->
  <line x1="150" y1="340" x2="50" y2="340" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="340" x2="50" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="50" y1="200" x2="150" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="60" y="330" class="text" font-size="10">No</text>
  
  <!-- Arrowhead marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>"""
    else:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <style>
      .box {{ fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; }}
      .diamond {{ fill: #fff3cd; stroke: #ff9800; stroke-width: 2; }}
      .start {{ fill: #d4edda; stroke: #28a745; stroke-width: 2; }}
      .end {{ fill: #f8d7da; stroke: #dc3545; stroke-width: 2; }}
      .text {{ font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }}
    </style>
  </defs>
  
  <!-- Start -->
  <rect x="150" y="20" width="100" height="40" rx="5" class="start"/>
  <text x="200" y="45" class="text">Start</text>
  
  <!-- Initialize -->
  <rect x="150" y="80" width="100" height="40" rx="5" class="box"/>
  <text x="200" y="105" class="text">Initialize</text>
  
  <!-- Process -->
  <polygon points="200,140 250,180 200,220 150,180" class="diamond"/>
  <text x="200" y="185" class="text">Process?</text>
  
  <!-- Execute -->
  <rect x="150" y="240" width="100" height="40" rx="5" class="box"/>
  <text x="200" y="265" class="text">Execute</text>
  
  <!-- End -->
  <rect x="150" y="320" width="100" height="40" rx="5" class="end"/>
  <text x="200" y="345" class="text">End</text>
  
  <!-- Arrows -->
  <line x1="200" y1="60" x2="200" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="120" x2="200" y2="140" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="220" x2="200" y2="240" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="200" y1="280" x2="200" y2="320" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Arrowhead marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#333"/>
    </marker>
  </defs>
</svg>"""
    
    return svg


def optimize_svg(svg_content: str):
    """Optimize SVG by removing unnecessary whitespace."""
    # Remove extra whitespace and newlines
    svg_content = re.sub(r'\s+', ' ', svg_content)
    svg_content = re.sub(r'>\s+<', '><', svg_content)
    return svg_content.strip()


def main():
    """Main function."""
    algorithm_folders = find_all_algorithm_folders()
    
    created = 0
    skipped = 0
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Generating SVG flowcharts...\n")
    
    for algo_dir in algorithm_folders:
        vis_dir = algo_dir / "visualizations"
        if not vis_dir.exists():
            vis_dir.mkdir(parents=True, exist_ok=True)
        
        svg_path = vis_dir / "flowchart.svg"
        if svg_path.exists():
            skipped += 1
            continue
        
        category = get_algorithm_category(algo_dir)
        algorithm_name = algo_dir.name.replace("_", " ").title()
        
        svg_content = generate_svg_flowchart(algorithm_name, category)
        optimized_svg = optimize_svg(svg_content)
        
        svg_path.write_text(optimized_svg, encoding="utf-8")
        created += 1
        
        if created % 50 == 0:
            print(f"Created {created} SVG files...")
    
    print(f"\n=== Summary ===")
    print(f"Created SVG files: {created}")
    print(f"Skipped (already exists): {skipped}")
    print(f"Total: {len(algorithm_folders)}")


if __name__ == "__main__":
    main()

