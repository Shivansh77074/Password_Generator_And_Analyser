
# ============================================================================
# File: src/core/constants.py
# ============================================================================
"""
Security-focused constants and character sets.
All values are immutable and cryptographically safe.
"""

import string
from typing import Final, List

# Character Sets (immutable)
UPPERCASE: Final[str] = string.ascii_uppercase
LOWERCASE: Final[str] = string.ascii_lowercase
DIGITS: Final[str] = string.digits
SYMBOLS: Final[str] = string.punctuation

# Extended symbol set for maximum security
EXTENDED_SYMBOLS: Final[str] = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'

# Common weak password patterns
COMMON_PATTERNS: Final[List[str]] = [
    'password', 'pass', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', 'letmein', 'trustno1', 'dragon', 'baseball',
    'iloveyou', 'master', 'sunshine', 'ashley', 'bailey',
    'shadow', 'superman', 'qazwsx', 'michael', 'football',
    'welcome', 'jesus', 'ninja', 'mustang', 'admin',
    'login', 'passw0rd', 'p@ssword', 'test', 'user'
]

# Sequential character patterns
SEQUENTIAL_PATTERNS: Final[List[str]] = [
    'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij',
    'ijk', 'jkl', 'klm', 'lmn', 'mno', 'nop', 'opq', 'pqr',
    'qrs', 'rst', 'stu', 'tuv', 'uvw', 'vwx', 'wxy', 'xyz',
    '123', '234', '345', '456', '567', '678', '789',
    'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
    'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl',
    'zxc', 'xcv', 'cvb', 'vbn', 'bnm'
]

# Keyboard patterns
KEYBOARD_PATTERNS: Final[List[str]] = [
    'qwerty', 'asdfgh', 'zxcvbn', '1qaz2wsx', 'qazwsx',
    'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
]

# Repeated character patterns (regex)
REPEATED_CHAR_PATTERN: Final[str] = r'(.)\1{2,}'

# Date patterns (regex)
DATE_PATTERN: Final[str] = r'\d{2,4}[/-]\d{1,2}[/-]\d{1,2}'