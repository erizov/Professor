from framework.logging_utils import get_logger
logger = get_logger(__name__)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Activity Selection implementation."""


def activity_selection():
    """
    Implement Activity Selection.
    
    Time Complexity: O(n log n)
    Space Complexity: O(1)
    """
    logger.info("==" * 35)
    logger.info("Activity Selection")
    logger.info("==" * 35)
    logger.info(f"Category: Greedy Algorithm")
    logger.info(f"Time Complexity: O(n log n)")
    logger.info(f"Space Complexity: O(1)")
    logger.info("==" * 35)


if __name__ == "__main__":
    activity_selection()