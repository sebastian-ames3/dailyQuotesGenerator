# Task List: V3.0 Implementation

**Features:** Responsive Quote Box + Settings Page Replacement
**Version:** 3.0
**Created:** 2025-11-13
**Status:** Ready for Development

---

## Phase 1: Responsive Quote Box

### Task 1.1: Update Quote Container CSS
**Priority:** P0
**Estimated Time:** 15 minutes
**Related REQ:** REQ-RQB-001 to REQ-RQB-008

**Subtasks:**
- [ ] Open `index.html` in editor
- [ ] Locate `.quote-container` CSS (line ~56)
- [ ] Change `width: 500px` → `width: fit-content`
- [ ] Change `max-width: 90vw` → `max-width: min(800px, 90vw)`
- [ ] Add `min-width: 320px`
- [ ] Verify `min-height: 180px` exists
- [ ] Verify `max-height: 80vh` exists
- [ ] Remove `border: 4px solid red` debug border if present
- [ ] Update transition property to include width/height if needed

**Acceptance Criteria:**
- CSS properties updated correctly
- No syntax errors in CSS

---

### Task 1.2: Test Quote Box Responsiveness Locally
**Priority:** P0
**Estimated Time:** 20 minutes
**Related REQ:** REQ-RQB-001 to REQ-RQB-015

**Subtasks:**
- [ ] Start local HTTP server: `python -m http.server 8081`
- [ ] Open `http://localhost:8081/index.html` in browser
- [ ] Test short quote (force fallback, select short quote)
- [ ] Test medium quote
- [ ] Test long quote (100+ words)
- [ ] Verify buttons (⚙️, 🌙, ×) remain visible
- [ ] Verify author citation remains at bottom
- [ ] Verify progress bar remains at bottom
- [ ] Test all 4 position settings (bottomRight, topLeft, etc.)
- [ ] Test on mobile viewport (Chrome DevTools: 375px width)

**Acceptance Criteria:**
- Box width adapts to quote length
- Box never exceeds viewport boundaries
- All UI elements remain visible

---

### Task 1.3: Create Playwright Tests for Quote Responsiveness
**Priority:** P0
**Estimated Time:** 30 minutes
**Related REQ:** REQ-RQB-001 to REQ-RQB-018

**Subtasks:**
- [ ] Create `tests/responsive-quote-box.spec.js`
- [ ] **Test Case 1:** Load quote, measure width, verify < 800px
- [ ] **Test Case 2:** Force short quote (10 words), verify min-width: 320px
- [ ] **Test Case 3:** Force long quote (inject 200 words), verify max-width: 800px
- [ ] **Test Case 4:** Test mobile viewport (375px), verify box respects 90vw
- [ ] **Test Case 5:** Test all 4 positions, verify box stays in viewport
- [ ] **Test Case 6:** Verify buttons remain visible in all scenarios
- [ ] Add screenshot capture for visual regression
- [ ] Add console logging for dimensions

**Acceptance Criteria:**
- All 6 test cases pass
- Screenshots captured for review
- No elements outside viewport

**Test Code Structure:**
```javascript
test('short quote uses min-width', async ({ page }) => {
  await page.goto('http://localhost:8081/index.html');

  // Inject short quote
  await page.evaluate(() => {
    document.querySelector('.quote-text').textContent = 'Short quote.';
  });

  const box = await page.locator('.quote-container').boundingBox();
  expect(box.width).toBeGreaterThanOrEqual(320);
  expect(box.width).toBeLessThanOrEqual(500);
});
```

---

### Task 1.4: Manual Cross-Browser Testing
**Priority:** P1
**Estimated Time:** 20 minutes
**Related REQ:** REQ-RQB-001 to REQ-RQB-018

**Subtasks:**
- [ ] Test in Chrome (primary browser)
- [ ] Test in Firefox
- [ ] Test in Edge
- [ ] Test in Safari (if available)
- [ ] Verify `fit-content` support in all browsers
- [ ] Verify `min()` function support
- [ ] Test light and dark themes
- [ ] Test all 3 font sizes (small, medium, large)

**Acceptance Criteria:**
- Consistent behavior across all browsers
- No layout issues detected

---

## Phase 2: Settings Page Replacement

### Task 2.1: Update Settings Panel CSS
**Priority:** P0
**Estimated Time:** 20 minutes
**Related REQ:** REQ-SPR-010 to REQ-SPR-014

