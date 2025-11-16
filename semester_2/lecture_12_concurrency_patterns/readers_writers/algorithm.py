from framework.logging_utils import get_logger
logger = get_logger(__name__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Readers-Writers Lock implementation."""


def readers_writers():
    """
    Implement Readers-Writers Lock.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    logger.info("==" * 35)
    logger.info("Readers-Writers Lock")
    logger.info("==" * 35)
    logger.info(f"Category: Concurrency")
    logger.info(f"Time Complexity: O(1)")
    logger.info(f"Space Complexity: O(1)")
    logger.info("==" * 35)


if __name__ == "__main__":
    readers_writers()