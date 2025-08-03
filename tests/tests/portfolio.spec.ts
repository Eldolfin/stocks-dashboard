import { test, expect } from '@playwright/test';
import path from 'path';

test('net worth display from Excel upload', async ({ page }) => {
  const email = `test-user-${test.info().workerIndex}-${Date.now()}@a.a`;
  const password = "test";

  // Register and login first
  await page.goto('/');
  await page.getByRole('link', { name: '📝' }).click();

  // Register
  await page.getByRole('textbox', { name: 'Your email' }).click();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).click();
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();

  // Login
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();
  await page.getByRole('textbox', { name: 'Your email' }).click();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).click();
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();

  // Navigate to portfolio page
  await page.goto('/portfolio');

  // Verify initial state - should show upload interface
  await expect(page.getByText('Step 1:')).toBeVisible();
  await expect(page.getByText('Step 2:')).toBeVisible();
  await expect(page.getByText('Upload file')).toBeVisible();

  // Upload the test Excel file
  const testFilePath = path.join(__dirname, '..', 'data', 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  const fileInput = page.locator('#etoro-excel');
  await fileInput.setInputFiles(testFilePath);

  // Wait for the upload to complete and charts to render
  await expect(page.locator('canvas')).toBeVisible({ timeout: 10000 });

  // Should now show both charts
  // Check for Net Worth chart title
  await expect(page.getByText('Net Worth Over Time')).toBeVisible();
  
  // Check for profit chart (existing functionality should still work)
  // The profit chart doesn't have a visible title, but should have canvas elements
  const canvases = page.locator('canvas');
  await expect(canvases).toHaveCount(2); // Should have 2 charts now: net worth + profit

  // Test precision slider
  const precisionSlider = page.locator('#precision-range');
  await expect(precisionSlider).toBeVisible();
  
  // Change precision and verify charts update
  await precisionSlider.fill('0'); // Year precision
  await expect(page.getByText('Year')).toBeVisible();
  
  await precisionSlider.fill('2'); // Day precision  
  await expect(page.getByText('Day')).toBeVisible();

  // Verify the charts are still present after precision change
  await expect(canvases).toHaveCount(2);
  await expect(page.getByText('Net Worth Over Time')).toBeVisible();
});

test('net worth functionality with saved reports', async ({ page }) => {
  const email = `test-user-${test.info().workerIndex}-${Date.now()}@a.a`;
  const password = "test";

  // Register and login
  await page.goto('/');
  await page.getByRole('link', { name: '📝' }).click();

  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();

  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();

  await page.goto('/portfolio');

  // Upload a file first
  const testFilePath = path.join(__dirname, '..', 'data', 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await page.locator('#etoro-excel').setInputFiles(testFilePath);
  
  // Wait for upload to complete
  await expect(page.locator('canvas')).toBeVisible({ timeout: 10000 });

  // Should now show "Previously Uploaded Reports" section
  await expect(page.getByText('Previously Uploaded Reports:')).toBeVisible();
  
  // Should see the uploaded file in the list
  const reportButton = page.getByRole('button').filter({ hasText: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' });
  await expect(reportButton).toBeVisible();

  // Click on the saved report to re-analyze
  await reportButton.click();

  // Verify charts are still displayed
  await expect(page.locator('canvas')).toHaveCount(2);
  await expect(page.getByText('Net Worth Over Time')).toBeVisible();
});