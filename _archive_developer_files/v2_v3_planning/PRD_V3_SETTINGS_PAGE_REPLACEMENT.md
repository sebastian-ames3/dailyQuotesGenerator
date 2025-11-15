# PRD: Settings Page Replacement (V3.0)

**Version:** 3.0
**Status:** Draft
**Created:** 2025-11-13
**Owner:** Sebastian Ames
**Priority:** P0 (Critical UX fix)

---

## Problem Statement

### Current State

The settings panel has critical visibility issues:

- **Position**: `position: absolute; top: 100%` places it below the quote box
- **Off-Screen**: Panel frequently extends beyond viewport, especially when quote box is centered
- **No Visual Feedback**: User clicks settings cog (⚙️) but sees nothing (panel is off-screen)
- **Confusing UX**: No clear indication that settings are open or where they are

### User Pain Points

1. **Invisible Settings**: User clicks ⚙️ → nothing appears → assumes it's broken
2. **Viewport Issues**: Even when visible, panel is often partially off-screen
3. **No Navigation**: No clear way to "exit" settings and return to quote
4. **Mobile Unusable**: On mobile, settings panel is almost always off-screen

### Impact

- **Critical UX Bug**: Settings are functionally unusable in many scenarios
- **User Frustration**: Feature appears broken
- **Mobile**: Completely unusable on mobile devices
- **Accessibility**: Screen reader users have no clear navigation model

---

## Goals & Success Metrics

### Primary Goals

1. Settings panel is **always visible** when opened (100% viewport compliance)
2. Clear mental model: User is either "viewing quote" OR "in settings" (single view at a time)
3. Clear navigation: Back button returns user to quote view
4. Mobile-friendly: Settings panel works perfectly on all screen sizes

### Success Metrics

- **Visibility**: 100% of settings interactions show panel in viewport
- **Discoverability**: 0% user confusion about where settings are
- **Navigation**: 100% of users understand how to return to quote (back button)
- **Mobile**: Settings panel fully functional on screens as small as 320px

### Non-Goals

- Overlay/modal approach (rejected in favor of page replacement)
- Settings panel as sidebar
- Multiple settings pages (keep single page for simplicity)
- Settings preview while viewing quote (unnecessary complexity)

---

## Requirements

### P0 (Must Have)

#### Page Replacement Behavior

- **REQ-SPR-001**: Clicking ⚙️ (settings button) **hides** the quote box completely
- **REQ-SPR-002**: Clicking ⚙️ **shows** the settings panel in the same position as quote box
- **REQ-SPR-003**: Only one element visible at a time (quote box OR settings panel)
- **REQ-SPR-004**: Settings panel occupies same footprint as quote box (centered, same z-index)

#### Back Button

- **REQ-SPR-005**: Settings panel has a **back button** (← or similar) at top-left
- **REQ-SPR-006**: Back button label: "Back to Quote" (clear affordance)
- **REQ-SPR-007**: Clicking back button **hides** settings panel and **shows** quote box
- **REQ-SPR-008**: Back button is keyboard accessible (Tab, Enter, Space)
- **REQ-SPR-009**: Esc key also closes settings and returns to quote

#### Positioning & Layout

- **REQ-SPR-010**: Settings panel uses `position: fixed` (not absolute)
- **REQ-SPR-011**: Settings panel centered: `top: 50%; left: 50%; transform: translate(-50%, -50%)`
- **REQ-SPR-012**: Settings panel size: `min-width: 400px; max-width: min(600px, 90vw)`
- **REQ-SPR-013**: Settings panel respects `max-height: 80vh` with scrolling for overflow
- **REQ-SPR-014**: Settings panel has same visual styling as quote box (border-radius, shadow, theme support)

#### State Management

- **REQ-SPR-015**: JavaScript tracks settings open/closed state
- **REQ-SPR-016**: Quote box gets `.settings-open` class when settings are open (for hiding)
- **REQ-SPR-017**: Settings panel gets `.show` class when open
- **REQ-SPR-018**: Settings remain open if user interacts with settings controls
- **REQ-SPR-019**: Settings changes persist to localStorage (already implemented)

#### Visual Transitions

- **REQ-SPR-020**: Fade transition (0.3s) when switching between quote and settings
- **REQ-SPR-021**: No slide animation (instant position change, fade only)
- **REQ-SPR-022**: Smooth opacity transition for professional feel

### P1 (Should Have)

- **REQ-SPR-023**: Settings panel has same gradient accent line as quote box
- **REQ-SPR-024**: Back button has hover state for visual feedback
- **REQ-SPR-025**: Settings panel has focus trap (Tab cycles within settings only)
- **REQ-SPR-026**: Accessibility: Screen reader announces "Settings" when opened

