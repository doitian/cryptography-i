from __future__ import print_function
from itertools import chain
import requests

def query_guess(cipher, guess, padding_mask):
    query = "".join(
            "%02x" % (c ^ g ^ m)
            for (c, g, m) in zip(cipher, guess, padding_mask)
            )
    r = requests.get('http://crypto-class.appspot.com/po', params={'er': query})
    return r.status_code


cipher = bytearray.fromhex('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4')
guess = bytearray(b'\0' * len(cipher))
padding_mask = bytearray(b'\0' * len(cipher))

plain_blocks = []
last_pos = len(cipher) - 16 - 1
padding_len = 0

padding_mask[last_pos] = 1
for ch in range(0, 16):
    guess[last_pos] = ch
    response = query_guess(cipher, guess, padding_mask)
    if response == 404 or (response == 200 and ch != 1):
        padding_len = ch
        for i in range(0, ch):
            guess[last_pos - i] = ch
        break

# resolve padding
current_last_pos = last_pos

# padding_len = 16

for i in range(padding_len, last_pos + 1):
    if i > 0 and (i % 16) == 0:
        current_last_pos = current_last_pos - 16
        plain_blocks.append(repr(bytes(guess[-32:-16])))
        cipher = cipher[0:-16]
        guess = bytearray(b'\0' * len(cipher))
        padding_mask = bytearray(b'\0' * len(cipher))

    for rpos in range(0, (i % 16) + 1):
        padding_mask[current_last_pos - rpos] = (i % 16) + 1

    # guess i-th char backward
    pos = last_pos - i
    print("Guess " + str(pos))
    for ch in chain(range(97, 123), range(65, 97), range(32, 65), range(123, 127)):
        guess[pos] = ch
        response = query_guess(cipher, guess, padding_mask)
        if response == 404 or (response == 200 and i > 0):
            print(repr(chr(ch)))
            print(repr(bytes(guess[0:-16])))
            break


plain_blocks.reverse()
print(" ".join(plain_blocks))
