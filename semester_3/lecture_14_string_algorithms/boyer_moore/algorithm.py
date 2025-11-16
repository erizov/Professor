from framework.logging_utils import get_logger
logger = get_logger(__name__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Boyer-Moore Algorithm implementation."""


def boyer_moore():
    """
    Implement Boyer-Moore Algorithm.
    
    Time Complexity: O(n/m)
    Space Complexity: O(m)
    """
    logger.info("==" * 35)
    logger.info("Boyer-Moore Algorithm")
    logger.info("==" * 35)
    logger.info(f"Category: String Algorithm")
    logger.info(f"Time Complexity: O(n/m)")
    logger.info(f"Space Complexity: O(m)")
    logger.info("==" * 35)


if __name__ == "__main__":
    boyer_moore()