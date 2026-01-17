
# ============================================================================
# File: src/validator/policy_validator.py
# ============================================================================
"""
Password policy validator.
Validates passwords against configurable security policies.
"""

from typing import Dict, List
from .policy_rules import PasswordPolicy
from ..analyzer.password_analyzer import PasswordAnalyzer


class PolicyValidator:
    """
    Validates passwords against security policies.
    """
    
    def __init__(self, policy: PasswordPolicy):
        """
        Initialize validator with policy.
        
        Args:
            policy: PasswordPolicy instance
        """
        self.policy = policy
        self.analyzer = PasswordAnalyzer()
    
    def validate(self, password: str) -> Dict:
        """
        Validate password against policy.
        
        Args:
            password: Password to validate (not stored)
        
        Returns:
            Dict with:
                - valid: bool
                - errors: List[str]
                - warnings: List[str]
        
        Security: Password validated in-place, never stored.
        """
        errors = []
        warnings = []
        
        # Basic length check
        if len(password) < self.policy.min_length:
            errors.append(
                f'Password must be at least {self.policy.min_length} characters'
            )
        
        if len(password) > self.policy.max_length:
            errors.append(
                f'Password must not exceed {self.policy.max_length} characters'
            )
        
        # Character type requirements
        if self.policy.require_uppercase and not any(c.isupper() for c in password):
            errors.append('Password must contain at least one uppercase letter')
        
        if self.policy.require_lowercase and not any(c.islower() for c in password):
            errors.append('Password must contain at least one lowercase letter')
        
        if self.policy.require_numbers and not any(c.isdigit() for c in password):
            errors.append('Password must contain at least one number')
        
        if self.policy.require_symbols and not any(not c.isalnum() for c in password):
            errors.append('Password must contain at least one symbol')
        
        # Analyze for patterns and entropy
        analysis = self.analyzer.analyze(password)
        
        # Pattern checks
        if self.policy.forbid_common_patterns and analysis.get('has_common_patterns'):
            errors.append('Password contains common weak patterns')
        
        if self.policy.forbid_sequential and analysis.get('has_sequential'):
            errors.append('Password contains sequential characters')
        
        # Entropy check
        if self.policy.min_entropy and analysis['entropy'] < self.policy.min_entropy:
            errors.append(
                f'Password entropy too low '
                f'({analysis["entropy"]:.1f} < {self.policy.min_entropy} bits)'
            )
        
        # Generate warnings for weak but valid passwords
        if not errors:
            if analysis['score'] < 60:
                warnings.append('Password is weak. Consider making it stronger.')
            
            if not self.policy.require_symbols and not analysis['has_symbols']:
                warnings.append('Adding symbols would significantly improve strength')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'score': analysis['score'],
            'strength': analysis['strength']
        }