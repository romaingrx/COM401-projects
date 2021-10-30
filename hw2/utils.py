#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Oct 30, 12:28:36
@last modified : 2021 Oct 30, 12:55:56
"""

import re, sys


def get_value_from_parameters(filename: str, key: str):
    with open(filename, "r") as fd:
        raw_text = fd.read()
    z = re.findall(fr"^\s*{key}\s*=\s*(.+)\s*$", raw_text, re.MULTILINE)
    if len(z) != 1:
        if len(z):
            print("Found several matches for key `{key}` : ", z, file=sys.stderr)
        return None
    return z[0].replace("'", '"')  # TODO: replace?


if __name__ == "__main__":
    import json

    value = get_value_from_parameters("345081-parameters.txt", "Q3_dict")
    print(json.loads(value))