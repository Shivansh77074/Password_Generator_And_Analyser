
# ============================================================================
# File: src/ui/styles.py
# ============================================================================
"""
UI styling and theme configuration.
"""

from typing import Dict

# Color scheme
COLORS = {
    'primary': '#2196F3',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'weak': '#F44336',
    'medium': '#FF9800',
    'strong': '#2196F3',
    'very_strong': '#4CAF50',
    'background': '#FFFFFF',
    'text': '#212121',
    'secondary_text': '#757575',
    'border': '#BDBDBD'
}

# Font configurations
FONTS = {
    'title': ('Arial', 20, 'bold'),
    'heading': ('Arial', 14, 'bold'),
    'normal': ('Arial', 10),
    'mono': ('Courier', 12),
    'small': ('Arial', 9, 'italic')
}

# Widget padding
PADDING = {
    'main': 20,
    'section': 15,
    'widget': 10,
    'small': 5
}


def get_strength_color(strength: str) -> str:
    """
    Get color for strength level.
    
    Args:
        strength: Strength level string
    
    Returns:
        Color code
    """
    strength_lower = strength.lower().replace(' ', '_')
    return COLORS.get(strength_lower, COLORS['text'])


def configure_ttk_styles(style):
    """
    Configure ttk widget styles.
    
    Args:
        style: ttk.Style instance
    """
    # Configure button style
    style.configure('Generate.TButton', 
                   font=('Arial', 11, 'bold'),
                   padding=10)
    
    # Configure label styles
    style.configure('Title.TLabel', 
                   font=FONTS['title'],
                   foreground=COLORS['primary'])
    
    style.configure('Heading.TLabel', 
                   font=FONTS['heading'])
    
    style.configure('Security.TLabel',
                   font=FONTS['small'],
                   foreground=COLORS['success'])