### P2 (Nice to Have)

- **REQ-SPR-027**: Settings panel has subtle "page" indicator (e.g., "Settings • 1 of 1")
- **REQ-SPR-028**: Back button has icon (← arrow) for visual clarity
- **REQ-SPR-029**: Settings panel has "Save" button for explicit confirmation (optional, auto-save already works)

---

## Technical Design

### CSS Changes

#### Current Implementation (Broken)

```css
.settings-panel {
  position: absolute;
  top: 100%; /* ← Places below quote box, often off-screen */
  right: 0;
  margin-top: 8px;
  width: 300px;
}
```

#### Proposed Implementation (Page Replacement)

```css
.settings-panel {
  position: fixed; /* Viewport-relative */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* Centered */
  width: fit-content;
  min-width: 400px;
  max-width: min(600px, 90vw); /* Responsive */
  max-height: 80vh;
  background: var(--bg-color);
  border-radius: 12px;
  padding: 24px;
  padding-top: 56px; /* Space for back button */
  box-shadow: var(--shadow);
  opacity: 0;
  pointer-events: none;
  display: none;
  z-index: 1000000; /* Above quote box */
  overflow-y: auto;
}

.settings-panel.show {
  opacity: 1;
  pointer-events: auto;
  display: block;
}

/* Hide quote box when settings are open */
.quote-container.settings-open {
  opacity: 0;
  pointer-events: none;
}
```

### HTML Changes

#### Add Back Button to Settings Panel

```html
<div class="settings-panel" id="settingsPanel">
  <button
    class="back-button"
    id="backButton"
    aria-label="Back to quote"
    title="Back to Quote (Esc)"
  >
    ← Back
  </button>

  <!-- Existing settings controls... -->
  <h3>Settings</h3>
  <div class="setting-group">...</div>
</div>
```

#### Back Button CSS

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
  transition: background 0.2s ease;
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

### JavaScript Changes

#### Current Implementation

```javascript
function toggleSettings() {
  settingsPanel.classList.toggle('show');
}

settingsButton.addEventListener('click', toggleSettings);
```

#### Proposed Implementation

```javascript
let settingsOpen = false;

function openSettings() {
  settingsPanel.classList.add('show');
  container.classList.add('settings-open');
  settingsOpen = true;

  // Accessibility: Announce to screen readers
  settingsPanel.setAttribute('aria-hidden', 'false');
  container.setAttribute('aria-hidden', 'true');

  // Focus back button
  document.getElementById('backButton').focus();
}

function closeSettings() {
  settingsPanel.classList.remove('show');
  container.classList.remove('settings-open');
  settingsOpen = false;

  // Accessibility: Announce to screen readers
  settingsPanel.setAttribute('aria-hidden', 'true');
  container.setAttribute('aria-hidden', 'false');

  // Return focus to settings button
  settingsButton.focus();
}

// Event listeners
settingsButton.addEventListener('click', openSettings);
backButton.addEventListener('click', closeSettings);

// Esc key closes settings
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && settingsOpen) {
    closeSettings();
  }
});
```

### User Flow

```
┌─────────────────────────────────────┐
│ Quote Box (visible)                 │
│ ┌─────────────────────────────────┐ │
│ │ [⚙️] [🌙] [×]                    │ │
│ │ "Quote text here..."            │ │
│ │ — Author                        │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                ↓ Click ⚙️
┌─────────────────────────────────────┐
│ Settings Panel (visible)            │
│ ┌─────────────────────────────────┐ │
│ │ [← Back]                        │ │
│ │ Settings                        │ │
│ │                                 │ │
│ │ ⏱️ Timer Duration: 15s          │ │
│ │ 📍 Position: Bottom Right       │ │
│ │ 🔤 Font Size: Medium            │ │
│ │ 📂 Category: Motivation         │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                ↓ Click ← Back
┌─────────────────────────────────────┐
│ Quote Box (visible again)           │
│ (Settings changes applied)          │
└─────────────────────────────────────┘
```

---

## Testing Plan

### Unit Tests

- [ ] Verify CSS positioning (fixed, centered)
- [ ] Verify min/max width constraints
- [ ] Verify z-index layering
- [ ] Test `.settings-open` class application

### Integration Tests (Playwright)

- [ ] **Test 1**: Click ⚙️ → Settings panel visible, quote box hidden
- [ ] **Test 2**: Click back button → Quote box visible, settings hidden
- [ ] **Test 3**: Press Esc → Quote box visible, settings hidden
- [ ] **Test 4**: Settings panel fully in viewport (all screen sizes)
- [ ] **Test 5**: Settings changes persist after closing panel
- [ ] **Test 6**: Focus management (⚙️ → back button → ⚙️)
- [ ] **Test 7**: Mobile (375px viewport) → Settings panel fits perfectly

