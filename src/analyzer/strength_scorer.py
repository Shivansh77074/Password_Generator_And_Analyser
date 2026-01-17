
# ============================================================================
# File: src/analyzer/strength_scorer.py
# ============================================================================
"""
Password strength scoring system.
Implements comprehensive scoring algorithm based on multiple factors.
"""

import math
from typing import Dict
from config.settings import (
    SCORE_WEAK_THRESHOLD,
    SCORE_MEDIUM_THRESHOLD,
    SCORE_STRONG_THRESHOLD
)


class StrengthScorer:
    """
    Calculates comprehensive password strength scores.
    """
    
    def calculate_score(self, password: str, analysis: Dict) -> int:
        """
        Calculate overall password strength score (0-100).
        
        Scoring factors:
            - Length (30 points)
            - Character diversity (25 points)
            - Entropy (30 points)
            - No common patterns (10 points)
            - No sequential patterns (5 points)
        
        Args:
            password: Password being analyzed
            analysis: Analysis results dict
        
        Returns:
            Score from 0-100
        """
        score = 0
        
        # Length scoring (0-30 points)
        score += self._score_length(analysis['length'])
        
        # Diversity scoring (0-25 points)
        score += self._score_diversity(analysis)
        
        # Entropy scoring (0-30 points)
        score += self._score_entropy(analysis['entropy'])
        
        # Pattern bonuses/penalties
        score += self._score_patterns(analysis)
        
        # Ensure score is within bounds
        return max(0, min(100, score))
    
    def _score_length(self, length: int) -> int:
        """
        Score based on password length.
        
        Args:
            length: Password length
        
        Returns:
            Points (0-30)
        """
        if length >= 20:
            return 30
        elif length >= 16:
            return 28
        elif length >= 12:
            return 24
        elif length >= 10:
            return 20
        elif length >= 8:
            return 15
        else:
            return length * 2
    
    def _score_diversity(self, analysis: Dict) -> int:
        """
        Score based on character type diversity.
        
        Args:
            analysis: Analysis dict
        
        Returns:
            Points (0-25)
        """
        diversity_score = analysis.get('diversity_score', 0)
        return int(diversity_score * 25)
    
    def _score_entropy(self, entropy: float) -> int:
        """
        Score based on password entropy.
        
        Args:
            entropy: Entropy in bits
        
        Returns:
            Points (0-30)
        """
        if entropy >= 100:
            return 30
        elif entropy >= 80:
            return 28
        elif entropy >= 60:
            return 24
        elif entropy >= 40:
            return 18
        else:
            return int(entropy / 2)
    
    def _score_patterns(self, analysis: Dict) -> int:
        """
        Score based on pattern analysis.
        
        Args:
            analysis: Analysis dict
        
        Returns:
            Points (can be negative)
        """
        score = 0
        
        # Bonuses for no patterns
        if not analysis.get('has_common_patterns', False):
            score += 10
        if not analysis.get('has_sequential', False):
            score += 5
        
        # Penalties for patterns
        if analysis.get('has_common_patterns', False):
            score -= 25
        if analysis.get('has_sequential', False):
            score -= 15
        if analysis.get('has_keyboard_patterns', False):
            score -= 10
        if analysis.get('has_repeated_chars', False):
            score -= 10
        if analysis.get('has_date_pattern', False):
            score -= 5
        
        return score
    
    def get_strength_level(self, score: int) -> str:
        """
        Determine strength level from score.
        
        Args:
            score: Strength score (0-100)
        
        Returns:
            Strength level string
        """
        if score >= SCORE_STRONG_THRESHOLD:
            return 'Very Strong'
        elif score >= SCORE_MEDIUM_THRESHOLD:
            return 'Strong'
        elif score >= SCORE_WEAK_THRESHOLD:
            return 'Medium'
        else:
            return 'Weak'
    
    def get_strength_color(self, strength: str) -> str:
        """
        Get color code for strength level.
        
        Args:
            strength: Strength level
        
        Returns:
            Color name
        """
        colors = {
            'Weak': 'red',
            'Medium': 'orange',
            'Strong': 'blue',
            'Very Strong': 'green'
        }
        return colors.get(strength, 'gray')