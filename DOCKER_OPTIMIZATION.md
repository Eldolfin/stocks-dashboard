# Docker Build Optimization

This project has been updated to use faster build tools for improved Docker performance:

## Backend: uv (Python Package Manager)

The backend now uses [uv](https://github.com/astral-sh/uv) instead of pip for faster Python package installation:

- **Dockerfiles updated**: `backend/Dockerfile.dev` and `backend/Dockerfile.prod`
- **Benefits**: Much faster dependency resolution and installation (10-100x faster than pip)
- **Fallback**: Automatically falls back to pip if uv fails (network issues, etc.)
- **Command execution**: Uses `uv run` for improved performance

### Changes Made:
```dockerfile
# Install uv for faster package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install dependencies with uv (fallback to pip on network issues)
RUN uv pip install --system . || pip install .

# Run commands with uv
CMD [ "uv", "run", "flask", "run", "--host=0.0.0.0", "--debug"]
```

## Frontend: Deno Runtime

The frontend now uses [Deno](https://deno.com/) instead of Node.js for improved performance and modern tooling:

- **Dockerfiles updated**: `frontend/Dockerfile.dev` and `frontend/Dockerfile.prod`
- **Command**: `just dev-docker`
- **Features**:
  - Uses official `denoland/deno:alpine` Docker image
  - Native TypeScript support without transpilation
  - Built-in package management with import maps
  - No node_modules directory needed

## Usage

```bash
# Development mode (optimized with uv and Deno)
just dev-docker

# Production build (uses optimized Deno + uv)
just restart-prod

# Linting (uses Deno-based tools)
just lint
```

## Performance Improvements

### Backend (Python)
- **uv**: 10-100x faster Python package installation compared to pip
- **Parallel dependency resolution**: Much faster than pip's sequential approach
- **Better caching**: More efficient package caching mechanisms
- **Fallback safety**: Graceful degradation to pip if uv is unavailable

### Frontend (Deno)
- **Native TypeScript**: No transpilation step needed, Deno runs TypeScript directly
- **Import maps**: Dependencies loaded from npm registry via import maps in deno.json
- **Simplified builds**: No node_modules, direct execution from source
- **Modern runtime**: Built-in web APIs, no polyfills needed

### Infrastructure
- **Improved caching**: Better Docker layer caching with optimized COPY commands
- **Graceful fallbacks**: All optimizations include fallback to standard tools
- **Network resilience**: Retry mechanisms and offline-first approaches

## Development Workflow

### For Backend Development:
1. Uses uv for fast dependency installation
2. Falls back to pip if network issues occur
3. Runtime commands use `uv run` for better performance

### For Frontend Development:
1. Uses Deno with native TypeScript support
2. Dependencies managed via import maps in deno.json
3. Commands run with `deno task` for consistency
4. No node_modules directory needed

## Backward Compatibility

All changes maintain full backward compatibility:
- Original `just dev-docker` command works as before (with optimizations)
- All existing deno task commands remain functional
- Graceful fallbacks ensure builds work even if new tools fail

## Measuring Performance

To measure the improvements:

```bash
# Time optimized build
time just dev-docker

# Compare with original pip-based approach (revert Dockerfiles to test)
```

Expected improvements:
- **Backend builds**: 50-90% faster dependency installation
- **Frontend builds**: Faster startup and no transpilation overhead
- **Overall**: More reliable builds with better caching