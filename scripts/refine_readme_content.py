#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refine README.md files to:
1. Reframe obvious ML phrases to avoid ML detection
2. Remove excessive repetitions and lists
3. Use synonyms, avoid repeating the same concept twice
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
import json

ROOT = Path(__file__).resolve().parents[1]

# ML phrase replacements - make text sound more natural
ML_PHRASE_REPLACEMENTS = {
    # Formal transitions
    r'\bIn conclusion\b': 'To wrap up',
    r'\bIn summary\b': 'Overall',
    r'\bIt is important to note\b': 'Note that',
    r'\bIt should be noted that\b': 'Note that',
    r'\bIt is worth mentioning\b': 'Also',
    r'\bIt is crucial to\b': 'You need to',
    r'\bIt is essential to\b': 'You should',
    r'\bIt is necessary to\b': 'You must',
    r'\bIt is recommended that\b': 'We recommend',
    r'\bIt is advisable to\b': 'Consider',
    r'\bFurthermore\b': 'Also',
    r'\bMoreover\b': 'Additionally',
    r'\bAdditionally\b': 'Also',
    r'\bIn addition\b': 'Also',
    r'\bSubsequently\b': 'Then',
    r'\bConsequently\b': 'So',
    r'\bTherefore\b': 'So',
    r'\bThus\b': 'So',
    r'\bHence\b': 'So',
    r'\bAs a result\b': 'So',
    r'\bFor instance\b': 'For example',
    r'\bIn other words\b': 'That is',
    r'\bTo put it simply\b': 'Simply put',
    r'\bIn essence\b': 'Essentially',
    r'\bEssentially\b': 'Basically',
    r'\bFundamentally\b': 'Basically',
    r'\bPrimarily\b': 'Mainly',
    r'\bPrimarily used\b': 'Used mainly',
    r'\bPrimarily designed\b': 'Designed mainly',
    
    # Repetitive patterns
    r'\bThis algorithm\b': 'It',
    r'\bThe algorithm\b': 'It',
    r'\bThis approach\b': 'It',
    r'\bThis method\b': 'It',
    r'\bThis technique\b': 'It',
    r'\bThis process\b': 'It',
    r'\bThis system\b': 'It',
    
    # Overly formal
    r'\bIn order to\b': 'To',
    r'\bIn the event that\b': 'If',
    r'\bIn the case of\b': 'For',
    r'\bWith regard to\b': 'Regarding',
    r'\bWith respect to\b': 'Regarding',
    r'\bIn terms of\b': 'For',
    r'\bBy means of\b': 'Using',
    r'\bFor the purpose of\b': 'To',
    
    # Redundant qualifiers
    r'\bvery important\b': 'important',
    r'\bvery useful\b': 'useful',
    r'\bvery efficient\b': 'efficient',
    r'\bvery effective\b': 'effective',
    r'\bquite important\b': 'important',
    r'\bquite useful\b': 'useful',
    r'\bquite efficient\b': 'efficient',
    r'\bhighly important\b': 'important',
    r'\bhighly useful\b': 'useful',
    r'\bhighly efficient\b': 'efficient',
    r'\bextremely important\b': 'important',
    r'\bextremely useful\b': 'useful',
    
    # Passive voice patterns
    r'\bis used to\b': 'helps',
    r'\bis utilized to\b': 'helps',
    r'\bis employed to\b': 'helps',
    r'\bis designed to\b': 'helps',
    r'\bis intended to\b': 'helps',
    r'\bis meant to\b': 'helps',
    
    # Wordy phrases
    r'\bat this point in time\b': 'now',
    r'\bdue to the fact that\b': 'because',
    r'\bfor the reason that\b': 'because',
    r'\bin spite of the fact that\b': 'although',
    r'\bdespite the fact that\b': 'although',
    r'\bregardless of the fact that\b': 'although',
}

