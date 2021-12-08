#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 10:11:51
@last modified : 2021 Dec 07, 17:54:45
"""

from utils import get_values_from_parameters
from sage.all import *

PARAMETERS_FILENAME = "345081-parameters.txt"

p, r, h = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_p", "Q1_r", "Q1_h"))
G = get_values_from_parameters(PARAMETERS_FILENAME, ("Q1_g1", "Q1_g2"))

ec = EllipticCurve(GF(p), [1, 0])
K = GF(p ** 2)
