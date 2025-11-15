# PRD: File Archival Strategy - Production Repository Cleanup

**Version:** 1.0.0
**Status:** Draft
**Created:** 2025-11-15
**Owner:** Production Readiness Initiative

## Executive Summary

Transform the repository from a development/research workspace into a clean, production-ready public repository by archiving all developer-specific files and maintaining only production-essential files.

## Goals

1. **Primary Goal:** Create a professional, public-facing repository with only production code
2. **Secondary Goal:** Preserve all development/research artifacts for personal reference
3. **Tertiary Goal:** Ensure GitHub repository reflects only production-quality content

## Current State Analysis

### Root Directory Files

**Production Files (KEEP):**
- `quote_overlay.py` - Main application (1,188 lines)
- `LaunchQuote.bat` - Windows startup script
- `requirements.txt` - Python dependencies
- `README.md` - Public documentation
- `LICENSE` - MIT license
- `user_settings.json` - User configuration (gitignored)

**Documentation (EVALUATE):**
- `CHANGELOG.md` - Production changelog (KEEP - valuable for users)
- `SETUP.md` - Installation guide (KEEP - user-facing)
- `AUTO_LAUNCH_GUIDE.md` - Auto-launch instructions (KEEP - user-facing)
- `CLAUDE.md` - Development history (ARCHIVE - internal only)
- `BUTTON_DESIGN.md` - Design documentation (ARCHIVE - development artifact)
- `COLOR_SCHEMES.md` - Color scheme options (ARCHIVE - research artifact)

**Planning Documents (ARCHIVE ALL):**
- `PRD_V3_RESPONSIVE_QUOTE_BOX.md`
- `PRD_V3_SETTINGS_PAGE_REPLACEMENT.md`
- `PRD_V5.0.0_ADVANCED_DESIGN.md`
- `TASKS_V3_IMPLEMENTATION.md`

**Development Tools (ARCHIVE/DELETE):**
- `install_scheduled_quotes.bat` - Experimental (EVALUATE - if useful, keep; else archive)
- `uninstall_scheduled_quotes.bat` - Experimental (EVALUATE)
- `quote_demo_screenshot.png` - Screenshot (EVALUATE - if in README, keep; else archive)

**Node.js/Testing Infrastructure (ARCHIVE ALL):**
- `node_modules/` - Dependencies (DELETE - not needed, add to .gitignore)
- `package.json` - NPM config (ARCHIVE - testing-only)
- `package-lock.json` - NPM lockfile (ARCHIVE)
- `playwright.config.js` - Playwright config (ARCHIVE)
- `cspell.json` - Spell checker config (ARCHIVE - development tool)
- `test-results/` - Test output (DELETE - generated artifacts)
- `tests/` - Playwright test suite (ARCHIVE - 5 spec files)
- `test-settings-button.spec.js` - Orphaned test file (ARCHIVE)

**Subdirectories:**
- `config/` - Configuration files (EVALUATE)
  - `quotes_config.json` - Not currently used by Python version (ARCHIVE or DELETE)
  - `user_settings.json` - Used by Python (KEEP but gitignore)
- `scripts/` - Development scripts (ARCHIVE)
  - `accessibility-test.js` - Testing script (ARCHIVE)
- `_archive_developer_files/` - Existing archive (KEEP structure)

### Archive Analysis

**Already Archived (Good!):**
- `API_RESEARCH_REPORT.md`
- `CLAUDE.md` (old version)
- `CURATED_QUOTES.md`
- `DESIGN_AB_TEST.md`
- `DESIGN_QUICK_REFERENCE.md`
- `design-preview.html`
- `PRD.md`
- `RESEARCH_SUMMARY.md`
- `UX_RESEARCH_REPORT.md`

## File Classification System

### Category 1: Production Essential (PUBLIC)
**Criteria:** Required for end-users to run/understand the application

- Python source code (`quote_overlay.py`)
- Startup scripts (`LaunchQuote.bat`)
- Dependencies (`requirements.txt`)
- User documentation (`README.md`, `SETUP.md`, `AUTO_LAUNCH_GUIDE.md`)
- Legal (`LICENSE`)
- Changelog (`CHANGELOG.md`)

### Category 2: Development Artifacts (ARCHIVE)
**Criteria:** Valuable for development history but not needed by users

- PRD documents (planning, specifications)
- Design documents (`BUTTON_DESIGN.md`, `COLOR_SCHEMES.md`)
- Development guide (`CLAUDE.md`)
- Task lists and implementation notes
- Research reports (already archived)

### Category 3: Testing Infrastructure (ARCHIVE)
**Criteria:** Used for quality assurance during development

- Test suites (`tests/`)
- Test configuration (`playwright.config.js`, `package.json`)
- Test scripts (`scripts/accessibility-test.js`)
- Test spec files

