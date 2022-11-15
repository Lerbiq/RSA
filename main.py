import random
import time

import util

if __name__ == '__main__':
    start = time.time()
    k = 6
    p = 4
    q = 4
    while not util.isPrime(p, k):
        p = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

    while not util.isPrime(q, k):
        q = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

    end = time.time()

    print("Took " + str(end-start) + " seconds")
    print("Keys: " + str(p) + " , " + str(q))
    print("Lengths: " + str(len(str(p))) + " , " + str(len(str(q))))

    n = p * q

    print("N: " + str(n))

    euler = (p-1)*(q-1)

    print("Euler: " + str(euler))

    e = 4

    while not util.isPrime(e, k) and util.gcd(e, euler) != 1:
        e = random.randint(1 * pow(10, 20), 1 * pow(10, 21) - 1)

    print("E: " + str(e))

    d = pow(e, -1, euler)
    print("D: " + str(d))

    pub = (n, e)
    priv = (n, d)
    print("Pub: " + str(pub))
    print("Priv: " + str(priv))
