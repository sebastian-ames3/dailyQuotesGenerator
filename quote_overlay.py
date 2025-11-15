#!/usr/bin/env python3
"""
Morning Motivation Quote Generator - Frameless Overlay

A lightweight desktop overlay that displays motivational quotes from DummyJSON API
with offline fallback support. Features include customizable dark/light themes,
screen positions, quote categories, font sizes, and auto-close timer with
hover-to-pause functionality.

Author: Sebastian Ames
License: MIT
Version: 5.0.2
Python: 3.7+

Usage:
    python quote_overlay.py          # Run normally
    python quote_overlay.py --debug  # Run with debug output

Dependencies:
    - requests==2.32.3 (API calls)
    - Pillow==11.0.0 (optional, for gradient backgrounds)

Features:
    - Frameless overlay window (always-on-top)
    - Dark/Light theme support
    - 4 screen positions (corners)
    - 4 quote categories + All
    - Adjustable font size (small/medium/large)
    - Configurable timer (5-60 seconds)
    - Hover to pause timer
    - Click quote to search Google
    - Settings persistence (JSON file)
    - Responsive window sizing
    - Diagonal gradient backgrounds (with Pillow)

For setup and installation, see README.md and SETUP.md
"""

import json
import os
import random
import re
import shutil
import sys
import tempfile
import time
import tkinter as tk
import webbrowser
from tkinter import font, ttk
from urllib.parse import quote as url_quote

import requests

# PIL for advanced visual effects (V5.0.0+)
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Advanced visual effects disabled.")

# Debug mode - controlled via command line argument (--debug)
DEBUG_MODE = '--debug' in sys.argv

# Version information
__version__ = "5.0.2"
__author__ = "Sebastian Ames"
__license__ = "MIT"

# Animation and UI constants
WINDOW_OPACITY = 0.96          # Slight transparency for elegant look
FADE_IN_STEP = 0.12            # Opacity increment per frame (faster)
FADE_OUT_STEP = 0.16           # Opacity decrement per frame (faster)
FADE_IN_DELAY_MS = 15          # Milliseconds between fade-in frames
FADE_OUT_DELAY_MS = 12         # Milliseconds between fade-out frames

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

