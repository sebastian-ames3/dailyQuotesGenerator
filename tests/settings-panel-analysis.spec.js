const { test, expect } = require('@playwright/test');

test.describe('Settings Panel and Quote Box Analysis', () => {
  test('should capture current settings panel behavior', async ({ page }) => {
    // Start local server and navigate
    await page.goto('http://localhost:8080/index.html');

    // Wait for quote to appear
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Take screenshot of initial state
    await page.screenshot({
      path: 'test-results/01-initial-quote.png',
      fullPage: true
    });

    // Get quote box dimensions
    const quoteBox = await page.locator('.quote-container').boundingBox();
    console.log('Quote box dimensions:', quoteBox);

    // Click settings button
    await page.click('#settings-button');

    // Wait for settings panel
    await page.waitForSelector('#settings-panel', { state: 'visible', timeout: 5000 });

    // Take screenshot with settings panel open
    await page.screenshot({
      path: 'test-results/02-settings-panel-open.png',
      fullPage: true
    });

    // Get settings panel dimensions and position
    const settingsPanel = await page.locator('#settings-panel').boundingBox();
    console.log('Settings panel dimensions:', settingsPanel);

    // Check viewport
    const viewportSize = page.viewportSize();
    console.log('Viewport size:', viewportSize);

    // Check if settings panel is visible in viewport
    const isSettingsInViewport = settingsPanel.y + settingsPanel.height <= viewportSize.height;
    console.log('Settings panel fully in viewport?', isSettingsInViewport);

    // Check quote text length
    const quoteText = await page.locator('.quote-text').textContent();
    const wordCount = quoteText.trim().split(/\s+/).length;
    console.log('Quote word count:', wordCount);
    console.log('Quote text:', quoteText.substring(0, 100) + '...');
  });

  test('should test with short quote (force fallback)', async ({ page }) => {
    // Intercept API to force fallback quotes
    await page.route('**/dummyjson.com/**', route => route.abort());

    await page.goto('http://localhost:8080/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Take screenshot
    await page.screenshot({
      path: 'test-results/03-short-quote.png',
      fullPage: true
    });

    const quoteText = await page.locator('.quote-text').textContent();
    const quoteBox = await page.locator('.quote-container').boundingBox();
    console.log('Short quote dimensions:', quoteBox);
    console.log('Short quote words:', quoteText.trim().split(/\s+/).length);
  });

  test('should test settings panel at different positions', async ({ page }) => {
    await page.goto('http://localhost:8080/index.html');
    await page.waitForSelector('.quote-container', { timeout: 10000 });

    // Open settings
    await page.click('#settings-button');
    await page.waitForSelector('#settings-panel', { state: 'visible' });

    // Try different positions
    const positions = ['bottomRight', 'bottomLeft', 'topRight', 'topLeft'];

    for (const position of positions) {
      // Select position
      await page.selectOption('#position-select', position);
      await page.waitForTimeout(500);

      // Take screenshot
      await page.screenshot({
        path: `test-results/04-position-${position}.png`,
        fullPage: true
      });

      const quoteBox = await page.locator('.quote-container').boundingBox();
      const settingsPanel = await page.locator('#settings-panel').boundingBox();
      console.log(`Position ${position}:`, {
        quote: quoteBox,
        settings: settingsPanel
      });
    }
  });

  test('should analyze quote box with various quote lengths', async ({ page }) => {
    await page.goto('http://localhost:8080/index.html');

    // Inject custom quotes of different lengths
    await page.evaluate(() => {
      const testQuotes = [
        { text: 'Short quote here.', author: 'Test 1' },
        { text: 'This is a medium length quote that has about twenty words to see how the box responds to it.', author: 'Test 2' },
        { text: 'This is a very long quote that contains many words and should test the boundaries of the quote box to see if it scales appropriately. We want to see if the container expands to fit the content or if it causes overflow issues that might push other elements off screen. This is important for user experience.', author: 'Test 3' }
      ];

      // Store in window for later access
      window.testQuotes = testQuotes;
    });

    // Test each quote length
    for (let i = 0; i < 3; i++) {
      await page.evaluate((index) => {
        const quote = window.testQuotes[index];
        document.querySelector('.quote-text').textContent = quote.text;
        document.querySelector('.quote-author').textContent = `— ${quote.author}`;
      }, i);

      await page.waitForTimeout(500);

      await page.screenshot({
        path: `test-results/05-quote-length-${i + 1}.png`,
        fullPage: true
      });

      const quoteBox = await page.locator('.quote-container').boundingBox();
      const quoteText = await page.locator('.quote-text').textContent();
      console.log(`Quote ${i + 1} (${quoteText.split(/\s+/).length} words):`, quoteBox);
    }
  });
});
