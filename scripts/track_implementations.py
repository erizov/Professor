#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Track implementation progress across all algorithms.

Usage:
    python track_implementations.py --check
    python track_implementations.py --mark semester_1/lecture_01/merge_sort
    python track_implementations.py --report
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List


def is_placeholder(file_path: Path) -> bool:
    """
    Check if a file is a placeholder implementation.
    
    Args:
        file_path: Path to algorithm.py or Algorithm.java
        
    Returns:
        True if placeholder, False if real implementation
    """
    if not file_path.exists():
        return True
    
    content = file_path.read_text(encoding='utf-8')
    lines = [line for line in content.split('\n') if line.strip()]
    
    # Heuristics for placeholder detection
    if len(lines) < 30:  # Real implementations are longer
        return True
    
    # Check for placeholder indicators
    placeholder_indicators = [
        'def ' + file_path.parent.name + '():',
        'print("==" * 35)',
        'System.out.println("==".repeat(35))',
    ]
    
    for indicator in placeholder_indicators:
        if indicator in content and len(lines) < 50:
            return True
    
    return False


def scan_implementations() -> Dict[str, Dict]:
    """
    Scan all algorithms and check implementation status.
    
    Returns:
        Dictionary with implementation status
    """
    results = {
        'total': 0,
        'implemented': 0,
        'placeholder': 0,
        'by_semester': {},
        'details': []
    }
    
    base_path = Path(__file__).resolve().parents[1]
    
    for semester in range(1, 7):
        semester_path = base_path / f"semester_{semester}"
        if not semester_path.exists():
            continue
        
        semester_stats = {
            'total': 0,
            'implemented': 0,
            'placeholder': 0
        }
        
        for lecture_path in sorted(semester_path.iterdir()):
            if not lecture_path.is_dir():
                continue
            
            for algo_path in sorted(lecture_path.iterdir()):
                if not algo_path.is_dir():
                    continue
                
                results['total'] += 1
                semester_stats['total'] += 1
                
                # Check Python implementation
                py_file = algo_path / "algorithm.py"
                java_file = algo_path / "Algorithm.java"
                
                py_placeholder = is_placeholder(py_file)
                java_placeholder = is_placeholder(java_file)
                
                # Consider implemented if at least one language is done
                is_impl = not (py_placeholder and java_placeholder)
                
                if is_impl:
                    results['implemented'] += 1
                    semester_stats['implemented'] += 1
                else:
                    results['placeholder'] += 1
                    semester_stats['placeholder'] += 1
                
                results['details'].append({
                    'path': str(algo_path.relative_to(base_path)),
                    'name': algo_path.name,
                    'semester': semester,
                    'lecture': lecture_path.name,
                    'python_done': not py_placeholder,
                    'java_done': not java_placeholder,
                    'status': 'implemented' if is_impl else 'placeholder'
                })
        
        results['by_semester'][f'semester_{semester}'] = semester_stats
    
    return results


def print_report(results: Dict) -> None:
    """Print formatted report."""
    print("\n" + "=" * 70)
    print("IMPLEMENTATION PROGRESS REPORT")
    print("=" * 70)
    print()
    
    # Overall stats
    total = results['total']
    impl = results['implemented']
    placeholder = results['placeholder']
    percentage = (impl / total * 100) if total > 0 else 0
    
    print(f"Overall Progress: {impl}/{total} ({percentage:.1f}%)")
    print(f"  ✓ Implemented: {impl}")
    print(f"  ⚠ Placeholders: {placeholder}")
    print()
    
    # By semester
    print("Progress by Semester:")
    print("-" * 70)
    for semester_name, stats in sorted(results['by_semester'].items()):
        impl_sem = stats['implemented']
        total_sem = stats['total']
        pct = (impl_sem / total_sem * 100) if total_sem > 0 else 0
        
        bar_length = 40
        filled = int(bar_length * pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"{semester_name}: [{bar}] {pct:5.1f}% "
              f"({impl_sem}/{total_sem})")
    print()
    
    # Recently implemented (if any)
    implemented = [
        d for d in results['details'] if d['status'] == 'implemented'
    ]
    
    if implemented:
        print("Implemented Algorithms:")
        print("-" * 70)
        for item in implemented[:10]:  # Show first 10
            status = "✓✓" if (item['python_done'] and 
                             item['java_done']) else "✓"
            print(f"  {status} {item['path']}")
        
        if len(implemented) > 10:
            print(f"  ... and {len(implemented) - 10} more")
        print()
    
    # Pending
    pending = [
        d for d in results['details'] if d['status'] == 'placeholder'
    ]
    
    if pending:
        print(f"Pending Implementations ({len(pending)}):")
        print("-" * 70)
        
        # Group by category
        by_lecture = {}
        for item in pending:
            lecture = item['lecture']
            if lecture not in by_lecture:
                by_lecture[lecture] = []
            by_lecture[lecture].append(item)
        
        for lecture, items in sorted(by_lecture.items())[:5]:
            print(f"\n  {lecture}: ({len(items)} algorithms)")
            for item in items[:3]:
                print(f"    ⚠ {item['name']}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
    
    print("\n" + "=" * 70)
    
    # Recommendations
    if percentage < 25:
        print("\n💡 Recommendation: Start with sorting algorithms")
        print("   Use: AI_IMPLEMENTATION_GUIDE.md")
    elif percentage < 50:
        print("\n💡 Recommendation: Continue with ML basics")
    elif percentage < 75:
        print("\n💡 Recommendation: Tackle design patterns")
    else:
        print("\n🎉 Almost done! Finish the remaining algorithms!")
    
    print()


def save_progress(results: Dict, output_file: str = 
                 'implementation_progress.json') -> None:
    """Save progress to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Progress saved to {output_file}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Track algorithm implementation progress"
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check implementation status'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate detailed report'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save progress to JSON'
    )
    parser.add_argument(
        '--list-pending',
        action='store_true',
        help='List all pending algorithms'
    )
    
    args = parser.parse_args()
    
    # Default to check if no args
    if not any(vars(args).values()):
        args.check = True
    
    print("Scanning algorithms...")
    results = scan_implementations()
    
    if args.check or args.report:
        print_report(results)
    
    if args.save:
        save_progress(results)
    
    if args.list_pending:
        pending = [
            d for d in results['details'] 
            if d['status'] == 'placeholder'
        ]
        print("\nAll Pending Algorithms:")
        print("-" * 70)
        for item in pending:
            print(f"  ⚠ {item['path']}")


if __name__ == "__main__":
    main()

