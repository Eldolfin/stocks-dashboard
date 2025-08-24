set dotenv-load := true
export MY_UID := `id -u`
export MY_GID := `id -g`

mod tests
mod backend
mod frontend

help:
    just --list

docker-down:
    just _dc-dev down

dev-docker:
    echo 'Starting at {{BOLD}}{{GREEN}}http://localhost:8085/'
    just _dc-dev up --watch --build

lint:
    just backend lint
    just frontend lint

# Pull from upstream and restart with new version
restart-prod:
    git pull
    just _dc-prod up -d --build --wait

_dc-dev *args:
    #!/bin/sh
    cd dev
    docker compose                \
        -f docker-compose.yml     \
        -f docker-compose.dev.yml \
        {{args}}

_dc-prod *args:
    #!/bin/sh
    cd dev
    docker compose                \
        -f docker-compose.yml     \
        {{args}}

build-android: frontend::install
    cargo tauri android build

dev-android: frontend::install
    cargo tauri android dev

# Removes all built files
[confirm("Are you sure you want to delete everything?")]
clean:
    rm -rf                  \
    ./frontend/node_modules \
    ./frontend/.svelte-kit  \
    ./backend/.venv         \
    ./data-collector/target \
    ./app/target
