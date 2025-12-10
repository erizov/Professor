#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze API usage and costs broken down by level (school/univer) and language (en/ru).
"""

import sys
import sqlite3
from pathlib import Path
from collections import defaultdict

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def analyze_existing_files() -> dict:
    """Analyze existing MD files to get actual token usage."""
    stats = {
        'school': {'en': [], 'ru': []},
        'univer': {'en': [], 'ru': []}
    }
    
    for level in ['school', 'univer']:
        for lang in ['en', 'ru']:
            pattern = f"semester_*/lecture_*/*/{level}.{lang}.md"
            for md_file in ROOT.glob(pattern):
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        char_count = len(content)
                        # Rough estimate: 1 token ≈ 4 characters
                        token_estimate = char_count / 4
                        stats[level][lang].append({
                            'file': md_file,
                            'chars': char_count,
                            'tokens': token_estimate
                        })
                except Exception as e:
                    pass
    
    return stats


def calculate_prompt_tokens() -> dict:
    """Estimate prompt tokens for each level/language combination."""
    # Sample prompts to estimate
    sample_prompts = {
        'school_en': """Create a brief about the "Algorithm Name" algorithm for school students:

- Explain the principle of operation in very simple language.
- Specify the algorithm complexity in O-notation.
- Where is it used in practice.
- What can the algorithm be compared to.
- Minimal code example (only important parts).
- Common mistakes.
- Recommended literature.

Structure the brief using subheadings, lists, and short examples.""",
        
        'school_ru': """Составь бриф для школьников об алгоритме "Algorithm Name" (простыми словами):

- Объясни принцип работы очень простым языком.
- Укажи сложность алгоритма в O-нотации.
- Где применяется на практике.
- С чем можно сравнить алгоритм.
- Минимальный пример кода (только важное).
- Частые ошибки.
- Рекомендуемая литература.

Структурируй бриф, используй подзаголовки, списки и короткие примеры.""",
        
        'univer_en': """Create a brief about the "Algorithm Name" algorithm for college students:

- Specify convergence speed and complexity estimate in O-notation.
- Where the algorithm is used in real frameworks and software.
- What it's similar to in concept.
- Which algorithms it's often used with.
- Key code (only important parts).
- Common application errors.
- Recommended literature.

Structure the brief using subheadings, lists, and short examples.""",
        
        'univer_ru': """Составь бриф для студентов колледжа об алгоритме "Algorithm Name":

- Укажи скорость схождения и оценку сложности по O-нотации.
- Где применяется алгоритм в реальных фреймворках и ПО.
- На что похож по идее.
- С какими алгоритмами часто используется.
- Приведи ключевой код (только важные части).
- Распространённые ошибки применения.
- Рекомендуемая литература.

