#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check API balance and estimate costs for processing all algorithms.
"""

import sys
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


def check_balance() -> None:
    """Check API balance if possible."""
    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE
        )
        
        # Try to get account info (may not be available through proxy)
        print("Checking API balance...")
        print(f"Base URL: {OPENAI_API_BASE}")
        print(f"API Key: {OPENAI_API_KEY[:7]}...{OPENAI_API_KEY[-4:]}")
        print("\nNote: Balance checking may not be available through proxy.")
        print("Check your proxy provider's dashboard for balance information.")
        
    except Exception as e:
        print(f"Error checking balance: {e}")


def estimate_costs() -> None:
    """Estimate costs for processing all algorithms."""
    # GPT-3.5-turbo pricing (as of 2024)
    # Input: $0.50 per 1M tokens
    # Output: $1.50 per 1M tokens
    
    # Estimate tokens per request
    # Prompt: ~200-300 tokens (prompt text)
    # Response: ~800-1200 tokens (brief content)
    # Total: ~1000-1500 tokens per request
    
    algorithms_count = 680  # Found in the script
    prompts_per_algorithm = 4
    total_requests = algorithms_count * prompts_per_algorithm
    
    # Conservative estimates
    tokens_per_prompt = 200  # Prompt tokens
    tokens_per_response = 1000  # Response tokens (brief)
    tokens_per_request = tokens_per_prompt + tokens_per_response
    
    total_input_tokens = total_requests * tokens_per_prompt
    total_output_tokens = total_requests * tokens_per_response
    total_tokens = total_requests * tokens_per_request
    
    # Pricing (per 1M tokens)
    input_price_per_million = 0.50  # $0.50 per 1M input tokens
    output_price_per_million = 1.50  # $1.50 per 1M output tokens
    
    input_cost = (total_input_tokens / 1_000_000) * input_price_per_million
    output_cost = (total_output_tokens / 1_000_000) * output_price_per_million
    total_cost = input_cost + output_cost
    
    print("\n" + "="*70)
    print("COST ESTIMATION FOR ALL ALGORITHMS")
    print("="*70)
    print(f"\nAlgorithms to process: {algorithms_count}")
    print(f"Prompts per algorithm: {prompts_per_algorithm}")
    print(f"Total API requests: {total_requests:,}")
    print(f"\nToken estimates per request:")
    print(f"  Input (prompt): ~{tokens_per_prompt} tokens")
    print(f"  Output (response): ~{tokens_per_response} tokens")
    print(f"  Total: ~{tokens_per_request} tokens")
    print(f"\nTotal token estimates:")
    print(f"  Input tokens: {total_input_tokens:,} ({total_input_tokens/1_000_000:.2f}M)")
    print(f"  Output tokens: {total_output_tokens:,} ({total_output_tokens/1_000_000:.2f}M)")
    print(f"  Total tokens: {total_tokens:,} ({total_tokens/1_000_000:.2f}M)")
    print(f"\nCost estimates (GPT-3.5-turbo pricing):")
    print(f"  Input cost: ${input_cost:.2f}")
    print(f"  Output cost: ${output_cost:.2f}")
    print(f"  TOTAL ESTIMATED COST: ${total_cost:.2f}")
    print("\n" + "="*70)
    print("\nNote: Actual costs may vary based on:")
    print("  - Actual token usage per request")
    print("  - Proxy provider markup (if any)")
    print("  - Rate limits and retries")
    print("  - API pricing changes")
    print("\nRecommendation: Start with a small batch to verify actual costs.")


def analyze_previous_usage() -> None:
    """Analyze previous API usage from processed algorithms."""
    import sqlite3
    
    db_path = ROOT / "database" / "algorithm_prompts.db"
    
    if not db_path.exists():
        print("\nNo previous usage data found.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
        processed_count = cursor.fetchone()[0]
        
        print("\n" + "="*70)
        print("PREVIOUS PROCESSING STATISTICS")
        print("="*70)
        print(f"\nAlgorithms processed: {processed_count}")
        print(f"Prompts generated: {processed_count * 4}")
        print("\nNote: This shows prompts saved to database.")
        print("Actual API calls may differ if some failed.")
        
        conn.close()
        
    except Exception as e:
        print(f"\nError reading database: {e}")


if __name__ == "__main__":
    print("="*70)
    print("API BALANCE & COST ESTIMATION")
    print("="*70)
    
    check_balance()
    analyze_previous_usage()
    estimate_costs()

