FROM node:lts-alpine AS builder
WORKDIR /app

COPY package*.json .
RUN npm install
COPY . .
RUN npm run prepare
RUN npm run test:ts && \
 npm run build

FROM node:lts-alpine AS runner

WORKDIR /app

COPY --from=builder /app/package*.json .
RUN npm ci --omit dev
COPY --from=builder /app/build/ build/

EXPOSE 3000

ENV NODE_ENV=production

CMD [ "node", "build/" ]
