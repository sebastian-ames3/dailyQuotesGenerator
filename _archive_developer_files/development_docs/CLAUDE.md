# Claude Development Guide

This document tracks development history, architectural decisions, and key lessons learned for the Morning Motivation Quote Generator.

## ⚠️ CRITICAL USER REQUIREMENTS - READ THIS FIRST

### PRIMARY PRODUCT: Python Frameless Overlay ONLY

**WHAT THE USER WANTS:**
- **Frameless desktop overlay window** using Python + Tkinter (`quote_overlay.py`)
- Window appears upon Windows sign-in via LaunchQuote.bat
- **NO browser windows EVER** - must NEVER open in Brave, Edge, Chrome, or any browser
- Native-looking desktop notification experience
- Single file to maintain: `quote_overlay.py`

**WHAT THE USER DOES NOT WANT:**
- Browser-based interface (not even in "app mode")
- Multiple versions to maintain (HTML + Python)
- Visible browser UI, tabs, or processes
- `index.html` in production repository

### Development Approach

**Single Source of Truth: `quote_overlay.py`**
- ALL features must be implemented in Python + Tkinter
- Use `index.html` temporarily as reference during development ONLY
- Delete all HTML files when Python features are complete
- Test by running: `python quote_overlay.py`

**Why This Matters:**
- User runs LaunchQuote.bat daily on startup
- LaunchQuote.bat executes `quote_overlay.py` (not browser)
- Previous development focused on HTML, but user never sees it

---

## Development History

### V1.0.0 - Initial Release (2025-11-12)
- HTML/CSS/JavaScript single-file application
- DummyJSON API integration with fallback quotes
- 15-second auto-close timer with hover-to-pause
- Click-to-search functionality
- Python frameless overlay alternative (quote_overlay.py)
- Windows auto-launch batch file (LaunchQuote.bat)

### V2.0.0 - Feature Expansion (2025-11-13)

**Critical Bug Fixes:**
- Regex-based sentence splitting: `/(?<=[.!?…])\s+(?=["""''(\[]?\w)/u`
- Interior uppercase detection: `/(?<!^)(?<![''])[A-Z]/gu`
- Word-boundary regex for motivation filtering
- Fixed text normalization mangling quotes with varied punctuation

**New Features:**
- **Dark/Light Mode:** CSS custom properties, system preference detection, localStorage persistence
- **Settings Panel:** Timer duration (5-60s), position (4 corners), font size, real-time preview
- **Quote Categories:** 4 pre-defined categories with keyword matching, API retry logic
- **Configuration Files:** `quotes_config.json`, `user_settings.json`

### V2.0.1 - Critical Layout Fixes (2025-11-13)

**Issue:** Settings/theme/close buttons not visible, quotes overlapping buttons

**Root Causes:**
1. Animation transforms (`translateX(450px)`) left in positioning function → container pushed off-screen
2. `overflow-y: auto` on container clipped absolutely positioned buttons
3. No padding reserved for fixed-position buttons

**Fixes:**
- Removed transform from `applyPosition()` (only set top/bottom/left/right)
- Moved overflow from container to quote-content wrapper
- Added `padding-top: 56px` for button space, `z-index: 10` for button layering

**Key Lesson:** Browser caching and visual bugs require screenshot verification via Playwright, not just code review.

### V3.0.0 - Responsive Quote Box + Settings Modal (2025-11-14)

**Phase 1: Responsive Quote Box**
- Changed `width: 500px` → `width: fit-content`
- Constraints: `min-width: 320px`, `max-width: min(800px, 90vw)`
- Dynamically adapts from 320px (short quotes) to 800px (long quotes)

**Phase 2: Settings Modal**
- Changed settings panel from slide-in to centered modal (replaces quote box entirely)
- Fixed ARIA accessibility bug: moved settings panel outside quote-container (sibling, not child)
- Browser blocked focus on elements inside `aria-hidden="true"` containers
- Fixed timer variable naming issues

**Key Lesson:** Interactive elements must be siblings of containers that get `aria-hidden`, not children.

### V4.0.0 - Python Overlay Feature Parity (2025-11-14)

**Critical Discovery:** User uses `quote_overlay.py` via LaunchQuote.bat, not HTML version. All V2/V3 features existed only in HTML.

**Implementation (All 4 Phases Completed):**

1. **Settings Infrastructure:** `user_settings.json` persistence, settings window (Toplevel) with all controls
2. **Dark/Light Theme:** Theme toggle, THEMES dictionary, `apply_theme()` with widget tracking
3. **Responsive Window Sizing:** `calculate_window_width()` using font metrics (min 320px, max 800px)
4. **Enhanced Category System:** 4 categories with comprehensive keywords, word-boundary regex, API retry logic

