FROM python:3.9

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /root/repo

WORKDIR /app

COPY spa_server.py ./
COPY update_repo.sh ./
RUN chmod +x update_repo.sh

EXPOSE 3000

RUN echo "* * * * * /app/update_repo.sh >> /root/cron.log 2>&1" | crontab -

CMD ["sh", "-c", "cd /root && /app/update_repo.sh && cron && cd /app && python3 spa_server.py"]
