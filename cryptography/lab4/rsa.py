def euler(_p, _q):
    return (_p - 1)*(_q - 1)

def get_keys(p, q):
    eul = euler(p, q)
    n = p * q
    for i in range(3, eul):
      if i>1:
        for j in range(2,i):
            if(i % j==0):
                break
        else:

            if eul % i != 0:
                e = i
                break
    d = 1
    while True:
        if (d*e)%eul == 1:
            break
        else:
            d += 1
    return n, e, d


def encrypt(mes, e, n, info=False):
    ans = mes**e % n
    if info:
        print('Encrypting:')
        print(f'{mes}^{e} % {n} = {ans}\n')
    return ans


def decrypt(mes, d, n, info=False):
    ans = mes**d % n
    if info:
        print('Decrypting:')
        print(f'{mes}^{d} % {n} = {ans}\n')
    return ans


if __name__ == '__main__':
    message = 105
    p = 11
    q = 29

    n, e, d = get_keys(p, q)
    enc = encrypt(message, e, n)
    dec = decrypt(enc, d, n)

    print(f'Message: {message}\np={p} q={q} e={e}\n')
    print(f'n={n} phi={euler(p, q)} e={e} d={d}')
    print(f'Private key:{ {d, n}}\nPublic key: { {e, n}}')
    print(f'Encrypted message: {enc}')
    print(f'Decrypted message: {dec}')

    
