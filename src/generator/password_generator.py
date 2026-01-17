

# ============================================================================
# File: src/generator/password_generator.py
# ============================================================================
"""
Secure password generator using cryptographically secure randomness.
Implements stateless password generation with guaranteed character diversity.
"""

from typing import Dict
from ..core.security import secure_random_choice, secure_shuffle
from ..core.exceptions import InvalidLengthError, InvalidCharsetError
from .charset_builder import CharsetBuilder
from .entropy_calculator import EntropyCalculator
from config.settings import MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH


class PasswordGenerator:
    """
    Stateless, cryptographically secure password generator.
    
    Security Guarantees:
        - Uses secrets module (CSPRNG)
        - No password history or state
        - Each generation is independent
        - Guarantees character diversity
    """
    
    def __init__(self):
        """
        Initialize password generator.
        
        Note: No state variables. All operations are stateless.
        """
        self.charset_builder = CharsetBuilder()
        self.entropy_calc = EntropyCalculator()
    
    def generate(self, length: int, options: Dict[str, bool]) -> str:
        """
        Generate a cryptographically secure random password.
        
        Args:
            length: Password length
            options: Dict with keys: uppercase, lowercase, numbers, symbols
        
        Returns:
            Generated password (exists only in return value)
        
        Raises:
            InvalidLengthError: If length is invalid
            InvalidCharsetError: If no character sets selected
        
        Security:
            - CSPRNG via secrets module
            - Stateless operation
            - Guaranteed character diversity
            - Secure shuffle prevents patterns
        """
        # Validate length
        if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
            raise InvalidLengthError(length, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
        
        # Validate and build character set
        if not self.charset_builder.validate_options(options):
            raise InvalidCharsetError()
        
        charset = self.charset_builder.build_charset(options)
        required_charsets = self.charset_builder.get_required_chars(options)
        
        # Ensure password can fit all required character types
        if len(required_charsets) > length:
            raise InvalidLengthError(
                length, 
                len(required_charsets), 
                MAX_PASSWORD_LENGTH
            )
        
        # Generate password with guaranteed diversity
        password_chars = []
        
        # Add one character from each required set
        for char_set in required_charsets:
            password_chars.append(secure_random_choice(char_set))
        
        # Fill remaining positions with random characters
        remaining = length - len(password_chars)
        for _ in range(remaining):
            password_chars.append(secure_random_choice(charset))
        
        # Securely shuffle to eliminate position patterns
        password_chars = secure_shuffle(password_chars)
        
        # Return password (no storage)
        return ''.join(password_chars)
    
    def generate_multiple(self, count: int, length: int, 
                         options: Dict[str, bool]) -> list:
        """
        Generate multiple passwords.
        
        Args:
            count: Number of passwords to generate
            length: Password length
            options: Character set options
        
        Returns:
            List of passwords
        
        Note: Each password is generated independently with no correlation.
        """
        return [self.generate(length, options) for _ in range(count)]
    
    def calculate_entropy(self, length: int, options: Dict[str, bool]) -> float:
        """
        Calculate entropy for given parameters.
        
        Args:
            length: Password length
            options: Character set options
        
        Returns:
            Entropy in bits
        """
        return self.entropy_calc.entropy_from_options(length, options)