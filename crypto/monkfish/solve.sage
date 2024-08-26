#!/usr/bin/sage

from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from random import SystemRandom
from pwn import process

n = 112
m = 112
q = 5
FF.<x> = GF(q)


def apply(F, v):
    out = []
    for i in range(m):
        out.append((v.T * F[i] * v)[0, 0])
    return matrix(FF, m, 1, out)

def apply_verif_info(F, a, b):
    out = []
    for i in range(m):
        out.append((a.T * (F[i] + F[i].T) * b)[0, 0])
    return matrix(FF, m, 1, out)

def create_pok(v, s, F):
    t = matrix(FF, n, 1, [FF.random_element() for i in range(n)])
    com = apply(F, t)
    verif = apply_verif_info(F, t, s)
    a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
    return (com, t - a * s, verif)

def verif_pok(v, F, pi):
    com = pi[0]
    resp = pi[1]
    verif = pi[2]
    a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v) + list(verif)])).digest()[0] % len(list(FF))]
    out1 = apply(F, resp)
    out2 = com + (a * a) * v - a * verif
    return out1 == out2

output = False
io = None

com = None
resp = None
verify = None

while output != True:
    io = process("./server.sage")

    io.recvline()
    m0 = eval(io.recvline().decode('utf-8').split("=")[1])
    m1 = eval(io.recvline().decode('utf-8').split("=")[1])
    m2 = eval(io.recvline().decode('utf-8').split("=")[1])
    io.recvline()
    seed = eval(io.recvline().decode('utf-8').split("=")[1])
    v = matrix(FF, m, 1, [list(FF)[i] for i in eval(io.recvline().decode('utf-8').split("=")[1])])

    gen_seed = bytes(seed)

    F = []

    for i in range(m):
        cur = []
        for j in range(n):
            cur.append([])
            for k in range(n):
                cur[-1].append(list(FF)[sha256(gen_seed).digest()[0] % len(list(FF))])
                gen_seed = sha256(gen_seed).digest()
        F.append(matrix(FF, n, n, cur))


    # Forge proof (1/4 of the time)

    t = matrix(FF, n, 1, [FF.random_element() for i in range(n)])
    com = apply(F, t)
    # a = list(FF)[sha256(bytes([list(FF).index(i[0]) for i in list(com) + list(v)])).digest()[0] % len(list(FF))]
    a = FF('1')
    resp = matrix(FF, n, 1, [FF.random_element() for i in range(n)])

    fake_out = apply(F, resp)
    verif = ((com + (a * a) * v) - fake_out) * a.inverse()

    output = verif_pok(v, F, (com, resp, verif))

io.sendline(str([list(FF).index(i[0]) for i in list(com)]).encode())
io.sendline(str([list(FF).index(i[0]) for i in list(resp)]).encode())
io.sendline(str([list(FF).index(i[0]) for i in list(verif)]).encode())

io.interactive()
