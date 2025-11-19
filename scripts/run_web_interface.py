#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run web interface for algorithm course.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Check if database exists
DB_PATH = ROOT / "database" / "algorithms.db"
if not DB_PATH.exists():
    print("Database not found. Populating database...")
    from database.populate_database import populate_database

    populate_database()

# Run Flask app
from web_interface.app import app

if __name__ == "__main__":
    print("Starting web interface...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host="0.0.0.0", port=5000)
