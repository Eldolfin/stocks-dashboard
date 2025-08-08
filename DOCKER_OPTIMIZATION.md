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

## Frontend: Enhanced Node.js Build

The frontend uses optimized Node.js configurations for improved performance:

- **Dockerfiles updated**: `frontend/Dockerfile.dev` and `frontend/Dockerfile.prod`
- **Command**: `just dev-docker`
- **Features**:
  - `corepack enable` for better package manager performance
  - `npm ci --prefer-offline` for faster installs with better caching
  - Multi-stage builds for production with layer optimization

## Usage

```bash
# Development mode (optimized with uv and enhanced npm)
just dev-docker

# Production build (uses optimized Node.js + uv)
just restart-prod

# Linting (uses existing npm-based tools)
just lint
```

## Performance Improvements

### Backend (Python)
- **uv**: 10-100x faster Python package installation compared to pip
- **Parallel dependency resolution**: Much faster than pip's sequential approach
- **Better caching**: More efficient package caching mechanisms
- **Fallback safety**: Graceful degradation to pip if uv is unavailable

### Frontend (JavaScript/TypeScript)
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
1. Enhanced npm with better caching and `corepack enable`
2. Uses `npm ci --prefer-offline` for faster, more reliable installs
3. Production builds use multi-stage optimization

## Backward Compatibility

All changes maintain full backward compatibility:
- Original `just dev-docker` command works as before (with optimizations)
- All existing npm scripts and commands remain functional
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
- **Overall**: More reliable builds with better caching