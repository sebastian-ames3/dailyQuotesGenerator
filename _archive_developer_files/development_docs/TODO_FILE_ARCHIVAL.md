# TODO: File Archival - Production Repository Cleanup

**Status:** Ready to execute
**Estimated Time:** 30-45 minutes
**Last Updated:** 2025-11-15

## What's Done ✅

- ✅ Security Audit & Hardening (V5.0.2)
  - API response validation
  - Settings validation
  - Dependency pinning
  - Atomic file writes
  - Resource limits
  - Debug mode

- ✅ Code Cleanup & Quality (V5.0.2)
  - Dead code removed (118 lines)
  - Imports optimized
  - Performance improvements
  - Version constants added
  - Enhanced documentation

- ✅ Comprehensive PRD created: `PRD_PRODUCTION_CLEANUP_FILE_ARCHIVAL.md`

## What's Left 📋

### Final Step: File Archival

Clean up the repository for public GitHub release by archiving developer files and removing generated artifacts.

---

## Execution Checklist

### Phase 1: Open Questions (5 min)

Before starting, answer these questions:

- [ ] **quotes_config.json** - Is this file used by Python version?
  - Check: Does `quote_overlay.py` import or read `config/quotes_config.json`?
  - If NO → Archive it
  - If YES → Keep in config/ directory

- [ ] **install_scheduled_quotes.bat** - Useful for users?
  - Does this provide value beyond LaunchQuote.bat?
  - If YES → Keep and document in SETUP.md
  - If NO → Archive it

- [ ] **uninstall_scheduled_quotes.bat** - Keep with install.bat?
  - If keeping install.bat → Keep this too
  - If archiving install.bat → Archive this too

- [ ] **quote_demo_screenshot.png** - Is this in README?
  - Open README.md and search for "screenshot" or ".png"
  - If referenced → Keep for documentation
  - If not referenced → Archive or delete

### Phase 2: Create Archive Structure (5 min)

```bash
# Create subdirectories in _archive_developer_files/
mkdir _archive_developer_files/v2_v3_planning
mkdir _archive_developer_files/v5_planning
mkdir _archive_developer_files/development_docs
mkdir _archive_developer_files/testing
mkdir _archive_developer_files/testing/tests
mkdir _archive_developer_files/testing/scripts
mkdir _archive_developer_files/html_version
mkdir _archive_developer_files/config_unused
```

### Phase 3: Move Planning Documents (5 min)

```bash
# V2/V3 planning docs
mv PRD_V3_RESPONSIVE_QUOTE_BOX.md _archive_developer_files/v2_v3_planning/
mv PRD_V3_SETTINGS_PAGE_REPLACEMENT.md _archive_developer_files/v2_v3_planning/
mv TASKS_V3_IMPLEMENTATION.md _archive_developer_files/v2_v3_planning/

# V5 planning docs
mv PRD_V5.0.0_ADVANCED_DESIGN.md _archive_developer_files/v5_planning/
mv BUTTON_DESIGN.md _archive_developer_files/v5_planning/
mv COLOR_SCHEMES.md _archive_developer_files/v5_planning/

# Production cleanup PRDs (archive after archival is complete)
# These will be moved in Phase 7
```

### Phase 4: Move Development Docs (3 min)

```bash
# CLAUDE.md is the big development history doc
mv CLAUDE.md _archive_developer_files/development_docs/

# DESIGN_QUICK_REFERENCE.md might already be archived - verify first
ls _archive_developer_files/v1_research/ | grep DESIGN_QUICK_REFERENCE
# If not there, and if it exists in root:
# mv DESIGN_QUICK_REFERENCE.md _archive_developer_files/development_docs/
```

### Phase 5: Move Testing Infrastructure (10 min)

```bash
# Move test files
mv tests/button-visibility.spec.js _archive_developer_files/testing/tests/
mv tests/button-visibility-simple.spec.js _archive_developer_files/testing/tests/
mv tests/responsive-quote-box.spec.js _archive_developer_files/testing/tests/
mv tests/settings-page-replacement.spec.js _archive_developer_files/testing/tests/
mv tests/visual-test.spec.js _archive_developer_files/testing/tests/

# Move test scripts
mv scripts/accessibility-test.js _archive_developer_files/testing/scripts/

# Move test configuration files
mv playwright.config.js _archive_developer_files/testing/
mv package.json _archive_developer_files/testing/
mv package-lock.json _archive_developer_files/testing/
mv cspell.json _archive_developer_files/testing/
mv test-settings-button.spec.js _archive_developer_files/testing/

# Remove now-empty directories
rmdir tests
rmdir scripts
```

### Phase 6: Delete Generated Artifacts (2 min)

**⚠️ IMPORTANT: These can be regenerated, safe to delete**

```bash
# Delete node_modules (12,000+ files)
rm -rf node_modules/

# Delete test results
rm -rf test-results/
```

### Phase 7: Move Production Cleanup PRDs (2 min)

```bash
# After archival is complete, archive the PRDs themselves
mv PRD_PRODUCTION_CLEANUP_FILE_ARCHIVAL.md _archive_developer_files/development_docs/
mv PRD_PRODUCTION_CLEANUP_SECURITY_AUDIT.md _archive_developer_files/development_docs/
mv PRD_PRODUCTION_CLEANUP_CODE_QUALITY.md _archive_developer_files/development_docs/
mv TODO_FILE_ARCHIVAL.md _archive_developer_files/development_docs/
```

