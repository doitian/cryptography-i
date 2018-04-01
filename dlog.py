import gmpy2
from gmpy2 import mpz

B = 2 ** 20

def dlog(g, h, p):
    if h == 1:
        return mpz(0)

    ginverse = gmpy2.powmod(g, -1, p)

    left = h
    lookup_table = { h: 0 }
    for i in range(B):
        left = (left * ginverse) % p
        if left == 1:
            return i + 1
        lookup_table[left] = i + 1

    gb = gmpy2.powmod(g, B, p)
    gbpow = 1
    for x in range(B):
        gbpow = (gbpow * gb) % p
        x1 = lookup_table.get(gbpow)
        if x1 is not None:
            x0 = x + 1
            return (x0 * B + x1) % p

    return None

p = mpz('134078079299425970995740249982058461274793658205923933'
        '77723561443721764030073546976801874298166903427690031'
        '858186486050853753882811946569946433649006084171')

g = mpz('11717829880366207009516117596335367088558084999998952205'
        '59997945906392949973658374667057217647146031292859482967'
        '5428279466566527115212748467589894601965568')

h = mpz('323947510405045044356526437872806578864909752095244'
        '952783479245297198197614329255807385693795855318053'
        '2878928001494706097394108577585732452307673444020333')

r = dlog(g, h, p)
print(r)
print(gmpy2.powmod(g, r, p) == h)
