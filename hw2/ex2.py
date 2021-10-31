#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux (345081) & Thomas Benchetrit (284001)
@date : 2021 Oct 30, 12:21:25
@last modified : 2021 Oct 31, 21:30:39
"""
from sage.all import Mod, discrete_log
from utils import get_value_from_parameters

# Q2
param = "345081-parameters.txt"
p = get_value_from_parameters(param, "Q2_p")
q = get_value_from_parameters(param, "Q2_q")
g = Mod(get_value_from_parameters(param, "Q2_g"), p)
C = [Mod(get_value_from_parameters(param, f"Q2_c{k}"), p) for k in range(1, 10)]

mp = 1
for c in C:
    mp *= c
print(Mod(mp, p))

# 2.
m = Mod(get_value_from_parameters(param, "Q2_mdash"), p)
mx = discrete_log(m, g)
mi = list(str(bin(mx))[2:])
mi = len(list(filter(lambda x: x == "1", mi)))
mi = min(mi, 2 ** 32)
print(mx)
print(mi)
