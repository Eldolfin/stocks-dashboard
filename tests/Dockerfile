FROM denoland/deno:alpine

# Install required tools for Playwright
USER root
RUN apk add --no-cache nodejs

WORKDIR /tests

# Copy deno configuration
COPY deno.json .

# Install Playwright browsers
RUN deno run -A npm:playwright install chromium

COPY playwright.config.ts .
COPY data/ data/

CMD ["deno", "task", "test"]
