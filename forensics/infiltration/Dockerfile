FROM python:3.11-alpine AS base

FROM pwn.red/jail

COPY --from=base / /srv

COPY server.py /srv/app/run

RUN chmod +x /srv/app/run

ENV JAIL_TIME=30 JAIL_MEM=20M JAIL_CPU=200