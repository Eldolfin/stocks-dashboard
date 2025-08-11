import { test } from './fixtures/auth';
import { test as baseTest, expect } from '@playwright/test';
import * as path from 'path';

test('upload etoro excel and calculate net worth', async ({ loggedInPage }) => {
  test.setTimeout(180_000);
  // Navigate to portfolio page
  await loggedInPage.getByRole('link', { name: 'Portfolio' }).click();
  await loggedInPage.waitForURL('/portfolio');
  await expect(loggedInPage.getByRole('button', { name: 'Upload file' })).toBeVisible();

  // Upload the Excel file
  const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await loggedInPage.setInputFiles('input[type="file"]', filePath);

  await loggedInPage.getByRole('button', { name: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' }).click();

  await loggedInPage.waitForLoadState("networkidle");

  await expect(loggedInPage.locator('canvas').nth(0)).toBeVisible();
  await expect(loggedInPage.locator('canvas').nth(1)).toBeVisible({timeout: 60_000});

  // Click on the uploaded report name to go to analysis page
  await loggedInPage.getByRole('button', { name: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' }).click();
  await loggedInPage.waitForLoadState("networkidle");

  // Wait for analysis charts to load first
  await expect(loggedInPage.locator('canvas').nth(0)).toBeVisible({timeout: 60_000});
  await expect(loggedInPage.locator('canvas').nth(1)).toBeVisible({timeout: 60_000});

  // Now test the index comparison feature
  const searchBox = loggedInPage.getByPlaceholder('Search index...');
  await expect(searchBox).toBeVisible();
  await searchBox.fill('S&P 500');
  await loggedInPage.getByRole('button', { name: /S&P 500/ }).click();

  // Third chart (comparison) should appear
  await expect(loggedInPage.locator('canvas').nth(2)).toBeVisible({ timeout: 60_000 });
  // await loggedInPage.waitForTimeout(2000);

  // await expect(loggedInPage).toHaveScreenshot("portfolio-hover-first.png")
});

baseTest('portfolio page shows login message and redirects when not logged in', async ({ page }) => {
  // Navigate to portfolio page without logging in
  await page.goto('/portfolio');

  // Should see the login required message
  await expect(page.getByText('Login Required')).toBeVisible();
  await expect(page.getByText('You need to be logged in to access portfolio analysis features. Redirecting to login page...')).toBeVisible();

  // Should be redirected to login page after the delay
  await page.waitForURL('/login');
  await expect(page).toHaveURL('/login');

  // Should see the login form
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
});

// test('previously uploaded portfolio', async ({ loggedInPage }) => {
//   // Navigate to portfolio page
//   await loggedInPage.getByRole('link', { name: 'Portfolio' }).click();
//   await loggedInPage.waitForURL('/portfolio');
//   await expect(loggedInPage.getByRole('button', { name: 'Upload file' })).toBeVisible();

//   // Upload the Excel file
//   const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
//   await loggedInPage.setInputFiles('input[type="file"]', filePath);

//   await loggedInPage.waitForLoadState("networkidle");

//   // Reload the page and check if the data is still there
//   await loggedInPage.reload();
//   await loggedInPage.waitForLoadState("networkidle");

//   await loggedInPage.locator('canvas').hover({
//     position: { x: 140, y: 320 },
//   });
//   await loggedInPage.waitForTimeout(2000);

//   await expect(loggedInPage).toHaveScreenshot("portfolio-hover-first-reloaded.png")
// });
