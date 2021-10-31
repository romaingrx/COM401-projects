#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux (345081) & Thomas Benchetrit (284001)
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Oct 31, 21:38:59
"""

import re
import json
import numpy as np
from itertools import product
from sage.all import Mod, power_mod
from utils import get_value_from_parameters
from tqdm.contrib.concurrent import process_map
from extended_euclidian_algorithm import extended_euclidian_algorithm

parameters_filename = "345081-parameters.txt"

p = get_value_from_parameters(parameters_filename, "Q3_p")
g = get_value_from_parameters(parameters_filename, "Q3_g")
q = get_value_from_parameters(parameters_filename, "Q3_q")
u = get_value_from_parameters(parameters_filename, "Q3_u")
cipher_text = get_value_from_parameters(parameters_filename, "Q3_ct")
mapping_dict = get_value_from_parameters(parameters_filename, "Q3_dict")
hashed_public_key = get_value_from_parameters(parameters_filename, "Q3_H")

# List of all possible pairs (pi, pj)
possibilities = np.array(list(product(mapping_dict.values(), mapping_dict.values())))

# Define multiplication in a group
def mul(a, b, m):
    return Mod(a * b, m)


# Define the modular inverse
def inv(a, m):
    d, u, _ = extended_euclidian_algorithm(a, m)
    if d != 1:
        return None
    return u


# Return true if pair (p1, p2) correspond to the first two characters of the cipher regarding this equation:
# $\dfrac{R_1^u}{R_2} = \dfrac{p_1^u}{p_2}$
def is_matching(pair):
    p1, p2 = pair
    R1, R2 = cipher_text[0][1], cipher_text[1][1]
    return mul(power_mod(R1, u, p), inv(R2, p), p) == mul(
        power_mod(p1, u, p), inv(p2, p), p
    )


# Get the pair that corresponds to the 2 first characters in the cipher
matches = np.array(process_map(is_matching, possibilities))
[[p1, p2]] = possibilities[matches]


# Return the whole text based on the first character because we can use:
# $p_{i+1}=\dfrac{p_i^u\, C_{i+1}}{C_i^u}$
def get_text_with_first_guess(p1):
    inv_mapping_dict = dict(
        zip(mapping_dict.values(), mapping_dict.keys())
    )  # Get the dict from value to character
    text = inv_mapping_dict[p1]  # Get the first char as the beginning of the text
    pi = p1
    for i in range(len(cipher_text) - 1):
        [[Ri, Ci], [Rj, Cj]] = cipher_text[i : i + 2]
        # Get the next character value from the formula
        pj = mul(mul(power_mod(pi, u, p), Cj, p), inv(power_mod(Ci, u, p), p), p)
        text += inv_mapping_dict[pj]
        pi = pj
    return text


print("Generate all text")
text = get_text_with_first_guess(p1)
print(f"Q3_pt={repr(text)}")
