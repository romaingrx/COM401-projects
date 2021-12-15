#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 11:40:12
@last modified : 2021 Dec 09, 14:39:22
"""

# RSA LSB Oracle attack
# https://gist.github.com/Chrstm/fe25e02c9620cf2e8e2c5854b96dc5dd

# Paillier LSB Oracle attack
# https://gist.github.com/73spica/0ff38748cdc07747857b4688ea5f1f6a

from utils import get_values_from_parameters
from extended_euclidian_algorithm import extended_euclidian_algorithm

import os, random
from sage.all import power_mod
from fractions import Fraction
from math import floor, ceil, log2

SCIPER = 345081
PARAMETERS_FILENAME = f"{SCIPER}-parameters.txt"

(n, g), c = get_values_from_parameters(PARAMETERS_FILENAME, ("Q2_pk", "Q2_c"))


LSB = lambda value: int(
    os.popen(f"echo {SCIPER} {value} | nc lasecpi1.epfl.ch 5555").read()
)


def attack_paillier_lsb(c, decrypt_lsb, n, steps=None):
    bounds = [0, Fraction(n)]

    steps = steps or ceil(log2(n))
    for step in range(1, steps + 1):
        c = (c * c) % (n * n)
        lsb = decrypt_lsb(c)

        # if we have a bit for lsb, then set the lower bound as lb+ub/2, otherwise set it for the upper bound
        bounds[1 - lsb] = sum(bounds) / 2
        upper_bound, lower_bound = floor(bounds[1]), ceil(bounds[0])
        if lower_bound == upper_bound:
            return lower_bound

        print(f"Step {step}/{steps}", end="\r")

    print("\nThe message was not found")
    return bounds


UNIT_TEST = True
if UNIT_TEST:

    def random_unit_element(n):
        a = random.randint(1, n)
        gcd, u, v = extended_euclidian_algorithm(a, n)
        if gcd != 1:
            return random_unit_element(n)
        return a

    r = random_unit_element(n)  # The random value in Z_n^*
    message = 42  # The message
    c = (
        power_mod(g, message, n * n) * power_mod(r, n, n * n) % (n * n)
    )  # Encrypt message
    decrypted_message = attack_paillier_lsb(c, LSB, n)
    assert (
        decrypted_message == message
    ), f"decrypted message {decrypted_message} != message {message}"


m = attack_paillier_lsb(c, LSB, n)
print()
print(f"Q2_m={m}")
