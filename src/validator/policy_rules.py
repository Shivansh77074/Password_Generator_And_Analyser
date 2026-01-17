
# ============================================================================
# File: src/validator/policy_rules.py
# ============================================================================
"""
Password policy rules and configuration.
Defines customizable security policies for web applications.
"""

from dataclasses import dataclass
from typing import Optional
from config.settings import (
    DEFAULT_POLICY_MIN_LENGTH,
    DEFAULT_POLICY_MAX_LENGTH,
    DEFAULT_REQUIRE_UPPERCASE,
    DEFAULT_REQUIRE_LOWERCASE,
    DEFAULT_REQUIRE_NUMBERS,
    DEFAULT_REQUIRE_SYMBOLS
)


@dataclass
class PolicyRule:
    """
    Individual password policy rule.
    """
    name: str
    description: str
    enabled: bool
    error_message: str


class PasswordPolicy:
    """
    Configurable password policy for web applications.
    Defines security requirements and validation rules.
    """
    
    def __init__(self,
                 min_length: int = DEFAULT_POLICY_MIN_LENGTH,
                 max_length: int = DEFAULT_POLICY_MAX_LENGTH,
                 require_uppercase: bool = DEFAULT_REQUIRE_UPPERCASE,
                 require_lowercase: bool = DEFAULT_REQUIRE_LOWERCASE,
                 require_numbers: bool = DEFAULT_REQUIRE_NUMBERS,
                 require_symbols: bool = DEFAULT_REQUIRE_SYMBOLS,
                 min_entropy: Optional[float] = None,
                 forbid_common_patterns: bool = True,
                 forbid_sequential: bool = True):
        """
        Initialize password policy.
        
        Args:
            min_length: Minimum password length
            max_length: Maximum password length
            require_uppercase: Require uppercase letters
            require_lowercase: Require lowercase letters
            require_numbers: Require numbers
            require_symbols: Require symbols
            min_entropy: Minimum entropy in bits
            forbid_common_patterns: Reject common patterns
            forbid_sequential: Reject sequential patterns
        """
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_numbers = require_numbers
        self.require_symbols = require_symbols
        self.min_entropy = min_entropy
        self.forbid_common_patterns = forbid_common_patterns
        self.forbid_sequential = forbid_sequential
    
    def get_rules(self) -> list:
        """
        Get list of all policy rules.
        
        Returns:
            List of PolicyRule objects
        """
        rules = []
        
        rules.append(PolicyRule(
            name='min_length',
            description=f'Minimum {self.min_length} characters',
            enabled=True,
            error_message=f'Password must be at least {self.min_length} characters'
        ))
        
        if self.require_uppercase:
            rules.append(PolicyRule(
                name='uppercase',
                description='At least one uppercase letter',
                enabled=True,
                error_message='Password must contain at least one uppercase letter'
            ))
        
        if self.require_lowercase:
            rules.append(PolicyRule(
                name='lowercase',
                description='At least one lowercase letter',
                enabled=True,
                error_message='Password must contain at least one lowercase letter'
            ))
        
        if self.require_numbers:
            rules.append(PolicyRule(
                name='numbers',
                description='At least one number',
                enabled=True,
                error_message='Password must contain at least one number'
            ))
        
        if self.require_symbols:
            rules.append(PolicyRule(
                name='symbols',
                description='At least one symbol',
                enabled=True,
                error_message='Password must contain at least one symbol'
            ))
        
        if self.forbid_common_patterns:
            rules.append(PolicyRule(
                name='no_common_patterns',
                description='No common weak patterns',
                enabled=True,
                error_message='Password contains common weak patterns'
            ))
        
        return rules
    
    def to_dict(self) -> dict:
        """Convert policy to dictionary."""
        return {
            'min_length': self.min_length,
            'max_length': self.max_length,
            'require_uppercase': self.require_uppercase,
            'require_lowercase': self.require_lowercase,
            'require_numbers': self.require_numbers,
            'require_symbols': self.require_symbols,
            'min_entropy': self.min_entropy,
            'forbid_common_patterns': self.forbid_common_patterns,
            'forbid_sequential': self.forbid_sequential
        }
