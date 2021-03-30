from rsa import encrypt, decrypt, get_keys, euler
def example1():
    print('--------Example 1--------')
    message = 72
    p = 11
    q = 17
    print(f'Message: {message}\np={p} q={q}\n')
    n, e, d = get_keys(p, q)
    enc = encrypt(message, e, n, 1)
    dec = decrypt(enc, d, n, 1)


    print(f'Private key:{ {d, n}}\nPublic key: { {e, n}}')
    print(f'Encrypted message: {enc}')
    print(f'Decrypted message: {dec}\n\n')


def example2():
    print('--------Example 2--------')
    message = 111111
    p = 3557
    q = 2579

    print(f'Message: {message}\np={p} q={q}\n')
    n, e, d = get_keys(p, q)
    enc = encrypt(message, e, n, 1)

    dec = decrypt(enc, d, n, 1)


    print(f'Private key:{ {d, n}}\nPublic key: { {e, n}}')
    print(f'Encrypted message: {enc}')
    print(f'Decrypted message: {dec}')


def my_encrypt(message, info=False):

    p = 11
    q = 29
    ascii_mess = [ord(x) for x in message]
    n, e, d = get_keys(p, q)

    if info:
        print('--------My encryption--------')
        print(f'Message: {message}\nASCII: {ascii_mess}\np={p} q={q}\n')
        print(f'n={n}\nphi={euler(p, q)}\ne={e}\nd={d}')
        print(f'Private key:{ {d, n}}\nPublic key: { {e, n}}\n')

    enc = []
    for letter in ascii_mess:
        enc.append(encrypt(letter, e, n))
        if info: print(f'Encrypted letter: {enc[-1]}')

    return enc

def my_decrypt(crypt_ascii_mess, d, n, info=False):
    if info:
        print('--------My decryption--------')
        print(f'Encrypted ASCII message: {crypt_ascii_mess}\n')

    dec = []
    for letter in crypt_ascii_mess:
        dec.append(decrypt(letter, d, n))
        if info: print(f'Decrypted letter: {dec[-1]}')

    res = ''.join([chr(c) for c in dec])

    if info: print(f'\nDecrypted ASCII message: {dec}')

    return res
