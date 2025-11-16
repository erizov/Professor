#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA (Rivest-Shamir-Adleman) Algorithm.

Asymmetric cryptographic algorithm for secure data transmission.
Uses public and private key pairs for encryption and decryption.
"""

import sys
from pathlib import Path
from typing import Tuple
import random
import math

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


def is_prime(n: int) -> bool:
    """
    Check if number is prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_prime(min_val: int, max_val: int) -> int:
    """
    Generate a random prime number.
    
    Args:
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Prime number
    """
    while True:
        num = random.randint(min_val, max_val)
        if is_prime(num):
            return num


def gcd(a: int, b: int) -> int:
    """
    Calculate greatest common divisor.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        GCD of a and b
    """
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Tuple (gcd, x, y) such that ax + by = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Calculate modular inverse.
    
    Args:
        a: Number
        m: Modulus
        
    Returns:
        Modular inverse of a mod m
    """
    gcd_val, x, _ = extended_gcd(a, m)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Modular exponentiation.
    
    Args:
        base: Base
        exp: Exponent
        mod: Modulus
        
    Returns:
        (base^exp) mod mod
    """
    result = 1
    base = base % mod
    
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    
    return result


class RSA:
    """RSA encryption/decryption implementation."""
    
    def __init__(self, p: int = None, q: int = None, e: int = None):
        """
        Initialize RSA with keys.
        
        Args:
            p: First prime (if None, will generate)
            q: Second prime (if None, will generate)
            e: Public exponent (if None, will choose)
        """
        if p is None or q is None:
            # Generate small primes for demonstration
            p = generate_prime(100, 200)
            q = generate_prime(100, 200)
        
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        
        # Choose public exponent
        if e is None:
            e = 65537  # Common choice
            while gcd(e, self.phi) != 1:
                e += 2
        
        self.e = e
        self.d = mod_inverse(e, self.phi)
    
    def get_public_key(self) -> Tuple[int, int]:
        """
        Get public key.
        
        Returns:
            Tuple (n, e)
        """
        return (self.n, self.e)
    
    def get_private_key(self) -> Tuple[int, int]:
        """
        Get private key.
        
        Returns:
            Tuple (n, d)
        """
        return (self.n, self.d)
    
    def encrypt(self, message: int) -> int:
        """
        Encrypt message using public key.
        
        Args:
            message: Message to encrypt (must be < n)
            
        Returns:
            Encrypted message
        """
        if message >= self.n:
            raise ValueError("Message too large for key size")
        return mod_pow(message, self.e, self.n)
    
    def decrypt(self, ciphertext: int) -> int:
        """
        Decrypt ciphertext using private key.
        
        Args:
            ciphertext: Encrypted message
            
        Returns:
            Decrypted message
        """
        return mod_pow(ciphertext, self.d, self.n)
    
    def encrypt_string(self, message: str) -> list:
        """
        Encrypt string message.
        
        Args:
            message: String to encrypt
            
        Returns:
            List of encrypted integers
        """
        encrypted = []
        for char in message:
            encrypted.append(self.encrypt(ord(char)))
        return encrypted
    
    def decrypt_string(self, ciphertext: list) -> str:
        """
        Decrypt list of integers to string.
        
        Args:
            ciphertext: List of encrypted integers
            
        Returns:
            Decrypted string
        """
        decrypted = []
        for num in ciphertext:
            decrypted.append(chr(self.decrypt(num)))
        return ''.join(decrypted)


