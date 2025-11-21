#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web interface blueprint for unified algorithm execution (Java and Python).
"""

from flask import Blueprint, request, jsonify
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.java_executor import get_executor as get_java_executor
from framework.python_executor import get_executor as get_python_executor

algorithm_executor_bp = Blueprint('algorithm_executor', __name__, url_prefix='/api/algorithm')


@algorithm_executor_bp.route('/algorithms', methods=['GET'])
def list_algorithms():
    """List all available algorithms (Java and Python)."""
    try:
        language = request.args.get('language', '').lower()  # 'java', 'python', or '' for all
        semester = request.args.get('semester')
        lecture = request.args.get('lecture')
        
        all_algorithms = []
        
        # Get Java algorithms
        if not language or language == 'java':
            java_executor = get_java_executor()
            java_algorithms = java_executor.list_algorithms(
                semester=semester,
                lecture=lecture
            )
            for algo in java_algorithms:
                algo['language'] = 'java'
            all_algorithms.extend(java_algorithms)
        
        # Get Python algorithms
        if not language or language == 'python':
            python_executor = get_python_executor()
            python_algorithms = python_executor.list_algorithms(
                semester=semester,
                lecture=lecture
            )
            for algo in python_algorithms:
                algo['language'] = 'python'
            all_algorithms.extend(python_algorithms)
        
        return jsonify({
            'success': True,
            'algorithms': all_algorithms,
            'count': len(all_algorithms)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@algorithm_executor_bp.route('/execute', methods=['POST'])
def execute_algorithm():
    """Execute an algorithm (Java or Python)."""
    try:
        data = request.get_json()
        
        # Get algorithm identifier
        path = data.get('path')
        language = data.get('language', '').lower()  # 'java' or 'python'
        semester = data.get('semester')
        lecture = data.get('lecture')
        algorithm = data.get('algorithm')
        timeout = data.get('timeout', 60)
        input_data = data.get('input')
        
        if not language:
            return jsonify({
                'success': False,
                'error': 'Language must be specified (java or python)'
            }), 400
        
        # Find and execute based on language
        if language == 'java':
            executor = get_java_executor()
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
                    'language': 'java',
                    'package': algo_info.package or '',
                    'class_name': algo_info.class_name
                }
            })
        
        elif language == 'python':
            executor = get_python_executor()
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
                    'language': 'python',
                    'module_name': algo_info.module_name or '',
                    'function_name': algo_info.function_name or '',
                    'class_name': algo_info.class_name or ''
                }
            })
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported language: {language}'
            }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@algorithm_executor_bp.route('/source/<language>/<path:algorithm_path>', methods=['GET'])
def get_algorithm_source(language, algorithm_path):
    """Get source code for an algorithm (Java or Python)."""
    try:
        language = language.lower()
        
        if language == 'java':
            executor = get_java_executor()
        elif language == 'python':
            executor = get_python_executor()
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported language: {language}'
            }), 400
        
        # Normalize path separators (handle both Windows \ and Unix /)
        normalized_path = algorithm_path.replace('\\', '/')
        
        # Try multiple path variations
        path_variations = [
            normalized_path,
            algorithm_path,
            normalized_path.replace('semester_', 'semester_0') if 'semester_' in normalized_path and len(normalized_path.split('semester_')[1].split('/')[0]) == 1 else None,
            normalized_path.replace('semester_0', 'semester_') if 'semester_0' in normalized_path else None,
        ]
        path_variations = [p for p in path_variations if p]  # Remove None values
        
        algo_info = None
        for path_var in path_variations:
            # Try to find algorithm with current path variation
            algo_info = executor.find_algorithm(path=path_var)
            if algo_info:
                break
            
            # Try finding by matching full_path
            algorithms = executor.discover_algorithms()
            for algo in algorithms:
                algo_path_normalized = algo.full_path.replace('\\', '/')
                if (algo_path_normalized == path_var or 
                    algo.full_path == path_var or
                    algo_path_normalized.endswith(path_var) or
                    path_var.endswith(algo_path_normalized)):
                    algo_info = algo
                    break
            if algo_info:
                break
        
        if not algo_info:
            return jsonify({
                'success': False,
                'error': f'Algorithm not found: {algorithm_path}'
            }), 404
        
        # Read source file
        try:
            source_code = algo_info.path.read_text(encoding='utf-8')
            return jsonify({
                'success': True,
                'source': source_code,
                'path': algo_info.full_path,
                'name': algo_info.name,
                'language': language
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

