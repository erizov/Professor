#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contextual Help implementation.

This file contains the implementation of the Contextual Help algorithm.
"""

from typing import List, Optional, Dict, Set


class ContextualHelp:
    """Contextual help system."""

    def __init__(self):
        self.help_topics: Dict[str, dict] = {}
        self.context_rules: List[dict] = {}

    def add_help_topic(
        self, topic_id: str, title: str, content: str, keywords: List[str]
    ) -> None:
        """Add help topic."""
        self.help_topics[topic_id] = {
            "title": title,
            "content": content,
            "keywords": keywords,
        }

    def get_help(self, context: str) -> List[dict]:
        """Get contextual help."""
        context_lower = context.lower()
        matches = []

        for topic_id, topic in self.help_topics.items():
            score = sum(
                1 for keyword in topic["keywords"] if keyword.lower() in context_lower
            )
            if score > 0:
                matches.append(
                    {"topic_id": topic_id, "title": topic["title"], "score": score}
                )

        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:5]  # Top 5 matches


def main() -> None:
    """Demonstrate Contextual Help."""
    print("=" * 70)
    print("CONTEXTUAL HELP")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Contextual Help")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
