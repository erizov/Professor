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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("AES (ADVANCED ENCRYPTION STANDARD) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic AES Encryption
    logger.info("Example 1: Basic AES-256 Encryption")
    logger.info("-" * 70)
    
    aes = AESEncryption(key_size=256)
    
    plaintext = b"Hello, this is a secret message!"
    logger.info(f"Plaintext: {plaintext.decode()}")
    
    ciphertext, iv = aes.encrypt(plaintext)
    logger.info(f"Ciphertext (hex): {ciphertext.hex()[:64]}...")
    logger.info(f"IV (hex): {iv.hex()}")
    
    decrypted = aes.decrypt(ciphertext, iv)
    logger.info(f"Decrypted: {decrypted.decode()}")
    logger.info(f"Match: {plaintext == decrypted}")
    logger.info()
    
    # Example 2: String Encryption
    logger.info("Example 2: String Encryption/Decryption")
    logger.info("-" * 70)
    
    messages = [
        "Sensitive user data",
        "Credit card number: 1234-5678-9012-3456",
        "API key: sk_live_1234567890abcdef"
    ]
    
    for message in messages:
        encrypted = aes.encrypt_string(message)
        decrypted = aes.decrypt_string(encrypted)
        logger.info(f"Original: {message}")
        logger.info(f"Encrypted: {encrypted[:50]}...")
        logger.info(f"Decrypted: {decrypted}")
        logger.info(f"Match: {message == decrypted}")
        logger.info()
    
    # Example 3: Different Key Sizes
    logger.info("Example 3: Different AES Key Sizes")
    logger.info("-" * 70)
    
    plaintext = b"Test message for different key sizes"
    
    for key_size in [128, 192, 256]:
        aes = AESEncryption(key_size=key_size)
        ciphertext, iv = aes.encrypt(plaintext)
        decrypted = aes.decrypt(ciphertext, iv)
        
        logger.info(f"AES-{key_size}:")
        logger.info(f"  Key size: {len(aes.key)} bytes")
        logger.info(f"  Ciphertext size: {len(ciphertext)} bytes")
        logger.info(f"  Decryption successful: {plaintext == decrypted}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("AES Encryption")
    
    def encryption_operations():
        aes = AESEncryption(key_size=256)
        data = b"x" * 1024  # 1KB of data
        
        ciphertext, iv = aes.encrypt(data)
        decrypted = aes.decrypt(ciphertext, iv)
        
        return len(decrypted)
    
    result, metrics = timer.measure(encryption_operations)
    logger.info(f"Time to encrypt/decrypt 1KB: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nAlgorithm Summary:")
    logger.info("\nDescription:")
    logger.info("  Advanced Encryption Standard (AES) is a symmetric encryption")
    logger.info("  algorithm widely used for secure data transmission.")
    logger.info("\nKey Sizes:")
    logger.info("  - AES-128: 128-bit key (16 bytes)")
    logger.info("  - AES-192: 192-bit key (24 bytes)")
    logger.info("  - AES-256: 256-bit key (32 bytes)")
    logger.info("\nTime Complexity:")
    logger.info("  - Encryption: O(n) where n is data size")
    logger.info("  - Decryption: O(n) where n is data size")
    logger.info("\nKey Advantages:")
    logger.info("  - Fast encryption/decryption")
    logger.info("  - Secure (NIST approved)")
    logger.info("  - Widely supported")
    logger.info("  - Hardware acceleration available")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Requires secure key exchange")
    logger.info("  - Key management complexity")
    logger.info("  - Not quantum-resistant")
    logger.info("\nWhen to Use:")
    logger.info("  - Data at rest encryption")
    logger.info("  - Secure communication")
    logger.info("  - Database encryption")
    logger.info("  - File encryption")
    logger.info("\nCommon Use Cases:")
    logger.info("  - TLS/SSL")
    logger.info("  - VPN protocols")
    logger.info("  - Disk encryption")
    logger.info("  - Database encryption")
    logger.info("  - Secure messaging")
    logger.info("\nSecurity Notes:")
    logger.info("  - Always use random IVs")
    logger.info("  - Use authenticated encryption (AES-GCM) when possible")
    logger.info("  - Protect keys securely")
    logger.info("  - Use appropriate key sizes (256-bit recommended)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()