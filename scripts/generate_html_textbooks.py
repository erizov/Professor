#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate HTML textbooks that can be printed to PDF.

No external dependencies required.
"""

import datetime
from pathlib import Path
from typing import List


def create_html_document(title: str, files: List[str], 
                         output_file: str) -> bool:
    """
    Create HTML document from markdown files.
    
    Args:
        title: Document title
        files: List of markdown files to include
        output_file: Output HTML filename
        
    Returns:
        True if successful
    """
    print(f"\nGenerating: {output_file}")
    print("-" * 70)
    
    html_parts = []
    
    # HTML Header
    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @media print {{
            body {{ margin: 0; }}
            .no-print {{ display: none; }}
            .page-break {{ page-break-before: always; }}
        }}
        
        body {{
            font-family: 'Segoe UI', 'Georgia', serif;
            line-height: 1.8;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        
        .document {{
            background: white;
            padding: 60px;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            min-height: 100vh;
        }}
        
        .cover {{
            text-align: center;
            padding: 100px 0;
            border-bottom: 3px solid #667eea;
        }}
        
        .cover h1 {{
            font-size: 48px;
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .cover .subtitle {{
            font-size: 24px;
            color: #764ba2;
            margin: 20px 0;
        }}
        
        .cover .author {{
            font-size: 18px;
            color: #666;
            margin: 30px 0;
        }}
        
        .cover .date {{
            font-size: 14px;
            color: #999;
        }}
        
        .toc {{
            background: #f9f9f9;
            padding: 30px;
            margin: 40px 0;
            border-left: 5px solid #667eea;
        }}
        
        .toc h2 {{
            color: #667eea;
            margin-top: 0;
        }}
        
        .toc ul {{
            list-style: none;
            padding: 0;
        }}
        
        .toc li {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        
        .toc a {{
            color: #764ba2;
            text-decoration: none;
            font-size: 16px;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 36px;
            margin-top: 60px;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        h2 {{
            color: #764ba2;
            font-size: 28px;
            margin-top: 40px;
            margin-bottom: 15px;
        }}
        
        h3 {{
            color: #555;
            font-size: 22px;
            margin-top: 30px;
            margin-bottom: 10px;
        }}
        
        h4 {{
            color: #666;
            font-size: 18px;
            margin-top: 20px;
        }}
        
        p {{
            margin: 15px 0;
            text-align: justify;
        }}
        
        code {{
            background: #f4f4f4;
            padding: 3px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            color: #c7254e;
        }}
        
        pre {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.5;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: #d4d4d4;
        }}
        
        blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        .section {{
            margin: 40px 0;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 12px;
            font-size: 12px;
            margin: 0 5px;
        }}
        
        .alert {{
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .alert-success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            color: #155724;
        }}
        
        .alert-warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            color: #856404;
        }}
        
        .alert-info {{
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            color: #0c5460;
        }}
        
        .print-button {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            z-index: 1000;
        }}
        
        .print-button:hover {{
            background: #5568d3;
        }}
        
        @page {{
            margin: 2cm;
        }}
    </style>
</head>
<body>
    <div class="document">
        <!-- Cover Page -->
        <div class="cover">
            <h1>{title}</h1>
            <div class="subtitle">Comprehensive Computer Science Course</div>
            <div class="author">University Professor of Computer Science</div>
            <div class="date">Generated: {datetime.datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        <div class="page-break"></div>
        
        <!-- Table of Contents -->
        <div class="toc">
            <h2>📚 Table of Contents</h2>
            <ul>
""")
    
    # Build TOC
    toc_items = []
    for filepath in files:
        path = Path(filepath)
        if path.exists():
            name = path.stem.replace('_', ' ').replace('-', ' ').title()
            anchor = path.stem.lower().replace('_', '-')
            toc_items.append((name, anchor))
            html_parts.append(f'                <li><a href="#{anchor}">{name}</a></li>\n')
    
    html_parts.append("""            </ul>
        </div>
        <div class="page-break"></div>
        
        <!-- Main Content -->
""")
    
    # Add content from files
    for filepath in files:
        path = Path(filepath)
        if not path.exists():
            print(f"  ⚠ Skipping: {filepath} (not found)")
            continue
        
        print(f"  ✓ Adding: {filepath}")
        content = path.read_text(encoding='utf-8')
        
        anchor = path.stem.lower().replace('_', '-')
        name = path.stem.replace('_', ' ').replace('-', ' ').title()
        
        html_parts.append(f'        <div class="section" id="{anchor}">\n')
        html_parts.append(f'            <h1>{name}</h1>\n')
        
        # Simple markdown to HTML conversion
        html_content = markdown_to_html(content)
        html_parts.append(html_content)
        
        html_parts.append('        </div>\n')
        html_parts.append('        <div class="page-break"></div>\n\n')
    
    # Footer
    html_parts.append("""    </div>
    
    <!-- Print Button -->
    <button class="print-button no-print" onclick="window.print()">
        🖨️ Print / Save as PDF
    </button>
    
    <script>
        // Smooth scroll to anchors
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
""")
    
    # Write HTML file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(html_parts)
        
        file_size = Path(output_file).stat().st_size / 1024
        print(f"  ✓ Generated: {output_file} ({file_size:.1f} KB)")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown to HTML (simple implementation).
    
    Args:
        markdown_text: Markdown text
        
    Returns:
        HTML string
    """
    lines = markdown_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    code_lang = ''
    
    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                code_lang = line.strip()[3:].strip()
                html_lines.append(f'<pre><code class="{code_lang}">')
                in_code_block = True
            continue
        
        if in_code_block:
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_lines.append(escaped)
            continue
        
        # Headings
        if line.startswith('####'):
            html_lines.append(f'<h4>{line[4:].strip()}</h4>')
        elif line.startswith('###'):
            html_lines.append(f'<h3>{line[3:].strip()}</h3>')
        elif line.startswith('##'):
            html_lines.append(f'<h2>{line[2:].strip()}</h2>')
        elif line.startswith('#'):
            html_lines.append(f'<h1>{line[1:].strip()}</h1>')
        
        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            html_lines.append(f'<li>{line.strip()[3:]}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            
            # Paragraphs
            if line.strip():
                # Format badges and alerts
                formatted = line
                if '✅' in line or '✓' in line:
                    formatted = f'<div class="alert alert-success">{line}</div>'
                elif '⚠️' in line or '❌' in line:
                    formatted = f'<div class="alert alert-warning">{line}</div>'
                elif '📝' in line or 'ℹ️' in line:
                    formatted = f'<div class="alert alert-info">{line}</div>'
                else:
                    formatted = f'<p>{format_inline(line)}</p>'
                
                html_lines.append(formatted)
            else:
                html_lines.append('<br>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)


def format_inline(text: str) -> str:
    """Format inline markdown elements."""
    import re
    
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    return text


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("HTML TEXTBOOK GENERATION")
    print("=" * 70)
    print("\nGenerating HTML documents (print to PDF from browser)")
    
    # Main textbook
    textbook_files = [
        "README.md",
        "QUICKSTART.md",
        "COURSE_PLAN_6SEMESTERS.md",
        "ALGORITHM_INDEX.md",
    ]
    
    success1 = create_html_document(
        "Algorithms Course - 6 Semesters",
        textbook_files,
        "Algorithms_Course_Textbook.html"
    )
    
    # Improvements document
    improvements_files = [
        "CRITIQUES.md",
        "IMPLEMENTATION_STATUS.md",
        "ACTUAL_STATUS.md",
        "AI_IMPLEMENTATION_GUIDE.md",
    ]
    
    success2 = create_html_document(
        "Professional Critiques & Improvements",
        improvements_files,
        "Algorithms_Course_Improvements.html"
    )
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("✅ HTML documents generated successfully!")
        print()
        print("Generated files:")
        print("  1. Algorithms_Course_Textbook.html")
        print("  2. Algorithms_Course_Improvements.html")
        print()
        print("To create PDF:")
        print("  1. Open HTML file in browser (Chrome/Edge recommended)")
        print("  2. Press Ctrl+P (or Cmd+P on Mac)")
        print("  3. Select 'Save as PDF' as destination")
        print("  4. Click 'Save'")
        print()
        print("Or use the 'Print / Save as PDF' button in the document!")
    else:
        print("⚠️ Some documents failed to generate")
    print("=" * 70)
    
    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

