import random
import re

from unidecode import unidecode

def mod_exp(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def millerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = mod_exp(a, d, n)

    if x == 1 or x == n - 1:
        return True

    while d != n-1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n-1:
            return True

    return False


def isPrime(n, k):
    if n is None:
        return False
    if k is None:
        raise Exception("The k precision parameter must be an integer. None was provided.")
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for i in range(k):
        if not millerTest(d, n):
            return False

    return True


def gcd(a, b):
    if a < 1 | b < 1:
        raise Exception("Číslo a nebo b je menší než 1")
    while b != 0:
        temp = a
        a = b
        b = temp % b
    return a


def capitalize(match):
    return match.group().capitalize()


def normalize_text(text):
    text = unidecode(text)
    return text


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
