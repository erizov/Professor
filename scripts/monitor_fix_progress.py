#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor progress of fix scripts.
"""

import sqlite3
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_status():
    """Get current test status."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Java status
    cursor.execute("""
        SELECT COUNT(DISTINCT algorithm_path) 
        FROM test_results 
        WHERE language = ? AND status = ?
    """, ('java', 'success'))
    java_success = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(DISTINCT algorithm_path) 
        FROM test_results 
        WHERE language = ? AND status IN (?, ?)
    """, ('java', 'failure', 'error'))
    java_fail = cursor.fetchone()[0]
    
    # Python status
    cursor.execute("""
        SELECT COUNT(DISTINCT algorithm_path) 
        FROM test_results 
        WHERE language = ? AND status = ?
    """, ('python', 'success'))
    py_success = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(DISTINCT algorithm_path) 
        FROM test_results 
        WHERE language = ? AND status IN (?, ?)
    """, ('python', 'failure', 'error'))
    py_fail = cursor.fetchone()[0]
    
    # Recent activity (last 2 minutes)
    cursor.execute("""
        SELECT language, status, COUNT(*) 
        FROM test_results 
        WHERE timestamp > datetime('now', '-2 minutes')
        GROUP BY language, status
    """)
    recent = cursor.fetchall()
    
    conn.close()
    
    return {
        'java': {'success': java_success, 'fail': java_fail},
        'python': {'success': py_success, 'fail': py_fail},
        'recent': recent
    }


def main():
    """Monitor progress."""
    print("=" * 70)
    print("FIX SCRIPTS PROGRESS MONITOR")
    print("=" * 70)
    print()
    
    prev_status = None
    
    try:
        while True:
            status = get_status()
            
            # Only print if status changed
            if status != prev_status:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Current Status:")
                print(f"  Java:   {status['java']['success']:3d} success, {status['java']['fail']:3d} failures/errors")
                print(f"  Python: {status['python']['success']:3d} success, {status['python']['fail']:3d} failures/errors")
                
                if status['recent']:
                    print("  Recent activity (last 2 min):")
                    for lang, stat, count in status['recent']:
                        print(f"    {lang} - {stat}: {count}")
                
                prev_status = status
            
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    main()

