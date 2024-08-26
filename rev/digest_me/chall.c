#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define BINOP(op, src1, src2, dst) \
  asm volatile ( \
      "movb " #src1 "(%%rax), %%cl\n" \
      op #src2 "(%%rax), %%cl\n" \
      "movb %%cl, " #dst "(%%rax)\n" \
      :: "a"(heap) : "rcx", "memory", "cc");

#define OR(src1, src2, dst) BINOP("orb ", src1, src2, dst)
#define AND(src1, src2, dst) BINOP("andb ", src1, src2, dst)
#define XOR(src1, src2, dst) BINOP("xor ", src1, src2, dst)
#define SET(dst, val) asm volatile ( \
    "movb $" #val ", " #dst "(%%rax)\n" \
    :: "a"(heap) : "rcx", "memory");

#define CHECK 1

int main() {
  puts("Welcome!\nPlease enter the flag here: ");
  char* heap = calloc(1, 100000);
  const int M = 2368;

  if (0) {
try_again:
    puts("Try again: ");
  }

  char flag[1000] = { 0 };

  fgets(flag, sizeof(flag) - 1, stdin);
  size_t n = strcspn(flag, "\n");
  flag[n] = '\0';

  if (strncmp("corctf{", flag, 7) != 0 || n <= 1 || flag[n - 1] != '}') goto try_again;

  char* inner = flag + 7;

  // Flag is cPv3v8VfWbP

  // Search: 62 ^ 11 / 62 ^ 4 ~= 3.5 trillion

  if (CHECK && (inner[1] != inner[10] || inner[2] != inner[4] || inner[0] != inner[9] + 1 || inner[7] != inner[0] + 3)) {
    goto try_again;
  }

  for (int i = 0; i < 11; ++i) {
    if (CHECK && !isalnum(inner[i])) {
      goto try_again;
    }
    
   
    for (int j = 0; j < 8; ++j) {
      heap[M + 8 * i + j] = !!((inner[i]) & (1 << (7 - j)));
    }
  }

  unsigned long long length = 11;

  heap[M + length * 8] = 1;
  for (int j = 0; j < 64; ++j) {
    heap[M + 448 + j] = !!(__builtin_bswap64(length * 8) & (1ULL << (63 - j)));
  }

#include "ops.inc"

  uint32_t correct[4] = { 0x0, 0x0, 0x19c603ba, 0x14353ce4 };
  uint32_t hash[4] = { 0 };

  for (int i = 0; i < 128; i += 32) {
    for (int j = 0; j < 32; j++) {
      hash[i / 32] |= heap[i + j] * (1 << (31 - j));
    }
  }

  uint64_t lol = 14337776340792277733ULL;

  for (int i = 2; i < 4; ++i) {
    if (hash[i] != correct[i]) {
      goto try_again;
    }
  }

  puts("Nice!\n");

  char result[100] = { 0 };
  strcpy(result, "Full flag: corctf{        /           }");
  *(uint64_t*)&result[18] = lol ^ *(uint64_t*)hash;
  for (int i = 0; i < 11; ++i) {
    result[27 + i] = inner[i] + 1;
  }

  puts(result);
}
