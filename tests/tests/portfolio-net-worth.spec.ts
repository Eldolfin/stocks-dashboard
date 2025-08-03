import { test, expect } from '@playwright/test';
import path from 'path';

test('Portfolio net worth over time feature', async ({ page }) => {
  const email = `test-user-networth-${test.info().workerIndex}-${Date.now()}@a.a`;
  const password = "test";

  // First register and login
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
  
  // Verify the portfolio page loads
  await expect(page.getByText('Step 1:')).toBeVisible();
  await expect(page.getByText('Download excel report from Etoro')).toBeVisible();
  await expect(page.getByText('Step 2:')).toBeVisible();
  await expect(page.getByText('Upload file')).toBeVisible();

  // Upload the test Excel file
  const testFilePath = path.join(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await page.locator('#etoro-excel').setInputFiles(testFilePath);

  // Wait for the analysis to complete
  await expect(page.locator('.animate-spin')).toBeVisible();
  await expect(page.locator('.animate-spin')).not.toBeVisible({ timeout: 30000 });

  // Check that both views are available
  await expect(page.getByText('Profit Analysis')).toBeVisible();
  await expect(page.getByText('Net Worth Over Time')).toBeVisible();

  // Initial view should be profit analysis (default)
  await expect(page.locator('canvas')).toBeVisible(); // Chart should be visible

  // Switch to net worth view
  await page.getByText('Net Worth Over Time').click();
  
  // Verify the net worth chart is displayed
  await expect(page.locator('canvas')).toBeVisible();
  
  // Check that the chart title indicates it's net worth
  // The chart should now show a line chart instead of bar chart
  
  // Switch back to profit view
  await page.getByText('Profit Analysis').click();
  await expect(page.locator('canvas')).toBeVisible();

  // Test precision slider
  const precisionSlider = page.locator('#precision-range');
  await expect(precisionSlider).toBeVisible();
  
  // Change precision and verify it updates
  await precisionSlider.fill('0'); // Year precision
  await expect(page.getByText('Year')).toBeVisible();
  
  await precisionSlider.fill('2'); // Day precision  
  await expect(page.getByText('Day')).toBeVisible();

  // Test the net worth view with different precision
  await page.getByText('Net Worth Over Time').click();
  await expect(page.locator('canvas')).toBeVisible();
});

test('Portfolio net worth with previously uploaded reports', async ({ page }) => {
  const email = `test-user-existing-${test.info().workerIndex}-${Date.now()}@a.a`;
  const password = "test";

  // Register and login (same as above)
  await page.goto('/');
  await page.getByRole('link', { name: '📝' }).click();

  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();

  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();

  // Upload a file first
  await page.goto('/portfolio');
  const testFilePath = path.join(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await page.locator('#etoro-excel').setInputFiles(testFilePath);
  
  // Wait for analysis
  await expect(page.locator('.animate-spin')).not.toBeVisible({ timeout: 30000 });

  // Refresh the page to simulate coming back later
  await page.reload();

  // Check that previously uploaded reports section appears
  await expect(page.getByText('Previously Uploaded Reports:')).toBeVisible();
  
  // Click on the uploaded report
  const reportLink = page.locator('button').filter({ hasText: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' });
  await expect(reportLink).toBeVisible();
  await reportLink.click();

  // Wait for re-analysis
  await expect(page.locator('.animate-spin')).not.toBeVisible({ timeout: 30000 });

  // Verify both views work with the re-analyzed data
  await expect(page.getByText('Net Worth Over Time')).toBeVisible();
  await page.getByText('Net Worth Over Time').click();
  await expect(page.locator('canvas')).toBeVisible();
});