def main() -> None:
    """Demonstration of RSA Algorithm."""
    logger.info("=" * 70)
    logger.info("RSA (RIVEST-SHAMIR-ADLEMAN) ALGORITHM DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Key Generation
    logger.info("Example 1: Generate RSA Key Pair")
    logger.info("-" * 70)
    
    rsa = RSA()
    public_key = rsa.get_public_key()
    private_key = rsa.get_private_key()
    
    logger.info(f"Public key (n, e): ({public_key[0]}, {public_key[1]})")
    logger.info(f"Private key (n, d): ({private_key[0]}, {private_key[1]})")
    logger.info(f"Key size: {public_key[0].bit_length()} bits")
    logger.info()
    
    # Example 2: Encrypt/Decrypt Integer
    logger.info("Example 2: Encrypt and Decrypt Integer")
    logger.info("-" * 70)
    
    message = 42
    encrypted = rsa.encrypt(message)
    decrypted = rsa.decrypt(encrypted)
    
    logger.info(f"Original message: {message}")
    logger.info(f"Encrypted: {encrypted}")
    logger.info(f"Decrypted: {decrypted}")
    logger.info(f"Match: {message == decrypted}")
    logger.info()
    
    # Example 3: Encrypt/Decrypt String
    logger.info("Example 3: Encrypt and Decrypt String")
    logger.info("-" * 70)
    
    text = "HELLO"
    encrypted_text = rsa.encrypt_string(text)
    decrypted_text = rsa.decrypt_string(encrypted_text)
    
    logger.info(f"Original text: {text}")
    logger.info(f"Encrypted: {encrypted_text}")
    logger.info(f"Decrypted: {decrypted_text}")
    logger.info(f"Match: {text == decrypted_text}")
    logger.info()
    
    # Example 4: Multiple Messages
    logger.info("Example 4: Encrypt Multiple Messages")
    logger.info("-" * 70)
    
    messages = [10, 20, 30, 40, 50]
    encrypted_messages = [rsa.encrypt(m) for m in messages]
    decrypted_messages = [rsa.decrypt(e) for e in encrypted_messages]
    
    logger.info("Messages:", messages)
    logger.info("Encrypted:", encrypted_messages)
    logger.info("Decrypted:", decrypted_messages)
    logger.info(f"All match: {messages == decrypted_messages}")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("RSA")
    
    def rsa_operations():
        rsa = RSA()
        message = 12345
        encrypted = rsa.encrypt(message)
        decrypted = rsa.decrypt(encrypted)
        return decrypted == message
    
    result, metrics = timer.measure(rsa_operations)
    logger.info(f"Time to encrypt and decrypt: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nAlgorithm Summary:")
    logger.info("\nIntent:")
    logger.info("  Asymmetric cryptographic algorithm for secure data transmission.")
    logger.info("  Uses public and private key pairs for encryption and decryption.")
    logger.info("\nKey Generation:")
    logger.info("  1. Choose two large prime numbers p and q")
    logger.info("  2. Calculate n = p * q")
    logger.info("  3. Calculate φ(n) = (p-1) * (q-1)")
    logger.info("  4. Choose public exponent e (usually 65537)")
    logger.info("  5. Calculate private exponent d = e^(-1) mod φ(n)")
    logger.info("\nEncryption:")
    logger.info("  c = m^e mod n (where m is message, c is ciphertext)")
    logger.info("\nDecryption:")
    logger.info("  m = c^d mod n")
    logger.info("\nKey Advantages:")
    logger.info("  - Asymmetric (public/private key pair)")
    logger.info("  - Secure for key exchange")
    logger.info("  - Digital signatures")
    logger.info("  - Widely used and trusted")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Slow compared to symmetric encryption")
    logger.info("  - Requires large key sizes (2048+ bits)")
    logger.info("  - Vulnerable to quantum computing")
    logger.info("  - Key management complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - Key exchange")
    logger.info("  - Digital signatures")
    logger.info("  - Secure communication setup")
    logger.info("  - Certificate-based authentication")
    logger.info("\nCommon Use Cases:")
    logger.info("  - SSL/TLS handshakes")
    logger.info("  - SSH key authentication")
    logger.info("  - Digital signatures")
    logger.info("  - Email encryption (PGP)")
    logger.info("\nSecurity Considerations:")
    logger.info("  - Use key sizes >= 2048 bits for production")
    logger.info("  - Protect private keys")
    logger.info("  - Use proper padding (OAEP)")
    logger.info("  - Consider post-quantum cryptography")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()