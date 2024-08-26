FROM ubuntu:20.04 AS base

RUN apt-get update && apt-get -y install python3 python3-pip

RUN rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install cryptography

FROM pwn.red/jail

COPY --from=base / /srv

COPY release/run.sh /srv/app/run

RUN chmod +x /srv/app/run

COPY release/flag.txt /srv/app/

COPY release/chall-setup.py /srv/app/

COPY release/boat /srv/app/

COPY release/libcrypto.so.3 /srv/app/

COPY release/libc.so.6 /srv/app/

COPY release/proper-ld.so /srv/app

ENV JAIL_TIME=6000 JAIL_CPU=500 JAIL_MEM=50M JAIL_TMP_SIZE=20M JAIL_PIDS=15
