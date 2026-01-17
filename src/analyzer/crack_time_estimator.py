
# ============================================================================
# File: src/analyzer/crack_time_estimator.py
# ============================================================================
"""
Crack time estimator for brute-force attack resistance.
Provides realistic time estimates based on modern attack capabilities.
"""

from config.settings import BRUTE_FORCE_RATE


class CrackTimeEstimator:
    """
    Estimates time required to crack password via brute force.
    """
    
    def __init__(self, attempts_per_second: int = BRUTE_FORCE_RATE):
        """
        Initialize estimator.
        
        Args:
            attempts_per_second: Brute force rate (default: 1 billion/sec)
        """
        self.attempts_per_second = attempts_per_second
    
    def estimate_from_entropy(self, entropy: float) -> str:
        """
        Estimate crack time from entropy.
        
        Args:
            entropy: Password entropy in bits
        
        Returns:
            Human-readable time estimate
        """
        if entropy <= 0:
            return 'Instant'
        
        # Calculate total combinations
        combinations = 2 ** entropy
        
        # Calculate average time (half the keyspace)
        seconds = combinations / (2 * self.attempts_per_second)
        
        return self._format_time(seconds)
    
    def estimate_from_length_and_charset(self, length: int, 
                                        charset_size: int) -> str:
        """
        Estimate crack time from password parameters.
        
        Args:
            length: Password length
            charset_size: Size of character set
        
        Returns:
            Human-readable time estimate
        """
        if length <= 0 or charset_size <= 0:
            return 'Instant'
        
        # Calculate entropy
        entropy = length * (charset_size ** 0.5)  # Simplified
        
        combinations = charset_size ** length
        seconds = combinations / (2 * self.attempts_per_second)
        
        return self._format_time(seconds)
    
    def _format_time(self, seconds: float) -> str:
        """
        Format seconds into human-readable string.
        
        Args:
            seconds: Time in seconds
        
        Returns:
            Formatted string
        """
        if seconds < 0.001:
            return 'Instant'
        elif seconds < 1:
            return 'Less than 1 second'
        elif seconds < 60:
            return f'{int(seconds)} seconds'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""}'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""}'
        elif seconds < 2592000:  # 30 days
            days = int(seconds / 86400)
            return f'{days} day{"s" if days != 1 else ""}'
        elif seconds < 31536000:  # 1 year
            months = int(seconds / 2592000)
            return f'{months} month{"s" if months != 1 else ""}'
        elif seconds < 3153600000:  # 100 years
            years = int(seconds / 31536000)
            return f'{years} year{"s" if years != 1 else ""}'
        elif seconds < 31536000000:  # 1000 years
            return 'Centuries'
        else:
            return 'Millennia+'
    
    def get_security_level(self, entropy: float) -> str:
        """
        Get security level based on crack time.
        
        Args:
            entropy: Password entropy
        
        Returns:
            Security level description
        """
        time_estimate = self.estimate_from_entropy(entropy)
        
        if 'Instant' in time_estimate or 'second' in time_estimate:
            return 'Very Weak - Crackable instantly'
        elif 'minute' in time_estimate or 'hour' in time_estimate:
            return 'Weak - Crackable in hours'
        elif 'day' in time_estimate:
            return 'Moderate - Crackable in days'
        elif 'month' in time_estimate:
            return 'Good - Crackable in months'
        elif 'year' in time_estimate and 'Centur' not in time_estimate:
            return 'Strong - Crackable in years'
        else:
            return 'Very Strong - Crackable in centuries+'
