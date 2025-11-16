from framework.logging_utils import get_logger
logger = get_logger(__name__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rabin-Karp Algorithm implementation."""


def rabin_karp():
    """
    Implement Rabin-Karp Algorithm.
    
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    """
    logger.info("==" * 35)
    logger.info("Rabin-Karp Algorithm")
    logger.info("==" * 35)
    logger.info(f"Category: String Algorithm")
    logger.info(f"Time Complexity: O(n + m)")
    logger.info(f"Space Complexity: O(1)")
    logger.info("==" * 35)


if __name__ == "__main__":
    rabin_karp()