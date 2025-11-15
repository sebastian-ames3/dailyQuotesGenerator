# Product Requirements Document (PRD) - V5.0.0

## Advanced Visual Design with Pillow

**Version:** 5.0.0
**Status:** Planning
**Target Date:** TBD
**Priority:** High - User Experience Enhancement

---

## Executive Summary

Transform the Python overlay from basic Tkinter styling to a modern, polished UI with rounded corners, gradient backgrounds, drop shadows, and smooth animations using the Pillow (PIL) library.

**Goal:** Create a visually impressive, app-like experience while maintaining the lightweight, frameless overlay architecture.

---

## Current State (V4.0.1)

**What Works:**
- ✅ Functional settings, theme toggle, all features working
- ✅ Text-based buttons (no emoji issues)
- ✅ Clean but basic design
- ✅ Light/dark theme support

**Limitations:**
- ❌ No rounded corners (rectangular window)
- ❌ Flat colors (no gradients)
- ❌ No shadows or depth
- ❌ Basic button styling
- ❌ Instant transitions (no animations)
- ❌ Limited visual polish

---

## User Requirements

From user feedback:
> "can we adjust the color of the background and text... something different but still simple is nice"
> "is this the extent of how detailed we can design a python script overlay?"
> **Decision:** "i think option b is best" (Advanced design with Pillow)

**User Expectations:**
1. Fresh, modern color scheme
2. More visually polished than current design
3. Still simple and clean (not overwhelming)
4. Maintain fast startup and lightweight feel
5. Run automatically on Windows sign-in

---

## Success Criteria

- [ ] Window has rounded corners (12-16px radius)
- [ ] Gradient backgrounds (subtle, not garish)
- [ ] Drop shadow effect for depth
- [ ] Modern button styling with hover effects
- [ ] Smooth fade-in/fade-out animations
- [ ] New color scheme implemented
- [ ] Startup time remains under 1 second
- [ ] All existing features still work
- [ ] No visual glitches or artifacts
- [ ] Works on Windows 10/11

---

## Technical Requirements

### Dependencies
- **New:** Pillow (PIL Fork) - `pip install Pillow`
- **Existing:** tkinter, requests, json, os

### Compatibility
- Python 3.7+
- Windows 10/11
- Screen resolutions: 1920x1080 and higher

---

## Feature Breakdown

### Phase 1: Setup & Infrastructure
**Priority:** Critical - Foundation for all visual enhancements

**Tasks:**
1. Add Pillow to requirements.txt
2. Create `requirements.txt` file:
   ```
   requests>=2.28.0
   Pillow>=10.0.0
   ```
3. Update README with installation instructions
4. Create utility module for PIL helper functions
5. Test Pillow installation on Windows

**Acceptance Criteria:**
- Pillow installs without errors
- Can import PIL and ImageDraw
- No conflicts with existing tkinter code

---

### Phase 2: Rounded Corners
**Priority:** High - Most noticeable visual improvement

**Implementation Approach:**
1. Create rounded rectangle mask using PIL
2. Apply mask to window using `wm_attributes`
3. Handle window transparency (`-alpha`)
4. Ensure mask updates when window resizes

**Technical Details:**
```python
def create_rounded_rectangle(width, height, radius, color):
    """Create a rounded rectangle image using PIL"""
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=color
    )
    return image
```

**Challenges:**
- Tkinter doesn't natively support shaped windows on all platforms
- May need to use layered window approach
- Transparency handling varies by Windows version

**Acceptance Criteria:**
- Window has 12px rounded corners
- No jagged edges or artifacts
- Rounded corners work in both light/dark themes
- Window shadow doesn't clip at corners

---

### Phase 3: Gradient Backgrounds
**Priority:** Medium - Visual polish

**Implementation:**
1. Create gradient image using PIL
2. Convert to PhotoImage for Tkinter
3. Set as Label background
4. Support multiple gradient directions:
   - Vertical (top to bottom)
   - Horizontal (left to right)
   - Diagonal (135°)
   - Radial (center outward)

**Color Scheme Options:**

