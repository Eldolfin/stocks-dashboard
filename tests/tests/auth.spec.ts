import { test } from './fixtures/auth';
import { expect } from '@playwright/test';

test('register + login', async ({ loggedInPage }) => {
  // back to the home page
  await expect(loggedInPage.getByRole('heading', { name: 'WallStreet Bets 💸' })).toBeVisible();
  await expect(loggedInPage.getByRole('button', { name: 'Logout' })).toBeVisible();
});

test('logout', async ({ loggedInPage }) => {
  await loggedInPage.getByRole('button', { name: 'Logout' }).click();
  await expect(loggedInPage.getByRole('link', { name: 'Register' })).toBeVisible();
});
