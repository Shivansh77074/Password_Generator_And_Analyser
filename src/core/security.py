



# ============================================================================
# File: src/core/security.py
# ============================================================================
"""
Core security functions using cryptographically secure randomness.
All functions use the secrets module for CSPRNG operations.

SECURITY GUARANTEE: No state is maintained between function calls.
"""

import secrets
from typing import List, TypeVar

T = TypeVar('T')


def secure_random_choice(sequence: str) -> str:
    """
    Securely select a random character from a sequence.
    
    Args:
        sequence: Non-empty string of characters
    
    Returns:
        Randomly selected character
    
    Raises:
        ValueError: If sequence is empty
    
    Security:
        - Uses secrets.choice (CSPRNG)
        - No state maintained
        - Uniform distribution
    """
    if not sequence:
        raise ValueError("Cannot choose from empty sequence")
    return secrets.choice(sequence)


def secure_randint(min_val: int, max_val: int) -> int:
    """
    Generate cryptographically secure random integer.
    
    Args:
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
    
    Returns:
        Random integer in range [min_val, max_val]
    
    Security:
        - Uses secrets.randbelow for unbiased selection
        - Uniform distribution guaranteed
    """
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val")
    
    range_size = max_val - min_val + 1
    return min_val + secrets.randbelow(range_size)


def secure_shuffle(items: List[T]) -> List[T]:
    """
    Securely shuffle a list using Fisher-Yates algorithm with CSPRNG.
    
    Args:
        items: List to shuffle
    
    Returns:
        New shuffled list (original unchanged)
    
    Security:
        - Fisher-Yates algorithm with secrets.randbelow
        - Uniform permutation distribution
        - Original list not modified
        - No state maintained
    """
    shuffled = items.copy()
    n = len(shuffled)
    
    for i in range(n - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    
    return shuffled


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token (URL-safe).
    
    Args:
        length: Token length in bytes
    
    Returns:
        URL-safe base64 encoded token
    
    Security:
        - Uses secrets.token_urlsafe
        - Suitable for session tokens, API keys, etc.
    """
    return secrets.token_urlsafe(length)


def compare_secure(a: str, b: str) -> bool:
    """
    Constant-time string comparison to prevent timing attacks.
    
    Args:
        a: First string
        b: Second string
    
    Returns:
        True if strings are equal
    
    Security:
        - Uses secrets.compare_digest
        - Resistant to timing attacks
    """
    return secrets.compare_digest(a, b)