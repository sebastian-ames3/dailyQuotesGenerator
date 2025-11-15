# PRD: Code Cleanup & Production Readiness

**Version:** 1.0.0
**Status:** Draft
**Created:** 2025-11-15
**Owner:** Production Readiness Initiative

## Executive Summary

Polish `quote_overlay.py` to production quality by removing debug code, improving documentation, ensuring code consistency, and optimizing for end-user experience. Transform developer code into maintainable, professional, public-facing software.

## Goals

1. **Code Quality:** Remove all debug code, TODOs, and development artifacts
2. **Documentation:** Ensure all functions have clear docstrings and comments
3. **Consistency:** Apply uniform code style and naming conventions
4. **Performance:** Optimize any inefficient code paths
5. **User Experience:** Improve error messages and user-facing text
6. **Maintainability:** Make code easy for future contributors to understand

## Code Quality Checklist

### 1. Dead Code Removal

#### 1.1 Unused Functions
**Task:** Search for functions that are defined but never called

**Method:**
```bash
# Search for function definitions
grep -n "def " quote_overlay.py

# For each function, verify it's called somewhere
```

**Known Candidates:**
- `create_icon_button()` - Lines 215-328 - **NEVER USED**
  - Created infrastructure for icon buttons
  - Never applied to UI (kept text buttons)
  - Status: REMOVE or mark as "Future Enhancement"

**Action Items:**
- [ ] Review create_icon_button() - Remove or move to archive
- [ ] Search for other unused functions
- [ ] Document decision (keep vs remove)

#### 1.2 Commented Code
**Task:** Search for commented-out code blocks

**Method:**
```python
# Look for patterns like:
# OLD_CODE = "something"
# if old_condition:
#     old_logic()
```

**Known Locations:**
- None found in current review

**Action Items:**
- [ ] Search for `#` comments with code
- [ ] Remove commented debug code
- [ ] Keep comments that explain why (not what)

#### 1.3 Unused Imports
**Task:** Verify all imports are used

**Current Imports:**
```python
import tkinter as tk
from tkinter import font, ttk
import requests
import random
import sys
import json
import os
from urllib.parse import quote as url_quote
from PIL import Image, ImageDraw, ImageFilter, ImageTk  # Conditional
```

**Verification:**
- `tkinter` - ✅ Used extensively
- `font, ttk` - ✅ Used for widgets
- `requests` - ✅ Used for API calls
- `random` - ✅ Used for fallback quotes
- `sys` - ✅ Used for exit codes
- `json` - ✅ Used for settings
- `os` - ✅ Used for file paths
- `url_quote` - ✅ Used for search
- `PIL.Image` - ✅ Used for gradients
- `PIL.ImageDraw` - ✅ Used in create_icon_button() - **UNUSED IF FUNCTION REMOVED**
- `PIL.ImageFilter` - ❌ **UNUSED** - imported but never used

**Action Items:**
- [ ] Remove `ImageFilter` from imports (not used)
- [ ] If create_icon_button() removed, also remove `ImageDraw`

#### 1.4 Unused Constants
**Task:** Verify all constants are used

**Defined Constants:**
```python
FALLBACK_QUOTES - ✅ Used
CATEGORY_KEYWORDS - ✅ Used
THEMES - ✅ Used
CONFIG - ✅ Used
SETTINGS_FILE - ✅ Used
```

**Action Items:**
- [ ] All constants confirmed in use
- [ ] No cleanup needed

### 2. Debug Code Removal

#### 2.1 Print Statements
**Task:** Review all print() statements - remove debug prints, keep error messages

**Current Print Statements:**
```python
Line 22: print("Warning: Pillow not installed. Advanced visual effects disabled.")
Line 388: print(f"Error loading settings: {e}")
Line 398: print(f"Error saving settings: {e}")
Line 702: print(f"API fetch attempt {attempt + 1} failed: {e}")
```

**Analysis:**
- Line 22: ✅ **KEEP** - Useful warning for users
- Line 388: ⚠️ **REVIEW** - Should log instead of print?
- Line 398: ⚠️ **REVIEW** - Should log instead of print?
- Line 702: ⚠️ **DEBUG INFO** - User doesn't need to know attempt numbers

**Action Items:**
- [ ] Decide on logging strategy (print vs logging module vs silent)
- [ ] Remove or improve "API fetch attempt" message
- [ ] Consider adding --quiet flag for no output
- [ ] Document output behavior in README