# Theme color schemes - Monochrome Modern (V5.0.0)
THEMES = {
    'light': {
        'bg': '#ffffff',          # Pure white
        'bg_gradient': '#f5f5f5',  # Very light gray (for diagonal gradient)
        'text': '#0a0a0a',        # Almost black
        'author': '#525252',      # Medium gray
        'hint': '#a3a3a3',        # Light gray
        'accent': '#171717',      # Charcoal (buttons)
        'accent_hover': '#404040', # Lighter charcoal
        'close_hover_bg': '#fee2e2',  # Soft red tint
        'close_hover_fg': '#dc2626',  # Red
        'window_bg': '#ffffff',   # Same as bg
        'border': '#e5e5e5',      # Light gray border
        'progress_bg': '#d4d4d4', # Light gray bar
        'shadow': 'rgba(10, 10, 10, 0.15)'  # Subtle black shadow
    },
    'dark': {
        'bg': '#0a0a0a',          # Almost black
        'bg_gradient': '#1a1a1a',  # Slightly lighter black (for diagonal gradient)
        'text': '#fafafa',        # Off-white
        'author': '#a3a3a3',      # Light gray
        'hint': '#737373',        # Medium-light gray
        'accent': '#404040',      # Medium gray (buttons) - FIXED from white
        'accent_hover': '#525252', # Lighter gray on hover
        'close_hover_bg': '#7f1d1d', # Dark red
        'close_hover_fg': '#fecaca',  # Light red
        'window_bg': '#0a0a0a',   # Same as bg
        'border': '#262626',      # Dark gray border
        'progress_bg': '#404040', # Dark gray bar
        'shadow': 'rgba(0, 0, 0, 0.4)'  # Stronger shadow for dark mode
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

# Pre-compiled regex patterns for performance
# Sentence splitter - handles straight and curly quotes properly
SENTENCE_SPLIT_PATTERN = re.compile(
    r'(?<=[.!?…])\s+(?=["\'""''(\[]?\w)',
    re.UNICODE
)


def create_diagonal_gradient(width, height, color1, color2):
    """
    Create a diagonal gradient image (top-left to bottom-right) using PIL.
    Optimized version using numpy-like array operations.

    Args:
        width: Image width in pixels
        height: Image height in pixels
        color1: Starting color (hex string like '#faf8f5')
        color2: Ending color (hex string like '#f3ede6')

    Returns:
        PIL Image object with diagonal gradient, or None if PIL unavailable or invalid size
    """
    if not PIL_AVAILABLE:
        # Fallback: solid color image
        return None

    # SECURITY: Validate image dimensions to prevent excessive memory usage
    MAX_WIDTH = 1920   # Full HD width
    MAX_HEIGHT = 1080  # Full HD height

    if width <= 0 or height <= 0 or width > MAX_WIDTH or height > MAX_HEIGHT:
        print(f"Warning: Invalid gradient size {width}x{height}, using fallback")
        return None

    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    # Create image with putdata for better performance
    image = Image.new('RGB', (width, height))

    # Maximum distance is diagonal length
    max_distance = (width**2 + height**2) ** 0.5

    # Pre-calculate all pixel colors
    pixels = []
    for y in range(height):
        for x in range(width):
            # Calculate distance from top-left corner (0,0)
            distance = (x**2 + y**2) ** 0.5
            # Normalize to 0-1 range
            ratio = min(distance / max_distance, 1.0)

            # Interpolate between colors
            r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * ratio)
            g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * ratio)
            b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * ratio)

            pixels.append((r, g, b))

    # Apply all pixels at once (much faster than point-by-point)
    image.putdata(pixels)

    return image


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
        """Load settings from JSON file with validation"""
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

                    # SECURITY: Validate all settings values before using them
                    validated = {}

                    # Validate timerDuration (must be int/float in range 5-60)
                    if 'timerDuration' in saved:
                        timer = saved['timerDuration']
                        if isinstance(timer, (int, float)) and 5 <= timer <= 60:
                            validated['timerDuration'] = int(timer)

                    # Validate position (must be one of allowed values)
                    if 'position' in saved:
                        allowed_positions = ['bottomRight', 'bottomLeft', 'topRight', 'topLeft']
                        if saved['position'] in allowed_positions:
                            validated['position'] = saved['position']

                    # Validate fontSize (must be one of allowed values)
                    if 'fontSize' in saved:
                        allowed_sizes = ['small', 'medium', 'large']
                        if saved['fontSize'] in allowed_sizes:
                            validated['fontSize'] = saved['fontSize']

                    # Validate category (must be one of allowed categories)
                    if 'category' in saved:
                        allowed_categories = ['motivation', 'learning', 'creativity', 'productivity', 'all']
                        if saved['category'] in allowed_categories:
                            validated['category'] = saved['category']

                    # Validate theme (must be light or dark)
                    if 'theme' in saved:
                        if saved['theme'] in ['light', 'dark']:
                            validated['theme'] = saved['theme']

                    # Merge validated settings with defaults
                    return {**defaults, **validated}
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error loading settings: {e}")
            else:
                print("Unable to load saved settings. Using defaults.")

        return defaults

    def save_settings(self):
        """Save settings to JSON file using atomic write to prevent corruption"""
        tmp_path = None
        try:
            # Write to temporary file first (atomic write pattern)
            with tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                dir=os.path.dirname(SETTINGS_FILE),
                suffix='.tmp'
            ) as tmp:
                json.dump(self.settings, tmp, indent=2)
                tmp_path = tmp.name

            # Atomic rename (replaces old file only after new one is complete)
            shutil.move(tmp_path, SETTINGS_FILE)

        except Exception as e:
            if DEBUG_MODE:
                print(f"Error saving settings: {e}")
            else:
                print("Unable to save settings. Changes may not persist.")
            # Clean up temporary file if it exists
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass  # Best effort cleanup

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
                bg=colors['accent'],
                fg='white',
                activebackground=colors['accent_hover'],
                activeforeground='white'
            )

        if 'theme_btn' in self.widgets:
            # Update theme button text - shows opposite of current theme
            button_text = 'Dark' if theme == 'light' else 'Light'
            self.widgets['theme_btn'].configure(
                text=button_text,
                bg=colors['accent'],
                fg='white',
                activebackground=colors['accent_hover'],
                activeforeground='white'
            )

        if 'close_btn' in self.widgets:
            self.widgets['close_btn'].configure(
                fg=colors['hint'],
                bg=colors['window_bg'],
                activebackground=colors['close_hover_bg'],
                activeforeground=colors['close_hover_fg']
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
        # Get current theme colors
        colors = THEMES.get(self.settings.get('theme', 'light'), THEMES['light'])

        # Remove window decorations (frameless)
        self.root.overrideredirect(True)

        # Set window properties
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg=colors['window_bg'])

        # Set transparency for modern look
        try:
            self.root.attributes('-alpha', WINDOW_OPACITY)
        except:
            pass  # Some systems don't support alpha

        # Note: Position will be set by apply_position() in __init__

        # Fade in animation
        self.root.attributes('-alpha', 0.0)
        self.fade_in()

    def fade_in(self, alpha=0.0):
        """Fade in animation - snappy and fast (V5.0.0)"""
        if alpha < WINDOW_OPACITY:
            alpha += FADE_IN_STEP
            try:
                self.root.attributes('-alpha', alpha)
                self.root.after(FADE_IN_DELAY_MS, lambda: self.fade_in(alpha))
            except:
                pass

    def fade_out(self):
        """Fade out animation then close - snappy and fast (V5.0.0)"""
        current_alpha = self.root.attributes('-alpha')
        if current_alpha > 0:
            new_alpha = current_alpha - FADE_OUT_STEP
            try:
                self.root.attributes('-alpha', new_alpha)
                self.root.after(FADE_OUT_DELAY_MS, self.fade_out)
            except:
                self.root.quit()
        else:
            self.root.quit()

    def matches_category(self, quote_text, category='all'):
        """Check if a quote matches the selected category using word-boundary matching"""
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

        Handles:
        - ALL CAPS words: "HELLO WORLD" → "Hello world"
        - ALL CAPS with apostrophes: "WHO'S THERE" → "Who's there"
        - Interior capitals: "HeLLo" → "Hello"
        - Capitals after apostrophes: "It'S" → "It's"
        - Proper sentence capitalization (only first word capitalized)
        - Preserves punctuation (!, ?, ..., etc.)
        - Properly handles both straight (') and curly (') quotes
        """
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Split into sentences using pre-compiled pattern
        sentences = SENTENCE_SPLIT_PATTERN.split(text) if SENTENCE_SPLIT_PATTERN.search(text) else [text]

        cleaned_sentences = []

        for sentence in sentences:
            words = sentence.split()
            fixed_words = []

            for word_idx, word in enumerate(words):
                # Step 1: Check if word is ALL CAPS
                # Extract only alphabetic characters to check
                alpha_chars = [c for c in word if c.isalpha()]

                if alpha_chars and len(alpha_chars) > 1 and all(c.isupper() for c in alpha_chars):
                    # ALL CAPS word (like "HELLO" or "WHO'S") - lowercase everything
                    word = word.lower()

                # Step 2: Fix interior capitals
                # Process character by character to handle apostrophes correctly
                new_chars = []
                for char_idx, char in enumerate(word):
                    if char_idx == 0:
                        # Lowercase first char for now (will capitalize later if needed)
                        new_chars.append(char.lower() if char.isalpha() else char)
                    elif char.isupper() and char.isalpha():
                        # Check if previous char was apostrophe
                        if char_idx > 0 and word[char_idx - 1] in ["'", "'"]:
                            # Capital after apostrophe - lowercase it (fixes "It'S" → "It's")
                            new_chars.append(char.lower())
                        else:
                            # Interior capital not after apostrophe - lowercase it
                            new_chars.append(char.lower())
                    else:
                        new_chars.append(char)

                word = ''.join(new_chars)

                # Step 3: Capitalize first letter ONLY if this is the first word in sentence
                if word_idx == 0:
                    for i, char in enumerate(word):
                        if char.isalpha():
                            word = word[:i] + word[i].upper() + word[i+1:]
                            break

                fixed_words.append(word)

            cleaned_sentences.append(' '.join(fixed_words))

        return ' '.join(cleaned_sentences)

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
                    author = data.get("author", "Unknown")

                    # SECURITY: Validate API response data types and lengths
                    if not isinstance(quote_text, str) or not isinstance(author, str):
                        continue  # Skip invalid data types

                    if len(quote_text) > 1000 or len(author) > 100:
                        continue  # Skip overly long quotes to prevent UI overflow

                    # Check if quote matches selected category
                    if self.matches_category(quote_text, selected_category):
                        # Normalize the text to fix capitalization issues
                        normalized_text = self.normalize_text(quote_text)
                        return {
                            "text": normalized_text,
                            "author": author
                        }
                    # If not matching category, try again
                    continue

            except Exception as e:
                if DEBUG_MODE:
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
        # Get current theme colors
        colors = THEMES.get(self.settings.get('theme', 'light'), THEMES['light'])

        # Create gradient background if PIL is available
        gradient_bg_color = colors['window_bg']
        if PIL_AVAILABLE:
            window_width = CONFIG.get("window_width", 340)
            window_height = 200

            gradient_img = create_diagonal_gradient(
                window_width, window_height,
                colors['bg'], colors['bg_gradient']
            )

            if gradient_img:
                self.gradient_photo = ImageTk.PhotoImage(gradient_img)
                # Create a label to hold the gradient background (fullscreen)
                gradient_label = tk.Label(self.root, image=self.gradient_photo, bd=0, highlightthickness=0)
                gradient_label.place(x=0, y=0, width=window_width, height=window_height)
                # Keep reference to prevent garbage collection
                self.widgets['gradient_bg'] = gradient_label
                # Use empty string for bg to make frames semi-transparent visually
                # (They'll still have the gradient showing through)

        # Main frame - no background if gradient exists (shows gradient through)
        main_frame = tk.Frame(
            self.root,
            bg=gradient_bg_color if not PIL_AVAILABLE else gradient_bg_color,
            highlightbackground=colors['border'],
            highlightthickness=1,
            bd=0
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        # Raise to be on top of gradient
        if PIL_AVAILABLE:
            main_frame.lift()
        self.widgets['main_frame'] = main_frame

        # Top accent bar
        top_bar = tk.Frame(main_frame, bg=colors['accent'], height=4)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        self.widgets['top_bar'] = top_bar

        # Button container frame at the top - ensures buttons don't overlap with content
        button_frame = tk.Frame(main_frame, bg=colors['window_bg'], height=30)
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
            fg=colors['hint'],
            bg=colors['window_bg'],
            bd=0,
            cursor='hand2',
            command=self.close_quote,
            activebackground=colors['close_hover_bg'],
            activeforeground=colors['close_hover_fg'],
            padx=8,
            pady=0,
            relief=tk.FLAT
        )
        close_btn.place(relx=1.0, rely=0.5, anchor='e', x=0, y=0)
        self.widgets['close_btn'] = close_btn

        # Theme toggle button (middle position) - Text-based
        theme_btn = tk.Button(
            button_frame,
            text='Dark' if self.settings.get('theme', 'light') == 'light' else 'Light',
            font=('Segoe UI', 8, 'bold'),
            fg='white',
            bg=colors['accent'],
            bd=0,
            cursor='hand2',
            command=self.toggle_theme,
            activebackground=colors['accent_hover'],
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
            bg=colors['accent'],
            bd=0,
            cursor='hand2',
            command=self.show_settings,
            activebackground=colors['accent_hover'],
            activeforeground='white',
            padx=8,
            pady=4,
            relief=tk.FLAT
        )
        settings_btn.place(relx=1.0, rely=0.5, anchor='e', x=-95, y=0)
        self.widgets['settings_btn'] = settings_btn

        # Content frame with padding - positioned BELOW buttons
        content_frame = tk.Frame(main_frame, bg=colors['window_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=CONFIG["window_padding"], pady=(0, CONFIG["window_padding"]))
        self.widgets['content_frame'] = content_frame

        # Quote text - NORMAL CASE, elegant typography
        quote_font = font.Font(family='Segoe UI', size=13, weight='normal')
        self.quote_label = tk.Label(
            content_frame,
            text=f'"{quote_data["text"]}"',
            font=quote_font,
            fg=colors['text'],
            bg=colors['window_bg'],
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
            fg=colors['author'],
            bg=colors['window_bg'],
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
            fg=colors['hint'],
            bg=colors['window_bg'],
            justify=tk.CENTER
        )
        hint_label.pack(anchor='center', pady=(4, 6))
        self.widgets['hint_label'] = hint_label

        # Progress bar (thinner, more subtle)
        self.progress_frame = tk.Frame(content_frame, bg=colors['progress_bg'], height=2)
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(6, 0))
        self.widgets['progress_frame'] = self.progress_frame

        self.progress_bar = tk.Frame(self.progress_frame, bg=colors['accent'], height=2)
        self.progress_bar.place(relwidth=1.0, relheight=1.0)
        self.widgets['progress_bar'] = self.progress_bar

        # Hover events for pause/resume
        main_frame.bind('<Enter>', lambda e: self.pause_timer())
        main_frame.bind('<Leave>', lambda e: self.resume_timer())

        # Keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.close_quote())

    def start_timer(self):
        """Start the countdown timer"""
        self.start_time = time.time()
        self.is_paused = False
        self.update_progress()

    def update_progress(self):
        """Update progress bar and check if time is up"""
        if self.is_paused:
            return

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
            elapsed = (time.time() - self.start_time) * 1000
            self.remaining_time = CONFIG["timer_duration"] - elapsed

    def resume_timer(self):
        """Resume the timer when mouse leaves"""
        if self.is_paused:
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

        # Get current theme colors
        colors = THEMES.get(self.settings.get('theme', 'light'), THEMES['light'])

        # Create new settings window
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x350")
        self.settings_window.configure(bg=colors['window_bg'])
        self.settings_window.resizable(False, False)

        # Make it stay on top
        self.settings_window.attributes('-topmost', True)

        # Handle window close
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)

        # Main frame with padding
        main_frame = tk.Frame(self.settings_window, bg=colors['window_bg'], padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Settings",
            font=('Segoe UI', 16, 'bold'),
            bg=colors['window_bg'],
            fg=colors['text']
        )
        title_label.pack(pady=(0, 20))

        # Timer Duration Slider
        timer_frame = tk.Frame(main_frame, bg=colors['window_bg'])
        timer_frame.pack(fill=tk.X, pady=10)

        timer_label = tk.Label(
            timer_frame,
            text=f"Timer Duration: {self.settings['timerDuration']}s",
            font=('Segoe UI', 11),
            bg=colors['window_bg'],
            fg=colors['text']
        )
        timer_label.pack(anchor='w')

        timer_slider = tk.Scale(
            timer_frame,
            from_=5,
            to=60,
            orient=tk.HORIZONTAL,
            resolution=5,
            bg=colors['window_bg'],
            fg=colors['accent'],
            highlightthickness=0,
            troughcolor=colors['progress_bg'],
            command=lambda v: self.on_timer_change(int(v), timer_label)
        )
        timer_slider.set(self.settings['timerDuration'])
        timer_slider.pack(fill=tk.X, pady=5)

        # Position Selector
        position_frame = tk.Frame(main_frame, bg=colors['window_bg'])
        position_frame.pack(fill=tk.X, pady=10)

        position_label = tk.Label(
            position_frame,
            text="Position:",
            font=('Segoe UI', 11),
            bg=colors['window_bg'],
            fg=colors['text']
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
        font_size_frame = tk.Frame(main_frame, bg=colors['window_bg'])
        font_size_frame.pack(fill=tk.X, pady=10)

        font_size_label = tk.Label(
            font_size_frame,
            text="Font Size:",
            font=('Segoe UI', 11),
            bg=colors['window_bg'],
            fg=colors['text']
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
        category_frame = tk.Frame(main_frame, bg=colors['window_bg'])
        category_frame.pack(fill=tk.X, pady=10)

        category_label = tk.Label(
            category_frame,
            text="Quote Category:",
            font=('Segoe UI', 11),
            bg=colors['window_bg'],
            fg=colors['text']
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
            bg=colors['accent'],
            fg='white',
            activebackground=colors['accent_hover'],
            activeforeground='white',
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
