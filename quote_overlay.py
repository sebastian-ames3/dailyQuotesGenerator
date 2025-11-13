#!/usr/bin/env python3
"""
Morning Motivation Quote Generator - Frameless Overlay
A true frameless desktop overlay window that displays motivational quotes.
"""

import tkinter as tk
from tkinter import font
import requests
import random
import json
import sys
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

# Configuration
CONFIG = {
    "timer_duration": 15000,  # 15 seconds in milliseconds
    "api_url": "https://dummyjson.com/quotes/random",
    "api_timeout": 5,  # 5 seconds
    "window_width": 340,  # Smaller, notification-sized width
    "window_padding": 18,  # Tighter padding
    "corner_offset": 24,  # Distance from screen edges
}


class QuoteOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.timer_id = None
        self.is_paused = False
        self.start_time = None
        self.remaining_time = CONFIG["timer_duration"]

        # Setup window
        self.setup_window()

        # Fetch and display quote
        quote_data = self.get_quote()
        self.create_widgets(quote_data)

        # Start timer
        self.start_timer()

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

        # Position window in bottom-right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position (bottom-right) - notification size
        x = screen_width - CONFIG["window_width"] - CONFIG["corner_offset"]
        y = screen_height - 200 - CONFIG["corner_offset"]  # Increased height to show author

        self.root.geometry(f'{CONFIG["window_width"]}x200+{x}+{y}')

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

    def is_motivational(self, quote_text):
        """Check if a quote is motivational/inspirational (not just wisdom)"""
        # Keywords that indicate motivational/inspirational content
        motivational_keywords = [
            'believe', 'can', 'will', 'achieve', 'success', 'dream', 'goal',
            'start', 'begin', 'do', 'action', 'courage', 'brave', 'try',
            'possible', 'impossible', 'never give up', 'keep going', 'persist',
            'overcome', 'conquer', 'triumph', 'victory', 'win', 'fight',
            'inspire', 'motivate', 'passion', 'purpose', 'destiny', 'future',
            'change', 'grow', 'improve', 'better', 'greatest', 'potential',
            # User-requested keywords
            'productivity', 'productive', 'inspirational', 'creativity',
            'creative', 'innovation', 'innovative', 'create', 'make', 'build'
        ]

        # Keywords that suggest wisdom/philosophy (filter these out)
        wisdom_keywords = [
            'think', 'know', 'knowledge', 'wise', 'wisdom', 'understand',
            'philosophy', 'truth', 'reality', 'existence', 'meaning'
        ]

        quote_lower = quote_text.lower()

        # Count motivational vs wisdom keywords
        motivational_count = sum(1 for keyword in motivational_keywords if keyword in quote_lower)
        wisdom_count = sum(1 for keyword in wisdom_keywords if keyword in quote_lower)

        # Prefer motivational quotes (more motivational than wisdom keywords)
        return motivational_count > wisdom_count

    def normalize_text(self, text):
        """Normalize text to proper sentence case, removing ALL weird capitalizations"""
        import re

        # Remove extra whitespace
        text = ' '.join(text.split())

        # Split into sentences
        sentences = text.split('. ')
        normalized = []

        for sentence in sentences:
            if sentence:
                words = sentence.split()
                fixed_words = []

                for i, word in enumerate(words):
                    # Skip empty words
                    if not word:
                        continue

                    # Check if word has weird capitalization (capital letters in middle)
                    # Examples: "They'Re", "It'S", "DoN'T"
                    has_weird_caps = False
                    if len(word) > 1:
                        # Check for capital letters after the first character (excluding after apostrophes at start)
                        for j, char in enumerate(word[1:], 1):
                            if char.isupper() and (j == 1 or word[j-1] not in ["'", "'"]):
                                has_weird_caps = True
                                break

                    # Fix the word
                    if word.isupper() and len(word) > 1:
                        # ALL CAPS word → Capitalize
                        word = word.capitalize()
                    elif has_weird_caps:
                        # Weird caps in middle → Convert to lowercase, then capitalize first letter
                        word = word.lower()
                        word = word[0].upper() + word[1:] if len(word) > 1 else word.upper()
                    elif i == 0:
                        # First word → Ensure starts with capital
                        word = word[0].upper() + word[1:] if len(word) > 1 else word.upper()

                    fixed_words.append(word)

                normalized.append(' '.join(fixed_words))

        return '. '.join(normalized)

    def get_quote(self):
        """Fetch quote from API with fallback, filtering for motivational content"""
        max_attempts = 5  # Try up to 5 times to get a motivational quote

        for attempt in range(max_attempts):
            try:
                response = requests.get(CONFIG["api_url"], timeout=CONFIG["api_timeout"])
                if response.status_code == 200:
                    data = response.json()
                    quote_text = data.get("quote", "")

                    # Check if quote is motivational/inspirational
                    if self.is_motivational(quote_text):
                        # Normalize the text to fix capitalization issues
                        normalized_text = self.normalize_text(quote_text)
                        return {
                            "text": normalized_text,
                            "author": data.get("author", "Unknown")
                        }
                    # If not motivational, try again
                    continue

            except Exception as e:
                print(f"API fetch attempt {attempt + 1} failed: {e}")
                break

        # Fallback to curated motivational quotes
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

        # Top accent bar (gradient blue)
        top_bar = tk.Frame(main_frame, bg='#667eea', height=4)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        # Content frame with padding
        content_frame = tk.Frame(main_frame, bg='#e8eaed')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=CONFIG["window_padding"], pady=CONFIG["window_padding"])

        # Close button (top-right, subtle)
        close_btn = tk.Button(
            content_frame,
            text='×',
            font=('Segoe UI', 16, 'normal'),
            fg='#888',
            bg='#e8eaed',
            bd=0,
            cursor='hand2',
            command=self.close_quote,
            activebackground='#d8dadd',
            activeforeground='#333',
            padx=6,
            pady=2
        )
        close_btn.place(relx=1.0, rely=0.0, anchor='ne', x=0, y=0)

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
        self.quote_label.pack(pady=(6, 10), anchor='w')

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

        # Progress bar (thinner, more subtle)
        self.progress_frame = tk.Frame(content_frame, bg='#c0c0c0', height=2)
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(6, 0))

        self.progress_bar = tk.Frame(self.progress_frame, bg='#667eea', height=2)
        self.progress_bar.place(relwidth=1.0, relheight=1.0)

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
