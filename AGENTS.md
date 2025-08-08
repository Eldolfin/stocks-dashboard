# Agent Instructions

The project runs with hot reload enabled via Docker, so there's no need to manually start the server.

## Build/Lint/Test Commands

### Backend (Python/Flask)
- Lint: `just lint` (runs ruff check and mypy)
- Format: `just format` (runs ruff format)
- Test: `just test` (runs pytest with last-failed)
- Watch tests: `just watch-test`
- Single test: `uv run pytest tests/test_file.py::test_name`

### Frontend (Svelte/TypeScript)
- Lint: `npm run check` (runs svelte-check)
- Format: `npm run format` (runs prettier)
- Type check: `npm run test:ts` (runs tsc --noEmit)
- Dev server: `npm run dev`

### E2E Tests
- Run tests: `npx playwright test`
- Run with UI: `npx playwright test --ui`
- Update snapshots: `just update-snapshots`

## Code Style Guidelines

### Python
- Use ruff for linting and formatting
- Use mypy for type checking
- Follow PEP 8 naming conventions
- Use type hints for all function parameters and return types
- Use explicit error handling with try/except blocks

### TypeScript/Svelte
- Use ESLint with prettier for linting/formatting
- Use PascalCase for components, camelCase for variables/functions
- Use explicit typing with TypeScript
- Prefer composition over inheritance
- Use reactive declarations ($) for derived state

### General
- Use 4 spaces for indentation in Python, 2 spaces in TypeScript
- Keep functions small and focused
- Write clear, concise commit messages
- Use meaningful variable names
- Add comments for complex logic

## Special Instructions
- NEVER cancel long-running commands (Docker builds, tests, etc.) - set appropriate timeouts
- Always run `just lint` and `just test` before committing
- When Docker fails due to network restrictions, use local development with `cd frontend && npm run dev` and `cd backend && uv run python -m flask run`
- Fix the known ESLint issue in `frontend/src/routes/+page.svelte` about using `SvelteMap` instead of `Map`
