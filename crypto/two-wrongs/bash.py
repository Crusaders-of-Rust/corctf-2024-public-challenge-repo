import binascii
from Crypto.Cipher import AES
enc = binascii.unhexlify('8c69af48e6d7003daa26a1d293c0ff1b358e995991887e9ee78af630c1d5de30')
b =['01110011', '01010010', '00010100', '01110001', '00001101', '00101010', '00101000', '01111011', '01010011', '01110011', '01111000', '00011011', '00010011', '01100101', '01000000', '00011001']
max_number = 2**16

for num in range(max_number):
	bins = format(num, '016b')
	key = b''
	for i in range(16):
		if bins[i] == '0':
			key += int(b[i], 2).to_bytes()
		else:
			cur_list = list(b[i])
			cur_list[0] = '1' if cur_list[0] == '0' else '0'
			key += int(''.join(cur_list), 2).to_bytes()
	cipher = AES.new(key, AES.MODE_ECB)
	dec = cipher.decrypt(enc)
	if b'cor' in dec:
		print('success', dec)