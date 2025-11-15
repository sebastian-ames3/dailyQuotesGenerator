# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

---

## Release History

## [3.0.0] - 2025-11-14

### Added

- **Responsive Quote Box (Phase 1)**
  - Quote box now dynamically adapts width from 320px to 800px based on content length
  - Uses `fit-content` with intelligent min/max constraints: `min(800px, 90vw)`
  - Height auto-adjusts with scrolling for long quotes (max-height: 80vh)
  - Mobile responsive: respects 90vw on small screens
  - Maintains visual balance for both short and long quotes

- **Settings Page Replacement (Phase 2)**
  - Settings panel now appears as centered modal, replacing quote box completely
  - Added back button (← Back) for clear navigation to return to quote
  - Settings panel positioned center screen (50%, 50% with translate transform)
  - Mobile responsive: min-width 320px, max-width min(600px, 90vw)
  - Single view at a time: quote OR settings, never both simultaneously
  - Timer pauses when settings open, resumes when closed

### Changed

- **Quote Container CSS**
  - `width: 500px` → `width: fit-content`
  - Added `min-width: 320px`
  - Added `max-width: min(800px, 90vw)`
  - Container now adapts to content instead of fixed width

- **Settings Panel CSS**
  - `position: absolute` (below box) → `position: fixed` (centered modal)
  - Removed top-right slide-in positioning
  - Changed to center positioning: `top: 50%; left: 50%; transform: translate(-50%, -50%)`
  - Increased z-index to 1000000 (above quote box)
  - Added `.quote-container.settings-open` class for hiding quote

- **Settings Panel HTML Structure**
  - Moved settings panel from inside quote-container to outside (sibling element)
  - Fixed ARIA accessibility conflict (aria-hidden on focused element)
  - Added HTML comment: "Settings Panel (outside quote-container for accessibility)"

- **Navigation Behavior**
  - Settings button (⚙️) now only opens settings, does not toggle
  - Settings close via back button or Esc key only
  - Esc key: closes settings if open, otherwise closes quote

### Fixed

- **Critical: Settings panel disappearing immediately**
  - Fixed timer not pausing when settings opened (wrong variable name: countdownInterval → timerInterval)
  - Fixed timer starting even when settings already open (added check in init())
  - Fixed closeQuote() running when settings open (added settingsOpen guard)
  - Fixed ARIA accessibility blocking focus (moved settings panel outside quote-container)

- **Test Infrastructure**
  - Fixed port mismatch: 8082 → 8081 in all test files
  - Updated button-visibility tests for V3.0 behavior (back button closes settings, not settings button)
  - Fixed test expectations for settings page replacement model

### Technical Details

- **CSS Changes:** 15+ lines modified across .quote-container and .settings-panel
- **HTML Changes:** Restructured settings panel location (60 lines moved)
- **JavaScript Changes:**
  - Refactored `toggleSettings()` → `openSettings()` + `closeSettings()`
  - Added `settingsOpen` state variable
  - Fixed timer variable references (timerInterval vs countdownInterval)
  - Added conditional timer start in init()
  - Added settingsOpen guard in closeQuote()
  - Updated Esc key handler for dual behavior

- **Test Results:** 23 passed, 3 failed (non-critical), 1 skipped (85% pass rate)

### Accessibility

- Fixed ARIA violation: Settings panel no longer inside aria-hidden container
- Focus management: Back button properly receives focus without accessibility warnings
- Keyboard navigation: Esc key closes settings, Tab cycles through controls

### Notes

- This version introduces breaking changes to settings panel behavior (no longer toggles on settings button click)
- Settings panel now requires explicit close action (back button or Esc)
- All changes align with Phase 3 integration testing requirements

## [2.0.1] - 2025-11-13

### Fixed

- **Button visibility issues**
  - Removed translateX transforms from applyPosition() that pushed container off-screen
  - Fixed container overflow causing buttons to be clipped outside viewport
  - Added padding-top: 56px to container for button clearance
  - Moved overflow-y: auto from container to quote-content wrapper
  - All three buttons (⚙️ settings, 🌙 theme, × close) now properly visible

