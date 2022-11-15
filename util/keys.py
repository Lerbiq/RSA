import random
import util.util as u


class Keys:

    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.euler = None
        self.e = None
        self.d = None

    def get_pub(self):
        return self.n, self.e

    def get_priv(self):
        return self.n, self.d

    def generate_keys(self, precision):
        k = precision
        while not u.isPrime(self.p, k):
            self.p = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

        while not u.isPrime(self.q, k):
            self.q = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

        self.n = self.p * self.q

        self.euler = (self.p - 1) * (self.q - 1)

        self.e = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)
        while not u.isPrime(self.e, k) and u.gcd(self.e, self.euler) != 1:
            self.e = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

        self.d = pow(self.e, -1, self.euler)
