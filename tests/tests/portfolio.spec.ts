import { test, expect } from '@playwright/test';
import * as path from 'path';

test('upload etoro excel and calculate net worth', async ({ page, request }) => {
  const email = `test-networth-${test.info().workerIndex}-${Date.now()}@a.a`;
  const password = "test";

  // Register and login a user
  await page.goto('/');
  await page.getByRole('link', { name: '📝' }).click();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForLoadState('networkidle');
  await expect(page.getByRole('heading', { name: 'WallStreet Bets 💸' })).toBeVisible();

  // Navigate to portfolio page
  await page.getByRole('link', { name: '📊' }).click();
  await page.waitForURL('/portfolio');
  await expect(page.getByRole('button', { name: 'Upload file' })).toBeVisible();

  // Upload the Excel file
  const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await page.setInputFiles('input[type="file"]', filePath);

  await page.waitForLoadState("networkidle");

  await page.locator('canvas').hover({
    position: { x: 140, y: 320 },
  });
  await page.waitForTimeout(2000);

  await expect(page).toHaveScreenshot("portfolio-hover-first.png")
});
