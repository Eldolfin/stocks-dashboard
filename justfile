set dotenv-load := true
set dotenv-required := true

mod tests

help:
    just --list

dev-docker:
    #!/bin/sh
    set -xe

    cd dev
    docker compose                \
        -f docker-compose.yml     \
        -f docker-compose.dev.yml \
        down
    docker compose                \
        -f docker-compose.yml     \
        -f docker-compose.dev.yml \
        up -d --build
    echo 'You can now open the website at http://127.0.0.1:8085/'
    docker compose logs -f

dev-front:
    cd frontend && npm run dev

dev:
    kitty -e just dev-docker >/dev/null 2>&1 &
    kitty -e just dev-front >/dev/null 2>&1 &

restart-backend-docker:
    cd dev && docker compose up --build backend

build-push-images:
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-frontend:latest frontend
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-backend:latest -f backend/Dockerfile.prod backend
