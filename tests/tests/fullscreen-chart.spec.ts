import { test } from './fixtures/auth';
import { expect } from '@playwright/test';

test('details view has fullscreen button on main price chart', async ({ loggedInPage }) => {
	// Navigate to a details page (using a known ticker)
	await loggedInPage.goto('/details/AAPL');
	await loggedInPage.waitForLoadState('networkidle');

	// Look for the fullscreen button on the main price chart
	const fullscreenButton = loggedInPage.locator('button[aria-label*="View price chart in fullscreen"]');
	await expect(fullscreenButton).toBeVisible();

	// Verify the button has the fullscreen icon (SVG path)
	const fullscreenIcon = fullscreenButton.locator('svg path');
	await expect(fullscreenIcon).toBeVisible();
});

test('compare view has fullscreen button on main growth chart', async ({ loggedInPage }) => {
	// Navigate to a compare page (using known tickers)
	await loggedInPage.goto('/compare/AAPL,MSFT');
	await loggedInPage.waitForLoadState('networkidle');

	// Look for the fullscreen button on the main growth comparison chart
	const fullscreenButton = loggedInPage.locator('button[aria-label*="View growth comparison chart in fullscreen"]');
	await expect(fullscreenButton).toBeVisible();

	// Verify the button has the fullscreen icon (SVG path)
	const fullscreenIcon = fullscreenButton.locator('svg path');
	await expect(fullscreenIcon).toBeVisible();
});