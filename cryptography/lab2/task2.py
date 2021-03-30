# Текст програми, що реалізує криптосистему XOR(двійкового гамування)
import random

ENCODING = "cp866"


def genereted_key(text):
    random.seed(len(text))
    key = ""
    for x in range(len(text)):
        key += chr(random.randint(20, 120))
    return key.encode(ENCODING)


def xor(text, key):
    result = ""
    for i, j in zip(text, key):
        result += chr(i ^ j)
    print("Encoded:    ", repr(result))


text = "verz"
#print("Text:   ", repr(text))

text_b = text.encode(ENCODING)
key = "poli".encode(ENCODING)
#print("generated:", genereted_key(text_b))
print("Key:  ", repr(key.decode(ENCODING)))
xor("verz", "poli")