**Subtasks:**
- [ ] Open `index.html` in editor
- [ ] Locate `.settings-panel` CSS (line ~246)
- [ ] Change `position: absolute` → `position: fixed`
- [ ] Change `top: 100%; right: 0` → `top: 50%; left: 50%`
- [ ] Add `transform: translate(-50%, -50%)`
- [ ] Change `width: 300px` → `width: fit-content`
- [ ] Add `min-width: 400px`
- [ ] Add `max-width: min(600px, 90vw)`
- [ ] Add `max-height: 80vh`
- [ ] Add `overflow-y: auto`
- [ ] Update `z-index: 10001` → `z-index: 1000000`
- [ ] Add `display: none` to hidden state
- [ ] Update `.show` class to include `display: block`

**Acceptance Criteria:**
- Settings panel CSS updated correctly
- Panel positioned at center of viewport
- Panel respects size constraints

---

### Task 2.2: Add CSS for Quote Box Hiding
**Priority:** P0
**Estimated Time:** 5 minutes
**Related REQ:** REQ-SPR-001 to REQ-SPR-003

**Subtasks:**
- [ ] Add new CSS class `.quote-container.settings-open`
- [ ] Set `opacity: 0` and `pointer-events: none`
- [ ] Add smooth transition for opacity

**CSS Code:**
```css
.quote-container.settings-open {
  opacity: 0;
  pointer-events: none;
}
```

**Acceptance Criteria:**
- CSS class added correctly
- Transition is smooth

---

### Task 2.3: Add Back Button to Settings Panel HTML
**Priority:** P0
**Estimated Time:** 10 minutes
**Related REQ:** REQ-SPR-005 to REQ-SPR-009

**Subtasks:**
- [ ] Locate settings panel HTML (line ~465)
- [ ] Add back button HTML before `<h3>Settings</h3>`
- [ ] Set button ID: `backButton`
- [ ] Add ARIA label: "Back to quote"
- [ ] Add title: "Back to Quote (Esc)"
- [ ] Add button text: "← Back"

**HTML Code:**
```html
<button
  class="back-button"
  id="backButton"
  aria-label="Back to quote"
  title="Back to Quote (Esc)"
>
  ← Back
</button>
```

**Acceptance Criteria:**
- Back button HTML added
- Proper accessibility attributes included

---

### Task 2.4: Add Back Button CSS
**Priority:** P0
**Estimated Time:** 15 minutes
**Related REQ:** REQ-SPR-005, REQ-SPR-024

**Subtasks:**
- [ ] Add `.back-button` CSS class
- [ ] Position absolute, top-left (top: 16px, left: 16px)
- [ ] Style similar to close button (transparent background, hover state)
- [ ] Add focus state (outline)
- [ ] Add cursor: pointer
- [ ] Add z-index: 10

**CSS Code:**
```css
.back-button {
  position: absolute;
  top: 16px;
  left: 16px;
  background: transparent;
  border: none;
  color: var(--text-color);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.2s ease, color 0.2s ease;
  z-index: 10;
}

.back-button:hover {
  background: var(--close-hover-bg);
  color: var(--close-hover-color);
}

.back-button:focus {
  outline: 2px solid var(--accent-solid);
  outline-offset: 2px;
}
```

**Acceptance Criteria:**
- Back button styled correctly
- Hover and focus states work
- Button visible in light and dark themes

---

### Task 2.5: Update JavaScript - Settings State Management
**Priority:** P0
**Estimated Time:** 25 minutes
**Related REQ:** REQ-SPR-015 to REQ-SPR-019

**Subtasks:**
- [ ] Locate JavaScript section (line ~600)
- [ ] Add `let settingsOpen = false;` global variable
- [ ] Rename `toggleSettings()` → `openSettings()` and `closeSettings()`
- [ ] Implement `openSettings()` function:
  - Add `show` class to settings panel
  - Add `settings-open` class to quote container
  - Set `settingsOpen = true`
  - Update ARIA attributes
  - Focus back button
- [ ] Implement `closeSettings()` function:
  - Remove `show` class from settings panel
  - Remove `settings-open` class from quote container
  - Set `settingsOpen = false`
  - Update ARIA attributes
  - Return focus to settings button
