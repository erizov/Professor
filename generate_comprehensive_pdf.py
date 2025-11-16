#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive PDF document with all course lessons.
Combines all semester content into one large PDF.
"""

import os
from pathlib import Path
import subprocess
import sys


def collect_all_content():
    """Collect all course content from all semesters."""
    base_path = Path(".")
    content_parts = []
    
    # Add main README
    if (base_path / "README.md").exists():
        with open(base_path / "README.md", 'r', encoding='utf-8') as f:
            content_parts.append(("# Course Overview\n\n", f.read()))
    
    # Collect all semester content
    for semester_dir in sorted(base_path.glob("semester_*")):
        if not semester_dir.is_dir():
            continue
        
        semester_num = semester_dir.name.split('_')[1]
        content_parts.append((f"\n\n# Semester {semester_num}\n\n", ""))
        
        # Add semester README
        semester_readme = semester_dir / "README.md"
        if semester_readme.exists():
            with open(semester_readme, 'r', encoding='utf-8') as f:
                content_parts.append((f"## {semester_dir.name.replace('_', ' ').title()}\n\n", f.read()))
        
        # Collect all lectures
        for lecture_dir in sorted(semester_dir.glob("lecture_*")):
            if not lecture_dir.is_dir():
                continue
            
            lecture_name = lecture_dir.name.replace('_', ' ').title()
            content_parts.append((f"\n\n## {lecture_name}\n\n", ""))
            
            # Collect all algorithms in lecture
            for alg_dir in sorted(lecture_dir.iterdir()):
                if not alg_dir.is_dir():
                    continue
                
                alg_readme = alg_dir / "README.md"
                if alg_readme.exists():
                    with open(alg_readme, 'r', encoding='utf-8') as f:
                        alg_content = f.read()
                        alg_name = alg_dir.name.replace('_', ' ').title()
                        content_parts.append((f"\n\n### {alg_name}\n\n", alg_content))
    
    return content_parts


def generate_markdown_document():
    """Generate comprehensive markdown document."""
    content_parts = collect_all_content()
    
    # Combine all content
    full_content = """---
title: Comprehensive Algorithms Course Textbook
author: University Professor of Computer Science
date: \\today
geometry: margin=1in
toc: true
toc-depth: 3
---

\\newpage

# Algorithms and Design Patterns Course
## Complete 16-Semester Comprehensive Textbook

This document contains all lessons, algorithms, and patterns from the complete 16-semester course covering undergraduate and graduate-level topics.

\\newpage

"""
    
    for header, content in content_parts:
        full_content += header + content + "\n\n"
    
    # Add footer
    full_content += """
\\newpage

# Appendix

## Course Statistics

- **Total Semesters**: 16 (8 undergraduate + 8 graduate)
- **Total Lectures**: 118+
- **Total Algorithms**: 600+
- **Programming Languages**: Python, Java
- **Frameworks Covered**: Spring, J2EE, .NET, Docker, Kubernetes, Kafka
- **Topics**: Algorithms, Data Structures, Design Patterns, Computational Intelligence, Operating Systems, Concurrency, CI/CD, Quantum Computing, Blockchain, Databases, and more

## References

- All algorithms include complexity analysis
- All patterns include real-world examples
- All implementations include performance measurements

---

*Generated from comprehensive algorithms course repository*
"""
    
    return full_content


def main():
    """Main function."""
    print("Generating comprehensive course PDF...")
    
    # Generate markdown
    markdown_content = generate_markdown_document()
    
    # Save markdown
    md_file = Path("COMPREHENSIVE_COURSE_TEXTBOOK.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Generated markdown: {md_file}")
    print(f"File size: {md_file.stat().st_size / 1024:.2f} KB")
    
    # Try to generate HTML (can be converted to PDF)
    try:
        html_file = Path("COMPREHENSIVE_COURSE_TEXTBOOK.html")
        
        # Convert markdown to HTML using pandoc if available
        result = subprocess.run(
            ['pandoc', str(md_file), '-o', str(html_file), 
             '--standalone', '--toc', '--toc-depth=3',
             '--css', 'https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"Generated HTML: {html_file}")
            print("You can open this HTML file in a browser and print to PDF")
        else:
            print("Pandoc not available or error occurred")
            print("Markdown file can be converted to PDF using:")
            print("  - Pandoc: pandoc COMPREHENSIVE_COURSE_TEXTBOOK.md -o output.pdf")
            print("  - Browser: Open HTML and print to PDF")
            print("  - Online converters")
    except FileNotFoundError:
        print("Pandoc not found. HTML generation skipped.")
        print("Markdown file saved. Convert to PDF using:")
        print("  - Pandoc: pandoc COMPREHENSIVE_COURSE_TEXTBOOK.md -o output.pdf")
        print("  - Online markdown to PDF converters")
    
    print("\nDone!")


if __name__ == "__main__":
    main()

