
# ============================================================================
# File: src/api/validators.py
# ============================================================================
""" 
Request validators for API endpoints.
Validates and sanitizes user input.
"""

from typing import Dict, Tuple, Optional
from config.web_settings import MAX_PASSWORD_LENGTH, MAX_BULK_GENERATION


class RequestValidator:
    """
    Validates API requests.
    """
    
    @staticmethod
    def validate_generate_request(data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate password generation request.
        
        Args:
            data: Request JSON data
        
        Returns:
            (is_valid, error_message)
        """
        # Check required fields
        if 'length' not in data:
            return False, 'Missing required field: length'
        
        if 'options' not in data:
            return False, 'Missing required field: options'
        
        # Validate length
        try:
            length = int(data['length'])
            if length < 4 or length > MAX_PASSWORD_LENGTH:
                return False, f'Length must be between 4 and {MAX_PASSWORD_LENGTH}'
        except (ValueError, TypeError):
            return False, 'Invalid length value'
        
        # Validate options
        options = data['options']
        if not isinstance(options, dict):
            return False, 'Options must be a dictionary'
        
        required_keys = ['uppercase', 'lowercase', 'numbers', 'symbols']
        if not all(key in options for key in required_keys):
            return False, f'Options must contain: {", ".join(required_keys)}'
        
        # Check at least one option is enabled
        if not any(options.values()):
            return False, 'At least one character set must be selected'
        
        return True, None
    
    @staticmethod
    def validate_bulk_request(data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate bulk generation request.
        
        Args:
            data: Request JSON data
        
        Returns:
            (is_valid, error_message)
        """
        # First validate basic generation params
        is_valid, error = RequestValidator.validate_generate_request(data)
        if not is_valid:
            return False, error
        
        # Check count
        if 'count' not in data:
            return False, 'Missing required field: count'
        
        try:
            count = int(data['count'])
            if count < 1 or count > MAX_BULK_GENERATION:
                return False, f'Count must be between 1 and {MAX_BULK_GENERATION}'
        except (ValueError, TypeError):
            return False, 'Invalid count value'
        
        return True, None
    
    @staticmethod
    def validate_analyze_request(data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate password analysis request.
        
        Args:
            data: Request JSON data
        
        Returns:
            (is_valid, error_message)
        """
        # Check required fields
        if 'password' not in data:
            return False, 'Missing required field: password'
        
        password = data['password']
        
        # Check type
        if not isinstance(password, str):
            return False, 'Password must be a string'
        
        # Check length
        if len(password) > MAX_PASSWORD_LENGTH:
            return False, f'Password exceeds maximum length of {MAX_PASSWORD_LENGTH}'
        
        return True, None
