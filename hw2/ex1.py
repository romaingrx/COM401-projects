#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux (345081) & Thomas Benchetrit (284001)
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Oct 31, 21:30:39
"""

import ast
import string
import base64
import hashlib
import numpy as np
from utils import get_value_from_parameters

param = "345081-parameters.txt"
A = string.printable


def inverse(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_s


def encrypt(K, plaintext):
    a, b = K
    x = [f(x) for x in list(plaintext)]
    y = [(a * c + b) % n for c in x]
    ciphertext = "".join([g(c) for c in y])
    return ciphertext


def decrypt(K, ciphertext):
    a, b = K
    new_a = inverse(a, n)
    return encrypt((new_a, -b * new_a), ciphertext)


def checksum(*args):
    data = ";".join(map(str, args)).encode()
    return hashlib.new("sha256", data=data).hexdigest()


f = lambda x: A.index(x)
g = lambda x: A[x]
n = len(A)

# 1.
K = get_value_from_parameters(param, "Q1a_K")
s = get_value_from_parameters(param, "Q1a_M")
base64_ciphertext = base64.b64decode(s).decode("utf-8")
encr_s = encrypt(K, base64_ciphertext)
def_s = base64.b64encode(encr_s.encode(encoding="utf-8"))
print(f"Q1a_K={repr(def_s)}")

# 2.
K = get_value_from_parameters(param, "Q1b_K")
s = get_value_from_parameters(param, "Q1b_C")
base64_ciphertext = base64.b64decode(s).decode("utf-8")
decr_s = decrypt(K, str(base64_ciphertext))
print(f"Q1b_M={repr(decr_s)}")

# 3.
T = get_value_from_parameters(param, "Q1c_T")
s = get_value_from_parameters(param, "Q1c_C")
base64_ciphertext = base64.b64decode(s).decode()

# Will contain the probability of each character in the base64 ciphertext
empirical_probabilities = {}
for i in range(len(base64_ciphertext)):
    char = base64_ciphertext[i]
    if char in empirical_probabilities:
        empirical_probabilities[char] += 1
    else:
        empirical_probabilities[char] = 1

empirical_probabilities = {
    k: v / len(base64_ciphertext) for k, v in empirical_probabilities.items()
}
matching_char_dict = {}
for key1, prob1 in T.items():
    for key2, prob2 in empirical_probabilities.items():
        if prob1 == prob2:
            print(f"{repr(key1)} -> {repr(key2)}\t with probability {prob1:.5f}")
            matching_char_dict[key1] = key2

print("The system to resolve is as follow in order to find K(k0, k1):")
for key1, key2 in matching_char_dict.items():
    print(f"\t({f(key1)}*k0 + k1) mod {100} = {f(key2)} mod {n}")

# From this we get that ' ' -> '\x0c', 'o' -> '9', 't' -> ' '
# By resolving the overdetermined linear system ([3x2][2x1]=[3x1]),
K = (17, 101)
text = decrypt(K, base64_ciphertext)
print(f"Q1c_M={repr(text)}")
print(f"Q1c_K={repr(K)}")

# H = get_value_from_parameters(param, "Q1c_H")
# assert checksum(base64.b64encode(text.encode()).decode(), K[0], K[1]) == H