**Selected:** Ocean Breeze (User to confirm)
- Light gradient: #f0f4f8 → #e0e7ff
- Dark gradient: #0f172a → #1e293b
- Accent: #0891b2 (cyan/teal)

**Alternative Schemes Available:**
- Warm Minimalist (amber/brown)
- Forest Green (emerald)
- Monochrome Modern (black/white)
- Sunset Gradient (orange/purple)

**Acceptance Criteria:**
- Smooth gradient (no color banding)
- Gradient updates when theme switches
- Performance impact < 50ms startup time
- Gradient doesn't interfere with text readability

---

### Phase 4: Drop Shadow Effect
**Priority:** Medium - Adds depth and separation

**Implementation:**
1. Create shadow layer using PIL Gaussian blur
2. Position shadow offset (x=0, y=4px)
3. Blur radius: 20px
4. Shadow opacity: 15-25%
5. Layer behind main window

**Technical Approach:**
- Use PIL ImageFilter.GaussianBlur
- Create semi-transparent shadow image
- Composite shadow + window
- Update shadow when window moves (may be performance-intensive)

**Performance Consideration:**
- Pre-render shadow at common window sizes (320px, 500px, 800px)
- Cache shadow images
- Only regenerate when window size changes significantly

**Acceptance Criteria:**
- Subtle shadow visible on light backgrounds
- Shadow doesn't appear on dark backgrounds (looks muddy)
- No performance lag when moving window
- Shadow updates correctly when window resizes

---

### Phase 5: Modern Button Design
**Priority:** High - User interaction polish

**Enhancements:**
1. Replace text buttons with icon buttons:
   - Settings: ⚙ icon (SVG rendered to image)
   - Theme: 🌙/☀ icon (custom designed, no emoji)
   - Close: × icon (larger, clearer)

2. Button hover effects:
   - Smooth color transition (200ms)
   - Slight scale increase (105%)
   - Cursor change (hand pointer)

3. Button states:
   - Normal: Semi-transparent background
   - Hover: Solid accent color
   - Active: Slightly darker
   - Disabled: Grayed out

**Icon Creation:**
- Use PIL to draw simple geometric icons
- 24x24px at 2x resolution (48x48 actual)
- Monochrome with theme-aware colors

**Acceptance Criteria:**
- Icons are crisp and clear
- Hover animations are smooth
- Icons work in both themes
- No delay when hovering
- Icons scale properly on high-DPI displays

---

### Phase 6: Smooth Animations
**Priority:** Low - Nice-to-have polish

**Animation Types:**

1. **Fade In (on startup):**
   - Duration: 300ms
   - Easing: ease-out
   - Alpha: 0.0 → 0.96
   - Current: Already exists (make smoother)

2. **Fade Out (on close):**
   - Duration: 200ms
   - Easing: ease-in
   - Alpha: 0.96 → 0.0
   - Current: Already exists (make smoother)

3. **Settings Panel Slide:**
   - Duration: 250ms
   - Easing: ease-in-out
   - Transform: translate Y(-20px, opacity 0) → (0px, opacity 1)

4. **Theme Switch:**
   - Duration: 300ms
   - Cross-fade between themes
   - Update all colors smoothly

**Implementation:**
- Use `after()` method for frame timing
- 60 FPS target (16ms per frame)
- Easing functions: custom or use `numpy` if available

**Performance Budget:**
- Each animation frame < 16ms
- Total animation overhead < 100ms

**Acceptance Criteria:**
- Animations feel natural, not jarring
- No stutter or frame drops
- User can interrupt animations
- Animations don't delay critical actions

---

### Phase 7: Color Scheme Implementation
**Priority:** High - User-requested change

**Selected Scheme: Ocean Breeze** (pending user confirmation)

