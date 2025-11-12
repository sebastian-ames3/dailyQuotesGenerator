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
