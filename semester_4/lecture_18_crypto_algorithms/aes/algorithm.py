#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AES (Advanced Encryption Standard) Algorithm.

Symmetric encryption algorithm widely used for secure data transmission.
Supports key sizes of 128, 192, or 256 bits.
"""

import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class AESEncryption:
    """AES encryption/decryption wrapper."""
    
    def __init__(self, key_size: int = 256):
        """
        Initialize AES encryption.
        
        Args:
            key_size: Key size in bits (128, 192, or 256)
        """
        if key_size not in [128, 192, 256]:
            raise ValueError("Key size must be 128, 192, or 256 bits")
        
        self.key_size = key_size
        self.key = os.urandom(key_size // 8)  # Generate random key
        self.backend = default_backend()
    
    def encrypt(self, plaintext: bytes) -> tuple[bytes, bytes]:
        """
        Encrypt plaintext using AES.
        
        Args:
            plaintext: Data to encrypt
            
        Returns:
            Tuple of (ciphertext, iv)
        """
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Pad plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext)
        padded_data += padder.finalize()
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return ciphertext, iv
    
    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """
        Decrypt ciphertext using AES.
        
        Args:
            ciphertext: Encrypted data
            iv: Initialization vector
            
        Returns:
            Decrypted plaintext
        """
        # Create cipher
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext)
        plaintext += unpadder.finalize()
        
        return plaintext
    
    def encrypt_string(self, plaintext: str) -> str:
        """
        Encrypt string and return base64 encoded result.
        
        Args:
            plaintext: String to encrypt
            
        Returns:
            Base64 encoded ciphertext and IV
        """
        ciphertext, iv = self.encrypt(plaintext.encode('utf-8'))
        combined = iv + ciphertext
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt_string(self, encrypted: str) -> str:
        """
        Decrypt base64 encoded string.
        
        Args:
            encrypted: Base64 encoded ciphertext and IV
            
        Returns:
            Decrypted string
        """
        combined = base64.b64decode(encrypted)
        iv = combined[:16]
        ciphertext = combined[16:]
        plaintext = self.decrypt(ciphertext, iv)
        return plaintext.decode('utf-8')


def main() -> None:
    """Demonstration of AES Encryption."""
    print("=" * 70)
    print("AES (ADVANCED ENCRYPTION STANDARD) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic AES Encryption
    print("Example 1: Basic AES-256 Encryption")
    print("-" * 70)
    
    aes = AESEncryption(key_size=256)
    
    plaintext = b"Hello, this is a secret message!"
    print(f"Plaintext: {plaintext.decode()}")
    
    ciphertext, iv = aes.encrypt(plaintext)
    print(f"Ciphertext (hex): {ciphertext.hex()[:64]}...")
    print(f"IV (hex): {iv.hex()}")
    
    decrypted = aes.decrypt(ciphertext, iv)
    print(f"Decrypted: {decrypted.decode()}")
    print(f"Match: {plaintext == decrypted}")
    print()
    
    # Example 2: String Encryption
    print("Example 2: String Encryption/Decryption")
    print("-" * 70)
    
    messages = [
        "Sensitive user data",
        "Credit card number: 1234-5678-9012-3456",
        "API key: sk_live_1234567890abcdef"
    ]
    
    for message in messages:
        encrypted = aes.encrypt_string(message)
        decrypted = aes.decrypt_string(encrypted)
        print(f"Original: {message}")
        print(f"Encrypted: {encrypted[:50]}...")
        print(f"Decrypted: {decrypted}")
        print(f"Match: {message == decrypted}")
        print()
    
    # Example 3: Different Key Sizes
    print("Example 3: Different AES Key Sizes")
    print("-" * 70)
    
    plaintext = b"Test message for different key sizes"
    
    for key_size in [128, 192, 256]:
        aes = AESEncryption(key_size=key_size)
        ciphertext, iv = aes.encrypt(plaintext)
        decrypted = aes.decrypt(ciphertext, iv)
        
        print(f"AES-{key_size}:")
        print(f"  Key size: {len(aes.key)} bytes")
        print(f"  Ciphertext size: {len(ciphertext)} bytes")
        print(f"  Decryption successful: {plaintext == decrypted}")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("AES Encryption")
    
    def encryption_operations():
        aes = AESEncryption(key_size=256)
        data = b"x" * 1024  # 1KB of data
        
        ciphertext, iv = aes.encrypt(data)
        decrypted = aes.decrypt(ciphertext, iv)
        
        return len(decrypted)
    
    result, metrics = timer.measure(encryption_operations)
    print(f"Time to encrypt/decrypt 1KB: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nAlgorithm Summary:")
    print("\nDescription:")
    print("  Advanced Encryption Standard (AES) is a symmetric encryption")
    print("  algorithm widely used for secure data transmission.")
    print("\nKey Sizes:")
    print("  - AES-128: 128-bit key (16 bytes)")
    print("  - AES-192: 192-bit key (24 bytes)")
    print("  - AES-256: 256-bit key (32 bytes)")
    print("\nTime Complexity:")
    print("  - Encryption: O(n) where n is data size")
    print("  - Decryption: O(n) where n is data size")
    print("\nKey Advantages:")
    print("  - Fast encryption/decryption")
    print("  - Secure (NIST approved)")
    print("  - Widely supported")
    print("  - Hardware acceleration available")
    print("\nKey Disadvantages:")
    print("  - Requires secure key exchange")
    print("  - Key management complexity")
    print("  - Not quantum-resistant")
    print("\nWhen to Use:")
    print("  - Data at rest encryption")
    print("  - Secure communication")
    print("  - Database encryption")
    print("  - File encryption")
    print("\nCommon Use Cases:")
    print("  - TLS/SSL")
    print("  - VPN protocols")
    print("  - Disk encryption")
    print("  - Database encryption")
    print("  - Secure messaging")
    print("\nSecurity Notes:")
    print("  - Always use random IVs")
    print("  - Use authenticated encryption (AES-GCM) when possible")
    print("  - Protect keys securely")
    print("  - Use appropriate key sizes (256-bit recommended)")
    print("=" * 70)


if __name__ == "__main__":
    main()
