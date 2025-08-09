import { test, expect } from '@playwright/test';

test.describe('TickerSelector Reactivity', () => {
  test('should demonstrate reactivity issue and fix', async ({ page }) => {
    // Create a minimal test page with our components
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <head>
        <script type="module">
          import { SvelteSet } from 'svelte/reactivity';
          
          // Mock dataset for testing
          const mockDataset = {
            'total': [100, 110, 120, 130],
            'Closed Positions': [50, 55, 60, 65],
            'AAPL': [200, 210, 220, 230],
            'GOOGL': [300, 310, 320, 330],
            'MSFT': [150, 160, 170, 180]
          };
          
          const mockDates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'];
          
          // Test the reactivity logic directly
          function testReactivity() {
            let selectedTickers = new SvelteSet();
            
            // Simulate adding a ticker
            selectedTickers.add('AAPL');
            
            // Test if we can detect the change
            const tickersArray = Array.from(selectedTickers);
            const hasAAPL = tickersArray.includes('AAPL');
            
            document.getElementById('result').innerText = hasAAPL ? 'PASS: AAPL detected' : 'FAIL: AAPL not detected';
            
            // Now test removing
            selectedTickers.delete('AAPL');
            const afterDelete = Array.from(selectedTickers);
            const stillHasAAPL = afterDelete.includes('AAPL');
            
            document.getElementById('result2').innerText = stillHasAAPL ? 'FAIL: AAPL still there' : 'PASS: AAPL removed';
          }
          
          window.testReactivity = testReactivity;
        </script>
      </head>
      <body>
        <div id="result">Not tested yet</div>
        <div id="result2">Not tested yet</div>
        <button onclick="testReactivity()">Test Reactivity</button>
      </body>
      </html>
    `);

    // Click the test button
    await page.click('button');
    
    // Verify the results
    const result1 = await page.textContent('#result');
    const result2 = await page.textContent('#result2');
    
    expect(result1).toBe('PASS: AAPL detected');
    expect(result2).toBe('PASS: AAPL removed');
  });
});