# Contributing to Algorithms and Design Patterns Course

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Algorithm Submission Guidelines](#algorithm-submission-guidelines)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/Professor.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Set up environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python/Java version)

### Suggesting Enhancements

1. Check existing issues and enhancement suggestions
2. Create an issue describing:
   - The enhancement
   - Use case and benefits
   - Possible implementation approach

### Adding Algorithms

See [Algorithm Submission Guidelines](#algorithm-submission-guidelines) below.

## Algorithm Submission Guidelines

### Required Files

Each algorithm must include:

1. **README.md** - Comprehensive documentation
2. **algorithm.py** - Python implementation
3. **Algorithm.java** - Java implementation (or algorithm.sql for database algorithms)
4. **metadata.json** - Algorithm metadata
5. **test_algorithm.py** - Unit tests

### README.md Structure

```markdown
# Algorithm Name

**Category**: [Category]

**Time Complexity**: O(...)
**Space Complexity**: O(...)

## TL;DR
[One-sentence summary]

## Learning Objectives
[5-6 specific objectives]

## Prerequisites
[Required knowledge]

## Introduction
[Comprehensive introduction]

## Short Description
[Concise description - does NOT repeat introduction]

## Implementation
[Reference to code files]

## Examples of Implementation
[Framework examples: Spring, .NET, Docker, Kubernetes, etc.]

## Often Used Together With
[Related algorithms/patterns]

## Do Not Confuse With
[Similar but different concepts]

## Real-World Applications
[Industry examples]

## Common Misconceptions
[Wrong vs. correct statements]
```

### Code Requirements

#### Python
- Follow PEP 8 style guide
- Use type hints for all public functions
- Include docstrings (PEP 257)
- Maximum line length: 79 characters
- Use 4 spaces for indentation
- Include error handling and logging

#### Java
- Follow Java naming conventions
- Include Javadoc comments
- Use proper access modifiers
- Include error handling
- Follow standard Java formatting

#### SQL
- Use standard SQL syntax
- Include comments explaining queries
- Follow database-specific best practices
- Include examples for different databases

### Testing Requirements

- Write unit tests for all algorithms
- Test edge cases (empty input, single element, etc.)
- Include performance tests where applicable
- Aim for >80% code coverage
- Tests should be clear and well-documented

## Code Style Guidelines

### Python

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm implementation.
"""

from typing import List, Optional
from framework.logging_utils import get_logger

logger = get_logger(__name__)


def algorithm_name(arr: List[int]) -> List[int]:
    """
    Algorithm description.
    
    Args:
        arr: Input array
        
    Returns:
        Processed array
        
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    
    # Implementation
    return arr
```

### Java

```java
import java.util.*;
import java.util.logging.Logger;

/**
 * Algorithm implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    /**
     * Algorithm description.
     * 
     * @param arr Input array
     * @return Processed array
     */
    public static int[] algorithmName(int[] arr) {
        if (arr == null || arr.length == 0) {
            return new int[0];
        }
        
        // Implementation
        return arr;
    }
}
```

## Testing Guidelines

### Unit Tests

```python
import unittest
from tests.test_framework_setup import AlgorithmTestCase

class TestAlgorithm(AlgorithmTestCase):
    def test_basic_functionality(self):
        """Test basic algorithm functionality."""
        result = self.algorithm([1, 2, 3])
        self.assertIsNotNone(result)
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty input
        result = self.algorithm([])
        self.assertEqual(result, [])
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_algorithms.py

# Run with coverage
pytest --cov=. tests/
```

## Documentation Guidelines

- Write clear, concise documentation
- Include examples and use cases
- Explain complexity analysis
- Add framework integration examples
- Include "Do Not Confuse With" sections
- Provide real-world applications

## Pull Request Process

1. **Update your branch**: `git pull origin main`
2. **Run tests**: Ensure all tests pass
3. **Check code style**: Run linters and formatters
4. **Update documentation**: Update README if needed
5. **Create PR** with:
   - Clear title and description
   - Reference to related issues
   - List of changes
   - Screenshots (if applicable)

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] All CI checks passing

## Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, PR will be merged
4. Thank you for contributing!

## Questions?

- Open an issue for questions
- Check existing documentation
- Review similar algorithms for examples

---

Thank you for contributing to the Algorithms and Design Patterns Course!

