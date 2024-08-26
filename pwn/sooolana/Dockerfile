FROM ubuntu:24.04 AS base

FROM pwn.red/jail

COPY --from=base / /srv

COPY rust_src/out/challenge /srv/app/challenge

COPY flag.txt /srv/app/flag.txt
COPY run.sh /srv/app/run
RUN chmod +x /srv/app/run
ENV JAIL_TIME=600 JAIL_CPU=500 JAIL_MEM=50M
