#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug test_reports API endpoint."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from web_interface.test_reports import get_test_results
from flask import Flask
from flask.testing import FlaskClient

app = Flask(__name__)
app.register_blueprint(get_test_results.__self__)

# Test with different filters
with app.test_request_context('/api/test-results?language=java'):
    try:
        result = get_test_results()
        print("=" * 80)
        print("TEST WITH language=java")
        print("=" * 80)
        print(f"Status Code: {result[1] if isinstance(result, tuple) else 200}")
        if isinstance(result, tuple):
            import json
            data = json.loads(result[0].data)
            print(f"Results count: {len(data.get('results', []))}")
            if data.get('error'):
                print(f"Error: {data['error']}")
            else:
                print(f"First 3 results:")
                for r in data.get('results', [])[:3]:
                    print(f"  - {r.get('algorithm_path')} | {r.get('language')} | {r.get('latest_status')}")
        else:
            import json
            data = json.loads(result.data)
            print(f"Results count: {len(data.get('results', []))}")
            if data.get('error'):
                print(f"Error: {data['error']}")
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

