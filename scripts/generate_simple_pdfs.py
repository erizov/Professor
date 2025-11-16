#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple PDF generation using markdown2pdf or pandoc.

Alternative to reportlab - easier to install.
"""

import subprocess
import sys
from pathlib import Path


def check_pandoc():
    """Check if pandoc is installed."""
    try:
        subprocess.run(['pandoc', '--version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_with_pandoc(input_files: list, output_file: str, 
                         title: str):
    """Generate PDF using pandoc."""
    print(f"Generating {output_file} with pandoc...")
    
    # Create combined markdown
    combined_md = f"combined_{Path(output_file).stem}.md"
    
    with open(combined_md, 'w', encoding='utf-8') as outf:
        outf.write(f"---\n")
        outf.write(f"title: {title}\n")
        outf.write(f"author: University Professor of Computer Science\n")
        outf.write(f"date: \\today\n")
        outf.write(f"geometry: margin=1in\n")
        outf.write(f"---\n\n")
        outf.write(f"\\newpage\n\n")
        
        for filepath in input_files:
            path = Path(filepath)
            if path.exists():
                print(f"  Adding: {filepath}")
                content = path.read_text(encoding='utf-8')
                outf.write(f"# {path.stem.replace('_', ' ').title()}\n\n")
                outf.write(content)
                outf.write(f"\n\n\\newpage\n\n")
    
    # Convert to PDF
    cmd = [
        'pandoc',
        combined_md,
        '-o', output_file,
        '--pdf-engine=xelatex',
        '--toc',
        '--toc-depth=2',
        '-V', 'linkcolor:blue',
        '-V', 'geometry:a4paper',
        '-V', 'geometry:margin=2cm',
        '--highlight-style=tango'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Generated: {output_file}")
            # Cleanup
            Path(combined_md).unlink()
            return True
        else:
            print(f"✗ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def generate_html_fallback(input_files: list, output_file: str,
                           title: str):
    """Generate HTML if PDF fails."""
    print(f"Generating {output_file} (HTML fallback)...")
    
    html_file = output_file.replace('.pdf', '.html')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .content {{
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #667eea; }}
        h2 {{ color: #764ba2; }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .toc {{
            background: #f9f9f9;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="content">
        <h1>{title}</h1>
        <p><strong>Generated:</strong> {Path().resolve()}</p>
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
""")
        
        # Add TOC
        for filepath in input_files:
            path = Path(filepath)
            if path.exists():
                name = path.stem.replace('_', ' ').title()
                anchor = path.stem.lower()
                f.write(f'                <li><a href="#{anchor}">{name}</a></li>\n')
        
        f.write("""            </ul>
        </div>
        <hr>
""")
        
        # Add content
        for filepath in input_files:
            path = Path(filepath)
            if path.exists():
                content = path.read_text(encoding='utf-8')
                anchor = path.stem.lower()
                name = path.stem.replace('_', ' ').title()
                
                f.write(f'        <div id="{anchor}">\n')
                f.write(f'            <h1>{name}</h1>\n')
                
                # Simple markdown to HTML
                html_content = content.replace('&', '&amp;')
                html_content = html_content.replace('<', '&lt;')
                html_content = html_content.replace('>', '&gt;')
                html_content = html_content.replace('\n\n', '</p><p>')
                html_content = html_content.replace('# ', '<h1>')
                html_content = html_content.replace('\n', '<br>')
                
                f.write(f'            <div>{html_content}</div>\n')
                f.write('        </div>\n        <hr>\n')
        
        f.write("""    </div>
</body>
</html>
""")
    
    print(f"✓ Generated HTML: {html_file}")
    print(f"  You can open this in a browser and print to PDF")
    return True


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("SIMPLE PDF GENERATION")
    print("=" * 70)
    print()
    
    # Check for pandoc
    has_pandoc = check_pandoc()
    
    if has_pandoc:
        print("✓ Pandoc found - will generate PDFs")
    else:
        print("⚠ Pandoc not found - will generate HTML instead")
        print("  Install pandoc: https://pandoc.org/installing.html")
        print()
    
    # Define documents
    textbook_files = [
        "README.md",
        "COURSE_PLAN_6SEMESTERS.md",
        "ALGORITHM_INDEX.md",
        "QUICKSTART.md",
    ]
    
    improvements_files = [
        "CRITIQUES.md",
        "IMPLEMENTATION_STATUS.md",
        "ACTUAL_STATUS.md",
        "AI_IMPLEMENTATION_GUIDE.md",
    ]
    
    # Generate textbook
    if has_pandoc:
        success1 = generate_with_pandoc(
            textbook_files,
            "Algorithms_Course_Textbook.pdf",
            "Algorithms Course - 6 Semesters Complete Textbook"
        )
    else:
        success1 = generate_html_fallback(
            textbook_files,
            "Algorithms_Course_Textbook.pdf",
            "Algorithms Course - 6 Semesters Complete Textbook"
        )
    
    print()
    
    # Generate improvements
    if has_pandoc:
        success2 = generate_with_pandoc(
            improvements_files,
            "Algorithms_Course_Improvements.pdf",
            "Professional Critiques & Improvement Suggestions"
        )
    else:
        success2 = generate_html_fallback(
            improvements_files,
            "Algorithms_Course_Improvements.pdf",
            "Professional Critiques & Improvement Suggestions"
        )
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("✅ Documents generated successfully!")
        print()
        if has_pandoc:
            print("Generated PDFs:")
            print("  1. Algorithms_Course_Textbook.pdf")
            print("  2. Algorithms_Course_Improvements.pdf")
        else:
            print("Generated HTML files:")
            print("  1. Algorithms_Course_Textbook.html")
            print("  2. Algorithms_Course_Improvements.html")
            print()
            print("To convert to PDF:")
            print("  - Open in browser and Print to PDF")
            print("  - Or install pandoc for automatic conversion")
    else:
        print("⚠️ Some documents failed to generate")
    print("=" * 70)
    
    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    sys.exit(main())