- [ ] Update settings button listener to call `openSettings()`

**JavaScript Code:**
```javascript
let settingsOpen = false;

function openSettings() {
  settingsPanel.classList.add('show');
  container.classList.add('settings-open');
  settingsOpen = true;

  // Accessibility
  settingsPanel.setAttribute('aria-hidden', 'false');
  container.setAttribute('aria-hidden', 'true');

  // Focus management
  document.getElementById('backButton').focus();
}

function closeSettings() {
  settingsPanel.classList.remove('show');
  container.classList.remove('settings-open');
  settingsOpen = false;

  // Accessibility
  settingsPanel.setAttribute('aria-hidden', 'true');
  container.setAttribute('aria-hidden', 'false');

  // Return focus
  settingsButton.focus();
}

// Update event listener
settingsButton.addEventListener('click', openSettings);
```

**Acceptance Criteria:**
- Settings open/close functions work correctly
- State variable tracks open/closed correctly
- ARIA attributes updated properly

---

### Task 2.6: Add Back Button Event Listener
**Priority:** P0
**Estimated Time:** 5 minutes
**Related REQ:** REQ-SPR-006, REQ-SPR-007

**Subtasks:**
- [ ] Get back button element: `const backButton = document.getElementById('backButton');`
- [ ] Add click listener: `backButton.addEventListener('click', closeSettings);`

**JavaScript Code:**
```javascript
const backButton = document.getElementById('backButton');
backButton.addEventListener('click', closeSettings);
```

**Acceptance Criteria:**
- Back button closes settings and returns to quote

---

### Task 2.7: Add Esc Key Listener
**Priority:** P0
**Estimated Time:** 10 minutes
**Related REQ:** REQ-SPR-009

**Subtasks:**
- [ ] Update existing Esc key listener to check `settingsOpen` state
- [ ] If settings open and Esc pressed, call `closeSettings()`
- [ ] Ensure existing Esc behavior (close quote) still works

**JavaScript Code:**
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (settingsOpen) {
      closeSettings();
    } else {
      closeQuote();
    }
  }
});
```

**Acceptance Criteria:**
- Esc closes settings when settings are open
- Esc closes quote when settings are closed

---

### Task 2.8: Pause Timer When Settings Open
**Priority:** P1
**Estimated Time:** 15 minutes
**Related REQ:** Open Question #5 in PRD

**Subtasks:**
- [ ] In `openSettings()`, call `clearInterval(countdownInterval)` if timer is running
- [ ] In `closeSettings()`, restart timer with remaining time
- [ ] Store remaining time before pausing: `let pausedTimeRemaining`

**JavaScript Code:**
```javascript
let pausedTimeRemaining = null;

function openSettings() {
  // ... existing code ...

  // Pause timer
  if (countdownInterval) {
    clearInterval(countdownInterval);
    pausedTimeRemaining = timerDuration; // Store remaining time
  }
}

function closeSettings() {
  // ... existing code ...

  // Resume timer
  if (pausedTimeRemaining !== null) {
    startTimer(pausedTimeRemaining);
    pausedTimeRemaining = null;
  }
}
```

**Acceptance Criteria:**
- Timer pauses when settings open
- Timer resumes when settings close
- Remaining time preserved

---

### Task 2.9: Test Settings Page Replacement Locally
**Priority:** P0
**Estimated Time:** 20 minutes
**Related REQ:** REQ-SPR-001 to REQ-SPR-022

**Subtasks:**
- [ ] Start local HTTP server
- [ ] Open `http://localhost:8081/index.html`
- [ ] Click ⚙️ settings button
- [ ] Verify quote box disappears (opacity 0)
- [ ] Verify settings panel appears (centered, visible)
- [ ] Click back button
- [ ] Verify settings panel disappears
- [ ] Verify quote box reappears
- [ ] Press ⚙️ again, then press Esc
- [ ] Verify settings close correctly
- [ ] Test in mobile viewport (375px)
- [ ] Test light and dark themes
- [ ] Test focus management (Tab, Shift+Tab)

**Acceptance Criteria:**
- Settings panel always visible when open
- Quote box hidden when settings open
- Back button works
- Esc key works
- Focus management correct

---

### Task 2.10: Create Playwright Tests for Settings Page Replacement
**Priority:** P0
**Estimated Time:** 30 minutes
**Related REQ:** REQ-SPR-001 to REQ-SPR-026

