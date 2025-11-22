#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate algorithm_type for existing algorithms in the database.
"""

import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def classify_algorithm_type_from_path(folder_path: str) -> str:
    """Classify algorithm type from folder path."""
    path_lower = folder_path.lower().replace('\\', '/')
    
    # Extract lecture name from path
    parts = path_lower.split('/')
    lecture_name = None
    algorithm_name = None
    
    if len(parts) >= 2:
        lecture_name = parts[-2] if len(parts) >= 2 else None
        algorithm_name = parts[-1] if parts else None
    
    # Classification based on lecture name and algorithm name
    if lecture_name:
        if 'sorting' in lecture_name or 'sort' in lecture_name:
            return 'sorting'
        elif 'search' in lecture_name:
            return 'searching'
        elif 'graph' in lecture_name:
            return 'graph_algorithms'
        elif 'dynamic_programming' in lecture_name or 'dp' in lecture_name:
            return 'dynamic_programming'
        elif 'greedy' in lecture_name:
            return 'greedy'
        elif 'heap' in lecture_name or 'priority' in lecture_name:
            return 'data_structure'
        elif 'tree' in lecture_name:
            return 'data_structure'
        elif 'string' in lecture_name:
            return 'string_algorithms'
        elif 'pattern' in lecture_name:
            return 'design_pattern'
        elif 'distributed' in lecture_name:
            return 'distributed_systems'
        elif 'database' in lecture_name or 'db' in lecture_name or 'nosql' in lecture_name:
            return 'database'
        elif 'security' in lecture_name or 'cryptography' in lecture_name:
            return 'security'
        elif 'machine_learning' in lecture_name or 'ml' in lecture_name:
            return 'machine_learning'
        elif 'ai' in lecture_name or 'artificial_intelligence' in lecture_name:
            return 'artificial_intelligence'
        elif 'quantum' in lecture_name:
            return 'quantum_computing'
        elif 'cloud' in lecture_name:
            return 'cloud_computing'
        elif 'os' in lecture_name or 'operating_system' in lecture_name:
            return 'operating_systems'
        elif 'consensus' in lecture_name:
            return 'distributed_systems'
        elif 'cicd' in lecture_name:
            return 'devops'
        elif 'rag' in lecture_name:
            return 'ai'
        elif 'observability' in lecture_name:
            return 'devops'
        elif 'documentation' in lecture_name or 'knowledge' in lecture_name:
            return 'documentation'
        elif 'governance' in lecture_name:
            return 'data_governance'
    
    # Classification based on algorithm name
    if algorithm_name:
        if 'sort' in algorithm_name:
            return 'sorting'
        elif 'search' in algorithm_name:
            return 'searching'
        elif 'graph' in algorithm_name:
            return 'graph_algorithms'
        elif 'heap' in algorithm_name or 'priority' in algorithm_name:
            return 'data_structure'
        elif 'tree' in algorithm_name:
            return 'data_structure'
        elif 'hash' in algorithm_name:
            return 'data_structure'
        elif 'queue' in algorithm_name or 'stack' in algorithm_name:
            return 'data_structure'
    
    return 'fundamental'


def populate_algorithm_types():
    """Populate algorithm_type for all algorithms."""
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure algorithm_type column exists
    try:
        cursor.execute("ALTER TABLE algorithms ADD COLUMN algorithm_type TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Get all algorithms without algorithm_type
    cursor.execute("""
        SELECT id, folder_path, algorithm_type 
        FROM algorithms 
        WHERE algorithm_type IS NULL OR algorithm_type = ''
    """)
    
    algorithms = cursor.fetchall()
    print(f"Found {len(algorithms)} algorithms without algorithm_type")
    
    updated_count = 0
    for algo_id, folder_path, current_type in algorithms:
        algo_type = classify_algorithm_type_from_path(folder_path)
        
        cursor.execute("""
            UPDATE algorithms 
            SET algorithm_type = ? 
            WHERE id = ?
        """, (algo_type, algo_id))
        
        updated_count += 1
        if updated_count % 50 == 0:
            print(f"Updated {updated_count} algorithms...")
    
    conn.commit()
    conn.close()
    
    print(f"Successfully updated {updated_count} algorithms with algorithm_type")


if __name__ == "__main__":
    populate_algorithm_types()

