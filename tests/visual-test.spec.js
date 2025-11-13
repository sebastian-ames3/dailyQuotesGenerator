const { test, expect } = require('@playwright/test');
const path = require('path');

test('visual verification - capture quote with visible buttons', async ({ page }) => {
  // Set viewport to standard desktop size
  await page.setViewportSize({ width: 1280, height: 720 });

  const indexPath = path.join(__dirname, '..', 'index.html');
  await page.goto(`file://${indexPath}`);

  // Wait for quote container to be visible
  const quoteContainer = page.locator('#quoteContainer');
  await expect(quoteContainer).toBeVisible({ timeout: 10000 });

  // Wait for slide-in animation to complete
  await page.waitForTimeout(600);

  // Get the bounding box to create a focused screenshot
  const containerBox = await quoteContainer.boundingBox();

  // Take a screenshot of just the quote container area
  await page.screenshot({
    path: 'test-results/quote-container-close-up.png',
    clip: {
      x: Math.max(0, containerBox.x - 50),
      y: Math.max(0, containerBox.y - 50),
      width: Math.min(containerBox.width + 100, 600),
      height: Math.min(containerBox.height + 100, 400)
    }
  });

  // Highlight the buttons by hovering over them
  await page.locator('#settingsButton').hover();
  await page.waitForTimeout(200);

  await page.screenshot({
    path: 'test-results/settings-button-hover.png',
    clip: {
      x: Math.max(0, containerBox.x - 50),
      y: Math.max(0, containerBox.y - 50),
      width: Math.min(containerBox.width + 100, 600),
      height: Math.min(containerBox.height + 100, 400)
    }
  });

  console.log('Visual test screenshots saved to test-results/');
  console.log('- quote-container-close-up.png');
  console.log('- settings-button-hover.png');
});
