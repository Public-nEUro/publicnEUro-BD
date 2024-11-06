FROM node:20 AS build

ARG ENVIRONMENT

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build -- --configuration $ENVIRONMENT

FROM nginx:latest

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build app/dist/frontend /usr/share/nginx/html
