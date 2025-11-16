from framework.logging_utils import get_logger
logger = get_logger(__name__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gradient Descent implementation."""


def gradient_descent():
    """
    Implement Gradient Descent.
    
    Time Complexity: O(n*d*i)
    Space Complexity: O(d)
    """
    logger.info("==" * 35)
    logger.info("Gradient Descent")
    logger.info("==" * 35)
    logger.info(f"Category: Machine Learning")
    logger.info(f"Time Complexity: O(n*d*i)")
    logger.info(f"Space Complexity: O(d)")
    logger.info("==" * 35)


if __name__ == "__main__":
    gradient_descent()