#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Oct 30, 22:49:19
"""

import re
import json
import numpy as np
from sage.all import *
from itertools import product
from utils import get_value_from_parameters
from tqdm.contrib.concurrent import process_map
from extended_euclidian_algorithm import extended_euclidian_algorithm

parameters_filename = "345081-parameters.txt"

p = Integer(get_value_from_parameters(parameters_filename, "Q3_p"))
g = Integer(get_value_from_parameters(parameters_filename, "Q3_g"))
q = Integer(get_value_from_parameters(parameters_filename, "Q3_q"))
mapping_dict = json.loads(get_value_from_parameters(parameters_filename, "Q3_dict"))
hashed_public_key = bytes(
    get_value_from_parameters(parameters_filename, "Q3_H")[2:-1].encode("ASCII")
)
u = Integer(get_value_from_parameters(parameters_filename, "Q3_u"))
cipher_text = [
    (Integer(Ri), Integer(Ci))
    for Ri, Ci in re.findall(
        "\((\w+), (\w+)\)", get_value_from_parameters(parameters_filename, "Q3_ct")
    )
]

mod = p
possibilities = np.array(list(product(mapping_dict.values(), mapping_dict.values())))


def mul(a, b, m):
    return Mod((a * b), m)


def inv(a, m):
    d, u, v = extended_euclidian_algorithm(a, m)
    if d != 1:
        return None
    return u


def is_matching(pair):
    p1, p2 = pair
    c1, c2 = cipher_text[0][1], cipher_text[1][1]
    return mul(power_mod(c1, u, mod), inv(c2, mod), mod) == mul(
        power_mod(p1, u, mod), inv(p2, mod), mod
    )


matches = np.array(process_map(is_matching, possibilities))
[[p1, p2]] = possibilities[matches]


def get_text_with_first_guess(p1):
    inv_mapping_dict = dict(zip(mapping_dict.values(), mapping_dict.keys()))
    text = inv_mapping_dict[p1]
    pi = p1
    # for i, ((Ri, Ci), (Rj, Cj)) in enumerate(zip(cipher_text[:-1], cipher_text[-1:])):
    for i in range(len(cipher_text) - 1):
        Ci = cipher_text[i][1]
        Cj = cipher_text[i + 1][1]
        pj = mul(
            mul(power_mod(pi, u, mod), Cj, mod), inv(power_mod(Ci, u, mod), mod), mod
        )
        text += inv_mapping_dict[pj]
        pi = pj
    return text


raw_text = get_text_with_first_guess(p1)
print(raw_text)
