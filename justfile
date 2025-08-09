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

# Take screenshots of the running website
screenshot *args:
    #!/bin/bash
    echo "📸 Taking screenshots of the stocks dashboard..."
    # Ensure dev environment is running
    if ! curl -s --fail http://localhost:8085 > /dev/null 2>&1; then
        echo "🚀 Starting development environment..."
        just dev-docker &
        # Wait for services to be ready
        timeout=60
        while [ $timeout -gt 0 ] && ! curl -s --fail http://localhost:8085 > /dev/null 2>&1; do
            sleep 2
            ((timeout-=2))
        done
        if [ $timeout -le 0 ]; then
            echo "❌ Frontend failed to start"
            exit 1
        fi
    fi
    # Run the screenshot utility (use working TypeScript version in normal env, demo script in restricted env)
    if command -v npx >/dev/null 2>&1 && [ -f tests/node_modules/@playwright/test/package.json ]; then
        cd tests && npx tsx screenshot-utility.ts {{args}}
    else
        ./demo-screenshots.sh {{args}}
    fi

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
