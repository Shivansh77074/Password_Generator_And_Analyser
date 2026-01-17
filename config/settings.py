

# ============================================================================
# File: config/settings.py
# ============================================================================
"""
Application-wide configuration settings.
All settings are immutable and security-focused.
"""

from typing import Final

# UI Configuration
UI_WINDOW_WIDTH: Final[int] = 750
UI_WINDOW_HEIGHT: Final[int] = 850
UI_PADDING: Final[int] = 20
UI_FONT_FAMILY: Final[str] = 'Arial'
UI_MONO_FONT: Final[str] = 'Courier'

# Generator Configuration
MIN_PASSWORD_LENGTH: Final[int] = 4
MAX_PASSWORD_LENGTH: Final[int] = 128
DEFAULT_PASSWORD_LENGTH: Final[int] = 16

# Security Configuration
CSPRNG_MODULE: Final[str] = 'secrets'  # Never change this
ALLOW_PASSWORD_HISTORY: Final[bool] = False  # Never enable
ALLOW_PASSWORD_LOGGING: Final[bool] = False  # Never enable

# Strength Scoring Thresholds
SCORE_WEAK_THRESHOLD: Final[int] = 40
SCORE_MEDIUM_THRESHOLD: Final[int] = 60
SCORE_STRONG_THRESHOLD: Final[int] = 80

# Entropy Thresholds (bits)
ENTROPY_WEAK: Final[float] = 40.0
ENTROPY_MEDIUM: Final[float] = 60.0
ENTROPY_STRONG: Final[float] = 80.0

# Crack Time Estimation (attempts per second)
BRUTE_FORCE_RATE: Final[int] = 1_000_000_000  # 1 billion/sec

# Policy Defaults
DEFAULT_POLICY_MIN_LENGTH: Final[int] = 8
DEFAULT_POLICY_MAX_LENGTH: Final[int] = 128
DEFAULT_REQUIRE_UPPERCASE: Final[bool] = True
DEFAULT_REQUIRE_LOWERCASE: Final[bool] = True
DEFAULT_REQUIRE_NUMBERS: Final[bool] = True
DEFAULT_REQUIRE_SYMBOLS: Final[bool] = False