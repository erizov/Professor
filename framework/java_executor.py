#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Java Algorithm Execution Framework.

Provides a unified interface to execute any Java algorithm from a common place.
Supports both web interface and command-line usage.
"""

import subprocess
import re
from pathlib import Path
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass
import json

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class AlgorithmInfo:
    """Information about an algorithm."""
    name: str
    path: Path
    package: Optional[str]
    class_name: str
    semester: str
    lecture: str
    algorithm: str
    full_path: str


class JavaExecutor:
    """Unified Java algorithm executor."""
    
    def __init__(self, root: Path = ROOT):
        """Initialize executor with project root."""
        self.root = root
        self._algorithm_cache: Optional[List[AlgorithmInfo]] = None
    
    def discover_algorithms(self) -> List[AlgorithmInfo]:
        """Discover all Algorithm.java files in the project."""
        if self._algorithm_cache is not None:
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
                    
                    java_file = algo_dir / "Algorithm.java"
                    if not java_file.exists():
                        continue
                    
                    algorithm_name = algo_dir.name
                    
                    # Extract package name
                    package = self._extract_package(java_file)
                    
                    # Get class name
                    class_name = self._extract_class_name(java_file)
                    
                    # Get relative path
                    try:
                        relative_path = java_file.relative_to(self.root)
                    except ValueError:
                        relative_path = java_file
                    
                    info = AlgorithmInfo(
                        name=f"{semester_name}/{lecture_name}/{algorithm_name}",
                        path=java_file,
                        package=package,
                        class_name=class_name,
                        semester=semester_name,
                        lecture=lecture_name,
                        algorithm=algorithm_name,
                        full_path=str(relative_path)
                    )
                    algorithms.append(info)
        
        self._algorithm_cache = algorithms
        return algorithms
    
    def _extract_package(self, java_file: Path) -> Optional[str]:
        """Extract package name from Java file."""
        try:
            content = java_file.read_text(encoding='utf-8')
            # Look for actual package declaration (not in comments)
            # Check for package at start of line (possibly with whitespace)
            for line in content.split('\n'):
                # Skip comment lines
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                    continue
                # Look for package declaration
                match = re.search(r'^\s*package\s+([^;]+);', line)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None
    
    def _extract_class_name(self, java_file: Path) -> str:
        """Extract class name from Java file."""
        try:
            content = java_file.read_text(encoding='utf-8')
            # Look for public class ClassName
            match = re.search(r'public\s+class\s+(\w+)', content)
            if match:
                return match.group(1)
            # Look for class ClassName (without public)
            match = re.search(r'class\s+(\w+)', content)
            if match:
                return match.group(1)
        except Exception:
            pass
        return "Algorithm"
    
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
            # Find by full path
            for algo in algorithms:
                if algo.full_path == path or str(algo.path) == path:
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
    
    def compile_algorithm(self, algorithm_info: AlgorithmInfo) -> Tuple[bool, str]:
        """Compile a Java algorithm."""
        try:
            result = subprocess.run(
                ["javac", str(algorithm_info.path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.root)
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Compilation failed"
                return False, error_msg
            
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out after 30 seconds"
        except Exception as e:
            return False, f"Compilation error: {e}"
    
    def execute_algorithm(
        self,
        algorithm_info: AlgorithmInfo,
        timeout: int = 60,
        input_data: Optional[str] = None
    ) -> Tuple[bool, str, str, float]:
        """
        Execute a Java algorithm.
        
        Returns:
            (success, stdout, stderr, execution_time)
        """
        import time
        
        # Compile first
        compiled, compile_error = self.compile_algorithm(algorithm_info)
        if not compiled:
            return False, "", compile_error, 0.0
        
        # Determine class name and classpath
        # Check if there's an actual package declaration (not in comments)
        package = algorithm_info.package
        
        if package:
            # Has actual package declaration - use fully qualified name
            class_name = f"{package}.{algorithm_info.class_name}"
            # Use project root as classpath
            classpath = str(self.root)
        else:
            # No package declaration - compile creates .class in same directory
            # Use simple class name and set classpath to algorithm directory
            class_name = algorithm_info.class_name
            classpath = str(algorithm_info.path.parent)
        
        # Prepare command
        cmd = ["java", "-cp", classpath, class_name]
        
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
                "package": algo.package or "",
                "class_name": algo.class_name
            })
        
        return result


# Global executor instance
_executor = None


def get_executor() -> JavaExecutor:
    """Get global executor instance."""
    global _executor
    if _executor is None:
        _executor = JavaExecutor()
    return _executor

