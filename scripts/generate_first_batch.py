#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find first batch of files needing content generation."""

from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithm_prompts.db"

files_to_gen = []
for algo_dir in sorted(ROOT.glob('semester_*/lecture_*/*')):
    if not algo_dir.is_dir() or algo_dir.name.startswith('.'):
        continue
    for md in ['univer.en.md', 'school.en.md', 'univer.ru.md', 'school.ru.md']:
        md_file = algo_dir / md
        if md_file.exists():
            try:
                content = md_file.read_text(encoding='utf-8')
                if 'This file is queued for content generation' in content or 'AI-Generated Content' in content:
                    files_to_gen.append((md_file, algo_dir.name, md))
                    if len(files_to_gen) >= 10:
                        break
            except:
                pass
    if len(files_to_gen) >= 10:
        break

print('First 10 files to generate:')
for i, (md_file, algo_name, md) in enumerate(files_to_gen[:10], 1):
    print(f'{i}. {md_file} ({algo_name})')

