#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ner implementation.

This file contains the implementation of the Ner algorithm.
"""

from typing import List, Optional, Dict, Set


class NER:
    """Named Entity Recognition."""

    def __init__(self):
        self.model: any = None
        self.entities: Dict[str, List[dict]] = {}

    def extract_entities(self, text: str) -> List[dict]:
        """Extract named entities."""
        entities = []
        words = text.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 1:
                entities.append(
                    {"text": word, "label": "PERSON", "start": i, "end": i + 1}
                )
        return entities

    def tag(self, text: str) -> List[tuple]:
        """Tag text with entities."""
        entities = self.extract_entities(text)
        words = text.split()
        tags = []
        entity_set = {e["text"] for e in entities}
        for word in words:
            if word in entity_set:
                tags.append((word, "ENTITY"))
            else:
                tags.append((word, "O"))
        return tags


def main() -> None:
    """Demonstrate Ner."""
    print("=" * 70)
    print("NER")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Ner")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
