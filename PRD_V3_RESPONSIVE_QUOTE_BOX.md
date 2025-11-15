# PRD: Responsive Quote Box (V3.0)

**Version:** 3.0
**Status:** Draft
**Created:** 2025-11-13
**Owner:** Sebastian Ames
**Priority:** P0 (Critical UX improvement)

---

## Problem Statement

### Current State

The quote box has a fixed width of `500px`, which creates several UX issues:

- Short quotes (10-15 words) appear cramped with excessive whitespace
- Long quotes (50+ words) feel compressed and harder to read
- The box doesn't reflect the content it contains
- Visual imbalance between quote length and container size

### User Pain Points

1. **Visual Inefficiency**: Short quotes waste screen space, long quotes feel crowded
2. **Reading Experience**: Fixed width doesn't optimize readability for varying content lengths
3. **Aesthetic**: The box doesn't feel "smart" or adaptive to content

### Impact

- **User Experience**: Poor visual hierarchy and readability
- **Design Quality**: Appears static and unpolished
- **Accessibility**: Sub-optimal reading experience for different quote lengths

---

## Goals & Success Metrics

### Primary Goals

1. Quote box dynamically adapts width and height based on quote content
2. Maintain readability across all quote lengths (5-200 words)
3. Ensure box always fits within viewport constraints
4. Smooth, imperceptible transitions when quotes change

### Success Metrics

- **Responsiveness**: Box width/height adjusts to 100% of tested quote lengths (5, 20, 50, 100+ words)
- **Viewport Compliance**: 0% of quotes cause overflow or off-screen rendering
- **Visual Balance**: User testing confirms improved aesthetics (subjective)
- **Performance**: Resize calculations complete in <50ms

### Non-Goals

- Tiered/preset sizing (we want fully dynamic)
- Animated resize transitions (would be distracting)
- Custom user-defined dimensions
- Different layouts for different quote types

---

## Requirements

### P0 (Must Have)

#### Responsive Width

