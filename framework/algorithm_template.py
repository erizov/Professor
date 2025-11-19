#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm Template Generator.

Creates standard structure for algorithm implementations.
"""

import json
from pathlib import Path
from typing import Dict, Any


ALGORITHM_README_TEMPLATE = """# {name}

## Overview

{description}

## Complexity Analysis

- **Time Complexity**: {time_complexity}
- **Space Complexity**: {space_complexity}
- **Best Case**: {best_case}
- **Average Case**: {average_case}
- **Worst Case**: {worst_case}

## Advantages

{advantages}

## Disadvantages

{disadvantages}

## When to Use

{when_to_use}

## When NOT to Use

{when_not_to_use}

## Common Mistakes

{common_mistakes}

## Common Misconceptions

{misconceptions}

## Implementation Notes

{implementation_notes}

## References

{references}
"""


PYTHON_TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{name} implementation.

{description}
"""

from typing import List, Any


def {function_name}(data: List[Any]) -> List[Any]:
    """
    {name} algorithm.
    
    Args:
        data: Input data to process
        
    Returns:
        Processed result
    """
    # TODO: Implement algorithm
    pass


def main() -> None:
    """Demonstration of {name}."""
    print("=" * 70)
    print("{name}")
    print("=" * 70)
    
    # Example usage
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {{data}}")
    
    result = {function_name}(data.copy())
    print(f"Result:   {{result}}")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
'''


JAVA_TEMPLATE = """import java.util.Arrays;

/**
 * {name} implementation.
 * 
 * {description}
 */
public class Algorithm {{
    
    /**
     * {name} algorithm.
     * 
     * @param data Input array
     * @return Processed array
     */
    public static int[] {methodName}(int[] data) {{
        // TODO: Implement algorithm
        return data;
    }}
    
    /**
     * Main method for demonstration.
     */
    public static void main(String[] args) {{
        System.out.println("=" .repeat(70));
        System.out.println("{name}");
        System.out.println("=" .repeat(70));
        
        int[] data = {{64, 34, 25, 12, 22, 11, 90}};
        System.out.println("Original: " + Arrays.toString(data));
        
        int[] result = {methodName}(data.clone());
        System.out.println("Result:   " + Arrays.toString(result));
        
        System.out.println("=" .repeat(70));
    }}
}}
"""


def create_algorithm_structure(base_path: Path, metadata: Dict[str, Any]) -> None:
    """
    Create algorithm folder structure with templates.

    Args:
        base_path: Base directory for algorithm
        metadata: Algorithm metadata
    """
    base_path.mkdir(parents=True, exist_ok=True)

    # Create metadata.json
    with open(base_path / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # Create README.md
    readme_content = ALGORITHM_README_TEMPLATE.format(**metadata)
    with open(base_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Create Python implementation
    function_name = metadata["name"].lower().replace(" ", "_")
    python_content = PYTHON_TEMPLATE.format(
        name=metadata["name"],
        description=metadata["description"],
        function_name=function_name,
    )
    with open(base_path / "algorithm.py", "w", encoding="utf-8") as f:
        f.write(python_content)

    # Create Java implementation
    method_name = "".join(
        word.capitalize() for word in metadata["name"].lower().split()
    )
    method_name = method_name[0].lower() + method_name[1:]

    java_content = JAVA_TEMPLATE.format(
        name=metadata["name"],
        description=metadata["description"],
        methodName=method_name,
    )
    with open(base_path / "Algorithm.java", "w", encoding="utf-8") as f:
        f.write(java_content)
