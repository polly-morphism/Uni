from tasks import *

if __name__ == '__main__':
    print('RSA crypting\n')
    # example1()
    # example2() # it counts around 83 secs, be ready
    print('Encrypted message: ', my_encrypt(message='sikorsky',
                                            info=True),'\n\n')
    print('Decrypted message: ', my_decrypt(crypt_ascii_mess = [202, 293, 83, 78, 108, 202, 83, 154],
                                            d=187, n=319,
                                            info=True), '\n\n')
