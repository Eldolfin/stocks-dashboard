# Finance dashboard

using flask for the backend and svelte for the frontend.

## Preview
![Portfolio hover graph screenshot](./tests/tests/portfolio.spec.ts-snapshots/portfolio-hover-first-chromium-linux.png)

## Demo Video

A comprehensive demo video showcasing all features is available. The demo covers:

- **Stock Search & Selection**: Search for multiple tickers (AAPL, GOOGL, MSFT) and select them for comparison
- **Stock Comparison**: View interactive charts comparing multiple stocks side-by-side  
- **Individual Stock Details**: Detailed view with historical charts and key performance indicators
- **eToro Portfolio Analysis**: Upload and analyze eToro Excel files with interactive portfolio charts

### Creating the Demo Video

The demo video is generated using our comprehensive E2E test suite:

1. **Generate test materials**: `./generate-demo-materials.sh`
2. **Start development environment**: `just dev-docker`  
3. **Run comprehensive test**: `cd tests && just demo`
4. **Record demo video**: `cd tests && just demo-with-video`

See the [Demo Video Script](./DEMO_VIDEO_SCRIPT.md) for detailed recording guidelines and [Comprehensive Test Documentation](./tests/COMPREHENSIVE_TEST.md) for technical details.

## Features

### 🔍 Stock Search & Analysis
- Real-time stock search with company information
- Interactive price charts and historical data
- Key performance indicators and metrics
- Multi-stock comparison functionality

### 📊 Portfolio Management  
- eToro Excel file import and analysis
- Portfolio performance tracking
- Interactive portfolio charts with hover details
- Investment analysis and insights

### 🎯 User Experience
- Responsive design for all devices
- Real-time data updates
- Intuitive navigation and search
- Professional financial dashboard interface

## Getting started

### Live version

available at [wsb.eldolfin.top](https://wsb.eldolfin.top/)

### Development

dependencies: just, docker, docker-compose, npm

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. Install them with:

```sh
pre-commit install
```

### Backend

```sh
just dev-docker
```

full deployment with reverse proxy at http://localhost:8085/

api doc at http://localhost:5000/openapi/

## Testing

### End-to-End Tests

The project includes comprehensive E2E tests using Playwright:

```sh
# Run all tests
just tests ci

# Run specific test
cd tests && npx playwright test comprehensive-walkthrough.spec.ts

# Run tests with UI for debugging  
cd tests && npx playwright test --ui

# Update test screenshots
just update-snapshots
```

### Comprehensive Feature Test

A complete walkthrough test covers all major features:
- Stock search and selection
- Multi-stock comparison charts
- Individual ticker details
- eToro portfolio file upload and analysis

See [Comprehensive Test Documentation](./tests/COMPREHENSIVE_TEST.md) for details.

### Backend Tests

```sh
# Run backend unit tests
just backend test

# Run with coverage
just backend test-coverage
```

## TODO

see the
[V1 issue board](https://gitea.eldolfin.top/Eldolfin/finance-plots/projects/10)