**Light Theme:**
```python
OCEAN_LIGHT = {
    'bg_primary': '#f0f4f8',      # Main background
    'bg_secondary': '#e0e7ff',    # Gradient end
    'text_primary': '#1a365d',    # Quote text
    'text_secondary': '#4a5568',  # Author
    'text_hint': '#94a3b8',       # Hint text
    'accent': '#0891b2',          # Buttons, accent line
    'accent_hover': '#0e7490',    # Button hover
    'close_hover': '#ef4444',     # Close button hover
    'border': '#cbd5e1',          # Subtle borders
    'shadow': 'rgba(15, 23, 42, 0.1)'  # Drop shadow
}
```

**Dark Theme:**
```python
OCEAN_DARK = {
    'bg_primary': '#0f172a',      # Main background
    'bg_secondary': '#1e293b',    # Gradient end
    'text_primary': '#e2e8f0',    # Quote text
    'text_secondary': '#94a3b8',  # Author
    'text_hint': '#64748b',       # Hint text
    'accent': '#06b6d4',          # Buttons, accent line
    'accent_hover': '#0891b2',    # Button hover
    'close_hover': '#ef4444',     # Close button hover
    'border': '#334155',          # Subtle borders
    'shadow': 'rgba(0, 0, 0, 0.4)'  # Drop shadow
}
```

**Implementation:**
1. Replace existing THEMES dictionary
2. Update all widget references
3. Test readability (WCAG AA compliance)
4. Ensure gradient blends smoothly

**Acceptance Criteria:**
- All text is readable (contrast ratio ≥ 4.5:1)
- Colors feel cohesive, not random
- Accent color stands out but doesn't overwhelm
- Theme toggle works smoothly
- User can optionally select other color schemes in settings

---

## Testing Plan

### Manual Testing
1. **Visual Inspection:**
   - [ ] Rounded corners are smooth
   - [ ] Gradients are subtle and pleasant
   - [ ] Shadow adds depth without being distracting
   - [ ] Buttons are clearly interactive
   - [ ] Animations are smooth (60 FPS)

2. **Functionality Testing:**
   - [ ] All V4.0.1 features still work
   - [ ] Settings panel opens/closes
   - [ ] Theme toggle updates all colors
   - [ ] Timer works correctly
   - [ ] Hover-to-pause still functions
   - [ ] Window positions correctly (all 4 corners)
   - [ ] Responsive sizing still works

3. **Performance Testing:**
   - [ ] Startup time < 1 second
   - [ ] Memory usage < 100MB
   - [ ] CPU usage < 5% when idle
   - [ ] No lag when hovering buttons
   - [ ] Animations don't stutter

4. **Cross-Environment Testing:**
   - [ ] Works on Windows 10
   - [ ] Works on Windows 11
   - [ ] Works on 1920x1080 display
   - [ ] Works on 4K display
   - [ ] Works with 100% scaling
   - [ ] Works with 150% scaling (high DPI)

### Automated Testing (Optional)
- Screenshot comparison tests
- Performance benchmarks
- Memory leak detection

---

## Implementation Timeline

**Estimated Duration:** 4-6 hours of focused work

**Phase Order:**
1. Phase 1: Setup (30 min)
2. Phase 7: Color Scheme (1 hour) - Quick win for user
3. Phase 2: Rounded Corners (1.5 hours) - Most impactful
4. Phase 3: Gradients (1 hour)
5. Phase 5: Modern Buttons (1 hour)
6. Phase 4: Drop Shadow (1 hour) - Optional, time permitting
7. Phase 6: Animations (1 hour) - Optional, polish

**Minimum Viable Product (MVP):**
- Phase 1, 2, 7 (Setup, Rounded Corners, Color Scheme)
- Estimated: 3 hours

**Full Feature Set:**
- All phases
- Estimated: 6 hours

---

## Risks & Mitigation

### Risk 1: Performance Degradation
**Impact:** Medium
**Likelihood:** Medium
**Mitigation:**
- Pre-render and cache images
- Use lightweight gradients
- Profile performance at each phase
- Have rollback plan if too slow

### Risk 2: Pillow Installation Issues
**Impact:** High
**Likelihood:** Low
**Mitigation:**
- Clear installation instructions
- Bundle Pillow with installer (future)
- Graceful fallback to basic design if Pillow missing

