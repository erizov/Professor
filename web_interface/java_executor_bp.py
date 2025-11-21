#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web interface blueprint for Java algorithm execution.
"""

from flask import Blueprint, request, jsonify
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.java_executor import get_executor

java_executor_bp = Blueprint('java_executor', __name__, url_prefix='/api/java')


@java_executor_bp.route('/algorithms', methods=['GET'])
def list_algorithms():
    """List all available Java algorithms."""
    try:
        executor = get_executor()
        semester = request.args.get('semester')
        lecture = request.args.get('lecture')
        
        algorithms = executor.list_algorithms(
            semester=semester,
            lecture=lecture
        )
        
        return jsonify({
            'success': True,
            'algorithms': algorithms,
            'count': len(algorithms)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@java_executor_bp.route('/execute', methods=['POST'])
def execute_algorithm():
    """Execute a Java algorithm."""
    try:
        data = request.get_json()
        
        # Get algorithm identifier
        path = data.get('path')
        semester = data.get('semester')
        lecture = data.get('lecture')
        algorithm = data.get('algorithm')
        timeout = data.get('timeout', 60)
        input_data = data.get('input')
        
        executor = get_executor()
        
        # Find algorithm
        algo_info = executor.find_algorithm(
            path=path,
            semester=semester,
            lecture=lecture,
            algorithm=algorithm
        )
        
        if not algo_info:
            return jsonify({
                'success': False,
                'error': 'Algorithm not found'
            }), 404
        
        # Execute
        success, stdout, stderr, execution_time = executor.execute_algorithm(
            algo_info,
            timeout=timeout,
            input_data=input_data
        )
        
        return jsonify({
            'success': success,
            'stdout': stdout,
            'stderr': stderr,
            'execution_time': execution_time,
            'algorithm': {
                'name': algo_info.name,
                'path': algo_info.full_path,
                'package': algo_info.package or '',
                'class_name': algo_info.class_name
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@java_executor_bp.route('/info/<path:algorithm_path>', methods=['GET'])
def get_algorithm_info(algorithm_path):
    """Get information about a specific algorithm."""
    try:
        executor = get_executor()
        
        algo_info = executor.find_algorithm(path=algorithm_path)
        
        if not algo_info:
            return jsonify({
                'success': False,
                'error': 'Algorithm not found'
            }), 404
        
        return jsonify({
            'success': True,
            'algorithm': {
                'name': algo_info.name,
                'path': algo_info.full_path,
                'package': algo_info.package or '',
                'class_name': algo_info.class_name,
                'semester': algo_info.semester,
                'lecture': algo_info.lecture,
                'algorithm': algo_info.algorithm
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@java_executor_bp.route('/source/<path:algorithm_path>', methods=['GET'])
def get_algorithm_source(algorithm_path):
    """Get Java source code for an algorithm."""
    try:
        executor = get_executor()
        
        # Normalize path separators (handle both / and \)
        normalized_path = algorithm_path.replace('\\', '/')
        
        # Try to find algorithm with normalized path
        algo_info = executor.find_algorithm(path=normalized_path)
        
        # If not found, try with original path
        if not algo_info:
            algo_info = executor.find_algorithm(path=algorithm_path)
        
        # If still not found, try finding by matching full_path
        if not algo_info:
            algorithms = executor.discover_algorithms()
            for algo in algorithms:
                # Compare normalized paths
                algo_path_normalized = algo.full_path.replace('\\', '/')
                if algo_path_normalized == normalized_path or algo.full_path == algorithm_path:
                    algo_info = algo
                    break
        
        if not algo_info:
            return jsonify({
                'success': False,
                'error': f'Algorithm not found: {algorithm_path}'
            }), 404
        
        # Read Java file content
        try:
            source_code = algo_info.path.read_text(encoding='utf-8')
            return jsonify({
                'success': True,
                'source': source_code,
                'path': algo_info.full_path,
                'name': algo_info.name
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Could not read source file: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

