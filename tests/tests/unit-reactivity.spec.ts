import { test, expect } from '@playwright/test';

test.describe('TickerSelector Reactivity', () => {
  test('should work with array-based selectedTickers', async ({ page }) => {
    // Create a test page that simulates our component behavior
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <head>
        <script type="module">
          // Simulate our component logic with arrays instead of SvelteSet
          function createTickerSelector() {
            let selectedTickers = [];
            
            // Mock dataset
            const dataset = {
              'total': [100, 110, 120, 130],
              'Closed Positions': [50, 55, 60, 65],
              'AAPL': [200, 210, 220, 230],
              'GOOGL': [300, 310, 320, 330],
              'MSFT': [150, 160, 170, 180]
            };
            
            const defaultShown = ['total', 'Closed Positions'];
            
            function selectTicker(ticker) {
              const index = selectedTickers.indexOf(ticker);
              if (index >= 0) {
                selectedTickers.splice(index, 1);
              } else {
                selectedTickers.push(ticker);
              }
              selectedTickers = [...selectedTickers]; // Trigger reactivity
              updateChart();
            }
            
            function updateChart() {
              const result = {};
              
              // Add default shown tickers
              for (const ticker of defaultShown) {
                result[ticker] = dataset[ticker];
              }
              
              // Add selected tickers
              for (const ticker of selectedTickers) {
                if (dataset[ticker]) {
                  result[ticker] = dataset[ticker];
                }
              }
              
              const resultKeys = Object.keys(result);
              document.getElementById('chart-data').textContent = 
                \`Chart has \${resultKeys.length} datasets: \${resultKeys.join(', ')}\`;
              document.getElementById('selected-count').textContent = 
                \`Selected: \${selectedTickers.length} tickers\`;
            }
            
            // Initialize
            updateChart();
            
            return { selectTicker };
          }
          
          const selector = createTickerSelector();
          window.selectTicker = selector.selectTicker;
        </script>
      </head>
      <body>
        <div id="chart-data">Chart loading...</div>
        <div id="selected-count">Selected: 0 tickers</div>
        <button onclick="selectTicker('AAPL')">Toggle AAPL</button>
        <button onclick="selectTicker('GOOGL')">Toggle GOOGL</button>
        <button onclick="selectTicker('MSFT')">Toggle MSFT</button>
      </body>
      </html>
    `);

    // Check initial state - should have default tickers
    await expect(page.locator('#chart-data')).toContainText('Chart has 2 datasets: total, Closed Positions');
    await expect(page.locator('#selected-count')).toContainText('Selected: 0 tickers');
    
    // Select AAPL
    await page.click('button:has-text("Toggle AAPL")');
    await expect(page.locator('#chart-data')).toContainText('Chart has 3 datasets: total, Closed Positions, AAPL');
    await expect(page.locator('#selected-count')).toContainText('Selected: 1 tickers');
    
    // Select GOOGL
    await page.click('button:has-text("Toggle GOOGL")');
    await expect(page.locator('#chart-data')).toContainText('Chart has 4 datasets');
    await expect(page.locator('#selected-count')).toContainText('Selected: 2 tickers');
    
    // Deselect AAPL
    await page.click('button:has-text("Toggle AAPL")');
    await expect(page.locator('#chart-data')).toContainText('Chart has 3 datasets: total, Closed Positions, GOOGL');
    await expect(page.locator('#selected-count')).toContainText('Selected: 1 tickers');
  });
});