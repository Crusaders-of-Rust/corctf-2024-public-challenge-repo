#!/usr/bin/python3
# Run: python3 gen.py > ops.inc

A = 0
B = 32
C = 64
D = 96

F = 128
tmp0 = 160
tmp1 = 192
tmp2 = 224

zero = 256
one = 288

K_start = 320
M = 2368

tmpbit0 = 2880
tmpbit1 = 2881

a0 = 4000
b0 = 4032
c0 = 4064
d0 = 4096
def emit_and(a, b, c):
  for p in range(0, 32):
    print(f"AND({a+p},{b+p},{c+p});")

def reverse(x):
  if x < 8:
    return x + 24
  if x < 16:
    return x + 8
  if x < 24:
    return x - 8
  return x - 24
def emit_add(a, b, c, tmp1, tmp2):
  for p in range(31, -1, -1):
    p = reverse(p)
    if p == 7:
      print(f"XOR({a+p},{b+p},{c+p});")
      print(f"AND({a+p},{b+p},{tmp1});")
    else:
      print(f"XOR({a+p},{b+p},{tmp2});")
      print(f"XOR({tmp2},{tmp1},{c+p});")
      print(f"AND({tmp2},{tmp1},{tmp1});")
      print(f"AND({a+p},{b+p},{tmp2});")
      print(f"OR({tmp2},{tmp1},{tmp1});")

def emit_set(a, val):
  for p in range(0, 32):
    print(f"SET({a+31-p}, {1 if (val & (1 << p)) != 0 else 0});")

def emit_or(a, b, c):
  for p in range(0, 32):
    print(f"OR({a+p},{b+p},{c+p});")

def emit_xor(a, b, c):
  for p in range(0, 32):
    print(f"XOR({a+p},{b+p},{c+p});")

def emit_not(a, c):
  emit_xor(a, one, c)

def emit_mov(a, c):
  emit_or(a, zero, c)

def emit_zero(c):
  emit_and(c, zero, c)

def emit_rotate(a, b, count):
  for p in range(0, 32):
    print(f"OR({a+reverse(p)},{zero+reverse(p)},{(b+reverse((32+p-count)%32))})")

s = [ 7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22 ,
     5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20 ,
     4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23 ,
     6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21 ]

emit_set(one, (1 << 32) - 1)

emit_set(a0, 0x0)
emit_set(b0, 0x0)
emit_set(c0, 0x0)
emit_set(d0, 0x0)

emit_mov(a0, A)
emit_mov(b0, B)
emit_mov(c0, C)
emit_mov(d0, D)

table = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 ]

def bswap(val):
  return ((((val) & 0xff000000) >> 24)|
            (((val) & 0x00ff0000) >>  8) |
                  (((val) & 0x0000ff00) <<  8) |
                        (((val) & 0x000000ff) << 24))

for i in range(0, 64):
  emit_set(K_start + 32 * i, bswap(table[i]));

for i in range(0, 64):
  g = 0
  if i < 16:
    emit_and(B, C, tmp0)
    emit_not(B, tmp1)
    emit_and(tmp1, D, tmp2)
    emit_or(tmp0, tmp2, F)
    g = i
  elif i < 32:
    emit_and(D, B, tmp0)
    emit_not(D, tmp1)
    emit_and(tmp1, C, tmp2)
    emit_or(tmp0, tmp2, F)
    g = (5 * i + 1) % 16
  elif i < 48:
    emit_xor(B, C, tmp0)
    emit_xor(tmp0, D, F)
    g = (3 * i + 5) % 16
  else:
    emit_not(D, tmp0)
    emit_or(tmp0, B, tmp1)
    emit_xor(C, tmp1, F)
    g = (7 * i) % 16

  emit_add(F, A, tmp0, tmpbit0, tmpbit1)
  emit_add(tmp0, M + 32 * g, tmp1, tmpbit0, tmpbit1)
  emit_add(tmp1, K_start + 32 * i, F, tmpbit0, tmpbit1)

  emit_mov(D, A)
  emit_mov(C, D)
  emit_mov(B, C)

  emit_rotate(F, tmp1, s[i])

  emit_add(tmp1, B, tmp2, tmpbit0, tmpbit1)
  emit_mov(tmp2, B);

emit_add(a0, A, tmp0, tmpbit0, tmpbit1)
emit_mov(tmp0, A)
emit_add(b0, B, tmp0, tmpbit0, tmpbit1)
emit_mov(tmp0, B)
emit_add(c0, C, tmp0, tmpbit0, tmpbit1)
emit_mov(tmp0, C)
emit_add(d0, D, tmp0, tmpbit0, tmpbit1)
emit_mov(tmp0, D)
