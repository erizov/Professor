#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate interactive HTML version of the textbook with search and filters.
Creates a self-contained HTML file with JavaScript for filtering algorithms.
"""

import re
import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import markdown

ROOT = Path(__file__).resolve().parents[1]
TEXTBOOK_PATH = ROOT / "COMPREHENSIVE_COURSE_TEXTBOOK.md"
OUTPUT_PATH = ROOT / "COMPREHENSIVE_COURSE_TEXTBOOK.html"


def extract_algorithm_metadata() -> List[Dict]:
    """Extract metadata for all algorithms."""
    algorithms = []
    
    for semester_dir in ROOT.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
            
        semester_num = int(semester_dir.name.replace("semester_", ""))
        difficulty = "Undergraduate" if semester_num <= 8 else "Graduate"
        
        for lecture_dir in semester_dir.glob("lecture_*"):
            if not lecture_dir.is_dir():
                continue
                
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                    
                # Check if it's an algorithm folder
                has_code = (
                    (algo_dir / "algorithm.py").exists()
                    or (algo_dir / "Algorithm.java").exists()
                    or (algo_dir / "algorithm.sql").exists()
                )
                
                if not has_code:
                    continue
                
                algo_name = algo_dir.name
                rel_path = str(algo_dir.relative_to(ROOT))
                
                # Extract metadata
                metadata_file = algo_dir / "metadata.json"
                category = "Algorithm"
                if metadata_file.exists():
                    try:
                        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
                        category = metadata.get("category", "Algorithm")
                    except:
                        pass
                
                # Determine languages
                languages = []
                if (algo_dir / "algorithm.py").exists():
                    languages.append("Python")
                if (algo_dir / "Algorithm.java").exists():
                    languages.append("Java")
                if (algo_dir / "algorithm.sql").exists():
                    languages.append("SQL")
                
                algorithms.append({
                    "name": algo_name,
                    "displayName": algo_name.replace("_", " ").title(),
                    "semester": f"Semester {semester_num}",
                    "semesterNum": semester_num,
                    "lecture": lecture_dir.name.replace("_", " ").title(),
                    "category": category,
                    "difficulty": difficulty,
                    "languages": languages,
                    "path": rel_path,
                })
    
    return algorithms


def convert_markdown_to_html(markdown_content: str, algorithms: List[Dict]) -> str:
    """Convert Markdown to HTML and add data attributes for filtering."""
    # Add data attributes to algorithm sections before conversion
    # This helps with filtering later
    
    # Create a mapping of algorithm names to their metadata
    algo_map = {algo["name"]: algo for algo in algorithms}
    algo_map_display = {algo["displayName"].lower(): algo for algo in algorithms}
    
    # Find algorithm sections and add data attributes
    lines = markdown_content.split('\n')
    processed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is a heading that might match an algorithm
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            heading_text = heading_match.group(2).strip()
            heading_lower = heading_text.lower()
            
            # Try to match with algorithm names
            for algo_name, algo in algo_map.items():
                algo_name_lower = algo_name.lower().replace('_', ' ')
                display_lower = algo["displayName"].lower()
                
                # Check if heading matches algorithm
                if (algo_name_lower in heading_lower or 
                    display_lower in heading_lower or
                    heading_lower in algo_name_lower or
                    heading_lower in display_lower):
                    
                    # Add data attributes to the heading
                    data_attrs = (
                        f' data-algorithm="{algo_name}"'
                        f' data-semester="{algo["semester"]}"'
                        f' data-category="{algo["category"]}"'
                        f' data-difficulty="{algo["difficulty"]}"'
                        f' data-languages="{",".join(algo["languages"])}"'
                    )
                    line = line.replace(heading_text, heading_text + data_attrs)
                    break
        
        processed_lines.append(line)
        i += 1
    
    processed_content = '\n'.join(processed_lines)
    
    # Configure markdown extensions
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "nl2br",
        ],
        extension_configs={
            "toc": {
                "permalink": True,
            },
        },
    )
    
    html = md.convert(processed_content)
    return html


def generate_html_template(html_content: str, algorithms: List[Dict]) -> str:
    """Generate complete HTML with search and filter functionality."""
    
    # Get unique values for filters
    semesters = sorted(set(a["semester"] for a in algorithms), key=lambda x: int(x.split()[-1]))
    categories = sorted(set(a["category"] for a in algorithms))
    languages = sorted(set(lang for a in algorithms for lang in a["languages"]))
    difficulties = sorted(set(a["difficulty"] for a in algorithms))
    
    # Convert algorithms to JSON for JavaScript
    algorithms_json = json.dumps(algorithms, indent=2)
    
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Algorithms Course Textbook</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .filters {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 20px;
            z-index: 100;
        }}
        
        .filters h2 {{
            margin-bottom: 20px;
            color: #667eea;
            font-size: 1.5em;
        }}
        
        .filter-group {{
            margin-bottom: 20px;
        }}
        
        .filter-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }}
        
        .filter-input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        
        .filter-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-select {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-checkboxes {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .filter-checkbox {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .filter-checkbox input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}
        
        .filter-checkbox label {{
            margin: 0;
            cursor: pointer;
            font-weight: normal;
        }}
        
        .results-info {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }}
        
        .content {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
            margin-top: 30px;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .content h1 {{
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .content h2 {{
            font-size: 1.75em;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
        }}
        
        .content h3 {{
            font-size: 1.5em;
        }}
        
        .content code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        .content pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        .content pre code {{
            background: transparent;
            padding: 0;
            color: inherit;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        .content table th,
        .content table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        .content table th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}
        
        .content table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        .algorithm-card {{
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            transition: all 0.3s;
        }}
        
        .algorithm-card:hover {{
            border-color: #667eea;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .algorithm-card.hidden {{
            display: none;
        }}
        
        .algorithm-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        
        .algorithm-tag {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .algorithm-tag.category {{
            background: #4caf50;
        }}
        
        .algorithm-tag.language {{
            background: #ff9800;
        }}
        
        .algorithm-tag.difficulty {{
            background: #9c27b0;
        }}
        
        .clear-filters {{
            background: #f44336;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin-top: 10px;
            transition: background 0.3s;
        }}
        
        .clear-filters:hover {{
            background: #d32f2f;
        }}
        
        @media (max-width: 768px) {{
            .filters {{
                position: relative;
            }}
            
            .filter-checkboxes {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Comprehensive Algorithms Course Textbook</h1>
            <p>Interactive searchable and filterable textbook with {len(algorithms)} algorithms</p>
        </div>
        
        <div class="filters">
            <h2>🔍 Search & Filter</h2>
            
            <div class="filter-group">
                <label for="search-input">Search by Name:</label>
                <input type="text" id="search-input" class="filter-input" placeholder="Type algorithm name...">
            </div>
            
            <div class="filter-group">
                <label for="semester-filter">Semester:</label>
                <select id="semester-filter" class="filter-select">
                    <option value="">All Semesters</option>
                    {''.join(f'<option value="{s}">{s}</option>' for s in semesters)}
                </select>
            </div>
            
            <div class="filter-group">
                <label for="category-filter">Category/Type:</label>
                <select id="category-filter" class="filter-select">
                    <option value="">All Categories</option>
                    {''.join(f'<option value="{c}">{c}</option>' for c in categories)}
                </select>
            </div>
            
            <div class="filter-group">
                <label>Programming Language:</label>
                <div class="filter-checkboxes">
                    {''.join(f'''
                    <div class="filter-checkbox">
                        <input type="checkbox" id="lang-{lang.lower()}" value="{lang}" class="language-filter" checked>
                        <label for="lang-{lang.lower()}">{lang}</label>
                    </div>
                    ''' for lang in languages)}
                </div>
            </div>
            
            <div class="filter-group">
                <label>Difficulty Level:</label>
                <div class="filter-checkboxes">
                    {''.join(f'''
                    <div class="filter-checkbox">
                        <input type="checkbox" id="diff-{diff.lower()}" value="{diff}" class="difficulty-filter" checked>
                        <label for="diff-{diff.lower()}">{diff}</label>
                    </div>
                    ''' for diff in difficulties)}
                </div>
            </div>
            
            <button class="clear-filters" onclick="clearAllFilters()">Clear All Filters</button>
            
            <div class="results-info" id="results-info">
                Showing all {len(algorithms)} algorithms
            </div>
        </div>
        
        <div class="content" id="content">
            {html_content}
        </div>
    </div>
    
    <script>
        // Algorithm data
        const algorithms = {algorithms_json};
        
        // Filter elements
        const searchInput = document.getElementById('search-input');
        const semesterFilter = document.getElementById('semester-filter');
        const categoryFilter = document.getElementById('category-filter');
        const languageFilters = document.querySelectorAll('.language-filter');
        const difficultyFilters = document.querySelectorAll('.difficulty-filter');
        const resultsInfo = document.getElementById('results-info');
        const content = document.getElementById('content');
        
        // Get all algorithm sections (marked with data attributes)
        function getAlgorithmSections() {{
            const algorithmSections = new Map();
            
            // Find all elements with data-algorithm attribute
            const algoElements = content.querySelectorAll('[data-algorithm]');
            algoElements.forEach(element => {{
                const algoName = element.getAttribute('data-algorithm');
                if (algoName) {{
                    // Find the section containing this element
                    let section = element;
                    // Look for the next heading or section boundary
                    let current = element.nextElementSibling;
                    let sectionEnd = null;
                    
                    // Find where this section ends (next heading of same or higher level)
                    const level = parseInt(element.tagName.charAt(1)) || 1;
                    while (current) {{
                        if (current.tagName && current.tagName.match(/^H[1-6]$/)) {{
                            const nextLevel = parseInt(current.tagName.charAt(1));
                            if (nextLevel <= level) {{
                                sectionEnd = current;
                                break;
                            }}
                        }}
                        current = current.nextElementSibling;
                    }}
                    
                    // Create a wrapper for this section
                    if (!algorithmSections.has(algoName)) {{
                        algorithmSections.set(algoName, element);
                    }}
                }}
            }});
            
            // Also try to match by text content for headings without data attributes
            const headings = content.querySelectorAll('h1, h2, h3, h4, h5, h6');
            algorithms.forEach(algo => {{
                if (!algorithmSections.has(algo.name)) {{
                    headings.forEach(heading => {{
                        const text = heading.textContent.toLowerCase();
                        const algoName = algo.name.toLowerCase().replace(/_/g, ' ');
                        const displayName = algo.displayName.toLowerCase();
                        
                        if (text.includes(algoName) || text.includes(displayName) ||
                            algoName.includes(text) || displayName.includes(text)) {{
                            algorithmSections.set(algo.name, heading);
                        }}
                    }});
                }}
            }});
            
            return algorithmSections;
        }}
        
        // Apply filters
        function applyFilters() {{
            const searchTerm = searchInput.value.toLowerCase().trim();
            const selectedSemester = semesterFilter.value;
            const selectedCategory = categoryFilter.value;
            const selectedLanguages = Array.from(languageFilters)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            const selectedDifficulties = Array.from(difficultyFilters)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            
            let visibleCount = 0;
            const algorithmSections = getAlgorithmSections();
            
            algorithms.forEach(algo => {{
                // Check search term
                const matchesSearch = !searchTerm || 
                    algo.name.toLowerCase().includes(searchTerm) ||
                    algo.displayName.toLowerCase().includes(searchTerm);
                
                // Check semester
                const matchesSemester = !selectedSemester || algo.semester === selectedSemester;
                
                // Check category
                const matchesCategory = !selectedCategory || algo.category === selectedCategory;
                
                // Check languages
                const matchesLanguage = selectedLanguages.length === 0 ||
                    algo.languages.some(lang => selectedLanguages.includes(lang));
                
                // Check difficulty
                const matchesDifficulty = selectedDifficulties.length === 0 ||
                    selectedDifficulties.includes(algo.difficulty);
                
                const isVisible = matchesSearch && matchesSemester && matchesCategory && 
                                matchesLanguage && matchesDifficulty;
                
                // Show/hide algorithm section
                const section = algorithmSections.get(algo.name);
                if (section) {{
                    if (isVisible) {{
                        section.style.display = '';
                        // Show all siblings until next algorithm section
                        let current = section.nextElementSibling;
                        const sectionLevel = parseInt(section.tagName?.charAt(1)) || 1;
                        while (current) {{
                            if (current.tagName && current.tagName.match(/^H[1-6]$/)) {{
                                const nextLevel = parseInt(current.tagName.charAt(1));
                                if (nextLevel <= sectionLevel && current.hasAttribute('data-algorithm')) {{
                                    break;
                                }}
                            }}
                            current.style.display = '';
                            current = current.nextElementSibling;
                        }}
                        visibleCount++;
                    }} else {{
                        section.style.display = 'none';
                        // Hide all siblings until next algorithm section
                        let current = section.nextElementSibling;
                        const sectionLevel = parseInt(section.tagName?.charAt(1)) || 1;
                        while (current) {{
                            if (current.tagName && current.tagName.match(/^H[1-6]$/)) {{
                                const nextLevel = parseInt(current.tagName.charAt(1));
                                if (nextLevel <= sectionLevel && current.hasAttribute('data-algorithm')) {{
                                    break;
                                }}
                            }}
                            current.style.display = 'none';
                            current = current.nextElementSibling;
                        }}
                    }}
                }} else {{
                    // If section not found, count it as visible if it matches
                    if (isVisible) {{
                        visibleCount++;
                    }}
                }}
            }});
            
            // Update results info
            resultsInfo.textContent = `Showing ${{visibleCount}} of ${{algorithms.length}} algorithms`;
            if (visibleCount === 0) {{
                resultsInfo.style.background = '#ffebee';
                resultsInfo.style.borderLeftColor = '#f44336';
            }} else {{
                resultsInfo.style.background = '#e3f2fd';
                resultsInfo.style.borderLeftColor = '#2196f3';
            }}
        }}
        
        // Clear all filters
        function clearAllFilters() {{
            searchInput.value = '';
            semesterFilter.value = '';
            categoryFilter.value = '';
            languageFilters.forEach(cb => cb.checked = true);
            difficultyFilters.forEach(cb => cb.checked = true);
            applyFilters();
        }}
        
        // Add event listeners
        searchInput.addEventListener('input', applyFilters);
        semesterFilter.addEventListener('change', applyFilters);
        categoryFilter.addEventListener('change', applyFilters);
        languageFilters.forEach(cb => cb.addEventListener('change', applyFilters));
        difficultyFilters.forEach(cb => cb.addEventListener('change', applyFilters));
        
        // Initial filter application
        applyFilters();
    </script>
</body>
</html>"""
    
    return template


def main():
    """Generate interactive HTML textbook."""
    print("Extracting algorithm metadata...")
    algorithms = extract_algorithm_metadata()
    print(f"Found {len(algorithms)} algorithms")
    
    print("Reading textbook Markdown...")
    if not TEXTBOOK_PATH.exists():
        print(f"[ERROR] Textbook not found: {TEXTBOOK_PATH}")
        return
    
    markdown_content = TEXTBOOK_PATH.read_text(encoding="utf-8")
    
    print("Converting Markdown to HTML...")
    html_content = convert_markdown_to_html(markdown_content, algorithms)
    
    print("Generating interactive HTML...")
    html_template = generate_html_template(html_content, algorithms)
    
    print(f"Writing HTML to {OUTPUT_PATH}...")
    OUTPUT_PATH.write_text(html_template, encoding="utf-8")
    
    print("[SUCCESS] Interactive textbook generated!")
    print(f"Open {OUTPUT_PATH} in your browser to use the search and filters.")


if __name__ == "__main__":
    main()

