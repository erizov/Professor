#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Algorithm Execution Framework.

Provides a unified interface to execute any Python algorithm from a common place.
Supports both web interface and command-line usage.
"""

import subprocess
import re
import ast
import sys
from pathlib import Path
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class AlgorithmInfo:
    """Information about an algorithm."""
    name: str
    path: Path
    module_name: Optional[str]
    function_name: Optional[str]
    class_name: Optional[str]
    semester: str
    lecture: str
    algorithm: str
    full_path: str


class PythonExecutor:
    """Unified Python algorithm executor."""
    
    def __init__(self, root: Path = ROOT):
        """Initialize executor with project root."""
        self.root = root
        self._algorithm_cache: Optional[List[AlgorithmInfo]] = None
    
    def discover_algorithms(self, force_refresh: bool = False) -> List[AlgorithmInfo]:
        """Discover all algorithm.py files in the project."""
        if self._algorithm_cache is not None and not force_refresh:
            return self._algorithm_cache
        
        algorithms = []
        
        for semester_dir in sorted(self.root.glob("semester_*")):
            if not semester_dir.is_dir():
                continue
            
            semester_name = semester_dir.name
            
            for lecture_dir in sorted(semester_dir.glob("lecture_*")):
                if not lecture_dir.is_dir():
                    continue
                
                lecture_name = lecture_dir.name
                
                for algo_dir in sorted(lecture_dir.iterdir()):
                    if not algo_dir.is_dir():
                        continue
                    
                    python_file = algo_dir / "algorithm.py"
                    if not python_file.exists():
                        continue
                    
                    algorithm_name = algo_dir.name
                    
                    # Extract module, function, and class names
                    module_name = self._extract_module_name(python_file)
                    function_name = self._extract_main_function(python_file)
                    class_name = self._extract_main_class(python_file)
                    
                    # Get relative path
                    try:
                        relative_path = python_file.relative_to(self.root)
                    except ValueError:
                        relative_path = python_file
                    
                    info = AlgorithmInfo(
                        name=f"{semester_name}/{lecture_name}/{algorithm_name}",
                        path=python_file,
                        module_name=module_name,
                        function_name=function_name,
                        class_name=class_name,
                        semester=semester_name,
                        lecture=lecture_name,
                        algorithm=algorithm_name,
                        full_path=str(relative_path)
                    )
                    algorithms.append(info)
        
        if not force_refresh:
            self._algorithm_cache = algorithms
        return algorithms
    
    def _extract_module_name(self, python_file: Path) -> Optional[str]:
        """Extract module name from Python file path."""
        try:
            relative_path = python_file.relative_to(self.root)
            # Convert path to module name (e.g., semester_01/lecture_01/... -> semester_01.lecture_01....)
            parts = relative_path.parent.parts
            module_parts = list(parts) + [relative_path.stem]
            return '.'.join(module_parts)
        except ValueError:
            return None
    
    def _extract_main_function(self, python_file: Path) -> Optional[str]:
        """Extract main function name from Python file."""
        try:
            content = python_file.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            # Look for main function or function with algorithm name
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if it's a main function or the algorithm name
                    if node.name == 'main' or node.name == python_file.parent.name:
                        return node.name
            
            # Look for any top-level function
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    return node.name
        except Exception:
            pass
        return None
    
    def _extract_main_class(self, python_file: Path) -> Optional[str]:
        """Extract main class name from Python file."""
        try:
            content = python_file.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            # Look for class with algorithm name or first class
            algorithm_name = python_file.parent.name.replace('_', '').title()
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if class name matches algorithm name
                    if node.name.lower().replace('_', '') == algorithm_name.lower().replace('_', ''):
                        return node.name
            
            # Return first class found
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    return node.name
        except Exception:
            pass
        return None
    
    def find_algorithm(
        self,
        semester: Optional[str] = None,
        lecture: Optional[str] = None,
        algorithm: Optional[str] = None,
        path: Optional[str] = None
    ) -> Optional[AlgorithmInfo]:
        """Find algorithm by various criteria."""
        algorithms = self.discover_algorithms()
        
        if path:
            # Normalize path separators for comparison
            path_normalized = path.replace('\\', '/')
            
            # Find by full path (try multiple formats)
            for algo in algorithms:
                # Compare normalized paths
                algo_full_path_normalized = algo.full_path.replace('\\', '/')
                algo_path_str_normalized = str(algo.path).replace('\\', '/')
                
                if (algo.full_path == path or 
                    str(algo.path) == path or
                    algo_full_path_normalized == path_normalized or
                    algo_path_str_normalized == path_normalized):
                    return algo
            return None
        
        # Find by semester/lecture/algorithm
        for algo in algorithms:
            if semester and algo.semester != semester:
                continue
            if lecture and algo.lecture != lecture:
                continue
            if algorithm and algo.algorithm != algorithm:
                continue
            return algo
        
        return None
    
    def execute_algorithm(
        self,
        algorithm_info: AlgorithmInfo,
        timeout: int = 60,
        input_data: Optional[str] = None
    ) -> Tuple[bool, str, str, float]:
        """
        Execute a Python algorithm.
        
        Returns:
            (success, stdout, stderr, execution_time)
        """
        import time
        
        # Prepare command
        # Most Python files have a main() function, so we'll run the file directly
        cmd = [sys.executable, str(algorithm_info.path)]
        
        # Execute
        start_time = time.time()
        try:
            if input_data:
                result = subprocess.run(
                    cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(self.root)
                )
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=str(self.root)
                )
            
            execution_time = time.time() - start_time
            success = result.returncode == 0
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            
            return success, stdout, stderr, execution_time
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return False, "", f"Execution timed out after {timeout} seconds", execution_time
        except Exception as e:
            execution_time = time.time() - start_time
            return False, "", f"Execution error: {e}", execution_time
    
    def list_algorithms(
        self,
        semester: Optional[str] = None,
        lecture: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """List all algorithms, optionally filtered."""
        algorithms = self.discover_algorithms()
        
        result = []
        for algo in algorithms:
            if semester and algo.semester != semester:
                continue
            if lecture and algo.lecture != lecture:
                continue
            
            result.append({
                "name": algo.name,
                "semester": algo.semester,
                "lecture": algo.lecture,
                "algorithm": algo.algorithm,
                "path": algo.full_path,
                "module_name": algo.module_name or "",
                "function_name": algo.function_name or "",
                "class_name": algo.class_name or ""
            })
        
        return result


# Global executor instance
_executor = None


def get_executor(force_refresh: bool = False) -> PythonExecutor:
    """Get global executor instance."""
    global _executor
    if _executor is None or force_refresh:
        _executor = PythonExecutor()
        if force_refresh:
            _executor.discover_algorithms(force_refresh=True)
    return _executor

