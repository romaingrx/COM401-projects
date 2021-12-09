#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 10:11:51
@last modified : 2021 Dec 08, 13:50:47
"""

from utils import get_values_from_parameters
from sage.all import EllipticCurve, GF

PARAMETERS_FILENAME = "345081-parameters.txt"

p, r, h = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_p", "Q1_r", "Q1_h"))
g = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_g1", "Q1_g2"))
g1x1, g2x1 = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_g1x1", "Q1_g2x1"))

ec = EllipticCurve(GF(p), [1, 0])
K = GF(p ** 2)