### Visual Regression Tests

- [ ] Screenshot: Settings panel in light theme
- [ ] Screenshot: Settings panel in dark theme
- [ ] Screenshot: Transition from quote to settings (opacity fade)
- [ ] Screenshot: Settings panel on mobile

### Accessibility Tests

- [ ] Screen reader announces "Settings" when opened
- [ ] Tab navigation cycles within settings panel
- [ ] Esc key closes settings
- [ ] Focus returns to ⚙️ button after closing
- [ ] ARIA attributes updated correctly

### Manual Testing

- [ ] Test all 4 quote positions (settings should always be centered)
- [ ] Test with long settings panel content (scrolling)
- [ ] Test theme toggle while in settings
- [ ] Test changing all settings, verify they apply to quote
- [ ] Test rapid open/close (no visual glitches)

---

## Rollout Plan

### Phase 1: Development

1. Update CSS for `.settings-panel` (fixed positioning)
2. Add `.settings-open` class CSS for quote box
3. Add back button HTML and CSS
4. Update JavaScript (openSettings, closeSettings functions)
5. Add Esc key listener
6. Add accessibility attributes

### Phase 2: Testing

1. Run Playwright visual tests (7 scenarios)
2. Manual testing (desktop + mobile)
3. Accessibility testing (keyboard, screen reader)
4. Cross-browser testing (Chrome, Firefox, Safari, Edge)

### Phase 3: Deployment

1. Commit changes with descriptive message
2. Update CHANGELOG.md (V3.0 - Settings Page Replacement)
3. Update CLAUDE.md (architectural decision: page replacement)
4. Push to GitHub

### Phase 4: Validation

1. User feedback (GitHub issues)
2. Monitor for edge cases
3. Iterate if needed

---

## Dependencies

### Technical

- No new dependencies (pure HTML/CSS/JS change)
- Requires browser support for `transform: translate()` (✅ all modern browsers)
- Requires browser support for CSS transitions (✅ all modern browsers)

### Design

- Back button icon (← arrow) - using Unicode character (no icon library needed)

### Testing

- Playwright already installed (V2.0.1)
- Accessibility testing tools (axe-core already in package.json)

---

## Open Questions

1. **Should back button be at top-left or top-right?**
   - **Decision**: Top-left. Standard pattern for "back" navigation.

2. **Should settings panel have a title bar with close button?**
   - **Decision**: No. Back button is sufficient. Keep minimal.

3. **Should we add a "Save" button or rely on auto-save?**
   - **Decision**: Auto-save. Settings apply immediately via localStorage.

4. **Should settings panel be dismissible by clicking outside?**
   - **Decision**: No. User must explicitly click back button or press Esc. Prevents accidental closes.

5. **Should timer continue running while in settings?**
   - **Decision**: No. Pause timer when settings open, resume when closed.

---

## Risks & Mitigation

| Risk                                             | Likelihood | Impact | Mitigation                                      |
| ------------------------------------------------ | ---------- | ------ | ----------------------------------------------- |
| User doesn't understand "page replacement" model | Medium     | Medium | Clear back button label, Esc key support        |
| Focus management bugs                            | Medium     | High   | Comprehensive keyboard testing, ARIA attributes |
| Settings panel too wide on mobile                | Low        | Medium | `max-width: 90vw` constraint                    |
| Z-index conflicts with other elements            | Low        | High   | Use high z-index (1000000), test thoroughly     |
| Performance issues with fade transitions         | Low        | Low    | Use GPU-accelerated opacity transitions         |
| User forgets settings are open                   | Low        | Low    | No auto-close, user must explicitly exit        |

---

## Acceptance Criteria

### Definition of Done

- [ ] All P0 requirements implemented and tested
- [ ] Back button functional (click, keyboard, Esc)
- [ ] Settings panel always visible in viewport
- [ ] Quote box hidden when settings open
- [ ] Focus management works correctly
- [ ] Playwright tests pass (7 scenarios)
- [ ] Accessibility tests pass (keyboard, screen reader)
- [ ] Cross-browser testing completed
- [ ] No visual regressions detected
- [ ] Code committed with descriptive message
- [ ] CHANGELOG.md and CLAUDE.md updated

### User Acceptance

- User confirms settings are now always visible
- User confirms back button is intuitive
- User confirms no confusion about navigation
- User confirms mobile experience is good

---

## Related Documents

- `PRD_V3_RESPONSIVE_QUOTE_BOX.md` - Quote box responsive redesign
- `CLAUDE.md` - Development history and lessons learned
- `CHANGELOG.md` - Version history

---

**Status**: Ready for implementation pending user approval