**Subtasks:**
- [ ] Create `tests/settings-page-replacement.spec.js`
- [ ] **Test Case 1:** Click ⚙️ → Settings visible, quote hidden
- [ ] **Test Case 2:** Click back → Quote visible, settings hidden
- [ ] **Test Case 3:** Press Esc → Settings close correctly
- [ ] **Test Case 4:** Settings panel in viewport (check boundingBox)
- [ ] **Test Case 5:** Focus management (⚙️ → back button → ⚙️)
- [ ] **Test Case 6:** Mobile viewport → Settings fit correctly
- [ ] **Test Case 7:** Change settings, close, verify applied
- [ ] Add screenshot capture for visual regression
- [ ] Add ARIA attribute verification

**Acceptance Criteria:**
- All 7 test cases pass
- Screenshots captured
- Settings always in viewport

**Test Code Structure:**
```javascript
test('settings panel replaces quote box', async ({ page }) => {
  await page.goto('http://localhost:8081/index.html');

  // Initial state: quote visible, settings hidden
  await expect(page.locator('.quote-container')).toBeVisible();
  await expect(page.locator('.settings-panel')).not.toBeVisible();

  // Click settings button
  await page.click('#settingsButton');

  // Settings visible, quote hidden
  await expect(page.locator('.settings-panel')).toBeVisible();
  await expect(page.locator('.quote-container')).toHaveClass(/settings-open/);

  // Verify settings panel in viewport
  const settingsBox = await page.locator('.settings-panel').boundingBox();
  const viewport = page.viewportSize();
  expect(settingsBox.y).toBeGreaterThan(0);
  expect(settingsBox.y + settingsBox.height).toBeLessThanOrEqual(viewport.height);
});
```

---

### Task 2.11: Accessibility Testing
**Priority:** P1
**Estimated Time:** 20 minutes
**Related REQ:** REQ-SPR-026

**Subtasks:**
- [ ] Run axe-core accessibility tests: `npx @axe-core/cli http://localhost:8081/index.html`
- [ ] Test with keyboard only (no mouse):
  - Tab to settings button, press Enter
  - Tab to back button, press Enter
  - Repeat with Esc key
- [ ] Test with screen reader (if available):
  - Verify "Settings" announcement when opened
  - Verify "Back to quote" button label
  - Verify setting controls are labeled
- [ ] Verify ARIA attributes:
  - `aria-hidden` on quote box and settings panel
  - `aria-label` on back button
- [ ] Test focus trap (Tab cycles within settings only)

**Acceptance Criteria:**
- No accessibility violations detected
- Keyboard navigation works perfectly
- Screen reader announces correctly
- ARIA attributes correct

---

## Phase 3: Integration & Refinement

### Task 3.1: Test Both Features Together
**Priority:** P0
**Estimated Time:** 20 minutes

**Subtasks:**
- [ ] Load short quote → Verify responsive box → Open settings → Close settings
- [ ] Load long quote → Verify responsive box → Open settings → Close settings
- [ ] Test all 4 positions with responsive box and settings panel
- [ ] Test all font sizes with responsive box and settings panel
- [ ] Test theme switching while in settings
- [ ] Test category switching, verify quote box resizes appropriately

**Acceptance Criteria:**
- No conflicts between two features
- Settings changes apply correctly to responsive quote box
- No visual glitches

---

### Task 3.2: Run Full Playwright Test Suite
**Priority:** P0
**Estimated Time:** 10 minutes

**Subtasks:**
- [ ] Run all Playwright tests: `npx playwright test --reporter=line`
- [ ] Review test results
- [ ] Fix any failing tests
- [ ] Review screenshots for visual regressions
- [ ] Verify no elements outside viewport in any test

**Acceptance Criteria:**
- All Playwright tests pass
- No visual regressions detected
- All screenshots show correct layout

---

### Task 3.3: Cross-Browser Testing
**Priority:** P1
**Estimated Time:** 25 minutes

**Subtasks:**
- [ ] Test in Chrome (Windows/Mac)
- [ ] Test in Firefox
- [ ] Test in Edge
- [ ] Test in Safari (if available)
- [ ] Test on physical mobile device (iOS and/or Android)
- [ ] Verify consistent behavior across all browsers

