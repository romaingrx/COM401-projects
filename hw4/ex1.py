#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 26, 12:06:15
@last modified : 2021 Dec 27, 15:18:29
"""

import numpy as np
from utils import get_values_from_parameters, set_filename

SCIPER = 345081
FILENAME = f"{SCIPER}-params.txt"
set_filename(FILENAME)

Q1_ops = np.array(get_values_from_parameters("Q1_ops"))
n_sent = sum(Q1_ops == "send")
received_messages = Q1_ops[Q1_ops != "send"].astype(int)
MK_keys_in_cache = set(range(1, n_sent)) - set(received_messages)
print("Number of sent messages by Alice : ", n_sent)
print("Received messages by Bob : ", received_messages)

print(f"Alice keys in cache : RK_new, ga', x1, CK_{n_sent}")
print(
    f"Knowing CK_{n_sent}, we can only have next messages from i+1 to infinity (and beyond)"
)
print("Q1_a1={}")

# Bob can decrypt all messages, starting from CK_0 he can get all CK_i
print(
    f"Bob keys in cache : RK_new, ga', CK_{n_sent}, ",
    ", ".join([f"MK_{i}" for i in MK_keys_in_cache]),
)
print("Q1_b1=", MK_keys_in_cache)
