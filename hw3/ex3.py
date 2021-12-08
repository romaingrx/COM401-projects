#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 17:20:06
@last modified : 2021 Dec 07, 17:45:09
"""

from utils import get_values_from_parameters
from sage.all import *
import random

SCIPER = 345081
PARAMETERS_FILENAME = f"{SCIPER}-parameters.txt"

alpha, mu, l = get_values_from_parameters(
    PARAMETERS_FILENAME, ("Q3a_a", "Q3a_m", "Q3a_l")
)


def get_prime(alpha, mu, l):
    # TODO: find lambda
    lamb = 117
    s = random.randint(0, 2 ** l - 1)
    p = 0
    while not is_prime(p):
        s |= mu
        p = Integer(0)
        for i in range(math.floor(lamb / l) - 1):
            p = p << l + s
            s = alpha * s % (2 ** l)
    return p


print(get_prime(alpha, mu, l))
