import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  const email = `test-user-${test.info().workerIndex}@a.a`;
  const password = "test";

  await page.goto('http://localhost:5173/');
  await page.getByRole('link', { name: '📝' }).click();

  // /register
  await page.getByRole('textbox', { name: 'Your email' }).click();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).click();
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Register' }).click();

  // /login
  await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();
  await page.getByRole('textbox', { name: 'Your email' }).click();
  await page.getByRole('textbox', { name: 'Your email' }).fill(email);
  await page.getByRole('textbox', { name: 'Your password' }).click();
  await page.getByRole('textbox', { name: 'Your password' }).fill(password);
  await page.getByRole('button', { name: 'Login' }).click();

  // back to the home page
  await expect(page.getByRole('heading', { name: 'Search' })).toBeVisible();

  // TODO: we should not need to refresh here for hte logout button to be visible
  await page.goto('http://localhost:5173/');
  await expect(page.getByRole('button', { name: '🔓' })).toBeVisible();
});
