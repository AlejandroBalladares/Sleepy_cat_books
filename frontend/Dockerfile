FROM node:lts-slim

WORKDIR /app

COPY package*.json /app/

RUN corepack enable && \
  corepack use pnpm@* && \
  pnpm install --frozen-lockfile

COPY ./ /app/

ENV PUBLIC_BACKEND_URL "http://sleepy-cat-books-backend:8080"

RUN pnpm run build

CMD [ "npm", "run", "preview", "--", "--host"]