#### 2.2 Developer Comments
**Task:** Remove comments like "# TODO", "# FIXME", "# HACK"

**Method:**
```bash
grep -n "TODO\|FIXME\|HACK\|XXX\|TEMP" quote_overlay.py
```

**Known Locations:**
- None found in initial review

**Action Items:**
- [ ] Run grep search
- [ ] Remove or resolve all TODOs
- [ ] Convert FIXMEs to GitHub issues if needed

### 3. Documentation Quality

#### 3.1 Module Docstring
**Current (Lines 1-5):**
```python
#!/usr/bin/env python3
"""
Morning Motivation Quote Generator - Frameless Overlay
A true frameless desktop overlay window that displays motivational quotes.
"""
```

**Improvement Needed:**
```python
#!/usr/bin/env python3
"""
Morning Motivation Quote Generator - Frameless Overlay

A lightweight desktop overlay that displays motivational quotes from DummyJSON API
with offline fallback support. Features include customizable themes, positions,
categories, and auto-close timer with hover-to-pause functionality.

Author: Sebastian Ames
License: MIT
Version: 5.0.1
Python: 3.7+

Usage:
    python quote_overlay.py [--debug]

Dependencies:
    - requests>=2.31.0
    - Pillow>=10.0.0 (optional, for advanced visual effects)

For setup and installation, see README.md
"""
```

**Action Items:**
- [ ] Enhance module docstring with version, author, usage
- [ ] Add brief feature summary
- [ ] Document command-line arguments
- [ ] Link to README for full docs

#### 3.2 Function Docstrings
**Task:** Ensure all functions have proper docstrings

**Docstring Standard:**
```python
def function_name(param1, param2):
    """
    Brief one-line description.

    Detailed explanation if needed. Explain the why, not the what.

    Args:
        param1 (type): Description
        param2 (type): Description

    Returns:
        type: Description

    Raises:
        ExceptionType: When this happens

    Example:
        >>> function_name("value1", "value2")
        expected_output
    """
```

**Functions Needing Docstring Review:**

**EXCELLENT** (Keep as-is):
- `create_diagonal_gradient()` - Lines 161-213 - ✅ Comprehensive docstring
- `create_icon_button()` - Lines 215-328 - ✅ Good docstring (if keeping function)
- `normalize_text()` - Lines 603-676 - ✅ Detailed docstring with examples

**GOOD** (Minor improvements):
- `load_settings()` - Lines 371-390 - Has docstring, could add Args/Returns
- `save_settings()` - Lines 392-398 - Has docstring, could add Raises
- `get_quote()` - Lines 678-706 - Has docstring, could explain retry logic
- `search_quote()` - Lines 944-948 - Has docstring, could add Args

**MISSING** (Add docstrings):
- `__init__()` - Lines 331-369 - ❌ No docstring
- `calculate_window_width()` - Lines 400-414 - ❌ No docstring
- `apply_position()` - Lines 416-442 - ❌ No docstring
- `apply_font_size()` - Lines 444-454 - ❌ No docstring
- `apply_theme()` - Lines 456-528 - ❌ No docstring
- `toggle_theme()` - Lines 530-536 - ❌ No docstring
- `setup_window()` - Lines 538-560 - ❌ No docstring
- `fade_in()` - Lines 562-570 - ❌ No docstring
- `fade_out()` - Lines 572-583 - ❌ No docstring
- `matches_category()` - Lines 585-601 - ❌ No docstring
- `get_fallback_quote()` - Lines 708-720 - ❌ No docstring
- `create_widgets()` - Lines 722-895 - ❌ No docstring
- `start_timer()` - Lines 897-902 - ❌ No docstring
- `update_progress()` - Lines 904-919 - ❌ No docstring
- `pause_timer()` - Lines 921-928 - ❌ No docstring
- `resume_timer()` - Lines 930-936 - ❌ No docstring
- `close_quote()` - Lines 938-942 - ❌ No docstring
- `show_settings()` - Lines 950-1131 - ❌ No docstring
- `on_timer_change()` - Lines 1133-1138 - ❌ No docstring
- `on_position_change()` - Lines 1140-1148 - ❌ No docstring
- `on_font_size_change()` - Lines 1150-1155 - ❌ No docstring
- `on_category_change()` - Lines 1157-1164 - ❌ No docstring
- `close_settings()` - Lines 1166-1172 - ❌ No docstring
- `run()` - Lines 1174-1176 - ❌ No docstring

