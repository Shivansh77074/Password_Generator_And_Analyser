
# ============================================================================
# File: config/web_settings.py
# ============================================================================
"""
Web application configuration.
Security-focused settings for Flask app.
"""

import os
from typing import Final

# Flask Configuration
SECRET_KEY: Final[str] = os.getenv('SECRET_KEY', os.urandom(32).hex())
DEBUG: Final[bool] = os.getenv('DEBUG', 'False').lower() == 'true'
HOST: Final[str] = os.getenv('HOST', '127.0.0.1')
PORT: Final[int] = int(os.getenv('PORT', 5000))

# CORS Configuration
CORS_ORIGINS: Final[list] = ['http://localhost:5000', 'http://127.0.0.1:5000']

# Rate Limiting
RATE_LIMIT_STORAGE: Final[str] = 'memory://'
RATE_LIMIT_GENERATE: Final[str] = '100 per minute'
RATE_LIMIT_ANALYZE: Final[str] = '200 per minute'
RATE_LIMIT_DEFAULT: Final[str] = '500 per hour'

# API Configuration
API_PREFIX: Final[str] = '/api/v1'
MAX_PASSWORD_LENGTH: Final[int] = 128
MAX_BULK_GENERATION: Final[int] = 50

# Security Headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
}
