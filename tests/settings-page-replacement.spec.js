const { test, expect } = require('@playwright/test');

test.describe('Settings Page Replacement', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8081/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });
  });

  test('Test 1: Settings panel replaces quote box', async ({ page }) => {
    // Initial state: quote visible, settings hidden
    const quoteBox = page.locator('.quote-container');
    const settingsPanel = page.locator('.settings-panel');

    await expect(quoteBox).toBeVisible();
    await expect(settingsPanel).not.toBeVisible();

    console.log('✓ Initial state: Quote visible, settings hidden');

    // Click settings button
    await page.click('#settingsButton');
    await page.waitForTimeout(500);

    // Settings visible, quote hidden
    await expect(settingsPanel).toBeVisible();
    await expect(quoteBox).toHaveClass(/settings-open/);

    console.log('✓ After opening: Settings visible, quote has settings-open class');

    // Take screenshot
    await page.screenshot({
      path: 'test-results/settings-01-panel-open.png',
      fullPage: true,
    });
  });

  test('Test 2: Back button closes settings', async ({ page }) => {
    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    const settingsPanel = page.locator('.settings-panel');
    const quoteBox = page.locator('.quote-container');

    await expect(settingsPanel).toBeVisible();

    // Click back button
    await page.click('#backButton');
    await page.waitForTimeout(300);

    // Quote visible, settings hidden
    await expect(quoteBox).toBeVisible();
    await expect(quoteBox).not.toHaveClass(/settings-open/);
    await expect(settingsPanel).not.toBeVisible();

    console.log('✓ Back button closes settings and shows quote');

    await page.screenshot({
      path: 'test-results/settings-02-back-button.png',
      fullPage: true,
    });
  });

  test('Test 3: Esc key closes settings', async ({ page }) => {
    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    const settingsPanel = page.locator('.settings-panel');
    const quoteBox = page.locator('.quote-container');

    await expect(settingsPanel).toBeVisible();

    // Press Esc
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);

    // Quote visible, settings hidden
    await expect(quoteBox).toBeVisible();
    await expect(quoteBox).not.toHaveClass(/settings-open/);
    await expect(settingsPanel).not.toBeVisible();

    console.log('✓ Esc key closes settings');

    await page.screenshot({
      path: 'test-results/settings-03-esc-key.png',
      fullPage: true,
    });
  });

  test('Test 4: Settings panel always in viewport', async ({ page }) => {
    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    const settingsBox = await page.locator('.settings-panel').boundingBox();
    const viewport = page.viewportSize();

    console.log(
      `Settings panel: x=${settingsBox.x}, y=${settingsBox.y}, w=${settingsBox.width}, h=${settingsBox.height}`
    );
    console.log(`Viewport: w=${viewport.width}, h=${viewport.height}`);

    // Verify panel is within viewport
    expect(settingsBox.x).toBeGreaterThanOrEqual(0);
    expect(settingsBox.y).toBeGreaterThanOrEqual(0);
    expect(settingsBox.x + settingsBox.width).toBeLessThanOrEqual(viewport.width);
    expect(settingsBox.y + settingsBox.height).toBeLessThanOrEqual(viewport.height);

    console.log('✓ Settings panel fully in viewport');

    await page.screenshot({
      path: 'test-results/settings-04-viewport.png',
      fullPage: true,
    });
  });

  test('Test 5: Focus management', async ({ page }) => {
    // Initial focus
    const settingsButton = page.locator('#settingsButton');

    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    // Focus should be on back button
    const backButton = page.locator('#backButton');
    await expect(backButton).toBeFocused();

    console.log('✓ Back button receives focus when settings open');

    // Close settings
    await page.click('#backButton');
    await page.waitForTimeout(300);

    // Focus should return to settings button
    await expect(settingsButton).toBeFocused();

    console.log('✓ Settings button receives focus when settings close');

    await page.screenshot({
      path: 'test-results/settings-05-focus.png',
      fullPage: true,
    });
  });

  test('Test 6: Mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('http://localhost:8081/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Clear any saved positioning
    await page.evaluate(() => {
      localStorage.clear();
    });

    // Reload to apply defaults
    await page.reload();
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    const settingsBox = await page.locator('.settings-panel').boundingBox();
    const viewport = page.viewportSize();

    console.log(`Mobile - Viewport: ${viewport.width}px, Settings: ${settingsBox.width}px`);

    // Settings panel should respect min-width: 320px and max-width: 90vw
    // On 375px viewport: 90vw = 337.5px
    expect(settingsBox.width).toBeGreaterThanOrEqual(319); // Allow sub-pixel rendering
    expect(settingsBox.width).toBeLessThanOrEqual(viewport.width * 0.92); // Allow small margin

    // Should be within viewport
    expect(settingsBox.x).toBeGreaterThanOrEqual(0);
    expect(settingsBox.x + settingsBox.width).toBeLessThanOrEqual(viewport.width);

    console.log('✓ Settings panel fits mobile viewport');

    await page.screenshot({
      path: 'test-results/settings-06-mobile.png',
      fullPage: true,
    });
  });

  test('Test 7: Settings changes persist', async ({ page }) => {
    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    // Change timer duration (range slider - use fill)
    await page.fill('#timerSlider', '30');
    await page.waitForTimeout(200);

    // Change font size
    await page.selectOption('#fontSizeSelect', 'large');
    await page.waitForTimeout(200);

    console.log('✓ Settings changed');

    // Close settings
    await page.click('#backButton');
    await page.waitForTimeout(300);

    // Verify settings applied to quote box
    const quoteText = page.locator('.quote-text');
    const fontSize = await quoteText.evaluate((el) => window.getComputedStyle(el).fontSize);

    console.log(`Font size after settings: ${fontSize}`);
    expect(fontSize).toBe('20px'); // Large font size

    console.log('✓ Settings changes applied to quote');

    await page.screenshot({
      path: 'test-results/settings-07-persist.png',
      fullPage: true,
    });
  });

  test('Test 8: ARIA attributes', async ({ page }) => {
    const settingsPanel = page.locator('.settings-panel');
    const quoteBox = page.locator('.quote-container');

    // Initial ARIA state
    let settingsAriaHidden = await settingsPanel.getAttribute('aria-hidden');
    let quoteAriaHidden = await quoteBox.getAttribute('aria-hidden');

    console.log(`Initial ARIA - Settings: ${settingsAriaHidden}, Quote: ${quoteAriaHidden}`);

    // Open settings
    await page.click('#settingsButton');
    await page.waitForTimeout(300);

    // Check ARIA after opening
    settingsAriaHidden = await settingsPanel.getAttribute('aria-hidden');
    quoteAriaHidden = await quoteBox.getAttribute('aria-hidden');

    console.log(`After open ARIA - Settings: ${settingsAriaHidden}, Quote: ${quoteAriaHidden}`);

    expect(settingsAriaHidden).toBe('false');
    expect(quoteAriaHidden).toBe('true');

    // Close settings
    await page.click('#backButton');
    await page.waitForTimeout(300);

    // Check ARIA after closing
    settingsAriaHidden = await settingsPanel.getAttribute('aria-hidden');
    quoteAriaHidden = await quoteBox.getAttribute('aria-hidden');

    console.log(`After close ARIA - Settings: ${settingsAriaHidden}, Quote: ${quoteAriaHidden}`);

    expect(settingsAriaHidden).toBe('true');
    expect(quoteAriaHidden).toBe('false');

    console.log('✓ ARIA attributes updated correctly');

    await page.screenshot({
      path: 'test-results/settings-08-aria.png',
      fullPage: true,
    });
  });
});
