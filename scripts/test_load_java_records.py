#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test loading Java records from test_reports API."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from flask import Flask
from web_interface.test_reports import test_reports_bp

app = Flask(__name__)
app.register_blueprint(test_reports_bp)

print("=" * 80)
print("TESTING JAVA RECORDS LOADING")
print("=" * 80)
print()

# Test 1: Direct database query
print("Test 1: Direct database query")
print("-" * 80)
import sqlite3
conn = sqlite3.connect(ROOT / "test_results.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*) 
    FROM test_results 
    WHERE LOWER(language) = LOWER('java')
""")
java_count = cursor.fetchone()[0]
print(f"Total Java records in DB: {java_count}")

cursor.execute("""
    SELECT algorithm_path, language, status, timestamp
    FROM test_results 
    WHERE LOWER(language) = LOWER('java')
    ORDER BY timestamp DESC
    LIMIT 5
""")
print("\nSample Java records:")
for row in cursor.fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
conn.close()

print()
print("=" * 80)
print()

# Test 2: Using test_reports function with Flask test client
print("Test 2: Using Flask test client")
print("-" * 80)

with app.test_client() as client:
    # Test without filter
    print("\n2a. Request without language filter:")
    response = client.get('/api/test-results')
    if response.status_code == 200:
        data = response.get_json()
        results = data.get('results', [])
        java_results = [r for r in results if r.get('language', '').lower() == 'java']
        print(f"  Total results: {len(results)}")
        print(f"  Java results: {len(java_results)}")
        if java_results:
            print(f"  First Java result: {java_results[0].get('algorithm_path')} | {java_results[0].get('language')} | {java_results[0].get('latest_status')}")
        else:
            print("  ⚠ No Java results found!")
    else:
        print(f"  ❌ Error: {response.status_code}")
        print(f"  Response: {response.get_data(as_text=True)}")
    
    # Test with Java filter
    print("\n2b. Request with language=java filter:")
    response = client.get('/api/test-results?language=java')
    if response.status_code == 200:
        data = response.get_json()
        if 'error' in data:
            print(f"  ❌ Error: {data['error']}")
        else:
            results = data.get('results', [])
            print(f"  Total Java results: {len(results)}")
            if results:
                print(f"  First 3 results:")
                for i, r in enumerate(results[:3], 1):
                    print(f"    {i}. {r.get('algorithm_path')} | {r.get('language')} | {r.get('latest_status')}")
            else:
                print("  ⚠ No results returned!")
    else:
        print(f"  ❌ Error: {response.status_code}")
        print(f"  Response: {response.get_data(as_text=True)}")

print()
print("=" * 80)
print()

# Test 3: Direct function call
print("Test 3: Direct function call")
print("-" * 80)

from web_interface.test_reports import get_test_results
from flask import Flask

test_app = Flask(__name__)

with test_app.test_request_context('/api/test-results?language=java'):
    try:
        result = get_test_results()
        if isinstance(result, tuple):
            # It's a tuple (response, status_code)
            response, status_code = result
            if status_code == 200:
                data = response.get_json()
                if 'error' in data:
                    print(f"  ❌ Error: {data['error']}")
                else:
                    results = data.get('results', [])
                    print(f"  Total Java results: {len(results)}")
                    if results:
                        print(f"  First 3 results:")
                        for i, r in enumerate(results[:3], 1):
                            print(f"    {i}. {r.get('algorithm_path')} | {r.get('language')} | {r.get('latest_status')}")
                    else:
                        print("  ⚠ No results returned!")
            else:
                print(f"  ❌ Status code: {status_code}")
                data = response.get_json()
                print(f"  Error: {data.get('error', 'Unknown error')}")
        else:
            # It's a response object
            data = result.get_json()
            if 'error' in data:
                print(f"  ❌ Error: {data['error']}")
            else:
                results = data.get('results', [])
                print(f"  Total Java results: {len(results)}")
                if results:
                    print(f"  First 3 results:")
                    for i, r in enumerate(results[:3], 1):
                        print(f"    {i}. {r.get('algorithm_path')} | {r.get('language')} | {r.get('latest_status')}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 80)
print("TEST COMPLETE")
print("=" * 80)

