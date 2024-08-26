FROM sagemath/sagemath:latest AS base
RUN sage --pip install pycryptodome
FROM pwn.red/jail
COPY --from=base / /srv
COPY --chmod=755 run.sh /srv/app/run
COPY server.sage /srv/app/server.sage
COPY flag.txt /srv/app/
ENV JAIL_TIME=1800 JAIL_PIDS=20 JAIL_MEM=1G JAIL_CPU=1000 JAIL_TMP_SIZE=1M JAIL_ENV_HOME=/tmp