- **REQ-RQB-001**: Box width must be `fit-content` (auto-adjusts to text)
- **REQ-RQB-002**: Minimum width: `320px` (ensures UI elements don't overlap)
- **REQ-RQB-003**: Maximum width: `min(800px, 90vw)` (readable line length + viewport constraint)
- **REQ-RQB-004**: Width adjusts instantly when new quote loads

#### Responsive Height

- **REQ-RQB-005**: Height must auto-adjust to content (no fixed height)
- **REQ-RQB-006**: Minimum height: `180px` (ensures buttons + progress bar visible)
- **REQ-RQB-007**: Maximum height: `80vh` (prevents overflow, enables scrolling if needed)
- **REQ-RQB-008**: Vertical overflow triggers scrolling in `.quote-content` only

#### Layout Integrity

- **REQ-RQB-009**: Buttons (⚙️, 🌙, ×) remain fixed at top regardless of quote length
- **REQ-RQB-010**: Author citation remains visible at bottom
- **REQ-RQB-011**: Progress bar remains visible at bottom
- **REQ-RQB-012**: Gradient accent line remains at top

#### Position Consistency

- **REQ-RQB-013**: Box remains centered when width/height changes
- **REQ-RQB-014**: Corner positioning (bottomRight, topLeft, etc.) still works
- **REQ-RQB-015**: Box never extends beyond viewport boundaries

### P1 (Should Have)

- **REQ-RQB-016**: Mobile responsive (handles small screens gracefully)
- **REQ-RQB-017**: Handles edge cases (empty quotes, extremely long quotes)
- **REQ-RQB-018**: Maintains aspect ratio for visual harmony

### P2 (Nice to Have)

- **REQ-RQB-019**: Smooth fade transition when quote changes (opacity only, not size)
- **REQ-RQB-020**: Accessibility: Screen reader announces size changes
- **REQ-RQB-021**: Performance: Debounce resize calculations if needed

---

## Technical Design

### CSS Changes

#### Current Implementation (Fixed Width)

```css
.quote-container {
  width: 500px;
  max-width: 90vw;
  min-height: 180px;
  max-height: 80vh;
}
```

#### Proposed Implementation (Responsive)

```css
.quote-container {
  width: fit-content; /* Auto-adjusts to content */
  min-width: 320px; /* Prevent too narrow */
  max-width: min(800px, 90vw); /* Readable + viewport constraint */
  min-height: 180px; /* Ensure UI elements visible */
  max-height: 80vh; /* Prevent viewport overflow */
}
```

### Layout Structure

```
┌─────────────────────────────────────┐
│ .quote-container (fit-content)      │
│ ┌─────────────────────────────────┐ │
│ │ Buttons: ⚙️ 🌙 ×                 │ │ ← Fixed position
│ ├─────────────────────────────────┤ │
│ │ .quote-content (scrollable)     │ │ ← Grows with content
│ │   .quote-text (dynamic)         │ │
│ │   .quote-author                 │ │
│ └─────────────────────────────────┘ │
│ Progress bar                        │ ← Fixed at bottom
└─────────────────────────────────────┘
```

### Constraints

- `min-width: 320px` → Ensures buttons don't overlap (need ~120px for 3 buttons + spacing)
- `max-width: 800px` → Optimal reading line length (60-80 characters per line)
- `max-width: 90vw` → Mobile constraint (10% padding on sides)
- `max-height: 80vh` → Ensures box doesn't exceed viewport, enables scrolling

### Edge Cases

1. **Very short quotes (5-10 words)**: Box shrinks to `min-width: 320px`
2. **Very long quotes (200+ words)**: Box grows to `max-width: 800px`, enables vertical scrolling
3. **Mobile screens (<400px)**: Box respects `90vw` constraint
4. **Multi-line author names**: Included in height calculation
5. **Font size changes**: Box recalculates based on new font size

---

## Testing Plan

### Unit Tests

- [ ] Verify CSS properties applied correctly
- [ ] Test `fit-content` in all major browsers (Chrome, Firefox, Safari, Edge)
- [ ] Verify min/max constraints enforced

### Integration Tests (Playwright)

- [ ] **Test 1**: Short quote (10 words) → Box width < 500px
- [ ] **Test 2**: Medium quote (30 words) → Box width ≈ 500-600px
- [ ] **Test 3**: Long quote (80 words) → Box width = 800px (max)
- [ ] **Test 4**: Very long quote (200 words) → Vertical scrolling enabled
- [ ] **Test 5**: Mobile viewport (375px) → Box respects 90vw constraint
- [ ] **Test 6**: Position changes (4 corners) → Box stays in viewport

### Visual Regression Tests

- [ ] Screenshot comparison before/after for each quote length
- [ ] Verify buttons remain visible and positioned correctly
- [ ] Verify progress bar and author remain at bottom

### Manual Testing

- [ ] Load 20 random quotes, verify visual balance
- [ ] Test all font sizes (small/medium/large)
- [ ] Test light and dark themes
- [ ] Test all position settings (4 corners)
- [ ] Test with screen reader (announce quote changes)

---

## Rollout Plan

### Phase 1: Development

1. Update `.quote-container` CSS with responsive properties
2. Test locally with various quote lengths
3. Verify layout integrity (buttons, author, progress bar)

### Phase 2: Testing

1. Run Playwright visual tests
2. Manual testing on desktop (Chrome, Firefox, Edge)
3. Mobile testing (Chrome DevTools + physical device)

### Phase 3: Deployment

1. Commit changes with descriptive message
2. Update CHANGELOG.md with V3.0 notes
3. Update CLAUDE.md with design decisions
4. Push to GitHub

### Phase 4: Validation

1. Monitor for user feedback (GitHub issues)
2. Check for edge case reports
3. Iterate if needed

---

## Dependencies

### Technical

- No new dependencies (pure CSS change)
- Requires browser support for `fit-content` (✅ all modern browsers)
- Requires browser support for `min()` function (✅ all modern browsers)

### Design

- None (uses existing design system)

### Testing

- Playwright already installed (V2.0.1)
- Test scripts need creation/update

---

## Open Questions

1. **Should we add subtle resize animation?**
   - **Decision**: No. Instant resize is cleaner and less distracting.

2. **What about quotes with unusual formatting (bullet points, line breaks)?**
   - **Decision**: Out of scope for V3.0. API quotes are plain text. Handle in future if needed.

3. **Should max-width be configurable in settings?**
   - **Decision**: No. Keep settings simple. 800px is optimal for readability.

4. **What if quote + author exceeds 80vh on mobile?**
   - **Decision**: Scrolling is acceptable. Happens rarely with curated quotes.

---

## Risks & Mitigation

| Risk                                            | Likelihood | Impact | Mitigation                                   |
| ----------------------------------------------- | ---------- | ------ | -------------------------------------------- |
| Browser compatibility issues with `fit-content` | Low        | High   | Test in all major browsers, provide fallback |
| Box too wide on ultrawide monitors              | Medium     | Low    | `max-width: 800px` caps it at readable width |
| Performance issues with dynamic resizing        | Low        | Medium | Profile with Playwright, optimize if needed  |
| Visual instability when quotes change           | Medium     | Medium | Use opacity transition, not size animation   |
| Scrolling UX confusion for long quotes          | Low        | Low    | Subtle scrollbar styling, test with users    |

---

## Acceptance Criteria

### Definition of Done

- [x] CSS updated with responsive properties
- [ ] All P0 requirements implemented and tested
- [ ] Playwright tests pass (5 quote length scenarios)
- [ ] Manual testing completed (all browsers, mobile)
- [ ] No visual regressions detected
- [ ] Buttons, author, progress bar remain visible in all scenarios
- [ ] Box stays within viewport for all quote lengths and positions
- [ ] Code committed with descriptive message
- [ ] CHANGELOG.md and CLAUDE.md updated

### User Acceptance

- User confirms improved visual balance across quote lengths
- User confirms no layout issues observed
- User confirms smooth experience across devices

---

## Related Documents

- `PRD_V3_SETTINGS_PAGE_REPLACEMENT.md` - Settings panel redesign
- `CLAUDE.md` - Development history and lessons learned
- `CHANGELOG.md` - Version history

---

**Status**: Ready for implementation pending user approval