### Category 4: Generated Artifacts (DELETE)
**Criteria:** Can be regenerated, should not be in git

- `node_modules/` (12,000+ files)
- `test-results/` (generated output)
- Build artifacts
- Cache files

### Category 5: User Data (GITIGNORE)
**Criteria:** User-specific, should never be committed

- `user_settings.json` (in root)
- Any `.log` files
- Any `.cache` directories

## Archival Strategy

### Phase 1: Preparation
1. Create comprehensive inventory (this document)
2. Review each file category with user
3. Verify no production code in "archive" categories
4. Create backup branch before major changes

### Phase 2: Archive Structure
```
_archive_developer_files/
├── v1_research/           (already exists with V1 research)
│   ├── API_RESEARCH_REPORT.md
│   ├── CURATED_QUOTES.md
│   ├── DESIGN_AB_TEST.md
│   ├── design-preview.html
│   ├── PRD.md
│   ├── RESEARCH_SUMMARY.md
│   └── UX_RESEARCH_REPORT.md
├── v2_v3_planning/       (new - V2/V3 PRDs and tasks)
│   ├── PRD_V3_RESPONSIVE_QUOTE_BOX.md
│   ├── PRD_V3_SETTINGS_PAGE_REPLACEMENT.md
│   └── TASKS_V3_IMPLEMENTATION.md
├── v5_planning/          (new - V5 planning)
│   ├── PRD_V5.0.0_ADVANCED_DESIGN.md
│   ├── BUTTON_DESIGN.md
│   └── COLOR_SCHEMES.md
├── development_docs/     (new - development guides)
│   ├── CLAUDE.md
│   └── DESIGN_QUICK_REFERENCE.md
├── testing/              (new - all test infrastructure)
│   ├── tests/
│   │   ├── button-visibility.spec.js
│   │   ├── button-visibility-simple.spec.js
│   │   ├── responsive-quote-box.spec.js
│   │   ├── settings-page-replacement.spec.js
│   │   └── visual-test.spec.js
│   ├── scripts/
│   │   └── accessibility-test.js
│   ├── playwright.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── cspell.json
│   └── test-settings-button.spec.js
├── html_version/         (new - archived HTML implementation)
│   └── (any remaining .html files if found)
└── config/               (new - unused config files)
    └── quotes_config.json (if not used in production)
```

### Phase 3: Execution Plan

**Step 1: Create Archive Subdirectories**
```bash
mkdir _archive_developer_files/v2_v3_planning
mkdir _archive_developer_files/v5_planning
mkdir _archive_developer_files/development_docs
mkdir _archive_developer_files/testing
mkdir _archive_developer_files/testing/tests
mkdir _archive_developer_files/testing/scripts
mkdir _archive_developer_files/html_version
mkdir _archive_developer_files/config
```

**Step 2: Move Planning Documents**
```bash
# V2/V3 planning
mv PRD_V3_RESPONSIVE_QUOTE_BOX.md _archive_developer_files/v2_v3_planning/
mv PRD_V3_SETTINGS_PAGE_REPLACEMENT.md _archive_developer_files/v2_v3_planning/
mv TASKS_V3_IMPLEMENTATION.md _archive_developer_files/v2_v3_planning/

# V5 planning
mv PRD_V5.0.0_ADVANCED_DESIGN.md _archive_developer_files/v5_planning/
mv BUTTON_DESIGN.md _archive_developer_files/v5_planning/
mv COLOR_SCHEMES.md _archive_developer_files/v5_planning/
```

**Step 3: Move Development Docs**
```bash
mv CLAUDE.md _archive_developer_files/development_docs/
# DESIGN_QUICK_REFERENCE.md already in archive - verify
```

**Step 4: Move Testing Infrastructure**
```bash
# Move test directories
mv tests/* _archive_developer_files/testing/tests/
mv scripts/* _archive_developer_files/testing/scripts/

# Move test config files
mv playwright.config.js _archive_developer_files/testing/
mv package.json _archive_developer_files/testing/
mv package-lock.json _archive_developer_files/testing/
mv cspell.json _archive_developer_files/testing/
mv test-settings-button.spec.js _archive_developer_files/testing/
```

**Step 5: Move Unused Config**
```bash
# Only if quotes_config.json is not used by Python version
# (need to verify in code)
# mv config/quotes_config.json _archive_developer_files/config/
```

**Step 6: Delete Generated Artifacts**
```bash
rm -rf node_modules/
rm -rf test-results/
# Note: Keep empty tests/ and scripts/ dirs or remove completely
```

**Step 7: Clean Up Empty Directories**
```bash
# Remove empty directories if all contents moved
rmdir tests/     # if empty
rmdir scripts/   # if empty
rmdir config/    # if empty (only if quotes_config.json moved)
```

### Phase 4: Update .gitignore