**Action Items:**
- [ ] Add docstrings to all public methods
- [ ] Include Args, Returns, Raises where applicable
- [ ] Use consistent docstring format (Google style recommended)
- [ ] Private methods (_method_name) can have simpler docstrings

#### 3.3 Inline Comments
**Task:** Review inline comments for clarity and necessity

**Guidelines:**
- Comments should explain **WHY**, not **WHAT**
- Remove obvious comments like `# Increment counter`
- Keep complex logic explanations
- Explain any non-obvious decisions

**Good Examples (Keep):**
```python
# Line 158: SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.json')
# Good! Path is in same directory as script

# Line 552: self.root.attributes('-alpha', 0.96)  # Slight transparency for elegance
# Good! Explains the design choice
```

**Action Items:**
- [ ] Review all inline comments
- [ ] Remove redundant comments
- [ ] Add comments for complex algorithms
- [ ] Explain magic numbers with comments

### 4. Code Style & Consistency

#### 4.1 Naming Conventions
**Task:** Ensure PEP 8 naming compliance

**PEP 8 Rules:**
- `ClassName` - PascalCase for classes
- `function_name` - snake_case for functions
- `CONSTANT_NAME` - SCREAMING_SNAKE_CASE for constants
- `variable_name` - snake_case for variables
- `_private_method` - leading underscore for internal methods

**Current Compliance:**
- `QuoteOverlay` - ✅ Class name correct
- All functions - ✅ snake_case
- All constants - ✅ SCREAMING_SNAKE_CASE
- All variables - ✅ snake_case

**Action Items:**
- [ ] Run PEP 8 checker: `pip install pycodestyle && pycodestyle quote_overlay.py`
- [ ] Fix any naming violations
- [ ] Verify consistency

#### 4.2 Line Length & Formatting
**Task:** Ensure lines are ≤ 79 characters (PEP 8) or ≤ 100 (relaxed)

**Method:**
```bash
# Find long lines
awk 'length($0) > 100 {print NR": "length($0)" chars"}' quote_overlay.py
```

**Known Long Lines:**
- Line 846: `wraplength=CONFIG["window_width"] - CONFIG["window_padding"] * 2 - 30,`

**Action Items:**
- [ ] Find all lines > 100 characters
- [ ] Break into multiple lines with proper indentation
- [ ] Use parentheses for implicit line continuation
- [ ] Ensure readability

#### 4.3 Import Organization
**Task:** Organize imports per PEP 8

**PEP 8 Import Order:**
1. Standard library imports
2. Related third-party imports
3. Local application imports

**Current (Lines 7-18):**
```python
import tkinter as tk
from tkinter import font, ttk
import requests
import random
import sys
import json
import os
from urllib.parse import quote as url_quote

# PIL for advanced visual effects (V5.0.0+)
try:
    from PIL import Image, ImageDraw, ImageFilter, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Advanced visual effects disabled.")
```

**Improved:**
```python
# Standard library imports
import json
import os
import random
import sys
import tkinter as tk
from tkinter import font, ttk
from urllib.parse import quote as url_quote

# Third-party imports
import requests

# Optional third-party imports
try:
    from PIL import Image, ImageDraw, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Advanced visual effects disabled.")
```

**Action Items:**
- [ ] Reorder imports (standard → third-party → local)
- [ ] Alphabetize within each group
- [ ] Remove unused `ImageFilter` import
- [ ] Add blank lines between groups

#### 4.4 Whitespace & Blank Lines
**Task:** Ensure proper spacing per PEP 8

**PEP 8 Rules:**
- 2 blank lines before top-level class/function definitions
- 1 blank line before method definitions
- Use blank lines sparingly inside functions to show logical sections

**Action Items:**
- [ ] Verify 2 blank lines before `class QuoteOverlay:`
- [ ] Verify 2 blank lines before standalone functions
- [ ] Check method spacing
- [ ] Remove excessive blank lines

### 5. Performance Optimization

#### 5.1 Gradient Caching
**Current Implementation (Lines 727-746):**
```python
gradient_img = create_diagonal_gradient(
    window_width, window_height,
    colors['bg'], colors['bg_gradient']
)

if gradient_img:
    self.gradient_photo = ImageTk.PhotoImage(gradient_img)
```

**Issue:** Gradient regenerated on every theme change

