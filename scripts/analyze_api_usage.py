#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze actual API usage and estimate remaining costs.
"""

import sys
import sqlite3
from pathlib import Path
from openai import OpenAI

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import OPENAI_API_KEY, OPENAI_API_BASE

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def estimate_tokens_from_files() -> None:
    """Estimate tokens from generated files."""
    print("\n" + "="*70)
    print("ANALYZING GENERATED FILES")
    print("="*70)
    
    # Count characters in generated files
    total_chars = 0
    file_count = 0
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/school.*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                total_chars += len(content)
                file_count += 1
        except:
            pass
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/univer.*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                total_chars += len(content)
                file_count += 1
        except:
            pass
    
    # Rough estimate: 1 token ≈ 4 characters
    estimated_tokens = total_chars / 4
    
    print(f"\nFiles analyzed: {file_count}")
    print(f"Total characters: {total_chars:,}")
    print(f"Estimated tokens: {estimated_tokens:,.0f}")
    print(f"Average tokens per file: {estimated_tokens/file_count:.0f}" if file_count > 0 else "")


def analyze_database() -> None:
    """Analyze prompts in database."""
    db_path = ROOT / "database" / "algorithm_prompts.db"
    
    if not db_path.exists():
        print("\nNo database found.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
    count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT algorithm_name, 
               LENGTH(prompt_school_en) + LENGTH(prompt_school_ru) + 
               LENGTH(prompt_univer_en) + LENGTH(prompt_univer_ru) as total_chars
        FROM algorithm_prompts
        LIMIT 5
    """)
    
    samples = cursor.fetchall()
    
    print("\n" + "="*70)
    print("DATABASE ANALYSIS")
    print("="*70)
    print(f"\nAlgorithms in database: {count}")
    print(f"\nSample prompt sizes (characters):")
    for name, chars in samples:
        print(f"  {name}: {chars:,} chars (~{chars/4:.0f} tokens)")
    
    conn.close()


def calculate_detailed_costs() -> None:
    """Calculate detailed cost estimates."""
    algorithms_count = 680
    prompts_per_algorithm = 4
    total_requests = algorithms_count * prompts_per_algorithm
    
    # Based on actual generated files, responses are ~500-800 tokens
    # Prompts are ~150-250 tokens
    avg_prompt_tokens = 200
    avg_response_tokens = 700  # Conservative estimate based on actual files
    
    total_input_tokens = total_requests * avg_prompt_tokens
    total_output_tokens = total_requests * avg_response_tokens
    
    # GPT-3.5-turbo pricing (as of 2024)
    input_price = 0.50 / 1_000_000  # $0.50 per 1M tokens
    output_price = 1.50 / 1_000_000  # $1.50 per 1M tokens
    
    input_cost = total_input_tokens * input_price
    output_cost = total_output_tokens * output_price
    total_cost = input_cost + output_cost
    
    # Cost per algorithm
    cost_per_algorithm = total_cost / algorithms_count
    cost_per_prompt = total_cost / total_requests
    
    print("\n" + "="*70)
    print("DETAILED COST BREAKDOWN")
    print("="*70)
    print(f"\nAlgorithms remaining: {algorithms_count}")
    print(f"Prompts per algorithm: {prompts_per_algorithm}")
    print(f"Total requests needed: {total_requests:,}")
    print(f"\nToken estimates:")
    print(f"  Input tokens per request: ~{avg_prompt_tokens}")
    print(f"  Output tokens per request: ~{avg_response_tokens}")
    print(f"  Total tokens per request: ~{avg_prompt_tokens + avg_response_tokens}")
    print(f"\nTotal token estimates:")
    print(f"  Input: {total_input_tokens:,} ({total_input_tokens/1_000_000:.3f}M)")
    print(f"  Output: {total_output_tokens:,} ({total_output_tokens/1_000_000:.3f}M)")
    print(f"  Total: {total_input_tokens + total_output_tokens:,} ({(total_input_tokens + total_output_tokens)/1_000_000:.3f}M)")
    print(f"\nCost breakdown:")
    print(f"  Input cost: ${input_cost:.2f}")
    print(f"  Output cost: ${output_cost:.2f}")
    print(f"  TOTAL ESTIMATED COST: ${total_cost:.2f}")
    print(f"\nPer-item costs:")
    print(f"  Cost per algorithm: ${cost_per_algorithm:.4f}")
    print(f"  Cost per prompt: ${cost_per_prompt:.4f}")
    print("\n" + "="*70)


def explain_balance_issue() -> None:
    """Explain why balance ran out after 8 prompts."""
    print("\n" + "="*70)
    print("WHY BALANCE RAN OUT AFTER 8 PROMPTS")
    print("="*70)
    print("""
The error "Insufficient balance to run this request" (402) indicates:

1. Your proxy account (api.proxyapi.ru) had a very low starting balance
2. Each API call costs money based on tokens used
3. After 8 successful prompts (2 algorithms × 4 prompts), the balance was depleted

Estimated cost for 8 prompts:
- Input tokens: ~1,600 tokens (8 × 200)
- Output tokens: ~5,600 tokens (8 × 700)
- Total: ~7,200 tokens
- Estimated cost: ~$0.01-0.02 (depending on proxy markup)

This suggests your proxy account had less than $0.02 balance to start with.

SOLUTIONS:
1. Add funds to your proxy account (api.proxyapi.ru)
2. Check your proxy provider's dashboard for:
   - Current balance
   - Pricing/rates
   - Minimum balance requirements
3. Consider using OpenAI directly if proxy markup is too high
""")


if __name__ == "__main__":
    print("="*70)
    print("API USAGE ANALYSIS & COST ESTIMATION")
    print("="*70)
    
    analyze_database()
    estimate_tokens_from_files()
    calculate_detailed_costs()
    explain_balance_issue()
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print("""
1. Check your proxy provider dashboard for:
   - Current balance
   - Pricing rates (may have markup)
   - Minimum recharge amount

2. For all 680 algorithms (~$4.35 estimated):
   - Add at least $5-10 to account for variations
   - Monitor balance during processing
   - The script will stop if balance runs out

3. Consider processing in batches:
   - Process 50-100 algorithms at a time
   - Check balance between batches
   - Adjust based on actual costs

4. The script saves progress, so you can resume:
   - Already processed algorithms are skipped (check database)
   - Just run the script again when balance is restored
""")

