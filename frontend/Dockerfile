FROM node:20 as build

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build:prod

FROM nginx:latest

COPY --from=build app/dist/frontend /usr/share/nginx/html
