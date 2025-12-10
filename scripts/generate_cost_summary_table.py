#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a formatted cost summary table.
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def print_summary_table() -> None:
    """Print formatted summary table."""
    
    print("\n" + "="*80)
    print("COST SUMMARY TABLE - ALL LEVELS AND LANGUAGES")
    print("="*80)
    
    # Data from analysis
    data = [
        {
            'category': 'School - English',
            'prompt_tokens': 104,
            'response_tokens': 449,
            'total_tokens': 554,
            'cost_per_request': 0.0007,
            'total_requests': 680,
            'total_cost': 0.49
        },
        {
            'category': 'School - Russian',
            'prompt_tokens': 97,
            'response_tokens': 458,
            'total_tokens': 555,
            'cost_per_request': 0.0007,
            'total_requests': 680,
            'total_cost': 0.50
        },
        {
            'category': 'University - English',
            'prompt_tokens': 109,
            'response_tokens': 631,
            'total_tokens': 740,
            'cost_per_request': 0.0010,
            'total_requests': 680,
            'total_cost': 0.68
        },
        {
            'category': 'University - Russian',
            'prompt_tokens': 108,
            'response_tokens': 660,
            'total_tokens': 768,
            'cost_per_request': 0.0010,
            'total_requests': 680,
            'total_cost': 0.71
        }
    ]
    
    print(f"\n{'Category':<25} {'Prompt':<8} {'Response':<10} {'Total':<8} {'Cost/Req':<10} {'Total Cost':<12}")
    print("-" * 80)
    
    total_cost = 0
    for item in data:
        print(f"{item['category']:<25} "
              f"{item['prompt_tokens']:<8.0f} "
              f"{item['response_tokens']:<10.0f} "
              f"{item['total_tokens']:<8.0f} "
              f"${item['cost_per_request']:<9.4f} "
              f"${item['total_cost']:<11.2f}")
        total_cost += item['total_cost']
    
    print("-" * 80)
    print(f"{'TOTAL':<25} {'':<8} {'':<10} {'':<8} {'':<10} ${total_cost:<11.2f}")
    
    print("\n" + "="*80)
    print("BREAKDOWN SUMMARY")
    print("="*80)
    
    school_total = data[0]['total_cost'] + data[1]['total_cost']
    univer_total = data[2]['total_cost'] + data[3]['total_cost']
    en_total = data[0]['total_cost'] + data[2]['total_cost']
    ru_total = data[1]['total_cost'] + data[3]['total_cost']
    
    print(f"\nBy Level:")
    print(f"  School (en + ru):     ${school_total:.2f} ({school_total/total_cost*100:.1f}%)")
    print(f"  University (en + ru): ${univer_total:.2f} ({univer_total/total_cost*100:.1f}%)")
    
    print(f"\nBy Language:")
    print(f"  English (school + univer): ${en_total:.2f} ({en_total/total_cost*100:.1f}%)")
    print(f"  Russian (school + univer): ${ru_total:.2f} ({ru_total/total_cost*100:.1f}%)")
    
    print(f"\nPer Algorithm (all 4 prompts): ${total_cost/680:.4f}")
    print(f"Per Prompt (average):         ${total_cost/2720:.4f}")
    
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print("""
1. University-level prompts cost ~43% more than school-level
   - More detailed responses require more tokens
   - Russian responses are slightly longer than English

2. Total cost breakdown:
   - School level: 41.7% of total cost
   - University level: 58.3% of total cost
   - English: 49.3% of total cost
   - Russian: 50.7% of total cost

3. Cost efficiency:
   - Cheapest: School prompts ($0.0007 each)
   - Most expensive: University Russian ($0.0010 each)
   - Average: $0.0009 per prompt

4. Recommendation:
   - Add $3-5 to account for variations and proxy markup
   - Process in batches of 100-200 algorithms
   - Monitor balance during processing
""")


if __name__ == "__main__":
    print_summary_table()

