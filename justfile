set dotenv-load := true

mod tests
mod backend
mod frontend

generate-api-types:
	cd frontend && just generate-api-types

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
        up -d --build --wait
    echo 'You can now open the website at http://127.0.0.1:8085/'
    docker compose logs -f

dev:
    kitty -e just dev-docker >/dev/null 2>&1 &

build-push-images:
    # TODO: move to github
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-frontend:latest frontend
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-backend:latest -f backend/Dockerfile.prod backend
