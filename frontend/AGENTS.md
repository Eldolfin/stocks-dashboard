# Agent Instructions

The project runs with hot reload enabled via Docker, so there's no need to manually start the server.

## Build/Lint/Test Commands

### Frontend (Svelte/TypeScript)

- Lint: `npm run check` (runs svelte-check)
- Format: `npm run format` (runs prettier)
- Type check: `npm run test:ts` (runs tsc --noEmit)
- Generate API types: `npm run generate-api-types`

### Running Single Tests

- Use `npm run test:ts` for TypeScript type checking

## Code Style Guidelines

### TypeScript/Svelte

- Use ESLint with prettier for linting/formatting
- Use PascalCase for components, camelCase for variables/functions
- Use explicit typing with TypeScript
- Prefer composition over inheritance
- Use reactive declarations ($) for derived state
- Use typed open api client @src/generated/api.d.ts for API interactions

### General

- Use 2 spaces for indentation in TypeScript
- Keep functions small and focused
- Write clear, concise commit messages
- Use meaningful variable names
- Add comments for complex logic

### Imports

- Use absolute imports with $lib when possible
- Group imports logically (external, then internal)
- Use type-only imports (`import type`) for types

### Error Handling

- Use try/catch blocks for async operations
- Handle API errors gracefully with user feedback
- Log errors appropriately for debugging

### Naming Conventions

- Components: PascalCase
- Variables/Functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case
