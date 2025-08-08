set dotenv-load := true

mod tests
mod backend
mod frontend

help:
    just --list

dev-docker:
    just _dc-dev down
    just _dc-dev up -d --build --wait
    echo 'You can now open the website at {{BOLD}}{{GREEN}}http://localhost:8085/'
    just _dc-dev logs -f

lint:
    just backend lint
    just frontend lint

# Generate demo materials and run comprehensive E2E test
demo:
    ./generate-demo-materials.sh
    echo "To run the full demo test:"
    echo "1. Start dev environment: just dev-docker"
    echo "2. Run test: cd tests && just demo"

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
