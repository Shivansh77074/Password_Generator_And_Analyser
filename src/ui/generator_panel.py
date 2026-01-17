

# ============================================================================
# File: src/ui/generator_panel.py
# ============================================================================
"""
Password generator panel UI component.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ..generator import PasswordGenerator
from .styles import COLORS, FONTS, PADDING, configure_ttk_styles


class GeneratorPanel:
    """
    Password generator UI panel.
    Provides interface for password generation with customization.
    """
    
    def __init__(self, parent):
        """
        Initialize generator panel.
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.generator = PasswordGenerator()
        
        # UI variables
        self.current_password = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.entropy_var = tk.StringVar(value='Entropy: 0.0 bits')
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all generator panel widgets."""
        # Main frame
        self.frame = ttk.LabelFrame(self.parent, text='Password Generator', 
                                   padding=PADDING['section'])
        
        # Length control
        self._create_length_control()
        
        # Character set options
        self._create_charset_options()
        
        # Password display
        self._create_password_display()
        
        # Action buttons
        self._create_action_buttons()
        
        # Entropy display
        self._create_entropy_display()
    
    def _create_length_control(self):
        """Create password length slider."""
        length_frame = ttk.Frame(self.frame)
        length_frame.pack(fill=tk.X, pady=PADDING['widget'])
        
        ttk.Label(length_frame, text='Length:', 
                 font=FONTS['normal']).pack(side=tk.LEFT, padx=(0, 10))
        
        length_value = ttk.Label(length_frame, textvariable=self.length_var,
                                font=FONTS['normal'], width=3)
        length_value.pack(side=tk.LEFT)
        
        length_slider = ttk.Scale(length_frame, from_=4, to=64,
                                 variable=self.length_var,
                                 orient=tk.HORIZONTAL,
                                 command=self._on_length_change)
        length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
    
    def _create_charset_options(self):
        """Create character set checkboxes."""
        options_frame = ttk.LabelFrame(self.frame, text='Character Sets',
                                      padding=PADDING['widget'])
        options_frame.pack(fill=tk.X, pady=PADDING['widget'])
        
        # Create 2x2 grid of checkboxes
        ttk.Checkbutton(options_frame, text='Uppercase (A-Z)',
                       variable=self.uppercase_var,
                       command=self._update_entropy).grid(row=0, column=0, 
                                                          sticky=tk.W, pady=2)
        
        ttk.Checkbutton(options_frame, text='Lowercase (a-z)',
                       variable=self.lowercase_var,
                       command=self._update_entropy).grid(row=1, column=0,
                                                          sticky=tk.W, pady=2)
        
        ttk.Checkbutton(options_frame, text='Numbers (0-9)',
                       variable=self.numbers_var,
                       command=self._update_entropy).grid(row=0, column=1,
                                                          sticky=tk.W, 
                                                          padx=20, pady=2)
        
        ttk.Checkbutton(options_frame, text='Symbols (!@#$...)',
                       variable=self.symbols_var,
                       command=self._update_entropy).grid(row=1, column=1,
                                                          sticky=tk.W,
                                                          padx=20, pady=2)
    
    def _create_password_display(self):
        """Create password display field."""
        display_frame = ttk.Frame(self.frame)
        display_frame.pack(fill=tk.X, pady=PADDING['widget'])
        
        self.password_entry = ttk.Entry(display_frame,
                                       textvariable=self.current_password,
                                       font=FONTS['mono'],
                                       state='readonly')
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        copy_btn = ttk.Button(display_frame, text='📋 Copy',
                             command=self._copy_password,
                             width=10)
        copy_btn.pack(side=tk.LEFT, padx=(5, 0))
    
    def _create_action_buttons(self):
        """Create action buttons."""
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=PADDING['widget'])
        
        generate_btn = ttk.Button(button_frame, text='Generate Password',
                                 command=self._generate_password,
                                 style='Generate.TButton')
        generate_btn.pack()
    
    def _create_entropy_display(self):
        """Create entropy information display."""
        entropy_label = ttk.Label(self.frame, textvariable=self.entropy_var,
                                 font=FONTS['normal'],
                                 foreground=COLORS['primary'])
        entropy_label.pack(pady=(5, 0))
    
    def _get_options(self) -> dict:
        """Get current character set options."""
        return {
            'uppercase': self.uppercase_var.get(),
            'lowercase': self.lowercase_var.get(),
            'numbers': self.numbers_var.get(),
            'symbols': self.symbols_var.get()
        }
    
    def _on_length_change(self, value):
        """Handle length slider change."""
        self.length_var.set(int(float(value)))
        self._update_entropy()
    
    def _update_entropy(self):
        """Update entropy display."""
        try:
            options = self._get_options()
            if any(options.values()):
                length = self.length_var.get()
                entropy = self.generator.calculate_entropy(length, options)
                rating = self.generator.entropy_calc.get_entropy_rating(entropy)
                self.entropy_var.set(f'Entropy: {entropy:.1f} bits ({rating})')
            else:
                self.entropy_var.set('Entropy: 0.0 bits (Select character sets)')
        except Exception:
            self.entropy_var.set('Entropy: 0.0 bits')
    
    def _generate_password(self):
        """Generate new password."""
        try:
            options = self._get_options()
            length = self.length_var.get()
            
            if not any(options.values()):
                messagebox.showerror('Error',
                                   'Please select at least one character set')
                return
            
            # Generate password
            password = self.generator.generate(length, options)
            self.current_password.set(password)
            
            # Update entropy
            self._update_entropy()
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to generate password: {str(e)}')
    
    def _copy_password(self):
        """Copy password to clipboard."""
        password = self.current_password.get()
        
        if not password:
            messagebox.showwarning('Warning',
                                 'No password to copy. Generate one first.')
            return
        
        try:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(password)
            self.parent.update()
            messagebox.showinfo('Success', 'Password copied to clipboard!')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to copy: {str(e)}')
    
    def pack(self, **kwargs):
        """Pack the panel frame."""
        self.frame.pack(**kwargs)