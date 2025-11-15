#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Interface for Algorithms Course.

Flask application to browse and execute algorithms.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def scan_algorithms() -> List[Dict[str, Any]]:
    """
    Scan all semesters and collect algorithm information.
    
    Returns:
        List of algorithm dictionaries
    """
    algorithms = []
    base_path = Path(__file__).parent.parent
    
    for semester in range(1, 5):
        semester_path = base_path / f"semester_{semester}"
        if not semester_path.exists():
            continue
            
        for lecture_path in sorted(semester_path.iterdir()):
            if not lecture_path.is_dir():
                continue
                
            for algo_path in sorted(lecture_path.iterdir()):
                if not algo_path.is_dir():
                    continue
                    
                metadata_file = algo_path / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', 
                             encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    metadata['semester'] = semester
                    metadata['lecture'] = lecture_path.name
                    metadata['algorithm'] = algo_path.name
                    metadata['path'] = str(
                        algo_path.relative_to(base_path)
                    )
                    algorithms.append(metadata)
    
    return algorithms


@app.route('/')
def index() -> str:
    """Render main page."""
    return render_template('index.html')


@app.route('/api/algorithms')
def get_algorithms() -> Any:
    """Get all algorithms with metadata."""
    try:
        algorithms = scan_algorithms()
        return jsonify(algorithms)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run', methods=['POST'])
def run_algorithm() -> Any:
    """Execute an algorithm."""
    data = request.json
    semester = data.get('semester')
    lecture = data.get('lecture')
    algorithm = data.get('algorithm')
    language = data.get('language', 'python')
    
    if not all([semester, lecture, algorithm]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    try:
        cmd = [
            sys.executable,
            'runner.py',
            '--semester', str(semester),
            '--lecture', lecture,
            '--algorithm', algorithm,
            '--lang', language
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timeout'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/readme/<path:algorithm_path>')
def get_readme(algorithm_path: str) -> Any:
    """Get README content for an algorithm."""
    try:
        base_path = Path(__file__).parent.parent
        readme_path = base_path / algorithm_path / "README.md"
        
        if not readme_path.exists():
            return jsonify({'error': 'README not found'}), 404
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

