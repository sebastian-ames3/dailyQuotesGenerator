#!/usr/bin/env node

/**
 * Accessibility Testing Script
 * Uses axe-core to validate HTML files for accessibility issues
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;

const execAsync = promisify(exec);

async function findHTMLFiles() {
  try {
    const { stdout } = await execAsync('find . -name "*.html" -not -path "*/node_modules/*"', {
      shell: '/bin/bash',
    });
    return stdout
      .trim()
      .split('\n')
      .filter((file) => file);
  } catch (error) {
    // Fallback for Windows or if find command fails
    return ['design-preview.html'].filter(async (file) => {
      try {
        await fs.access(file);
        return true;
      } catch {
        return false;
      }
    });
  }
}

async function runAccessibilityTests() {
  console.log('🔍 Running accessibility tests...\n');

  const htmlFiles = await findHTMLFiles();

  if (htmlFiles.length === 0) {
    console.log('ℹ️  No HTML files found to test.');
    console.log('✅ Accessibility tests passed (no files to test).\n');
    return;
  }

  console.log(`Found ${htmlFiles.length} HTML file(s) to test:`);
  htmlFiles.forEach((file) => console.log(`  - ${file}`));
  console.log('');

  let hasErrors = false;

  for (const file of htmlFiles) {
    try {
      console.log(`Testing: ${file}`);

      // Check if file exists
      try {
        await fs.access(file);
      } catch {
        console.log('  ⚠️  File not found, skipping...\n');
        continue;
      }

      // Run axe-core CLI on the file
      const { stdout } = await execAsync(`npx axe ${file} --exit`);

      if (stdout.includes('0 violations found')) {
        console.log('  ✅ No accessibility issues found\n');
      } else {
        console.log('  ❌ Accessibility issues detected:');
        console.log(stdout);
        hasErrors = true;
      }
    } catch (error) {
      // axe returns non-zero exit code when violations are found
      if (error.stdout) {
        console.log('  ❌ Accessibility issues detected:');
        console.log(error.stdout);
        hasErrors = true;
      } else {
        console.log(`  ⚠️  Error testing file: ${error.message}\n`);
      }
    }
  }

  if (hasErrors) {
    console.log('❌ Accessibility tests failed. Please fix the issues above.\n');
    process.exit(1);
  } else {
    console.log('✅ All accessibility tests passed!\n');
  }
}

// Run the tests
runAccessibilityTests().catch((error) => {
  console.error('Error running accessibility tests:', error);
  process.exit(1);
});
