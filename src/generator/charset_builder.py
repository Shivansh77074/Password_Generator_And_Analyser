

# ============================================================================
# File: src/generator/charset_builder.py
# ============================================================================
"""
Character set builder for password generation.
Constructs character sets based on user options.
"""

from typing import Dict, Set
from ..core.constants import UPPERCASE, LOWERCASE, DIGITS, SYMBOLS


class CharsetBuilder:
    """
    Builds character sets for password generation.
    Ensures proper character set construction and validation.
    """
    
    @staticmethod
    def build_charset(options: Dict[str, bool]) -> str:
        """
        Build character set from options.
        
        Args:
            options: Dict with keys: uppercase, lowercase, numbers, symbols
        
        Returns:
            Combined character set string
        
        Raises:
            ValueError: If no character sets selected
        """
        charset = ''
        
        if options.get('uppercase', False):
            charset += UPPERCASE
        if options.get('lowercase', False):
            charset += LOWERCASE
        if options.get('numbers', False):
            charset += DIGITS
        if options.get('symbols', False):
            charset += SYMBOLS
        
        if not charset:
            raise ValueError("At least one character set must be selected")
        
        return charset
    
    @staticmethod
    def get_required_chars(options: Dict[str, bool]) -> list:
        """
        Get list of required characters (one from each selected set).
        
        Args:
            options: Character set options
        
        Returns:
            List of character sets that must be represented
        """
        required = []
        
        if options.get('uppercase', False):
            required.append(UPPERCASE)
        if options.get('lowercase', False):
            required.append(LOWERCASE)
        if options.get('numbers', False):
            required.append(DIGITS)
        if options.get('symbols', False):
            required.append(SYMBOLS)
        
        return required
    
    @staticmethod
    def calculate_charset_size(options: Dict[str, bool]) -> int:
        """
        Calculate total size of character set.
        
        Args:
            options: Character set options
        
        Returns:
            Total number of unique characters
        """
        size = 0
        
        if options.get('uppercase', False):
            size += len(UPPERCASE)
        if options.get('lowercase', False):
            size += len(LOWERCASE)
        if options.get('numbers', False):
            size += len(DIGITS)
        if options.get('symbols', False):
            size += len(SYMBOLS)
        
        return size
    
    @staticmethod
    def validate_options(options: Dict[str, bool]) -> bool:
        """
        Validate character set options.
        
        Args:
            options: Options to validate
        
        Returns:
            True if valid
        """
        return any(options.values())