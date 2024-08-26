FROM ubuntu:20.04 AS base

RUN apt-get update && apt-get -y install python3 python3-pip
RUN python3 -m pip install qiskit qiskit-aer pycryptodome

FROM pwn.red/jail

COPY --from=base / /srv

COPY flag.py /srv/app/

COPY wrong.py /srv/app/run

RUN chmod +x /srv/app/run

ENV JAIL_TIME=900 JAIL_MEM=100M JAIL_CPU=750 JAIL_TMP_SIZE=10M JAIL_POW=10000