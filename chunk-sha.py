import sys
from Crypto.Hash import SHA256

CHUNK_SIZE = 1024


def sha256(chunk, next_digest = None):
    h = SHA256.new()
    h.update(chunk)
    if next_digest is not None:
        h.update(next_digest)
    return h.digest()

def hash_file(path):
    digest = None
    with open(sys.argv[1], 'rb') as f:
        f.seek(0, 2)
        fn = f.tell()
        remainder = fn % CHUNK_SIZE

        if remainder > 0:
            fn -= remainder
            f.seek(fn)
            digest = sha256(f.read(remainder))

        while fn > 0:
            fn -= CHUNK_SIZE
            f.seek(fn)
            digest = sha256(f.read(CHUNK_SIZE), digest)

    return digest


print(hash_file(sys.argv[1]).hex())
