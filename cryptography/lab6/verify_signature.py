import hashlib
import rsa
import pprint
import re

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
print(_hash)


with open(FILE_NAME + '.sgn', 'rb') as inf:
    signature = inf.read()
#print(signature)

with open('private_key_1024.pem', 'rb') as inf:
    priv_key = rsa.PrivateKey.load_pkcs1(inf.read())

message = rsa.decrypt(signature, priv_key)
pprint.pprint(message)

_new_hash = re.findall('file hash: (.+)', message.decode('utf-8'))[0]

print(_hash == _new_hash)