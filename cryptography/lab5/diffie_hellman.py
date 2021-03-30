class DiffieHellman:
    """ Class to represent the Diffie-Hellman key exchange protocol """

    # Current minimum recommendation is 2048 bit.
    def __init__(self, p, g, a):
        self.p = p
        self.g = g
        self.__a = a

    def get_private_key(self):
        """ Return the private key (a) """
        return self.__a

    def gen_public_key(self):
        """ Return A, A = g ^ a mod p """
        # calculate G^a mod p
        A = pow(self.g, self.__a, self.p)
        print("public key = g ^ a mod p =", A)
        return A

    def gen_shared_key(self, other_contribution, sha=0):
        """ Return g ^ ab mod p """
        self.shared_key = pow(other_contribution, self.__a, self.p)
        print("shared key = g ^ ab mod p =", self.shared_key)
        if sha:
            return hashlib.sha256(str(self.shared_key).encode()).hexdigest()
        else:
            return self.shared_key


g = 5
p = 23
a = 6
b = 15

print("g = 5, p = 23, a = 6, b = 15")

Alice = DiffieHellman(p, g, a)
Bob = DiffieHellman(p, g, b)

print("Generate public key for Alice")
A = Alice.gen_public_key()

print("Generate public key for Bob")
B = Bob.gen_public_key()

print("A =", A, "B =", B)

print("Generate shared key for Bob")
bob_sharedkey = Bob.gen_shared_key(A)

print("Generate shared key for Alice")
alice_sharedkey = Alice.gen_shared_key(B)
