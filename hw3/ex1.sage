#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 10:11:51
@last modified : 2021 Dec 08, 11:48:29
"""

from utils import get_values_from_parameters
from sage.all import EllipticCurve, GF, GCD, power_mod
from tqdm import tqdm

PARAMETERS_FILENAME = "345081-parameters.txt"

# === FIRST PART ===

p, r, h = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_p", "Q1_r", "Q1_h"))
q = p ** h

assert GCD(r, q) == 1, "Assert that the order of G is coprime with the cardinality of the field ^ the embedding degree"

# Defining the elliptic curve on our function
E = EllipticCurve(GF(p), [1, 0])
R.<x> = GF(p)[]
K.<i> = GF(p ** 2, modulus=x ^ 2 + 1)
EK = E.base_extend(K)

# assert ((p + 1) / 4).is_integer(), "Should work since p is 3 modulo 4"
# I = power_mod(-1, (p + 1) // 4, p ** 2)

# Define the phi function
phi = lambda h: EK(-h[0], i * h[1])

def e_circ(g1:tuple, g2:tuple):
    """
    :param g1: the first point on the EC
    :param g2: the first point on the EC
    :return: the tate pairing ê function on the points p1 and p2
    """
    p1 = EK(g1)
    return p1.tate_pairing(phi(g2), p1.order(), h)


g = get_values_from_parameters(PARAMETERS_FILENAME, (f"Q1_g1", f"Q1_g2"))

def is_valid_SDH(index: int) -> bool:
    """
    :param index: the index of the 2 points gx_i and gz_i
    :return: true if the 2 points are a valid SDH pair
    """
    gx = get_values_from_parameters(PARAMETERS_FILENAME, (f"Q1_g1x{index}", f"Q1_g2x{index}"))
    gz = get_values_from_parameters(PARAMETERS_FILENAME, (f"Q1_g1z{index}", f"Q1_g2z{index}"))

    return e_circ(gx, gx) == e_circ(g, gz)


# print("Calculating the valid SDH pairs")
Q1_k = [i for i in tqdm(range(1, 21)) if is_valid_SDH(i)]
print("Q1_k=", Q1_k)

# === SECOND PART ===

q, x0, y0 = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_q", "Q1_x0", "Q1_y0"))

variables = x, y, A, B = var("x y A B")

equations = (
    x0 ** 3 + A * x0 + B - y0 ** 2,
    x ** 3 + A * x + B - y ** 2,
    (x + 1) ** 3 + A * (x + 1) + B - y ** 2,
    (x + 2) ** 3 + A * (x + 2) + B - y ** 2,
)

solutions = solve(equations, variables, solution_dict=True)

a = solutions[0][A]
b = (solutions[0][B]).mod(q)
j_invariant = 1728 * (4 * (a^3)) / (4 * (a^3) + 27 * (b^2))
j_num, j_den = j_invariant.numerator(), j_invariant.denominator()
g = gcd(j_num, j_den)

print("Q1_a=", j_num / g)
print("Q1_b=", j_den / g)