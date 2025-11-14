const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Button Visibility Tests', () => {
  test('all buttons should be visible and clickable', async ({ page }) => {
    // Navigate to the index.html file
    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    // Wait for the quote container to be visible
    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });

    // Take an initial screenshot
    await page.screenshot({
      path: 'test-results/initial-state.png',
      fullPage: true
    });

    // Test 1: Settings button (⚙️)
    const settingsButton = page.locator('#settingsButton');
    await expect(settingsButton).toBeVisible();
    await expect(settingsButton).toBeEnabled();

    // Check if button is in viewport
    const settingsBox = await settingsButton.boundingBox();
    expect(settingsBox).not.toBeNull();
    expect(settingsBox.y).toBeGreaterThanOrEqual(0);
    expect(settingsBox.x).toBeGreaterThanOrEqual(0);

    console.log('Settings button position:', settingsBox);

    // Test 2: Theme toggle (🌙)
    const themeToggle = page.locator('#themeToggle');
    await expect(themeToggle).toBeVisible();
    await expect(themeToggle).toBeEnabled();

    const themeBox = await themeToggle.boundingBox();
    expect(themeBox).not.toBeNull();
    expect(themeBox.y).toBeGreaterThanOrEqual(0);
    expect(themeBox.x).toBeGreaterThanOrEqual(0);

    console.log('Theme toggle position:', themeBox);

    // Test 3: Close button (×)
    const closeButton = page.locator('#closeButton');
    await expect(closeButton).toBeVisible();
    await expect(closeButton).toBeEnabled();

    const closeBox = await closeButton.boundingBox();
    expect(closeBox).not.toBeNull();
    expect(closeBox.y).toBeGreaterThanOrEqual(0);
    expect(closeBox.x).toBeGreaterThanOrEqual(0);

    console.log('Close button position:', closeBox);

    // Take screenshot with annotations showing button positions
    await page.screenshot({
      path: 'test-results/buttons-visible.png',
      fullPage: true
    });

    // Test 4: Verify buttons are not overlapping with content
    const quoteText = page.locator('#quoteText');
    const quoteTextBox = await quoteText.boundingBox();

    console.log('Quote text position:', quoteTextBox);

    // Buttons should be above the quote text (lower y value)
    expect(settingsBox.y).toBeLessThan(quoteTextBox.y);
    expect(themeBox.y).toBeLessThan(quoteTextBox.y);
    expect(closeBox.y).toBeLessThan(quoteTextBox.y);

    // Test 5: Click settings button to verify it opens the panel
    await settingsButton.click();

    // Wait for settings panel to appear
    const settingsPanel = page.locator('#settingsPanel');
    await expect(settingsPanel).toHaveClass(/show/);
    await expect(settingsPanel).toBeVisible();

    // Take screenshot with settings panel open
    await page.screenshot({
      path: 'test-results/settings-panel-open.png',
      fullPage: true
    });

    console.log('Settings panel opened successfully');

    // Test 6: Verify settings panel has expected controls
    await expect(page.locator('#timerSlider')).toBeVisible();
    await expect(page.locator('#positionSelect')).toBeVisible();
    await expect(page.locator('#fontSizeSelect')).toBeVisible();
    await expect(page.locator('#categorySelect')).toBeVisible();

    // Test 7: Close settings panel using back button (V3.0 behavior)
    const backButton = page.locator('#backButton');
    await backButton.click();
    await expect(settingsPanel).not.toHaveClass(/show/);

    console.log('Settings panel closed successfully');

    // Test 8: Test theme toggle functionality
    const initialThemeIcon = await themeToggle.textContent();
    console.log('Initial theme icon:', initialThemeIcon);

    await themeToggle.click();

    // Wait a bit for theme transition
    await page.waitForTimeout(500);

    const newThemeIcon = await themeToggle.textContent();
    console.log('New theme icon:', newThemeIcon);

    // Icon should change from moon to sun or vice versa
    expect(initialThemeIcon).not.toBe(newThemeIcon);

    // Take screenshot in different theme
    await page.screenshot({
      path: 'test-results/theme-toggled.png',
      fullPage: true
    });

    // Test 9: Verify all buttons are still clickable after interactions
    await expect(settingsButton).toBeEnabled();
    await expect(themeToggle).toBeEnabled();
    await expect(closeButton).toBeEnabled();

    console.log('All button visibility and functionality tests passed!');
  });

  test('buttons should be accessible with keyboard navigation', async ({ page }) => {
    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });

    // Tab to settings button
    await page.keyboard.press('Tab');
    const settingsButton = page.locator('#settingsButton');
    await expect(settingsButton).toBeFocused();

    // Press Enter to open settings
    await page.keyboard.press('Enter');
    const settingsPanel = page.locator('#settingsPanel');
    await expect(settingsPanel).toHaveClass(/show/);

    console.log('Keyboard navigation test passed!');
  });

  test('buttons should have proper z-index and not be hidden by content', async ({ page }) => {
    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });

    // Check z-index values
    const settingsButton = page.locator('#settingsButton');
    const zIndex = await settingsButton.evaluate(el =>
      window.getComputedStyle(el).getPropertyValue('z-index')
    );

    console.log('Settings button z-index:', zIndex);
    expect(parseInt(zIndex)).toBeGreaterThanOrEqual(10);

    // Verify buttons are positioned absolutely
    const position = await settingsButton.evaluate(el =>
      window.getComputedStyle(el).getPropertyValue('position')
    );

    console.log('Settings button position style:', position);
    expect(position).toBe('absolute');

    console.log('Z-index test passed!');
  });

  test('container padding should provide space for buttons', async ({ page }) => {
    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });

    // Check padding-top value
    const paddingTop = await quoteContainer.evaluate(el =>
      window.getComputedStyle(el).getPropertyValue('padding-top')
    );

    console.log('Container padding-top:', paddingTop);

    // Should be 56px as per the changes
    expect(paddingTop).toBe('56px');

    // Check that quote-content has overflow
    const quoteContent = page.locator('.quote-content');
    const overflow = await quoteContent.evaluate(el =>
      window.getComputedStyle(el).getPropertyValue('overflow-y')
    );

    console.log('Quote content overflow-y:', overflow);
    expect(overflow).toBe('auto');

    console.log('Container padding test passed!');
  });
});
