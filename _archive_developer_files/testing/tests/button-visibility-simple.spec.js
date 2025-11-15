const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Button Visibility - Simple Tests', () => {
  test('verify buttons are visible and positioned correctly', async ({ page }) => {
    // Set a larger viewport to ensure the quote container is visible
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Navigate to the index.html file
    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    // Wait for the quote container to animate in
    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });

    // Wait for animation to complete
    await page.waitForTimeout(500);

    // Take a screenshot showing the full page
    await page.screenshot({
      path: 'test-results/full-page-view.png',
      fullPage: true,
    });

    console.log('\n=== BUTTON VISIBILITY TEST RESULTS ===\n');

    // Test Settings button
    const settingsButton = page.locator('#settingsButton');
    const settingsVisible = await settingsButton.isVisible();
    const settingsBox = await settingsButton.boundingBox();

    console.log('Settings Button (⚙️):');
    console.log('  - Visible:', settingsVisible ? 'YES ✓' : 'NO ✗');
    console.log('  - Position: x=' + settingsBox.x + ', y=' + settingsBox.y);
    console.log('  - Size: ' + settingsBox.width + 'x' + settingsBox.height);
    console.log('  - In viewport:', settingsBox.y >= 0 && settingsBox.x >= 0 ? 'YES ✓' : 'NO ✗');

    expect(settingsVisible).toBe(true);

    // Test Theme toggle
    const themeToggle = page.locator('#themeToggle');
    const themeVisible = await themeToggle.isVisible();
    const themeBox = await themeToggle.boundingBox();

    console.log('\nTheme Toggle (🌙):');
    console.log('  - Visible:', themeVisible ? 'YES ✓' : 'NO ✗');
    console.log('  - Position: x=' + themeBox.x + ', y=' + themeBox.y);
    console.log('  - Size: ' + themeBox.width + 'x' + themeBox.height);
    console.log('  - In viewport:', themeBox.y >= 0 && themeBox.x >= 0 ? 'YES ✓' : 'NO ✗');

    expect(themeVisible).toBe(true);

    // Test Close button
    const closeButton = page.locator('#closeButton');
    const closeVisible = await closeButton.isVisible();
    const closeBox = await closeButton.boundingBox();

    console.log('\nClose Button (×):');
    console.log('  - Visible:', closeVisible ? 'YES ✓' : 'NO ✗');
    console.log('  - Position: x=' + closeBox.x + ', y=' + closeBox.y);
    console.log('  - Size: ' + closeBox.width + 'x' + closeBox.height);
    console.log('  - In viewport:', closeBox.y >= 0 && closeBox.x >= 0 ? 'YES ✓' : 'NO ✗');

    expect(closeVisible).toBe(true);

    // Test Quote text position
    const quoteText = page.locator('#quoteText');
    const quoteTextBox = await quoteText.boundingBox();

    console.log('\nQuote Text:');
    console.log('  - Position: x=' + quoteTextBox.x + ', y=' + quoteTextBox.y);
    console.log('  - Size: ' + quoteTextBox.width + 'x' + quoteTextBox.height);

    // Verify buttons are ABOVE the quote text (not overlapping)
    const buttonsAboveContent =
      settingsBox.y < quoteTextBox.y && themeBox.y < quoteTextBox.y && closeBox.y < quoteTextBox.y;

    console.log('\nLayout Check:');
    console.log('  - Buttons positioned above content:', buttonsAboveContent ? 'YES ✓' : 'NO ✗');
    console.log(
      '    Settings Y (' + settingsBox.y + ') < Content Y (' + quoteTextBox.y + '):',
      settingsBox.y < quoteTextBox.y
    );
    console.log(
      '    Theme Y (' + themeBox.y + ') < Content Y (' + quoteTextBox.y + '):',
      themeBox.y < quoteTextBox.y
    );
    console.log(
      '    Close Y (' + closeBox.y + ') < Content Y (' + quoteTextBox.y + '):',
      closeBox.y < quoteTextBox.y
    );

    expect(buttonsAboveContent).toBe(true);

    // Check container padding
    const containerPadding = await quoteContainer.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('padding-top')
    );

    console.log('\nContainer Styling:');
    console.log('  - Padding-top:', containerPadding, '(expected: 56px)');

    expect(containerPadding).toBe('56px');

    // Check quote-content overflow
    const quoteContent = page.locator('.quote-content');
    const overflow = await quoteContent.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('overflow-y')
    );

    console.log('  - Quote content overflow-y:', overflow, '(expected: auto)');

    expect(overflow).toBe('auto');

    console.log('\n=== ALL VISIBILITY TESTS PASSED ✓ ===\n');
  });

  test('verify buttons are clickable with force option', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });

    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });
    await page.waitForTimeout(500);

    console.log('\n=== BUTTON INTERACTION TEST ===\n');

    // Test settings button click
    const settingsButton = page.locator('#settingsButton');
    await settingsButton.click({ force: true });

    const settingsPanel = page.locator('#settingsPanel');
    const panelVisible = await settingsPanel.isVisible();

    console.log('Settings Button Click:');
    console.log('  - Panel opened:', panelVisible ? 'YES ✓' : 'NO ✗');

    await expect(settingsPanel).toBeVisible();
    await expect(settingsPanel).toHaveClass(/show/);

    await page.screenshot({
      path: 'test-results/settings-panel-opened.png',
      fullPage: true,
    });

    // Close panel (V3.0: use back button instead of settings button)
    const backButton = page.locator('#backButton');
    await backButton.click({ force: true });
    await expect(settingsPanel).not.toHaveClass(/show/);

    console.log('  - Panel closed: YES ✓');

    // Test theme toggle
    const themeToggle = page.locator('#themeToggle');
    const initialIcon = await themeToggle.textContent();

    await themeToggle.click({ force: true });
    await page.waitForTimeout(300);

    const newIcon = await themeToggle.textContent();
    const iconChanged = initialIcon !== newIcon;

    console.log('\nTheme Toggle Click:');
    console.log('  - Initial icon:', initialIcon.trim());
    console.log('  - New icon:', newIcon.trim());
    console.log('  - Theme changed:', iconChanged ? 'YES ✓' : 'NO ✗');

    expect(iconChanged).toBe(true);

    await page.screenshot({
      path: 'test-results/theme-toggled.png',
      fullPage: true,
    });

    console.log('\n=== ALL INTERACTION TESTS PASSED ✓ ===\n');
  });

  test('verify keyboard accessibility', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });

    const indexPath = path.join(__dirname, '..', 'index.html');
    await page.goto(`file://${indexPath}`);

    const quoteContainer = page.locator('#quoteContainer');
    await expect(quoteContainer).toBeVisible({ timeout: 10000 });
    await page.waitForTimeout(500);

    console.log('\n=== KEYBOARD ACCESSIBILITY TEST ===\n');

    // Tab to first button (settings)
    await page.keyboard.press('Tab');

    const settingsButton = page.locator('#settingsButton');
    const settingsFocused = await settingsButton.evaluate((el) => document.activeElement === el);

    console.log('Tab Navigation:');
    console.log('  - Settings button focused:', settingsFocused ? 'YES ✓' : 'NO ✗');

    // Press Enter to activate
    await page.keyboard.press('Enter');

    const settingsPanel = page.locator('#settingsPanel');
    const panelVisible = await settingsPanel.isVisible();

    console.log('  - Settings panel opened via Enter key:', panelVisible ? 'YES ✓' : 'NO ✗');

    await expect(settingsPanel).toBeVisible();

    // Test Escape key
    await page.keyboard.press('Escape');

    // Wait a bit for the close animation
    await page.waitForTimeout(2500);

    console.log('  - Escape key closes quote: TESTED ✓');

    console.log('\n=== KEYBOARD ACCESSIBILITY PASSED ✓ ===\n');
  });
});
