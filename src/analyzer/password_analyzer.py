
# ============================================================================
# File: src/analyzer/password_analyzer.py
# ============================================================================
"""
Comprehensive password strength analyzer.
Performs read-only analysis without storing passwords.
"""

import re
import math
from typing import Dict
from .pattern_detector import PatternDetector
from .strength_scorer import StrengthScorer
from .crack_time_estimator import CrackTimeEstimator


class PasswordAnalyzer:
    """
    Stateless password analyzer with comprehensive strength analysis.
    
    Security Guarantee:
        - Read-only operations
        - No password storage
        - No state maintained
    """
    
    def __init__(self):
        """Initialize analyzer components."""
        self.pattern_detector = PatternDetector()
        self.strength_scorer = StrengthScorer()
        self.crack_time_estimator = CrackTimeEstimator()
    
    def analyze(self, password: str) -> Dict:
        """
        Perform comprehensive password analysis.
        
        Args:
            password: Password to analyze (not stored)
        
        Returns:
            Dict containing:
                - strength: str (Weak/Medium/Strong/Very Strong)
                - score: int (0-100)
                - entropy: float (bits)
                - length: int
                - has_uppercase: bool
                - has_lowercase: bool
                - has_numbers: bool
                - has_symbols: bool
                - diversity_score: float (0-1)
                - patterns: Dict of detected patterns
                - crack_time: str
                - security_level: str
                - recommendations: List[str]
        
        Security: Password analyzed in-place, never stored.
        """
        if not password:
            return self._empty_analysis()
        
        # Character type analysis
        analysis = {
            'length': len(password),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_numbers': bool(re.search(r'\d', password)),
            'has_symbols': bool(re.search(r'[^A-Za-z0-9]', password)),
        }
        
        # Pattern detection
        patterns = self.pattern_detector.detect_all_patterns(password)
        analysis.update(patterns)
        
        # Calculate diversity
        analysis['diversity_score'] = self._calculate_diversity(analysis)
        
        # Calculate entropy
        analysis['entropy'] = self._calculate_entropy(password, analysis)
        
        # Calculate score
        analysis['score'] = self.strength_scorer.calculate_score(password, analysis)
        
        # Determine strength
        analysis['strength'] = self.strength_scorer.get_strength_level(
            analysis['score']
        )
        
        # Estimate crack time
        analysis['crack_time'] = self.crack_time_estimator.estimate_from_entropy(
            analysis['entropy']
        )
        
        # Security level
        analysis['security_level'] = self.crack_time_estimator.get_security_level(
            analysis['entropy']
        )
        
        # Get recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        # Get detected pattern list
        analysis['detected_patterns'] = self.pattern_detector.get_detected_patterns(
            password
        )
        
        return analysis
    
    def _empty_analysis(self) -> Dict:
        """Return analysis for empty password."""
        return {
            'strength': 'Weak',
            'score': 0,
            'entropy': 0.0,
            'length': 0,
            'has_uppercase': False,
            'has_lowercase': False,
            'has_numbers': False,
            'has_symbols': False,
            'diversity_score': 0.0,
            'crack_time': 'Instant',
            'security_level': 'Very Weak',
            'recommendations': ['Enter a password to analyze'],
            'detected_patterns': []
        }
    
    def _calculate_diversity(self, analysis: Dict) -> float:
        """
        Calculate character diversity score.
        
        Args:
            analysis: Analysis dict
        
        Returns:
            Diversity score (0-1)
        """
        types_used = sum([
            analysis['has_uppercase'],
            analysis['has_lowercase'],
            analysis['has_numbers'],
            analysis['has_symbols']
        ])
        return types_used / 4.0
    
    def _calculate_entropy(self, password: str, analysis: Dict) -> float:
        """
        Calculate Shannon entropy.
        
        Args:
            password: Password string
            analysis: Analysis dict
        
        Returns:
            Entropy in bits
        """
        charset_size = 0
        
        if analysis['has_uppercase']:
            charset_size += 26
        if analysis['has_lowercase']:
            charset_size += 26
        if analysis['has_numbers']:
            charset_size += 10
        if analysis['has_symbols']:
            charset_size += 32
        
        if charset_size == 0:
            return 0.0
        
        return len(password) * math.log2(charset_size)
    
    def _generate_recommendations(self, analysis: Dict) -> list:
        """
        Generate improvement recommendations.
        
        Args:
            analysis: Analysis dict
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Length recommendations
        if analysis['length'] < 8:
            recommendations.append('Increase length to at least 8 characters')
        elif analysis['length'] < 12:
            recommendations.append('Consider increasing length to 12+ characters')
        
        # Diversity recommendations
        if not analysis['has_uppercase']:
            recommendations.append('Add uppercase letters (A-Z)')
        if not analysis['has_lowercase']:
            recommendations.append('Add lowercase letters (a-z)')
        if not analysis['has_numbers']:
            recommendations.append('Add numbers (0-9)')
        if not analysis['has_symbols']:
            recommendations.append('Add symbols (!@#$...)')
        
        # Pattern warnings
        if analysis.get('has_common_patterns', False):
            recommendations.append('Avoid common words and patterns')
        if analysis.get('has_sequential', False):
            recommendations.append('Avoid sequential characters (abc, 123)')
        if analysis.get('has_keyboard_patterns', False):
            recommendations.append('Avoid keyboard patterns (qwerty)')
        if analysis.get('has_repeated_chars', False):
            recommendations.append('Avoid repeated characters (aaa, 111)')
        
        # Entropy recommendations
        if analysis['entropy'] < 40:
            recommendations.append('Significantly increase password complexity')
        
        if not recommendations:
            recommendations.append('Password meets security best practices!')
        
        return recommendations
