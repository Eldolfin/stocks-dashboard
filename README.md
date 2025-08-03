# Finance dashboard

using flask for the backend and svelte for the frontend.

## Preview
![Portfolio hover graph screenshot](./tests/tests/portfolio.spec.ts-snapshots/portfolio-hover-first-chromium-linux.png)

## Getting started

### Live version

available at [wsb.eldolfin.top](https://wsb.eldolfin.top/)

### Development

dependencies: just, docker, docker-compose, npm

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. Install them with:

```sh
pip install pre-commit
pre-commit install
```

The hooks will automatically run:
- **Backend**: `ruff check`, `ruff format`, and `mypy` on Python files
- **Frontend**: `svelte-check` and `prettier` on TypeScript/Svelte files
- **General**: trailing whitespace removal, end-of-file fixing, YAML validation

You can run hooks manually on all files:
```sh
pre-commit run --all-files
```

### Backend

```sh
just dev-docker
```

full deployment with reverse proxy at http://localhost:8085/

- backend hot reloads
- frontend does not

api doc at http://localhost:5000/openapi/

### Frontend

- start the backend with the command above

```sh
just dev-front
```

launches the front in dev-mode

- both backend and frontend hot reload now

front available at http://localhost:5173/

## TODO

see the
[V1 issue board](https://gitea.eldolfin.top/Eldolfin/finance-plots/projects/10)
