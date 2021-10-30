#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Sep 29, 11:47:38
@last modified : 2021 Oct 29, 14:02:40
"""

import numpy as np


def extended_euclidian_algorithm(a, b):
    """
    returns d, u, v such that d = au + bv = gcd(a, b)
    """
    x = np.array([a, 1, 0])
    y = np.array([b, 0, 1])

    while y[0] > 0:
        q = x[0] // y[0]
        x, y = y, x - q * y
    return x


if __name__ == "__main__":
    gcd, u, v = extended_euclidian_algorithm(69, 2)
    print(gcd, u, v)
