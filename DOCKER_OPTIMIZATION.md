# Docker Build Optimization

This project has been updated to use faster build tools for improved Docker performance:

## Backend: uv (Python Package Manager)

The backend now uses [uv](https://github.com/astral-sh/uv) instead of pip for faster Python package installation:

- **Dockerfiles updated**: `backend/Dockerfile.dev` and `backend/Dockerfile.prod`
- **Benefits**: Much faster dependency resolution and installation
- **Fallback**: Automatically falls back to pip if uv fails (network issues, etc.)

## Frontend: Enhanced with Deno Support

The frontend provides two build options:

### Standard Build (Node.js)
- Uses improved npm configurations with caching optimizations
- `docker-compose.dev.yml` - Uses `Dockerfile.dev`
- Command: `just dev-docker`

### Deno-Enhanced Build
- Incorporates Deno for faster linting and type checking
- `docker-compose.deno-dev.yml` - Uses `Dockerfile.deno-dev`  
- Command: `just dev-docker-deno`
- Benefits: Faster TypeScript checking, built-in formatting tools

## Usage

```bash
# Standard development mode
just dev-docker

# Deno-enhanced development mode (faster linting/checking)
just dev-docker-deno

# Production build (uses optimized Node.js + uv)
just restart-prod
```

## Performance Improvements

- **uv**: 10-100x faster Python package installation compared to pip
- **Deno tooling**: Faster TypeScript checking and linting compared to npm tools
- **Improved caching**: Better Docker layer caching with optimized COPY commands
- **Fallback safety**: Graceful degradation to standard tools if faster ones fail