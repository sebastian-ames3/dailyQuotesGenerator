#!/usr/bin/env python3
"""
Quote Scheduler - Shows quotes based on time windows
Only shows a quote if logging in during/after designated time windows
"""

import json
import os
from datetime import datetime, time
from pathlib import Path

# Configuration
SCHEDULE_CONFIG = {
    "time_windows": [
        {"name": "morning", "trigger_time": "05:00", "window_hours": 6},  # 5am-11am
        {"name": "midday", "trigger_time": "12:00", "window_hours": 5},   # 12pm-5pm
    ]
}

TRACKER_FILE = Path(__file__).parent / ".quote_tracker.json"


def load_tracker():
    """Load the tracker file that records when quotes were last shown"""
    if TRACKER_FILE.exists():
        try:
            with open(TRACKER_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_tracker(tracker):
    """Save the tracker file"""
    with open(TRACKER_FILE, 'w') as f:
        json.dump(tracker, f, indent=2)


def is_in_time_window(window_config):
    """Check if current time is within the window"""
    now = datetime.now()
    current_time = now.time()

    # Parse trigger time
    trigger_hour, trigger_minute = map(int, window_config["trigger_time"].split(":"))
    trigger = time(trigger_hour, trigger_minute)

    # Calculate end of window
    window_hours = window_config["window_hours"]
    end_hour = (trigger_hour + window_hours) % 24
    end_time = time(end_hour, 0)

    # Check if current time is within window
    if trigger <= end_time:
        return trigger <= current_time < end_time
    else:  # Window crosses midnight
        return current_time >= trigger or current_time < end_time


def should_show_quote():
    """Determine if a quote should be shown based on schedule"""
    tracker = load_tracker()
    today = datetime.now().strftime("%Y-%m-%d")

    for window in SCHEDULE_CONFIG["time_windows"]:
        window_name = window["name"]

        # Check if we're in this time window
        if is_in_time_window(window):
            # Check if we've already shown a quote for this window today
            last_shown = tracker.get(window_name)

            if last_shown != today:
                # Show quote and mark as shown for today
                tracker[window_name] = today
                save_tracker(tracker)
                return True

    return False


if __name__ == "__main__":
    import sys
    import subprocess

    if should_show_quote():
        # Launch the quote overlay
        script_dir = Path(__file__).parent
        quote_script = script_dir / "quote_overlay.py"

        try:
            # Try to run the Python quote overlay
            subprocess.run([sys.executable, str(quote_script)], check=False)
        except Exception as e:
            print(f"Error launching quote: {e}")
            sys.exit(1)
    else:
        # Not in a time window or already shown today - exit silently
        sys.exit(0)
