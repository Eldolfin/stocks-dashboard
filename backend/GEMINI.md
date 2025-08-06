---
This file provides context for the Gemini AI assistant to work on this project.

## Project Purpose

This project is the backend API for a financial dashboard. It is built with Python and Flask.

## Technologies Used

*   **Framework:** Flask
*   **Database:** SQLite
*   **API Documentation:** flask-openapi3
*   **Data Validation:** pydantic
*   **Dependencies:**
    *   yfinance
    *   flask
    *   flask-openapi3
    *   pydantic
    *   flask_cors
    *   openpyxl
    *   flask-caching
    *   flask-login
    *   pandas
    *   google-genai
    *   matplotlib

## Main Files and Their Functions

The backend is structured in a layered architecture: `endpoints`, `services`, and `database`.

*   `src/app.py`: The main Flask application file. It initializes the app, database, and registers the API blueprints from the `endpoints` layer.
*   `src/models.py`: Defines Pydantic models for API request and response schemas.

### Endpoints Layer (`src/endpoints/`)
Exposes the API to the outside world. It handles HTTP requests and responses.

*   `src/endpoints/auth.py`: Defines authentication-related API endpoints and maps them to the `AuthService`.
*   `src/endpoints/stocks.py`: Defines API endpoints for retrieving stock data and maps them to the `StocksService`.

### Services Layer (`src/services/`)
Contains the core business logic of the application.

*   `src/services/auth_service.py`: Handles the logic for user registration, login, and profile management. Interacts with the `AuthRepository`.
*   `src/services/stocks_service.py`: Implements the logic for fetching and processing financial data (tickers, KPIs, comparisons). Interacts with the `stocks_repository` and uses helper services.
*   `src/services/etoro_data.py`: A helper service for processing and analyzing uploaded eToro Excel statements.
*   `src/services/intervals.py`: A helper service providing utility functions for time interval conversions.

### Data Access Layer (`src/database/`)
Responsible for all interactions with data sources.

*   `src/database/auth_repository.py`: Manages all database operations related to users (creation, retrieval, updates) in the SQLite database.
*   `src/database/stocks_repository.py`: Acts as a data source for financial information by wrapping the `yfinance` library.

## Database

The application uses a SQLite database. When running inside the Docker container, the database is located at `/database/database.db`. The database is initialized in `src/app.py`, and the schema is defined directly in the code.

## Development Workflow

*   **Linting:** `just lint`
*   **Formatting:** `just format`
*   **Auto-fix Linting:** `uv run ruff check --fix --unsafe-fixes`
*   **Testing:** `just test`
*   **CI:** `just ci` (never run this you don't need it)

Before committing, ensure that the code is properly linted and formatted by running `just lint` and `just format`. All tests should pass before pushing to the main branch.

## Testing

The project uses `pytest` for testing. The tests are located in the `tests/` directory and are separated into `test_auth.py` and `test_stocks.py`.

To run the tests, use the `just test` command. The tests make live requests to the application, so it's assumed the backend is already running during development. The backend is configured with hot-reload, so it does not need to be manually restarted for changes to take effect before testing.

When adding a new feature, new tests should be added to ensure the feature works as expected and that existing functionality is not broken. The tests should cover both success and error cases.