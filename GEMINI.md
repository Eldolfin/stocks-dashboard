This file provides context for the Gemini AI assistant to work on this project.

## Project Purpose

This project is a financial dashboard that displays stock information. It has a Python Flask backend and a Svelte frontend.

## Technologies Used

### Backend

*   **Framework:** Flask
*   **API Documentation:** flask-openapi3
*   **Data Validation:** pydantic
*   **Data Source:** yfinance
*   **Key Libraries:**
    *   `yfinance`: Used for fetching financial data from Yahoo Finance.
    *   `flask`: Web framework for the backend API.
    *   `flask-openapi3`: Generates OpenAPI documentation for the Flask API.
    *   `pydantic`: Data validation and settings management using Python type hints.
    *   `flask_cors`: Handles Cross-Origin Resource Sharing (CORS) for the Flask app.
    *   `openpyxl`: Used for reading and writing Excel files (specifically for eToro analysis).

### Frontend

*   **Framework:** Svelte
*   **Build Tool:** Vite
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS, Flowbite-Svelte
*   **Charting:** Chart.js, chartjs-plugin-zoom
*   **Key Libraries:**
    *   `@sveltejs/kit`: Svelte framework for building web applications.
    *   `chart.js`: Flexible JavaScript charting library.
    *   `chartjs-plugin-zoom`: Plugin for Chart.js to enable zooming and panning.
    *   `tailwindcss`: A utility-first CSS framework.
    *   `flowbite-svelte`: Svelte components for Flowbite, a popular UI kit.
    *   `openapi-fetch`: Client for fetching data from OpenAPI-specified APIs.
    *   `luxon`: Library for working with dates and times.
    *   `moment`: Another library for parsing, validating, manipulating, and formatting dates.

## Main Files and Their Functions

### Backend

*   `backend/app.py`:
    *   **Purpose:** The main Flask application file that defines the API endpoints.
    *   **Functions:**
        *   `create_app()`: Factory function to create and configure the Flask app.
*   `backend/src/auth.py`:
    *   **Purpose:** Defines authentication-related endpoints.
    *   **Functions:**
        *   `register`: Handles user registration.
        *   `login`: Authenticates users.
        *   `get_user`: Retrieves the current user's information.
        *   `logout`: Logs out the current user.
        *   `upload_profile_picture`: Handles profile picture uploads.
        *   `get_profile_picture`: Serves profile pictures.
*   `backend/src/stocks.py`:
    *   **Purpose:** Defines endpoints for retrieving stock data.
    *   **Functions:**
        *   `get_ticker`: Retrieves historical price data for a given ticker.
        *   `get_compare_growth`: Compares the growth of multiple tickers.
        *   `get_kpis`: Fetches Key Performance Indicators (KPIs) for a specific ticker.
        *   `search_ticker`: Performs a full-text search for tickers.
        *   `analyze_etoro_excel`: Analyzes an uploaded eToro Excel sheet to extract closed position data.

*   `backend/src/etoro_data.py`:
    *   **Purpose:** Contains functions for processing eToro Excel statements.
    *   **Functions:**
        *   `column_date_to_timestamp(column: pd.Series)`: Converts date columns in a Pandas DataFrame to timestamps.
        *   `extract_closed_position(etoro_statement: bytes, time_unit="m")`: Extracts and processes closed position data from an eToro Excel statement.

*   `backend/src/intervals.py`:
    *   **Purpose:** Provides utility functions for converting between time intervals and durations.
    *   **Functions:**
        *   `interval_to_duration(interval: str)`: Converts a string interval (e.g., "1mo", "5d") to a `timedelta` object.
        *   `duration_to_interval(duration: timedelta)`: Converts a `timedelta` object to a suitable interval string.

*   `backend/src/models.py`:
    *   **Purpose:** Defines Pydantic models for API request and response schemas, ensuring data validation and clear API contracts.
    *   **Key Models:**
        *   `TickerQuery`, `TickerResponse`: For historical price data.
        *   `CompareGrowthQuery`, `CompareGrowthResponse`: For comparing ticker growth.
        *   `KPIQuery`, `KPIResponse`, `MainKPIs`, `AnalystPriceTargets`, `Info`: For ticker KPIs and detailed information.
        *   `SearchQuery`, `SearchResponse`, `RawQuote`, `Quote`: For ticker search functionality.
        *   `EtoroForm`, `EtoroAnalysisResponse`, `PrecisionEnum`: For eToro analysis.
        *   `NotFoundResponse`: Generic response for resource not found errors.

### Frontend

*   `frontend/src/app.css`:
    *   **Purpose:** Global CSS file for the Svelte application, including Tailwind CSS imports and custom theme variables.

*   `frontend/src/app.d.ts`:
    *   **Purpose:** TypeScript declaration file for SvelteKit's `App` namespace, used for type augmentation.

*   `frontend/src/app.html`:
    *   **Purpose:** The main HTML template for the Svelte application.

