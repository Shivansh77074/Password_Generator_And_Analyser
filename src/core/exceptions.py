
# ============================================================================
# File: src/core/exceptions.py
# ============================================================================
"""
Custom exceptions for password utility.
Provides clear error messages without exposing sensitive data.
"""


class PasswordUtilityError(Exception):
    """Base exception for password utility errors."""
    pass


class InvalidLengthError(PasswordUtilityError):
    """Raised when password length is invalid."""
    
    def __init__(self, length: int, min_len: int, max_len: int):
        self.length = length
        self.min_len = min_len
        self.max_len = max_len
        super().__init__(
            f"Invalid password length {length}. "
            f"Must be between {min_len} and {max_len}."
        )


class InvalidCharsetError(PasswordUtilityError):
    """Raised when no character sets are selected."""
    
    def __init__(self):
        super().__init__(
            "At least one character set must be selected "
            "(uppercase, lowercase, numbers, or symbols)."
        )


class PolicyViolationError(PasswordUtilityError):
    """Raised when password violates policy rules."""
    
    def __init__(self, violations: list):
        self.violations = violations
        super().__init__(
            f"Password violates policy: {'; '.join(violations)}"
        )


class InsufficientEntropyError(PasswordUtilityError):
    """Raised when password has insufficient entropy."""
    
    def __init__(self, entropy: float, required: float):
        self.entropy = entropy
        self.required = required
        super().__init__(
            f"Insufficient entropy: {entropy:.1f} bits "
            f"(required: {required:.1f} bits)"
        )