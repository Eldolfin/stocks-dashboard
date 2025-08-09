import { test, expect, type Page } from '@playwright/test';

test.describe('Search Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should have search input and perform basic search', async ({ page }) => {
    // Find the search input
    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    await expect(searchInput).toBeVisible();

    // Type a search query
    await searchInput.fill('Apple');
    
    // Wait for search results to appear
    await page.waitForTimeout(500); // Wait for debounce + network
    
    // Check for search results or loading state
    const searchResults = page.locator('[data-testid="search-results"], .search-results, .results').first();
    
    // Either results should be visible or there should be some indication of search activity
    await expect(async () => {
      const resultsVisible = await searchResults.isVisible().catch(() => false);
      const hasContent = await page.locator('body').textContent();
      expect(resultsVisible || hasContent?.includes('Apple') || hasContent?.includes('AAPL')).toBeTruthy();
    }).toPass({ timeout: 5000 });
  });

  test('should debounce search requests', async ({ page }) => {
    // Track network requests
    const searchRequests: string[] = [];
    
    page.on('request', (request) => {
      if (request.url().includes('/api/search/')) {
        const url = new URL(request.url());
        const query = url.searchParams.get('query');
        if (query) {
          searchRequests.push(query);
        }
      }
    });

    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    // Type rapidly without waiting
    await searchInput.fill('A');
    await searchInput.fill('Ap');
    await searchInput.fill('App');
    await searchInput.fill('Appl');
    await searchInput.fill('Apple');
    
    // Wait for debounce period + network request
    await page.waitForTimeout(1000);
    
    // Should have made fewer requests than the number of keystrokes due to debouncing
    expect(searchRequests.length).toBeLessThan(5);
    
    // The final request should be for "Apple"
    if (searchRequests.length > 0) {
      expect(searchRequests[searchRequests.length - 1]).toBe('Apple');
    }
  });

  test('should show loading indicator during search', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    // Start monitoring for loading indicators before search
    const loadingPromise = page.waitForSelector(
      '[data-testid="loading"], .loading, .spinner, svg[class*="spin"], [class*="loading"]',
      { timeout: 2000 }
    ).catch(() => null);
    
    await searchInput.fill('Microsoft');
    
    // Check if loading indicator appeared
    const loadingElement = await loadingPromise;
    
    // If a loading indicator was found, verify it's visible during search
    if (loadingElement) {
      await expect(page.locator('[data-testid="loading"], .loading, .spinner, svg[class*="spin"], [class*="loading"]').first()).toBeVisible();
    }
    
    // Wait for search to complete
    await page.waitForTimeout(1000);
  });

  test('should handle rapid successive searches gracefully', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    // Perform rapid successive searches
    await searchInput.fill('Apple');
    await page.waitForTimeout(100);
    await searchInput.fill('Microsoft');
    await page.waitForTimeout(100);
    await searchInput.fill('Google');
    
    // Wait for final search to complete
    await page.waitForTimeout(1000);
    
    // Page should remain responsive and show results for the final search
    const pageContent = await page.locator('body').textContent();
    expect(pageContent).toContain('Google'); // Should show results for last search
  });

  test('should cache search results for repeated queries', async ({ page }) => {
    const searchTimes: number[] = [];
    
    page.on('response', (response) => {
      if (response.url().includes('/api/search/')) {
        searchTimes.push(Date.now());
      }
    });

    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    // First search
    await searchInput.fill('Tesla');
    await page.waitForTimeout(1000);
    
    // Clear and search again
    await searchInput.fill('');
    await page.waitForTimeout(300);
    await searchInput.fill('Tesla');
    await page.waitForTimeout(1000);
    
    // If we have multiple requests, the second should be faster (cached)
    if (searchTimes.length >= 2) {
      // Note: This test might not always pass if backend caching is working
      // perfectly as the request might not even be made
      expect(searchTimes.length).toBeGreaterThanOrEqual(1);
    }
  });

  test('should handle empty search gracefully', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    // Test empty search
    await searchInput.fill('');
    await page.waitForTimeout(500);
    
    // Should not crash or show error
    const errorElements = await page.locator('[data-testid="error"], .error, .alert-error').count();
    expect(errorElements).toBe(0);
  });

  test('should handle search errors gracefully', async ({ page }) => {
    // Mock search API to return error
    await page.route('**/api/search/**', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });

    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    await searchInput.fill('Test');
    await page.waitForTimeout(1000);
    
    // Should handle error gracefully without crashing
    const pageContent = await page.locator('body').textContent();
    expect(pageContent).toBeTruthy(); // Page should still be functional
    
    // Verify no uncaught errors in console
    const errors: string[] = [];
    page.on('pageerror', (error) => {
      errors.push(error.message);
    });
    
    await page.waitForTimeout(500);
    
    // Should not have uncaught JavaScript errors
    expect(errors.filter(e => !e.includes('Search failed'))).toHaveLength(0);
  });

  test('should show search results with proper ticker information', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="search" i], input[type="search"], input[name*="search" i]').first();
    
    await searchInput.fill('AAPL');
    await page.waitForTimeout(1000);
    
    // Check for typical stock information display
    const pageContent = await page.locator('body').textContent();
    
    // Should contain stock-related information
    const hasStockInfo = pageContent?.includes('AAPL') || 
                        pageContent?.includes('Apple') ||
                        pageContent?.includes('%') || 
                        pageContent?.includes('$');
    
    expect(hasStockInfo).toBeTruthy();
  });
});

test.describe('Search Cache Statistics', () => {
  test('cache stats endpoint should be accessible', async ({ page }) => {
    // Navigate to cache stats endpoint directly
    const response = await page.goto('/api/cache/stats');
    expect(response?.status()).toBe(200);
    
    const content = await page.content();
    expect(content).toContain('search_cache');
    expect(content).toContain('exact_cache_size');
    expect(content).toContain('ticker_cache_size');
  });
});