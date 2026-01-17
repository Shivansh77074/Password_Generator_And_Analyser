

# ============================================================================
# File: src/analyzer/pattern_detector.py
# ============================================================================
"""
Pattern detection for password analysis.
Detects common weak patterns and security issues.
"""

import re
from typing import List, Dict
from ..core.constants import (
    COMMON_PATTERNS,
    SEQUENTIAL_PATTERNS,
    KEYBOARD_PATTERNS,
    REPEATED_CHAR_PATTERN,
    DATE_PATTERN
)


class PatternDetector:
    """
    Detects weak patterns and security issues in passwords.
    All operations are read-only and stateless.
    """
    
    def __init__(self):
        """Initialize pattern detector."""
        self.common_patterns = COMMON_PATTERNS
        self.sequential_patterns = SEQUENTIAL_PATTERNS
        self.keyboard_patterns = KEYBOARD_PATTERNS
    
    def detect_all_patterns(self, password: str) -> Dict[str, bool]:
        """
        Detect all pattern types in password.
        
        Args:
            password: Password to analyze (not stored)
        
        Returns:
            Dict of pattern detection results
        """
        return {
            'has_common_patterns': self.has_common_patterns(password),
            'has_sequential': self.has_sequential_patterns(password),
            'has_keyboard_patterns': self.has_keyboard_patterns(password),
            'has_repeated_chars': self.has_repeated_characters(password),
            'has_date_pattern': self.has_date_pattern(password),
            'has_number_only_suffix': self.has_number_suffix(password),
        }
    
    def has_common_patterns(self, password: str) -> bool:
        """
        Check if password contains common weak patterns.
        
        Args:
            password: Password to check
        
        Returns:
            True if common patterns found
        """
        password_lower = password.lower()
        return any(pattern in password_lower for pattern in self.common_patterns)
    
    def has_sequential_patterns(self, password: str) -> bool:
        """
        Check for sequential character patterns (abc, 123, etc.).
        
        Args:
            password: Password to check
        
        Returns:
            True if sequential patterns found
        """
        password_lower = password.lower()
        
        for pattern in self.sequential_patterns:
            if pattern in password_lower or pattern[::-1] in password_lower:
                return True
        
        return False
    
    def has_keyboard_patterns(self, password: str) -> bool:
        """
        Check for keyboard layout patterns (qwerty, asdfgh, etc.).
        
        Args:
            password: Password to check
        
        Returns:
            True if keyboard patterns found
        """
        password_lower = password.lower()
        return any(pattern in password_lower for pattern in self.keyboard_patterns)
    
    def has_repeated_characters(self, password: str, min_repeat: int = 3) -> bool:
        """
        Check for repeated characters (aaa, 111, etc.).
        
        Args:
            password: Password to check
            min_repeat: Minimum number of repetitions
        
        Returns:
            True if repeated characters found
        """
        pattern = r'(.)\1{' + str(min_repeat - 1) + r',}'
        return bool(re.search(pattern, password))
    
    def has_date_pattern(self, password: str) -> bool:
        """
        Check for date patterns (1990, 01/01/2000, etc.).
        
        Args:
            password: Password to check
        
        Returns:
            True if date patterns found
        """
        return bool(re.search(DATE_PATTERN, password))
    
    def has_number_suffix(self, password: str) -> bool:
        """
        Check if password ends with numbers only (weak pattern).
        
        Args:
            password: Password to check
        
        Returns:
            True if ends with numbers
        """
        return bool(re.search(r'\d+$', password))
    
    def get_detected_patterns(self, password: str) -> List[str]:
        """
        Get list of all detected pattern types.
        
        Args:
            password: Password to analyze
        
        Returns:
            List of detected pattern names
        """
        patterns = []
        results = self.detect_all_patterns(password)
        
        pattern_names = {
            'has_common_patterns': 'Common weak patterns',
            'has_sequential': 'Sequential characters',
            'has_keyboard_patterns': 'Keyboard patterns',
            'has_repeated_chars': 'Repeated characters',
            'has_date_pattern': 'Date patterns',
            'has_number_only_suffix': 'Numbers-only suffix'
        }
        
        for key, detected in results.items():
            if detected:
                patterns.append(pattern_names[key])
        
        return patterns