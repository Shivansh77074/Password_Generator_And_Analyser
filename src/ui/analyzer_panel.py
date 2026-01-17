
# ============================================================================
# File: src/ui/analyzer_panel.py
# ============================================================================
"""
Password analyzer panel UI component.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ..analyzer import PasswordAnalyzer
from ..validator import PolicyValidator, PasswordPolicy
from .styles import COLORS, FONTS, PADDING, get_strength_color


class AnalyzerPanel:
    """
    Password analyzer UI panel.
    Provides interface for password strength analysis.
    """
    
    def __init__(self, parent):
        """
        Initialize analyzer panel.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.analyzer = PasswordAnalyzer()
        self.policy = PasswordPolicy()
        self.validator = PolicyValidator(self.policy)
        
        # UI variables
        self.show_password_var = tk.BooleanVar(value=False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all analyzer panel widgets."""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text='Password Analyzer',
                                   padding=PADDING['section'])
        
        # Input section
        self._create_input_section()
        
        # Action button
        self._create_action_button()
        
        # Results display
        self._create_results_display()
    
    def _create_input_section(self):
        """Create password input section."""
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill=tk.X, pady=PADDING['widget'])
        
        ttk.Label(input_frame, text='Enter password to analyze:',
                 font=FONTS['normal']).pack(anchor=tk.W)
        
        # Password entry
        entry_container = ttk.Frame(input_frame)
        entry_container.pack(fill=tk.X, pady=(5, 0))
        
        self.password_entry = ttk.Entry(entry_container,
                                       font=FONTS['mono'],
                                       show='●')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clear button
        clear_btn = ttk.Button(entry_container, text='Clear',
                              command=self._clear_input,
                              width=8)
        clear_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Show/hide toggle
        show_check = ttk.Checkbutton(input_frame, text='Show password',
                                    variable=self.show_password_var,
                                    command=self._toggle_visibility)
        show_check.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_action_button(self):
        """Create analyze button."""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=PADDING['widget'])
        
        analyze_btn = ttk.Button(button_frame, text='Analyze Password',
                                command=self._analyze_password,
                                style='Generate.TButton')
        analyze_btn.pack()
    
    def _create_results_display(self):
        """Create results text display."""
        results_frame = ttk.LabelFrame(self.frame, text='Analysis Results',
                                      padding=PADDING['widget'])
        results_frame.pack(fill=tk.BOTH, expand=True, pady=PADDING['widget'])
        
        # Text widget with scrollbar
        text_container = ttk.Frame(results_frame)
        text_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(text_container,
                                   height=15,
                                   width=60,
                                   font=FONTS['mono'],
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   state='disabled')
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.results_text.yview)
        
        # Configure text tags for colors
        self._configure_text_tags()
    
    def _configure_text_tags(self):
        """Configure text widget color tags."""
        self.results_text.tag_configure('weak', foreground=COLORS['weak'])
        self.results_text.tag_configure('medium', foreground=COLORS['medium'])
        self.results_text.tag_configure('strong', foreground=COLORS['strong'])
        self.results_text.tag_configure('very_strong', foreground=COLORS['very_strong'])
        self.results_text.tag_configure('heading', font=FONTS['heading'])
        self.results_text.tag_configure('success', foreground=COLORS['success'])
        self.results_text.tag_configure('warning', foreground=COLORS['warning'])
    
    def _toggle_visibility(self):
        """Toggle password visibility."""
        if self.show_password_var.get():
            self.password_entry.configure(show='')
        else:
            self.password_entry.configure(show='●')
    
    def _clear_input(self):
        """Clear password input and results."""
        self.password_entry.delete(0, tk.END)
        self._clear_results()
    
    def _clear_results(self):
        """Clear results display."""
        self.results_text.configure(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.configure(state='disabled')
    
    def _analyze_password(self):
        """Analyze entered password."""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showwarning('Warning',
                                 'Please enter a password to analyze')
            return
        
        try:
            # Perform analysis
            analysis = self.analyzer.analyze(password)
            validation = self.validator.validate(password)
            
            # Display results
            self._display_results(analysis, validation)
            
        except Exception as e:
            messagebox.showerror('Error', f'Analysis failed: {str(e)}')
    
    def _display_results(self, analysis: dict, validation: dict):
        """
        Display analysis results.
        
        Args:
            analysis: Analysis results dict
            validation: Validation results dict
        """
        self.results_text.configure(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        # Strength header
        strength = analysis['strength']
        tag = strength.lower().replace(' ', '_')
        self.results_text.insert(tk.END, f"STRENGTH: {strength.upper()}\n", 
                                ['heading', tag])
        self.results_text.insert(tk.END, f"Score: {analysis['score']}/100\n\n")
        
        # Metrics
        self.results_text.insert(tk.END, "METRICS\n", 'heading')
        self.results_text.insert(tk.END, f"Length: {analysis['length']} characters\n")
        self.results_text.insert(tk.END, f"Entropy: {analysis['entropy']:.1f} bits\n")
        self.results_text.insert(tk.END, f"Diversity: {analysis['diversity_score']:.0%}\n")
        self.results_text.insert(tk.END, f"Crack Time: {analysis['crack_time']}\n")
        self.results_text.insert(tk.END, f"Security: {analysis['security_level']}\n\n")
        
        # Character types
        self.results_text.insert(tk.END, "CHARACTER TYPES\n", 'heading')
        self._insert_check('Uppercase', analysis['has_uppercase'])
        self._insert_check('Lowercase', analysis['has_lowercase'])
        self._insert_check('Numbers', analysis['has_numbers'])
        self._insert_check('Symbols', analysis['has_symbols'])
        self.results_text.insert(tk.END, "\n")
        
        # Detected patterns
        if analysis['detected_patterns']:
            self.results_text.insert(tk.END, "DETECTED ISSUES\n", 'heading')
            for pattern in analysis['detected_patterns']:
                self.results_text.insert(tk.END, f"  ⚠  {pattern}\n", 'warning')
            self.results_text.insert(tk.END, "\n")
        
        # Policy validation
        self.results_text.insert(tk.END, "POLICY VALIDATION\n", 'heading')
        if validation['valid']:
            self.results_text.insert(tk.END, "  ✓  Meets policy requirements\n", 
                                   'success')
        else:
            for error in validation['errors']:
                self.results_text.insert(tk.END, f"  ✗  {error}\n", 'weak')
        
        if validation['warnings']:
            self.results_text.insert(tk.END, "\nWarnings:\n")
            for warning in validation['warnings']:
                self.results_text.insert(tk.END, f"  •  {warning}\n", 'warning')
        
        self.results_text.insert(tk.END, "\n")
        
        # Recommendations
        if analysis['recommendations']:
            self.results_text.insert(tk.END, "RECOMMENDATIONS\n", 'heading')
            for rec in analysis['recommendations']:
                self.results_text.insert(tk.END, f"  •  {rec}\n")
        
        self.results_text.configure(state='disabled')
    
    def _insert_check(self, label: str, value: bool):
        """Insert checkmark line."""
        symbol = '✓' if value else '✗'
        tag = 'success' if value else 'weak'
        self.results_text.insert(tk.END, f"  {symbol}  {label}: ", tag)
        self.results_text.insert(tk.END, f"{value}\n")
    
    def pack(self, **kwargs):
        """Pack the panel frame."""
        self.frame.pack(**kwargs)
