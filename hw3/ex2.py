#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Dec 07, 11:40:12
@last modified : 2021 Dec 07, 16:31:27
"""

# RSA LSB Oracle attack
# https://gist.github.com/Chrstm/fe25e02c9620cf2e8e2c5854b96dc5dd

# Paillier LSB Oracle attack
# https://gist.github.com/73spica/0ff38748cdc07747857b4688ea5f1f6a

from utils import get_values_from_parameters, ask_oracle
from sage.all import *
import socket, subprocess

SCIPER = 345081
PARAMETERS_FILENAME = f"{SCIPER}-parameters.txt"

(n, g), c = get_values_from_parameters(PARAMETERS_FILENAME, ("Q2_pk", "Q2_c"))


def get_lsb(value):
    return int(
        subprocess.check_output(
            [
                "echo",
                str(SCIPER),
                str(value),
                "|",
                "ncat",
                "lasicpi1.epfl.ch",
                "5555",
            ],
            shell=True,
        )
    )


def get_lsb(value):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        sockfd.settimeout(2)
        sockfd.connect(("lasecpi1.epfl.ch", 5555))
        sockfd.send(f"{SCIPER} {value}\n".encode())
        recv_value = sockfd.recv(1).decode()
    return int(recv_value)


lb, ub = Integer(0), Integer(n)
cipher = c
i = 0
while True:
    try:
        lsb = get_lsb((cipher * cipher) % (n * n))
    except socket.timeout:
        input("Type any key to continue")
        continue
    except socket.gaierror:
        input("Type any key to continue")
        continue
    if lsb:
        lb = (lb + ub) / 2
    else:
        ub = (lb + ub) / 2
    diff = ub - lb
    if diff.numerator() / diff.denominator() == 0:
        m = ub
        break
    i += 1
    print(
        f"Current step : {i}",
        end="\r",
    )
    cipher = (cipher * cipher) % (n * n)
print(i)
print(m)