**Add to .gitignore:**
```gitignore
# User settings (never commit)
user_settings.json

# Node modules (if ever used again)
node_modules/

# Test results
test-results/

# Python cache
__pycache__/
*.pyc
*.pyo

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
```

## Post-Archival Production Structure

**Root directory after cleanup:**
```
dailyQuotesGenerator/
├── _archive_developer_files/    (organized archive - not in .gitignore)
├── quote_overlay.py              (main application)
├── LaunchQuote.bat               (startup script)
├── requirements.txt              (dependencies)
├── user_settings.json            (user config - gitignored)
├── README.md                     (public docs)
├── SETUP.md                      (setup guide)
├── AUTO_LAUNCH_GUIDE.md          (auto-launch guide)
├── CHANGELOG.md                  (version history)
├── LICENSE                       (MIT license)
├── .gitignore                    (git configuration)
└── install_scheduled_quotes.bat  (if keeping)
└── uninstall_scheduled_quotes.bat (if keeping)
└── quote_demo_screenshot.png     (if referenced in README)
```

**Optional: Keep if Useful**
- `install_scheduled_quotes.bat` - If this provides value to users (Windows Task Scheduler setup)
- `uninstall_scheduled_quotes.bat` - Companion to above
- `quote_demo_screenshot.png` - If shown in README for demo purposes

## Success Criteria

### Functional Requirements
- [ ] All production files remain in root
- [ ] Application runs without errors after archival
- [ ] No broken imports or missing dependencies
- [ ] User settings persist correctly
- [ ] LaunchQuote.bat still works

### Documentation Requirements
- [ ] README.md updated if structure changed
- [ ] SETUP.md updated if paths changed
- [ ] CHANGELOG.md documents cleanup as V5.0.2 or similar
- [ ] All archived files preserve their original content

### Repository Requirements
- [ ] Root directory has ≤15 files (excluding hidden files)
- [ ] No node_modules in repository
- [ ] No test-results in repository
- [ ] user_settings.json in .gitignore
- [ ] Archive directory organized by category

### Verification Checklist
- [ ] Run `python quote_overlay.py` - works without errors
- [ ] Check all imports resolve correctly
- [ ] Verify user_settings.json still loads/saves
- [ ] Test theme switching
- [ ] Test settings panel
- [ ] Run git status - no unintended changes
- [ ] Review .gitignore - all user files ignored
- [ ] Confirm archive structure matches design

## Risk Assessment

### High Risk
- **Accidentally deleting production code** → Mitigation: Create backup branch first
- **Breaking imports/dependencies** → Mitigation: Test application after each move
- **Losing development history** → Mitigation: Archive files, don't delete

### Medium Risk
- **README references archived files** → Mitigation: Update documentation
- **Paths hardcoded in scripts** → Mitigation: Search for references before moving
- **User confusion about new structure** → Mitigation: Update CHANGELOG

### Low Risk
- **GitHub Pages broken links** → Mitigation: Not using GitHub Pages
- **External references to old structure** → Mitigation: No known external references

## Open Questions

1. **quotes_config.json**: Is this file used by the Python version? (Need to check code)
   - If NO → Archive it
   - If YES → Keep in root or config/ directory

2. **install/uninstall .bat files**: Are these useful for users?
   - If YES → Keep and document in SETUP.md
   - If NO → Archive them

3. **quote_demo_screenshot.png**: Is this in README?
   - If YES → Keep for documentation
   - If NO → Archive or delete

4. **config/ directory**: Should it exist if only user_settings.json remains?
   - Option A: Keep config/ with user_settings.json
   - Option B: Move user_settings.json to root, delete config/

5. **DESIGN_QUICK_REFERENCE.md**: Already in archive - verify no duplicate in root

6. **Archive commit strategy**:
   - Option A: One big commit "Archive developer files"
   - Option B: Multiple commits per category
   - User preference?

## Implementation Timeline

**Total Estimated Time:** 1.5 hours

1. **Preparation (15 min)**
   - Review this PRD with user
   - Answer open questions
   - Create backup branch
   - Final go/no-go decision

2. **Execution (45 min)**
   - Create archive directory structure
   - Move files systematically by category
   - Delete generated artifacts
   - Clean up empty directories
   - Update .gitignore

3. **Verification (20 min)**
   - Test application thoroughly
   - Verify all imports work
   - Check all features functional
   - Review git status
   - Confirm archive organized correctly

4. **Documentation (10 min)**
   - Update CHANGELOG.md
   - Update README.md if needed
   - Add this PRD to archive

## Next Steps

1. User reviews and approves this PRD
2. User answers open questions
3. Create backup branch: `git checkout -b backup-pre-cleanup`
4. Execute Phase 3 (file moves) systematically
5. Run verification checklist
6. Commit changes with clear message
7. Move to Security Audit PRD
