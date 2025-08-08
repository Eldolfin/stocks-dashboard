import { test as base, expect } from '@playwright/test';
import type { Page } from '@playwright/test';

type MyFixtures = {
  loggedInPage: Page;
};

export const test = base.extend<MyFixtures>({
  loggedInPage: async ({ page }, use, testInfo) => {
    const email = `test-user-${testInfo.workerIndex}-${Math.random().toString(36).substring(2, 15)}@a.a`;
    const password = "test";

    await page.goto('/');
    await page.getByRole('link', { name: 'Register' }).click();

    // /register
    await page.getByRole('textbox', { name: 'Your email' }).fill(email);
    await page.getByRole('textbox', { name: 'Your password' }).fill(password);
    await page.getByRole('button', { name: 'Register' }).click();
    // After registration, wait for the login page elements
    await expect(page.getByRole('button', { name: 'Login' })).toBeVisible();

    // /login
    await page.getByRole('textbox', { name: 'Your email' }).fill(email);
    await page.getByRole('textbox', { name: 'Your password' }).fill(password);
    await page.getByRole('button', { name: 'Login' }).click();

    // After login, wait for the home page elements
    await expect(page.getByRole('heading', { name: 'WallStreet Bets 💸' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Logout' })).toBeVisible();

    await use(page);
  },
});
