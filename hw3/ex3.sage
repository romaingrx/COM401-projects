#!/usr/bin/env sage
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 10, 13:07:22
@last modified : 2021 Dec 10, 19:43:53
"""

import os, math, base64, socket
from sage.all import *
import random
from itertools import chain, combinations
from utils import get_values_from_parameters

SCIPER = 345081
PARAMETERS_FILENAME = f"{SCIPER}-parameters.txt"


# === FIRST PART ===
a, mu, l, N = get_values_from_parameters(
    PARAMETERS_FILENAME, ("Q3a_a", "Q3a_m", "Q3a_l", "Q3a_N")
)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_prime(t, l, s0, a, st):
    p = 0
    S = IntegerModRing(2 ** l)
    s = S(s0)
    for i in range(0, t + 1):
        p = (p << l) + int(s)
        s = a * s
    return p


def bit_extracted(number, k, p):
    return ((1 << k) - 1) & (number >> (p - 1))


def ex3_1(a, m, l, n):
    R = IntegerModRing(2 ** (2 * l))
    S = IntegerModRing(2 ** (l))

    n_mod = R(n)
    lmbd = 1024
    t = math.floor(lmbd / l) - 1

    su = R((2 ** (l + 1) + a))

    # Compute pl
    pl = R(a * n_mod / (su))
    F = factor(int(pl))
    for elem in list(powerset([x[0] for x in F]))[1:]:
        pl = int(pl)
        spt = prod(elem)
        assert pl % spt == 0
        sqt = pl / spt
        assert (spt * sqt) == pl
        sp0 = S(spt / (a ** t))
        sq0 = S(sqt / (a ** t))
        if int(sp0) | int(m) == int(sp0) and int(sq0) | int(m) == int(sq0):
            p = get_prime(t, l, sp0, a, spt)
            q = get_prime(t, l, sq0, a, sqt)
            assert p * q == n
            assert p in Primes() and q in Primes()
            assert p != q
            return p, q


# p, q = ex3_1(a, mu, l, N)
# print(f"Q3a_p={p}")
# print(f"Q3a_q={q}")


# === SECOND PART ===
e, N, C = get_values_from_parameters(
    PARAMETERS_FILENAME, ("Q3b_e", "Q3b_N", "Q3b_C"), cast=Integer
)

ask_oracle = lambda c: int(
    os.popen(f"echo {SCIPER} {hex(c)[2:]} | nc lasecpi1.epfl.ch 8888").read()
)


def ex3_2(e, n, c):
    R = IntegerModRing(n)
    u = n
    l = 0
    for i in range(1, n.nbits() + 1):
        new_c = R(c * ((2 ** i) ** e))
        lsb = ask_oracle(int(new_c))
        mid = (u + l) / 2
        if lsb == 0:
            u = mid
        else:
            l = mid
        print(f"Step {i}/{n.nbits()+1}", end="\r")

    for i in range(int(l), int(u) + 1):
        if int(R(i ** e)) == int(c):
            return i
    return -1


decrypted_message = ex3_2(e, N, C)
hex_message = hex(decrypted_message)[2:]
message = "".join(
    [chr(int(a + b, base=16)) for a, b in zip(hex_message[::2], hex_message[1::2])]
)
print("Message decrypted : ", repr(message))
print(f"Q3b_M={repr(base64.b64encode(bytes(message.encode('utf-8'))))}")

# === THIRD PART ===

e, n, C, l = get_values_from_parameters(
    PARAMETERS_FILENAME, ("e", "Q3c_N", "C", "Q3c_l"), cast=Integer
)
N = IntegerModRing(n)
C = N(C)

# Query the oracle
def ask_oracle(c):
    value = os.popen(f"echo {SCIPER} {hex(c)[2:]} | nc lasecpi1.epfl.ch 8889").read()
    return int(value) if value != "" else ask_oracle(c)


# Compute f
def f(x):
    return N(C * (N(x ** e)))


# Check wether x1>=x2 heuristically
def greater(x1, x2):
    return ask_oracle(f(N(x1 - x2))) == 1


def div_rem(x, y):
    x = N(x)
    y = N(y)

    # Find b
    b = 0
    while not greater(N(N(2) ** b * y), x):
        b = b + 1

    # Set the 2 bounds
    low = 0
    high = (2 ** b) % n

    # Binary search
    while low <= high:
        # mid
        q = (high + low) // 2

        # We found it
        if low + 1 == high:
            if greater(N(x), N(high * y)):
                return (high, x - high * y)
            else:
                return (low, x - low * y)

        if low == high:
            return (low, x - low * y)

        # If x>=yq
        if greater(N(x), N(y * q)):
            low = q
        else:
            high = q

    return (-1, -1)


def ex3_3_xgcd(x, y, zero=0):
    a, b, s, t, u, v = x, y, 1, 0, 0, 1
    while b != zero:
        q, r = div_rem(a, b)
        a, b = b, r
        s, t = s - q * u, t - q * v
        s, t, u, v = u, v, s, t
    return a, s, t


def ex3_3():
    while True:
        # Choose a and b at random
        a = random.randint(1, n)
        b = random.randint(1, n)
        while f(N(a)) == f(0) or f(N(b)) == f(0):
            a = random.randint(1, n)
            b = random.randint(1, n)

        aa, _, _ = ex3_3_xgcd(a, b)

        # If we found a such that f(a) = 1
        if f(aa) == 1:
            x = N(aa)
            m = 1 / x
            assert N(m ** e) == N(C)
            return m


decrypted_message = ex3_3()
hex_message = hex(decrypted_message)[2:]
message = "".join(
    [chr(int(a + b, base=16)) for a, b in zip(hex_message[::2], hex_message[1::2])]
)
print("Message decrypted : ", repr(message))
print(f"Q3c_M={repr(base64.b64encode(bytes(message.encode('utf-8'))))}")