Структурируй бриф, используй подзаголовки, списки и короткие примеры."""
    }
    
    prompt_tokens = {}
    for key, prompt in sample_prompts.items():
        # Estimate: 1 token ≈ 4 characters
        prompt_tokens[key] = len(prompt) / 4
    
    return prompt_tokens


def analyze_database() -> dict:
    """Get statistics from database."""
    db_path = ROOT / "database" / "algorithm_prompts.db"
    
    if not db_path.exists():
        return {'total': 0, 'algorithms': []}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT algorithm_name FROM algorithm_prompts")
    algorithms = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return {'total': total, 'algorithms': algorithms}


def calculate_costs_by_category() -> dict:
    """Calculate costs broken down by level and language."""
    algorithms_count = 680
    
    # Get actual token usage from existing files
    file_stats = analyze_existing_files()
    prompt_tokens = calculate_prompt_tokens()
    
    # Calculate averages from existing files
    response_tokens = {}
    for level in ['school', 'univer']:
        for lang in ['en', 'ru']:
            tokens_list = [f['tokens'] for f in file_stats[level][lang]]
            if tokens_list:
                response_tokens[f'{level}_{lang}'] = sum(tokens_list) / len(tokens_list)
            else:
                # Fallback estimates
                if level == 'school':
                    response_tokens[f'{level}_{lang}'] = 600 if lang == 'en' else 650
                else:
                    response_tokens[f'{level}_{lang}'] = 800 if lang == 'en' else 850
    
    # Pricing (GPT-3.5-turbo)
    input_price_per_million = 0.50
    output_price_per_million = 1.50
    
    results = {}
    
    for level in ['school', 'univer']:
        for lang in ['en', 'ru']:
            key = f'{level}_{lang}'
            prompt_token_count = prompt_tokens[key]
            response_token_count = response_tokens[key]
            
            # Per request
            input_tokens = prompt_token_count
            output_tokens = response_token_count
            total_tokens = input_tokens + output_tokens
            
            # Cost per request
            input_cost = (input_tokens / 1_000_000) * input_price_per_million
            output_cost = (output_tokens / 1_000_000) * output_price_per_million
            total_cost = input_cost + output_cost
            
            # For all algorithms
            total_requests = algorithms_count
            total_input_tokens = input_tokens * total_requests
            total_output_tokens = output_tokens * total_requests
            total_category_cost = total_cost * total_requests
            
            results[key] = {
                'level': level,
                'language': lang,
                'prompt_tokens': prompt_token_count,
                'response_tokens': response_token_count,
                'total_tokens_per_request': total_tokens,
                'cost_per_request': total_cost,
                'total_requests': total_requests,
                'total_input_tokens': total_input_tokens,
                'total_output_tokens': total_output_tokens,
                'total_cost': total_category_cost
            }
    
    return results


def print_detailed_analysis() -> None:
    """Print detailed analysis."""
    print("="*70)
    print("DETAILED USAGE & COST ANALYSIS BY LEVEL AND LANGUAGE")
    print("="*70)
    
    # Database stats
    db_stats = analyze_database()
    print(f"\n[Database] Algorithms processed: {db_stats['total']}")
    
    # File stats
    file_stats = analyze_existing_files()
    print(f"\n[Files] Existing MD files:")
    for level in ['school', 'univer']:
        for lang in ['en', 'ru']:
            count = len(file_stats[level][lang])
            if count > 0:
                avg_tokens = sum(f['tokens'] for f in file_stats[level][lang]) / count
                print(f"  {level}.{lang}: {count} files, avg {avg_tokens:.0f} tokens")
    
    # Cost breakdown
    costs = calculate_costs_by_category()
    
    print("\n" + "="*70)
    print("COST BREAKDOWN BY CATEGORY")
    print("="*70)
    
    total_cost = 0
    total_tokens_input = 0
    total_tokens_output = 0
    
    for key in ['school_en', 'school_ru', 'univer_en', 'univer_ru']:
        data = costs[key]
        total_cost += data['total_cost']
        total_tokens_input += data['total_input_tokens']
        total_tokens_output += data['total_output_tokens']
        
        print(f"\n[{data['level'].upper()}.{data['language'].upper()}]")
        print(f"  Prompt tokens: {data['prompt_tokens']:.0f}")
        print(f"  Response tokens: {data['response_tokens']:.0f}")
        print(f"  Total tokens per request: {data['total_tokens_per_request']:.0f}")
        print(f"  Cost per request: ${data['cost_per_request']:.4f}")
        print(f"  Total requests: {data['total_requests']:,}")
        print(f"  Total input tokens: {data['total_input_tokens']:,.0f} ({data['total_input_tokens']/1_000_000:.3f}M)")
        print(f"  Total output tokens: {data['total_output_tokens']:,.0f} ({data['total_output_tokens']/1_000_000:.3f}M)")
        print(f"  Total cost: ${data['total_cost']:.2f}")
    
    print("\n" + "="*70)
    print("SUMMARY TOTALS")
    print("="*70)
    print(f"\nTotal algorithms: 680")
    print(f"Total prompts: 2,720 (680 × 4)")
    print(f"\nTotal input tokens: {total_tokens_input:,.0f} ({total_tokens_input/1_000_000:.3f}M)")
    print(f"Total output tokens: {total_tokens_output:,.0f} ({total_tokens_output/1_000_000:.3f}M)")
    print(f"Total tokens: {total_tokens_input + total_tokens_output:,.0f} ({(total_tokens_input + total_tokens_output)/1_000_000:.3f}M)")
    print(f"\nTOTAL ESTIMATED COST: ${total_cost:.2f}")
    
    print("\n" + "="*70)
    print("BREAKDOWN BY LEVEL")
    print("="*70)
    
    school_cost = costs['school_en']['total_cost'] + costs['school_ru']['total_cost']
    univer_cost = costs['univer_en']['total_cost'] + costs['univer_ru']['total_cost']
    
    print(f"\nSchool level (en + ru):")
    print(f"  Total cost: ${school_cost:.2f}")
    print(f"  Percentage: {school_cost/total_cost*100:.1f}%")
    
    print(f"\nUniversity level (en + ru):")
    print(f"  Total cost: ${univer_cost:.2f}")
    print(f"  Percentage: {univer_cost/total_cost*100:.1f}%")
    
    print("\n" + "="*70)
    print("BREAKDOWN BY LANGUAGE")
    print("="*70)
    
    en_cost = costs['school_en']['total_cost'] + costs['univer_en']['total_cost']
    ru_cost = costs['school_ru']['total_cost'] + costs['univer_ru']['total_cost']
    
    print(f"\nEnglish (school + univer):")
    print(f"  Total cost: ${en_cost:.2f}")
    print(f"  Percentage: {en_cost/total_cost*100:.1f}%")
    
    print(f"\nRussian (school + univer):")
    print(f"  Total cost: ${ru_cost:.2f}")
    print(f"  Percentage: {ru_cost/total_cost*100:.1f}%")
    
    print("\n" + "="*70)
    print("COST PER ITEM")
    print("="*70)
    print(f"\nCost per algorithm (all 4 prompts): ${total_cost/680:.4f}")
    print(f"Cost per prompt: ${total_cost/2720:.4f}")
    print(f"\nCost per school.en prompt: ${costs['school_en']['cost_per_request']:.4f}")
    print(f"Cost per school.ru prompt: ${costs['school_ru']['cost_per_request']:.4f}")
    print(f"Cost per univer.en prompt: ${costs['univer_en']['cost_per_request']:.4f}")
    print(f"Cost per univer.ru prompt: ${costs['univer_ru']['cost_per_request']:.4f}")


if __name__ == "__main__":
    print_detailed_analysis()

