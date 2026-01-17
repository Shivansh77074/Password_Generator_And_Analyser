
# ============================================================================
# File: src/api/middleware.py
# ============================================================================
"""
Security middleware for Flask application.
"""

from functools import wraps
from flask import request, jsonify
from config.web_settings import SECURITY_HEADERS


def add_security_headers(response):
    """
    Add security headers to response.
    
    Args:
        response: Flask response object
    
    Returns:
        Modified response
    """
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


def require_json(f):
    """
    Decorator to require JSON content type.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        return f(*args, **kwargs)
    return decorated_function


def handle_errors(f):
    """
    Decorator to handle errors gracefully.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log error here in production
            return jsonify({
                'success': False,
                'error': 'An internal error occurred'
            }), 500
    return decorated_function
