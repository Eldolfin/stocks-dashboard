# Comprehensive E2E Test - Quick Reference

## What does this test do?

The comprehensive E2E test (`comprehensive-walkthrough.spec.ts`) validates ALL major features of the stocks dashboard by simulating a complete user journey:

1. **🏠 Home Page** - Loads main dashboard
2. **🔍 Stock Search** - Searches for AAPL, GOOGL, MSFT
3. **☑️ Selection** - Selects multiple stocks for comparison  
4. **📊 Comparison** - Views stock comparison charts
5. **📈 Details** - Examines individual stock details
6. **📁 Portfolio** - Uploads eToro Excel file
7. **💹 Analysis** - Reviews portfolio analysis results

## Quick Commands

```bash
# Basic test run
cd tests && npx playwright test comprehensive-walkthrough.spec.ts

# Debug mode with browser UI
cd tests && npx playwright test comprehensive-walkthrough.spec.ts --ui

# Generate demo assets
cd tests && just demo

# Record video demo
cd tests && just demo-with-video
```

## Output Files

- **Screenshots**: `tests/comprehensive-walkthrough.spec.ts-snapshots/`
- **Test Report**: `tests/playwright-report/index.html`  
- **Videos** (if enabled): `tests/test-results/`

## Screenshots Generated

1. `01-aapl-search-results.png` - AAPL search results
2. `02-selected-stocks.png` - Multiple stocks selected
3. `03-comparison-chart.png` - Stock comparison view
4. `04-ticker-details.png` - Individual stock details
5. `05-portfolio-analysis.png` - Portfolio analysis
6. `06-analysis-page.png` - Analysis subpage (if exists)

## For Demo Video Creation

1. Run `just demo` to generate screenshots
2. Run `just demo-with-video` to record browser interactions
3. Use screenshots as storyboard reference
4. Combine recordings for final demo video

## Troubleshooting

- **Server not running**: Start with `just dev-docker`
- **Test fails**: Run with `--ui` to debug interactively  
- **Screenshots differ**: Use `--update-snapshots` to refresh
- **File upload fails**: Check test data file exists

## Integration with CI/CD

The test runs automatically in GitHub Actions and can be used for:
- Regression testing before releases
- Demo content generation
- Feature validation
- User acceptance testing