**Optimization:**
```python
# Cache gradients per theme
self.gradient_cache = {}

def get_or_create_gradient(self, width, height, theme):
    """Get cached gradient or create new one"""
    cache_key = f"{width}x{height}_{theme}"
    if cache_key not in self.gradient_cache:
        colors = THEMES[theme]
        gradient_img = create_diagonal_gradient(
            width, height,
            colors['bg'], colors['bg_gradient']
        )
        if gradient_img:
            self.gradient_cache[cache_key] = ImageTk.PhotoImage(gradient_img)
    return self.gradient_cache.get(cache_key)
```

**Action Items:**
- [ ] Implement gradient caching
- [ ] Clear cache if memory usage becomes issue
- [ ] Measure memory impact

#### 5.2 Import Optimization
**Current (Line 899, 909, 926, 933):**
```python
import time  # Imported 4 times in different methods!
```

**Issue:** Importing time module multiple times unnecessarily

**Fix:** Add `import time` to top-level imports

**Action Items:**
- [ ] Move `import time` to module imports
- [ ] Move `import re` to module imports (used in normalize_text and matches_category)
- [ ] Move `import webbrowser` to module imports
- [ ] Move `import math` to module imports (used in create_icon_button)
- [ ] Remove all inline imports

#### 5.3 Regex Compilation
**Current (Line 619):**
```python
SENTENCE_SPLIT = re.compile(
    r'(?<=[.!?…])\s+(?=["\'""''(\[]?\w)',
    re.UNICODE
)
```

**Issue:** Regex compiled inside `normalize_text()` function on every call

**Fix:** Move to module-level constant

**Action Items:**
- [ ] Move SENTENCE_SPLIT regex to module constants
- [ ] Move any other regex patterns to constants
- [ ] Pre-compile all regex patterns

### 6. Error Handling Improvements

#### 6.1 Specific Exception Handling
**Current Pattern:**
```python
except Exception as e:
```

**Issue:** Catching all exceptions is too broad

**Improved:**
```python
except (json.JSONDecodeError, IOError) as e:
    print(f"Error loading settings: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise  # Re-raise unexpected errors
```

**Action Items:**
- [ ] Review all try/except blocks
- [ ] Use specific exception types
- [ ] Keep broad `Exception` as last resort
- [ ] Re-raise unexpected errors for debugging

#### 6.2 Graceful Degradation Messages
**Task:** Improve user-facing error messages

**Current:**
```python
print(f"Error loading settings: {e}")  # Technical message
```

**Improved:**
```python
print("Settings file could not be loaded. Using default settings.")
if DEBUG_MODE:
    print(f"Technical details: {e}")
```

**Action Items:**
- [ ] Separate user messages from debug messages
- [ ] Make user messages friendly and actionable
- [ ] Add debug flag for technical details
- [ ] Consider using logging module

### 7. User-Facing Text

#### 7.1 UI Text Quality
**Task:** Review all user-visible strings

**Current UI Text:**
- Line 872: `'Click quote to learn more'` - ✅ Good
- Line 984: `"Settings"` - ✅ Good
- Line 996: `"Timer Duration: {value}s"` - ✅ Good
- Line 1024: `"Position:"` - ✅ Good
- Line 1060: `"Font Size:"` - ✅ Good
- Line 1085: `"Quote Category:"` - ✅ Good
- Line 1119: `"Close"` - ✅ Good

**Action Items:**
- [ ] Review all UI strings for clarity
- [ ] Ensure consistent capitalization
- [ ] Check for typos
- [ ] Consider internationalization (i18n) hooks for future

#### 7.2 Console Output
**Task:** Make console output professional

**Current:**
- `"Warning: Pillow not installed. Advanced visual effects disabled."` - ✅ Good
- `"Error loading settings: {e}"` - ⚠️ Could be more user-friendly
- `"Error saving settings: {e}"` - ⚠️ Could be more user-friendly
- `"API fetch attempt {attempt + 1} failed: {e}"` - ❌ Too technical

**Improved:**
```python
# Pillow warning - keep as-is
print("Notice: Pillow library not installed. Using basic visuals.")

# Settings errors - simplify
print("Unable to load saved settings. Using defaults.")

# API errors - remove or make optional
if DEBUG_MODE:
    print(f"API fetch attempt {attempt + 1} failed: {e}")
```

**Action Items:**
- [ ] Review all print statements
- [ ] Make messages user-friendly
- [ ] Hide technical details unless debug mode
- [ ] Consider adding --quiet flag

### 8. Production Readiness Checklist

#### 8.1 Version Information
**Task:** Add version tracking

**Current:** No version info in code

**Add:**
```python
__version__ = "5.0.1"
__author__ = "Sebastian Ames"
__license__ = "MIT"
```

