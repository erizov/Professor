#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blockchain Structure implementation.

This file contains the implementation of the Blockchain Structure algorithm.
"""

from typing import List, Optional, Dict, Set


class Block:
    """Block in blockchain."""
    def __init__(self, index: int, data: any, previous_hash: str):
        import time
        import hashlib
        import json
        
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash."""
        import hashlib
        import json
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Mine block with given difficulty."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    """Blockchain implementation."""
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
    
    def create_genesis_block(self) -> Block:
        """Create genesis block."""
        return Block(0, "Genesis Block", "0")
    
    def get_latest_block(self) -> Block:
        """Get latest block."""
        return self.chain[-1]
    
    def add_block(self, data: any) -> None:
        """Add new block."""
        previous_hash = self.get_latest_block().hash
        new_block = Block(len(self.chain), data, previous_hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def is_valid(self) -> bool:
        """Validate blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if current.hash != current.calculate_hash():
                return False
            
            if current.previous_hash != previous.hash:
                return False
        
        return True


def main() -> None:
    """Demonstrate Blockchain Structure."""
    print("=" * 70)
    print("BLOCKCHAIN STRUCTURE")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Blockchain Structure")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
