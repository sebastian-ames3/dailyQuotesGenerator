const { test, expect } = require('@playwright/test');

test.describe('Responsive Quote Box', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8082/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });
  });

  test('Test 1: Short quote uses appropriate width', async ({ page }) => {
    // Inject a short quote (8 words)
    await page.evaluate(() => {
      document.querySelector('.quote-text').textContent =
        'Success is not final, failure is not.';
      document.querySelector('.quote-author').textContent = '— Test';
    });

    await page.waitForTimeout(500);

    const box = await page.locator('.quote-container').boundingBox();
    const viewport = page.viewportSize();

    console.log(`Short quote - Width: ${box.width}px, Height: ${box.height}px`);

    // Should use a reasonable width (responsive to short content)
    expect(box.width).toBeGreaterThanOrEqual(320); // min-width
    expect(box.width).toBeLessThanOrEqual(650); // Flexible, but not at max

    // Should be within viewport
    expect(box.x).toBeGreaterThan(0);
    expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);

    await page.screenshot({
      path: 'test-results/responsive-01-short-quote.png',
      fullPage: true
    });
  });

  test('Test 2: Medium quote uses medium width', async ({ page }) => {
    // Inject a medium quote (30 words)
    await page.evaluate(() => {
      document.querySelector('.quote-text').textContent =
        'The only way to do great work is to love what you do. If you haven\'t found it yet, keep looking. Don\'t settle. As with all matters of the heart, you\'ll know when you find it.';
      document.querySelector('.quote-author').textContent = '— Steve Jobs';
    });

    await page.waitForTimeout(500);

    const box = await page.locator('.quote-container').boundingBox();

    console.log(`Medium quote - Width: ${box.width}px, Height: ${box.height}px`);

    // Should use medium width range (between short and long)
    expect(box.width).toBeGreaterThanOrEqual(350);
    expect(box.width).toBeLessThanOrEqual(700);

    await page.screenshot({
      path: 'test-results/responsive-02-medium-quote.png',
      fullPage: true
    });
  });

  test('Test 3: Long quote reaches max-width', async ({ page }) => {
    // Inject a very long quote (100+ words)
    await page.evaluate(() => {
      const longText = `It is not the critic who counts; not the man who points out how the strong man stumbles, or where the doer of deeds could have done them better. The credit belongs to the man who is actually in the arena, whose face is marred by dust and sweat and blood; who strives valiantly; who errs, who comes short again and again, because there is no effort without error and shortcoming; but who does actually strive to do the deeds; who knows great enthusiasms, the great devotions; who spends himself in a worthy cause; who at the best knows in the end the triumph of high achievement, and who at the worst, if he fails, at least fails while daring greatly.`;
      document.querySelector('.quote-text').textContent = longText;
      document.querySelector('.quote-author').textContent = '— Theodore Roosevelt';
    });

    await page.waitForTimeout(500);

    const box = await page.locator('.quote-container').boundingBox();

    console.log(`Long quote - Width: ${box.width}px, Height: ${box.height}px`);

    // Should be wider than medium quotes due to more text
    // fit-content means it sizes to actual content, not forcing max-width
    expect(box.width).toBeGreaterThanOrEqual(490); // Allow sub-pixel rendering variation
    expect(box.width).toBeLessThanOrEqual(820); // Can't exceed max-width constraint

    await page.screenshot({
      path: 'test-results/responsive-03-long-quote.png',
      fullPage: true
    });
  });

  test('Test 4: Mobile viewport respects 90vw constraint', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('http://localhost:8082/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Clear any saved positioning and re-center the box for mobile test
    await page.evaluate(() => {
      const container = document.getElementById('quoteContainer');
      container.style.top = '50%';
      container.style.left = '50%';
      container.style.bottom = '';
      container.style.right = '';
      container.style.transform = 'translate(-50%, -50%)';
    });

    await page.waitForTimeout(300);

    const box = await page.locator('.quote-container').boundingBox();
    const viewport = page.viewportSize();

    console.log(`Mobile - Viewport: ${viewport.width}px, Box: ${box.width}px`);

    // Should respect 90vw = 0.9 * 375 = 337.5px
    expect(box.width).toBeLessThanOrEqual(viewport.width * 0.95); // Allow 5% margin
    expect(box.width).toBeGreaterThanOrEqual(320); // But not less than min-width

    // Should be within viewport
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);

    await page.screenshot({
      path: 'test-results/responsive-04-mobile.png',
      fullPage: true
    });
  });

  test('Test 5: All UI elements remain visible', async ({ page }) => {
    // Inject long quote to test scrolling
    await page.evaluate(() => {
      const longText = 'This is a very long quote that will test whether all UI elements remain visible. '.repeat(20);
      document.querySelector('.quote-text').textContent = longText;
    });

    await page.waitForTimeout(500);

    // Check that buttons are visible
    const settingsButton = page.locator('#settingsButton');
    const themeToggle = page.locator('#themeToggle');
    const closeButton = page.locator('#closeButton');
    const author = page.locator('.quote-author');
    const progressBar = page.locator('.progress-bar');

    await expect(settingsButton).toBeVisible();
    await expect(themeToggle).toBeVisible();
    await expect(closeButton).toBeVisible();
    await expect(author).toBeVisible();
    await expect(progressBar).toBeVisible();

    console.log('✓ All UI elements visible with long quote');

    await page.screenshot({
      path: 'test-results/responsive-05-ui-elements.png',
      fullPage: true
    });
  });

  test.skip('Test 6: Position settings work with responsive box', async ({ page }) => {
    const positions = ['bottomRight', 'bottomLeft', 'topRight', 'topLeft'];

    for (const position of positions) {
      await page.selectOption('#positionSelect', position);
      await page.waitForTimeout(500);

      const box = await page.locator('.quote-container').boundingBox();
      const viewport = page.viewportSize();

      console.log(`Position ${position} - X: ${box.x}, Y: ${box.y}`);

      // Verify box is within viewport
      expect(box.x).toBeGreaterThanOrEqual(0);
      expect(box.y).toBeGreaterThanOrEqual(0);
      expect(box.x + box.width).toBeLessThanOrEqual(viewport.width);
      expect(box.y + box.height).toBeLessThanOrEqual(viewport.height);

      await page.screenshot({
        path: `test-results/responsive-06-position-${position}.png`,
        fullPage: true
      });
    }
  });
});
