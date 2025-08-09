import { test } from './fixtures/auth';
import { test as baseTest, expect } from '@playwright/test';
import * as path from 'path';

test('upload etoro excel and calculate net worth', async ({ loggedInPage }) => {
  // Navigate to portfolio page
  await loggedInPage.getByRole('link', { name: 'Portfolio' }).click();
  await loggedInPage.waitForURL('/portfolio');
  await expect(loggedInPage.getByRole('button', { name: 'Upload file' })).toBeVisible();

  // Upload the Excel file
  const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await loggedInPage.setInputFiles('input[type="file"]', filePath);

  await loggedInPage.getByRole('button', { name: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' }).click();

  await loggedInPage.waitForLoadState("networkidle");

  await loggedInPage.locator('canvas').first().hover({
    position: { x: 140, y: 320 },
  });
  await loggedInPage.waitForTimeout(2000);

  await expect(loggedInPage).toHaveScreenshot("portfolio-hover-first.png")
});

baseTest('portfolio page shows login modal when not logged in', async ({ page }) => {
  // Navigate to portfolio page without logging in
  await page.goto('/portfolio');
  await page.waitForURL('/portfolio');
  
  // Check that the login modal is visible
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByText('Login to your account')).toBeVisible();
  
  // Check that we can switch to register tab
  await page.getByRole('button', { name: 'Register' }).click();
  await expect(page.getByText('Create new account')).toBeVisible();
  
  // Check that we can switch back to login tab
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByText('Login to your account')).toBeVisible();
  
  // Check that cancel button works and redirects
  await page.getByRole('button', { name: 'Cancel' }).click();
  await page.waitForURL('/');
  await expect(page).toHaveURL('/');
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
