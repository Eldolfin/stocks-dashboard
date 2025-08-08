# Stocks Dashboard (Finance Dashboard)

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

This is a full-stack finance dashboard application using Flask backend (Python) and Svelte frontend (TypeScript). The project uses Docker for development with `just` as the task runner.

## Critical Setup Requirements

### Required Tools
- **just** - Task runner (install: `wget -qO- 'https://github.com/casey/just/releases/download/1.42.4/just-1.42.4-x86_64-unknown-linux-musl.tar.gz' | tar -xzf- && sudo mv just /usr/local/bin/`)
- **Docker & docker-compose** - For full development environment
- **npm** - For frontend development (usually pre-installed)
- **uv** - Python package manager for backend (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Environment Setup
Always start by copying the environment file:
```bash
cp .env.example .env
```

## Working Effectively

### Primary Development Approach (Docker)
**NEVER CANCEL these commands - Docker builds can take 3-15 minutes:**

```bash
just dev-docker
```
- **Expected time**: 3-15 minutes for first build, 30 seconds for subsequent starts
- **NEVER CANCEL**: Set timeout to 20+ minutes for initial build
- **NEVER CANCEL**: Set timeout to 5+ minutes for subsequent starts
- Opens full application at http://localhost:8085/
- Backend API available at http://localhost:5000/
- OpenAPI docs at http://localhost:5000/openapi/

**Known Issue**: In network-restricted environments, Docker builds may fail with SSL certificate errors. Use alternative local development approach below.

### Alternative Local Development (Network-Restricted Environments)

When Docker fails due to network restrictions, develop components separately:

#### Frontend Development
```bash
cd frontend
npm install          # Takes ~45 seconds. NEVER CANCEL. Set timeout to 5+ minutes
npm run dev          # Starts dev server at http://localhost:3000/
```

#### Backend Development  
```bash
cd backend
uv sync              # Install dependencies - Takes 1-3 minutes. NEVER CANCEL
uv run python -m flask run --debug --host=0.0.0.0  # Starts at http://localhost:5000/
```

### Linting and Quality Checks
**NEVER CANCEL these commands - Allow 30+ seconds each:**

#### All Components
```bash
just lint            # Runs both backend and frontend linting. Takes ~30 seconds
```

#### Frontend Only  
```bash
cd frontend
npm run lint         # Takes ~10 seconds. Checks ESLint + Prettier
npm run check        # Takes ~15 seconds. Type checking with svelte-check  
npm run test:ts      # Takes ~5 seconds. TypeScript compilation check
```

#### Backend Only
```bash
cd backend
just lint            # Runs ruff + mypy. Takes ~10 seconds
just format          # Auto-format with ruff. Takes ~5 seconds
```

### Testing
**NEVER CANCEL these commands - Tests can take 2-10 minutes:**

#### Backend Tests
```bash
cd backend
just test            # Runs pytest. Takes 30 seconds - 2 minutes. NEVER CANCEL
just watch-test      # Continuous testing. NEVER CANCEL
```

#### E2E Tests (Playwright)
```bash
cd tests
npm install          # Takes ~5 seconds. NEVER CANCEL
just tests ci        # Full E2E test suite. Takes 2-10 minutes. NEVER CANCEL. Set timeout to 15+ minutes
npx playwright test --ui  # Interactive test runner
```

### Building
**NEVER CANCEL these commands - Builds can take 15-60 seconds:**

#### Frontend Build
```bash
cd frontend
npm run build        # Takes ~20 seconds. NEVER CANCEL. Set timeout to 2+ minutes
```

#### Production Docker Build
```bash
just restart-prod    # Takes 2-5 minutes. NEVER CANCEL. Set timeout to 10+ minutes
```

## Validation Scenarios

**Always test these scenarios after making changes:**

### Basic Functionality Test
1. Start development environment: `just dev-docker`
2. Open http://localhost:8085/ in browser
3. Verify login page loads
4. Test stock ticker search functionality
5. Verify portfolio dashboard displays correctly

### API Validation
1. Access http://localhost:5000/openapi/ for API documentation
2. Test GET /api/stocks/search endpoint
3. Verify authentication endpoints work

### Frontend Validation  
1. Check responsive design on mobile/desktop
2. Test chart interactions (zoom, pan, hover)
3. Verify navigation between pages works
4. Test form submissions

## Build and Test Timing Expectations

**Set these timeout values and NEVER CANCEL:**

| Command | Expected Time | Recommended Timeout |
|---------|--------------|-------------------|
| `just dev-docker` (first) | 3-15 minutes | 20+ minutes |
| `just dev-docker` (subsequent) | 30 seconds | 5+ minutes |
| `npm install` (frontend) | 45 seconds | 5+ minutes |
| `npm run build` | 20 seconds | 2+ minutes |
| `npm run lint` | 10 seconds | 30+ seconds |
| `npm run check` | 15 seconds | 30+ seconds |
| `just backend test` | 30 seconds - 2 minutes | 5+ minutes |
| `just tests ci` | 2-10 minutes | 15+ minutes |
| `just restart-prod` | 2-5 minutes | 10+ minutes |

## Repository Structure

### Key Directories
- `backend/` - Flask API (Python 3.13, uv package manager)
- `frontend/` - Svelte app (TypeScript, npm)  
- `tests/` - E2E tests (Playwright)
- `dev/` - Docker compose configurations
- `.github/workflows/` - CI/CD pipelines

### Important Files
- `justfile` - Main task runner configuration
- `backend/justfile` - Backend-specific tasks
- `frontend/justfile` - Frontend-specific tasks
- `tests/justfile` - Test-specific tasks
- `backend/pyproject.toml` - Python dependencies
- `frontend/package.json` - Node.js dependencies

### Common File Locations
- Backend source: `backend/src/`
- Frontend components: `frontend/src/lib/components/`
- Frontend pages: `frontend/src/routes/`
- Test specs: `tests/tests/`
- API types: `frontend/src/generated/api.d.ts`

## Debugging and Troubleshooting

### Docker Issues
If `just dev-docker` fails with SSL/network errors:
- Use local development approach
- Check Docker logs: `docker compose -f dev/docker-compose.yml logs`
- Try rebuilding: `docker compose -f dev/docker-compose.yml down && docker system prune -f`

### Backend Issues
- Check Flask logs in Docker container
- Use `uv run python -c "import flask; print(flask.__version__)"` to verify setup
- Backend API should be accessible at http://localhost:5000/

### Frontend Issues  
- Check browser console for errors
- Verify API endpoints are reachable
- Use `npm run dev` for hot reload during development

### Test Failures
- Run single test: `cd tests && npx playwright test tests/specific-test.spec.ts`
- Update snapshots: `cd tests && just update-snapshots`
- Check test artifacts in `tests/playwright-report/`

## CI/CD Requirements

**Always run these before committing:**

```bash
just lint            # Must pass - runs ruff, mypy, ESLint, prettier
npm run format       # Auto-fix formatting issues  
just backend test    # Backend tests must pass
```

The CI pipeline runs:
1. Linting checks (both backend and frontend)
2. Backend pytest suite
3. E2E Playwright tests

**Known Linting Issue**: There may be 1 ESLint error in `frontend/src/routes/+page.svelte` about using `SvelteMap` instead of `Map`. This should be fixed before committing.

## Network-Restricted Environment Workarounds

If you encounter SSL certificate or network issues:

1. **For Docker builds**: Use local development instead of `just dev-docker`
2. **For package installation**: May require manual dependency management
3. **For testing**: Focus on unit tests rather than full integration tests
4. **For validation**: Test individual components rather than full stack

Document any network restrictions as "does not work in restricted environments" rather than trying workarounds that may compromise security.