**Technical Achievements:**
- Single-file architecture maintained
- JSON file-based settings (replaces localStorage)
- Full Tkinter theme system with widget reference tracking
- Dynamic window sizing with font metrics

### V4.0.1 - Button Visibility Fix (2025-11-14)

**Issue:** Emoji buttons (⚙️, 🌙) didn't render on Windows/Tkinter

**Root Cause:** Windows console can't encode emoji, Tkinter has poor emoji font support

**Solution:**
- Replaced emoji with text buttons: "Settings", "Dark"/"Light", ×
- Purple pill buttons with red hover for close
- Dedicated button_frame (30px) positioned above content_frame

### V5.0.0 - Advanced Visual Design (2025-11-14)

**User Selected:** Monochrome Modern color scheme (#4), diagonal gradients, fast animations

**Implemented:**
- **Pillow Integration:** Added PIL dependency with graceful fallback
- **Monochrome Modern Colors:** Light (#ffffff → #f5f5f5), Dark (#0a0a0a → #1a1a1a), ultra-clean Apple-esque aesthetic
- **Diagonal Gradient:** Optimized `create_diagonal_gradient()` (~30-40ms startup)
- **Snappier Animations:** Fade in ~120ms (was ~384ms), fade out ~72ms (was ~960ms)
- Icon button infrastructure created (not yet applied to UI)

**Deferred:** Rounded corners, drop shadows (complex on Windows/Tkinter, not worth technical debt)

**Performance:** <1s startup, <100MB memory, 60+ FPS animations, no regressions

### V5.0.1 - Text Normalization Fix (2025-11-14)

**Issue:** Quotes displayed with inconsistent capitalization: "It'S", random ALL CAPS, "Hello World" instead of "Hello world"

**Root Causes:**
1. Capitals after apostrophes not lowercased ("It'S" → "It's")
2. ALL CAPS detection didn't account for apostrophes
3. Function capitalized every word instead of only first word

**Solution - Complete Rewrite:**
- **Step 1:** Detect ALL CAPS (check alphabetic chars only), lowercase entire word
- **Step 2:** Fix interior capitals character-by-character, check for apostrophes
- **Step 3:** Capitalize first word of sentence ONLY
- **Fixed SENTENCE_SPLIT regex:** `r'(?<=[.!?…])\s+(?=["\'""''(\[]?\w)'` with `re.UNICODE`

**Testing:** 10/10 test cases passing, including edge cases like "WHO'S THERE? IT'S ME!"

---

## Architectural Decisions

### Single-File Architecture
- **Python:** `quote_overlay.py` (single source of truth)
- **Benefits:** Easy distribution, no build process, portable, fast load
- **Settings:** JSON file (`user_settings.json`) instead of localStorage

### Theme System
- THEMES dictionary with complete color schemes for light/dark
- Widget reference tracking (`self.widgets{}`) for dynamic theming
- Theme preference persisted in user_settings.json

### Text Processing
- Regex-based sentence splitting and normalization
- Word-boundary matching for category filtering
- Unicode-aware patterns for apostrophes and quotes

### No Database Required
**User Directive:** "i dont want to track anything. even a local db isnt required"
- Single quote per session, no history
- User preferences in JSON file only
- Privacy-first approach

---

## Key Lessons Learned

### 1. Visual Bugs Need Screenshot Verification
- Playwright screenshot comparison catches viewport clipping invisible in code review
- Browser caching makes manual testing unreliable
- Use local HTTP server + cache-busting query parameters

### 2. ARIA Accessibility Can Cause Cascading Failures
- Settings panel nested inside `aria-hidden` container broke focus management
- Browser blocked focus on descendants, causing silent failures
- **Solution:** Interactive elements must be siblings of `aria-hidden` containers

### 3. Animation Transforms vs Static Positioning Don't Mix
- Transforms meant for animation left in positioning logic push elements off-screen
- Separate animation CSS from positioning completely

### 4. Regex Patterns Over String Operations
- User-provided regex patterns: 100% reliability vs ~80% with string splitting
- Handles edge cases (curly quotes, ellipses, varied punctuation)
- Self-documenting with Unicode support

### 5. Overflow Placement Matters
- `overflow-y: auto` on containers clips absolutely positioned children
- Move overflow to content wrapper only, not outer containers

---

## Development Workflow

### Commit Strategy
**User Preference:** "add features incrementally using PRDs and tasks. commit/merge them often"

**Benefits:**
- Easy to bisect regressions
- Clear changelog history
- Can cherry-pick individual features

### When to Use Sub-Agents
- **Playwright Testing:** Visual regression, screenshot comparison, automated UI verification
- **Research Phase:** API evaluation, UX best practices, design alternatives
- **Code Review:** Accessibility audit, performance optimization, security scanning

---

Last Updated: 2025-11-14 (V5.0.1 Complete)
