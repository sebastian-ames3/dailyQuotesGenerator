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
