#!/usr/bin/env python3
"""
Morning Motivation Quote Generator - Frameless Overlay
A true frameless desktop overlay window that displays motivational quotes.
"""

import tkinter as tk
from tkinter import font, ttk
import requests
import random
import sys
import json
import os
from urllib.parse import quote as url_quote

# Fallback quotes - MOTIVATIONAL & INSPIRATIONAL ONLY
# Focused on action, growth, persistence, and achieving goals
FALLBACK_QUOTES = [
    {
        "text": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt"
    },
    {
        "text": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "author": "Winston Churchill"
    },
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs"
    },
    {
        "text": "Don't watch the clock; do what it does. Keep going.",
        "author": "Sam Levenson"
    },
    {
        "text": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt"
    },
    {
        "text": "It does not matter how slowly you go as long as you do not stop.",
        "author": "Confucius"
    },
    {
        "text": "Everything you've ever wanted is on the other side of fear.",
        "author": "George Addair"
    },
    {
        "text": "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.",
        "author": "Roy T. Bennett"
    },
    {
        "text": "I learned that courage was not the absence of fear, but the triumph over it.",
        "author": "Nelson Mandela"
    },
    {
        "text": "Start where you are. Use what you have. Do what you can.",
        "author": "Arthur Ashe"
    },
    {
        "text": "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
        "author": "Roy T. Bennett"
    },
    {
        "text": "Hardships often prepare ordinary people for an extraordinary destiny.",
        "author": "C.S. Lewis"
    },
    {
        "text": "The only impossible journey is the one you never begin.",
        "author": "Tony Robbins"
    },
    {
        "text": "Your limitation—it's only your imagination.",
        "author": "Unknown"
    },
    {
        "text": "Great things never come from comfort zones.",
        "author": "Unknown"
    }
]

# Category keywords for filtering (from HTML V3.0.0)
CATEGORY_KEYWORDS = {
    'motivation': [
        'believe', 'achieve', 'success', 'dream', 'goal',
        'start', 'begin', 'action', 'courage', 'brave', 'try',
        'possible', 'impossible', 'persist', 'persevere',
        'overcome', 'conquer', 'triumph', 'victory', 'fight',
        'inspire', 'motivate', 'passion', 'purpose', 'destiny', 'future'
    ],
    'learning': [
        'learn', 'grow', 'improve', 'better', 'change',
        'adapt', 'develop', 'evolve', 'transform',
        'progress', 'advance', 'knowledge'
    ],
    'creativity': [
        'create', 'build', 'make', 'innovation', 'innovative',
        'creativity', 'creative', 'imagine', 'invention', 'design', 'art'
    ],
    'productivity': [
        'productivity', 'productive', 'focus', 'discipline',
        'work', 'effort', 'dedication', 'commitment', 'perseverance', 'do'
    ]
}

# Theme color schemes (from HTML V3.0.0)
THEMES = {
    'light': {
        'bg': '#ffffff',
        'text': '#1a1a1a',
        'author': '#666666',
        'hint': '#999999',
        'accent': '#667eea',
        'close_hover_bg': '#f0f0f0',
        'close_hover_fg': '#333333',
        'window_bg': '#e8eaed',
        'border': '#d0d0d0',
        'progress_bg': '#c0c0c0'
    },
    'dark': {
        'bg': '#1e1e1e',
        'text': '#e0e0e0',
        'author': '#a0a0a0',
        'hint': '#707070',
        'accent': '#667eea',
        'close_hover_bg': '#2d2d2d',
        'close_hover_fg': '#cccccc',
        'window_bg': '#2a2a2a',
        'border': '#3a3a3a',
        'progress_bg': '#4a4a4a'
    }
}

# Configuration
CONFIG = {
    "timer_duration": 15000,  # 15 seconds in milliseconds (default, will be overridden by settings)
    "api_url": "https://dummyjson.com/quotes/random",
    "api_timeout": 5,  # 5 seconds
    "window_width": 340,  # Default width (will be dynamic in Phase 3)
    "window_padding": 18,  # Tighter padding
    "corner_offset": 24,  # Distance from screen edges
}

# Settings file path
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.json')


class QuoteOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.timer_id = None
        self.is_paused = False
        self.start_time = None
        self.remaining_time = CONFIG["timer_duration"]
        self.settings_window = None

        # Widget references for theming
        self.widgets = {}

        # Load user settings
        self.settings = self.load_settings()

        # Apply settings to CONFIG
        CONFIG["timer_duration"] = self.settings["timerDuration"] * 1000  # Convert to ms

        # Update remaining time
        self.remaining_time = CONFIG["timer_duration"]

        # Setup window
        self.setup_window()

        # Fetch and display quote
        quote_data = self.get_quote()

        # Calculate responsive window width based on quote length
        window_width = self.calculate_window_width(quote_data["text"])
        CONFIG["window_width"] = window_width  # Update config for this quote

        self.create_widgets(quote_data)

        # Apply saved settings (position, fontSize, theme)
        self.apply_position(self.settings["position"], window_width)
        self.apply_font_size(self.settings["fontSize"])
        self.apply_theme(self.settings["theme"])

        # Start timer
        self.start_timer()

    def load_settings(self):
        """Load settings from JSON file"""
        defaults = {
            "timerDuration": 15,
            "position": "bottomRight",
            "fontSize": "medium",
            "category": "motivation",
            "theme": "light"
        }

        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    saved = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**defaults, **saved}
        except Exception as e:
            print(f"Error loading settings: {e}")

        return defaults

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def calculate_window_width(self, quote_text):
        """Calculate optimal window width based on quote text length"""
        # Create a temporary font to measure text
        temp_font = font.Font(family='Segoe UI', size=13, weight='normal')

        # Measure the text width
        text_width = temp_font.measure(f'"{quote_text}"')

        # Add padding (left + right + extra space)
        total_width = text_width + (CONFIG["window_padding"] * 2) + 60

        # Apply constraints: min 320px, max 800px
        window_width = max(320, min(total_width, 800))

        return window_width

    def apply_position(self, position, window_width=None):
        """Apply window position based on settings"""
        if window_width is None:
            window_width = CONFIG.get("window_width", 340)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_height = 200

        if position == "bottomRight":
            x = screen_width - window_width - CONFIG["corner_offset"]
            y = screen_height - window_height - CONFIG["corner_offset"]
        elif position == "bottomLeft":
            x = CONFIG["corner_offset"]
            y = screen_height - window_height - CONFIG["corner_offset"]
        elif position == "topRight":
            x = screen_width - window_width - CONFIG["corner_offset"]
            y = CONFIG["corner_offset"]
        elif position == "topLeft":
            x = CONFIG["corner_offset"]
            y = CONFIG["corner_offset"]
        else:
            # Default to bottomRight
            x = screen_width - window_width - CONFIG["corner_offset"]
            y = screen_height - window_height - CONFIG["corner_offset"]

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def apply_font_size(self, size):
        """Apply font size to quote label"""
        if hasattr(self, 'quote_label'):
            size_map = {
                "small": 11,
                "medium": 13,
                "large": 15
            }
            font_size = size_map.get(size, 13)
            quote_font = font.Font(family='Segoe UI', size=font_size, weight='normal')
            self.quote_label.configure(font=quote_font)

    def apply_theme(self, theme='light'):
        """Apply theme colors to all widgets"""
        colors = THEMES.get(theme, THEMES['light'])

        # Update root window
        self.root.configure(bg=colors['window_bg'])

        # Update all stored widgets
        if 'main_frame' in self.widgets:
            self.widgets['main_frame'].configure(
                bg=colors['window_bg'],
                highlightbackground=colors['border']
            )

        if 'top_bar' in self.widgets:
            self.widgets['top_bar'].configure(bg=colors['accent'])

        if 'button_frame' in self.widgets:
            self.widgets['button_frame'].configure(bg=colors['window_bg'])

        if 'content_frame' in self.widgets:
            self.widgets['content_frame'].configure(bg=colors['window_bg'])

        if 'settings_btn' in self.widgets:
            self.widgets['settings_btn'].configure(
                bg='#667eea',
                fg='white',
                activebackground='#5568d3',
                activeforeground='white'
            )

        if 'theme_btn' in self.widgets:
            # Update theme button text - shows opposite of current theme
            button_text = 'Dark' if theme == 'light' else 'Light'
            self.widgets['theme_btn'].configure(
                text=button_text,
                bg='#667eea',
                fg='white',
                activebackground='#5568d3',
                activeforeground='white'
            )

        if 'close_btn' in self.widgets:
            self.widgets['close_btn'].configure(
                fg=colors['hint'],
                bg=colors['window_bg'],
                activebackground='#ff5555',
                activeforeground='white'
            )

        if hasattr(self, 'quote_label'):
            self.quote_label.configure(
                fg=colors['text'],
                bg=colors['window_bg']
            )

        if 'author_label' in self.widgets:
            self.widgets['author_label'].configure(
                fg=colors['author'],
                bg=colors['window_bg']
            )

        if 'hint_label' in self.widgets:
            self.widgets['hint_label'].configure(
                fg=colors['hint'],
                bg=colors['window_bg']
            )

        if 'progress_frame' in self.widgets:
            self.widgets['progress_frame'].configure(bg=colors['progress_bg'])

        if 'progress_bar' in self.widgets:
            self.widgets['progress_bar'].configure(bg=colors['accent'])

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.settings.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.settings['theme'] = new_theme
        self.save_settings()
        self.apply_theme(new_theme)

    def setup_window(self):
        """Configure the frameless overlay window"""
        # Remove window decorations (frameless)
        self.root.overrideredirect(True)

        # Set window properties
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg='#e8eaed')

        # Set transparency for modern look
        try:
            self.root.attributes('-alpha', 0.96)  # Slight transparency for elegance
        except:
            pass  # Some systems don't support alpha

        # Note: Position will be set by apply_position() in __init__

        # Fade in animation
        self.root.attributes('-alpha', 0.0)
        self.fade_in()

    def fade_in(self, alpha=0.0):
        """Fade in animation"""
        if alpha < 0.96:
            alpha += 0.05
            try:
                self.root.attributes('-alpha', alpha)
                self.root.after(20, lambda: self.fade_in(alpha))
            except:
                pass

    def fade_out(self):
        """Fade out animation then close"""
        current_alpha = self.root.attributes('-alpha')
        if current_alpha > 0:
            new_alpha = current_alpha - 0.05
            try:
                self.root.attributes('-alpha', new_alpha)
                self.root.after(50, self.fade_out)
            except:
                self.root.quit()
        else:
            self.root.quit()

    def matches_category(self, quote_text, category='all'):
        """Check if a quote matches the selected category using word-boundary matching"""
        import re

        if category == 'all':
            return True

        keywords = CATEGORY_KEYWORDS.get(category, [])
        if not keywords:
            return True

        # Use word-boundary matching to avoid false positives
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', quote_text, re.IGNORECASE):
                return True

        return False

    def normalize_text(self, text):
        """Normalize text to fix capitalization issues
        Preserves punctuation (!, ?, ...) and handles curly apostrophes"""
        import re

        SENTENCE_SPLIT = re.compile(r'(?<=[.!?…])\s+(?=[\"""''(\[]?\w)')
        INTERIOR_UPPER = re.compile(r"(?<!^)(?<![''])[A-Z]")

        text = re.sub(r'\s+', ' ', text).strip()
        sentences = SENTENCE_SPLIT.split(text) or [text]

        cleaned = []
        for sentence in sentences:
            words = sentence.split()
            fixed = []
            for idx, word in enumerate(words):
                core = INTERIOR_UPPER.sub(lambda m: m.group(0).lower(), word)
                if core.isupper() and len(core) > 3:
                    core = core[0] + core[1:].lower()
                if idx == 0:
                    match = re.search(r'[A-Za-zÀ-ÖØ-öø-ÿ]', core)
                    if match:
                        pos = match.start()
                        core = core[:pos] + core[pos].upper() + core[pos + 1:]
                fixed.append(core)
            cleaned.append(' '.join(fixed))
        return ' '.join(cleaned)

    def get_quote(self):
        """Fetch quote from API with fallback, filtering by selected category"""
        max_attempts = 5  # Try up to 5 times to get a quote matching the category
        selected_category = self.settings.get('category', 'motivation')

        for attempt in range(max_attempts):
            try:
                response = requests.get(CONFIG["api_url"], timeout=CONFIG["api_timeout"])
                if response.status_code == 200:
                    data = response.json()
                    quote_text = data.get("quote", "")

                    # Check if quote matches selected category
                    if self.matches_category(quote_text, selected_category):
                        # Normalize the text to fix capitalization issues
                        normalized_text = self.normalize_text(quote_text)
                        return {
                            "text": normalized_text,
                            "author": data.get("author", "Unknown")
                        }
                    # If not matching category, try again
                    continue

            except Exception as e:
                print(f"API fetch attempt {attempt + 1} failed: {e}")
                break

        # Fallback to curated quotes filtered by category
        return self.get_fallback_quote(selected_category)

    def get_fallback_quote(self, category='all'):
        """Get a random fallback quote filtered by category"""
        if category == 'all':
            return random.choice(FALLBACK_QUOTES)

        # Filter fallback quotes by category
        filtered = [q for q in FALLBACK_QUOTES if self.matches_category(q["text"], category)]

        if filtered:
            return random.choice(filtered)

        # If no matches, return any quote
        return random.choice(FALLBACK_QUOTES)

    def create_widgets(self, quote_data):
        """Create the UI widgets"""
        # Main frame with shaded background
        main_frame = tk.Frame(
            self.root,
            bg='#e8eaed',
            highlightbackground='#d0d0d0',
            highlightthickness=1,
            bd=0
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.widgets['main_frame'] = main_frame

        # Top accent bar (gradient blue)
        top_bar = tk.Frame(main_frame, bg='#667eea', height=4)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        self.widgets['top_bar'] = top_bar

        # Button container frame at the top - ensures buttons don't overlap with content
        button_frame = tk.Frame(main_frame, bg='#e8eaed', height=30)
        button_frame.pack(fill=tk.X, side=tk.TOP, padx=CONFIG["window_padding"], pady=(CONFIG["window_padding"], 0))
        button_frame.pack_propagate(False)  # Maintain fixed height
        self.widgets['button_frame'] = button_frame

        # Modern button styling - using text instead of emojis for Windows compatibility
        # All buttons positioned in top-right with clear spacing

        # Close button (top-right, rightmost) - Using × symbol which renders well
        close_btn = tk.Button(
            button_frame,
            text='×',
            font=('Segoe UI', 18, 'bold'),
            fg='#666',
            bg='#e8eaed',
            bd=0,
            cursor='hand2',
            command=self.close_quote,
            activebackground='#ff5555',
            activeforeground='white',
            padx=8,
            pady=0,
            relief=tk.FLAT
        )
        close_btn.place(relx=1.0, rely=0.5, anchor='e', x=0, y=0)
        self.widgets['close_btn'] = close_btn

        # Theme toggle button (middle position) - Text-based
        theme_btn = tk.Button(
            button_frame,
            text='Light',  # Will be updated by apply_theme
            font=('Segoe UI', 8, 'bold'),
            fg='white',
            bg='#667eea',
            bd=0,
            cursor='hand2',
            command=self.toggle_theme,
            activebackground='#5568d3',
            activeforeground='white',
            padx=8,
            pady=4,
            relief=tk.FLAT
        )
        theme_btn.place(relx=1.0, rely=0.5, anchor='e', x=-35, y=0)
        self.widgets['theme_btn'] = theme_btn

        # Settings button (leftmost) - Text-based
        settings_btn = tk.Button(
            button_frame,
            text='Settings',
            font=('Segoe UI', 8, 'bold'),
            fg='white',
            bg='#667eea',
            bd=0,
            cursor='hand2',
            command=self.show_settings,
            activebackground='#5568d3',
            activeforeground='white',
            padx=8,
            pady=4,
            relief=tk.FLAT
        )
        settings_btn.place(relx=1.0, rely=0.5, anchor='e', x=-95, y=0)
        self.widgets['settings_btn'] = settings_btn

        # Content frame with padding - positioned BELOW buttons
        content_frame = tk.Frame(main_frame, bg='#e8eaed')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=CONFIG["window_padding"], pady=(0, CONFIG["window_padding"]))
        self.widgets['content_frame'] = content_frame

        # Quote text - NORMAL CASE, elegant typography
        quote_font = font.Font(family='Segoe UI', size=13, weight='normal')
        self.quote_label = tk.Label(
            content_frame,
            text=f'"{quote_data["text"]}"',
            font=quote_font,
            fg='#2c3e50',
            bg='#e8eaed',
            wraplength=CONFIG["window_width"] - CONFIG["window_padding"] * 2 - 30,
            justify=tk.LEFT,
            cursor='hand2'
        )
        self.quote_label.pack(pady=(0, 10), anchor='w')

        # Bind click to search
        self.quote_label.bind('<Button-1>', lambda e: self.search_quote(quote_data["text"]))

        # Author text - darker and more prominent
        author_font = font.Font(family='Segoe UI', size=12, slant='italic', weight='normal')
        author_label = tk.Label(
            content_frame,
            text=f'— {quote_data["author"]}',
            font=author_font,
            fg='#3a4a5a',
            bg='#e8eaed',
            justify=tk.RIGHT
        )
        author_label.pack(anchor='e', pady=(0, 8))
        self.widgets['author_label'] = author_label

        # Learn more hint
        hint_font = font.Font(family='Segoe UI', size=9, slant='italic')
        hint_label = tk.Label(
            content_frame,
            text='Click quote to learn more',
            font=hint_font,
            fg='#999',
            bg='#e8eaed',
            justify=tk.CENTER
        )
        hint_label.pack(anchor='center', pady=(4, 6))
        self.widgets['hint_label'] = hint_label

        # Progress bar (thinner, more subtle)
        self.progress_frame = tk.Frame(content_frame, bg='#c0c0c0', height=2)
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(6, 0))
        self.widgets['progress_frame'] = self.progress_frame

        self.progress_bar = tk.Frame(self.progress_frame, bg='#667eea', height=2)
        self.progress_bar.place(relwidth=1.0, relheight=1.0)
        self.widgets['progress_bar'] = self.progress_bar

        # Hover events for pause/resume
        main_frame.bind('<Enter>', lambda e: self.pause_timer())
        main_frame.bind('<Leave>', lambda e: self.resume_timer())

        # Keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.close_quote())

    def start_timer(self):
        """Start the countdown timer"""
        import time
        self.start_time = time.time()
        self.is_paused = False
        self.update_progress()

    def update_progress(self):
        """Update progress bar and check if time is up"""
        if self.is_paused:
            return

        import time
        elapsed = (time.time() - self.start_time) * 1000  # Convert to milliseconds
        progress = min(elapsed / CONFIG["timer_duration"], 1.0)

        # Update progress bar width (shrinking from right)
        self.progress_bar.place(relwidth=1.0 - progress, relheight=1.0)

        if progress >= 1.0:
            self.close_quote()
        else:
            self.timer_id = self.root.after(100, self.update_progress)

    def pause_timer(self):
        """Pause the timer on hover"""
        if not self.is_paused and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.is_paused = True
            import time
            elapsed = (time.time() - self.start_time) * 1000
            self.remaining_time = CONFIG["timer_duration"] - elapsed

    def resume_timer(self):
        """Resume the timer when mouse leaves"""
        if self.is_paused:
            import time
            self.start_time = time.time() - ((CONFIG["timer_duration"] - self.remaining_time) / 1000)
            self.is_paused = False
            self.update_progress()

    def close_quote(self):
        """Close the window with fade out animation"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.fade_out()

    def search_quote(self, text):
        """Open Google search for the quote"""
        import webbrowser
        search_query = url_quote(f'"{text}"')
        webbrowser.open(f'https://www.google.com/search?q={search_query}')

    def show_settings(self):
        """Open settings window"""
        # Pause timer while settings are open
        self.pause_timer()

        # If settings window already exists, focus it
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.focus()
            return

        # Create new settings window
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x350")
        self.settings_window.configure(bg='#e8eaed')
        self.settings_window.resizable(False, False)

        # Make it stay on top
        self.settings_window.attributes('-topmost', True)

        # Handle window close
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)

        # Main frame with padding
        main_frame = tk.Frame(self.settings_window, bg='#e8eaed', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Settings",
            font=('Segoe UI', 16, 'bold'),
            bg='#e8eaed',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))

        # Timer Duration Slider
        timer_frame = tk.Frame(main_frame, bg='#e8eaed')
        timer_frame.pack(fill=tk.X, pady=10)

        timer_label = tk.Label(
            timer_frame,
            text=f"Timer Duration: {self.settings['timerDuration']}s",
            font=('Segoe UI', 11),
            bg='#e8eaed',
            fg='#3a4a5a'
        )
        timer_label.pack(anchor='w')

        timer_slider = tk.Scale(
            timer_frame,
            from_=5,
            to=60,
            orient=tk.HORIZONTAL,
            resolution=5,
            bg='#e8eaed',
            fg='#667eea',
            highlightthickness=0,
            troughcolor='#c0c0c0',
            command=lambda v: self.on_timer_change(int(v), timer_label)
        )
        timer_slider.set(self.settings['timerDuration'])
        timer_slider.pack(fill=tk.X, pady=5)

        # Position Selector
        position_frame = tk.Frame(main_frame, bg='#e8eaed')
        position_frame.pack(fill=tk.X, pady=10)

        position_label = tk.Label(
            position_frame,
            text="Position:",
            font=('Segoe UI', 11),
            bg='#e8eaed',
            fg='#3a4a5a'
        )
        position_label.pack(anchor='w')

        position_var = tk.StringVar(value=self.settings['position'])
        position_options = [
            ("Bottom Right", "bottomRight"),
            ("Bottom Left", "bottomLeft"),
            ("Top Right", "topRight"),
            ("Top Left", "topLeft")
        ]

        position_dropdown = ttk.Combobox(
            position_frame,
            textvariable=position_var,
            values=[opt[0] for opt in position_options],
            state='readonly',
            font=('Segoe UI', 10)
        )
        # Set current value
        for opt_label, opt_value in position_options:
            if opt_value == self.settings['position']:
                position_dropdown.set(opt_label)
                break
        position_dropdown.pack(fill=tk.X, pady=5)
        position_dropdown.bind('<<ComboboxSelected>>', lambda e: self.on_position_change(position_var, position_options))

        # Font Size Selector
        font_size_frame = tk.Frame(main_frame, bg='#e8eaed')
        font_size_frame.pack(fill=tk.X, pady=10)

        font_size_label = tk.Label(
            font_size_frame,
            text="Font Size:",
            font=('Segoe UI', 11),
            bg='#e8eaed',
            fg='#3a4a5a'
        )
        font_size_label.pack(anchor='w')

        font_size_var = tk.StringVar(value=self.settings['fontSize'].capitalize())
        font_size_dropdown = ttk.Combobox(
            font_size_frame,
            textvariable=font_size_var,
            values=['Small', 'Medium', 'Large'],
            state='readonly',
            font=('Segoe UI', 10)
        )
        font_size_dropdown.set(self.settings['fontSize'].capitalize())
        font_size_dropdown.pack(fill=tk.X, pady=5)
        font_size_dropdown.bind('<<ComboboxSelected>>', lambda e: self.on_font_size_change(font_size_var))

        # Category Selector
        category_frame = tk.Frame(main_frame, bg='#e8eaed')
        category_frame.pack(fill=tk.X, pady=10)

        category_label = tk.Label(
            category_frame,
            text="Quote Category:",
            font=('Segoe UI', 11),
            bg='#e8eaed',
            fg='#3a4a5a'
        )
        category_label.pack(anchor='w')

        category_var = tk.StringVar(value=self.settings['category'])
        category_options = [
            ("Motivation & Inspiration", "motivation"),
            ("Learning & Growth", "learning"),
            ("Creativity & Innovation", "creativity"),
            ("Productivity & Focus", "productivity"),
            ("All Categories", "all")
        ]

        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=[opt[0] for opt in category_options],
            state='readonly',
            font=('Segoe UI', 10)
        )
        # Set current value
        for opt_label, opt_value in category_options:
            if opt_value == self.settings['category']:
                category_dropdown.set(opt_label)
                break
        category_dropdown.pack(fill=tk.X, pady=5)
        category_dropdown.bind('<<ComboboxSelected>>', lambda e: self.on_category_change(category_var, category_options))

        # Close button
        close_button = tk.Button(
            main_frame,
            text="Close",
            font=('Segoe UI', 11, 'bold'),
            bg='#667eea',
            fg='white',
            bd=0,
            cursor='hand2',
            command=self.close_settings,
            padx=20,
            pady=8
        )
        close_button.pack(pady=(20, 0))

    def on_timer_change(self, value, label):
        """Handle timer duration change"""
        self.settings['timerDuration'] = value
        label.config(text=f"Timer Duration: {value}s")
        CONFIG["timer_duration"] = value * 1000
        self.save_settings()

    def on_position_change(self, var, options):
        """Handle position change"""
        selected_label = var.get()
        for opt_label, opt_value in options:
            if opt_label == selected_label:
                self.settings['position'] = opt_value
                self.apply_position(opt_value)
                self.save_settings()
                break

    def on_font_size_change(self, var):
        """Handle font size change"""
        size = var.get().lower()
        self.settings['fontSize'] = size
        self.apply_font_size(size)
        self.save_settings()

    def on_category_change(self, var, options):
        """Handle category change"""
        selected_label = var.get()
        for opt_label, opt_value in options:
            if opt_label == selected_label:
                self.settings['category'] = opt_value
                self.save_settings()
                break

    def close_settings(self):
        """Close settings window and resume timer"""
        if self.settings_window:
            self.settings_window.destroy()
            self.settings_window = None
        # Resume timer
        self.resume_timer()

    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = QuoteOverlay()
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