### Phase 8: Update .gitignore (3 min)

Add to `.gitignore`:

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

# Temporary files
*.tmp
```

### Phase 9: Verification (5 min)

**Check Production Structure:**

```bash
# Root should have ~15 files
ls -1

# Expected files:
# - quote_overlay.py
# - LaunchQuote.bat
# - requirements.txt
# - user_settings.json (if exists, should be in .gitignore)
# - README.md
# - SETUP.md
# - AUTO_LAUNCH_GUIDE.md
# - CHANGELOG.md
# - LICENSE
# - .gitignore
# - _archive_developer_files/ (directory)
# - Optional: install_scheduled_quotes.bat, uninstall_scheduled_quotes.bat, quote_demo_screenshot.png
```

**Test Application:**

```bash
# Application should still work perfectly
python quote_overlay.py

# Verify:
# [ ] App launches
# [ ] Quote displays
# [ ] Settings button works
# [ ] Theme toggle works
# [ ] Timer works
# [ ] All features functional
```

**Check Git Status:**

```bash
git status

# Should show:
# - Deleted files (node_modules/, tests/, etc.)
# - Moved files (now in _archive_developer_files/)
# - New .gitignore entries
```

### Phase 10: Commit Changes (5 min)

```bash
# Stage all changes
git add -A

# Commit with clear message
git commit -m "$(cat <<'EOF'
V5.0.2: File Archival - Production Repository Cleanup

Organized repository for public GitHub release by archiving all
developer/research files and removing generated artifacts.

## Files Archived

**Planning Documents (6 files):**
- PRD_V3_RESPONSIVE_QUOTE_BOX.md → v2_v3_planning/
- PRD_V3_SETTINGS_PAGE_REPLACEMENT.md → v2_v3_planning/
- TASKS_V3_IMPLEMENTATION.md → v2_v3_planning/
- PRD_V5.0.0_ADVANCED_DESIGN.md → v5_planning/
- BUTTON_DESIGN.md → v5_planning/
- COLOR_SCHEMES.md → v5_planning/

**Development Documentation (4 files):**
- CLAUDE.md → development_docs/
- PRD_PRODUCTION_CLEANUP_*.md → development_docs/ (3 files)
- TODO_FILE_ARCHIVAL.md → development_docs/

**Testing Infrastructure:**
- tests/ → testing/tests/ (5 spec files)
- scripts/ → testing/scripts/ (1 file)
- playwright.config.js → testing/
- package.json, package-lock.json → testing/
- cspell.json → testing/
- test-settings-button.spec.js → testing/

## Files Deleted

- node_modules/ (~12,000 files - can regenerate)
- test-results/ (generated artifacts)
- tests/ (empty directory)
- scripts/ (empty directory)

## Files Added

- .gitignore entries for user data and generated files

## Production Repository Structure

Root directory now contains only:
- Production code (quote_overlay.py)
- User documentation (README.md, SETUP.md, etc.)
- Configuration files (requirements.txt, LaunchQuote.bat)
- Legal (LICENSE)
- Organized archive (_archive_developer_files/)

Total root files: ~15 (down from ~30)

## Verification

✅ Application tested and working
✅ All features functional
✅ No broken imports or dependencies
✅ Archive structure organized by category
✅ Git repository clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Expected Final Structure

```
dailyQuotesGenerator/
├── _archive_developer_files/     (organized archive)
│   ├── v1_research/              (existing - V1 research)
│   ├── v2_v3_planning/           (new - V2/V3 PRDs)
│   ├── v5_planning/              (new - V5 PRD & designs)
│   ├── development_docs/         (new - CLAUDE.md, PRDs)
│   └── testing/                  (new - all test infrastructure)
├── quote_overlay.py              (production code)
├── LaunchQuote.bat               (startup script)
├── requirements.txt              (pinned dependencies)
├── user_settings.json            (user config - gitignored)
├── README.md                     (public docs)
├── SETUP.md                      (setup guide)
├── AUTO_LAUNCH_GUIDE.md          (auto-launch guide)
├── CHANGELOG.md                  (version history)
├── LICENSE                       (MIT license)
└── .gitignore                    (updated)
```

---

## Notes for Tomorrow

**Starting Point:**
- Commit `281d7c0` has all security and code cleanup
- Repository is functional but needs organization
- All PRDs are written and ready

**What to Do:**
1. Read Phase 1 questions and answer them
2. Follow checklist phases 2-10 in order
3. Each phase is independent and can be done sequentially
4. Test after Phase 9 before committing

**Estimated Time:** 30-45 minutes total

**If Issues Arise:**
- Check `PRD_PRODUCTION_CLEANUP_FILE_ARCHIVAL.md` for detailed guidance
- All file moves are reversible with `git checkout`
- Test application after each major phase

---

## Quick Reference

**Current Version:** 5.0.2 (security + code cleanup)
**Next Version:** 5.0.2 (file archival - same version, just organization)
**Status:** Ready for execution
**Risk Level:** Low (just moving files, no code changes)

**After Completion:**
- Repository will be production-ready for GitHub
- Clean, professional structure
- All development history preserved in archive
- Easy for users to understand and contribute

---

**Good night! Pick this up tomorrow when you're fresh. 🌙**
