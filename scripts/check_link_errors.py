#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for link errors in MD files.
Finds broken internal links, missing files, and invalid references.
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def find_links_in_content(content: str, file_path: Path) -> List[Tuple[str, int, str]]:
    """Find all links in markdown content."""
    links = []
    
    # Pattern for markdown links: [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    
    for match in re.finditer(link_pattern, content):
        link_text = match.group(1)
        link_url = match.group(2)
        line_num = content[:match.start()].count('\n') + 1
        links.append((link_text, line_num, link_url))
    
    # Pattern for image links: ![alt](url)
    img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    
    for match in re.finditer(img_pattern, content):
        alt_text = match.group(1)
        img_url = match.group(2)
        line_num = content[:match.start()].count('\n') + 1
        links.append((f"Image: {alt_text}", line_num, img_url))
    
    return links


def check_link_validity(link_url: str, source_file: Path) -> Tuple[bool, str]:
    """Check if a link is valid."""
    # Skip external URLs
    if link_url.startswith('http://') or link_url.startswith('https://'):
        return True, "external"
    
    # Skip mailto links
    if link_url.startswith('mailto:'):
        return True, "mailto"
    
    # Skip anchors (fragment only)
    if link_url.startswith('#'):
        return True, "anchor"
    
    # Handle relative paths
    if link_url.startswith('/'):
        # Absolute path from root
        target_path = ROOT / link_url.lstrip('/')
    else:
        # Relative path from source file
        target_path = source_file.parent / link_url
    
    # Normalize path
    try:
        target_path = target_path.resolve()
        
        # Check if file exists
        if target_path.exists():
            return True, "valid"
        
        # Check if it's a directory (might be valid)
        if target_path.is_dir():
            return True, "directory"
        
        # Check for anchor links (file#anchor)
        if '#' in link_url:
            file_part = link_url.split('#')[0]
            anchor_part = link_url.split('#')[1]
            file_path = source_file.parent / file_part
            if file_path.exists():
                # Could check if anchor exists, but that's complex
                return True, "file_with_anchor"
        
        return False, f"File not found: {target_path}"
    except Exception as e:
        return False, f"Error resolving path: {e}"


def check_md_file(md_file: Path) -> List[Dict]:
    """Check a single MD file for link errors."""
    errors = []
    
    try:
        content = md_file.read_text(encoding='utf-8')
        links = find_links_in_content(content, md_file)
        
        for link_text, line_num, link_url in links:
            is_valid, reason = check_link_validity(link_url, md_file)
            if not is_valid:
                errors.append({
                    'file': str(md_file.relative_to(ROOT)),
                    'line': line_num,
                    'link_text': link_text,
                    'link_url': link_url,
                    'error': reason
                })
    except Exception as e:
        errors.append({
            'file': str(md_file.relative_to(ROOT)),
            'line': 0,
            'link_text': '',
            'link_url': '',
            'error': f"Error reading file: {e}"
        })
    
    return errors


def find_all_md_files() -> list:
    """Find all MD files."""
    md_files = []
    
    # Find all markdown files
    for md_file in ROOT.glob("**/*.md"):
        # Skip certain directories
        if 'node_modules' in str(md_file) or '.git' in str(md_file):
            continue
        md_files.append(md_file)
    
    return sorted(md_files)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("CHECKING LINK ERRORS")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nChecking links...")
    
    all_errors = []
    checked = 0
    
    for i, md_file in enumerate(md_files, 1):
        errors = check_md_file(md_file)
        all_errors.extend(errors)
        checked += 1
        
        if i % 100 == 0:
            print(f"Progress: {i}/{len(md_files)} ({i/len(md_files)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"Checked: {checked} files")
    print(f"Errors found: {len(all_errors)}")
    print(f"{'='*70}")
    
    if all_errors:
        print("\nLink Errors:")
        print("-" * 70)
        for error in all_errors[:50]:  # Show first 50
            print(f"File: {error['file']}")
            print(f"  Line {error['line']}: {error['link_text']}")
            print(f"  URL: {error['link_url']}")
            print(f"  Error: {error['error']}")
            print()
        
        if len(all_errors) > 50:
            print(f"... and {len(all_errors) - 50} more errors")
        
        # Save to file
        report_path = ROOT / "link_errors_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Link Errors Report\n")
            f.write("=" * 70 + "\n\n")
            for error in all_errors:
                f.write(f"File: {error['file']}\n")
                f.write(f"  Line {error['line']}: {error['link_text']}\n")
                f.write(f"  URL: {error['link_url']}\n")
                f.write(f"  Error: {error['error']}\n\n")
        
        print(f"\nFull report saved to: {report_path}")
        return 1
    
    print("\n✓ No link errors found!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

