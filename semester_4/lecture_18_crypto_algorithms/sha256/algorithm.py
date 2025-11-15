#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHA-256 (Secure Hash Algorithm 256-bit) Implementation.

Cryptographic hash function that produces a 256-bit (32-byte) hash value.
One-way function used for data integrity verification and digital signatures.
"""

import sys
from pathlib import Path
from typing import List
import struct

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# SHA-256 constants
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


def right_rotate(value: int, amount: int) -> int:
    """
    Right rotate a 32-bit integer.
    
    Args:
        value: Value to rotate
        amount: Number of bits to rotate
        
    Returns:
        Rotated value
    """
    return ((value >> amount) | (value << (32 - amount))) & 0xffffffff


def sha256(message: bytes) -> bytes:
    """
    Compute SHA-256 hash of message.
    
    Args:
        message: Input message as bytes
        
    Returns:
        32-byte hash value
    """
    # Initialize hash values
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19
    
    # Pre-processing
    original_length = len(message) * 8
    message = bytearray(message)
    message.append(0x80)
    
    # Pad message to multiple of 512 bits (64 bytes)
    while len(message) % 64 != 56:
        message.append(0)
    
    # Append original length
    message += struct.pack('>Q', original_length)
    
    # Process message in 512-bit chunks
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        
        # Create message schedule
        w = list(struct.unpack('>16I', chunk))
        w.extend([0] * 48)
        
        for i in range(16, 64):
            s0 = right_rotate(w[i-15], 7) ^ right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = right_rotate(w[i-2], 17) ^ right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xffffffff
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        
        # Main loop
        for i in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + K[i] + w[i]) & 0xffffffff
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff
        
        # Add compressed chunk to hash
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff
    
    # Produce final hash
    return struct.pack('>8I', h0, h1, h2, h3, h4, h5, h6, h7)


def sha256_hex(message: bytes) -> str:
    """
    Compute SHA-256 hash and return as hexadecimal string.
    
    Args:
        message: Input message as bytes
        
    Returns:
        Hexadecimal hash string
    """
    return sha256(message).hex()


def main() -> None:
    """Demonstration of SHA-256 Algorithm."""
    print("=" * 70)
    print("SHA-256 (SECURE HASH ALGORITHM 256-BIT) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Hash a simple string
    print("Example 1: Hash Simple String")
    print("-" * 70)
    
    message1 = b"Hello, World!"
    hash1 = sha256_hex(message1)
    print(f"Message: {message1.decode()}")
    print(f"SHA-256: {hash1}")
    print()
    
    # Example 2: Hash different messages
    print("Example 2: Hash Different Messages")
    print("-" * 70)
    
    messages = [
        b"",
        b"a",
        b"abc",
        b"message digest",
        b"The quick brown fox jumps over the lazy dog"
    ]
    
    for msg in messages:
        hash_val = sha256_hex(msg)
        print(f"'{msg.decode()}' -> {hash_val[:32]}...")
    print()
    
    # Example 3: Avalanche effect
    print("Example 3: Avalanche Effect (Small Change)")
    print("-" * 70)
    
    msg1 = b"Hello, World!"
    msg2 = b"Hello, World?"
    
    hash1 = sha256_hex(msg1)
    hash2 = sha256_hex(msg2)
    
    print(f"Message 1: {msg1.decode()}")
    print(f"Hash 1:    {hash1}")
    print(f"Message 2: {msg2.decode()}")
    print(f"Hash 2:    {hash2}")
    print(f"Different: {hash1 != hash2}")
    print()
    
    # Example 4: Deterministic hashing
    print("Example 4: Deterministic Hashing")
    print("-" * 70)
    
    message = b"Test message"
    hash1 = sha256_hex(message)
    hash2 = sha256_hex(message)
    hash3 = sha256_hex(message)
    
    print(f"Message: {message.decode()}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    print(f"Hash 3: {hash3}")
    print(f"All equal: {hash1 == hash2 == hash3}")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("SHA-256")
    
    def hash_operations():
        messages = [b"test" * i for i in range(1, 100)]
        hashes = [sha256_hex(msg) for msg in messages]
        return len(hashes)
    
    result, metrics = timer.measure(hash_operations)
    print(f"Time to hash 99 messages: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    # Example 6: Hash length verification
    print("Example 6: Hash Length Verification")
    print("-" * 70)
    
    test_messages = [b"", b"a", b"Hello, World!", b"x" * 1000]
    for msg in test_messages:
        hash_bytes = sha256(msg)
        hash_hex = hash_bytes.hex()
        print(f"Message length: {len(msg)} bytes")
        print(f"Hash length: {len(hash_bytes)} bytes ({len(hash_hex)} hex chars)")
        print()
    
    print("=" * 70)
    print("\nAlgorithm Summary:")
    print("\nIntent:")
    print("  Cryptographic hash function that produces a 256-bit (32-byte)")
    print("  hash value. One-way function for data integrity verification.")
    print("\nKey Properties:")
    print("  - Deterministic: Same input always produces same output")
    print("  - Fast computation")
    print("  - Avalanche effect: Small input change = large output change")
    print("  - One-way: Cannot reverse hash to get original message")
    print("  - Collision resistant: Hard to find two inputs with same hash")
    print("\nTime Complexity: O(n) where n is message length")
    print("Space Complexity: O(1) - fixed output size")
    print("\nKey Advantages:")
    print("  - Fast computation")
    print("  - Fixed output size (256 bits)")
    print("  - Widely used and trusted")
    print("  - Good avalanche effect")
    print("\nKey Disadvantages:")
    print("  - Vulnerable to quantum computing (Grover's algorithm)")
    print("  - Not suitable for password hashing (use bcrypt/argon2)")
    print("  - No key (use HMAC for keyed hashing)")
    print("\nWhen to Use:")
    print("  - Data integrity verification")
    print("  - Digital signatures")
    print("  - Blockchain (Bitcoin)")
    print("  - File checksums")
    print("  - Merkle trees")
    print("\nCommon Use Cases:")
    print("  - Git commit hashes")
    print("  - Blockchain transactions")
    print("  - File integrity checks")
    print("  - Digital signatures")
    print("  - Certificate fingerprints")
    print("\nSecurity Considerations:")
    print("  - Use SHA-256 or SHA-3 for new applications")
    print("  - Don't use for password hashing (use bcrypt/argon2)")
    print("  - Use HMAC-SHA256 for keyed hashing")
    print("  - Consider post-quantum alternatives for long-term security")
    print("=" * 70)


if __name__ == "__main__":
    main()