### Risk 3: Rounded Corners Don't Work on All Systems
**Impact:** Medium
**Likelihood:** Low
**Mitigation:**
- Test on multiple Windows versions
- Fallback to square corners if shaped windows unsupported
- Document known limitations

### Risk 4: Breaking Existing Features
**Impact:** High
**Likelihood:** Low
**Mitigation:**
- Thorough testing after each phase
- Git commits after each working phase
- Keep V4.0.1 as backup branch

---

## Open Questions

1. **Color Scheme:** User needs to confirm Ocean Breeze or select alternative
2. **Shadow Preference:** Should dark theme have shadow? (Looks muddy on dark backgrounds)
3. **Animation Speed:** Prefer subtle/slow or snappy/fast?
4. **Icon Style:** Outlined or filled icons?
5. **Gradient Direction:** Vertical, horizontal, or diagonal?

---

## Future Enhancements (Post-V5.0.0)

**V5.1.0 - User Customization:**
- Color picker in settings
- Custom gradient direction
- Adjustable corner radius
- Shadow intensity slider

**V5.2.0 - Advanced Effects:**
- Glassmorphism (frosted glass blur)
- Particle effects on quote change
- Animated background patterns
- Custom fonts (Google Fonts integration)

**V6.0.0 - Cross-Platform:**
- macOS support (Notification Center style)
- Linux support (GNOME/KDE integration)
- Unified codebase with platform-specific theming

---

## Documentation Updates Required

**Files to Update:**
1. `README.md` - Add Pillow installation
2. `CLAUDE.md` - Add V5.0.0 section
3. `CHANGELOG.md` - Create if doesn't exist
4. `BUTTON_DESIGN.md` - Update with new icon buttons
5. `requirements.txt` - Create with Pillow dependency

**New Files:**
1. `INSTALLATION.md` - Detailed setup guide
2. `DESIGN_SYSTEM.md` - Color schemes, spacing, typography

---

## Success Metrics

**User Satisfaction:**
- Visual appeal: "Wow" reaction vs "meh"
- Daily usage: Continues to use vs disables

**Technical Metrics:**
- Startup time: < 1 second
- Memory footprint: < 100MB
- Animation FPS: 60 (no drops)
- Zero crashes or visual glitches

**Code Quality:**
- Code coverage: > 80% (if we add tests)
- No performance regressions
- Clean separation of concerns (UI vs logic)

---

## Sign-off

**Created:** 2025-11-14
**Author:** Claude (AI Assistant)
**Status:** Awaiting user approval and color scheme selection
**Next Step:** User confirms approach, selects color scheme, then implementation begins in fresh session

---

## Appendix A: Pillow Capabilities Reference

**What Pillow Can Do:**
- ✅ Create images from scratch (RGBA, RGB)
- ✅ Draw shapes (rectangles, circles, polygons)
- ✅ Apply filters (blur, sharpen, enhance)
- ✅ Create gradients (linear, radial)
- ✅ Composite images (layering, alpha blending)
- ✅ Draw text with custom fonts
- ✅ Resize/rotate/transform images
- ✅ Export to various formats (PNG, JPEG, etc.)

**What Pillow Cannot Do:**
- ❌ Native Tkinter widget styling (still need Tkinter for UI)
- ❌ Hardware acceleration (all CPU-based)
- ❌ Real-time video/complex animations (too slow)
- ❌ Vector graphics (raster only)

**Performance Characteristics:**
- Image creation: ~5-10ms for 800x200 image
- Gradient generation: ~10-20ms
- Gaussian blur: ~50-100ms (expensive!)
- Composite operations: ~5-10ms

**Optimization Tips:**
- Pre-render static images at startup
- Cache images aggressively
- Use smallest necessary image sizes
- Avoid blur if possible (very expensive)

---

## Appendix B: Alternative Color Schemes (Full Specs)

See `COLOR_SCHEMES.md` for complete specifications of all 5 options:
1. Ocean Breeze (Recommended)
2. Warm Minimalist
3. Forest Green
4. Monochrome Modern
5. Sunset Gradient

---

**End of PRD**
