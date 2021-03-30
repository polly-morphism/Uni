import random

# from math import pow

a = random.randint(2, 10)


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# Generating large random numbers
def gen_key(p, g, x):
    return pow(g, x, p)


# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c


def decrypt(a, b, q, p):
    return (a ** (p - 1 - q) * b) % p


msg = 1903
p = 3581
g = 3  # alpha
x = 1669  # a
k = 1721

print("Original Message :", msg)
print("p = {}, g = {}, x = {}, k = {}".format(p, g, x, k))
print("Generating Key")

key = gen_key(p, g, x)
print("key", key)

a = gen_key(p, g, k)
b = ((key ** k) * msg) % p

print("a, b", a, b)
print("decrypted: ", decrypt(a, b, x, p))