*   `frontend/src/lib/chart-utils.ts`:
    *   **Purpose:** Utility functions for Chart.js, including color manipulation and data generation.
    *   **Functions:**
        *   `srand(seed: number)`: Sets the seed for the random number generator.
        *   `rand(min: number, max: number)`: Generates a random number within a specified range.
        *   `numbers(config: object)`: Generates an array of numbers based on configuration.
        *   `transparentize(value: string | number[], opacity: number)`: Makes a color transparent.
        *   `namedColor(index: number)`: Returns a color from a predefined list based on an index.

*   `frontend/src/lib/format-utils.ts`:
    *   **Purpose:** Utility functions for formatting numbers, percentages, and currency.
    *   **Functions:**
        *   `roundPrecision(value: number, precision: number)`: Rounds a number to a specified precision.
        *   `formatPercent(ratio: number | null)`: Formats a number as a percentage.
        *   `formatCurrency(dollars: number | null)`: Formats a number as currency.
        *   `ratioColor(ratio: number | null | undefined)`: Returns a color (green, red, or gray) based on a ratio's sign.

*   `frontend/src/lib/index.ts`:
    *   **Purpose:** An empty file, typically used as an entry point for `$lib` alias imports.

*   `frontend/src/lib/typed-fetch-client.ts`:
    *   **Purpose:** Configures and exports an OpenAPI fetch client for interacting with the backend API.
    *   **Variables:**
        *   `client`: The configured OpenAPI fetch client.

*   `frontend/src/routes/+layout.svelte`:
    *   **Purpose:** The main layout component for the Svelte application, including navigation (Navbar, Sidebar) and dark mode toggle.

*   `frontend/src/routes/+page.svelte`:
    *   **Purpose:** The home page of the dashboard, featuring a ticker search and a table to display search results and compare selected tickers.
    *   **Functions:**
        *   `onSearch()`: Handles the ticker search functionality, fetching data from the backend.
        *   `comparedTickersUrl()`: Generates a URL string for comparing selected tickers.

*   `frontend/src/routes/portfolio/+page.svelte`:
    *   **Purpose:** Allows users to upload and analyze eToro Excel statements, displaying profit over time in a bar chart.
    *   **Functions:**
        *   Handles file upload and sends data to the backend for analysis.
        *   Displays the `BarChart` component with the analysis results.

*   `frontend/src/routes/compare/[tickers]/+page.server.ts`:
    *   **Purpose:** SvelteKit server load function for the ticker comparison page, fetching comparison data from the backend.
    *   **Functions:**
        *   `load({ params })`: Fetches growth comparison data for the tickers specified in the URL parameters.

*   `frontend/src/routes/compare/[tickers]/+page.svelte`:
    *   **Purpose:** Displays the growth comparison of multiple tickers using a `HistoryChart` component.

*   `frontend/src/routes/details/[ticker]/+page.server.ts`:
    *   **Purpose:** SvelteKit server load function for the ticker details page, fetching historical data and KPIs from the backend.
    *   **Functions:**
        *   `load({ params })`: Fetches historical price data and KPIs for the specified ticker.

*   `frontend/src/routes/details/[ticker]/+page.svelte`:
    *   **Purpose:** Displays detailed information about a specific ticker, including its price history (using `HistoryChart`) and various KPIs in a table.

*   `frontend/src/lib/components/BarChart.svelte`:
    *   **Purpose:** A reusable Svelte component for rendering bar charts using Chart.js.
    *   **Props:** `title`, `dataset`, `color`, `dates`.

*   `frontend/src/lib/components/HistoryChart.svelte`:
    *   **Purpose:** A reusable Svelte component for rendering line charts (historical data) using Chart.js, with zoom and pan functionality.
    *   **Props:** `title`, `dataset`, `dates`, `delta`.

### Testing

*   `tests/`:
    *   **Purpose:** Contains end-to-end tests for the application using Playwright.
    *   `tests/justfile`: Defines commands for running tests.
    *   `tests/playwright.config.ts`: Configuration file for Playwright.

## Development Workflow

*   When developing the frontend, run `npm run check` in the `frontend` folder and fix all the errors listed.
*   When developing the backend, run `uv run ruff check backend/` and `uv run ruff format backend/` to lint and format the code. Fix all the errors listed before committing.
*   To run the end-to-end tests, use the command `just tests run`. This will restart the frontend and backend with a clean database, and then run the Playwright tests.
*   After any feature addition or bug fix, you should write new end-to-end tests to validate the changes and ensure that everything works as expected.
*   If the end-to-end tests fail, you need to fix the issue and rerun the tests until they pass.
*   When commiting, some pre-commit hooks run lint checks, do not try to bypass them or disable them, think through the issue and handle them safely.
*   Don't try to install library, I'm using docker so they should be installed there. You can check their logs with docker compose logs in the `dev` folder

## API Type Generation

The frontend uses `openapi-typescript` to generate TypeScript types from the backend's OpenAPI specification. To regenerate the types, run `just generate-api-types`. This ensures type safety and autocompletion for API interactions in the frontend.
