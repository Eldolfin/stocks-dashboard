# Comprehensive E2E Test Documentation

## Overview

The `comprehensive-walkthrough.spec.ts` test provides a complete end-to-end walkthrough of all major features in the stocks dashboard application. This test serves dual purposes:

1. **Regression Testing**: Ensures all core functionality works as expected
2. **Demo Documentation**: Captures screenshots that can be used for documentation and demo videos

## Features Covered

### 1. Home Page Navigation
- Verifies the main landing page loads correctly
- Confirms the search functionality is available

### 2. Stock Search and Selection
- Tests searching for multiple stock tickers (AAPL, GOOGL, MSFT)
- Verifies search results display properly
- Tests the ticker selection mechanism via checkboxes

### 3. Stock Comparison
- Tests navigation to the comparison page
- Verifies multiple stocks can be compared simultaneously
- Confirms comparison charts load and display data

### 4. Individual Stock Details
- Tests navigation to individual ticker detail pages
- Verifies historical data charts display
- Confirms KPI information is visible

### 5. eToro Portfolio Analysis
- Tests navigation to the portfolio analysis section
- Verifies file upload functionality with sample eToro Excel files
- Confirms analysis results and charts display correctly
- Tests hover interactions with portfolio charts

## Screenshots Generated

The test automatically captures screenshots at key points:

1. `01-aapl-search-results.png` - Search results for AAPL
2. `02-selected-stocks.png` - Multiple stocks selected for comparison
3. `03-comparison-chart.png` - Stock comparison page with charts
4. `04-ticker-details.png` - Individual ticker details page
5. `05-portfolio-analysis.png` - Portfolio analysis with uploaded data
6. `06-analysis-page.png` - Analysis subpage (if available)

## Running the Test

### Prerequisites
- Development environment must be running on `localhost:8085`
- Test data file must be available: `tests/data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx`

### Commands

```bash
# Run the comprehensive test only
npx playwright test comprehensive-walkthrough.spec.ts

# Run with UI for debugging
npx playwright test comprehensive-walkthrough.spec.ts --ui

# Run and generate test report
npx playwright test comprehensive-walkthrough.spec.ts --reporter=html
```

### Using Docker (Recommended for CI)

```bash
# From the tests directory
just docker
just docker-playwright test comprehensive-walkthrough.spec.ts
```

## Test Design Features

### Robustness
- Includes comprehensive error handling and fallback mechanisms
- Uses flexible selectors that work across different UI states
- Implements proper wait strategies for dynamic content

### Debugging Support
- Extensive console logging for each test step
- Clear step documentation within the test code
- Meaningful screenshot names for easy identification

### Maintainability
- Modular structure with clear separation of test steps
- Helper functions for common operations
- Comprehensive documentation and comments

## Creating Demo Videos

The generated screenshots can be used to create demo videos by:

1. Running the test to capture current screenshots
2. Using the screenshots as a storyboard for video creation
3. Recording actual browser interactions following the test steps
4. Combining screenshots and recordings for comprehensive demos

## Troubleshooting

### Common Issues

**Server not running**: Ensure the development environment is started with `just dev-docker`

**Test timeouts**: The test includes extended timeouts for chart loading. If issues persist, check network connectivity and server performance.

**File upload failures**: Verify the test data file exists and is accessible at the expected path.

**Screenshot differences**: Screenshots may vary based on screen resolution and data loading times. Use `--update-snapshots` to refresh baseline images.

### Configuration

The test can be configured via:
- Timeout adjustments in the test file
- Screenshot comparison thresholds in `playwright.config.ts`
- Server URL changes in the Playwright configuration