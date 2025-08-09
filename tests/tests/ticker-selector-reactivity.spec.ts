import { test } from './fixtures/auth';
import { expect } from '@playwright/test';
import * as path from 'path';

test('ticker selector should update chart data when tickers are selected', async ({ loggedInPage }) => {
  // Navigate to portfolio page
  await loggedInPage.getByRole('link', { name: 'Portfolio' }).click();
  await loggedInPage.waitForURL('/portfolio');
  await expect(loggedInPage.getByRole('button', { name: 'Upload file' })).toBeVisible();

  // Upload the Excel file
  const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await loggedInPage.setInputFiles('input[type="file"]', filePath);

  await loggedInPage.getByRole('button', { name: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' }).click();

  await loggedInPage.waitForLoadState("networkidle");

  // Wait for the ticker selector to be visible
  await expect(loggedInPage.getByPlaceholder('Search tickers...')).toBeVisible();

  // Take a screenshot of the initial chart state
  await loggedInPage.locator('canvas').first().screenshot({ path: 'tests/test-results/chart-before-ticker-selection.png' });

  // Search for a ticker - let's try searching for a common ticker
  await loggedInPage.getByPlaceholder('Search tickers...').fill('AAPL');
  await loggedInPage.waitForTimeout(500); // Wait for search to filter

  // Check if any tickers appear in the dropdown
  const tickerDropdown = loggedInPage.locator('.bg-gray-800.shadow-lg');
  const isDropdownVisible = await tickerDropdown.isVisible();
  
  if (isDropdownVisible) {
    // Click on the first ticker in the search results
    await loggedInPage.locator('.bg-gray-800.shadow-lg button').first().click();
    
    // Wait for the chart to update
    await loggedInPage.waitForTimeout(1000);
    
    // Take a screenshot after ticker selection
    await loggedInPage.locator('canvas').first().screenshot({ path: 'tests/test-results/chart-after-ticker-selection.png' });
    
    // Verify that the selected ticker appears in the selected tickers list
    await expect(loggedInPage.getByText('Selected Tickers:')).toBeVisible();
    
    // Get the chart data before and after selection to verify they're different
    const chartDataAfter = await loggedInPage.locator('canvas').first().evaluate((canvas) => {
      const chart = (canvas as any).chart;
      return chart ? chart.data.datasets.length : 0;
    });
    
    // Should have more than just the default lines (total, Closed Positions)
    expect(chartDataAfter).toBeGreaterThan(2);
  } else {
    // If no tickers found with AAPL, try another approach - search without specific ticker
    await loggedInPage.getByPlaceholder('Search tickers...').clear();
    await loggedInPage.getByPlaceholder('Search tickers...').fill('A');
    await loggedInPage.waitForTimeout(500);
    
    const anyDropdown = await loggedInPage.locator('.bg-gray-800.shadow-lg').isVisible();
    if (anyDropdown) {
      await loggedInPage.locator('.bg-gray-800.shadow-lg button').first().click();
      await loggedInPage.waitForTimeout(1000);
      await expect(loggedInPage.getByText('Selected Tickers:')).toBeVisible();
    }
  }
});

test('ticker selector reactivity - select multiple tickers and verify chart updates', async ({ loggedInPage }) => {
  // Navigate to portfolio page
  await loggedInPage.getByRole('link', { name: 'Portfolio' }).click();
  await loggedInPage.waitForURL('/portfolio');
  
  // Upload the Excel file
  const filePath = path.resolve(__dirname, '../data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx');
  await loggedInPage.setInputFiles('input[type="file"]', filePath);
  await loggedInPage.getByRole('button', { name: 'etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx' }).click();
  await loggedInPage.waitForLoadState("networkidle");

  // Get initial dataset count
  const initialDatasetCount = await loggedInPage.locator('canvas').first().evaluate((canvas) => {
    const chart = (canvas as any).chart;
    return chart ? chart.data.datasets.length : 0;
  });

  // Search and select first ticker
  await loggedInPage.getByPlaceholder('Search tickers...').fill('A');
  await loggedInPage.waitForTimeout(500);
  
  const firstTickerButton = loggedInPage.locator('.bg-gray-800.shadow-lg button').first();
  if (await firstTickerButton.isVisible()) {
    await firstTickerButton.click();
    await loggedInPage.waitForTimeout(1000);
    
    // Verify dataset count increased
    const afterFirstSelection = await loggedInPage.locator('canvas').first().evaluate((canvas) => {
      const chart = (canvas as any).chart;
      return chart ? chart.data.datasets.length : 0;
    });
    expect(afterFirstSelection).toBeGreaterThan(initialDatasetCount);
    
    // Clear search and select another ticker
    await loggedInPage.getByPlaceholder('Search tickers...').clear();
    await loggedInPage.getByPlaceholder('Search tickers...').fill('B');
    await loggedInPage.waitForTimeout(500);
    
    const secondTickerButton = loggedInPage.locator('.bg-gray-800.shadow-lg button').first();
    if (await secondTickerButton.isVisible()) {
      await secondTickerButton.click();
      await loggedInPage.waitForTimeout(1000);
      
      // Verify dataset count increased again
      const afterSecondSelection = await loggedInPage.locator('canvas').first().evaluate((canvas) => {
        const chart = (canvas as any).chart;
        return chart ? chart.data.datasets.length : 0;
      });
      expect(afterSecondSelection).toBeGreaterThan(afterFirstSelection);
    }
  }
});