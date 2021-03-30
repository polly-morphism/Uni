import hashlib

#print(hashlib.algorithms_available)

#print(hashlib.algorithms_guaranteed)

'''
hash_obj = hashlib.sha1(b'Hello, world!')
print(hash_obj.hexdigest())

hash_obj = hashlib.sha1(b'abc')
print(hash_obj.hexdigest())

hash_obj = hashlib.sha224(b'abc')
print(hash_obj.hexdigest())

hash_obj = hashlib.sha512(b'abc')
print(hash_obj.hexdigest())


hash_obj = hashlib.sha1(b'The quick brown fox jumps over the lazy dog')
print(hash_obj.hexdigest())

hash_obj = hashlib.sha1(b'The quick brown fox jumps over the lazy cog')
print(hash_obj.hexdigest())

hash_obj = hashlib.sha1(b'')
print(hash_obj.hexdigest())
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
print(_hash)
