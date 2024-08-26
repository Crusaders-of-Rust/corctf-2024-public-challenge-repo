from pwn import *
import time, base64
import subprocess

start = time.time()

flag = ''
#sh = process(['python3', 'wrong.py'])
sh = remote('be.ax', 32422)

sh.recvuntil(b'proof of work:\n')

pow_cmd = sh.recvline().decode().strip()
pow_res = subprocess.check_output(pow_cmd, shell=True).decode().strip()

sh.sendline(pow_res)

sh.recvuntil(b': ')
sh.sendline(b'0 -5 -10 -15 -20 -25 -31 -37')

anses = []
sh.recvuntil(b'flag: ')
f = sh.recvline().decode().strip()
print(f)

while True:
	sh.recvuntil(b'ments: ')
	s = sh.recvline().decode().strip()
	#print(s)
	split = [s[i:i+6] for i in range(0, len(s), 6)]
	#print(split)
	sh.recvuntil(b'res.')
	sh.recvline()
	sh.sendline()
	for sens in split[1:]:
		ans = b''
		if sens == '000000':
			pass
		elif sens[:3] == '000':
			ans += b'z ' + str(int(sens[3:], 2) - 1).encode()
		else:
			ans += b'x ' + str(int(sens[:3], 2) - 1).encode()
		ans += b';h r'
		for i in range(7):
			ans += b';cz r ' + str(i).encode()
		ans += b';h r'
		sh.sendline(ans)
	#sh.recvuntil(b'circuit: ')
	#sh.interactive()
	sh.recvuntil(b'byte: ')
	ans = sh.recvline().decode().strip()
	ans = '0' + ans[1:]
	anses.append(ans)
	flag += chr(int(ans, 2))
	print(flag)
	print(time.time() - start)
	print(anses)

