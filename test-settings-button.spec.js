const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Settings Button Visibility Test', () => {
  test('should debug settings button visibility', async ({ page }) => {
    // Navigate to the HTML file
    const filePath = path.join(__dirname, 'index.html');
    await page.goto(`file://${filePath}`);

    // Wait for the container to be visible
    await page.waitForSelector('.quote-container.show', { timeout: 5000 });

    // Take initial screenshot
    await page.screenshot({ path: 'screenshot-initial.png', fullPage: true });

    // Get all buttons
    const settingsButton = page.locator('#settingsButton');
    const themeToggle = page.locator('#themeToggle');
    const closeButton = page.locator('#closeButton');

    console.log('\n=== BUTTON EXISTENCE CHECK ===');

    // Check if buttons exist in DOM
    const settingsExists = await settingsButton.count() > 0;
    const themeExists = await themeToggle.count() > 0;
    const closeExists = await closeButton.count() > 0;

    console.log('Settings button exists:', settingsExists);
    console.log('Theme toggle exists:', themeExists);
    console.log('Close button exists:', closeExists);

    console.log('\n=== VISIBILITY CHECK ===');

    // Check if buttons are visible
    const settingsVisible = await settingsButton.isVisible().catch(() => false);
    const themeVisible = await themeToggle.isVisible().catch(() => false);
    const closeVisible = await closeButton.isVisible().catch(() => false);

    console.log('Settings button visible:', settingsVisible);
    console.log('Theme toggle visible:', themeVisible);
    console.log('Close button visible:', closeVisible);

    console.log('\n=== COMPUTED STYLES - SETTINGS BUTTON ===');

    // Get computed styles for settings button
    const settingsStyles = await settingsButton.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        display: computed.display,
        visibility: computed.visibility,
        opacity: computed.opacity,
        position: computed.position,
        zIndex: computed.zIndex,
        top: computed.top,
        right: computed.right,
        width: computed.width,
        height: computed.height,
        fontSize: computed.fontSize,
        color: computed.color,
        backgroundColor: computed.backgroundColor,
        pointerEvents: computed.pointerEvents,
        transform: computed.transform,
        overflow: computed.overflow,
      };
    });

    console.log('Settings Button Styles:', JSON.stringify(settingsStyles, null, 2));

    console.log('\n=== COMPUTED STYLES - THEME TOGGLE ===');

    // Get computed styles for theme toggle
    const themeStyles = await themeToggle.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        display: computed.display,
        visibility: computed.visibility,
        opacity: computed.opacity,
        position: computed.position,
        zIndex: computed.zIndex,
        top: computed.top,
        right: computed.right,
        width: computed.width,
        height: computed.height,
        fontSize: computed.fontSize,
        color: computed.color,
        backgroundColor: computed.backgroundColor,
        pointerEvents: computed.pointerEvents,
      };
    });

    console.log('Theme Toggle Styles:', JSON.stringify(themeStyles, null, 2));

    console.log('\n=== COMPUTED STYLES - CLOSE BUTTON ===');

    // Get computed styles for close button
    const closeStyles = await closeButton.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        display: computed.display,
        visibility: computed.visibility,
        opacity: computed.opacity,
        position: computed.position,
        zIndex: computed.zIndex,
        top: computed.top,
        right: computed.right,
        width: computed.width,
        height: computed.height,
        fontSize: computed.fontSize,
        color: computed.color,
        backgroundColor: computed.backgroundColor,
        pointerEvents: computed.pointerEvents,
      };
    });

    console.log('Close Button Styles:', JSON.stringify(closeStyles, null, 2));

    console.log('\n=== BOUNDING BOX CHECK ===');

    // Get bounding boxes
    const settingsBbox = await settingsButton.boundingBox();
    const themeBbox = await themeToggle.boundingBox();
    const closeBbox = await closeButton.boundingBox();

    console.log('Settings button bounding box:', settingsBbox);
    console.log('Theme toggle bounding box:', themeBbox);
    console.log('Close button bounding box:', closeBbox);

    console.log('\n=== CONTAINER STYLES ===');

    // Check container styles
    const containerStyles = await page.locator('.quote-container').evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        position: computed.position,
        width: computed.width,
        height: computed.height,
        overflow: computed.overflow,
        overflowX: computed.overflowX,
        overflowY: computed.overflowY,
        bottom: computed.bottom,
        right: computed.right,
        zIndex: computed.zIndex,
        padding: computed.padding,
      };
    });

    console.log('Container Styles:', JSON.stringify(containerStyles, null, 2));

    console.log('\n=== BUTTON INNER HTML ===');

    // Get button inner HTML to check emoji rendering
    const settingsHTML = await settingsButton.innerHTML();
    const themeHTML = await themeToggle.innerHTML();
    const closeHTML = await closeButton.innerHTML();

    console.log('Settings button HTML:', settingsHTML);
    console.log('Theme toggle HTML:', themeHTML);
    console.log('Close button HTML:', closeHTML);

    console.log('\n=== TEXT CONTENT ===');

    // Get text content
    const settingsText = await settingsButton.textContent();
    const themeText = await themeToggle.textContent();
    const closeText = await closeButton.textContent();

    console.log('Settings button text:', settingsText, '(length:', settingsText.length, ')');
    console.log('Theme toggle text:', themeText, '(length:', themeText.length, ')');
    console.log('Close button text:', closeText, '(length:', closeText.length, ')');

    console.log('\n=== ELEMENT POSITION INFO ===');

    // Get detailed position info
    const positionInfo = await page.evaluate(() => {
      const settings = document.getElementById('settingsButton');
      const theme = document.getElementById('themeToggle');
      const close = document.getElementById('closeButton');
      const container = document.querySelector('.quote-container');

      return {
        settings: {
          offsetTop: settings.offsetTop,
          offsetLeft: settings.offsetLeft,
          offsetWidth: settings.offsetWidth,
          offsetHeight: settings.offsetHeight,
          clientTop: settings.clientTop,
          clientLeft: settings.clientLeft,
          clientWidth: settings.clientWidth,
          clientHeight: settings.clientHeight,
        },
        theme: {
          offsetTop: theme.offsetTop,
          offsetLeft: theme.offsetLeft,
          offsetWidth: theme.offsetWidth,
          offsetHeight: theme.offsetHeight,
        },
        close: {
          offsetTop: close.offsetTop,
          offsetLeft: close.offsetLeft,
          offsetWidth: close.offsetWidth,
          offsetHeight: close.offsetHeight,
        },
        container: {
          offsetWidth: container.offsetWidth,
          offsetHeight: container.offsetHeight,
          scrollWidth: container.scrollWidth,
          scrollHeight: container.scrollHeight,
          clientWidth: container.clientWidth,
          clientHeight: container.clientHeight,
        }
      };
    });

    console.log('Position Info:', JSON.stringify(positionInfo, null, 2));

    console.log('\n=== CHECKING FOR OVERLAPPING ELEMENTS ===');

    // Check if anything is covering the buttons
    const elementsAtSettingsButton = await page.evaluate(() => {
      const settings = document.getElementById('settingsButton');
      const rect = settings.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      const elementsAtPoint = document.elementsFromPoint(centerX, centerY);
      return elementsAtPoint.map(el => ({
        tagName: el.tagName,
        id: el.id,
        className: el.className,
      }));
    });

    console.log('Elements at settings button center:', JSON.stringify(elementsAtSettingsButton, null, 2));

    // Highlight buttons for visual debugging
    await page.evaluate(() => {
      const settings = document.getElementById('settingsButton');
      const theme = document.getElementById('themeToggle');
      const close = document.getElementById('closeButton');

      settings.style.outline = '3px solid red';
      theme.style.outline = '3px solid blue';
      close.style.outline = '3px solid green';
    });

    // Take screenshot with outlines
    await page.screenshot({ path: 'screenshot-with-outlines.png', fullPage: true });

    console.log('\n=== ATTEMPTING TO CLICK SETTINGS BUTTON ===');

    // Try to click settings button
    try {
      await settingsButton.click({ timeout: 2000 });
      console.log('Settings button clicked successfully!');

      // Check if settings panel opened
      await page.waitForTimeout(500);
      const panelVisible = await page.locator('#settingsPanel.show').isVisible();
      console.log('Settings panel visible after click:', panelVisible);

      // Take screenshot after click
      await page.screenshot({ path: 'screenshot-after-click.png', fullPage: true });
    } catch (error) {
      console.log('Failed to click settings button:', error.message);
    }

    console.log('\n=== FONT RENDERING CHECK ===');

    // Check if emoji fonts are rendering
    const fontCheck = await page.evaluate(() => {
      const settings = document.getElementById('settingsButton');
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      ctx.font = '20px "Segoe UI", Tahoma, Geneva, Verdana, sans-serif';
      const metrics = ctx.measureText('⚙️');

      return {
        emojiWidth: metrics.width,
        canvasSupported: !!ctx,
      };
    });

    console.log('Font rendering info:', fontCheck);

    console.log('\n=== TEST COMPLETE ===');
    console.log('Screenshots saved:');
    console.log('  - screenshot-initial.png');
    console.log('  - screenshot-with-outlines.png');
    console.log('  - screenshot-after-click.png (if click succeeded)');
  });
});
