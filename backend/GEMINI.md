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

*   `src/app.py`: The main Flask application file. It initializes the app, database, and registers the API blueprints.
*   `src/auth.py`: Defines authentication-related endpoints.
*   `src/stocks.py`: Defines endpoints for retrieving stock data.
*   `src/models.py`: Defines Pydantic models for API request and response schemas.
*   `src/etoro_data.py`: Contains functions for processing eToro Excel statements.
*   `src/intervals.py`: Provides utility functions for time intervals.

## Database

The application uses a SQLite database. When running inside the Docker container, the database is located at `/database/database.db`. The database is initialized in `src/app.py`, and the schema is defined directly in the code.

## Development Workflow

*   **Linting:** `just lint`
*   **Formatting:** `just format`
*   **Testing:** `just test`
*   **CI:** `just ci` (never run this you don't need it)

Before committing, ensure that the code is properly linted and formatted by running `just lint` and `just format`. All tests should pass before pushing to the main branch.

## Testing

The project uses `pytest` for testing. The tests are located in the `tests/` directory and are separated into `test_auth.py` and `test_stocks.py`.

To run the tests, use the `just test` command. The tests make live requests to the application, so it's assumed the backend is already running during development. The backend is configured with hot-reload, so it does not need to be manually restarted for changes to take effect before testing.

When adding a new feature, new tests should be added to ensure the feature works as expected and that existing functionality is not broken. The tests should cover both success and error cases.
---
