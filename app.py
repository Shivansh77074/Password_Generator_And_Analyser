
# ============================================================================
# File: app.py (MODIFIED)
# ============================================================================
"""
Flask web application for Secure Password Utility.
Production-ready with security best practices.
"""

from flask import Flask, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config.web_settings import (
    SECRET_KEY, DEBUG, HOST, PORT,
    CORS_ORIGINS, RATE_LIMIT_STORAGE,
    RATE_LIMIT_GENERATE, RATE_LIMIT_ANALYZE, RATE_LIMIT_DEFAULT,
    API_PREFIX
)
from src.api import api_bp
from src.api.middleware import add_security_headers


def create_app():
    """
    Application factory.
    
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JSON_SORT_KEYS'] = False
    
    # CORS
    CORS(app, origins=CORS_ORIGINS, supports_credentials=False)
    
    # Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=RATE_LIMIT_STORAGE,
        default_limits=[RATE_LIMIT_DEFAULT]
    )
    
    # Apply specific rate limits to API routes
    limiter.limit(RATE_LIMIT_GENERATE)(api_bp.route('/generate'))
    limiter.limit(RATE_LIMIT_GENERATE)(api_bp.route('/generate/bulk'))
    limiter.limit(RATE_LIMIT_ANALYZE)(api_bp.route('/analyze'))
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix=API_PREFIX)
    
    # Add security headers to all responses
    app.after_request(add_security_headers)
    
    # Routes
    @app.route('/')
    def index():
        """Serve main application page."""
        return render_template('index.html')
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 errors."""
        return {'success': False, 'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        """Handle rate limit errors."""
        return {'success': False, 'error': 'Rate limit exceeded. Please try again later.'}, 429
    
    return app


if __name__ == '__main__':
    app = create_app()
    print(f"🔐 Secure Password Utility running on http://{HOST}:{PORT}")
    print(f"📡 API endpoint: http://{HOST}:{PORT}{API_PREFIX}")
    print(f"⚠️  Security: All operations in-memory only. No logging enabled.")
    app.run(host=HOST, port=PORT, debug=DEBUG)
