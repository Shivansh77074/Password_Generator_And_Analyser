
# ============================================================================
# File: src/api/routes.py
# ============================================================================
"""
API routes for password utility.
RESTful endpoints with security best practices.
"""

from flask import Blueprint, request, jsonify
from ..generator import PasswordGenerator
from ..analyzer import PasswordAnalyzer
from ..validator import PolicyValidator, PasswordPolicy
from .validators import RequestValidator
from .middleware import require_json, handle_errors

api_bp = Blueprint('api', __name__)

# Initialize components (stateless)
generator = PasswordGenerator()
analyzer = PasswordAnalyzer()
policy = PasswordPolicy()
validator = PolicyValidator(policy)
request_validator = RequestValidator()


@api_bp.route('/generate', methods=['POST'])
@require_json
@handle_errors
def generate_password():
    """
    Generate a single password.
    
    Request JSON:
        {
            "length": int,
            "options": {
                "uppercase": bool,
                "lowercase": bool,
                "numbers": bool,
                "symbols": bool
            }
        }
    
    Response JSON:
        {
            "success": bool,
            "password": str,
            "entropy": float,
            "strength_estimate": str
        }
    """
    data = request.get_json()
    
    # Validate request
    is_valid, error = request_validator.validate_generate_request(data)
    if not is_valid:
        return jsonify({'success': False, 'error': error}), 400
    
    # Generate password
    length = int(data['length'])
    options = data['options']
    
    password = generator.generate(length, options)
    entropy = generator.calculate_entropy(length, options)
    entropy_rating = generator.entropy_calc.get_entropy_rating(entropy)
    
    return jsonify({
        'success': True,
        'password': password,
        'entropy': round(entropy, 2),
        'strength_estimate': entropy_rating
    })


@api_bp.route('/generate/bulk', methods=['POST'])
@require_json
@handle_errors
def generate_bulk():
    """
    Generate multiple passwords.
    
    Request JSON:
        {
            "length": int,
            "count": int,
            "options": {...}
        }
    
    Response JSON:
        {
            "success": bool,
            "passwords": [str],
            "count": int
        }
    """
    data = request.get_json()
    
    # Validate request
    is_valid, error = request_validator.validate_bulk_request(data)
    if not is_valid:
        return jsonify({'success': False, 'error': error}), 400
    
    # Generate passwords
    length = int(data['length'])
    count = int(data['count'])
    options = data['options']
    
    passwords = generator.generate_multiple(count, length, options)
    
    return jsonify({
        'success': True,
        'passwords': passwords,
        'count': len(passwords)
    })


@api_bp.route('/analyze', methods=['POST'])
@require_json
@handle_errors
def analyze_password():
    """
    Analyze password strength.
    
    Request JSON:
        {
            "password": str
        }
    
    Response JSON:
        {
            "success": bool,
            "analysis": {...}
        }
    """
    data = request.get_json()
    
    # Validate request
    is_valid, error = request_validator.validate_analyze_request(data)
    if not is_valid:
        return jsonify({'success': False, 'error': error}), 400
    
    # Analyze password
    password = data['password']
    analysis = analyzer.analyze(password)
    
    # Validate against policy
    validation = validator.validate(password)
    
    return jsonify({
        'success': True,
        'analysis': {
            'strength': analysis['strength'],
            'score': analysis['score'],
            'entropy': round(analysis['entropy'], 2),
            'length': analysis['length'],
            'diversity_score': round(analysis['diversity_score'], 2),
            'has_uppercase': analysis['has_uppercase'],
            'has_lowercase': analysis['has_lowercase'],
            'has_numbers': analysis['has_numbers'],
            'has_symbols': analysis['has_symbols'],
            'crack_time': analysis['crack_time'],
            'security_level': analysis['security_level'],
            'detected_patterns': analysis['detected_patterns'],
            'recommendations': analysis['recommendations'],
            'policy_valid': validation['valid'],
            'policy_errors': validation['errors'],
            'policy_warnings': validation['warnings']
        }
    })


@api_bp.route('/entropy/calculate', methods=['POST'])
@require_json
@handle_errors
def calculate_entropy():
    """
    Calculate entropy for given parameters.
    
    Request JSON:
        {
            "length": int,
            "options": {...}
        }
    
    Response JSON:
        {
            "success": bool,
            "entropy": float,
            "rating": str
        }
    """
    data = request.get_json()
    
    is_valid, error = request_validator.validate_generate_request(data)
    if not is_valid:
        return jsonify({'success': False, 'error': error}), 400
    
    length = int(data['length'])
    options = data['options']
    
    entropy = generator.calculate_entropy(length, options)
    rating = generator.entropy_calc.get_entropy_rating(entropy)
    
    return jsonify({
        'success': True,
        'entropy': round(entropy, 2),
        'rating': rating
    })


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'password-utility-api'
    })