**Action Items:**
- [ ] Add version constants
- [ ] Add --version flag
- [ ] Update version in module docstring
- [ ] Sync with CHANGELOG.md

#### 8.2 Command-Line Arguments
**Task:** Add professional CLI interface

**Current:** No argument parsing

**Add:**
```python
import argparse

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Morning Motivation Quote Generator - Frameless Overlay"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug output'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress all console output'
    )
    return parser.parse_args()

# In main:
if __name__ == "__main__":
    args = parse_args()
    DEBUG_MODE = args.debug
    QUIET_MODE = args.quiet
    # ...
```

**Action Items:**
- [ ] Add argparse for CLI arguments
- [ ] Support --version
- [ ] Support --debug
- [ ] Support --quiet
- [ ] Update documentation

#### 8.3 Exit Codes
**Task:** Use proper exit codes

**Current (Lines 1179-1187):**
```python
if __name__ == "__main__":
    try:
        app = QuoteOverlay()
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
```

**Status:** ✅ Already correct!
- Exit 0 on success/Ctrl+C
- Exit 1 on error

**Action Items:**
- [ ] Verify exit code behavior
- [ ] Document exit codes in README
- [ ] Add specific exit codes for different error types (optional)

### 9. Code Organization

#### 9.1 Logical Grouping
**Task:** Organize code into logical sections with comments

**Suggested Structure:**
```python
#!/usr/bin/env python3
"""Module docstring"""

# ============================================================================
# IMPORTS
# ============================================================================
# Standard library
...

# Third-party
...

# ============================================================================
# CONSTANTS
# ============================================================================
__version__ = "5.0.1"
...

FALLBACK_QUOTES = [...]
CATEGORY_KEYWORDS = {...}
THEMES = {...}
CONFIG = {...}
SETTINGS_FILE = ...

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def create_diagonal_gradient(...):
    ...

def create_icon_button(...):
    ...

# ============================================================================
# MAIN APPLICATION CLASS
# ============================================================================
class QuoteOverlay:
    ...

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    ...
```

**Action Items:**
- [ ] Add section divider comments
- [ ] Group related functions
- [ ] Ensure logical flow
- [ ] Make code scannable

#### 9.2 Class Method Ordering
**Task:** Order methods logically

**Recommended Order:**
1. `__init__()` - Constructor
2. Public methods (alphabetically or by feature area)
3. Event handlers (on_*  methods)
4. Private methods (_method_name)

**Current Order:** Already mostly good, minor tweaks needed

**Action Items:**
- [ ] Review method order
- [ ] Group related methods (e.g., timer methods together)
- [ ] Consider extracting settings methods to separate class (optional, may be overkill)

### 10. Final Polish

#### 10.1 Magic Numbers
**Task:** Replace magic numbers with named constants

**Examples:**
```python
# Line 552: self.root.attributes('-alpha', 0.96)
# Should be:
WINDOW_OPACITY = 0.96
self.root.attributes('-alpha', WINDOW_OPACITY)

# Line 565: alpha += 0.12
# Should be:
FADE_IN_STEP = 0.12
alpha += FADE_IN_STEP

# Line 576: new_alpha = current_alpha - 0.16
# Should be:
FADE_OUT_STEP = 0.16
new_alpha = current_alpha - FADE_OUT_STEP
```

**Action Items:**
- [ ] Find all magic numbers
- [ ] Create named constants
- [ ] Add comments explaining values
- [ ] Update CONFIG dict if appropriate

#### 10.2 String Literals
**Task:** Extract repeated strings to constants

**Examples:**
```python
# 'Segoe UI' appears 10+ times
# Should be:
UI_FONT_FAMILY = 'Segoe UI'

# 'window_bg' appears many times
# Could remain as-is (dictionary key) or extract
```

**Action Items:**
- [ ] Identify frequently repeated strings
- [ ] Extract to constants where appropriate
- [ ] Don't over-extract (readability vs DRY balance)

#### 10.3 Code Comments Review
**Task:** Final review of all comments

**Quality Criteria:**
- Comments are accurate (not outdated)
- Comments explain WHY, not WHAT
- Comments are grammatically correct
- Comments use proper capitalization and punctuation
- No dead commented code

**Action Items:**
- [ ] Read every comment
- [ ] Update outdated comments
- [ ] Fix grammar/spelling
- [ ] Remove dead code comments

## Success Criteria

