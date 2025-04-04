dev:
    cd dev && docker compose up -d --build && docker compose logs -f

build-push-images:
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-frontend:latest frontend
    docker build --push -t gitea.eldolfin.top/eldolfin/finance-plots-backend:latest -f backend/Dockerfile.prod backend
