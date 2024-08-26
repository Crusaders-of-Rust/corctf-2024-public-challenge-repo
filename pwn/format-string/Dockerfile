FROM ubuntu:20.04 AS base

FROM pwn.red/jail

COPY --from=base / /srv

COPY chal /srv/app/run

COPY flag.txt /srv/app/flag.txt

RUN chmod +x /srv/app/run

ENV JAIL_TIME=600 JAIL_CPU=500 JAIL_MEM=50M