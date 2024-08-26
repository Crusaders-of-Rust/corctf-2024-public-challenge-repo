#!/bin/bash
cp * /tmp
cd /tmp

chmod 777 flag.txt

python3 chall-setup.py > /dev/null
chmod +x /tmp/boat
LD_PRELOAD="/tmp/libcrypto.so.3 /tmp/libc.so.6" /tmp/boat 1032 &
LD_PRELOAD="/tmp/libcrypto.so.3 /tmp/libc.so.6" /tmp/boat 1033 &
LD_PRELOAD="/tmp/libcrypto.so.3 /tmp/libc.so.6" /tmp/boat 1035 &
LD_PRELOAD="/tmp/libcrypto.so.3 /tmp/libc.so.6" /tmp/boat 1024 &
LD_PRELOAD="/tmp/libcrypto.so.3 /tmp/libc.so.6" /tmp/boat 1031
