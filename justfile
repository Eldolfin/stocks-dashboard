set dotenv-load := true

mod tests
mod backend
mod frontend

help:
    just --list

dev-docker:
    just _dc-dev down
    just _dc-dev up -d --build --wait
    echo 'You can now open the website at http://localhost:8085/'
    just _dc-dev logs -f

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
