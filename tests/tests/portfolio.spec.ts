import { test } from '../fixtures/auth';
import { expect } from '@playwright/test';
import * as path from 'path';

test('upload etoro excel and calculate net worth', async ({ loggedInPage }) => {
  // Navigate to portfolio page
  await loggedInPage.getByRole('link', { name: '📊' }).click();
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

  // await expect(loggedInPage).toHaveScreenshot("portfolio-hover-first.png") // doesn't produce the same screenshot on CI TODO: debug this
});

// test('previously uploaded portfolio', async ({ loggedInPage }) => {
//   // Navigate to portfolio page
//   await loggedInPage.getByRole('link', { name: '📊' }).click();
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
