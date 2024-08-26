from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from binascii import hexlify
import random

with open("flag.txt", "rb") as f:
    FLAG = f.read()

os.unlink("flag.txt")

boats = [1024, 1032, 1031, 1033, 1035]
num_boats = len(boats)

def get_random_ascii(l):
    return "".join([chr(random.randint(0x41, 0x5a)) for x in range(l)])

def generate_aes_key_iv():
    key = get_random_ascii(32)  # 256-bit key for AES-256
    iv = get_random_ascii(16)   # 128-bit IV for AES
    return bytes(key, encoding='utf-8'), bytes(iv, encoding='utf-8')

def encrypt(data, key, iv):
    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the data
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext, key, iv):
    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return data

def split_string(string, num_parts):
    part_length = len(string) // num_parts
    return [string[i*part_length:(i+1)*part_length] for i in range(num_parts-1)] + [string[(num_parts-1)*part_length:]]

def main():
    #custom_string = input("Enter the string to encrypt: ").encode()
    parts = split_string(FLAG, num_boats)

    # Generate four different keys and IVs
    keys_ivs = [generate_aes_key_iv() for _ in range(num_boats)]

    ciphertexts = []

    # Encrypt each part of the custom string with each key and IV
    for i, (part, (key, iv)) in enumerate(zip(parts, keys_ivs)):
        ciphertext = encrypt(part, key, iv)
        ciphertexts.append(ciphertext)
        with open(f"{boats[i]}.key", "wb") as f:
            f.write(key)
        with open(f"{boats[i]}.iv", "wb") as g:
            g.write(iv)
        print(f"Encryption {i+1}:")
        print(f"Part: {part.decode(errors='ignore')}")
        print(f"Key: {key.hex()}")
        print(f"IV: {iv.hex()}")
        print(f"Ciphertext: {ciphertext.hex()}\n")

    # Concatenate the ciphertexts
    concatenated_ciphertext = b''.join(ciphertexts)
    print(f"{[hexlify(x) for x in ciphertexts]}")
    print(f"Concatenated Ciphertext: {concatenated_ciphertext.hex()}\n")
    
    with open("flag.enc", "w") as f:
        f.write(concatenated_ciphertext.hex())
    

    # Decrypt each part from the concatenated ciphertext
    decrypted_parts = []
    start = 0
    for i, (ciphertext, (key, iv)) in enumerate(zip(ciphertexts, keys_ivs)):
        end = start + len(ciphertext)
        decrypted_part = decrypt(concatenated_ciphertext[start:end], key, iv)
        decrypted_parts.append(decrypted_part)
        start = end
        print(f"Decryption {i+1}:")
        print(f"Ciphertext: {ciphertext.hex()}")
        print(f"Decrypted Part: {decrypted_part.decode(errors='ignore')}\n")

    decrypted_string = b''.join(decrypted_parts)
    print(f"Decrypted string: {decrypted_string.decode()}")

if __name__ == "__main__":
    main()