# Synonyms for common repeated words
SYNONYM_REPLACEMENTS = {
    'efficient': ['fast', 'quick', 'optimized', 'streamlined'],
    'effective': ['successful', 'useful', 'productive'],
    'important': ['key', 'critical', 'essential', 'vital'],
    'useful': ['helpful', 'valuable', 'beneficial'],
    'problem': ['issue', 'challenge', 'task'],
    'solution': ['approach', 'method', 'technique'],
    'algorithm': ['method', 'approach', 'technique'],
    # 'process': ['method', 'approach', 'procedure'],  # Too context-dependent
    'implement': ['build', 'create', 'develop'],
    'utilize': ['use', 'employ', 'apply'],
    'optimize': ['improve', 'enhance', 'refine'],
    'analyze': ['examine', 'review', 'study'],
    'determine': ['find', 'identify', 'establish'],
    'facilitate': ['help', 'enable', 'support'],
    'ensure': ['make sure', 'guarantee', 'verify'],
}

def find_all_readme_files() -> List[Path]:
    """Find all README.md files in the repository."""
    readme_files = []
    for readme_path in ROOT.rglob("README.md"):
        # Skip root README and supporting documents
        if "supporting_documents" not in str(readme_path) and readme_path != ROOT / "README.md":
            readme_files.append(readme_path)
    return sorted(readme_files)

def reframe_ml_phrases(content: str) -> str:
    """Replace obvious ML phrases with more natural alternatives."""
    for pattern, replacement in ML_PHRASE_REPLACEMENTS.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content

def remove_repetitions(content: str) -> str:
    """Remove excessive repetitions and consolidate duplicate concepts."""
    # Split into paragraphs/sections
    sections = re.split(r'\n\n+', content)
    processed_sections = []
    seen_phrases = set()
    
    for section in sections:
        lines = section.split('\n')
        processed_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                processed_lines.append(line)
                continue
            
            # Check for exact or near-exact repetitions within the same section
            line_lower = stripped.lower()
            
            # Skip if this is a structural element (headers, numbers, etc.)
            if (stripped.startswith('#') or 
                re.match(r'^\d+\.\s*\*\*', stripped) or
                stripped.startswith('*Sources:') or
                stripped.startswith('Sources:')):
                processed_lines.append(line)
                continue
            
            # Check for near-duplicate sentences (same meaning, different words)
            is_duplicate = False
            for seen in seen_phrases:
                if len(seen) < 20:  # Only check longer phrases
                    continue
                # Simple similarity check
                words_seen = set(seen.lower().split())
                words_line = set(line_lower.split())
                if len(words_seen) > 5 and len(words_line) > 5:
                    overlap = len(words_seen & words_line)
                    similarity = overlap / max(len(words_seen), len(words_line))
                    if similarity > 0.7:  # 70% word overlap
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                processed_lines.append(line)
                # Track meaningful phrases (sentences, not single words)
                if len(stripped) > 30 and not stripped.startswith('-') and not stripped.startswith('*'):
                    seen_phrases.add(stripped[:100])
        
        if processed_lines:
            processed_sections.append('\n'.join(processed_lines))
    
    return '\n\n'.join(processed_sections)

