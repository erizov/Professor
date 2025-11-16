#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Encryption Pattern.

General encryption pattern demonstrating symmetric and asymmetric encryption
concepts, key management, and encryption best practices.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Tuple
import os

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class EncryptionAlgorithm(ABC):
    """Abstract encryption algorithm."""
    
    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """Encrypt plaintext."""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt ciphertext."""
        pass


class SimpleXOREncryption(EncryptionAlgorithm):
    """Simple XOR encryption (for demonstration only - not secure)."""
    
    def encrypt(self, plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """Encrypt using XOR."""
        iv = os.urandom(16)
        ciphertext = bytearray()
        key_bytes = key * ((len(plaintext) // len(key)) + 1)
        
        for i, byte in enumerate(plaintext):
            ciphertext.append(byte ^ key_bytes[i] ^ iv[i % len(iv)])
        
        return bytes(ciphertext), iv
    
    def decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt using XOR."""
        plaintext = bytearray()
        key_bytes = key * ((len(ciphertext) // len(key)) + 1)
        
        for i, byte in enumerate(ciphertext):
            plaintext.append(byte ^ key_bytes[i] ^ iv[i % len(iv)])
        
        return bytes(plaintext)


class EncryptionService:
    """Encryption service with key management."""
    
    def __init__(self, algorithm: EncryptionAlgorithm):
        self.algorithm = algorithm
        self.key = os.urandom(32)
    
    def encrypt_data(self, data: bytes) -> Tuple[bytes, bytes]:
        """Encrypt data."""
        return self.algorithm.encrypt(data, self.key)
    
    def decrypt_data(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Decrypt data."""
        return self.algorithm.decrypt(ciphertext, self.key, iv)


def main() -> None:
    """Demonstration of Encryption Pattern."""
    logger.info("=" * 70)
    logger.info("ENCRYPTION PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    algorithm = SimpleXOREncryption()
    service = EncryptionService(algorithm)
    
    plaintext = b"Sensitive user data"
    ciphertext, iv = service.encrypt_data(plaintext)
    decrypted = service.decrypt_data(ciphertext, iv)
    
    logger.info(f"Plaintext: {plaintext.decode()}")
    logger.info(f"Decrypted: {decrypted.decode()}")
    logger.info(f"Match: {plaintext == decrypted}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern: Secure data encryption")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()