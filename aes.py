import sys
from Crypto.Cipher import AES

mode = sys.argv[1]
key = bytes.fromhex(sys.argv[2])
iv_cipher = bytes.fromhex(sys.argv[3])

iv = iv_cipher[:16]
cipher = iv_cipher[16:]
n_blocks = len(cipher) / 16

def decrypt(key, data):
    cryptor = AES.new(key, AES.MODE_CBC, b'\0' * 16)
    return cryptor.decrypt(data)

def encrypt(key, data):
    cryptor = AES.new(key, AES.MODE_CBC, b'\0' * 16)
    return cryptor.encrypt(data)

def xor_bytes(a, b):
    return bytes(l ^ r for (l, r) in zip(a, b))

plain_blocks = []
if mode == "cbc":
    prev_cipher_block = iv
    for pos in range(0, len(cipher), 16):
        cipher_block = cipher[pos:pos+16]
        decrypted = decrypt(key, cipher_block)
        plain_block = xor_bytes(prev_cipher_block, decrypted)
        plain_blocks.append(plain_block)
        prev_cipher_block = cipher_block
    plain_blocks[-1] = plain_blocks[-1][:-plain_blocks[-1][-1]]
else:
    counter = int.from_bytes(iv, 'big')
    for pos in range(0, len(cipher), 16):
        cipher_block = cipher[pos:pos+16]
        expand_key = encrypt(key, counter.to_bytes(16, 'big'))
        plain_block = xor_bytes(cipher_block, expand_key)
        plain_blocks.append(plain_block)
        counter += 1

# unpadding
print(b''.join(plain_blocks))