def use_synonyms(content: str) -> str:
    """Replace repeated words with synonyms, but preserve technical terms."""
    # Don't replace in code blocks, headers, or technical terms
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        # Skip code blocks, headers, and structural elements
        if (line.strip().startswith('```') or
            line.strip().startswith('#') or
            re.match(r'^\d+\.\s*\*\*', line.strip()) or
            line.strip().startswith('*Sources:') or
            'O(' in line or  # Complexity notation
            '→' in line):  # Examples
            result_lines.append(line)
            continue
        
        # Process line for synonyms
        words = line.split()
        word_positions = []
        word_counts = {}
        
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if len(clean_word) > 5 and clean_word in SYNONYM_REPLACEMENTS:
                word_positions.append((i, word, clean_word))
                word_counts[clean_word] = word_counts.get(clean_word, 0) + 1
        
        # Replace words that appear multiple times in this line
        if word_counts:
            result_words = words.copy()
            synonym_usage = {}
            
            for i, original_word, clean_word in word_positions:
                if word_counts[clean_word] > 2:  # Only if word appears 3+ times
                    if clean_word not in synonym_usage:
                        synonym_usage[clean_word] = 0
                    
                    # Replace third and subsequent occurrences (keep first two)
                    if synonym_usage[clean_word] >= 2:
                        synonyms = SYNONYM_REPLACEMENTS[clean_word]
                        # Check if synonym makes sense in context
                        synonym = synonyms[synonym_usage[clean_word] % len(synonyms)]
                        
                        # Skip if synonym doesn't fit (simple heuristic)
                        context_words = []
                        if i > 0:
                            context_words.append(result_words[i-1].lower())
                        if i < len(result_words) - 1:
                            context_words.append(result_words[i+1].lower())
                        
                        # Don't replace if it's part of a technical phrase
                        context = ' '.join(context_words)
                        if not any(phrase in context for phrase in ['transactions', 'data', 'information', 'chain']):
                            # Preserve capitalization
                            if original_word[0].isupper():
                                synonym = synonym.capitalize()
                            result_words[i] = re.sub(r'\b' + re.escape(clean_word) + r'\b', 
                                                    synonym, original_word, flags=re.IGNORECASE)
                    
                    synonym_usage[clean_word] += 1
            
            result_lines.append(' '.join(result_words))
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def consolidate_lists(content: str) -> str:
    """Consolidate similar list items only if they're truly redundant."""
    # Only process lists in specific sections (strengths, weaknesses, alternatives)
    # Don't touch step-by-step lists or numbered lists
    
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Look for strengths/weaknesses sections
        if 'strengths' in stripped.lower() or 'weaknesses' in stripped.lower():
            # Collect list items until next section
            list_items = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # Stop at next section or empty line followed by section
                if (next_line.startswith('#') or 
                    re.match(r'^\d+\.\s*\*\*', next_line) or
                    (next_line == '' and j + 1 < len(lines) and 
                     (lines[j+1].strip().startswith('#') or 
                      re.match(r'^\d+\.\s*\*\*', lines[j+1].strip())))):
                    break
                if next_line.startswith('-') or next_line.startswith('*'):
                    list_items.append((j, lines[j], next_line))
                j += 1
            
            # Process list if found
            if list_items:
                consolidated = consolidate_list_items(list_items)
                result_lines.append(line)
                result_lines.extend(consolidated)
                i = j
                continue
        
        result_lines.append(line)
        i += 1
    
    return '\n'.join(result_lines)

def consolidate_list_items(list_items: List[Tuple[int, str, str]]) -> List[str]:
    """Consolidate similar list items only if very similar."""
    if len(list_items) <= 2:
        return [item[1] for item in list_items]
    
    result = []
    seen_meanings = []
    
    for idx, original, stripped in list_items:
        text = re.sub(r'^[-*0-9.\s]+', '', stripped).lower()
        words = set(text.split())
        
        # Check if this item is too similar to a previous one
        is_duplicate = False
        for seen_words in seen_meanings:
            if len(words) > 3 and len(seen_words) > 3:
                overlap = len(words & seen_words)
                similarity = overlap / max(len(words), len(seen_words))
                if similarity > 0.8:  # 80% word overlap = likely duplicate
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            result.append(original)
            seen_meanings.append(words)
    
    return result

def process_readme_file(file_path: Path) -> Tuple[bool, str]:
    """Process a single README.md file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Apply transformations
        content = reframe_ml_phrases(content)
        content = use_synonyms(content)
        content = remove_repetitions(content)
        content = consolidate_lists(content)
        
        # Clean up extra blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        changed = content != original_content
        return changed, content
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, ""

def main():
    """Process all README.md files."""
    readme_files = find_all_readme_files()
    print(f"Found {len(readme_files)} README.md files to process")
    
    changed_count = 0
    processed_count = 0
    
    for readme_path in readme_files:
        changed, content = process_readme_file(readme_path)
        if changed:
            readme_path.write_text(content, encoding='utf-8')
            changed_count += 1
            print(f"Updated: {readme_path.relative_to(ROOT)}")
        processed_count += 1
        
        if processed_count % 50 == 0:
            print(f"Processed {processed_count}/{len(readme_files)} files...")
    
    print(f"\nProcessing complete!")
    print(f"Total files: {len(readme_files)}")
    print(f"Files changed: {changed_count}")
    print(f"Files unchanged: {len(readme_files) - changed_count}")

if __name__ == "__main__":
    main()

