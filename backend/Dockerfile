FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install setuptools \
    && pip3 install watchdog \
    && pip3 install gunicorn

COPY ./backend /backend
WORKDIR /backend

CMD printenv >> /etc/environment \
    && pip3.10 install -r requirements.txt \
    && gunicorn -w 1 --reload --bind 0.0.0.0:8080 --limit-request-line 1000000 'src.main:app'