**Acceptance Criteria:**
- Features work identically in all browsers
- No browser-specific bugs found

---

### Task 3.4: Performance Testing
**Priority:** P1
**Estimated Time:** 15 minutes

**Subtasks:**
- [ ] Open Chrome DevTools → Performance tab
- [ ] Record: Load quote → Open settings → Close settings → Load new quote
- [ ] Verify no layout thrashing (excessive reflows)
- [ ] Verify transitions are smooth (60fps)
- [ ] Check memory usage (no leaks)
- [ ] Test with 20 consecutive quote loads

**Acceptance Criteria:**
- Page load time < 1 second
- Transitions smooth (no janking)
- No memory leaks detected
- CPU usage reasonable

---

## Phase 4: Documentation & Deployment

### Task 4.1: Update CHANGELOG.md
**Priority:** P0
**Estimated Time:** 15 minutes

**Subtasks:**
- [ ] Add V3.0 section to CHANGELOG.md
- [ ] Document responsive quote box changes
- [ ] Document settings page replacement changes
- [ ] List all CSS/HTML/JS changes
- [ ] Note breaking changes (none expected)
- [ ] Add migration notes (none needed)

**Template:**
```markdown
## [3.0.0] - 2025-11-13

### Added
- **Responsive Quote Box**: Box now dynamically adapts width (320-800px) and height based on quote length
- **Settings Page Replacement**: Settings panel now appears as a centered modal that replaces the quote box instead of appearing below it
- **Back Button**: Added back button (← Back) to settings panel for clear navigation

### Changed
- Quote box width changed from fixed `500px` to dynamic `fit-content` with min/max constraints
- Settings panel positioning changed from `absolute` (below box) to `fixed` (centered)
- Settings panel now hides quote box when open (single view at a time)
- Esc key now closes settings panel if open, otherwise closes quote

### Fixed
- **Critical**: Settings panel no longer appears off-screen
- Settings panel now 100% visible on all screen sizes including mobile
- Quote box no longer wastes space with short quotes or feels cramped with long quotes

### Technical
- CSS: Updated `.quote-container` with `width: fit-content`, `min-width: 320px`, `max-width: min(800px, 90vw)`
- CSS: Updated `.settings-panel` with `position: fixed`, centered positioning
- CSS: Added `.quote-container.settings-open` class for hiding quote
- HTML: Added back button to settings panel
- JavaScript: Refactored `toggleSettings()` → `openSettings()` + `closeSettings()`
- JavaScript: Added timer pause/resume when settings open/close
```

**Acceptance Criteria:**
- CHANGELOG.md updated with complete V3.0 notes
- All changes documented clearly

---

### Task 4.2: Update CLAUDE.md
**Priority:** P0
**Estimated Time:** 20 minutes

**Subtasks:**
- [ ] Add V3.0 section to CLAUDE.md
- [ ] Document responsive quote box architectural decision
- [ ] Document settings page replacement architectural decision
- [ ] Add "Lessons Learned" section for V3.0
- [ ] Update "Architectural Decisions" section
- [ ] Document Playwright usage for testing
- [ ] Add user feedback notes

**Key Points to Document:**
- Why we chose `fit-content` over tiered sizing
- Why we chose page replacement over overlay/modal
- How Playwright helped validate the design
- User's requirement: "quote box should be fully responsive"

**Acceptance Criteria:**
- CLAUDE.md updated with V3.0 development history
- Architectural decisions documented

---

### Task 4.3: Update README.md (if needed)
**Priority:** P2
**Estimated Time:** 10 minutes

**Subtasks:**
- [ ] Review README.md for accuracy
- [ ] Update feature list if needed
- [ ] Update screenshots (if any)
- [ ] Add V3.0 highlights to top of README

**Acceptance Criteria:**
- README.md reflects current state of project

---

### Task 4.4: Git Commit & Push
**Priority:** P0
**Estimated Time:** 10 minutes

**Subtasks:**
- [ ] Review all changes: `git diff`
- [ ] Stage changes: `git add index.html tests/ CHANGELOG.md CLAUDE.md`
- [ ] Write descriptive commit message
- [ ] Commit: `git commit -m "..."`
- [ ] Push to GitHub: `git push origin main`