### Code Quality
- [ ] No dead/unused code
- [ ] No debug print statements (except with --debug flag)
- [ ] All functions have docstrings
- [ ] All complex logic has explanatory comments
- [ ] No TODO/FIXME comments

### Code Style
- [ ] Passes PEP 8 check (pycodestyle)
- [ ] Consistent naming conventions
- [ ] Proper import organization
- [ ] Appropriate line lengths (≤100 chars)
- [ ] Proper whitespace and blank lines

### Performance
- [ ] No unnecessary recomputation (caching where appropriate)
- [ ] No repeated imports inside functions
- [ ] Regex patterns pre-compiled
- [ ] Memory usage reasonable (<100MB)

### User Experience
- [ ] Professional console output
- [ ] User-friendly error messages
- [ ] Clean UI text
- [ ] Proper exit codes
- [ ] Command-line arguments work

### Documentation
- [ ] Module docstring comprehensive
- [ ] All public methods documented
- [ ] Inline comments explain complex logic
- [ ] README updated if needed
- [ ] Version information present

### Production Readiness
- [ ] No development artifacts
- [ ] Professional code organization
- [ ] Consistent code style
- [ ] Optimized performance
- [ ] Ready for public GitHub

## Implementation Plan

### Phase 1: Cleanup (1 hour)
1. Remove dead code (create_icon_button if not needed)
2. Remove unused imports (ImageFilter, ImageDraw)
3. Remove debug print statements
4. Clean up comments (remove TODOs, fix outdated)
5. Fix import organization

### Phase 2: Documentation (1.5 hours)
1. Enhance module docstring
2. Add docstrings to all methods (~25 methods)
3. Review and improve inline comments
4. Add section divider comments
5. Document magic numbers

### Phase 3: Optimization (30 minutes)
1. Move imports to module level
2. Pre-compile regex patterns
3. Implement gradient caching
4. Test performance improvements

### Phase 4: Polish (1 hour)
1. Add version constants
2. Implement argument parsing
3. Extract magic numbers to constants
4. Improve error messages
5. Run PEP 8 checker and fix issues
6. Final code review

### Phase 5: Verification (30 minutes)
1. Test all features still work
2. Verify exit codes
3. Test command-line arguments
4. Check memory usage
5. Final git status review

**Total Estimated Time:** 4.5 hours

## Tools & Commands

### Code Quality Tools
```bash
# PEP 8 checker
pip install pycodestyle
pycodestyle quote_overlay.py

# More comprehensive linting
pip install pylint
pylint quote_overlay.py

# Code formatting
pip install black
black --check quote_overlay.py  # Check only
black quote_overlay.py          # Auto-format

# Import sorting
pip install isort
isort --check quote_overlay.py  # Check only
isort quote_overlay.py          # Auto-sort
```

### Code Analysis
```bash
# Find long lines
awk 'length($0) > 100 {print NR": "length($0)" chars"}' quote_overlay.py

# Count lines of code
cloc quote_overlay.py

# Find TODOs/FIXMEs
grep -n "TODO\|FIXME\|HACK\|XXX" quote_overlay.py

# Find print statements
grep -n "print(" quote_overlay.py

# Find functions without docstrings
grep -A1 "def " quote_overlay.py | grep -v '"""'
```

### Testing
```bash
# Run application
python quote_overlay.py

# Test with debug mode
python quote_overlay.py --debug

# Test with quiet mode
python quote_overlay.py --quiet

# Check exit code
python quote_overlay.py; echo $?  # Unix/Mac
python quote_overlay.py & echo %ERRORLEVEL%  # Windows CMD
```

## Deliverables

1. **Cleaned quote_overlay.py** - Production-ready code
2. **Updated requirements.txt** - If any changes needed
3. **Code Quality Report** - PEP 8 compliance, lint results
4. **Performance Benchmarks** - Before/after optimization metrics
5. **Updated Documentation** - README, docstrings, comments

## Next Steps

1. User reviews this PRD
2. Execute cleanup in phases (1-5)
3. Run all quality tools
4. Test thoroughly
5. Prepare for final commit
6. Ready for GitHub public release

## Appendix: Quick Wins

**Immediate improvements (< 30 minutes):**
1. Remove `ImageFilter` import
2. Move `import time`, `import re`, `import math`, `import webbrowser` to top
3. Add `__version__ = "5.0.1"`
4. Improve "API fetch attempt" print statement
5. Add basic module docstring enhancement
6. Fix import order (standard → third-party)

These can be done immediately while reviewing the full PRD.
