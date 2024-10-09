FROM node:16-alpine

WORKDIR /app

RUN apk add --no-cache git bash curl

COPY package*.json ./
COPY server.js ./
COPY update_repo.sh ./
RUN chmod +x update_repo.sh

RUN npm install

EXPOSE 3000

RUN echo "* * * * * /app/update_repo.sh >> /root/cron.log 2>&1" | crontab -

CMD ["sh", "-c", "crond && npm start"]
