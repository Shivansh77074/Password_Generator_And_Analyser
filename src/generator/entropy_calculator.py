
# ============================================================================
# File: src/generator/entropy_calculator.py
# ============================================================================
"""
Entropy calculator for password strength measurement.
Calculates Shannon entropy and provides security metrics.
"""

import math
from typing import Dict


class EntropyCalculator:
    """
    Calculates password entropy and related security metrics.
    """
    
    @staticmethod
    def calculate_entropy(length: int, charset_size: int) -> float:
        """
        Calculate password entropy in bits.
        
        Formula: entropy = log2(charset_size ^ length)
                        = length * log2(charset_size)
        
        Args:
            length: Password length
            charset_size: Size of character set
        
        Returns:
            Entropy in bits
        """
        if charset_size <= 0 or length <= 0:
            return 0.0
        
        return length * math.log2(charset_size)
    
    @staticmethod
    def calculate_combinations(length: int, charset_size: int) -> float:
        """
        Calculate total possible password combinations.
        
        Args:
            length: Password length
            charset_size: Size of character set
        
        Returns:
            Number of possible combinations
        """
        if charset_size <= 0 or length <= 0:
            return 0.0
        
        return charset_size ** length
    
    @staticmethod
    def entropy_from_options(length: int, options: Dict[str, bool]) -> float:
        """
        Calculate entropy from generation options.
        
        Args:
            length: Password length
            options: Character set options
        
        Returns:
            Entropy in bits
        """
        charset_size = 0
        
        if options.get('uppercase', False):
            charset_size += 26
        if options.get('lowercase', False):
            charset_size += 26
        if options.get('numbers', False):
            charset_size += 10
        if options.get('symbols', False):
            charset_size += 32  # Approximate
        
        return EntropyCalculator.calculate_entropy(length, charset_size)
    
    @staticmethod
    def get_entropy_rating(entropy: float) -> str:
        """
        Get human-readable entropy rating.
        
        Args:
            entropy: Entropy in bits
        
        Returns:
            Rating string
        """
        if entropy >= 80:
            return "Excellent"
        elif entropy >= 60:
            return "Good"
        elif entropy >= 40:
            return "Fair"
        else:
            return "Poor"