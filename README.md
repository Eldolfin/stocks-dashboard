# Finance dashboard

using flask for the backend and svelte for the frontend.

## Getting started

### Live version

available at [wsb.eldolfin.top](https://wsb.eldolfin.top/)

### Development

dependencies: just, docker, docker-compose, npm

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
