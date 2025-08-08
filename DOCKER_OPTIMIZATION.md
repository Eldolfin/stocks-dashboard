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

## Frontend: Enhanced with Deno Support

The frontend provides two build options:

### Standard Build (Node.js Enhanced)
- Uses improved npm configurations with caching optimizations
- `docker-compose.dev.yml` - Uses `Dockerfile.dev`
- Command: `just dev-docker`
- Features:
  - `corepack enable` for better package manager performance
  - `npm ci --prefer-offline` for faster installs
  - Multi-stage builds for production

### Deno-Enhanced Build  
- Incorporates Deno for faster linting and type checking
- `docker-compose.deno-dev.yml` - Uses `Dockerfile.deno-dev`  
- Command: `just dev-docker-deno`
- Benefits: 
  - Faster TypeScript checking with built-in tools
  - No need for separate TypeScript compiler installation
  - Built-in formatting and linting tools

### Frontend Configuration Files Added:
- `frontend/deno.json` - Deno runtime and task configuration
- `frontend/import_map.json` - ES module import mapping
- `frontend/Dockerfile.deno-dev` - Multi-stage build with Deno tooling

## Usage

```bash
# Standard development mode (npm optimized)
just dev-docker

# Deno-enhanced development mode (faster linting/checking)
just dev-docker-deno

# Production build (uses optimized Node.js + uv)
just restart-prod

# Frontend-only deno tasks (when deno is available locally)
just frontend lint-deno      # Fast linting with deno
just frontend format-deno    # Fast formatting with deno
```

## Performance Improvements

### Backend (Python)
- **uv**: 10-100x faster Python package installation compared to pip
- **Parallel dependency resolution**: Much faster than pip's sequential approach
- **Better caching**: More efficient package caching mechanisms
- **Fallback safety**: Graceful degradation to pip if uv is unavailable

### Frontend (JavaScript/TypeScript)
- **Deno tooling**: Faster TypeScript checking and linting compared to npm tools
- **npm optimizations**: `--prefer-offline` flag for better caching
- **corepack**: Modern package manager with improved performance
- **Multi-stage builds**: Smaller production images with layer optimization

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
1. **Standard**: Enhanced npm with better caching
2. **Deno-enhanced**: Uses Deno for TypeScript tooling + npm for build process
3. Production builds use multi-stage optimization

## Backward Compatibility

All changes maintain full backward compatibility:
- Original `just dev-docker` command works as before (with optimizations)
- All existing npm scripts and commands remain functional
- Graceful fallbacks ensure builds work even if new tools fail

## Measuring Performance

To measure the improvements:

```bash
# Time standard build
time just dev-docker

# Time deno-enhanced build  
time just dev-docker-deno

# Compare with original pip-based approach (revert Dockerfiles to test)
```

Expected improvements:
- **Backend builds**: 50-90% faster dependency installation
- **Frontend builds**: 20-40% faster TypeScript checking and linting
- **Overall**: More reliable builds with better caching