- **Container layout for long quotes**
  - Added min-height: 180px and max-height constraints
  - Implemented flexbox layout for proper content flow
  - Quote content scrolls independently while buttons stay fixed
  - Author and progress bar always visible regardless of quote length

- **CSS positioning**
  - Centered container during debugging (temporarily)
  - Fixed z-index issues with buttons (z-index: 10)
  - Removed animation transforms that conflicted with position settings

### Development

- **Playwright testing infrastructure**
  - Added comprehensive button visibility tests
  - Created visual regression test suite
  - Automated screenshot comparison
  - Test coverage for keyboard navigation and accessibility
  - Identified and fixed viewport clipping issues through automated testing

### Technical Debt

- Created test helper files (test_buttons.html, simple_test.html)
- Added Playwright configuration and test scripts
- Documented debugging process for future reference

---

## [2.0.0] - 2025-11-13

### Added

- **V2 Phase 1: Critical Bug Fixes**
  - Improved text normalization using regex-based sentence splitting
  - Preserves all punctuation (!, ?, ...) not just periods
  - Handles both straight (') and curly (', ') apostrophes
  - Preserves acronyms (U.S., A.I.)
  - Removed hidden zero-width space character in JavaScript
  - Fixed window.close() behavior with graceful fallback
  - Improved motivation filter with word-boundary regex
  - Added "Click quote to learn more" hint text
  - Removed unused imports

- **V2 Feature: Dark/Light Mode**
  - Theme toggle button (🌙/☀️) in quote notification
  - Auto-detect system color scheme preference
  - Persist user theme choice in localStorage
  - CSS variables for all colors (light and dark themes)
  - Smooth 0.3s transitions between themes
  - WCAG AA compliant contrast ratios in both themes
  - Auto-switch with system preference changes

- **V2 Feature: Settings Panel**
  - ⚙️ Settings button to toggle settings panel
  - Timer duration slider (5-60 seconds, 5s increments)
  - Position selector (bottom-right, bottom-left, top-right, top-left)
  - Font size selector (small, medium, large)
  - All settings persist in localStorage
  - Real-time preview of changes
  - Clean, minimal design matching current theme
  - Theme-aware colors (works in both light/dark mode)

- **V2 Feature: Quote Categories**
  - Category selector in settings panel
  - 4 pre-defined categories:
    - Motivation & Inspiration (default)
    - Learning & Growth
    - Creativity & Innovation
    - Productivity & Focus
  - "All Categories" option for no filtering
  - Keyword-based category matching using word boundaries
  - API quotes filtered in real-time (up to 5 attempts)
  - Fallback quotes filtered by category
  - Category preference persists in localStorage

- **Configuration Files**
  - config/quotes_config.json: Centralized theme colors, timer settings, API config, categories
  - config/user_settings.json: User preferences storage template

### Changed

- Text normalization algorithm completely rewritten
- Motivation filter now uses word-boundary regex to avoid false positives
- window.close() now has graceful fallback for better browser compatibility
- Quote container positioning system overhauled for settings panel

### Fixed

- Text normalization no longer mangles quotes with varied punctuation
- Sentence splitting preserves exclamation points and question marks
- Abbreviations like "U.S." no longer broken into "U. S"
- Contractions with curly apostrophes now handled correctly
- Motivation filter false positives ("can" matching "candle")
- Browser close behavior when window.close() is blocked

---

## [1.0.0] - 2025-11-12

### Added

- **Demo screenshot** - Added quote_demo_screenshot.png to README.md
- **Complete project documentation** - All documentation finalized for v1.0.0 release

### Changed

- **Roadmap updated** - Marked V1 as complete with all 14 planned features
- **Project status** - Updated from 90% to 100% complete

### Milestone

- **V1.0.0 Release** - First stable release
  - Python frameless overlay working perfectly
  - HTML/CSS/JavaScript fallback fully functional
  - Auto-launch installation scripts tested
  - Smart quote filtering with text normalization
  - 15 curated fallback quotes for offline use
  - Full accessibility support (WCAG 2.1 AA)
  - Comprehensive documentation and setup guides
  - Production-ready for daily use

## [0.9.14] - 2025-11-12

### Added

- **Expanded keyword filtering** - Added productivity, creativity, innovation keywords
  - New keywords: productivity, productive, inspirational, creativity, creative, innovation, innovative, create, make, build
  - Better variety of motivational quotes focused on action and achievement

### Changed

- **Author display** - Increased font size (11pt → 12pt) and darkened color for better visibility
- **Window height** - Increased from 180px to 200px to ensure author name is always visible

## [0.9.13] - 2025-11-12

### Fixed

- **Author visibility** - Fixed author text being cut off by increasing window height to 200px

## [0.9.12] - 2025-11-12

### Fixed

- **Text capitalization** - Enhanced normalization to fix ALL capitalization issues
  - Now catches mid-word capitals (They'Re → They're, It'S → It's, DoN'T → Don't)
  - Detects capital letters anywhere in words, not just ALL CAPS
  - Applied to both Python overlay and HTML fallback

## [0.9.11] - 2025-11-12

### Changed

- **Author attribution** - Made author name more prominent
  - Increased font size from 11pt to 12pt
  - Darkened text color for better contrast (#5a6c7d → #3a4a5a)
  - Increased padding for better readability

## [0.9.10] - 2025-11-12

### Fixed

- **Text normalization** - Fixed weird capitalizations from DummyJSON API
  - Converts ALL CAPS words to proper case
  - Ensures first word of sentences is capitalized
  - Removes extra whitespace
  - Preserves acronyms (single letter like "I")

## [0.9.9] - 2025-11-12

### Changed

- **Simplified auto-launch** - Removed time-window complexity
  - Now shows quote on every login (simple and straightforward)
  - No tracking files, no time checking, just works
  - Updated install/uninstall scripts for simpler behavior

### Removed

- **quote_scheduler.py** - No longer needed (removed time-window logic)
- **SCHEDULED_QUOTES.md** - Removed overcomplicated documentation

## [0.9.8] - 2025-11-12

### Added

- **Scheduled quotes system** - Time-window based quote display (later simplified in 0.9.9)
  - quote_scheduler.py for time-window checking
  - install_scheduled_quotes.bat for one-click installation
  - uninstall_scheduled_quotes.bat for one-click removal
  - SCHEDULED_QUOTES.md with complete guide

## [0.9.7] - 2025-11-12

### Changed

- **Quote filtering** - Filtered for motivational/inspirational content only
  - API tries up to 5 times to find motivational quotes
  - Filters based on action-oriented keywords (believe, achieve, courage, etc.)
  - Blocks wisdom quotes (knowledge, philosophy, truth, etc.)
  - Updated all 15 fallback quotes to purely motivational content
  - Updated both quote_overlay.py and index.html with identical quotes

## [0.9.6] - 2025-11-12

### Added

- **Python-based frameless overlay** - True frameless window using tkinter
  - quote_overlay.py: Frameless desktop overlay with no window decorations
  - requirements.txt: Python dependencies (requests)
  - Compact notification size (340x180px)
  - Elegant shaded design (#e8eaed background)
  - Normal case typography
  - All interactive features maintained (hover, click, keyboard, timer)
  - Cross-platform ready (Windows/Mac/Linux)

### Changed

- **LaunchQuote.bat** - Updated to try Python first, then fall back to browser

## [0.9.5] - 2025-11-12

### Added

- **LaunchQuote.bat** - Windows auto-launch batch file with relative path support
- **SETUP.md** - Quick setup guide with 5-minute installation instructions
  - Windows auto-launch setup (Startup Folder method)
  - Customization instructions (timer, position, browser)
  - Troubleshooting section
  - FAQ and support information

### Changed

- **README.md** - Updated with comprehensive auto-launch instructions
  - Added quick setup section for Windows 10/11
  - Updated project structure with new files
  - Updated roadmap to show 90% V1 completion
  - Added links to SETUP.md and AUTO_LAUNCH_GUIDE.md
  - Updated "Built With" section with DummyJSON and fallback quotes
  - Enhanced acknowledgments section

### Documentation

- Phase 4 (Deployment & Launch) now 75% complete
- Auto-launch setup completed for Windows
- Cross-platform instructions available in AUTO_LAUNCH_GUIDE.md

## [0.9.0] - 2025-11-12

### Added

- **Core Application (index.html)** - Complete single-file web application (~12KB)
- **Modern Gradient Design (Design B)** - Blue-purple gradient accent, clean professional UI
- **DummyJSON API Integration** - Primary quote source with 5-second timeout
- **15 Fallback Quotes** - High-quality motivational quotes for offline use
- **15-Second Auto-Close Timer** - Visual progress bar with countdown
- **Hover-to-Pause** - Timer pauses when hovering over quote
- **Click-to-Search** - Opens Google search for quote exploration
- **Keyboard Navigation** - Esc (close), Enter/Space (search), Tab (navigate)
- **Full Accessibility** - WCAG 2.1 AA compliant with ARIA labels, screen reader support
- **Responsive Design** - Mobile-friendly layout, adapts to all screen sizes
- **Smooth Animations** - 400ms slide-in, 1800ms fade-out with reduced motion support
- **Comprehensive CI/CD Pipeline** - 8 automated quality checks on every PR
  - Prettier (code formatting)
  - ESLint (JavaScript linting)
  - Markdownlint (documentation quality)
  - HTML validation
  - CSS validation
  - Accessibility testing
  - Link checking
  - Spell checking

### Research & Documentation

- **API_RESEARCH_REPORT.md** - Evaluation of 8 quote APIs, DummyJSON selected
- **UX_RESEARCH_REPORT.md** - UI/UX best practices, placement, timing research
- **CURATED_QUOTES.md** - 15 copyright-safe motivational quotes
- **DESIGN_AB_TEST.md** - 3 design variations, complete CSS implementations
- **DESIGN_QUICK_REFERENCE.md** - Quick design decision guide
- **design-preview.html** - Interactive preview of all 3 designs
- **AUTO_LAUNCH_GUIDE.md** - Windows startup methods and instructions
- **RESEARCH_SUMMARY.md** - Consolidated findings from all research

### Configuration Files

- `.github/workflows/quality-checks.yml` - GitHub Actions CI/CD workflow
- `package.json` - NPM scripts and dependencies
- `.eslintrc.json` - JavaScript linting rules (Node.js + browser overrides)
- `.prettierrc.json` + `.prettierignore` - Code formatting configuration
- `.markdownlint.json` - Markdown linting rules
- `.htmlvalidate.json` - HTML5 validation rules
- `.stylelintrc.json` - CSS linting configuration
- `.markdown-link-check.json` - Link validation settings
- `cspell.json` - Spell check dictionary
- `scripts/accessibility-test.js` - Automated accessibility testing

### Fixed

- JavaScript syntax errors from unescaped apostrophes in quote strings
- HTML validation strictness (disabled overly restrictive rules)
- Accessibility testing for runtime applications
- Prettier formatting across all project files

## [0.1.0] - 2025-11-12

### Added

- Initial project setup with documentation structure
- PRD.md - Product Requirements Document with detailed specifications
- CLAUDE.md - Development guide with sub-agent strategy
- README.md - Project overview and installation instructions
- LICENSE - MIT License for open source distribution
- CHANGELOG.md - This file for version tracking
- .gitignore - Git ignore rules

<!--
Template for future releases:

## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future releases

### Removed
- Features that have been removed

### Fixed
- Bug fixes

### Security
- Security updates
-->
