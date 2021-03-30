#-*- coding: utf-8 -*-
import hashlib
from pathlib import Path
from datetime import datetime
import rsa

with open('private_key_1024.pem', 'rb') as inf:
    priv_key_pem = inf.read()
priv_key = rsa.PrivateKey.load_pkcs1(priv_key_pem)

with open('public_key_1024.pem', 'rb') as inf:
    public_key_pem = inf.read()
public_key = rsa.PublicKey.load_pkcs1(public_key_pem)

print (priv_key, '\n', public_key, '\n')

'''
BLOCK_SIZE = 2**20
FILE_NAME = 'zayava.docx'
raw_file = open(FILE_NAME, 'rb').read()

with open(FILE_NAME, 'rb') as inf:
    hash_obj = hashlib.sha1()
    while True:
        data = inf.read(BLOCK_SIZE)
        if not data:
            break
        hash_obj.update(data)

_hash = hash_obj.hexdigest()

#print(_hash)


date_str = datetime.now().date().isoformat()
file_size = Path(FILE_NAME).stat().st_size

metadata_to_encrypt = """file name: {0}
file size: {1}
sign date: {2}
file hash: {3}
""".format(FILE_NAME, file_size, date_str, _hash)
print(metadata_to_encrypt)


M = metadata_to_encrypt.encode('utf-8')
with open(FILE_NAME + '.sgn', 'wb') as outf:
    outf.write(rsa.encrypt(M, priv_key))

C = rsa.encrypt(M, priv_key)
print(C)
'''
