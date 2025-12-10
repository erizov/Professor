#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find files that need content generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

files_to_gen = []
processing_order = ['univer.en.md', 'school.en.md', 'univer.ru.md', 'school.ru.md']

for algo_dir in sorted(ROOT.glob('semester_*/lecture_*/*')):
    if not algo_dir.is_dir() or algo_dir.name.startswith('.'):
        continue
    
    for md_name in processing_order:
        md_file = algo_dir / md_name
        if md_file.exists():
            try:
                content = md_file.read_text(encoding='utf-8')
                if 'This file is queued for content generation' in content or 'AI-Generated Content' in content:
                    files_to_gen.append((md_file, algo_dir.name, md_name))
            except:
                pass

print(f'Found {len(files_to_gen)} files needing content generation')
print('\nFirst 20 files:')
for i, (md_file, algo_name, md_name) in enumerate(files_to_gen[:20], 1):
    print(f'{i}. {algo_name}/{md_name}')

