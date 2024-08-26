FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y git \
    python3 \
    python3-pip \
    build-essential \
    tcl

RUN pip3 install Flask-SocketIO==4.3.1 \
    Flask==2.0.3 \
    python-engineio==3.13.2 \
    python-socketio==4.6.0 \
    Werkzeug==2.0.3

WORKDIR /app

RUN git clone https://github.com/sqlite/sqlite && \
    cd sqlite && \
    git checkout 66dacae4c3f818d0a9e94ecb4433c823a69a98aa && \
    ./configure && \
    make && \
    cp .libs/libsqlite3.so.0.8.6 /usr/lib/x86_64-linux-gnu/

COPY app.py .
COPY chat.db .
COPY flag.txt .
COPY templates/ ./templates/

RUN useradd -m ctf
RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 5000
CMD ["python3", "app.py"]
