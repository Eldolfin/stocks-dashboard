set dotenv-load := true

mod tests
mod backend
mod frontend

help:
    just --list

generate-api-types:
	cd frontend && just generate-api-types

_docker-compose-dev *args:
    #!/bin/sh
    cd dev
    docker compose                \
        -f docker-compose.yml     \
        -f docker-compose.dev.yml \
        {{args}}

_docker-compose-prod *args:
    #!/bin/sh
    cd dev
    docker compose                \
        -f docker-compose.yml     \
        {{args}}


dev-docker:
    just _docker-compose-dev down
    just _docker-compose-dev up -d --build --wait
    echo 'You can now open the website at {{BOLD}}{{GREEN}}http://localhost:8085/'
    just _docker-compose-dev logs -f

dev:
    kitty -e just dev-docker >/dev/null 2>&1 &

build-push-images:
    # TODO: move to github
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-frontend:latest frontend
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-backend:latest -f backend/Dockerfile.prod backend

lint:
    just backend lint
    just frontend lint

prod:
    git pull
    cd dev && docker compose up -d --build --wait
