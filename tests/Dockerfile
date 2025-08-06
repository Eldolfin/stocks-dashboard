FROM mcr.microsoft.com/playwright:v1.54.2-noble

WORKDIR /tests

COPY package*.json .
RUN npm i

COPY playwright.config.ts .
COPY data/ data/


CMD ["npx", "-y", "playwright", "test"]