**Commit Message Template:**
```
V3.0: Responsive Quote Box + Settings Page Replacement

Features:
1. Responsive Quote Box
   - Width dynamically adapts to quote length (320-800px)
   - Height auto-adjusts to content with scrolling for long quotes
   - Box uses fit-content for intelligent sizing
   - Maintains readability and visual balance

2. Settings Page Replacement
   - Settings panel now appears centered, replacing quote box
   - Added back button (← Back) for clear navigation
   - Esc key closes settings and returns to quote
   - 100% viewport compliance - always visible
   - Timer pauses when settings open, resumes on close

CSS Changes:
- .quote-container: width: fit-content, min-width: 320px, max-width: min(800px, 90vw)
- .settings-panel: position: fixed, centered with transform
- Added .quote-container.settings-open for hiding quote
- Added .back-button styling

HTML Changes:
- Added back button to settings panel

JavaScript Changes:
- Refactored toggleSettings() → openSettings() + closeSettings()
- Added settingsOpen state tracking
- Added ARIA attribute management
- Added timer pause/resume functionality
- Updated Esc key handler to close settings or quote

Testing:
- Added tests/responsive-quote-box.spec.js (6 test cases)
- Added tests/settings-page-replacement.spec.js (7 test cases)
- All tests passing, no visual regressions

Fixes:
- Critical: Settings panel no longer off-screen
- Quote box now responsive to content length
- Focus management correct for settings navigation

Related:
- PRD_V3_RESPONSIVE_QUOTE_BOX.md
- PRD_V3_SETTINGS_PAGE_REPLACEMENT.md
- TASKS_V3_IMPLEMENTATION.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Acceptance Criteria:**
- Changes committed with descriptive message
- Pushed to GitHub successfully

---

## Task Summary

### Total Tasks: 30
- **Phase 1 (Responsive Quote Box)**: 4 tasks
- **Phase 2 (Settings Page Replacement)**: 11 tasks
- **Phase 3 (Integration & Refinement)**: 4 tasks
- **Phase 4 (Documentation & Deployment)**: 4 tasks

### Estimated Total Time: ~7 hours
- **Phase 1**: ~1.5 hours
- **Phase 2**: ~3 hours
- **Phase 3**: ~1.5 hours
- **Phase 4**: ~1 hour

### Priority Breakdown
- **P0 (Must Have)**: 24 tasks
- **P1 (Should Have)**: 5 tasks
- **P2 (Nice to Have)**: 1 task

---

## Implementation Order

### Session 1 (2-3 hours)
1. Task 1.1: Update Quote Container CSS
2. Task 1.2: Test Quote Box Responsiveness Locally
3. Task 2.1: Update Settings Panel CSS
4. Task 2.2: Add CSS for Quote Box Hiding
5. Task 2.3: Add Back Button HTML
6. Task 2.4: Add Back Button CSS

**Checkpoint:** Visual changes complete, ready for JavaScript

### Session 2 (2-3 hours)
7. Task 2.5: Update JavaScript - Settings State Management
8. Task 2.6: Add Back Button Event Listener
9. Task 2.7: Add Esc Key Listener
10. Task 2.8: Pause Timer When Settings Open
11. Task 2.9: Test Settings Page Replacement Locally
12. Task 3.1: Test Both Features Together

**Checkpoint:** Features functional, ready for automated testing

### Session 3 (1-2 hours)
13. Task 1.3: Create Playwright Tests for Quote Responsiveness
14. Task 2.10: Create Playwright Tests for Settings Page Replacement
15. Task 3.2: Run Full Playwright Test Suite
16. Task 2.11: Accessibility Testing (if time permits)

**Checkpoint:** Automated tests complete, ready for deployment

### Session 4 (1 hour)
17. Task 1.4: Manual Cross-Browser Testing
18. Task 3.3: Cross-Browser Testing
19. Task 4.1: Update CHANGELOG.md
20. Task 4.2: Update CLAUDE.md
21. Task 4.4: Git Commit & Push

**Checkpoint:** V3.0 deployed to GitHub

---

## Notes

- Keep HTTP server running throughout implementation: `python -m http.server 8081`
- Test frequently after each change (don't batch multiple changes)
- Take screenshots at key milestones for documentation
- If blocked, refer back to PRDs for requirements clarification
- User preference: Commit frequently (after each phase or major task)

---

**Status**: Ready to begin implementation
**Next Step**: Start with Task 1.1 (Update Quote Container CSS)
