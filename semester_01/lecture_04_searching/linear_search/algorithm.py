#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linear Search implementation."""


# Add project root to path for framework imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import List, TypeVar
from framework.logging_utils import get_logger
import logging
import sys

logger = get_logger(__name__)

T = TypeVar("T")


def linear_search(arr: List[T], target: T) -> int:
    """
    Search for target using linear search.

    Args:
        arr: List to search in
        target: Element to find

    Returns:
        Index if found, -1 otherwise

    Time: O(n), Space: O(1)
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1


def main():
    """Demonstration."""
    logger.info("=" * 70)
    logger.info("LINEAR SEARCH")
    logger.info("=" * 70)

    data = [64, 34, 25, 12, 22, 11, 90]
    target = 22

    result = linear_search(data, target)
    logger.info(f"Array: {data}")
    logger.info(f"Target: {target}")
    logger.info(f"Found at index: {result}")

    logger.info("\nComplexity: O(n) time, O(1) space")
    try:
        """Demonstration."""
        logger.info("=" * 70)
        logger.info("LINEAR SEARCH")
        logger.info("=" * 70)

        data = [64, 34, 25, 12, 22, 11, 90]
        target = 22

        result = linear_search(data, target)
        logger.info(f"Array: {data}")
        logger.info(f"Target: {target}")
        logger.info(f"Found at index: {result}")

        logger.info("\nComplexity: O(n) time, O(1) space")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
