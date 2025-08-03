FROM node:lts-alpine AS builder
WORKDIR /app

COPY package*.json .
RUN npm install
RUN npm run prepare
COPY . .
RUN npm run build

FROM node:lts-alpine AS runner

WORKDIR /app

RUN apk add --no-cache curl

COPY --from=builder /app/package*.json .
RUN npm ci --omit dev
COPY --from=builder /app/build/ build/

EXPOSE 3000

ENV NODE_ENV=production

CMD [ "node", "build/" ]

HEALTHCHECK CMD curl -f -o /dev/null http://localhost:3000
