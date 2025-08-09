# Screenshot Utility for Stocks Dashboard

This repository now includes a screenshot utility that can capture images of the running website using Playwright. This is useful for documentation, PR previews, and visual regression testing.

## Features

- ✅ **Automatic service startup**: Ensures backend and frontend are running before taking screenshots
- ✅ **Multiple page support**: Can screenshot all pages or specific URLs
- ✅ **Authentication handling**: Automatically logs in for protected pages
- ✅ **Flexible output**: Configurable output directory and naming
- ✅ **Full-page screenshots**: Captures entire page content, not just viewport
- ✅ **API documentation**: Includes OpenAPI/Swagger documentation screenshots

## Usage

### Using the just recipe (recommended)

```bash
# Take screenshots of all pages (default output: ./screenshots/)
just screenshot

# Take screenshots with custom output directory  
just screenshot ./my-screenshots

# Take screenshot of specific URL
just screenshot ./screenshots http://localhost:8085/login
```

### Using the shell script directly

```bash
# Take screenshots of all pages
./demo-screenshots.sh

# Custom output directory
./demo-screenshots.sh ./my-screenshots

# Specific URL
./demo-screenshots.sh ./screenshots http://localhost:8085/portfolio
```

### Using the TypeScript utility directly (advanced)

```bash
cd tests
npx tsx screenshot-utility.ts [output-dir] [url]
```

## Prerequisites

The screenshot utility automatically handles prerequisites, but you can also set them up manually:

1. **Development environment**: The backend and frontend must be running
   ```bash
   just dev-docker  # Starts both services
   ```

2. **Test dependencies**: Playwright and related packages
   ```bash
   cd tests && npm install
   ```

3. **Playwright browsers** (installed automatically in normal environments)
   ```bash
   cd tests && npx playwright install chromium
   ```

## Pages Captured

### Public Pages (no authentication required)
- **Homepage**: `http://localhost:8085/` - Main dashboard landing page
- **Login**: `http://localhost:8085/login` - User login form  
- **Register**: `http://localhost:8085/register` - User registration form
- **API Docs**: `http://localhost:5000/openapi/` - OpenAPI/Swagger documentation

### Protected Pages (requires authentication)
- **Portfolio**: `http://localhost:8085/portfolio` - User portfolio with file upload
- **Profile**: `http://localhost:8085/profile` - User profile management
- **Stock Details**: `http://localhost:8085/details/AAPL` - Individual stock analysis
- **Stock Comparison**: `http://localhost:8085/compare/AAPL,MSFT` - Side-by-side stock comparison

## Authentication Flow

For protected pages, the utility automatically:
1. Creates a test user account
2. Logs in with the test credentials  
3. Takes screenshots of authenticated pages
4. Cleans up the session

## Output

Screenshots are saved as PNG files in the specified directory (default: `./screenshots/`):

```
screenshots/
├── homepage.png
├── login-page.png
├── register-page.png  
├── api-docs.png
├── portfolio-page.png
├── profile-page.png
├── details-page-aapl.png
└── compare-page.png
```

## Configuration

### Custom Screenshot Configuration

You can modify the screenshot configurations in `tests/screenshot-utility.ts`:

```typescript
const customScreenshots: ScreenshotConfig[] = [
  {
    url: 'http://localhost:8085/my-page',
    name: 'my-custom-page',
    waitFor: 'h1', // Wait for specific element
    fullPage: true
  }
];
```

### Screenshot Options

- `url`: The URL to screenshot
- `name`: Output filename (without extension)  
- `waitFor`: Element selector to wait for, or milliseconds to wait
- `fullPage`: Whether to capture the full scrollable page

## Troubleshooting

### Services Not Running
```bash
# Make sure development environment is running
just dev-docker

# Check if services are accessible
curl http://localhost:8085/        # Frontend
curl http://localhost:5000/health  # Backend  
```

### Browser Installation Issues
```bash
# Manually install Playwright browsers
cd tests && npx playwright install chromium
```

### Network Restrictions
In network-restricted environments, the demo script provides a fallback that shows what would be captured without actually taking screenshots.

## Integration with CI/CD

The screenshot utility can be integrated into GitHub Actions workflows:

```yaml
- name: Take screenshots
  run: |
    just dev-docker
    just screenshot ./pr-screenshots
    
- name: Upload screenshots
  uses: actions/upload-artifact@v3
  with:
    name: website-screenshots
    path: pr-screenshots/
```

## Files Added

- `tests/screenshot-utility.ts` - Main TypeScript screenshot utility
- `demo-screenshots.sh` - Fallback script for restricted environments  
- `take-screenshots.sh` - Full-featured shell script wrapper
- `justfile` - Added `screenshot` recipe
- `.gitignore` - Added `screenshots/` directory to ignore list

## Examples

### Taking Screenshots for PR Review

```bash
# Start development environment
just dev-docker

# Take screenshots of all pages
just screenshot ./pr-screenshots

# Screenshots are now available in ./pr-screenshots/
ls -la ./pr-screenshots/
```

### Custom Single Page Screenshot

```bash
# Screenshot just the portfolio page
just screenshot ./portfolio-screenshot http://localhost:8085/portfolio
```

### Automated Screenshot Updates

```bash
# Script to update screenshots regularly
#!/bin/bash
just dev-docker
just screenshot ./latest-screenshots
git add latest-screenshots/
git commit -m "Update website screenshots"
```