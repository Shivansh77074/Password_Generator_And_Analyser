

# ============================================================================
# File: src/ui/main_window.py
# ============================================================================
"""
Main application window.
Combines generator and analyzer panels into unified interface.
"""

import tkinter as tk
from tkinter import ttk
from .generator_panel import GeneratorPanel
from .analyzer_panel import AnalyzerPanel
from .styles import COLORS, FONTS, PADDING, configure_ttk_styles
from config.settings import UI_WINDOW_WIDTH, UI_WINDOW_HEIGHT


class PasswordUtilityApp:
    """
    Main application window for password utility.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self._configure_window()
        self._setup_styles()
        self._create_widgets()
    
    def _configure_window(self):
        """Configure main window properties."""
        self.root.title('Secure Password Utility')
        self.root.geometry(f'{UI_WINDOW_WIDTH}x{UI_WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (UI_WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (UI_WINDOW_HEIGHT // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def _setup_styles(self):
        """Setup ttk styles."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        configure_ttk_styles(self.style)
    
    def _create_widgets(self):
        """Create all application widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=PADDING['main'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text='🔐 Secure Password Utility',
                         style='Title.TLabel')
        title.pack(pady=(0, PADDING['section']))
        
        # Generator panel
        self.generator_panel = GeneratorPanel(main_frame)
        self.generator_panel.pack(fill=tk.X, pady=(0, PADDING['section']))
        
        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=PADDING['section'])
        
        # Analyzer panel
        self.analyzer_panel = AnalyzerPanel(main_frame)
        self.analyzer_panel.pack(fill=tk.BOTH, expand=True)
        
        # Security notice
        self._create_security_notice(main_frame)
    
    def _create_security_notice(self, parent):
        """Create security notice at bottom."""
        notice_frame = ttk.Frame(parent)
        notice_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(PADDING['section'], 0))
        
        notice = ttk.Label(notice_frame,
                          text='🔒 All operations performed in memory only. '
                               'No passwords stored or logged.',
                          style='Security.TLabel')
        notice.pack()
    
    def run(self):
        """Start the application."""
        self.root.mainloop()
