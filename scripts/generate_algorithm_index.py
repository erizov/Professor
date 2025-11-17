#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive algorithm index.
Creates searchable index of all algorithms with metadata.
"""

import json
from pathlib import Path
from typing import Dict, List
import re

ROOT = Path(__file__).resolve().parents[1]

def extract_algorithm_info(algo_dir: Path) -> Dict:
    """Extract algorithm information."""
    info = {
        'name': algo_dir.name,
        'path': str(algo_dir.relative_to(ROOT)),
        'semester': None,
        'lecture': None,
        'category': None,
        'complexity': {},
        'languages': [],
        'has_tests': False,
        'has_docs': False
    }
    
    # Extract semester and lecture from path
    parts = algo_dir.parts
    for i, part in enumerate(parts):
        if part.startswith('semester_'):
            info['semester'] = part
            if i + 1 < len(parts):
                info['lecture'] = parts[i + 1]
            break
    
    # Read metadata
    metadata_file = algo_dir / "metadata.json"
    if metadata_file.exists():
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            info['category'] = metadata.get('category', 'algorithm')
            info['complexity'] = {
                'time': metadata.get('time_complexity', 'N/A'),
                'space': metadata.get('space_complexity', 'N/A')
            }
        except:
            pass
    
    # Check files
    if (algo_dir / "algorithm.py").exists():
        info['languages'].append('Python')
    if (algo_dir / "Algorithm.java").exists():
        info['languages'].append('Java')
    if (algo_dir / "algorithm.sql").exists():
        info['languages'].append('SQL')
    if (algo_dir / "test_algorithm.py").exists():
        info['has_tests'] = True
    if (algo_dir / "README.md").exists():
        info['has_docs'] = True
    
    return info

def generate_index() -> Dict:
    """Generate algorithm index."""
    index = {
        'algorithms': [],
        'by_semester': {},
        'by_category': {},
        'by_language': {'Python': [], 'Java': [], 'SQL': []},
        'statistics': {
            'total': 0,
            'with_tests': 0,
            'with_docs': 0,
            'languages': {}
        }
    }
    
    # Find all algorithm directories
    for algo_dir in ROOT.rglob("*/algorithm.py"):
        algo_dir = algo_dir.parent
        if not (algo_dir / "README.md").exists():
            continue
        
        info = extract_algorithm_info(algo_dir)
        index['algorithms'].append(info)
        
        # Index by semester
        if info['semester']:
            if info['semester'] not in index['by_semester']:
                index['by_semester'][info['semester']] = []
            index['by_semester'][info['semester']].append(info['name'])
        
        # Index by category
        category = info['category'] or 'uncategorized'
        if category not in index['by_category']:
            index['by_category'][category] = []
        index['by_category'][category].append(info['name'])
        
        # Index by language
        for lang in info['languages']:
            if lang in index['by_language']:
                index['by_language'][lang].append(info['name'])
        
        # Update statistics
        index['statistics']['total'] += 1
        if info['has_tests']:
            index['statistics']['with_tests'] += 1
        if info['has_docs']:
            index['statistics']['with_docs'] += 1
        for lang in info['languages']:
            index['statistics']['languages'][lang] = index['statistics']['languages'].get(lang, 0) + 1
    
    return index

def generate_markdown_index(index: Dict) -> str:
    """Generate markdown index."""
    md = "# Algorithm Index\n\n"
    md += "Comprehensive index of all algorithms and patterns in the course.\n\n"
    
    # Statistics
    md += "## Statistics\n\n"
    stats = index['statistics']
    md += f"- **Total Algorithms**: {stats['total']}\n"
    md += f"- **With Tests**: {stats['with_tests']} ({stats['with_tests']*100//stats['total'] if stats['total'] > 0 else 0}%)\n"
    md += f"- **With Documentation**: {stats['with_docs']} ({stats['with_docs']*100//stats['total'] if stats['total'] > 0 else 0}%)\n"
    md += f"- **Languages**: {', '.join(f'{lang} ({count})' for lang, count in stats['languages'].items())}\n\n"
    
    # By Semester
    md += "## By Semester\n\n"
    for semester in sorted(index['by_semester'].keys()):
        md += f"### {semester.replace('_', ' ').title()}\n\n"
        for algo in sorted(index['by_semester'][semester]):
            md += f"- [{algo.replace('_', ' ').title()}]({next((a['path'] for a in index['algorithms'] if a['name'] == algo), '#')})\n"
        md += "\n"
    
    # By Category
    md += "## By Category\n\n"
    for category in sorted(index['by_category'].keys()):
        md += f"### {category.replace('_', ' ').title()}\n\n"
        for algo in sorted(index['by_category'][category]):
            md += f"- [{algo.replace('_', ' ').title()}]({next((a['path'] for a in index['algorithms'] if a['name'] == algo), '#')})\n"
        md += "\n"
    
    # By Language
    md += "## By Language\n\n"
    for lang in sorted(index['by_language'].keys()):
        md += f"### {lang}\n\n"
        for algo in sorted(index['by_language'][lang]):
            md += f"- [{algo.replace('_', ' ').title()}]({next((a['path'] for a in index['algorithms'] if a['name'] == algo), '#')})\n"
        md += "\n"
    
    # Full List
    md += "## Full Algorithm List\n\n"
    md += "| Algorithm | Semester | Category | Languages | Tests | Docs |\n"
    md += "|-----------|----------|----------|-----------|-------|------|\n"
    
    for algo in sorted(index['algorithms'], key=lambda x: x['name']):
        semester = algo['semester'] or 'N/A'
        category = algo['category'] or 'N/A'
        languages = ', '.join(algo['languages']) or 'N/A'
        tests = '✓' if algo['has_tests'] else '✗'
        docs = '✓' if algo['has_docs'] else '✗'
        name_link = f"[{algo['name'].replace('_', ' ').title()}]({algo['path']})"
        md += f"| {name_link} | {semester} | {category} | {languages} | {tests} | {docs} |\n"
    
    return md

def main():
    """Generate algorithm index."""
    print("Generating algorithm index...")
    index = generate_index()
    
    # Save JSON index
    json_path = ROOT / "ALGORITHM_INDEX.json"
    json_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[OK] Saved JSON index: {json_path}")
    
    # Save Markdown index
    md_path = ROOT / "ALGORITHM_INDEX.md"
    md_content = generate_markdown_index(index)
    md_path.write_text(md_content, encoding='utf-8')
    print(f"[OK] Saved Markdown index: {md_path}")
    
    # Print statistics
    stats = index['statistics']
    print(f"\nStatistics:")
    print(f"  Total algorithms: {stats['total']}")
    print(f"  With tests: {stats['with_tests']}")
    print(f"  With docs: {stats['with_docs']}")
    print(f"  Languages: {dict(stats['languages'])}")

if __name__ == "__main__":
    main()

